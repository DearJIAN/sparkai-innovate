import sys

filepath = r'e:\LEAR-CODE-NEW\软件工程\my-keshe\README.md'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

target = '### v4.10.1 - 2026-07-01（当前版本）'

replacement = '''### v4.10.2 - 2026-07-02（当前版本）

> 修复 Live2D 模型对话时眼睛高频闪烁（“星星眼”）问题

#### 🐛 Bug 修复

- **Live2D 对话表情闪烁**：修复了在 AI 对话播放语音时，由于 Live2D Widget 底层音频分析器自动驱动 `ParamMouthOpenY`（嘴部张合参数），且当前模型的嘴部参数意外关联了眼睛放大，导致眼睛高频闪烁“星星眼”的问题。通过在 `HuahuoAssistant.vue` 的 `__applyOverlayStateToCore` 渲染拦截器中，强制将每一帧的 `ParamMouthOpenY` 锁定为 0，彻底切断了音频到眼睛的污染链路，稳定了对话期间的表情显示。

***

### v4.10.1 - 2026-07-01'''

if target in content:
    content = content.replace(target, replacement)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('README.md updated successfully.')
else:
    print('Target string not found in README.md.')
