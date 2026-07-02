import os

tts_path = r"e:\LEAR-CODE-NEW\软件工程\my-keshe\innovation-competition-platform\backend\services\tts_service.py"

with open(tts_path, 'r', encoding='utf-8') as f:
    old_content = f.read()

# I will write the complete new content.
new_content = """import hashlib
import os
import time
import uuid
import wave
import base64
import asyncio
import threading
from pathlib import Path
from threading import Event
from queue import Queue, Empty
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


def normalize_tts_provider(value: str) -> str:
    provider = (value or "").strip().lower()
    if provider in {"qianwen", "aliyun"}:
        return "qianwen"
    if provider == "doubao":
        return "doubao"
    raise TTSError(f"不支持的 TTS_PROVIDER={provider}，可选值：qianwen、doubao")


def get_tts_provider() -> str:
    return normalize_tts_provider(os.getenv("TTS_PROVIDER", "qianwen"))


def generate_tts_cache_key(text: str, voice_type: str, file_ext: str, sample_rate: int) -> str:
    provider = get_tts_provider()
    if provider == "qianwen":
        model_name = os.getenv("ALIYUN_TTS_MODEL", "qwen-tts-realtime").strip() or "qwen-tts-realtime"
    else:
        model_name = os.getenv("DOUBAO_TTS_RESOURCE_ID", "seed-tts-2.0").strip() or "seed-tts-2.0"
        
    raw = f"{provider}:{model_name}:{voice_type}:{text}:{file_ext}:{sample_rate}"
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


class AliyunTTSStreamingSession:
    def __init__(self, voice_type=None, sample_rate=24000):
        self.dashscope, self.AudioFormat, self.QwenTtsRealtime, self.QwenTtsRealtimeCallback = _ensure_dashscope()
        self.api_key = os.getenv("DASHSCOPE_API_KEY", "").strip() or os.getenv("ALIYUN_API_KEY", "").strip()
        self.model = os.getenv("ALIYUN_TTS_MODEL", "qwen-tts-realtime").strip() or "qwen-tts-realtime"
        self.voice = (voice_type or os.getenv("ALIYUN_TTS_VOICE", "Cherry")).strip() or "Cherry"
        self.sample_rate = sample_rate
        self.mode = os.getenv("ALIYUN_TTS_MODE", "server_commit").strip() or "server_commit"
        
        if not self.api_key:
            try:
                from services.ai_service import get_chat_config
                self.api_key = get_chat_config().get("api_key", "")
            except:
                pass
            
        if not self.api_key:
            raise TTSError("DASHSCOPE_API_KEY 未配置")
        
        self.dashscope.api_key = self.api_key
        self.client = None
        self.audio_queue = Queue()
        self.is_finished = False
        self.error = None

    def start(self):
        class StreamingCallback(self.QwenTtsRealtimeCallback):
            def __init__(self, outer):
                self.outer = outer

            def on_open(self) -> None:
                print("[Aliyun TTS Stream] connection opened")

            def on_close(self, code, msg) -> None:
                print(f"[Aliyun TTS Stream] connection closed: {code}, {msg}")

            def on_event(self, response: dict) -> None:
                try:
                    event_type = response.get("type")
                    if event_type == "response.audio.delta":
                        audio_b64 = response.get("delta", "")
                        if audio_b64:
                            self.outer.audio_queue.put(audio_b64)
                    elif event_type == "session.finished":
                        self.outer.is_finished = True
                    elif event_type == "error":
                        self.outer.error = str(response)
                        self.outer.is_finished = True
                except Exception as e:
                    self.outer.error = f"Event error: {e}"
                    self.outer.is_finished = True

        self.client = self.QwenTtsRealtime(model=self.model, callback=StreamingCallback(self))
        self.client.connect()
        self.client.update_session(
            voice=self.voice,
            response_format=self.AudioFormat.PCM_24000HZ_MONO_16BIT,
            mode=self.mode,
        )

    def feed_text(self, text):
        if self.client and text:
            self.client.append_text(text)

    def finish(self):
        if self.client:
            self.client.finish()

    def close(self):
        if self.client:
            try:
                self.client.close()
            except:
                pass

    def get_audio_deltas(self):
        while not self.is_finished or not self.audio_queue.empty():
            try:
                yield self.audio_queue.get(timeout=0.1)
            except Empty:
                if self.is_finished:
                    break
        if self.error:
            raise TTSError(self.error)


class DoubaoTTSStreamingSession:
    def __init__(self, voice_type=None, sample_rate=24000):
        import websockets
        self.websockets = websockets
        self.api_key = os.getenv("DOUBAO_TTS_API_KEY", "").strip()
        self.resource_id = os.getenv("DOUBAO_TTS_RESOURCE_ID", "seed-tts-2.0").strip()
        self.voice = (voice_type or os.getenv("DOUBAO_TTS_SPEAKER", "saturn_zh_female_keainvsheng_tob")).strip()
        self.endpoint = os.getenv("DOUBAO_TTS_WS_ENDPOINT", "wss://openspeech.bytedance.com/api/v3/tts/bidirection").strip()
        self.sample_rate = sample_rate
        
        if not self.api_key:
            raise TTSError("DOUBAO_TTS_API_KEY 未配置")
        if not self.endpoint:
            raise TTSError("DOUBAO_TTS_WS_ENDPOINT 未配置")

        self.audio_queue = Queue()
        self.is_finished = False
        self.error = None
        self.session_id = str(uuid.uuid4())
        self.connect_id = str(uuid.uuid4())
        
        self.loop = None
        self.thread = None
        self.ws = None
        
    def start(self):
        def _thread_target():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            try:
                self.loop.run_until_complete(self._async_run())
            except Exception as e:
                self.error = f"Doubao TTS 后台线程异常: {e}"
                self.is_finished = True
            finally:
                self.loop.close()

        self.thread = threading.Thread(target=_thread_target, daemon=True)
        self.thread.start()
        
        # 等待 WebSocket 准备就绪
        while not self.is_finished and self.ws is None:
            time.sleep(0.01)

    async def _async_run(self):
        from services.doubao_tts_protocols import (
            start_connection, start_session, wait_for_event, receive_message, MsgType, EventType, finish_connection
        )
        headers = {
            "X-Api-Key": self.api_key,
            "X-Api-Resource-Id": self.resource_id,
            "X-Api-Connect-Id": self.connect_id,
            "X-Control-Require-Usage-Tokens-Return": "*",
        }
        
        try:
            # 兼容不同版本的 websockets
            try:
                self.ws = await self.websockets.connect(self.endpoint, additional_headers=headers, max_size=10 * 1024 * 1024)
            except TypeError:
                self.ws = await self.websockets.connect(self.endpoint, extra_headers=headers, max_size=10 * 1024 * 1024)
                
            print(f"[Doubao TTS] provider=doubao resource_id={self.resource_id} speaker={self.voice} connect_id={self.connect_id} session_id={self.session_id} api_key={mask_secret(self.api_key)}")
            
            await start_connection(self.ws)
            await wait_for_event(self.ws, EventType.ConnectionStarted)
            
            req = {
                "req_params": {
                    "speaker": self.voice,
                    "audio_params": {
                        "format": "pcm",
                        "sample_rate": self.sample_rate,
                        "speech_rate": 0,
                        "loudness_rate": 0,
                        "enable_subtitle": False
                    }
                }
            }
            await start_session(self.ws, self.session_id, req)
            await wait_for_event(self.ws, EventType.SessionStarted)
            
            while not self.is_finished:
                msg = await receive_message(self.ws)
                if msg.msg_type == MsgType.AudioOnlyServer:
                    audio_b64 = base64.b64encode(msg.payload).decode("ascii")
                    self.audio_queue.put(audio_b64)
                elif msg.msg_type == MsgType.ServerEvent:
                    event = msg.payload
                    event_type = event.get("event")
                    if event_type == EventType.SessionFinished:
                        self.is_finished = True
                        break
                    elif event_type in (EventType.SessionFailed, EventType.ConnectionFailed):
                        self.error = f"Doubao TTS Event Error: {event}"
                        self.is_finished = True
                        break
        except Exception as e:
            self.error = f"Doubao TTS 连接或接收异常: {e}"
            self.is_finished = True
        finally:
            self.is_finished = True
            if self.ws:
                try:
                    await finish_connection(self.ws)
                    await self.ws.close()
                except:
                    pass

    def feed_text(self, text):
        if not text or not self.ws or not self.loop:
            return
            
        async def _feed():
            try:
                from services.doubao_tts_protocols import task_request, EventType
                request = {
                    "event": EventType.TaskRequest,
                    "req_params": {
                        "text": text
                    }
                }
                await task_request(self.ws, self.session_id, request)
            except Exception as e:
                self.error = f"Doubao TTS 喂入文本异常: {e}"
                self.is_finished = True
                
        asyncio.run_coroutine_threadsafe(_feed(), self.loop)

    def finish(self):
        if not self.ws or not self.loop:
            return
            
        async def _finish():
            try:
                from services.doubao_tts_protocols import finish_session, wait_for_event, EventType
                await finish_session(self.ws, self.session_id)
            except Exception as e:
                self.error = f"Doubao TTS 结束会话异常: {e}"
                self.is_finished = True
                
        asyncio.run_coroutine_threadsafe(_finish(), self.loop)

    def close(self):
        if self.ws and self.loop:
            async def _close():
                try:
                    from services.doubao_tts_protocols import finish_connection
                    await finish_connection(self.ws)
                    await self.ws.close()
                except:
                    pass
            try:
                asyncio.run_coroutine_threadsafe(_close(), self.loop)
            except:
                pass

    def get_audio_deltas(self):
        while not self.is_finished or not self.audio_queue.empty():
            try:
                yield self.audio_queue.get(timeout=0.1)
            except Empty:
                if self.is_finished:
                    break
        if self.error:
            raise TTSError(self.error)


def synthesize_doubao_tts(text: str, voice_type_override: Optional[str] = None) -> Tuple[bytes, str]:
    if not text or not text.strip():
        raise TTSError("TTS 文本不能为空")
    
    session = DoubaoTTSStreamingSession(voice_type=voice_type_override)
    session.start()
    session.feed_text(text)
    session.finish()
    
    pcm_buffer = bytearray()
    try:
        for audio_delta in session.get_audio_deltas():
            pcm_buffer.extend(base64.b64decode(audio_delta))
    finally:
        session.close()
        
    if not pcm_buffer:
        raise TTSError("豆包语音合成未返回音频数据")
        
    wav_audio = _pcm_to_wav_bytes(bytes(pcm_buffer), session.sample_rate)
    return wav_audio, "wav"


def create_tts_streaming_session(voice_type=None, sample_rate=None):
    provider = get_tts_provider()
    
    if provider == "qianwen":
        return AliyunTTSStreamingSession(
            voice_type=voice_type,
            sample_rate=sample_rate or int(os.getenv("ALIYUN_TTS_SAMPLE_RATE", "24000"))
        )
        
    if provider == "doubao":
        return DoubaoTTSStreamingSession(
            voice_type=voice_type,
            sample_rate=sample_rate or int(os.getenv("DOUBAO_TTS_SAMPLE_RATE", "24000"))
        )
        
    raise TTSError(f"无法创建 TTS 会话：未知的 provider={provider}")


def synthesize_speech(text: str, speaker_config: Optional[Dict] = None, voice_type: Optional[str] = None) -> Optional[str]:
    file_path, _ = synthesize_speech_with_detail(text, speaker_config, voice_type)
    return file_path


def synthesize_speech_with_detail(
    text: str,
    speaker_config: Optional[Dict] = None,
    voice_type: Optional[str] = None,
) -> Tuple[Optional[str], str]:
    provider = get_tts_provider()

    if provider == "qianwen":
        selected_voice = (voice_type or os.getenv("ALIYUN_TTS_VOICE", "Cherry")).strip() or "Cherry"
        sample_rate = int(os.getenv("ALIYUN_TTS_SAMPLE_RATE", "24000"))
    elif provider == "doubao":
        selected_voice = (voice_type or os.getenv("DOUBAO_TTS_SPEAKER", "saturn_zh_female_keainvsheng_tob")).strip() or "saturn_zh_female_keainvsheng_tob"
        sample_rate = int(os.getenv("DOUBAO_TTS_SAMPLE_RATE", "24000"))
    else:
        return None, f"收到未支持 provider={provider}"

    file_ext = "wav"
    cache_key = generate_tts_cache_key(text, selected_voice, file_ext, sample_rate)

    cached = get_cached_tts(cache_key)
    if cached:
        return cached, "cache-hit"

    try:
        if provider == "qianwen":
            audio, actual_ext = synthesize_aliyun_tts_realtime(text, voice_type_override=selected_voice)
        elif provider == "doubao":
            audio, actual_ext = synthesize_doubao_tts(text, voice_type_override=selected_voice)
            
        file_path = str(TTS_CACHE_DIR / f"{cache_key}.{actual_ext}")
        with open(file_path, "wb") as f:
            f.write(audio)
        cache_tts(cache_key, file_path)
        return file_path, f"ok-{provider}"
    except Exception as e:
        return None, str(e)


def preflight_tts() -> Dict:
    provider = get_tts_provider()
    
    if provider == "qianwen":
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
    elif provider == "doubao":
        voice_type = os.getenv("DOUBAO_TTS_SPEAKER", "saturn_zh_female_keainvsheng_tob").strip() or "saturn_zh_female_keainvsheng_tob"
        model = os.getenv("DOUBAO_TTS_RESOURCE_ID", "seed-tts-2.0").strip() or "seed-tts-2.0"
        sample_rate = int(os.getenv("DOUBAO_TTS_SAMPLE_RATE", "24000"))
        try:
            audio, file_ext = synthesize_doubao_tts("你好，这是一次豆包语音合成模型二点零预检。", voice_type_override=voice_type)
            return {
                "success": True,
                "provider": provider,
                "mode": "bidirectional-websocket",
                "resourceId": model,
                "voiceType": voice_type,
                "format": file_ext,
                "sampleRate": sample_rate,
                "audioBytes": len(audio),
            }
        except Exception as e:
            return {
                "success": False,
                "provider": provider,
                "mode": "bidirectional-websocket",
                "error": str(e),
                "hint": "请检查 DOUBAO_TTS_API_KEY 等配置，以及 websocket 依赖是否已安装。",
            }
    else:
        return {
            "success": False,
            "provider": provider,
            "error": "未知的 provider",
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
"""

with open("modify_tts.py", "w", encoding="utf-8") as f:
    f.write(f'''
with open(r"{tts_path}", "w", encoding="utf-8") as out:
    out.write("""{new_content}""")
''')

import subprocess
subprocess.run(["python", "modify_tts.py"])
os.remove("modify_tts.py")
print("tts_service.py updated successfully.")
