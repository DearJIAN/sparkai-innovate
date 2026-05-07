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
| 🤖 | [十、对话生成流程（大模型调用）](#十对话生成流程大模型调用) | 豆包/火山方舟大模型配置与调用 |
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

### 8.1 眼睛间歇性闪烁问题

**问题现象**：Live2D 角色眼睛出现间歇性闪烁（一闪一闪）

**根因分析**（参考项目历史修复记录 v4.3.2）：

| 根因 | 描述 | 影响 |
|------|------|------|
| **口型参数泄漏** | `startStreamMouthPulse` / `startSpeechMouthPulse` 以正弦波驱动 `ParamMouthOpenY`（幅度 0.3-0.8，60-80ms 间隔），但模型不具备口型素材，参数值泄漏到眼部参数 | 眼睛不自然开合 |
| **强制表情切换** | `onStreamStart` / `onSpeechStart` 强制设置星星眼，`onStreamEnd` / `onSpeechEnd` 强制重置为中性表情，形成反复切换 | 表情频繁跳动 |
| **参数冲突** | 口型脉冲函数与表情参数控制冲突 | 眼部参数被意外修改 |

**解决方案**：

```javascript
// 方案1：禁用口型脉冲函数（推荐）
function startStreamMouthPulse() {}  // 改为空函数
function stopStreamMouthPulse() {}   // 改为空函数
function startSpeechMouthPulse() {}  // 改为空函数
function stopSpeechMouthPulse() {}   // 改为空函数

// 方案2：移除强制表情设置
window.__voiceLive2dHooks = {
  onStreamStart: () => {},           // 不再强制设置星星眼
  onDelta: (payload) => {            // 仅通过关键词驱动表情
    const emotion = detectEmotionByText(payload?.text || '')
    if (emotion) {
      const expr = getExpressionByEmotion(emotion)
      if (expr) setBaseExpression(expr)
    }
  },
  onStreamEnd: () => {},             // 不再强制重置表情
  onSpeechStart: () => {},           // 不再强制设置星星眼
  onSpeechPulse: () => {},           // 禁用口型脉冲
  onSpeechEnd: () => {},             // 不再强制重置表情
}

// 方案3：移除 core.update 的 monkey-patch 中的口型应用
if (core && typeof core.update === 'function' && !core.__overlayUpdatePatched) {
  const oldCoreUpdate = core.update.bind(core)
  core.update = function(...args) {
    try {
      window.__applyOverlayStateToCore?.(core)  // 仅保留 overlay 应用
      // 移除 window.__applySpeechStateToCore?.(core)
    } catch (error) {}
    const result = oldCoreUpdate(...args)
    return result
  }
  core.__overlayUpdatePatched = true
}
```

**验证方法**：
1. 启动应用，进入 AI 对话界面
2. 发送消息触发流式回复
3. 观察角色眼睛是否稳定，无闪烁现象

---

## 九、语音识别实现

### 9.1 功能概述

语音识别系统实现以下能力：
- **浏览器原生 API**：优先使用 Web Speech API（Chrome/Safari）
- **后端 ASR 回退**：Firefox 等不支持原生 API 的浏览器使用后端火山引擎 ASR
- **情绪联动**：语音识别过程中实时检测情绪并切换表情

### 9.2 后端配置（.env）

项目使用多个大模型进行语音处理，关键配置如下：

```env
# ============================================
# 语音识别 ASR - /api/asr（必填）
# ============================================
# 火山方舟 ASR 配置
ASR_PROVIDER=doubao
DOUBAO_ASR_WS_URL=wss://openspeech.bytedance.com/api/v3/sauc/bigmodel
DOUBAO_ASR_APP_ID=your-asr-app-id-here
DOUBAO_ASR_ACCESS_TOKEN=your-asr-access-token-here
DOUBAO_ASR_SECRET_KEY=your-asr-secret-key-here
DOUBAO_ASR_RESOURCE_ID=volc.bigasr.sauc.duration
DOUBAO_ASR_MODEL_NAME=bigmodel
DOUBAO_ASR_FORMAT=wav
DOUBAO_ASR_RATE=16000
DOUBAO_ASR_BITS=16
DOUBAO_ASR_CHANNEL=1
DOUBAO_ASR_LANGUAGE=zh-CN

# ============================================
# 实时语音对话 - volc.speech.dialog（必填）
# ============================================
VOICE_REALTIME_APP_ID=your-app-id-here
VOICE_REALTIME_APP_KEY=your-app-key-here
VOICE_REALTIME_TOKEN=your-token-here
VOICE_REALTIME_RESOURCE_ID=volc.speech.dialog
VOICE_REALTIME_UID=huahuo-web
VOICE_REALTIME_DIALOG_ADDRESS=wss://openspeech.bytedance.com
VOICE_REALTIME_DIALOG_URI=/api/v3/realtime/dialogue
VOICE_REALTIME_SPEAKER=zh_male_yunzhou_jupiter_bigtts
VOICE_REALTIME_BOT_NAME=火花
VOICE_REALTIME_INPUT_MOD=text
```

### 9.3 后端 API 实现（ai.py）

```python
# backend/routes/ai.py

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

            # 保存上传的 webm 文件
            audio_file.save(webm_path)
            
            # 转换为 wav 格式（火山引擎要求）
            if webm_path.endswith('.webm'):
                convert_webm_to_wav(webm_path, wav_path)
            else:
                shutil.copy(webm_path, wav_path)

            recognized_text = ""
            provider_name = ""
            model_name = ""

            # 方案1：火山引擎 ASR
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
                    # 降级到 faster-whisper
                    asr_provider = "faster-whisper"

            # 方案2：本地 faster-whisper 模型（降级方案）
            if not recognized_text:
                try:
                    from opencc import OpenCC
                    cc = OpenCC("t2s")
                    model = WhisperModel("base", device="cpu", compute_type="int8")
                    segments, info = model.transcribe(wav_path, language="zh")
                    recognized_text = cc.convert(" ".join([s.text for s in segments]))
                    provider_name = "faster-whisper"
                    model_name = "base"
                except Exception as e:
                    pass

            if recognized_text:
                return jsonify({
                    "success": True,
                    "text": recognized_text,
                    "provider": provider_name,
                    "model": model_name
                })
            else:
                return jsonify({"error": "语音识别失败"}), 500

    except Exception as e:
        return jsonify({"error": f"ASR 错误: {str(e)}"}), 500


# WebSocket 调用火山引擎 ASR
async def _call_doubao_asr(wav_path, config):
    import websockets
    import gzip

    ws_url = config.get("ws_url", "wss://openspeech.bytedance.com/api/v3/sauc/bigmodel")
    app_id = config.get("app_id", "")
    access_token = config.get("access_token", "")
    resource_id = config.get("resource_id", "volc.bigasr.sauc.duration")
    model_name = config.get("model_name", "bigmodel")

    with open(wav_path, "rb") as f:
        audio_data = f.read()
    compressed_audio = gzip.compress(audio_data)

    request_id = str(uuid.uuid4())
    
    payload = {
        "header": {
            "app_id": app_id,
            "token": access_token,
            "resource_id": resource_id,
            "request_id": request_id,
            "timestamp": int(time.time() * 1000),
        },
        "parameter": {
            "model": model_name,
            "format": config.get("format", "wav"),
            "rate": int(config.get("rate", 16000)),
            "bits": int(config.get("bits", 16)),
            "channel": int(config.get("channel", 1)),
            "language": config.get("language", "zh-CN"),
        },
        "payload": {
            "audio": base64.b64encode(compressed_audio).decode("utf-8"),
        }
    }

    async with websockets.connect(ws_url) as websocket:
        await websocket.send(json.dumps(payload))
        response = await websocket.recv()
        result = json.loads(response)
        
        if result.get("header", {}).get("code") == 0:
            return result.get("payload", {}).get("result", {}).get("text", "")
        return ""
```

### 9.4 前端实现（HuahuoAssistant.vue）

```javascript
// 前端语音识别核心代码
const isListening = ref(false)
const isAsrProcessing = ref(false)
let recognition = null

function startVoiceRecognition() {
  // 优先使用浏览器原生 Web Speech API
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
  
  if (SpeechRecognition) {
    recognition = new SpeechRecognition()
    recognition.lang = 'zh-CN'           // 中文识别
    recognition.continuous = false       // 单次识别模式
    recognition.interimResults = true    // 返回中间结果
    
    // 识别结果回调
    recognition.onresult = (event) => {
      let finalTranscript = ''
      let interimTranscript = ''
      
      for (let i = event.resultIndex; i < event.results.length; i++) {
        if (event.results[i].isFinal) {
          finalTranscript += event.results[i][0].transcript
        } else {
          interimTranscript += event.results[i][0].transcript
        }
      }
      
      // 更新界面显示
      if (interimTranscript) {
        inputText.value = finalTranscript + interimTranscript
      } else {
        inputText.value = finalTranscript
        // 语音识别完成，触发表情切换
        handleVoiceInput(finalTranscript)
      }
    }
    
    recognition.onerror = (event) => {
      console.error('Speech recognition error:', event.error)
      isListening.value = false
      if (event.error !== 'no-speech') {
        ElMessage.error('语音识别出错：' + event.error)
      }
    }
    
    recognition.onend = () => {
      isListening.value = false
    }
    
    recognition.start()
    isListening.value = true
  } else {
    // Firefox 等不支持 Web Speech API 的浏览器，使用后端 ASR
    startFirefoxVoice()
  }
}

function stopVoiceRecognition() {
  if (recognition) {
    recognition.stop()
    recognition = null
  }
  isListening.value = false
}

// Firefox 回退方案：使用后端 ASR
async function startFirefoxVoice() {
  isListening.value = true
  isAsrProcessing.value = true
  
  try {
    // 使用 MediaRecorder 录制音频
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    const mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' })
    const audioChunks = []
    
    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunks.push(event.data)
      }
    }
    
    mediaRecorder.onstop = async () => {
      stream.getTracks().forEach(track => track.stop())
      
      // 上传音频到后端进行 ASR
      const audioBlob = new Blob(audioChunks, { type: 'audio/webm' })
      const formData = new FormData()
      formData.append('audio', audioBlob, 'voice.webm')
      
      try {
        const { uploadAsrAudio } = await import('@/api/ai')
        const res = await uploadAsrAudio(formData)
        const result = await res.json()
        
        if (result.success && result.text) {
          inputText.value = result.text
          handleVoiceInput(result.text)  // 触发表情切换
        }
      } catch (err) {
        console.error('ASR upload failed:', err)
        ElMessage.error('语音识别失败')
      } finally {
        isAsrProcessing.value = false
      }
    }
    
    // 录制 5 秒后自动停止
    mediaRecorder.start()
    setTimeout(() => {
      if (mediaRecorder.state === 'recording') {
        mediaRecorder.stop()
      }
    }, 5000)
    
  } catch (err) {
    console.error('Failed to start recording:', err)
    isListening.value = false
    isAsrProcessing.value = false
    ElMessage.error('无法访问麦克风')
  }
}

// 语音输入处理 - 触发表情切换
function handleVoiceInput(text) {
  const emotion = detectEmotionByText(text)
  if (emotion) {
    const expression = getExpressionByEmotion(emotion)
    setBaseExpression(expression)
  }
}
```

---

## 十、对话生成流程（大模型调用）

### 10.1 功能概述

语音识别完成后，系统会调用大模型（豆包/火山方舟）生成回复文本，完整流程如下：

```
用户语音 → 语音识别(ASR) → 文本生成(LLM) → 流式返回 → 语音合成(TTS) → 表情联动
```

### 10.2 后端大模型配置（.env）

项目使用火山方舟大模型进行对话生成，关键配置如下：

```env
# ============================================
# AI 对话 - 火山方舟（必填）
# ============================================
# 前往 https://console.volcengine.com/ark 获取 API Key
ARK_API_KEY=your-ark-api-key-here
ARK_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
ARK_MODEL=doubao-seed-1-6-251015
VOICE_TEMPERATURE=0.4

# ============================================
# 备用配置（GLM 模型）
# ============================================
# GLM_API_KEY=your-glm-api-key
# GLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4/
# GLM_MODEL=glm-4-flash
```

### 10.3 后端 LLM 服务（ai_service.py）

```python
# backend/services/ai_service.py

import os
import threading
from queue import Queue, Empty
from flask import Response, stream_with_context

# 全局 LLM 实例
_llm_instance = None

def get_env_value(*names, fallback=""):
    """获取环境变量，支持多个备选名称"""
    for name in names:
        value = os.getenv(name, "").strip()
        if value:
            return value
    return fallback

def get_chat_config():
    """获取聊天配置，支持多种模型提供商"""
    return {
        "api_key": get_env_value("GLM_API_KEY", "ARK_API_KEY", "VOICE_API_KEY"),
        "base_url": get_env_value("GLM_BASE_URL", "ARK_BASE_URL", fallback="https://dashscope.aliyuncs.com/compatible-mode/v1"),
        "model_name": get_env_value("GLM_MODEL", "ARK_MODEL", fallback="qwen-mt-flash"),
        "temperature": float(get_env_value("VOICE_TEMPERATURE", fallback="0.4")),
    }

def get_llm():
    """获取 LLM 实例，使用 langchain_openai"""
    global _llm_instance
    if _llm_instance is not None:
        return _llm_instance
    
    try:
        from langchain_openai import ChatOpenAI
        config = get_chat_config()
        _llm_instance = ChatOpenAI(
            model_name=config["model_name"],
            openai_api_key=config["api_key"],
            openai_api_base=config["base_url"],
            temperature=config["temperature"],
            max_tokens=4096,
            timeout=120,
            request_timeout=120,
        )
        return _llm_instance
    except Exception as e:
        raise RuntimeError(f"LLM 初始化失败: {e}")

# 对话系统提示词
SYSTEM_PROMPT = (
    "你是火花智创 SparkAI Innovate的 AI 助手「火花」。"
    "请始终使用中文，回答简洁、自然、可直接执行。"
    "只输出最终回答，不要输出思考过程、分析步骤、提示词复述或内部说明。"
    "\n\n【重要规则】"
    "\n1. 当用户问'你可以做什么'或类似问题时，根据用户角色列出对应功能："
    "\n   - 学生：智能引航、项目创意生成、模拟路演答辩、AI材料问答、商业计划书体检、路演稿生成、智能竞赛推荐"
    "\n   - 老师：智能引航、批量审核助手、智能反馈生成、AI材料问答、商业计划书体检、评审辅助、模拟路演答辩"
    "\n   - 评委：智能引航、评审意见草稿、评分一致性检查、AI材料问答、商业计划书体检、评审辅助"
    "\n   - 管理员：所有功能"
    "\n2. 当用户要求'生成项目简介/简历/创意'或'如何组建团队'等需要具体信息的问题时，你必须先追问用户的关键信息。"
    "\n3. 回答时使用自然流畅的中文，可以适当使用加粗强调关键词，但不要过度使用标题符号。"
)

ROLE_MAP = {'student': '学生', 'teacher': '老师', 'judge': '评委', 'admin': '管理员'}

def build_langchain_messages(question, session_id, scene_name="火花智创", user_role='student'):
    """构建 LangChain 消息格式"""
    from langchain_core.messages import HumanMessage, AIMessage
    
    role_desc = ROLE_MAP.get(user_role, '学生')
    record = get_chat_record(session_id)
    history = record["messages"] if record else []
    
    messages = []
    
    # 添加历史对话
    for entry in history:
        content = str(entry.get("content") or "").strip()
        if not content:
            continue
        entry_role = entry.get("role")
        if entry_role == "assistant":
            messages.append(AIMessage(content=content))
        else:
            messages.append(HumanMessage(content=content))
    
    # 添加当前用户消息
    user_prompt = f"{SYSTEM_PROMPT}\n\n当前用户角色：{role_desc}\n当前场景：{scene_name}\n用户问题：{question}"
    messages.append(HumanMessage(content=user_prompt))
    
    return messages, user_prompt, record

def call_llm_chat(question, scene_name, session_id, user_role='student'):
    """调用 LLM 生成回复"""
    llm = get_llm()
    messages, user_prompt, record = build_langchain_messages(question, session_id, scene_name, user_role)
    response = llm.invoke(messages)
    reply = sanitize_answer_text(response.content) if response.content else ""
    return reply, user_prompt, record

def generate_stream_response(question, scene_name, session_id, use_voice=False):
    """生成流式响应（核心函数）"""
    if not session_id:
        session_id = os.urandom(8).hex()
    
    queue = Queue()
    worker_fn = _stream_voice_model if use_voice else _stream_text_model
    worker = threading.Thread(target=worker_fn, args=(queue, question, scene_name, session_id), daemon=True)
    worker.start()
    
    @stream_with_context
    def generate():
        yield f"sessionId:{session_id}\n"
        while True:
            try:
                item = queue.get(timeout=0.5)
            except Empty:
                if not worker.is_alive():
                    break
                continue
            if item is None:
                break
            if isinstance(item, dict) and item.get('error'):
                yield f"\nerror:{item.get('detail', '未知错误')}\n"
                break
            yield f"delta:{str(item)}\n"
        yield "done:1\n"
    
    response = Response(generate(), mimetype='text/plain; charset=utf-8')
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['X-Accel-Buffering'] = 'no'
    return response
```

### 10.4 后端 API 路由（ai.py）

```python
# backend/routes/ai.py

@ai_bp.route('/chat/stream', methods=['POST'])
@jwt_required()
def chat_stream():
    """聊天流式接口"""
    payload = request.get_json(silent=True) or {}
    question = str(payload.get('message') or payload.get('question') or '').strip()
    scene_name = str(payload.get('scene') or '火花智创').strip() or '火花智创'
    session_id = normalize_session_id(payload.get('sessionId'))
    
    if not question:
        return jsonify({"error": "消息不能为空"}), 400
    
    try:
        return generate_stream_response(question, scene_name, session_id, use_voice=False)
    except Exception as e:
        return jsonify({"error": f"对话失败: {str(e)}"}), 500
```

### 10.5 前端调用（HuahuoAssistant.vue）

```javascript
// 前端聊天接口调用
export function chatStream(message, sessionId, scene = '火花智创') {
  return fetch('/api/ai/chat/stream', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token') || ''}`,
    },
    body: JSON.stringify({ message, sessionId, scene }),
  })
}

// 处理流式响应
async function handleChatStream(response) {
  const reader = response.body.getReader()
  const decoder = new TextDecoder('utf-8')
  
  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    
    const chunk = decoder.decode(value)
    const lines = chunk.split('\n').filter(line => line.trim())
    
    for (const line of lines) {
      if (line.startsWith('sessionId:')) {
        sessionId.value = line.split(':')[1]
      } else if (line.startsWith('delta:')) {
        const text = line.slice(6)
        streamingText.value += text
        // 实时检测情绪并切换表情
        const emotion = detectEmotionByText(streamingText.value)
        if (emotion) {
          const expression = getExpressionByEmotion(emotion)
          setBaseExpression(expression)
        }
      } else if (line.startsWith('done:')) {
        currentReplyText.value = streamingText.value
        streamingText.value = ''
        isStreaming.value = false
      }
    }
  }
}

// 语音识别完成后触发对话
function handleVoiceInput(text) {
  // 触发表情切换
  const emotion = detectEmotionByText(text)
  if (emotion) {
    const expression = getExpressionByEmotion(emotion)
    setBaseExpression(expression)
  }
  
  // 发送消息并获取回复
  sendMessage(text)
}

async function sendMessage(text) {
  if (!text.trim()) return
  
  messages.value.push({
    role: 'user',
    content: text,
    timestamp: new Date().toISOString()
  })
  
  isStreaming.value = true
  streamingText.value = ''
  
  try {
    const response = await chatStream(text, sessionId.value)
    await handleChatStream(response)
  } catch (error) {
    console.error('Chat error:', error)
    isStreaming.value = false
    ElMessage.error('对话失败，请重试')
  }
}
```

### 10.6 完整流程时序图

```
用户操作                    前端组件                  后端API                  LLM服务
    |                          |                        |                       |
    |--点击麦克风开始语音输入--> |                        |                       |
    |                          |                        |                       |
    |--说话..."你好"-----------|                        |                       |
    |                          |                        |                       |
    |<--语音识别完成-----------|                        |                       |
    |                          |--POST /api/ai/chat/stream-->                       |
    |                          |                        |--调用 LangChain LLM--> |
    |                          |                        |                       |
    |                          |<--流式返回 delta--------|                       |
    |<--UI更新显示回复----------|                        |                       |
    |                          |                        |                       |
    |                          |                        |<--LLM完成回复---------|
    |                          |<--返回 done------------|                       |
    |                          |                        |                       |
    |--自动触发表情切换-------->|                        |                       |
    |                          |--调用 setBaseExpression-->                       |
    |                          |                        |                       |
```

---

## 十一、语音合成（朗读）实现

### 11.1 功能概述

语音合成系统实现以下能力：
- **浏览器原生 TTS**：使用 Web Speech Synthesis API
- **后端 TTS**：火山引擎 TTS 服务（支持更多音色）
- **缓存机制**：避免重复合成相同文本
- **表情联动**：朗读过程中根据内容切换表情

### 11.2 后端 TTS 服务（tts_service.py）

```python
# backend/services/tts_service.py

import os
import hashlib
import time
import requests
from typing import Dict, Optional
from pathlib import Path

# 缓存目录配置
TTS_CACHE_DIR = Path(__file__).parent / "tts_cache"
TTS_CACHE_DIR.mkdir(exist_ok=True)

# 内存缓存（7天有效期）
TTS_CACHE: Dict[str, Dict] = {}
CACHE_TTL = 3600 * 24 * 7

# 火山引擎 TTS API
TTS_API_URL = "https://openspeech.bytedance.com/api/v1/tts"

# 音色配置
SPEAKER_CONFIG = {
    "default": {
        "speaker": "zh_male_yunzhou_jupiter_bigtts",
        "speed": 1.0,
        "volume": 1.0,
        "pitch": 0,
    },
    "female": {
        "speaker": "zh_female_xiaoyun",
        "speed": 1.0,
        "volume": 1.0,
        "pitch": 0,
    }
}


def generate_tts_cache_key(text: str, speaker: str = "default") -> str:
    """生成缓存键"""
    raw = f"{text}:{speaker}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()


def get_cached_tts(cache_key: str) -> Optional[str]:
    """获取缓存的音频文件路径"""
    if cache_key in TTS_CACHE:
        entry = TTS_CACHE[cache_key]
        if time.time() - entry["timestamp"] < CACHE_TTL:
            if os.path.exists(entry["file_path"]):
                return entry["file_path"]
            else:
                del TTS_CACHE[cache_key]
    return None


def cache_tts(cache_key: str, file_path: str):
    """缓存音频文件路径"""
    TTS_CACHE[cache_key] = {
        "file_path": file_path,
        "timestamp": time.time()
    }


def synthesize_speech(text: str, speaker_config: Optional[Dict] = None) -> Optional[str]:
    """
    合成语音
    :param text: 要合成的文本
    :param speaker_config: 音色配置
    :return: 音频文件路径，失败返回 None
    """
    cache_key = generate_tts_cache_key(text, "default")

    # 检查缓存
    cached = get_cached_tts(cache_key)
    if cached:
        return cached

    # 合并配置
    config = SPEAKER_CONFIG["default"]
    if speaker_config:
        config.update(speaker_config)

    # 获取 API 凭证
    api_key = os.getenv("VOICE_REALTIME_TOKEN") or os.getenv("VOICE_REALTIME_API_KEY")
    app_id = os.getenv("VOICE_REALTIME_APP_ID")

    if not api_key or not app_id:
        return None

    # 构建请求体
    payload = {
        "app": {
            "appid": app_id,
            "token": api_key,
            "cluster": "volcano_tts",
        },
        "user": {
            "uid": "tts_" + str(int(time.time()))
        },
        "audio": {
            "voice_type": config["speaker"],
            "encoding": "mp3",
            "speed_ratio": config["speed"],
            "volume_ratio": config["volume"],
            "pitch_ratio": config["pitch"],
        },
        "request": {
            "reqid": str(int(time.time() * 1000)),
            "text": text,
            "operation": "query",
        }
    }

    try:
        response = requests.post(
            TTS_API_URL,
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            result = response.json()
            # 3000 表示成功
            if result.get("code") == 3000:
                audio_data = result.get("data", "")
                if audio_data:
                    import base64
                    audio_bytes = base64.b64decode(audio_data)

                    # 保存到缓存目录
                    file_path = str(TTS_CACHE_DIR / f"{cache_key}.mp3")
                    with open(file_path, "wb") as f:
                        f.write(audio_bytes)

                    # 更新缓存
                    cache_tts(cache_key, file_path)
                    return file_path

        return None
    except Exception as e:
        print(f"TTS Error: {e}")
        return None


def get_tts_cache_stats() -> Dict:
    """获取缓存统计信息"""
    total_size = 0
    for entry in TTS_CACHE.values():
        file_path = entry.get("file_path")
        if file_path and os.path.exists(file_path):
            total_size += os.path.getsize(file_path)

    return {
        "cache_size": len(TTS_CACHE),
        "total_bytes": total_size,
        "cache_dir": str(TTS_CACHE_DIR)
    }


def clear_tts_cache():
    """清除所有缓存"""
    for entry in TTS_CACHE.values():
        file_path = entry.get("file_path")
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass

    TTS_CACHE.clear()

    for file in TTS_CACHE_DIR.glob("*.mp3"):
        try:
            file.unlink()
        except:
            pass

    return {"message": "语音缓存已清除"}
```

### 10.3 后端 API 路由（ai.py）

```python
# backend/routes/ai.py

@ai_bp.route('/tts/synthesize', methods=['POST'])
@jwt_required()
def synthesize_tts():
    """语音合成 API"""
    payload = request.get_json(silent=True) or {}
    text = str(payload.get('text') or '').strip()
    
    if not text:
        return jsonify({"error": "文本内容不能为空"}), 400
    
    try:
        file_path = synthesize_speech(text)
        if not file_path:
            return jsonify({"error": "语音合成失败"}), 500
        
        return jsonify({
            "success": True,
            "audio_url": f"/api/ai/tts/audio/{os.path.basename(file_path)}"
        })
    except Exception as e:
        return jsonify({"error": f"语音合成失败: {str(e)}"}), 500


@ai_bp.route('/tts/audio/<filename>')
def serve_tts_audio(filename):
    """提供合成的音频文件"""
    file_path = str(TTS_CACHE_DIR / filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "音频文件不存在"}), 404
    return send_from_directory(str(TTS_CACHE_DIR), filename)
```

### 10.4 前端实现（HuahuoAssistant.vue）

```javascript
// 前端语音合成核心代码
const isSpeaking = ref(false)
let speechUtterance = null

function toggleSpeech() {
  // 如果正在播放，停止播放
  if (isSpeaking.value) {
    window.speechSynthesis.cancel()
    isSpeaking.value = false
    notifyLive2dHook('onSpeechEnd')
    return
  }
  
  // 如果没有回复内容，不播放
  if (!currentReplyText.value) return
  
  // 创建语音合成实例
  const u = new SpeechSynthesisUtterance(currentReplyText.value)
  u.lang = 'zh-CN'      // 中文
  u.rate = 1.0          // 语速
  u.pitch = 1.0         // 音调
  
  // 获取可用语音列表
  const voices = window.speechSynthesis.getVoices()
  const zhVoice = voices.find(v => v.lang.startsWith('zh') && v.name.includes('Female')) || 
                  voices.find(v => v.lang.startsWith('zh'))
  
  if (zhVoice) {
    u.voice = zhVoice
  }
  
  // 绑定事件回调
  u.onstart = () => {
    isSpeaking.value = true
    notifyLive2dHook('onSpeechStart')
  }
  
  u.onend = () => {
    isSpeaking.value = false
    notifyLive2dHook('onSpeechEnd')
  }
  
  u.onerror = () => {
    isSpeaking.value = false
    notifyLive2dHook('onSpeechEnd')
  }
  
  // 开始播放
  window.speechSynthesis.speak(u)
  speechUtterance = u
}

// 分析结果朗读
function speakAnalysisResult() {
  if (!analysisResult.value) return
  currentReplyText.value = analysisResult.value
  toggleSpeech()
}

// 组件卸载时清理
onUnmounted(() => {
  if (speechUtterance) {
    window.speechSynthesis.cancel()
  }
})
```

### 10.5 API 接口调用（ai.js）

```javascript
// frontend/src/api/ai.js

// 语音合成接口
export const synthesizeTts = (data) => request.post('/ai/tts/synthesize', data)

// 语音识别接口
export const uploadAsrAudio = (formData) => {
  return fetch('/api/ai/asr', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    },
    body: formData
  })
}
```

---

## 十二、语音关键词触发表情

### 12.1 三种触发方案

**方案一：语音输入时实时检测**

```javascript
// 在语音识别过程中实时检测关键词
recognition.onresult = (event) => {
  let fullText = ''
  
  for (let i = event.resultIndex; i < event.results.length; i++) {
    fullText += event.results[i][0].transcript
  }
  
  // 实时检测情绪并切换表情
  const emotion = detectEmotionByText(fullText)
  if (emotion) {
    const expression = getExpressionByEmotion(emotion)
    setBaseExpression(expression)
  }
  
  inputText.value = fullText
}
```

**方案二：语音合成时按句子分段触发**

```javascript
// 将文本按标点符号分割
function splitTextBySentence(text) {
  return text.split(/[。！？；；]/).filter(s => s.trim())
}

// 逐句合成并触发表情
async function speakWithExpression(text) {
  const sentences = splitTextBySentence(text)
  
  for (const sentence of sentences) {
    // 根据句子内容切换表情
    const emotion = detectEmotionByText(sentence)
    if (emotion) {
      const expression = getExpressionByEmotion(emotion)
      setBaseExpression(expression)
    }
    
    // 合成并播放当前句子
    const utterance = new SpeechSynthesisUtterance(sentence)
    utterance.lang = 'zh-CN'
    
    await new Promise((resolve) => {
      utterance.onend = resolve
      utterance.onerror = resolve
      window.speechSynthesis.speak(utterance)
    })
  }
}
```

**方案三：关键词优先级映射（扩展语音场景词汇）**

```javascript
// useLive2d.js - 情绪检测函数
export function detectEmotionByText(text) {
  const lower = (text || '').toLowerCase()
  
  // 开心类关键词（语音场景扩展）
  if (/开心|高兴|太好了|哈哈|棒|厉害|优秀|成功|恭喜|太棒了|太好了|真棒|厉害/.test(lower)) return 'happy'
  
  // 害羞类关键词
  if (/害羞|脸红|不好意思|羞|羞涩/.test(lower)) return 'shy'
  
  // 生气类关键词（语音场景扩展）
  if (/生气|愤怒|烦|讨厌|气死|气死我了|可恶|讨厌|烦人/.test(lower)) return 'angry'
  
  // 难过类关键词（语音场景扩展）
  if (/难过|伤心|失望|遗憾|抱歉|对不起|可惜|伤心/.test(lower)) return 'sad'
  
  // 困惑类关键词（语音场景扩展）
  if (/晕|头晕|困惑|迷茫|不懂|什么|怎么回事|搞不懂/.test(lower)) return 'dizzy'
  
  // 惊讶类关键词（语音场景扩展）
  if (/惊讶|天哪|哇|震惊|意外|哇塞|我的天|哇哦/.test(lower)) return 'surprise'
  
  return null
}

// 情绪到表情的映射
export function getExpressionByEmotion(emotion) {
  const emotionMap = {
    'happy': '07 星星眼',
    'shy': '02 脸红爱心',
    'angry': '03 生气',
    'sad': '08 流泪',
    'dizzy': '04 晕',
    'surprise': '07 星星眼'
  }
  return emotionMap[emotion] || '01黑脸'
}
```

---

## 十三、完整集成示例

### 13.1 VoiceInteractionService 类封装

```javascript
// 完整的语音交互服务类
class VoiceInteractionService {
  constructor() {
    this.recognition = null
    this.isListening = ref(false)
    this.isSpeaking = ref(false)
    this.onTextChange = null  // 文本变化回调
    this.onExpressionChange = null  // 表情变化回调
  }
  
  // 启动语音识别
  startListening() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    
    if (SpeechRecognition) {
      this.recognition = new SpeechRecognition()
      this.recognition.lang = 'zh-CN'
      this.recognition.interimResults = true
      
      this.recognition.onresult = (event) => {
        let text = ''
        for (let i = event.resultIndex; i < event.results.length; i++) {
          text += event.results[i][0].transcript
        }
        
        // 实时触发表情切换
        this.triggerExpressionByText(text)
        
        // 通知外部组件
        if (this.onTextChange) {
          this.onTextChange(text)
        }
      }
      
      this.recognition.onend = () => {
        this.isListening.value = false
      }
      
      this.recognition.start()
      this.isListening.value = true
    } else {
      this.startFallbackListening()
    }
  }
  
  // 回退方案：使用后端 ASR
  async startFallbackListening() {
    this.isListening.value = true
    
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' })
      const audioChunks = []
      
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunks.push(event.data)
        }
      }
      
      mediaRecorder.onstop = async () => {
        stream.getTracks().forEach(track => track.stop())
        
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' })
        const formData = new FormData()
        formData.append('audio', audioBlob, 'voice.webm')
        
        try {
          const res = await fetch('/api/ai/asr', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: formData
          })
          
          const result = await res.json()
          if (result.success && result.text) {
            this.triggerExpressionByText(result.text)
            if (this.onTextChange) {
              this.onTextChange(result.text)
            }
          }
        } catch (err) {
          console.error('ASR failed:', err)
        }
        
        this.isListening.value = false
      }
      
      mediaRecorder.start()
      setTimeout(() => {
        if (mediaRecorder.state === 'recording') {
          mediaRecorder.stop()
        }
      }, 5000)
      
    } catch (err) {
      console.error('Failed to start recording:', err)
      this.isListening.value = false
    }
  }
  
  // 停止语音识别
  stopListening() {
    if (this.recognition) {
      this.recognition.stop()
      this.recognition = null
    }
    this.isListening.value = false
  }
  
  // 根据文本触发表情
  triggerExpressionByText(text) {
    const emotion = detectEmotionByText(text)
    if (emotion) {
      const expression = getExpressionByEmotion(emotion)
      setBaseExpression(expression)
      
      if (this.onExpressionChange) {
        this.onExpressionChange(expression, emotion)
      }
    }
  }
  
  // 语音合成（浏览器原生）
  speak(text) {
    return new Promise((resolve) => {
      if (!text) {
        resolve()
        return
      }
      
      const utterance = new SpeechSynthesisUtterance(text)
      utterance.lang = 'zh-CN'
      
      utterance.onstart = () => {
        this.isSpeaking.value = true
        notifyLive2dHook('onSpeechStart')
      }
      
      utterance.onend = () => {
        this.isSpeaking.value = false
        notifyLive2dHook('onSpeechEnd')
        resolve()
      }
      
      utterance.onerror = () => {
        this.isSpeaking.value = false
        notifyLive2dHook('onSpeechEnd')
        resolve()
      }
      
      window.speechSynthesis.speak(utterance)
    })
  }
  
  // 带表情联动的语音合成
  async speakWithExpression(text) {
    const sentences = text.split(/[。！？；；]/).filter(s => s.trim())
    
    for (const sentence of sentences) {
      // 根据句子内容切换表情
      this.triggerExpressionByText(sentence)
      
      // 播放当前句子
      await this.speak(sentence)
    }
  }
  
  // 使用后端 TTS 合成语音
  async synthesizeAndSpeak(text) {
    try {
      const { synthesizeTts } = await import('@/api/ai')
      const result = await synthesizeTts({ text })
      
      if (result.success && result.audio_url) {
        const audio = new Audio(result.audio_url)
        audio.onplay = () => {
          this.isSpeaking.value = true
          notifyLive2dHook('onSpeechStart')
        }
        audio.onended = () => {
          this.isSpeaking.value = false
          notifyLive2dHook('onSpeechEnd')
        }
        audio.onerror = () => {
          this.isSpeaking.value = false
          notifyLive2dHook('onSpeechEnd')
        }
        await audio.play()
      }
    } catch (err) {
      console.error('TTS failed:', err)
      // 降级到浏览器原生 TTS
      await this.speak(text)
    }
  }
}

// 使用示例
const voiceService = new VoiceInteractionService()

// 启动语音输入
voiceService.onTextChange = (text) => {
  inputText.value = text
}

voiceService.onExpressionChange = (expression, emotion) => {
  console.log(`表情切换: ${expression} (${emotion})`)
}

// 绑定到麦克风按钮
document.getElementById('mic-button').addEventListener('click', () => {
  if (voiceService.isListening.value) {
    voiceService.stopListening()
  } else {
    voiceService.startListening()
  }
})

// 播放 AI 回复并触发表情
await voiceService.speakWithExpression(aiReplyText)
```

---

## 十四、总结

Live2D 表情与语音交互系统的核心设计亮点：

1. **双层状态管理**：Vue 响应式状态用于 UI 绑定，全局 window 对象用于跨组件/框架通信
2. **参数级叠加控制**：通过控制特定参数值实现叠加效果与基础表情的独立共存
3. **Monkey-patch 实时保障**：确保叠加效果在模型每帧更新时持续生效
4. **灵活的触发机制**：支持手动点击、情绪关键词自动切换两种模式
5. **完整的生命周期管理**：初始化时设置默认状态，卸载时清理全局对象
6. **多模型语音支持**：集成火山引擎 ASR/TTS 与浏览器原生 API，支持降级方案
7. **智能缓存机制**：TTS 结果自动缓存，避免重复合成
8. **表情语音联动**：根据语音内容实时切换角色表情，增强交互体验