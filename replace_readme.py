import sys

filepath = r'e:\LEAR-CODE-NEW\软件工程\my-keshe\README.md'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    (
        "- TTS 语音合成：火山 TTS HTTP API + 浏览器 SpeechSynthesis 双通道流",
        "- TTS 语音合成：阿里云（通义千问）qwen-tts-realtime 流式接口为主，浏览器 SpeechSynthesis 仅做备用/朗读按钮使用"
    ),
    (
        "tts_service.py            # TTS 服务，火山 TTS HTTP API",
        "tts_service.py            # TTS 服务，阿里云 Qwen Realtime TTS API"
    ),
    (
        "| `/api/ai/tts/synthesize`       | POST | JWT | TTS 语音合成（火山 TTS",
        "| `/api/ai/tts/synthesize`       | POST | JWT | TTS 语音合成（阿里云通义千问 TTS"
    ),
    (
        "确认火山 TTS API",
        "确认阿里云 TTS API"
    ),
    (
        "- **TTS 语音合成**：`tts_service.py`，火山 TTS HTTP API",
        "- **TTS 语音合成**：`tts_service.py`，阿里云 Qwen Realtime TTS API"
    ),
    (
        "- `tts_service.py`：火山 TTS 语音合成（HTTP API",
        "- `tts_service.py`：阿里云 TTS 语音合成（HTTP API"
    )
]

for old, new in replacements:
    content = content.replace(old, new)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("README.md updated.")
