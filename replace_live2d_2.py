import sys

filepath = r'e:\LEAR-CODE-NEW\软件工程\my-keshe\Live2D-表情与语音交互系统实现文档.md'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    (
        "火山 TTS HTTP API",
        "阿里云 Qwen Realtime TTS API"
    ),
    (
        "火山 TTS",
        "阿里云 TTS"
    )
]

for old, new in replacements:
    content = content.replace(old, new)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Live2D doc updated.")
