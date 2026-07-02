# Live2D 表情与语音交互系统实现文档

> **📌 文档定位**：本文档是 [README.md](./README.md) 的技术补充文档，专注于详细解析平台中 **Live2D 虚拟形象「火花」** 的表情系统与语音交互实现机制。如果你想了解项目整体概况，请先阅读 README.md；如果你想深入了解 AI 智能体的技术架构，请参阅 [AI-Agent功能分析报告.md](./AI-Agent功能分析报告.md)。
>
> 本文档详细阐述火花智创平台中 Live2D 虚拟形象「火花」的表情切换机制、语音识别实现、语音合成（朗读）功能，特别关注控制面板点击触发、「水印」与「月卡」叠加效果的共存逻辑。

---

## 📋 目录

| 图标 | 章节 | 标题 |
|------|------|------|
| 🎨 | [一、表情系统架构概览](#一表情系统架构概览) | 表情分类体系与数据结构 |
| 🗂️ | [二、状态管理机制](#二状态管理机制) | 双层状态管理与控制函数 |
| 🖱️ | [三、控制面板交互实现](#三控制面板交互实现) | 表情切换的 UI 交互逻辑 |
| 🔄 | [四、表情叠加共存机制](#四表情叠加共存机制) | 水印/月卡与基础表情的共存原理 |
| ⚡ | [五、实时更新保障](#五实时更新保障) | Monkey-patch 实现方案 |
| 🧠 | [六、情绪关键词触发表情](#六情绪关键词触发表情) | 文本情绪检测与表情映射 |
| 🔧 | [七、生命周期管理](#七生命周期管理) | 初始化与清理流程 |
| 🐛 | [八、常见问题与解决方案](#八常见问题与解决方案) | 眼睛闪烁问题分析与修复 |
| 🎤 | [九、语音识别实现](#九语音识别实现) | 前端实现、后端 API、大模型配置 |
| 🤖 | [十、对话生成流程（大模型调用）](#十对话生成流程大模型调用) | 阿里云通义千问大模型配置与调用 |
| 🔊 | [十一、语音合成（朗读）实现](#十一语音合成朗读实现) | TTS 服务、缓存机制、前端调用 |
| 🔑 | [十二、语音关键词触发表情](#十二语音关键词触发表情) | 语音内容驱动的表情切换 |
| 📦 | [十三、完整集成示例](#十三完整集成示例) | VoiceInteractionService 封装 |
| 📝 | [十四、总结](#十四总结) | 核心设计亮点 |

---

## 一、表情系统架构概览

### 1.1 表情分类体系

| 分类 | 类型 | 数量 | 说明 |
|------|------|------|------|
| **基础表情** | 核心表情 | 10 种 | 独立的表情状态，如黑脸、脸红爱心、生气等 |
| **叠加效果** | 修饰层 | 2 种 | 可与基础表情共存的视觉效果（水印、月卡） |

### 1.2 数据结构定义

```javascript
// 基础表情列表（HuahuoAssistant.vue:230）
const baseExpressions = [
  '01黑脸', '02 脸红爱心', '03 生气', '04 晕', '05 ＞＜', 
  '06 0.0', '07 星星眼', '08 流泪', '10 捧心', '11 要饭'
]

// 叠加效果配置（HuahuoAssistant.vue:231-233）
const overlayOptions = [
  { name: '月卡', parameters: ['key9'], parts: [] },
  { name: '水印', parameters: ['key12', 'Param45', 'Param48', 'Param49', 'Param50'], parts: [] }
]
```

---

## 二、状态管理机制

### 2.1 全局状态对象

系统采用双层状态管理：**Vue 响应式状态** + **全局 window 对象状态**。

```javascript
// Vue 响应式状态（HuahuoAssistant.vue:235-236）
const currentBaseExpression = ref('')
const activeOverlays = ref(new Set(['水印']))  // 默认开启水印

// 全局状态对象（HuahuoAssistant.vue:434-444）
window.__expressionControlsState = {
  initialized: false,
  currentBaseExpression: null,
  activeOverlays: new Set(['水印'])  // 默认开启水印
}

window.__expressionOverlayRules = {
  '月卡': { parameters: ['key9'], parts: [] },
  '水印': { parameters: ['key12', 'Param45', 'Param48', 'Param49', 'Param50'], parts: [] }
}
```

### 2.2 状态同步原则

| 操作 | Vue 状态更新 | 全局状态更新 | 触发同步 |
|------|-------------|-------------|---------|
| 设置基础表情 | `currentBaseExpression.value` | `__expressionControlsState.currentBaseExpression` | `__syncExpressionState()` |
| 切换叠加效果 | `activeOverlays.value` | `__expressionControlsState.activeOverlays` | `__syncExpressionState()` |

---

## 三、控制面板交互实现

### 3.1 基础表情切换

**触发方式**：点击表情面板中的基础表情按钮

```html
<!-- HuahuoAssistant.vue:48-54 -->
<div class="expression-grid">
  <div
    v-for="expr in baseExpressions"
    :key="expr"
    class="expression-item"
    :class="{ active: currentBaseExpression === expr }"
    @click="setBaseExpression(expr)"
  >{{ expr }}</div>
</div>
```

**核心函数**：

```javascript
// HuahuoAssistant.vue:662-669
function setBaseExpression(exprName) {
  // 1. 更新 Vue 响应式状态
  currentBaseExpression.value = exprName
  
  // 2. 更新全局状态对象
  window.__expressionControlsState.currentBaseExpression = exprName
  
  // 3. 获取当前 Live2D 模型
  const model = getCurrentCubism5Model()
  
  // 4. 同步状态到模型
  if (model) {
    window.__syncExpressionState(model)
  }
}
```

### 3.2 叠加效果切换

**触发方式**：勾选/取消叠加效果复选框

```html
<!-- HuahuoAssistant.vue:60-67 -->
<label v-for="ov in overlayOptions" :key="ov.name" class="overlay-item">
  <input
    type="checkbox"
    :checked="activeOverlays.has(ov.name)"
    @change="toggleOverlay(ov.name, $event.target.checked)"
  />
  <span>{{ ov.name }}</span>
</label>
```

**核心函数**：

```javascript
// HuahuoAssistant.vue:671-683
function toggleOverlay(overlayName, checked) {
  // 1. 更新 Vue 响应式状态
  if (checked) {
    activeOverlays.value.add(overlayName)
  } else {
    activeOverlays.value.delete(overlayName)
  }
  
  // 2. 更新全局状态对象
  if (checked) {
    window.__expressionControlsState.activeOverlays.add(overlayName)
  } else {
    window.__expressionControlsState.activeOverlays.delete(overlayName)
  }
  
  // 3. 同步状态到模型
  const model = getCurrentCubism5Model()
  if (model) {
    window.__syncExpressionState(model)
  }
}
```

---

## 四、表情状态同步核心机制

### 4.1 同步流程总览

```
用户操作 → 更新状态 → __syncExpressionState() → 重置参数 → 设置基础表情 → 应用叠加效果
```

### 4.2 `__syncExpressionState` 函数详解

```javascript
// HuahuoAssistant.vue:501-530
window.__syncExpressionState = function(model) {
  const state = window.__expressionControlsState
  if (!model) model = getCurrentCubism5Model()
  if (!model) return

  try {
    // 步骤1：重置表情相关参数（防止表情残留）
    const core = getCubismCoreModel(model)
    if (core) {
      const expressionParams = ['ParamEyeSmile', 'ParamEyeOpen', 'ParamTear']
      expressionParams.forEach(paramName => {
        const paramId = resolveParamIdObject(core, paramName)
        if (paramId) {
          const idx = core.getParameterIndex(paramId)
          if (idx >= 0) {
            core.setParameterValueByIndex(idx, 0, 1)  // 重置为默认值
          }
        }
      })
    }

    // 步骤2：应用基础表情
    if (state.currentBaseExpression) {
      model.setExpression?.(state.currentBaseExpression)
    }

    // 步骤3：应用叠加效果（关键：叠加在基础表情之上）
    window.__applyOverlayState(model)
  } catch (err) {
    console.error('[Expression Controls] Error syncing expression state:', err)
  }
}
```

---

## 五、叠加效果共存机制

### 5.1 核心设计理念

**叠加效果与基础表情的关系**：
- 基础表情通过 `model.setExpression()` 设置，影响整体面部表情
- 叠加效果通过参数控制（0/1 值），独立于基础表情存在
- 叠加效果可以与任意基础表情共存

### 5.2 参数级控制实现

```javascript
// HuahuoAssistant.vue:447-491
window.__applyOverlayStateToCore = function(core) {
  const state = window.__expressionControlsState
  if (!core) return

  const activeOv = state?.activeOverlays || new Set()
  const overlayRules = window.__expressionOverlayRules || {}

  // 收集所有需要控制的参数和部件
  const allParameterIds = new Set()
  const allPartIds = new Set()
  for (const rule of Object.values(overlayRules)) {
    const parameters = rule?.parameters || []
    const parts = rule?.parts || []
    for (const parameterId of parameters) allParameterIds.add(parameterId)
    for (const partId of parts) allPartIds.add(partId)
  }

  // 处理参数（核心共存逻辑）
  for (const parameterId of allParameterIds) {
    // 判断该参数是否应该启用（任一激活的overlay包含此参数则启用）
    const shouldEnable = [...activeOv].some((overlayName) => {
      return overlayRules[overlayName]?.parameters?.includes(parameterId)
    })

    const idObj = resolveParamIdObject(core, parameterId)
    if (!idObj) continue
    if (typeof core.getParameterIndex !== 'function' || 
        typeof core.setParameterValueByIndex !== 'function') continue

    const idx = core.getParameterIndex(idObj)
    if (idx >= 0) {
      core.setParameterValueByIndex(idx, shouldEnable ? 1 : 0, 1)
    }
  }

  // 处理部件（透明度控制）
  for (const partId of allPartIds) {
    const shouldEnable = [...activeOv].some((overlayName) => {
      return overlayRules[overlayName]?.parts?.includes(partId)
    })

    const idObj = resolvePartIdObject(core, partId)
    if (!idObj || typeof core.getPartIndex !== 'function' || 
        typeof core.setPartOpacityByIndex !== 'function') continue

    const idx = core.getPartIndex(idObj)
    if (idx >= 0) {
      core.setPartOpacityByIndex(idx, shouldEnable ? 1 : 0)
    }
  }
}
```

### 5.3 叠加效果共存矩阵

| 基础表情 | 水印 | 月卡 | 两者同时启用 |
|---------|------|------|-------------|
| 01黑脸 | ✓ | ✓ | ✓ |
| 02 脸红爱心 | ✓ | ✓ | ✓ |
| 03 生气 | ✓ | ✓ | ✓ |
| 04 晕 | ✓ | ✓ | ✓ |
| 05 ＞＜ | ✓ | ✓ | ✓ |
| 06 0.0 | ✓ | ✓ | ✓ |
| 07 星星眼 | ✓ | ✓ | ✓ |
| 08 流泪 | ✓ | ✓ | ✓ |
| 10 捧心 | ✓ | ✓ | ✓ |
| 11 要饭 | ✓ | ✓ | ✓ |

---

## 六、实时更新保障机制

### 6.1 Monkey-patch 核心更新函数

为确保叠加效果在模型每一帧更新时都保持激活状态，系统采用 Monkey-patch 技术：

```javascript
// HuahuoAssistant.vue:552-562
if (core && typeof core.update === 'function' && !core.__overlayUpdatePatched) {
  const oldCoreUpdate = core.update.bind(core)
  
  core.update = function(...args) {
    try {
      // 在每帧更新前应用叠加效果状态
      window.__applyOverlayStateToCore?.(core)
    } catch (error) {
      // 静默失败
    }
    
    // 执行原始更新逻辑
    const result = oldCoreUpdate(...args)
    return result
  }
  
  core.__overlayUpdatePatched = true  // 标记已patch，防止重复
}
```

### 6.2 更新时机

| 触发时机 | 机制 | 目的 |
|---------|------|------|
| 用户点击表情 | 直接调用 `__syncExpressionState()` | 即时响应交互 |
| 用户切换叠加 | 直接调用 `__syncExpressionState()` | 即时响应交互 |
| 模型每帧更新 | Monkey-patch `core.update` | 确保叠加效果持续生效 |
| 模型初始化完成 | 调用 `__syncExpressionState()` | 恢复上次保存的状态 |

---

## 七、情绪关键词触发机制

除了手动点击控制面板，表情还会根据 AI 对话内容自动切换：

```javascript
// useLive2d.js:1-22
export function detectEmotionByText(text) {
  const lower = (text || '').toLowerCase()
  if (/开心|高兴|太好了|哈哈|棒|厉害|优秀|成功|恭喜/.test(lower)) return 'happy'
  if (/害羞|脸红|不好意思|羞/.test(lower)) return 'shy'
  if (/生气|愤怒|烦|讨厌|气死/.test(lower)) return 'angry'
  if (/难过|伤心|失望|遗憾|抱歉/.test(lower)) return 'sad'
  if (/晕|头晕|困惑|迷茫|不懂/.test(lower)) return 'dizzy'
  if (/惊讶|天哪|哇|震惊|意外/.test(lower)) return 'surprise'
  return null
}

export function getExpressionByEmotion(emotion) {
  const map = {
    happy: '02 脸红爱心',
    shy: '02 脸红爱心',
    angry: '03 生气',
    sad: '08 流泪',
    dizzy: '04 晕',
    surprise: '07 星星眼'
  }
  return map[emotion] || '06 0.0'
}
```

**触发链路**：
```
AI 流式输出 → onDelta 钩子 → detectEmotionByText() → getExpressionByEmotion() → setBaseExpression()
```

---

## 八、初始化与清理流程

### 8.1 初始化流程

```javascript
// HuahuoAssistant.vue:1304
onMounted(() => {
  // ... 其他初始化
  
  // 初始化表情控制系统
  setupExpressionControls()
  
  // 初始化模型后设置随机表情
  setTimeout(() => {
    const model = getCurrentCubism5Model()
    if (model) {
      window.__syncExpressionState(model)
    }
    startAutoExpression()
  }, 1000)
})
```

### 8.2 清理流程

```javascript
// HuahuoAssistant.vue:1342
onBeforeUnmount(() => {
  // ... 其他清理
  
  // 清理全局状态
  delete window.__syncExpressionState
  delete window.__applyOverlayState
  delete window.__applyOverlayStateToCore
  delete window.__expressionControlsState
  delete window.__expressionOverlayRules
  delete window.__voiceLive2dHooks
})
```

---

## 九、关键函数汇总

| 函数名 | 位置 | 作用 |
|--------|------|------|
| `setBaseExpression(exprName)` | HuahuoAssistant.vue:662 | 设置基础表情 |
| `toggleOverlay(name, checked)` | HuahuoAssistant.vue:671 | 切换叠加效果 |
| `__syncExpressionState(model)` | HuahuoAssistant.vue:501 | 同步表情状态到模型 |
| `__applyOverlayState(model)` | HuahuoAssistant.vue:494 | 应用叠加效果 |
| `__applyOverlayStateToCore(core)` | HuahuoAssistant.vue:447 | 参数级叠加效果控制 |
| `setupExpressionControls()` | HuahuoAssistant.vue:432 | 初始化表情控制系统 |
| `setupExpressionWithOverlay()` | HuahuoAssistant.vue:537 | 设置 Monkey-patch |
| `detectEmotionByText(text)` | useLive2d.js:1 | 情绪关键词检测 |
| `getExpressionByEmotion(emotion)` | useLive2d.js:12 | 情绪到表情映射 |

---

## 八、常见问题与解决方案

### 8.1 眼睛间歇性闪烁（“星星眼”）问题

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

