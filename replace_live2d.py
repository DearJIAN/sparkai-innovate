import sys
import re

filepath = r'e:\LEAR-CODE-NEW\软件工程\my-keshe\Live2D-表情与语音交互系统实现文档.md'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# find everything from ### 8.1 to the end of the file or next ###
pattern = r'### 8\.1 眼睛间歇性闪烁问题.*?(?=### 8\.2|$)'
match = re.search(pattern, content, re.DOTALL)

replacement = '''### 8.1 眼睛间歇性闪烁（“星星眼”）问题

**现象**：无论用户在控制面板选择什么表情，只要进入 AI 对话并播放语音时，Live2D 角色的眼睛就会高频闪烁（瞬间变成“星星眼”又瞬间切换回来），但左侧控制面板依然显示原先选定的表情不变。

**根本原因**：
这并非“对话联动表情”逻辑导致。真正原因是：**Live2D Widget 自带的音频分析器与当前 .moc3 模型的内部物理绑定发生冲突。**
当 AI 助手回答并播放语音时，前端 Live2D 引擎底层的音频分析器会自动捕获声音音量，并试图驱动模型的嘴巴参数（`ParamMouthOpenY`）来实现“张嘴说话”的口型同步。然而，当前使用的“火花”模型在物理绑定（Rigging）上存在缺陷，它的口型参数 `ParamMouthOpenY` 意外牵连了眼睛的放大参数。因此，语音播放期间嘴部参数的高频跳动，直接导致了眼睛呈现疯狂放大的“星星眼”闪烁效果。

**修复方式**：
由于该模型本身并没有张嘴说话的素材需要同步，且存在物理绑定污染。我们可以直接在模型的配置文件中彻底移除并关闭 LipSync 模块。
在 `前端项目/public/live2d/huahuo/火花.model3.json` 中，将 `LipSync` 组的 `Ids` 置空即可：

```json
{
  "Target": "Parameter",
  "Name": "LipSync",
  "Ids": []
}
```
通过在数据源头切断引擎对嘴型特征的识别，Live2D SDK 将不再执行任何音频张合分析，从而一劳永逸地解决了眼睛异常闪烁的问题。

'''

if match:
    content = content[:match.start()] + replacement + content[match.end():]
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Live2D doc updated successfully.')
else:
    print('Target regex not found in Live2D doc.')
