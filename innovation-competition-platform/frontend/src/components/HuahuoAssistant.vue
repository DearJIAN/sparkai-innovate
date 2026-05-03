<template>
  <teleport to="body">
    <div class="huahuo-assistant">
      <!-- 加载状态 -->
      <div v-if="!loaded && !loadError" class="live2d-loading">
        <el-icon class="is-loading" size="28"><Loading /></el-icon>
        <span>火花加载中...</span>
      </div>
      <div v-if="loadError" class="live2d-error" @click="retryInit">
        <el-icon size="20"><WarningFilled /></el-icon>
        <span>加载失败，点击重试</span>
      </div>

      <div
        v-if="loaded"
        id="live2d-drag-handle"
        class="live2d-drag-handle"
        :class="{ 'panel-open': panelOpen }"
        @mousedown="startModelDrag"
        @touchstart="startModelDragTouch"
      >
        <el-icon size="14"><Rank /></el-icon>
      </div>

      <!-- 对话面板（整合版） -->
      <transition name="panel-slide">
        <div v-if="panelOpen" ref="panelRef" class="chat-panel" :style="panelStyle">
          <div class="panel-header" @mousedown="startDrag" @touchstart="startDragTouch">
            <div class="header-left">
              <span class="panel-title">🤖 火花 AI 助手</span>
              <el-tag v-if="isListening" type="danger" size="small" effect="dark" class="listening-tag">录音中</el-tag>
            </div>
            <div class="header-actions">
              <el-button size="small" text @click.stop="switchToAgent" title="AI 智能体">
                🤖
              </el-button>
              <el-button size="small" text @click.stop="switchToAnalysis" title="AI 分析工具">
                <el-icon><MagicStick /></el-icon>
              </el-button>
              <el-button size="small" text @click.stop="toggleExpressionPanel" title="切换表情">😊</el-button>
              <el-button size="small" text @click.stop="closePanel" title="收起面板">
                <el-icon><ArrowDown /></el-icon>
              </el-button>
            </div>
          </div>

          <div class="panel-body">
            <!-- 表情控制面板 -->
            <transition name="panel-slide">
              <div v-if="expressionPanelOpen" class="expression-panel">
                <div class="expression-section">
                  <div class="expression-section-title">基础表情</div>
                  <div class="expression-grid">
                    <div
                      v-for="expr in baseExpressions"
                      :key="expr"
                      class="expression-item"
                      :class="{ active: currentBaseExpression === expr }"
                      @click="setBaseExpression(expr)"
                    >{{ expr }}</div>
                  </div>
                </div>
                <div class="expression-section">
                  <div class="expression-section-title">修饰效果</div>
                  <div class="overlay-list">
                    <label v-for="ov in overlayOptions" :key="ov.name" class="overlay-item">
                      <input
                        type="checkbox"
                        :checked="activeOverlays.has(ov.name)"
                        @change="toggleOverlay(ov.name, $event.target.checked)"
                      />
                      <span>{{ ov.name }}</span>
                    </label>
                  </div>
                </div>
              </div>
            </transition>

            <!-- AI 分析模式 -->
            <div v-if="mode === 'analysis'" class="analysis-mode">
              <el-form :model="analysisForm" label-position="top" size="small">
                <el-form-item label="项目名称">
                  <el-input v-model="analysisForm.project_name" placeholder="输入项目名称" />
                </el-form-item>
                <el-form-item label="项目简介">
                  <el-input v-model="analysisForm.description" type="textarea" :rows="3" placeholder="描述你的项目想法" />
                </el-form-item>
                <el-form-item label="AI 功能">
                  <el-radio-group v-model="analysisForm.ai_type" size="small">
                    <el-radio-button value="summary">项目简介</el-radio-button>
                    <el-radio-button value="business_advice">商业建议</el-radio-button>
                    <el-radio-button value="risk_analysis">风险分析</el-radio-button>
                  </el-radio-group>
                </el-form-item>
                <el-button type="primary" :loading="analysisLoading" @click="handleAnalysis" style="width:100%" size="small">
                  {{ analysisLoading ? 'AI 生成中...' : '开始生成' }}
                </el-button>
              </el-form>
              <div v-if="analysisResult" class="analysis-result">
                <el-divider content-position="left">AI 分析结果</el-divider>
                <div class="markdown-body" v-html="renderMarkdown(analysisResult)"></div>
                <div class="analysis-actions">
                  <el-button size="small" type="primary" link @click="copyAnalysisResult">复制</el-button>
                  <el-button size="small" type="primary" link @click="speakAnalysisResult">朗读</el-button>
                </div>
              </div>
              <div class="mode-switch-hint">
                <el-button type="primary" link size="small" @click="mode = 'chat'">← 返回对话模式</el-button>
              </div>
            </div>

            <!-- AI 智能体模式 -->
            <div v-else-if="mode === 'agent'" class="agent-mode">
              <AgentPanel
                :user-role="userRole"
                :initial-context="agentInitialContext"
                compact
                @result="onAgentResult"
                @speak="onAgentSpeak"
              />
              <div class="mode-switch-hint">
                <el-button type="primary" link size="small" @click="mode = 'chat'">← 返回对话模式</el-button>
              </div>
            </div>

            <!-- 对话模式 -->
            <div v-else class="chat-mode">
              <div ref="messagesRef" class="chat-messages">
                <div v-if="messages.length === 0" class="chat-empty">
                  <p>👋 你好！我是火花，你的 AI 助手</p>
                  <p>输入文字或点击麦克风语音对话</p>
                  <div class="quick-questions">
                    <el-button v-for="q in quickQuestions" :key="q" size="small" round @click="sendQuickQuestion(q)">{{ q }}</el-button>
                  </div>
                </div>
                <div v-for="(msg, idx) in messages" :key="idx" class="message-item" :class="msg.role">
                  <div class="message-avatar">{{ msg.role === 'user' ? '👤' : '🤖' }}</div>
                  <div class="message-content">
                    <div v-if="msg.role === 'assistant'" class="markdown-body" v-html="renderMarkdown(msg.content)"></div>
                    <div v-else>{{ msg.content }}</div>
                    <div v-if="msg.role === 'assistant' && msg.type === 'navigate' && msg.navigate" class="message-actions">
                      <el-button type="primary" size="small" @click="handleNavigate(msg.navigate.route)">
                        🧭 前往 {{ msg.navigate.label || '目标页面' }} →
                      </el-button>
                    </div>
                    <div v-if="msg.role === 'assistant' && msg.type === 'agent_result'" class="message-capability-tag">
                      <el-tag size="small" type="success">🤖 智能体 · {{ getCapabilityLabel(msg.capability) }}</el-tag>
                    </div>
                  </div>
                </div>
                <div v-if="isStreaming" class="message-item assistant">
                  <div class="message-avatar">🤖</div>
                  <div class="message-content streaming">
                    <div class="markdown-body" v-html="renderMarkdown(streamingText)"></div>
                    <span class="cursor-blink">▌</span>
                  </div>
                </div>
              </div>

              <div class="chat-input-area">
                <el-input
                  v-model="inputText"
                  placeholder="输入消息..."
                  @keyup.enter="sendMessage"
                  :disabled="isStreaming"
                  size="default"
                  clearable
                >
                  <template #append>
                    <el-button @click="sendMessage" :loading="isStreaming" :disabled="!inputText.trim()">发送</el-button>
                  </template>
                </el-input>
                <div class="voice-controls">
                  <el-button
                    :type="isListening ? 'danger' : 'primary'"
                    circle
                    size="small"
                    @click="toggleVoiceRecognition"
                    :loading="isAsrProcessing"
                    title="语音输入"
                  >
                    <el-icon><Microphone /></el-icon>
                  </el-button>
                  <el-button
                    v-if="currentReplyText"
                    :type="isSpeaking ? 'warning' : 'success'"
                    circle
                    size="small"
                    @click="toggleSpeech"
                    :title="isSpeaking ? '停止朗读' : '朗读回复'"
                  >
                    <el-icon><component :is="isSpeaking ? 'VideoPause' : 'VideoPlay'" /></el-icon>
                  </el-button>
                  <el-button circle size="small" @click="clearMessages" title="清空对话">
                    <el-icon><Delete /></el-icon>
                  </el-button>
                  <el-button circle size="small" @click="newSession" title="新会话">
                    <el-icon><Plus /></el-icon>
                  </el-button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </teleport>
</template>

<script setup>
import { ref, reactive, computed, nextTick, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRouter } from 'vue-router'
import { marked } from 'marked'
import { chatStream, generateAnalysis } from '@/api/ai'
import { ElMessage } from 'element-plus'
import { Loading, WarningFilled, MagicStick, ArrowDown, Microphone, Delete, Plus, VideoPause, VideoPlay, Rank } from '@element-plus/icons-vue'
import { useLive2d } from '@/composables/useLive2d'
import AgentPanel from '@/views/ai-assistant/AgentPanel.vue'
import { useUserStore } from '@/stores/user'

const { detectEmotionByText, getExpressionByEmotion, updateExpressionByText, notifyLive2dHook } = useLive2d()
const userStore = useUserStore()

const showTips = ref(false)
const tipText = ref('')
const loaded = ref(false)
const loadError = ref(false)
const panelOpen = ref(false)
const mode = ref('chat')
const agentInitialContext = ref({})
const userRole = computed(() => userStore.currentRole || 'student')
let retryCount = 0

// 表情控制状态
const expressionPanelOpen = ref(false)
const baseExpressions = ['01黑脸', '02 脸红爱心', '03 生气', '04 晕', '05 ＞＜', '06 0.0', '07 星星眼', '08 流泪', '10 捧心', '11 要饭']
const overlayOptions = [
  { name: '月卡', parameters: ['key9'], parts: [] },
  { name: '水印', parameters: ['key12', 'Param45', 'Param48', 'Param49', 'Param50'], parts: [] }
]
const currentBaseExpression = ref('')
const activeOverlays = ref(new Set(['水印']))

const messages = ref([])
const inputText = ref('')
const isStreaming = ref(false)
const streamingText = ref('')
const currentReplyText = ref('')
const currentResponseType = ref('chat')
const currentNavigateData = ref(null)
const currentCapability = ref('')
const sessionId = ref('')
const isListening = ref(false)
const isAsrProcessing = ref(false)
const isSpeaking = ref(false)
const messagesRef = ref(null)
const panelRef = ref(null)
const panelStyle = ref({})
const panelPos = ref({ x: 0, y: 0 })
let recognition = null
let speechUtterance = null
let speechPulseInterval = null
let dragState = { dragging: false, startX: 0, startY: 0 }
let modelDragState = { dragging: false, startX: 0, startY: 0, origLeft: 0, origBottom: 0 }
let modelPatchLoopId = null

const analysisForm = reactive({ project_name: '', description: '', category: '', track: '', ai_type: 'summary' })
const analysisLoading = ref(false)
const analysisResult = ref('')

const quickQuestions = ['你可以做什么？', '帮我生成项目简介', '竞赛有哪些赛道？', '如何组建团队？']

marked.setOptions({ breaks: true, gfm: true })

function renderMarkdown(text) {
  if (!text) return ''
  try {
    let processed = text
    processed = processed.replace(/^(#{1,6})\s+/gm, (match, hashes) => {
      const level = hashes.length
      return `<h${level}>`
    })
    processed = processed.replace(/<h([1-6])>(.*)/g, (match, level, content) => {
      if (content.includes(`</h${level}>`)) return match
      return `<h${level}>${content}</h${level}>`
    })
    let html = marked.parse(processed, { breaks: true, gfm: true })
    html = html.replace(/#{1,6}\s/g, '')
    return html
  } catch { return text }
}

function openPanel() {
  panelOpen.value = true
  notifyLive2dHook('onStreamEnd')
}

function closePanel() {
  panelOpen.value = false
  expressionPanelOpen.value = false
}

function switchToAnalysis() {
  mode.value = 'analysis'
}

function switchToAgent() {
  if (isListening.value) {
    ElMessage.warning('请先停止语音识别')
    stopVoiceRecognition()
  }
  mode.value = 'agent'
}

function onAgentResult(text) {
  updateExpressionByText(text)
}

function onAgentSpeak(text) {
  if (isStreaming.value) {
    ElMessage.warning('当前正在生成对话回复，请稍后再朗读智能体结果')
    return
  }
  currentReplyText.value = text
  toggleSpeech()
}

function handleOpenHuahuoAgent(event) {
  panelOpen.value = true
  mode.value = 'agent'
  if (event.detail) {
    agentInitialContext.value = event.detail
  }
}

function toggleExpressionPanel() {
  expressionPanelOpen.value = !expressionPanelOpen.value
}

// ============================================================
// Live2D 核心辅助函数（参考 my_huahuo 实现）
// ============================================================

function getCurrentCubism5Model() {
  const manager = window.__live2dWidgetModelManager
  const appDelegate = manager?.cubism5model
  const subdelegate = appDelegate?.subdelegates?.at?.(0)
  const live2dManager = subdelegate?.getLive2DManager?.()
  return live2dManager?._models?.at?.(0) || null
}

function getModelTargets(target) {
  const seen = new Set()
  const out = []
  const push = (x) => {
    if (!x || seen.has(x)) return
    seen.add(x)
    out.push(x)
  }
  push(target)
  push(target?._model)
  push(target?._model?._model)
  push(target?.model)
  push(target?.model?._model)
  push(target?.model?._model?._model)
  return out
}

function idToString(idObj) {
  try {
    if (!idObj) return ''
    if (typeof idObj === 'string') return idObj
    if (typeof idObj.getString === 'function') {
      const s = idObj.getString()
      if (typeof s === 'string') return s
      if (s && typeof s.s === 'string') return s.s
    }
    if (typeof idObj.s === 'string') return idObj.s
  } catch (_) {}
  return ''
}

function getCubismCoreModel(target) {
  const targets = getModelTargets(target)
  for (const current of targets) {
    if (current?._parameterIds?.getSize && current?._parameterIds?.at) {
      return current
    }
  }
  return null
}

function resolveParamIdObject(core, paramId) {
  try {
    const ids = core?._parameterIds
    if (!ids?.getSize || !ids?.at) return null
    for (let i = 0; i < ids.getSize(); i += 1) {
      const idObj = ids.at(i)
      if (idToString(idObj) === paramId) return idObj
    }
  } catch (_) {}
  return null
}

function resolvePartIdObject(core, partId) {
  try {
    const ids = core?._partIds
    if (!ids?.getSize || !ids?.at) return null
    for (let i = 0; i < ids.getSize(); i += 1) {
      const idObj = ids.at(i)
      if (idToString(idObj) === partId) return idObj
    }
  } catch (_) {}
  return null
}

// ============================================================
// 表情 overlay 共存系统
// ============================================================

function setupExpressionControls() {
  // 表情控制状态
  window.__expressionControlsState = {
    initialized: false,
    currentBaseExpression: null,
    activeOverlays: new Set(['水印']) // 默认开启水印
  }

  // 修饰效果规则
  window.__expressionOverlayRules = {
    '月卡': { parameters: ['key9'], parts: [] },
    '水印': { parameters: ['key12', 'Param45', 'Param48', 'Param49', 'Param50'], parts: [] }
  }

  // 应用 overlay 状态到 core model
  window.__applyOverlayStateToCore = function(core) {
    const state = window.__expressionControlsState
    if (!core) return

    const activeOv = state?.activeOverlays || new Set()
    const overlayRules = window.__expressionOverlayRules || {}

    const allParameterIds = new Set()
    const allPartIds = new Set()
    for (const rule of Object.values(overlayRules)) {
      const parameters = rule?.parameters || []
      const parts = rule?.parts || []
      for (const parameterId of parameters) allParameterIds.add(parameterId)
      for (const partId of parts) allPartIds.add(partId)
    }

    for (const parameterId of allParameterIds) {
      const shouldEnable = [...activeOv].some((overlayName) => {
        return overlayRules[overlayName]?.parameters?.includes(parameterId)
      })

      const idObj = resolveParamIdObject(core, parameterId)
      if (!idObj) continue
      if (typeof core.getParameterIndex !== 'function' || typeof core.setParameterValueByIndex !== 'function') continue

      const idx = core.getParameterIndex(idObj)
      if (idx >= 0) {
        core.setParameterValueByIndex(idx, shouldEnable ? 1 : 0, 1)
      }
    }

    for (const partId of allPartIds) {
      const shouldEnable = [...activeOv].some((overlayName) => {
        return overlayRules[overlayName]?.parts?.includes(partId)
      })

      const idObj = resolvePartIdObject(core, partId)
      if (!idObj || typeof core.getPartIndex !== 'function' || typeof core.setPartOpacityByIndex !== 'function') continue

      const idx = core.getPartIndex(idObj)
      if (idx >= 0) {
        core.setPartOpacityByIndex(idx, shouldEnable ? 1 : 0)
      }
    }
  }

  // 应用 overlay 状态到 model
  window.__applyOverlayState = function(model) {
    if (!model) return
    const core = getCubismCoreModel(model)
    window.__applyOverlayStateToCore(core)
  }

  // 同步表情状态：先设置基础表情，再应用 overlay
  window.__syncExpressionState = function(model) {
    const state = window.__expressionControlsState
    if (!model) model = getCurrentCubism5Model()
    if (!model) return

    try {
      // 先重置核心模型的表情相关参数
      const core = getCubismCoreModel(model)
      if (core) {
        const expressionParams = ['ParamEyeSmile', 'ParamEyeOpen', 'ParamTear']
        expressionParams.forEach(paramName => {
          const paramId = resolveParamIdObject(core, paramName)
          if (paramId) {
            const idx = core.getParameterIndex(paramId)
            if (idx >= 0) {
              core.setParameterValueByIndex(idx, 0, 1)
            }
          }
        })
      }

      if (state.currentBaseExpression) {
        model.setExpression?.(state.currentBaseExpression)
      }

      window.__applyOverlayState(model)
    } catch (err) {
      console.error('[Expression Controls] Error syncing expression state:', err)
    }
  }

  // 应用语音口型状态到 core model
  window.__applySpeechStateToCore = function(core) {
    if (!core) return
    const paramId = resolveParamIdObject(core, 'ParamMouthOpenY')
    if (paramId && typeof core.getParameterIndex === 'function' && typeof core.setParameterValueByIndex === 'function') {
      const idx = core.getParameterIndex(paramId)
      if (idx >= 0) {
        core.setParameterValueByIndex(idx, window.__speechMouthOpenY || 0, 1)
      }
    }
  }
}

// ============================================================
// Monkey-patch core.update 实现 overlay
// ============================================================

function setupExpressionWithOverlay() {
  const model = getCurrentCubism5Model()
  if (!model || model.__expressionOverlayPatched) return

  // 设置随机表情方法
  model.setRandomExpression = function() {
    const baseExpr = baseExpressions[Math.floor(Math.random() * baseExpressions.length)]
    window.__expressionControlsState.currentBaseExpression = baseExpr
    currentBaseExpression.value = baseExpr
    window.__syncExpressionState(model)
  }

  // Monkey-patch core.update
  const core = getCubismCoreModel(model)

  if (core && typeof core.update === 'function' && !core.__overlayUpdatePatched) {
    const oldCoreUpdate = core.update.bind(core)
    core.update = function(...args) {
      try {
        // 每帧更新前：应用 overlay 参数
        window.__applyOverlayStateToCore?.(core)
      } catch (error) {
        // 静默处理
      }
      const result = oldCoreUpdate(...args)
      try {
        // 每帧更新后：应用 speech 参数（口型）
        window.__applySpeechStateToCore?.(core)
      } catch (error) {
        // 静默处理
      }
      return result
    }
    core.__overlayUpdatePatched = true
  }

  model.__expressionOverlayPatched = true
}

// ============================================================
// HitTest 防护（防止模型未就绪时点击报错）
// ============================================================

function patchHitTestGuard() {
  const model = getCurrentCubism5Model()
  if (!model || model.__hitTestGuardPatched || typeof model.hitTest !== 'function') return
  const oldHitTest = model.hitTest.bind(model)
  model.hitTest = (...args) => {
    try {
      if (!model || !model._modelSetting || !model._model) return false
      if (typeof model._model?.getHitAreasCount !== 'function') return false
      return oldHitTest(...args)
    } catch (_) {
      return false
    }
  }
  model.__hitTestGuardPatched = true
}

function patchModelPrototypeHitTestGuard() {
  const model = getCurrentCubism5Model()
  const proto = model ? Object.getPrototypeOf(model) : null
  if (!proto || proto.__hitTestPrototypeGuardPatched || typeof proto.hitTest !== 'function') return
  const oldHitTest = proto.hitTest
  proto.hitTest = function(...args) {
    try {
      if (!this || !this._modelSetting || !this._model) return false
      if (typeof this._model?.getHitAreasCount !== 'function') return false
      return oldHitTest.apply(this, args)
    } catch (_) {
      return false
    }
  }
  proto.__hitTestPrototypeGuardPatched = true
}

function patchLive2DManagerEventGuards() {
  const manager = window.__live2dWidgetModelManager?.cubism5model?.subdelegates?.at?.(0)?.getLive2DManager?.()
  if (!manager || manager.__eventGuardsPatched) return

  const wrap = (methodName) => {
    if (typeof manager[methodName] !== 'function') return
    const original = manager[methodName].bind(manager)
    manager[methodName] = (...args) => {
      try {
        const model = getCurrentCubism5Model()
        if (!model || !model._modelSetting || !model._model) return false
        if (typeof model._model?.getHitAreasCount !== 'function') return false
        return original(...args)
      } catch (err) {
        const msg = String(err?.message || err || '')
        if (msg.includes('getHitAreasCount') || msg.includes('_modelSetting') || msg.includes('null') || msg.includes('undefined')) {
          return false
        }
        throw err
      }
    }
  }

  wrap('onMouseMove')
  wrap('onMouseEnd')
  wrap('onTap')
  manager.__eventGuardsPatched = true
}

// ============================================================
// 模型修补循环 - 每300ms检查并patch模型
// ============================================================

function startModelPatchLoop() {
  if (window.__huahuoModelPatchLoopStarted) return
  window.__huahuoModelPatchLoopStarted = true

  modelPatchLoopId = window.setInterval(() => {
    patchHitTestGuard()
    patchModelPrototypeHitTestGuard()
    patchLive2DManagerEventGuards()
    setupExpressionWithOverlay()
  }, 300)
}

function stopModelPatchLoop() {
  if (modelPatchLoopId) {
    clearInterval(modelPatchLoopId)
    modelPatchLoopId = null
  }
  window.__huahuoModelPatchLoopStarted = false
}

// ============================================================
// 表情面板交互
// ============================================================

function setBaseExpression(exprName) {
  currentBaseExpression.value = exprName
  window.__expressionControlsState.currentBaseExpression = exprName
  const model = getCurrentCubism5Model()
  if (model) {
    window.__syncExpressionState(model)
  }
}

function toggleOverlay(overlayName, checked) {
  if (checked) {
    activeOverlays.value.add(overlayName)
    window.__expressionControlsState.activeOverlays.add(overlayName)
  } else {
    activeOverlays.value.delete(overlayName)
    window.__expressionControlsState.activeOverlays.delete(overlayName)
  }
  const model = getCurrentCubism5Model()
  if (model) {
    window.__syncExpressionState(model)
  }
}

function switchExpression() {
  const randomExpr = baseExpressions[Math.floor(Math.random() * baseExpressions.length)]
  setBaseExpression(randomExpr)
}

// ============================================================
// 语音 Live2D 钩子
// ============================================================

function setupVoiceHooks() {
  window.__voiceLive2dHooks = {
    onStreamStart: () => { window.__syncExpressionState && setBaseExpression('07 星星眼') },
    onDelta: (payload) => {
      const textLen = (payload?.text || payload || '').length
      const openY = Math.min(1, textLen / 20)
      window.__speechMouthOpenY = openY
      const emotion = detectEmotionByText(payload?.text || '')
      if (emotion) {
        const expr = getExpressionByEmotion(emotion)
        if (expr) setBaseExpression(expr)
      }
    },
    onStreamEnd: () => {
      setBaseExpression('06 0.0')
      window.__speechMouthOpenY = 0
    },
    onSpeechStart: () => { setBaseExpression('07 星星眼') },
    onSpeechPulse: (payload) => {
      window.__speechMouthOpenY = payload?.intensity || 0.5
    },
    onSpeechEnd: () => {
      setBaseExpression('06 0.0')
      window.__speechMouthOpenY = 0
    },
  }
}

// ============================================================
// Live2D 加载流程（参考 my_huahuo 的 autoload.js 方式）
// ============================================================

async function loadLive2DLibraries() {
  if (window.initWidget) return

  const live2dPath = '/live2d-widget-dist/'

  // 加载 CSS
  if (!document.querySelector('link[href*="waifu.css"]')) {
    const link = document.createElement('link')
    link.rel = 'stylesheet'
    link.href = live2dPath + 'waifu.css'
    document.head.appendChild(link)
  }

  // 加载 waifu-tips.js
  // 注意：waifu-tips.js 末尾有 export 语句，必须使用 type: 'module' 加载
  // 但 module 脚本中 window.initWidget 赋值仍然有效（显式赋值到 window 对象）
  await new Promise((resolve, reject) => {
    if (document.querySelector('script[src*="live2d-widget-dist/waifu-tips"]')) {
      resolve()
      return
    }
    const script = document.createElement('script')
    // waifu-tips.js 包含 export 语句，必须用 module 方式加载
    script.type = 'module'
    script.src = live2dPath + 'waifu-tips.js'
    script.onload = () => resolve()
    script.onerror = () => reject(new Error('Failed to load waifu-tips.js'))
    document.head.appendChild(script)
  })

  // 轮询等待 window.initWidget 可用（参考 my_huahuo 的 tryInit 方式）
  await new Promise((resolve) => {
    let attempts = 0
    const maxAttempts = 20 // 最多等 10 秒
    const interval = setInterval(() => {
      attempts++
      if (typeof window.initWidget === 'function' || attempts >= maxAttempts) {
        clearInterval(interval)
        resolve()
      }
    }, 500)
  })
}

async function initLive2D() {
  try {
    loadError.value = false

    // 清理可能阻碍加载的 localStorage 项
    window.localStorage.removeItem('waifu-display')
    window.localStorage.removeItem('modelId')
    window.localStorage.removeItem('modelTexturesId')

    // 加载库文件
    await loadLive2DLibraries()

    if (typeof window.initWidget !== 'function') {
      console.warn('[Live2D] initWidget not available after loading libraries')
      loadError.value = true
      return
    }

    console.log('[Live2D] initWidget found, initializing...')

    // 调用 initWidget（参考 my_huahuo 的参数配置）
    window.initWidget({
      waifuPath: '/live2d-widget-dist/waifu-huahuo.json',
      cubism2Path: '/live2d-widget-dist/live2d.min.js',
      cubism5Path: '/live2d-widget-dist/live2dcubismcore.min.js',
      modelId: 0,
      tools: [],
      drag: false,
      logLevel: 'warn'
    })

    // 等待模型加载完成（监听 live2d:model-ready 事件 + 轮询 canvas）
    await new Promise((resolve) => {
      let resolved = false

      // 方式1：监听 live2d:model-ready 事件
      const onModelReady = () => {
        if (!resolved) {
          resolved = true
          window.removeEventListener('live2d:model-ready', onModelReady)
          resolve()
        }
      }
      window.addEventListener('live2d:model-ready', onModelReady)

      // 方式2：轮询 canvas 作为备用
      let attempts = 0
      const maxAttempts = 30 // 最多等 9 秒
      const interval = setInterval(() => {
        attempts++
        const canvas = document.getElementById('live2d')
        if ((canvas && canvas.width > 0) || attempts >= maxAttempts) {
          if (!resolved) {
            resolved = true
            clearInterval(interval)
            window.removeEventListener('live2d:model-ready', onModelReady)
            resolve()
          }
        }
      }, 300)
    })

    loaded.value = true

    // 绑定点击事件到 waifu 元素
    const waifuEl = document.getElementById('waifu')
    if (waifuEl) {
      waifuEl.addEventListener('click', () => openPanel())
      waifuEl.style.cursor = 'pointer'
      const hint = document.createElement('div')
      hint.className = 'waifu-click-hint'
      hint.textContent = '点击对话'
      waifuEl.appendChild(hint)
    }

    // 隐藏 waifu-toggle 按钮（我们有自己的 UI）
    const toggleEl = document.getElementById('waifu-toggle')
    if (toggleEl) {
      toggleEl.style.display = 'none'
    }

    // 隐藏 waifu-tool 工具栏
    const toolEl = document.getElementById('waifu-tool')
    if (toolEl) {
      toolEl.style.display = 'none'
    }

    // 启动模型修补循环
    startModelPatchLoop()

    // 初始化默认表情
    setTimeout(() => {
      const model = getCurrentCubism5Model()
      if (model) {
        window.__syncExpressionState(model)
      }
    }, 1000)

  } catch (err) {
    console.warn('Live2D init error:', err.message)
    loadError.value = true
  }
}

function retryInit() {
  if (retryCount >= 3) { loadError.value = false; return }
  retryCount++
  loadError.value = false
  loaded.value = false
  initLive2D()
}

function scrollToBottom() {
  nextTick(() => { if (messagesRef.value) messagesRef.value.scrollTop = messagesRef.value.scrollHeight })
}

watch(messages, () => scrollToBottom(), { deep: true })
watch(streamingText, () => scrollToBottom())

async function sendMessage() {
  const text = inputText.value.trim()
  if (!text || isStreaming.value) return
  messages.value.push({ role: 'user', content: text })
  inputText.value = ''
  isStreaming.value = true
  streamingText.value = ''
  currentReplyText.value = ''
  currentResponseType.value = 'chat'
  currentNavigateData.value = null
  currentCapability.value = ''
  notifyLive2dHook('onStreamStart')

  let fullResponse = ''
  const MAX_RETRY = 2
  let retryCount = 0
  let success = false

  while (retryCount <= MAX_RETRY && !success) {
    try {
      const response = await chatStream(text, sessionId.value)
      if (!response.ok) throw new Error(`HTTP ${response.status}`)
      if (!response.body) throw new Error('响应体为空')

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''
      let lastChunkTime = Date.now()
      const CHUNK_TIMEOUT = 180000

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        lastChunkTime = Date.now()
        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          const trimmed = line.trim()
          if (!trimmed) continue

          if (trimmed.startsWith('sessionId:')) {
            sessionId.value = trimmed.slice(10).trim()
          } else if (trimmed.startsWith('type:')) {
            currentResponseType.value = trimmed.slice(5).trim()
          } else if (trimmed.startsWith('navigate:')) {
            try {
              currentNavigateData.value = JSON.parse(trimmed.slice(9))
            } catch (e) {}
          } else if (trimmed.startsWith('capability:')) {
            currentCapability.value = trimmed.slice(11).trim()
          } else if (trimmed.startsWith('delta:')) {
            const delta = trimmed.slice(6)
            streamingText.value += delta
            fullResponse += delta
            currentReplyText.value = fullResponse
            notifyLive2dHook('onDelta', { text: delta })
          } else if (trimmed.startsWith('error:')) {
            const errMsg = trimmed.slice(6)
            console.error('[AI Stream] Server error:', errMsg)
          }
        }

        if (Date.now() - lastChunkTime > CHUNK_TIMEOUT) {
          throw new Error('数据接收超时')
        }
      }

      if (buffer.trim()) {
        const trimmed = buffer.trim()
        if (trimmed.startsWith('delta:')) {
          const delta = trimmed.slice(6)
          streamingText.value += delta
          fullResponse += delta
        }
      }

      success = true
    } catch (err) {
      retryCount++
      console.error(`[AI Stream] Attempt ${retryCount} failed:`, err.message)
      if (retryCount > MAX_RETRY) {
        ElMessage.error('AI 对话服务暂时不可用，请稍后重试')
        break
      }
      await new Promise(r => setTimeout(r, 1000 * retryCount))
    }
  }

  if (fullResponse) {
    const msg = {
      role: 'assistant',
      content: fullResponse,
      type: currentResponseType.value || 'chat',
    }
    if (currentResponseType.value === 'navigate' && currentNavigateData.value) {
      msg.navigate = currentNavigateData.value
    }
    if (currentResponseType.value === 'agent_result' && currentCapability.value) {
      msg.capability = currentCapability.value
    }
    messages.value.push(msg)
  }

  isStreaming.value = false
  streamingText.value = ''
  notifyLive2dHook('onStreamEnd')
}

function sendQuickQuestion(q) { inputText.value = q; sendMessage() }

const CAPABILITY_LABELS = {
  project_idea: '项目创意生成',
  mock_defense: '模拟路演答辩',
  batch_review: '批量审核助手',
  smart_feedback: '智能反馈生成',
  review_draft: '评审意见草稿',
  score_check: '评分一致性检查',
  material_qa: '材料智能问答',
  bp_check: '商业计划书体检',
  roadshow: '路演稿生成',
  review_assist: '评审辅助',
  competition_recommend: '智能竞赛推荐',
}

function getCapabilityLabel(key) {
  return CAPABILITY_LABELS[key] || key
}

const router = useRouter()

function handleNavigate(route) {
  if (route) {
    router.push(route).catch(() => {})
  }
}

function toggleVoiceRecognition() { isListening.value ? stopVoiceRecognition() : startVoiceRecognition() }

function startVoiceRecognition() {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition
  if (SR) {
    recognition = new SR()
    recognition.lang = 'zh-CN'
    recognition.continuous = false
    recognition.interimResults = true
    recognition.onresult = (e) => {
      let final = '', interim = ''
      for (let i = e.resultIndex; i < e.results.length; i++) {
        if (e.results[i].isFinal) final += e.results[i][0].transcript
        else interim += e.results[i][0].transcript
      }
      if (interim) inputText.value = interim
      if (final) { inputText.value = final; nextTick(() => sendMessage()) }
    }
    recognition.onerror = (e) => { isListening.value = false; if (e.error !== 'no-speech') ElMessage.error('语音识别出错：' + e.error) }
    recognition.onend = () => { isListening.value = false }
    recognition.start()
    isListening.value = true
  } else {
    startFirefoxVoice()
  }
}

function stopVoiceRecognition() { if (recognition) { recognition.stop(); recognition = null }; isListening.value = false }

async function startFirefoxVoice() {
  try {
    isListening.value = true; isAsrProcessing.value = true
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    const mr = new MediaRecorder(stream, { mimeType: 'audio/webm' })
    const chunks = []
    mr.ondataavailable = (e) => { if (e.data.size > 0) chunks.push(e.data) }
    mr.onstop = async () => {
      stream.getTracks().forEach(t => t.stop()); isListening.value = false
      const blob = new Blob(chunks, { type: 'audio/webm' })
      const fd = new FormData(); fd.append('audio', blob, 'recording.webm')
      try {
        const { uploadAsrAudio } = await import('@/api/ai')
        const res = await uploadAsrAudio(fd)
        const result = await res.json()
        if (result.text) { inputText.value = result.text; nextTick(() => sendMessage()) }
        else ElMessage.error('语音识别失败')
      } catch (err) { ElMessage.error('语音识别失败：' + err.message) }
      finally { isAsrProcessing.value = false }
    }
    mr.start()
    setTimeout(() => { if (mr.state === 'recording') mr.stop() }, 5000)
  } catch (err) { isListening.value = false; isAsrProcessing.value = false; ElMessage.error('无法访问麦克风：' + err.message) }
}

function toggleSpeech() {
  if (isSpeaking.value) { window.speechSynthesis.cancel(); isSpeaking.value = false; notifyLive2dHook('onSpeechEnd'); stopSpeechMouthPulse(); return }
  if (!currentReplyText.value) return
  const u = new SpeechSynthesisUtterance(currentReplyText.value)
  u.lang = 'zh-CN'; u.rate = 1.0; u.pitch = 1.0
  const voices = window.speechSynthesis.getVoices()
  const zhVoice = voices.find(v => v.lang.startsWith('zh') && v.name.includes('Female')) || voices.find(v => v.lang.startsWith('zh'))
  if (zhVoice) u.voice = zhVoice
  u.onstart = () => { isSpeaking.value = true; notifyLive2dHook('onSpeechStart'); startSpeechMouthPulse() }
  u.onend = () => { isSpeaking.value = false; notifyLive2dHook('onSpeechEnd'); stopSpeechMouthPulse() }
  u.onerror = () => { isSpeaking.value = false; notifyLive2dHook('onSpeechEnd'); stopSpeechMouthPulse() }
  window.speechSynthesis.speak(u)
}

function startSpeechMouthPulse() {
  stopSpeechMouthPulse()
  const startTime = Date.now()
  speechPulseInterval = setInterval(() => {
    const elapsed = (Date.now() - startTime) / 1000
    const intensity = 0.3 + 0.5 * Math.abs(Math.sin(elapsed * 6))
    notifyLive2dHook('onSpeechPulse', { intensity })
  }, 80)
}

function stopSpeechMouthPulse() { if (speechPulseInterval) { clearInterval(speechPulseInterval); speechPulseInterval = null } }

function clearMessages() {
  messages.value = []
  currentReplyText.value = ''
  streamingText.value = ''
  sessionId.value = ''
  currentResponseType.value = 'chat'
  currentNavigateData.value = null
  currentCapability.value = ''
}
function newSession() { clearMessages() }

async function handleAnalysis() {
  if (!analysisForm.project_name && !analysisForm.description) { ElMessage.warning('请填写项目信息'); return }
  analysisLoading.value = true; analysisResult.value = ''
  notifyLive2dHook('onStreamStart')
  try {
    const res = await generateAnalysis(analysisForm)
    if (res.code === 200) analysisResult.value = res.data?.result || res.data?.content || '生成完成'
    else ElMessage.error(res.message || '生成失败')
  } catch (err) { ElMessage.error('AI 分析失败：' + err.message) }
  finally { analysisLoading.value = false; notifyLive2dHook('onStreamEnd') }
}

function copyAnalysisResult() {
  navigator.clipboard.writeText(analysisResult.value).then(() => ElMessage.success('已复制'))
}

function speakAnalysisResult() {
  if (!analysisResult.value) return
  currentReplyText.value = analysisResult.value
  toggleSpeech()
}

function startModelDrag(e) {
  e.preventDefault()
  e.stopPropagation()
  const waifuEl = document.getElementById('waifu')
  if (!waifuEl) return
  const rect = waifuEl.getBoundingClientRect()
  modelDragState = {
    dragging: true,
    startX: e.clientX,
    startY: e.clientY,
    origLeft: rect.left,
    origTop: rect.top
  }
  document.addEventListener('mousemove', onModelDrag)
  document.addEventListener('mouseup', stopModelDrag)
}

function startModelDragTouch(e) {
  const t = e.touches[0]
  const waifuEl = document.getElementById('waifu')
  if (!waifuEl) return
  const rect = waifuEl.getBoundingClientRect()
  modelDragState = {
    dragging: true,
    startX: t.clientX,
    startY: t.clientY,
    origLeft: rect.left,
    origTop: rect.top
  }
  document.addEventListener('touchmove', onModelDragTouch, { passive: false })
  document.addEventListener('touchend', stopModelDragTouch)
}

function onModelDrag(e) {
  if (!modelDragState.dragging) return
  const dx = e.clientX - modelDragState.startX
  const dy = e.clientY - modelDragState.startY
  const newLeft = modelDragState.origLeft + dx
  const newTop = modelDragState.origTop + dy
  applyModelPosition(newLeft, newTop)
}

function onModelDragTouch(e) {
  if (!modelDragState.dragging) return
  e.preventDefault()
  const t = e.touches[0]
  const dx = t.clientX - modelDragState.startX
  const dy = t.clientY - modelDragState.startY
  const newLeft = modelDragState.origLeft + dx
  const newTop = modelDragState.origTop + dy
  applyModelPosition(newLeft, newTop)
}

function applyModelPosition(left, top) {
  const waifuEl = document.getElementById('waifu')
  if (!waifuEl) return
  const maxX = window.innerWidth - waifuEl.offsetWidth
  const maxY = window.innerHeight - waifuEl.offsetHeight
  const clampedLeft = Math.max(0, Math.min(left, maxX))
  const clampedTop = Math.max(0, Math.min(top, maxY))
  waifuEl.style.left = clampedLeft + 'px'
  waifuEl.style.right = 'auto'
  waifuEl.style.bottom = 'auto'
  waifuEl.style.top = clampedTop + 'px'

  // 同步更新拖拽按钮位置到形象右侧
  const handleEl = document.getElementById('live2d-drag-handle')
  if (handleEl) {
    handleEl.style.left = (clampedLeft + waifuEl.offsetWidth - 4) + 'px'
    handleEl.style.top = (clampedTop + waifuEl.offsetHeight / 2 - 16) + 'px'
    handleEl.style.bottom = 'auto'
  }

  try {
    localStorage.setItem('huahuoModelPos', JSON.stringify({ left: clampedLeft, top: clampedTop }))
  } catch (_e) {}
}

function stopModelDrag() {
  modelDragState.dragging = false
  document.removeEventListener('mousemove', onModelDrag)
  document.removeEventListener('mouseup', stopModelDrag)
}

function stopModelDragTouch() {
  modelDragState.dragging = false
  document.removeEventListener('touchmove', onModelDragTouch)
  document.removeEventListener('touchend', stopModelDragTouch)
}

function startDrag(e) { dragState.dragging = true; dragState.startX = e.clientX - (panelPos.value.x || 0); dragState.startY = e.clientY - (panelPos.value.y || 0); document.addEventListener('mousemove', onDrag); document.addEventListener('mouseup', stopDrag) }
function startDragTouch(e) { const t = e.touches[0]; dragState.dragging = true; dragState.startX = t.clientX - (panelPos.value.x || 0); dragState.startY = t.clientY - (panelPos.value.y || 0); document.addEventListener('touchmove', onDragTouch, { passive: false }); document.addEventListener('touchend', stopDragTouch) }
function onDrag(e) { if (!dragState.dragging) return; panelPos.value = { x: e.clientX - dragState.startX, y: e.clientY - dragState.startY }; panelStyle.value = { transform: `translate(${panelPos.value.x}px, ${panelPos.value.y}px)` } }
function onDragTouch(e) { if (!dragState.dragging) return; e.preventDefault(); const t = e.touches[0]; panelPos.value = { x: t.clientX - dragState.startX, y: t.clientY - dragState.startY }; panelStyle.value = { transform: `translate(${panelPos.value.x}px, ${panelPos.value.y}px)` } }
function stopDrag() { dragState.dragging = false; document.removeEventListener('mousemove', onDrag); document.removeEventListener('mouseup', stopDrag); try { localStorage.setItem('huahuoPanelPos', JSON.stringify(panelPos.value)) } catch (_e) {} }
function stopDragTouch() { dragState.dragging = false; document.removeEventListener('touchmove', onDragTouch); document.removeEventListener('touchend', stopDragTouch); try { localStorage.setItem('huahuoPanelPos', JSON.stringify(panelPos.value)) } catch (_e) {} }

onMounted(() => {
  setupExpressionControls()
  setupVoiceHooks()
  initLive2D()
  window.addEventListener('open-huahuo-agent', handleOpenHuahuoAgent)
  try { const saved = localStorage.getItem('huahuoPanelPos'); if (saved) { panelPos.value = JSON.parse(saved); panelStyle.value = { transform: `translate(${panelPos.value.x}px, ${panelPos.value.y}px)` } } } catch (_e) {}
  try {
    const modelPos = localStorage.getItem('huahuoModelPos')
    if (modelPos) {
      const pos = JSON.parse(modelPos)
      const restorePos = () => {
        const waifuEl = document.getElementById('waifu')
        if (waifuEl) {
          waifuEl.style.left = pos.left + 'px'
          waifuEl.style.right = 'auto'
          waifuEl.style.bottom = 'auto'
          waifuEl.style.top = pos.top + 'px'
          // 同步恢复拖拽按钮位置
          const handleEl = document.getElementById('live2d-drag-handle')
          if (handleEl) {
            handleEl.style.left = (pos.left + waifuEl.offsetWidth - 4) + 'px'
            handleEl.style.top = (pos.top + waifuEl.offsetHeight / 2 - 16) + 'px'
            handleEl.style.bottom = 'auto'
          }
        }
      }
      setTimeout(restorePos, 2000)
    }
  } catch (_e) {}
  if (window.speechSynthesis) { window.speechSynthesis.getVoices(); window.speechSynthesis.onvoiceschanged = () => window.speechSynthesis.getVoices() }
})

onBeforeUnmount(() => {
  window.removeEventListener('open-huahuo-agent', handleOpenHuahuoAgent)
  stopVoiceRecognition()
  stopSpeechMouthPulse()
  stopModelPatchLoop()
  if (window.speechSynthesis) window.speechSynthesis.cancel()
  const waifuEl = document.getElementById('waifu')
  if (waifuEl) {
    waifuEl.style.display = 'none'
  }
})
</script>

<style>
.huahuo-assistant {
  z-index: 9999;
  position: fixed;
  bottom: 0;
  left: 20px;
}

#wafu-tool, #waifu-tool { display: none !important; }
#wafu-toggle, #waifu-toggle { display: none !important; }
#wafu-tips, #waifu-tips { display: none !important; }

#wafu, #waifu {
  position: fixed !important;
  left: 20px;
  right: auto;
  bottom: auto;
  top: auto;
  width: 300px;
  height: 300px;
  visibility: visible !important;
  z-index: 9999;
  cursor: grab;
  user-select: none;
}

#wafu:active, #waifu:active {
  cursor: grabbing;
}

#wafu.waifu-hidden, #waifu.waifu-hidden {
  display: block !important;
  visibility: visible !important;
}

.waifu-click-hint {
  text-align: center;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.7);
  background: rgba(0, 0, 0, 0.4);
  padding: 2px 12px;
  border-radius: 10px;
  margin-top: -4px;
  pointer-events: none;
  position: absolute;
  bottom: 8px;
  left: 50%;
  transform: translateX(-50%);
  white-space: nowrap;
}

.live2d-drag-handle {
  position: fixed;
  left: 316px;
  bottom: auto;
  top: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: rgba(15, 23, 42, 0.9);
  backdrop-filter: blur(8px);
  border-radius: 50%;
  color: #94a3b8;
  font-size: 11px;
  cursor: grab;
  user-select: none;
  white-space: nowrap;
  z-index: 10001;
  border: 1px solid rgba(6, 182, 212, 0.3);
  transition: color 0.2s, background 0.2s, opacity 0.3s;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
}

.live2d-drag-handle.panel-open {
  opacity: 0;
  pointer-events: none;
}

.live2d-drag-handle:hover {
  color: #e2e8f0;
  background: rgba(15, 23, 42, 0.95);
}

.live2d-drag-handle:active {
  cursor: grabbing;
}

.live2d-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  color: #06b6d4;
  font-size: 12px;
  padding: 10px 16px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 10px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.live2d-error {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #ef4444;
  font-size: 12px;
  padding: 8px 14px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  cursor: pointer;
}

/* 表情控制面板 */
.expression-panel {
  padding: 12px 16px;
  border-bottom: 1px solid rgba(6, 182, 212, 0.15);
  background: rgba(15, 23, 42, 0.6);
  max-height: 280px;
  overflow-y: auto;
}

.expression-panel::-webkit-scrollbar { width: 4px; }
.expression-panel::-webkit-scrollbar-thumb { background: rgba(6, 182, 212, 0.3); border-radius: 2px; }

.expression-section {
  margin-bottom: 10px;
}

.expression-section:last-child {
  margin-bottom: 0;
}

.expression-section-title {
  font-size: 12px;
  color: #94a3b8;
  margin-bottom: 8px;
  font-weight: 600;
}

.expression-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 6px;
}

.expression-item {
  padding: 6px 8px;
  border-radius: 8px;
  font-size: 12px;
  color: #cbd5e1;
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(6, 182, 212, 0.1);
  cursor: pointer;
  text-align: center;
  transition: all 0.2s ease;
  user-select: none;
}

.expression-item:hover {
  background: rgba(6, 182, 212, 0.15);
  border-color: rgba(6, 182, 212, 0.3);
  color: #e2e8f0;
}

.expression-item.active {
  background: rgba(6, 182, 212, 0.25);
  border-color: rgba(6, 182, 212, 0.5);
  color: #22d3ee;
  font-weight: 600;
}

.overlay-list {
  display: flex;
  gap: 12px;
}

.overlay-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #cbd5e1;
  cursor: pointer;
  user-select: none;
}

.overlay-item input[type="checkbox"] {
  accent-color: #06b6d4;
  width: 14px;
  height: 14px;
  cursor: pointer;
}

.overlay-item:hover {
  color: #e2e8f0;
}

.chat-panel {
  position: fixed;
  bottom: 20px;
  left: 20px;
  width: 400px;
  max-height: 580px;
  background: rgba(15, 23, 42, 0.96);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid rgba(6, 182, 212, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(6, 182, 212, 0.1);
  display: flex;
  flex-direction: column;
  z-index: 10000;
  overflow: hidden;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 16px;
  background: rgba(6, 182, 212, 0.1);
  border-bottom: 1px solid rgba(6, 182, 212, 0.15);
  cursor: move;
  user-select: none;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.panel-title {
  font-size: 14px;
  font-weight: 600;
  color: #e2e8f0;
}

.listening-tag {
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.header-actions {
  display: flex;
  gap: 2px;
}

.panel-body {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
}

.chat-mode, .analysis-mode, .agent-mode {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
}

.agent-mode {
  min-height: 0;
  overflow-y: auto;
}

.analysis-mode {
  padding: 16px;
  overflow-y: auto;
  max-height: 520px;
}

.analysis-mode :deep(.el-form-item) {
  margin-bottom: 12px;
}

.analysis-mode :deep(.el-form-item__label) {
  color: #94a3b8;
  font-size: 12px;
}

.analysis-mode :deep(.el-input__inner),
.analysis-mode :deep(.el-textarea__inner) {
  color: #e2e8f0 !important;
  background-color: rgba(30, 41, 59, 0.8) !important;
  border-color: rgba(6, 182, 212, 0.3) !important;
}

.analysis-mode :deep(.el-input__inner::placeholder),
.analysis-mode :deep(.el-textarea__inner::placeholder) {
  color: #64748b !important;
}

.analysis-mode :deep(.el-radio-button__inner) {
  color: #e2e8f0 !important;
  background-color: rgba(30, 41, 59, 0.6) !important;
  border-color: rgba(6, 182, 212, 0.3) !important;
}

.analysis-mode :deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
  color: #fff !important;
  background-color: #06b6d4 !important;
  border-color: #06b6d4 !important;
}

.analysis-result {
  margin-top: 12px;
  background: rgba(15, 23, 42, 0.6);
  border-radius: 10px;
  padding: 12px 14px;
  border: 1px solid rgba(6, 182, 212, 0.15);
}

.analysis-result :deep(.el-divider__text) {
  color: #06b6d4;
  font-size: 13px;
  font-weight: 600;
}

.analysis-result .markdown-body {
  color: #e2e8f0;
  font-size: 14px;
  line-height: 1.7;
}

.analysis-result .markdown-body h1,
.analysis-result .markdown-body h2,
.analysis-result .markdown-body h3,
.analysis-result .markdown-body h4,
.analysis-result .markdown-body h5,
.analysis-result .markdown-body h6 {
  color: #e2e8f0;
  font-size: 14px;
  font-weight: 600;
  margin: 6px 0 2px;
}

.analysis-result .markdown-body p {
  color: #e2e8f0;
  margin: 4px 0;
}

.analysis-result .markdown-body strong {
  color: #22d3ee;
}

.analysis-result .markdown-body ul,
.analysis-result .markdown-body ol {
  color: #e2e8f0;
}

.analysis-result .markdown-body li {
  color: #e2e8f0;
}

.analysis-result .markdown-body table {
  color: #e2e8f0;
}

.analysis-result .markdown-body th {
  color: #06b6d4;
  background: rgba(6, 182, 212, 0.15);
}

.analysis-result .markdown-body td {
  color: #e2e8f0;
}

.analysis-result .markdown-body code {
  color: #22d3ee;
  background: rgba(6, 182, 212, 0.1);
}

.analysis-result .markdown-body blockquote {
  color: rgba(255,255,255,0.7);
  border-left-color: rgba(6, 182, 212, 0.4);
}

.analysis-result .markdown-body hr {
  border-top-color: rgba(255,255,255,0.1);
}

.analysis-actions {
  margin-top: 8px;
  display: flex;
  gap: 8px;
}

.analysis-actions {
  display: flex;
  gap: 12px;
  margin-top: 8px;
}

.mode-switch-hint {
  text-align: center;
  margin-top: 12px;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 12px 16px;
  max-height: 400px;
  min-height: 200px;
}

.chat-messages::-webkit-scrollbar { width: 4px; }
.chat-messages::-webkit-scrollbar-thumb { background: rgba(6, 182, 212, 0.3); border-radius: 2px; }

.chat-empty {
  text-align: center;
  color: #94a3b8;
  padding: 20px 0;
}

.chat-empty p { margin: 6px 0; font-size: 13px; }

.quick-questions {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  justify-content: center;
  margin-top: 10px;
}

.message-item {
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
  align-items: flex-start;
}

.message-item.user { flex-direction: row-reverse; }

.message-avatar {
  font-size: 18px;
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.message-content {
  max-width: 360px;
  padding: 8px 12px;
  border-radius: 10px;
  font-size: 14px;
  line-height: 1.6;
  word-break: break-word;
}

.message-item.user .message-content {
  background: rgba(6, 182, 212, 0.2);
  color: #e2e8f0;
  border-bottom-right-radius: 4px;
}

.message-item.assistant .message-content {
  background: rgba(30, 41, 59, 0.8);
  color: #e2e8f0;
  border-bottom-left-radius: 4px;
}

.message-item.assistant .message-content .markdown-body {
  font-size: 14px;
  line-height: 1.6;
}

.message-item.assistant .message-content .markdown-body h1,
.message-item.assistant .message-content .markdown-body h2,
.message-item.assistant .message-content .markdown-body h3,
.message-item.assistant .message-content .markdown-body h4,
.message-item.assistant .message-content .markdown-body h5,
.message-item.assistant .message-content .markdown-body h6 {
  font-size: 14px;
  font-weight: 600;
  margin: 6px 0 2px;
  color: inherit;
}

.message-content.streaming { min-height: 20px; }

.cursor-blink {
  animation: blink 1s step-end infinite;
  color: #06b6d4;
}

.message-actions {
  margin-top: 8px;
}

.message-capability-tag {
  margin-top: 6px;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.chat-input-area {
  padding: 10px 16px;
  border-top: 1px solid rgba(6, 182, 212, 0.15);
  background: rgba(15, 23, 42, 0.8);
}

.voice-controls {
  display: flex;
  gap: 6px;
  margin-top: 8px;
  justify-content: center;
  align-items: center;
}

.markdown-body {
  font-size: 14px;
  line-height: 1.7;
  word-break: break-word;
}

.markdown-body :deep(h1), .markdown-body :deep(h2), .markdown-body :deep(h3),
.markdown-body :deep(h4), .markdown-body :deep(h5), .markdown-body :deep(h6) {
  margin: 8px 0 4px;
  font-weight: 600;
  font-size: 14px;
  color: inherit;
}
.markdown-body :deep(h1)::before { content: ''; }
.markdown-body :deep(p) { margin: 4px 0; }
.markdown-body :deep(ul), .markdown-body :deep(ol) { padding-left: 16px; margin: 4px 0; }
.markdown-body :deep(li) { margin: 2px 0; }
.markdown-body :deep(strong) { color: #22d3ee; font-weight: 600; }
.markdown-body :deep(em) { font-style: italic; }
.markdown-body :deep(blockquote) { border-left: 3px solid rgba(6, 182, 212, 0.4); padding-left: 10px; margin: 6px 0; color: rgba(255,255,255,0.7); }
.markdown-body :deep(hr) { border: none; border-top: 1px solid rgba(255,255,255,0.1); margin: 8px 0; }
.markdown-body :deep(table) { width: 100%; border-collapse: collapse; margin: 6px 0; font-size: 13px; }
.markdown-body :deep(th), .markdown-body :deep(td) { border: 1px solid rgba(6, 182, 212, 0.2); padding: 4px 8px; text-align: left; }
.markdown-body :deep(th) { background: rgba(6, 182, 212, 0.15); color: #06b6d4; font-weight: 600; }
.markdown-body :deep(code) { background: rgba(6, 182, 212, 0.1); padding: 1px 5px; border-radius: 3px; font-size: 13px; }
.markdown-body :deep(pre) { background: rgba(0, 0, 0, 0.3); padding: 10px; border-radius: 6px; overflow-x: auto; margin: 6px 0; }
.markdown-body :deep(pre code) { background: none; padding: 0; font-size: 13px; }

.panel-slide-enter-active, .panel-slide-leave-active {
  transition: all 0.3s ease;
}

.panel-slide-enter-from {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}

.panel-slide-leave-to {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}
</style>

<style>
.chat-panel .el-form-item__label {
  color: #94a3b8 !important;
  font-size: 12px !important;
}

.chat-panel .el-input__inner,
.chat-panel .el-textarea__inner {
  color: #e2e8f0 !important;
  background-color: transparent !important;
  border-color: rgba(6, 182, 212, 0.3) !important;
}

.chat-panel .el-input__inner::placeholder,
.chat-panel .el-textarea__inner::placeholder {
  color: #64748b !important;
}

.chat-panel .el-radio-button__inner {
  color: #e2e8f0 !important;
  background-color: transparent !important;
  border-color: rgba(6, 182, 212, 0.3) !important;
}

.chat-panel .el-radio-button__original-radio:checked + .el-radio-button__inner {
  color: #fff !important;
  background-color: #06b6d4 !important;
  border-color: #06b6d4 !important;
}

.chat-panel .el-select .el-input__inner {
  color: #e2e8f0 !important;
  background-color: transparent !important;
  border-color: rgba(6, 182, 212, 0.3) !important;
}

.chat-panel .el-select-dropdown {
  background-color: rgba(15, 23, 42, 0.95) !important;
  border: 1px solid rgba(6, 182, 212, 0.3) !important;
}

.chat-panel .el-select-dropdown__item {
  color: #e2e8f0 !important;
}

.chat-panel .el-select-dropdown__item.hover,
.chat-panel .el-select-dropdown__item:hover {
  background-color: rgba(6, 182, 212, 0.15) !important;
}

.chat-panel .el-select-dropdown__item.selected {
  color: #06b6d4 !important;
  font-weight: 600;
}

.chat-panel .el-divider__text {
  color: #06b6d4 !important;
  font-size: 13px !important;
  font-weight: 600;
}

.chat-panel .el-input-group__append {
  background-color: rgba(6, 182, 212, 0.2) !important;
  border-color: rgba(6, 182, 212, 0.3) !important;
  color: #06b6d4 !important;
  box-shadow: none !important;
}
</style>
