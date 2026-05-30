import hashlib
import os
import time
import uuid
import wave
from pathlib import Path
from threading import Event
from typing import Dict, Optional, Tuple

TTS_CACHE_DIR = Path(__file__).parent / "tts_cache"
TTS_CACHE_DIR.mkdir(exist_ok=True)

TTS_CACHE: Dict[str, Dict] = {}
CACHE_TTL = 3600 * 24 * 7


class TTSError(Exception):
    pass


def mask_secret(value: str) -> str:
    if not value:
        return "<EMPTY>"
    if len(value) <= 10:
        return "***"
    return value[:6] + "***" + value[-4:]


def generate_tts_cache_key(text: str, voice_type: str, file_ext: str, sample_rate: int) -> str:
    raw = f"{text}:{voice_type}:{file_ext}:{sample_rate}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()


def get_cached_tts(cache_key: str) -> Optional[str]:
    if cache_key in TTS_CACHE:
        entry = TTS_CACHE[cache_key]
        if time.time() - entry["timestamp"] < CACHE_TTL:
            if os.path.exists(entry["file_path"]):
                return entry["file_path"]
            del TTS_CACHE[cache_key]
    return None


def cache_tts(cache_key: str, file_path: str):
    TTS_CACHE[cache_key] = {"file_path": file_path, "timestamp": time.time()}


def get_tts_provider() -> str:
    return (os.getenv("TTS_PROVIDER", "aliyun").strip() or "aliyun").lower()


def _ensure_dashscope():
    try:
        import dashscope
        from dashscope.audio.qwen_tts_realtime import AudioFormat, QwenTtsRealtime, QwenTtsRealtimeCallback
    except ImportError as e:
        raise TTSError("未安装 dashscope 依赖，请先安装 requirements.txt 中的 dashscope") from e
    return dashscope, AudioFormat, QwenTtsRealtime, QwenTtsRealtimeCallback


def _pcm_to_wav_bytes(pcm_bytes: bytes, sample_rate: int) -> bytes:
    import io

    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(pcm_bytes)
    return buffer.getvalue()


def synthesize_aliyun_tts_realtime(text: str, voice_type_override: Optional[str] = None) -> Tuple[bytes, str]:
    if not text or not text.strip():
        raise TTSError("TTS 文本不能为空")

    dashscope, AudioFormat, QwenTtsRealtime, QwenTtsRealtimeCallback = _ensure_dashscope()

    api_key = os.getenv("DASHSCOPE_API_KEY", "").strip()
    model = os.getenv("ALIYUN_TTS_MODEL", "qwen-tts-realtime").strip() or "qwen-tts-realtime"
    voice = (voice_type_override or os.getenv("ALIYUN_TTS_VOICE", "Cherry")).strip() or "Cherry"
    sample_rate = int(os.getenv("ALIYUN_TTS_SAMPLE_RATE", "24000"))
    mode = os.getenv("ALIYUN_TTS_MODE", "server_commit").strip() or "server_commit"

    if not api_key:
        raise TTSError("DASHSCOPE_API_KEY 未配置，请在 .env 中填写阿里云 DashScope API Key")

    dashscope.api_key = api_key

    class RealtimeCallback(QwenTtsRealtimeCallback):
        def __init__(self):
            self.complete_event = Event()
            self.audio_buffer = bytearray()
            self.session_id = ""
            self.error_message = ""

        def on_open(self) -> None:
            print("[Aliyun TTS] connection opened")

        def on_close(self, close_status_code, close_msg) -> None:
            print(f"[Aliyun TTS] connection closed: code={close_status_code}, msg={close_msg}")

        def on_event(self, response: dict) -> None:
            try:
                event_type = response.get("type")
                if event_type == "session.created":
                    self.session_id = response.get("session", {}).get("id", "")
                    print(f"[Aliyun TTS] session created: {self.session_id}")
                elif event_type == "response.audio.delta":
                    import base64
                    recv_audio_b64 = response.get("delta", "")
                    if recv_audio_b64:
                        self.audio_buffer.extend(base64.b64decode(recv_audio_b64))
                elif event_type == "response.done":
                    print("[Aliyun TTS] response done")
                elif event_type == "session.finished":
                    print("[Aliyun TTS] session finished")
                    self.complete_event.set()
                elif event_type == "error":
                    self.error_message = str(response)
                    self.complete_event.set()
            except Exception as e:
                self.error_message = f"Aliyun TTS 事件处理失败: {e}"
                self.complete_event.set()

        def wait_for_finished(self, timeout_seconds: int = 60):
            finished = self.complete_event.wait(timeout_seconds)
            if not finished:
                self.error_message = "Aliyun TTS 等待超时"

    callback = RealtimeCallback()
    client = None
    try:
        print("[Aliyun TTS] model:", model)
        print("[Aliyun TTS] voice:", voice)
        print("[Aliyun TTS] sample_rate:", sample_rate)
        print("[Aliyun TTS] api_key:", mask_secret(api_key))

        client = QwenTtsRealtime(model=model, callback=callback)
        client.connect()
        client.update_session(
            voice=voice,
            response_format=AudioFormat.PCM_24000HZ_MONO_16BIT,
            mode=mode,
        )
        client.append_text(text)
        client.finish()
        callback.wait_for_finished()

        if callback.error_message:
            raise TTSError(f"阿里云语音合成失败：{callback.error_message}")

        pcm_audio = bytes(callback.audio_buffer)
        if not pcm_audio:
            raise TTSError("阿里云语音合成未返回音频数据")

        wav_audio = _pcm_to_wav_bytes(pcm_audio, sample_rate)
        return wav_audio, "wav"
    except TTSError:
        raise
    except Exception as e:
        raise TTSError(f"阿里云语音合成请求失败：{e}") from e
    finally:
        if client is not None:
            try:
                client.close()
            except Exception:
                pass


def synthesize_speech(text: str, speaker_config: Optional[Dict] = None, voice_type: Optional[str] = None) -> Optional[str]:
    file_path, _ = synthesize_speech_with_detail(text, speaker_config, voice_type)
    return file_path


def synthesize_speech_with_detail(
    text: str,
    speaker_config: Optional[Dict] = None,
    voice_type: Optional[str] = None,
) -> Tuple[Optional[str], str]:
    provider = get_tts_provider()
    if provider != "aliyun":
        return None, f"当前仅启用 aliyun TTS，收到未支持 provider={provider}"

    selected_voice = (voice_type or os.getenv("ALIYUN_TTS_VOICE", "Cherry")).strip() or "Cherry"
    sample_rate = int(os.getenv("ALIYUN_TTS_SAMPLE_RATE", "24000"))
    file_ext = "wav"
    cache_key = generate_tts_cache_key(text, selected_voice, file_ext, sample_rate)

    cached = get_cached_tts(cache_key)
    if cached:
        return cached, "cache-hit"

    try:
        audio, actual_ext = synthesize_aliyun_tts_realtime(text, voice_type_override=selected_voice)
        file_path = str(TTS_CACHE_DIR / f"{cache_key}.{actual_ext}")
        with open(file_path, "wb") as f:
            f.write(audio)
        cache_tts(cache_key, file_path)
        return file_path, "ok-aliyun"
    except Exception as e:
        return None, str(e)


def preflight_tts() -> Dict:
    provider = get_tts_provider()
    voice_type = os.getenv("ALIYUN_TTS_VOICE", "Cherry").strip() or "Cherry"
    model = os.getenv("ALIYUN_TTS_MODEL", "qwen-tts-realtime").strip() or "qwen-tts-realtime"
    sample_rate = int(os.getenv("ALIYUN_TTS_SAMPLE_RATE", "24000"))
    try:
        audio, file_ext = synthesize_aliyun_tts_realtime("你好，这是一次阿里云语音合成预检。", voice_type_override=voice_type)
        return {
            "success": True,
            "provider": provider,
            "mode": "realtime-sdk",
            "model": model,
            "voiceType": voice_type,
            "format": file_ext,
            "sampleRate": sample_rate,
            "audioBytes": len(audio),
        }
    except Exception as e:
        return {
            "success": False,
            "provider": provider,
            "mode": "realtime-sdk",
            "error": str(e),
            "hint": "请检查 DASHSCOPE_API_KEY、阿里云模型权限、voice 配置以及 dashscope 依赖是否已安装。",
        }


def get_tts_cache_stats() -> Dict:
    total_size = 0
    for entry in TTS_CACHE.values():
        file_path = entry.get("file_path")
        if file_path and os.path.exists(file_path):
            total_size += os.path.getsize(file_path)
    return {"cache_size": len(TTS_CACHE), "total_bytes": total_size, "cache_dir": str(TTS_CACHE_DIR)}


def clear_tts_cache():
    for entry in TTS_CACHE.values():
        file_path = entry.get("file_path")
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass
    TTS_CACHE.clear()
    for file in TTS_CACHE_DIR.glob("*.*"):
        try:
            file.unlink()
        except Exception:
            pass
    return {"message": "语音缓存已清除"}
