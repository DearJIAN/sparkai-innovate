import os
import asyncio
import uuid
import json
import gzip
import tempfile
import subprocess
import shutil

from flask import Blueprint, request, jsonify, send_from_directory
from models.user import User
from models.ai_record import AiRecord
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.response import success, error
from services.ai_service import (
    generate_project_summary,
    generate_business_advice,
    generate_risk_analysis,
    call_llm_chat,
    sanitize_answer_text,
    normalize_session_id,
    get_chat_record,
    trim_chat_history,
    generate_stream_response,
    generate_unified_stream,
    get_chat_config,
    get_env_value,
)
from services.tts_service import synthesize_speech, synthesize_speech_with_detail, preflight_tts, get_tts_cache_stats, clear_tts_cache, TTS_CACHE_DIR
from services.volc_realtime_bridge import is_voice_realtime_configured, get_voice_realtime_config

ai_bp = Blueprint('ai', __name__)


def _get_current_user():
    user_id = get_jwt_identity()
    if user_id is None:
        return None
    return User.query.get(int(user_id))


@ai_bp.route('/project-summary', methods=['POST'])
@jwt_required()
def project_summary():
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)
    data = request.get_json()
    project_info = {
        'name': data.get('project_name', ''),
        'description': data.get('description', ''),
        'category': data.get('category', ''),
        'track': data.get('track', '')
    }
    result = generate_project_summary(project_info)
    record = AiRecord(
        user_id=user.id,
        project_id=data.get('project_id'),
        type='summary',
        prompt=str(project_info),
        result=result
    )
    db.session.add(record)
    db.session.commit()
    return success({'result': result, 'type': 'summary'})


@ai_bp.route('/business-plan-advice', methods=['POST'])
@jwt_required()
def business_plan_advice():
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)
    data = request.get_json()
    project_info = {
        'name': data.get('project_name', ''),
        'description': data.get('description', ''),
        'category': data.get('category', ''),
        'track': data.get('track', '')
    }
    result = generate_business_advice(project_info)
    record = AiRecord(
        user_id=user.id,
        project_id=data.get('project_id'),
        type='business_advice',
        prompt=str(project_info),
        result=result
    )
    db.session.add(record)
    db.session.commit()
    return success({'result': result, 'type': 'business_advice'})


@ai_bp.route('/risk-analysis', methods=['POST'])
@jwt_required()
def risk_analysis():
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)
    data = request.get_json()
    project_info = {
        'name': data.get('project_name', ''),
        'description': data.get('description', ''),
        'category': data.get('category', ''),
        'track': data.get('track', '')
    }
    result = generate_risk_analysis(project_info)
    record = AiRecord(
        user_id=user.id,
        project_id=data.get('project_id'),
        type='risk_analysis',
        prompt=str(project_info),
        result=result
    )
    db.session.add(record)
    db.session.commit()
    return success({'result': result, 'type': 'risk_analysis'})


@ai_bp.route('/records', methods=['GET'])
@jwt_required()
def get_records():
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)
    records = AiRecord.query.filter_by(user_id=user.id).order_by(AiRecord.created_at.desc()).all()
    return success({'records': [r.to_dict() for r in records], 'total': len(records)})


@ai_bp.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    payload = request.get_json(silent=True) or {}
    question = str(payload.get('message') or payload.get('question') or '').strip()
    scene_name = str(payload.get('scene') or '火花智创').strip() or '火花智创'
    session_id = normalize_session_id(payload.get('sessionId'))

    if not question:
        return jsonify({"error": "消息不能为空"}), 400
    if not session_id:
        session_id = os.urandom(8).hex()

    try:
        reply, user_prompt, record = call_llm_chat(question, scene_name, session_id)
        if not reply:
            reply = '我刚刚没有组织出合适的回答，你可以换个方式再问一次。'
        if record is not None:
            record['messages'].append({'role': 'user', 'content': user_prompt})
            record['messages'].append({'role': 'assistant', 'content': reply})
            trim_chat_history(record)
        return jsonify({
            'reply': reply,
            'sessionId': session_id,
            'model': get_chat_config()['model_name'],
            'mode': 'langchain_chat',
        })
    except Exception as error:
        return jsonify({
            'error': '调用模型失败',
            'detail': error.__class__.__name__ + ': ' + str(error),
            'sessionId': session_id,
        }), 500


@ai_bp.route('/chat/stream', methods=['POST'])
@jwt_required()
def chat_stream():
    payload = request.get_json(silent=True) or {}
    question = str(payload.get('message') or payload.get('question') or '').strip()
    scene_name = str(payload.get('scene') or '火花智创').strip() or '火花智创'
    session_id = normalize_session_id(payload.get('sessionId'))

    if not question:
        return jsonify({"error": "消息不能为空"}), 400

    user = _get_current_user()
    role = user.role if user else 'student'

    return generate_unified_stream(question, role, scene_name, session_id)


@ai_bp.route('/voice/chat/stream', methods=['POST'])
@jwt_required()
def voice_chat_stream():
    payload = request.get_json(silent=True) or {}
    question = str(payload.get('message') or payload.get('question') or '').strip()
    scene_name = str(payload.get('scene') or '火花智创').strip() or '火花智创'
    session_id = normalize_session_id(payload.get('sessionId'))

    if not question:
        return jsonify({"error": "消息不能为空"}), 400

    return generate_stream_response(question, scene_name, session_id, use_voice=True)


@ai_bp.route('/voice/config', methods=['GET'])
@jwt_required()
def voice_config():
    voice_realtime = get_voice_realtime_config()
    return jsonify({
        "ok": True,
        "realtime_configured": is_voice_realtime_configured(),
        "speaker": voice_realtime["speaker"],
        "bot_name": voice_realtime["bot_name"],
        "input_mod": voice_realtime["input_mod"],
    })


@ai_bp.route('/health', methods=['GET'])
def health():
    config = get_chat_config()
    return jsonify({
        "ok": True,
        "chat_configured": bool(config["api_key"] and config["base_url"] and config["model_name"]),
        "voice_realtime_configured": is_voice_realtime_configured(),
        "model": config["model_name"],
    })


@ai_bp.route('/tts/synthesize', methods=['POST'])
@jwt_required()
def synthesize_tts():
    payload = request.get_json(silent=True) or {}
    text = str(payload.get('text') or '').strip()
    voice_type = str(payload.get('voiceType') or '').strip()
    if not text:
        return jsonify({"error": "文本内容不能为空"}), 400
    try:
        file_path, detail = synthesize_speech_with_detail(text, voice_type=voice_type or None)
        if not file_path:
            return jsonify({"error": "语音合成失败", "detail": detail}), 500
        return jsonify({
            "success": True,
            "audio_url": f"/api/ai/tts/audio/{os.path.basename(file_path)}"
        })
    except Exception as e:
        return jsonify({"error": f"语音合成失败: {str(e)}"}), 500


@ai_bp.route('/tts/audio/<filename>')
def serve_tts_audio(filename):
    file_path = str(TTS_CACHE_DIR / filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "音频文件不存在"}), 404
    return send_from_directory(str(TTS_CACHE_DIR), filename)


@ai_bp.route('/tts/preflight', methods=['GET'])
@jwt_required()
def tts_preflight():
    result = preflight_tts()
    return jsonify(result), (200 if result.get("success") else 500)


@ai_bp.route('/asr', methods=['POST'])
@jwt_required()
def asr():
    try:
        if 'audio' not in request.files:
            return jsonify({"error": "缺少音频文件"}), 400

        audio_file = request.files['audio']
        asr_provider = os.getenv("ASR_PROVIDER", "doubao").lower()

        with tempfile.TemporaryDirectory() as tmpdir:
            webm_path = os.path.join(tmpdir, f"{uuid.uuid4()}.webm")
            wav_path = os.path.join(tmpdir, f"{uuid.uuid4()}.wav")

            audio_file.save(webm_path)

            try:
                subprocess.run([
                    "ffmpeg", "-y", "-i", webm_path, "-ar", "16000", "-ac", "1", wav_path
                ], check=True, capture_output=True, text=True)
            except subprocess.CalledProcessError as e:
                return jsonify({"error": f"音频转换失败：{e.stderr}"}), 500

            recognized_text = ""
            provider_name = ""
            model_name = ""

            if asr_provider == "doubao":
                try:
                    doubao_config = {
                        "ws_url": get_env_value("DOUBAO_ASR_WS_URL", fallback="wss://openspeech.bytedance.com/api/v3/sauc/bigmodel"),
                        "app_id": get_env_value("DOUBAO_ASR_APP_ID", fallback=""),
                        "access_token": get_env_value("DOUBAO_ASR_ACCESS_TOKEN", fallback=""),
                        "resource_id": get_env_value("DOUBAO_ASR_RESOURCE_ID", fallback="volc.bigasr.sauc.duration"),
                        "model_name": get_env_value("DOUBAO_ASR_MODEL_NAME", fallback="bigmodel"),
                        "format": get_env_value("DOUBAO_ASR_FORMAT", fallback="wav"),
                        "rate": get_env_value("DOUBAO_ASR_RATE", fallback="16000"),
                        "bits": get_env_value("DOUBAO_ASR_BITS", fallback="16"),
                        "channel": get_env_value("DOUBAO_ASR_CHANNEL", fallback="1"),
                        "language": get_env_value("DOUBAO_ASR_LANGUAGE", fallback="zh-CN"),
                    }
                    loop = asyncio.new_event_loop()
                    recognized_text = loop.run_until_complete(_call_doubao_asr(wav_path, doubao_config))
                    loop.close()
                    provider_name = "doubao-asr"
                    model_name = doubao_config["model_name"]
                except Exception as e:
                    return jsonify({"error": f"豆包ASR失败：{str(e)}"}), 500

            if not recognized_text:
                try:
                    from opencc import OpenCC
                    cc = OpenCC("t2s")
                    from faster_whisper import WhisperModel
                    model = WhisperModel("small", device="cpu", compute_type="int8")
                    segments, info = model.transcribe(wav_path, language="zh", task="transcribe", vad_filter=True)
                    text_parts = [seg.text for seg in segments]
                    recognized_text = cc.convert("".join(text_parts).strip())
                    provider_name = "faster-whisper"
                    model_name = "small"
                except Exception as e:
                    return jsonify({"error": f"语音识别失败：{str(e)}"}), 500

            if not recognized_text:
                return jsonify({"error": "语音识别失败，未检测到有效语音"}), 400

        return jsonify({"text": recognized_text, "provider": provider_name, "model": model_name})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


async def _call_doubao_asr(wav_path, config):
    import websockets

    ws_url = config.get("ws_url", "wss://openspeech.bytedance.com/api/v3/sauc/bigmodel")
    app_id = config.get("app_id", "")
    access_token = config.get("access_token", "")
    resource_id = config.get("resource_id", "volc.bigasr.sauc.duration")
    model_name = config.get("model_name", "bigmodel")

    with open(wav_path, "rb") as f:
        audio_data = f.read()
    compressed_audio = gzip.compress(audio_data)

    request_id = str(uuid.uuid4())
    request_params = {
        "user": {"uid": ""},
        "audio": {"format": config.get("format", "wav"), "codec": "raw", "rate": int(config.get("rate", 16000)), "bits": int(config.get("bits", 16)), "channel": int(config.get("channel", 1))},
        "request": {"model_name": model_name, "enable_itn": True, "enable_punc": True, "enable_ddc": True, "show_utterances": True, "enable_nonstream": False},
    }
    request_payload = json.dumps(request_params).encode('utf-8')
    compressed_request = gzip.compress(request_payload)

    headers = {
        "X-Api-Resource-Id": resource_id,
        "X-Api-Request-Id": request_id,
        "X-Api-Access-Key": access_token,
        "X-Api-App-Key": app_id,
    }

    async with websockets.connect(ws_url, additional_headers=headers) as ws:
        version = 0b0001
        header_size = 0b0001
        message_type = 0b0001
        header_byte = (version << 4) | header_size
        type_flag_byte = (message_type << 4) | 0b0000
        ser_comp_byte = (0b0001 << 4) | 0b0001
        header = bytes([header_byte, type_flag_byte, ser_comp_byte, 0x00])
        payload_size = len(compressed_request)
        message = header + payload_size.to_bytes(4, 'big') + compressed_request
        await ws.send(message)

        response = await ws.recv()

        audio_message_type = 0b0010
        audio_message_flags = 0b0010
        audio_type_flag_byte = (audio_message_type << 4) | audio_message_flags
        audio_header = bytes([header_byte, audio_type_flag_byte, ser_comp_byte, 0x00])
        audio_payload_size = len(compressed_audio)
        audio_message = audio_header + audio_payload_size.to_bytes(4, 'big') + compressed_audio
        await ws.send(audio_message)

        final_result = await ws.recv()

        text = ""
        try:
            if len(final_result) > 12:
                payload_data = final_result[12:]
                try:
                    result_json = gzip.decompress(payload_data).decode('utf-8')
                except:
                    result_json = payload_data.decode('utf-8')
                result = json.loads(result_json)
                if "result" in result:
                    text = result.get("result", {}).get("text", "")
        except Exception:
            pass

        if not text:
            raise Exception("未收到有效识别结果")
        return text


@ai_bp.route('/expressions', methods=['GET'])
def expressions():
    return jsonify({
        "base": [
            {"name": "01黑脸", "file": "Expressions/01黑脸.exp3.json"},
            {"name": "02 脸红爱心", "file": "Expressions/02 脸红爱心.exp3.json"},
            {"name": "03 生气", "file": "Expressions/03 生气.exp3.json"},
            {"name": "04 晕", "file": "Expressions/04 晕.exp3.json"},
            {"name": "05 ＞＜", "file": "Expressions/05 ＞＜.exp3.json"},
            {"name": "06 0.0", "file": "Expressions/06 0.0.exp3.json"},
            {"name": "07 星星眼", "file": "Expressions/07 星星眼.exp3.json"},
            {"name": "08 流泪", "file": "Expressions/08 流泪.exp3.json"},
            {"name": "10 捧心", "file": "Expressions/10 捧心.exp3.json"},
            {"name": "11 要饭", "file": "Expressions/11 要饭.exp3.json"},
        ],
        "overlay": [
            {"name": "月卡", "file": "Expressions/月卡.exp3.json", "probability": 0.3},
            {"name": "水印", "file": "Expressions/水印.exp3.json", "probability": 0.2},
        ]
    })


@ai_bp.route('/model-info', methods=['GET'])
def model_info():
    return jsonify({
        "name": "huahuo",
        "path": "/live2d/huahuo/火花.model3.json",
    })
