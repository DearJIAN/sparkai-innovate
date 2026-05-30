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

      <!-- 对话面板（整合版） -->
      <transition name="panel-slide">
        <div v-if="panelOpen" ref="panelRef" class="chat-panel" :style="panelStyle">
          <div class="panel-header">
            <div class="header-drag-area" @mousedown="startDrag" @touchstart="startDragTouch">
              <span class="panel-title">🤖 火花 AI 助手</span>
              <el-tag v-if="isListening" type="danger" size="small" effect="light" class="listening-tag">录音中 {{ voiceRemainingSeconds }}s</el-tag>
              <el-tag v-else-if="isAsrProcessing" type="warning" size="small" effect="light" class="asr-tag">识别中 {{ asrRemainingSeconds }}s</el-tag>
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
          <!-- 右下角缩放手柄 -->
          <div class="panel-resize-handle" @mousedown.stop="startResize" title="拖拽调整大小">
            <svg class="resize-icon" viewBox="0 0 16 16" width="16" height="16">
              <path d="M2 14 L14 2 M6 14 L14 6 M10 14 L14 10" stroke="rgba(59, 130, 246, 0.6)" stroke-width="2" fill="none" stroke-linecap="round"/>
            </svg>
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
                <div class="chat-input-row">
                  <el-input
                    v-model="inputText"
                    type="textarea"
                    :autosize="{ minRows: 1, maxRows: 5 }"
                    placeholder="输入消息..."
                    @keydown.enter.exact.prevent="sendMessage"
                    :disabled="isStreaming"
                    clearable
                  />
                  <el-button class="chat-send-btn" @click="sendMessage" :loading="isStreaming" :disabled="!inputText.trim()">发送</el-button>
                </div>
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
import DOMPurify from 'dompurify'
import { chatStream, generateAnalysis } from '@/api/ai'
import { synthesizeTts } from '@/api/ai'
import { ElMessage } from 'element-plus'
import { Loading, WarningFilled, MagicStick, ArrowDown, Microphone, Delete, Plus, VideoPause, VideoPlay } from '@element-plus/icons-vue'
import { useLive2d } from '@/composables/useLive2d'
import AgentPanel from '@/views/ai-assistant/AgentPanel.vue'
import { useUserStore } from '@/stores/user'
import { withApiBase } from '@/utils/appBase'

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
const panelSize = ref({ width: 400, height: 580 })
let resizeState = { resizing: false, startX: 0, startY: 0, startW: 0, startH: 0 }
let isMobile = ref(false)
let recognition = null
let speechUtterance = null
let ttsAudio = null
let recognitionStartAt = 0
let recognitionFinalText = ''
let recognitionInterimText = ''
let recognitionManualStop = false
let recognitionStopTimer = null
let recognitionForceFinalizeTimer = null
let recognitionActive = false
let suppressAutoSendOnFinalize = false
let recognitionRestartAttempts = 0
let asrMediaRecorder = null
let asrMediaStream = null
let asrChunks = []
let asrManualStop = false
let asrTextPendingAutoSpeak = false
let listeningCountdownTimer = null
let listeningWindowStartAt = 0
const VOICE_LISTEN_MAX_MS = 60000
const voiceRemainingSeconds = ref(Math.ceil(VOICE_LISTEN_MAX_MS / 1000))
const ASR_PROCESS_MAX_MS = 15000
const asrRemainingSeconds = ref(Math.ceil(ASR_PROCESS_MAX_MS / 1000))
let asrCountdownTimer = null
let asrProcessStartAt = 0
let pendingAudioPlayToken = 0

function startListeningCountdown() {
  if (listeningCountdownTimer) clearInterval(listeningCountdownTimer)
  const tick = () => {
    const remain = Math.max(0, VOICE_LISTEN_MAX_MS - (Date.now() - listeningWindowStartAt))
    voiceRemainingSeconds.value = Math.max(0, Math.ceil(remain / 1000))
  }
  tick()
  listeningCountdownTimer = setInterval(tick, 200)
}

function stopListeningCountdown(reset = true) {
  if (listeningCountdownTimer) {
    clearInterval(listeningCountdownTimer)
    listeningCountdownTimer = null
  }
  if (reset) voiceRemainingSeconds.value = Math.ceil(VOICE_LISTEN_MAX_MS / 1000)
}

function startAsrCountdown() {
  if (asrCountdownTimer) clearInterval(asrCountdownTimer)
  asrProcessStartAt = Date.now()
  const tick = () => {
    const remain = Math.max(0, ASR_PROCESS_MAX_MS - (Date.now() - asrProcessStartAt))
    asrRemainingSeconds.value = Math.max(0, Math.ceil(remain / 1000))
  }
  tick()
  asrCountdownTimer = setInterval(tick, 200)
}

function stopAsrCountdown(reset = true) {
  if (asrCountdownTimer) {
    clearInterval(asrCountdownTimer)
    asrCountdownTimer = null
  }
  if (reset) asrRemainingSeconds.value = Math.ceil(ASR_PROCESS_MAX_MS / 1000)
}

function syncInputFromRecognition() {
  inputText.value = `${recognitionFinalText}${recognitionInterimText}`
}

function finalizeRecognitionAndSend() {
  if (recognitionStopTimer) { clearTimeout(recognitionStopTimer); recognitionStopTimer = null }
  if (recognitionForceFinalizeTimer) { clearTimeout(recognitionForceFinalizeTimer); recognitionForceFinalizeTimer = null }
  stopListeningCountdown()
  recognitionActive = false
  isListening.value = false
  const finalText = (recognitionFinalText + recognitionInterimText || inputText.value || '').trim()
  recognitionFinalText = ''
  recognitionInterimText = ''
  recognition = null
  if (finalText && !suppressAutoSendOnFinalize) {
    inputText.value = finalText
    nextTick(() => sendMessage({ autoSpeak: true }))
  }
  suppressAutoSendOnFinalize = false
}
let dragState = { dragging: false, startX: 0, startY: 0 }
let modelDragState = { dragging: false, startX: 0, startY: 0, origLeft: 0, origBottom: 0 }
let modelPatchLoopId = null
let autoExpressionTimer = null
let live2dInitPromise = null

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
    return DOMPurify.sanitize(html, {
      USE_PROFILES: { html: true },
      ADD_ATTR: ['target', 'rel']
    })
  } catch {
    return DOMPurify.sanitize(String(text))
  }
}

function openPanel() {
  // 如果正在拖拽 Live2D 模型，不打开面板
  if (isModelDragging) return
  panelOpen.value = true
}

function closePanel() {
  panelOpen.value = false
  expressionPanelOpen.value = false
}

function startAutoExpression() {
  stopAutoExpression()
  // 使用递归 setTimeout 代替 setInterval，实现随机间隔（15-25秒）
  // 避免固定间隔导致的机械感，减少表情切换频率
  const scheduleNextExpression = () => {
    const randomDelay = 15000 + Math.random() * 10000 // 15-25秒随机间隔
    autoExpressionTimer = window.setTimeout(() => {
      if (!isStreaming.value && !isSpeaking.value) {
        switchExpression()
      }
      scheduleNextExpression()
    }, randomDelay)
  }
  scheduleNextExpression()
}

function stopAutoExpression() {
  if (autoExpressionTimer) {
    clearInterval(autoExpressionTimer)
    autoExpressionTimer = null
  }
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
  // 注意：只处理 overlay 特有的参数，不触碰表情参数（ParamEyeSmile, ParamEyeOpen, ParamTear）
  // 避免与表情系统冲突导致眼睛闪烁
  const __expressionParamNames = new Set(['ParamEyeSmile', 'ParamEyeOpen', 'ParamTear'])
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
      // 跳过表情相关参数，避免与 setExpression 冲突
      if (__expressionParamNames.has(parameterId)) continue

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
  // 增加防抖，避免短时间内多次切换导致闪烁
  let __syncExpressionDebounceTimer = null
  window.__syncExpressionState = function(modelOrExpression) {
    if (__syncExpressionDebounceTimer) {
      clearTimeout(__syncExpressionDebounceTimer)
    }
    __syncExpressionDebounceTimer = setTimeout(() => {
      _doSyncExpressionState(modelOrExpression)
    }, 150)
  }

  function _doSyncExpressionState(modelOrExpression) {
    const state = window.__expressionControlsState
    let model = modelOrExpression
    if (typeof modelOrExpression === 'string') {
      state.currentBaseExpression = modelOrExpression
      currentBaseExpression.value = modelOrExpression
      model = getCurrentCubism5Model()
    }
    if (!model) model = getCurrentCubism5Model()
    if (!model) return

    try {
      // 不再强制重置表情参数，让 setExpression 自行管理
      // 避免与 core.update 中的 overlay 应用冲突导致闪烁

      if (state.currentBaseExpression) {
        model.setExpression?.(state.currentBaseExpression)
      }

      window.__applyOverlayState(model)
    } catch (err) {
      console.error('[Expression Controls] Error syncing expression state:', err)
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
        window.__applyOverlayStateToCore?.(core)
      } catch (error) {
      }
      const result = oldCoreUpdate(...args)
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
    onStreamStart: () => {},
    onDelta: (payload) => {
      const emotion = detectEmotionByText(payload?.text || '')
      if (emotion) {
        const expr = getExpressionByEmotion(emotion)
        if (expr) setBaseExpression(expr)
      }
    },
    onStreamEnd: () => {},
    onSpeechStart: () => {},
    onSpeechPulse: () => {},
    onSpeechEnd: () => {},
  }
}

// ============================================================
// Live2D 加载流程（参考 my_huahuo 的 autoload.js 方式）
// ============================================================

async function loadLive2DLibraries() {
  const live2dPath = '/live2d-widget-dist/'

  const oldScripts = document.querySelectorAll('script[src*="live2d-widget-dist"]')
  oldScripts.forEach(s => s.remove())

  try { delete window.initWidget } catch (_) {}
  try { delete window.loadlive2d } catch (_) {}
  try { delete window.__live2dWidgetModelManager } catch (_) {}

  if (!document.querySelector('link[href*="waifu.css"]')) {
    const link = document.createElement('link')
    link.rel = 'stylesheet'
    link.href = live2dPath + 'waifu.css'
    document.head.appendChild(link)
  }

  await new Promise((resolve, reject) => {
    const script = document.createElement('script')
    script.type = 'module'
    script.src = live2dPath + 'waifu-tips.js?' + Date.now()
    script.onload = () => resolve()
    script.onerror = () => reject(new Error('Failed to load waifu-tips.js'))
    document.head.appendChild(script)
  })

  await new Promise((resolve, reject) => {
    let attempts = 0
    const maxAttempts = 30
    const interval = setInterval(() => {
      attempts++
      if (typeof window.initWidget === 'function') {
        clearInterval(interval)
        resolve()
      } else if (attempts >= maxAttempts) {
        clearInterval(interval)
        reject(new Error('initWidget not available after loading'))
      }
    }, 300)
  })
}

async function initLive2D() {
  if (live2dInitPromise) return live2dInitPromise
  live2dInitPromise = doInitLive2D().finally(() => {
    live2dInitPromise = null
  })
  return live2dInitPromise
}

async function doInitLive2D() {
  loadError.value = false
  loaded.value = false

  const oldWaifu = document.getElementById('waifu')
  if (oldWaifu) oldWaifu.remove()
  const oldToggle = document.getElementById('waifu-toggle')
  if (oldToggle) oldToggle.remove()
  const oldTool = document.getElementById('waifu-tool')
  if (oldTool) oldTool.remove()

  window.localStorage.removeItem('waifu-display')
  window.localStorage.removeItem('modelId')
  window.localStorage.removeItem('modelTexturesId')

  let initSuccess = false
  let retries = 0
  const maxRetries = 2

  while (!initSuccess && retries <= maxRetries) {
    try {
      await loadLive2DLibraries()

      if (typeof window.initWidget !== 'function') {
        throw new Error('initWidget not available')
      }

      initSuccess = true
    } catch (error) {
      console.warn(`[Live2D] Load attempt ${retries + 1} failed:`, error.message)
      retries++
      if (retries <= maxRetries) {
        await new Promise(r => setTimeout(r, 1000 * retries))
      }
    }
  }

  if (!initSuccess) {
    console.error('[Live2D] Failed to load after all retries')
    loadError.value = true
    return
  }

  window.initWidget({
    waifuPath: '/live2d-widget-dist/waifu-huahuo.json',
    cubism2Path: '/live2d-widget-dist/live2d.min.js',
    cubism5Path: '/live2d-widget-dist/live2dcubismcore.min.js',
    modelId: 0,
    tools: [],
    drag: false,
    logLevel: 'warn'
  })

  await new Promise((resolve) => {
    let resolved = false

    const onModelReady = () => {
      if (!resolved) {
        resolved = true
        window.removeEventListener('live2d:model-ready', onModelReady)
        resolve()
      }
    }
    window.addEventListener('live2d:model-ready', onModelReady)

    let attempts = 0
    const maxAttempts = 30
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

  const waifuEl = document.getElementById('waifu')
  if (!waifuEl) return

  await new Promise((resolve) => {
    if (waifuEl.classList.contains('waifu-active')) {
      resolve()
      return
    }
    const observer = new MutationObserver((mutations) => {
      for (const m of mutations) {
        if (m.type === 'attributes' && m.attributeName === 'class') {
          if (waifuEl.classList.contains('waifu-active')) {
            observer.disconnect()
            resolve()
            return
          }
        }
      }
    })
    observer.observe(waifuEl, { attributes: true, attributeFilter: ['class'] })
    setTimeout(() => { observer.disconnect(); resolve() }, 5000)
  })

  try {
    waifuEl.style.left = '20px'
    waifuEl.style.bottom = '0'
    waifuEl.style.right = 'auto'
    waifuEl.style.top = 'auto'
    localStorage.removeItem('huahuoModelPos')

    waifuEl.style.opacity = '0'
    waifuEl.style.transform = 'translateY(320px)'
    waifuEl.style.pointerEvents = 'none'
    waifuEl.style.transition = 'opacity 0.5s ease-out, transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)'

    waifuEl.addEventListener('click', () => { switchExpression(); openPanel() })
    waifuEl.style.cursor = 'pointer'

    const existingHint = waifuEl.querySelector('.waifu-click-hint')
    if (existingHint) existingHint.remove()
    const hint = document.createElement('div')
    hint.className = 'waifu-click-hint'
    hint.textContent = '点击对话'
    waifuEl.appendChild(hint)

    // 移除旧的拖拽按钮（如果存在）
    const existingHandle = document.getElementById('live2d-drag-handle')
    if (existingHandle) existingHandle.remove()

    // 将拖拽事件绑定到 waifu 元素本身，按住人物即可拖拽
    waifuEl.addEventListener('mousedown', onWaifuMouseDown)
    waifuEl.addEventListener('touchstart', onWaifuTouchStart, { passive: false })

    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        waifuEl.style.opacity = '1'
        waifuEl.style.transform = 'translateY(0)'
        waifuEl.style.pointerEvents = 'auto'
        waifuEl.style.bottom = '0'

        const onTransitionEnd = () => {
          waifuEl.style.transition = 'left 0.3s ease-out, top 0.3s ease-out'
          waifuEl.style.transform = ''
          waifuEl.removeEventListener('transitionend', onTransitionEnd)
        }
        waifuEl.addEventListener('transitionend', onTransitionEnd)
      })
    })

    const toggleEl = document.getElementById('waifu-toggle')
    if (toggleEl) {
      toggleEl.style.display = 'none'
    }

    const toolEl = document.getElementById('waifu-tool')
    if (toolEl) {
      toolEl.style.display = 'none'
    }

    startModelPatchLoop()

    setTimeout(() => {
      const model = getCurrentCubism5Model()
      if (model) {
        window.__expressionControlsState = window.__expressionControlsState || {
          initialized: false,
          currentBaseExpression: null,
          activeOverlays: new Set(['水印'])
        }
        window.__expressionControlsState.activeOverlays.add('水印')
        activeOverlays.value = new Set(['水印'])
        window.__syncExpressionState(model)
      }
      startAutoExpression()
    }, 1500)
  } catch (err) {
    console.warn('Live2D init error:', err.message)
    loadError.value = true
  }
}

function retryInit() {
  if (retryCount >= 3) {
    ElMessage.warning('Live2D 连续加载失败，请刷新页面后再试')
    loadError.value = true
    return
  }
  retryCount++
  loadError.value = false
  loaded.value = false
  initLive2D().catch(() => {
    loadError.value = true
  })
}

function scrollToBottom() {
  nextTick(() => { if (messagesRef.value) messagesRef.value.scrollTop = messagesRef.value.scrollHeight })
}

watch(messages, () => scrollToBottom(), { deep: true })
watch(streamingText, () => scrollToBottom())
watch(panelOpen, (val) => {
  // 面板打开/关闭时的处理（拖拽按钮已移除，此 watch 保留用于后续扩展）
})

async function sendMessage(options = {}) {
  const { autoSpeak = true } = options
  const shouldAutoSpeak = autoSpeak || asrTextPendingAutoSpeak
  if (isListening.value) {
    suppressAutoSendOnFinalize = true
    stopVoiceRecognition(true)
  }
  const text = inputText.value.trim()
  if (!text || isStreaming.value) return
  asrTextPendingAutoSpeak = false
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
  let streamServerError = ''
  let hardStopByBilling = false
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
            streamServerError = errMsg
            if (errMsg.includes('Arrearage') || errMsg.includes('overdue-payment') || errMsg.includes('Access denied')) {
              hardStopByBilling = true
            }
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
      if (hardStopByBilling) break
    } catch (err) {
      retryCount++
      console.error(`[AI Stream] Attempt ${retryCount} failed:`, err.message)
      if (hardStopByBilling || retryCount > MAX_RETRY) {
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
    if (shouldAutoSpeak) {
      speakText(fullResponse, { forceRestart: true })
    }
  } else if (streamServerError) {
    const billingError = streamServerError.includes('Arrearage') || streamServerError.includes('overdue-payment') || streamServerError.includes('Access denied')
    messages.value.push({
      role: 'assistant',
      content: billingError
        ? '当前 AI 服务账号状态异常（欠费/权限受限），所以本次无法生成回复。请先在模型服务商控制台恢复账号状态后再试。'
        : `本次对话失败：${streamServerError}`
    })
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
  startFirefoxVoice()
}

function stopVoiceRecognition(manual = true) {
  asrManualStop = manual
  if (manual) suppressAutoSendOnFinalize = true
  if (recognitionStopTimer) { clearTimeout(recognitionStopTimer); recognitionStopTimer = null }
  if (asrMediaRecorder && asrMediaRecorder.state === 'recording') {
    try { asrMediaRecorder.stop() } catch (_e) {}
    return
  }
  isListening.value = false
  stopListeningCountdown()
}

async function startFirefoxVoice() {
  try {
    isListening.value = true
    isAsrProcessing.value = false
    asrManualStop = false
    listeningWindowStartAt = Date.now()
    startListeningCountdown()
    asrMediaStream = await navigator.mediaDevices.getUserMedia({ audio: true })
    asrMediaRecorder = new MediaRecorder(asrMediaStream, { mimeType: 'audio/webm' })
    asrChunks = []
    if (recognitionStopTimer) clearTimeout(recognitionStopTimer)
    recognitionStopTimer = setTimeout(() => {
      if (isListening.value) stopVoiceRecognition(false)
    }, VOICE_LISTEN_MAX_MS)

    asrMediaRecorder.ondataavailable = (e) => { if (e.data.size > 0) asrChunks.push(e.data) }
    asrMediaRecorder.onstop = async () => {
      try { asrMediaStream?.getTracks()?.forEach(t => t.stop()) } catch (_e) {}
      asrMediaStream = null
      isListening.value = false
      stopListeningCountdown()
      isAsrProcessing.value = true
      startAsrCountdown()
      const blob = new Blob(asrChunks, { type: 'audio/webm' })
      const fd = new FormData(); fd.append('audio', blob, 'recording.webm')
      try {
        const { uploadAsrAudio } = await import('@/api/ai')
        const res = await uploadAsrAudio(fd)
        if (!res.ok) {
          const failText = await res.text()
          throw new Error(`ASR请求失败(${res.status}) ${failText || ''}`.trim())
        }
        const result = await res.json()
        if (result.text) {
          inputText.value = result.text
          asrTextPendingAutoSpeak = true
          if (!asrManualStop && !suppressAutoSendOnFinalize) nextTick(() => sendMessage({ autoSpeak: true }))
        }
        else ElMessage.error(`语音识别失败${result.error ? '：' + result.error : ''}`)
      } catch (err) { ElMessage.error('语音识别失败：' + (err?.message || String(err))) }
      finally {
        isAsrProcessing.value = false
        stopAsrCountdown()
        asrMediaRecorder = null
        asrChunks = []
        asrManualStop = false
        suppressAutoSendOnFinalize = false
      }
    }
    asrMediaRecorder.start()
  } catch (err) {
    isListening.value = false
    isAsrProcessing.value = false
    stopListeningCountdown()
    stopAsrCountdown()
    ElMessage.error('无法访问麦克风：' + err.message)
  }
}

function toggleSpeech() {
  if (isSpeaking.value) { stopSpeechPlayback(); return }
  if (!currentReplyText.value) return
  speakText(currentReplyText.value)
}

function stopSpeechPlayback() {
  pendingAudioPlayToken += 1
  if (ttsAudio) {
    try { ttsAudio.pause() } catch (_e) {}
    try { ttsAudio.currentTime = 0 } catch (_e) {}
    ttsAudio = null
  }
  isSpeaking.value = false
  notifyLive2dHook('onSpeechEnd')
}

function speakText(text, options = {}) {
  const { forceRestart = false } = options
  if (!text) return
  if (forceRestart && isSpeaking.value) {
    stopSpeechPlayback()
  }
  const playToken = ++pendingAudioPlayToken
  notifyLive2dHook('onSpeechStart')
  isSpeaking.value = true
  synthesizeTts({ text }).then((res) => {
    const audioUrl = res?.audio_url || res?.data?.audio_url
    if (!audioUrl) throw new Error('TTS返回为空')
    const finalUrl = audioUrl.startsWith('http')
      ? audioUrl
      : (audioUrl.startsWith('/api/') ? audioUrl : withApiBase(audioUrl))
    const audio = new Audio()
    audio.preload = 'auto'
    audio.src = finalUrl
    ttsAudio = audio
    audio.onended = () => {
      if (ttsAudio === audio) ttsAudio = null
      isSpeaking.value = false
      notifyLive2dHook('onSpeechEnd')
    }
    audio.onerror = () => {
      if (playToken !== pendingAudioPlayToken) return
      if (ttsAudio === audio) ttsAudio = null
      isSpeaking.value = false
      notifyLive2dHook('onSpeechEnd')
      ElMessage.error('语音播放失败')
    }
    const tryPlay = () => {
      if (playToken !== pendingAudioPlayToken) return
      audio.onloadeddata = null
      audio.oncanplay = null
      audio.play().catch((playErr) => {
        if (playToken !== pendingAudioPlayToken) return
        if (playErr?.name === 'AbortError') return
        if (ttsAudio === audio) ttsAudio = null
        isSpeaking.value = false
        notifyLive2dHook('onSpeechEnd')
        ElMessage.error(`语音播放失败${playErr?.message ? '：' + playErr.message : ''}`)
      })
    }
    audio.onloadeddata = tryPlay
    audio.oncanplay = tryPlay
    audio.load()
  }).catch((err) => {
    if (playToken !== pendingAudioPlayToken) return
    isSpeaking.value = false
    notifyLive2dHook('onSpeechEnd')
    const detail = err?.response?.data?.detail || err?.response?.data?.error || err?.message
    ElMessage.error(`语音合成失败${detail ? '：' + detail : ''}`)
  })
}

function clearMessages() {
  if (isSpeaking.value) stopSpeechPlayback()
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

// 点击/拖拽区分状态
let modelClickState = { isDragging: false, startX: 0, startY: 0, moveThreshold: 5 }
// 全局标志：是否正在拖拽 Live2D 模型，用于阻止面板误打开
let isModelDragging = false

function onWaifuMouseDown(e) {
  // 如果点击的是面板内部元素，不触发拖拽
  if (e.target.closest('.chat-panel') || e.target.closest('.panel-resize-handle')) return

  modelClickState.isDragging = false
  modelClickState.startX = e.clientX
  modelClickState.startY = e.clientY
  isModelDragging = false

  const waifuEl = document.getElementById('waifu')
  if (!waifuEl) return
  const rect = waifuEl.getBoundingClientRect()
  modelDragState = {
    dragging: false,
    startX: e.clientX,
    startY: e.clientY,
    origLeft: rect.left,
    origTop: rect.top
  }

  document.addEventListener('mousemove', onWaifuMouseMove)
  document.addEventListener('mouseup', onWaifuMouseUp)
}

function onWaifuMouseMove(e) {
  const dx = e.clientX - modelClickState.startX
  const dy = e.clientY - modelClickState.startY
  const distance = Math.sqrt(dx * dx + dy * dy)

  // 移动超过阈值，判定为拖拽
  if (!modelDragState.dragging && distance > modelClickState.moveThreshold) {
    modelDragState.dragging = true
    modelClickState.isDragging = true
    isModelDragging = true
  }

  if (modelDragState.dragging) {
    e.preventDefault()
    const newLeft = modelDragState.origLeft + (e.clientX - modelDragState.startX)
    const newTop = modelDragState.origTop + (e.clientY - modelDragState.startY)
    applyModelPosition(newLeft, newTop)
  }
}

function onWaifuMouseUp(e) {
  document.removeEventListener('mousemove', onWaifuMouseMove)
  document.removeEventListener('mouseup', onWaifuMouseUp)

  if (!modelClickState.isDragging) {
    // 判定为点击，打开面板
    openPanel()
  }

  // 延迟重置拖拽标志，确保 click 事件能检测到拖拽状态
  setTimeout(() => {
    isModelDragging = false
  }, 100)
  modelDragState.dragging = false
  modelClickState.isDragging = false
}

function onWaifuTouchStart(e) {
  // 如果触摸的是面板内部元素，不触发拖拽
  if (e.target.closest('.chat-panel') || e.target.closest('.panel-resize-handle')) return

  const t = e.touches[0]
  modelClickState.isDragging = false
  modelClickState.startX = t.clientX
  modelClickState.startY = t.clientY
  isModelDragging = false

  const waifuEl = document.getElementById('waifu')
  if (!waifuEl) return
  const rect = waifuEl.getBoundingClientRect()
  modelDragState = {
    dragging: false,
    startX: t.clientX,
    startY: t.clientY,
    origLeft: rect.left,
    origTop: rect.top
  }

  document.addEventListener('touchmove', onWaifuTouchMove, { passive: false })
  document.addEventListener('touchend', onWaifuTouchEnd)
}

function onWaifuTouchMove(e) {
  const t = e.touches[0]
  const dx = t.clientX - modelClickState.startX
  const dy = t.clientY - modelClickState.startY
  const distance = Math.sqrt(dx * dx + dy * dy)

  // 移动超过阈值，判定为拖拽
  if (!modelDragState.dragging && distance > modelClickState.moveThreshold) {
    modelDragState.dragging = true
    modelClickState.isDragging = true
    isModelDragging = true
  }

  if (modelDragState.dragging) {
    e.preventDefault()
    const newLeft = modelDragState.origLeft + (t.clientX - modelDragState.startX)
    const newTop = modelDragState.origTop + (t.clientY - modelDragState.startY)
    applyModelPosition(newLeft, newTop)
  }
}

function onWaifuTouchEnd(e) {
  document.removeEventListener('touchmove', onWaifuTouchMove)
  document.removeEventListener('touchend', onWaifuTouchEnd)

  if (!modelClickState.isDragging) {
    // 判定为点击，打开面板
    openPanel()
  }

  // 延迟重置拖拽标志，确保 click 事件能检测到拖拽状态
  setTimeout(() => {
    isModelDragging = false
  }, 100)
  modelDragState.dragging = false
  modelClickState.isDragging = false
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

  try {
    localStorage.setItem('huahuoModelPos', JSON.stringify({ left: clampedLeft, top: clampedTop }))
  } catch (_e) {}
}

function startDrag(e) {
  if (resizeState.resizing) return
  dragState.dragging = true
  dragState.startX = e.clientX - (panelPos.value.x || 0)
  dragState.startY = e.clientY - (panelPos.value.y || 0)
  document.addEventListener('mousemove', onDrag)
  document.addEventListener('mouseup', stopDrag)
}
function startDragTouch(e) {
  if (resizeState.resizing) return
  const t = e.touches[0]
  dragState.dragging = true
  dragState.startX = t.clientX - (panelPos.value.x || 0)
  dragState.startY = t.clientY - (panelPos.value.y || 0)
  document.addEventListener('touchmove', onDragTouch, { passive: false })
  document.addEventListener('touchend', stopDragTouch)
}
function updatePanelStyle() {
  panelStyle.value = {
    transform: `translate(${panelPos.value.x}px, ${panelPos.value.y}px)`,
    width: panelSize.value.width + 'px',
    height: panelSize.value.height + 'px'
  }
}

function onDrag(e) {
  if (!dragState.dragging || resizeState.resizing) return
  const newX = e.clientX - dragState.startX
  const newY = e.clientY - dragState.startY
  // 允许窗口部分超出屏幕，只限制不能完全移出屏幕（保留100px可见区域）
  const minVisible = 100
  const maxX = window.innerWidth - minVisible
  const maxY = window.innerHeight - minVisible
  const minX = minVisible - panelSize.value.width
  const minY = minVisible - panelSize.value.height
  panelPos.value = {
    x: Math.max(minX, Math.min(newX, maxX)),
    y: Math.max(minY, Math.min(newY, maxY))
  }
  updatePanelStyle()
}
function onDragTouch(e) {
  if (!dragState.dragging || resizeState.resizing) return
  e.preventDefault()
  const t = e.touches[0]
  const newX = t.clientX - dragState.startX
  const newY = t.clientY - dragState.startY
  // 允许窗口部分超出屏幕，只限制不能完全移出屏幕（保留100px可见区域）
  const minVisible = 100
  const maxX = window.innerWidth - minVisible
  const maxY = window.innerHeight - minVisible
  const minX = minVisible - panelSize.value.width
  const minY = minVisible - panelSize.value.height
  panelPos.value = {
    x: Math.max(minX, Math.min(newX, maxX)),
    y: Math.max(minY, Math.min(newY, maxY))
  }
  updatePanelStyle()
}
function stopDrag() {
  dragState.dragging = false
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
  try { localStorage.setItem('huahuoPanelPos', JSON.stringify(panelPos.value)) } catch (_e) {}
}
function stopDragTouch() {
  dragState.dragging = false
  document.removeEventListener('touchmove', onDragTouch)
  document.removeEventListener('touchend', stopDragTouch)
  try { localStorage.setItem('huahuoPanelPos', JSON.stringify(panelPos.value)) } catch (_e) {}
}

function startResize(e) {
  e.preventDefault()
  e.stopPropagation()
  resizeState = { resizing: true, startX: e.clientX, startY: e.clientY, startW: panelSize.value.width, startH: panelSize.value.height }
  document.addEventListener('mousemove', onResize)
  document.addEventListener('mouseup', stopResize)
}
function onResize(e) {
  if (!resizeState.resizing) return
  const dx = e.clientX - resizeState.startX
  const dy = e.clientY - resizeState.startY
  const newW = Math.max(320, Math.min(800, resizeState.startW + dx))
  const newH = Math.max(400, Math.min(900, resizeState.startH + dy))
  panelSize.value = { width: newW, height: newH }
  updatePanelStyle()
}
function stopResize() {
  resizeState.resizing = false
  document.removeEventListener('mousemove', onResize)
  document.removeEventListener('mouseup', stopResize)
  try { localStorage.setItem('huahuoPanelSize', JSON.stringify(panelSize.value)) } catch (_e) {}
}

onMounted(() => {
  setupExpressionControls()
  setupVoiceHooks()
  window.addEventListener('open-huahuo-agent', handleOpenHuahuoAgent)

  // 检测移动端
  const checkMobile = () => {
    const wasMobile = isMobile.value
    isMobile.value = window.innerWidth <= 768
    if (isMobile.value) {
      panelSize.value = { width: Math.min(360, window.innerWidth - 20), height: Math.min(520, window.innerHeight - 100) }
      panelPos.value = { x: 10, y: window.innerHeight - panelSize.value.height - 80 }
    } else if (wasMobile !== isMobile.value) {
      // 从移动端切回桌面端时恢复保存的尺寸
      try { const savedSize = localStorage.getItem('huahuoPanelSize'); if (savedSize) { panelSize.value = JSON.parse(savedSize) } } catch (_e) {}
      try { const saved = localStorage.getItem('huahuoPanelPos'); if (saved) { panelPos.value = JSON.parse(saved) } } catch (_e) {}
    }
    updatePanelStyle()
  }
  checkMobile()
  window.addEventListener('resize', checkMobile)

  const currentPath = window.location.pathname
  if (currentPath === '/login' || currentPath === '/register') {
    return
  }

  initLive2D().catch(() => {
    loadError.value = true
  })
})

onBeforeUnmount(() => {
  window.removeEventListener('open-huahuo-agent', handleOpenHuahuoAgent)
  window.removeEventListener('resize', checkMobile)
  stopVoiceRecognition()
  stopListeningCountdown(false)
  stopAsrCountdown(false)
  stopModelPatchLoop()
  stopAutoExpression()
  stopSpeechPlayback()

  try {
    const manager = window.__live2dWidgetModelManager
    if (manager?.cubism5model) {
      if (typeof manager.cubism5model.release === 'function') {
        manager.cubism5model.release()
      }
    }
  } catch (_e) {}

  const waifuEl = document.getElementById('waifu')
  if (waifuEl) waifuEl.remove()
  const waifuToggle = document.getElementById('waifu-toggle')
  if (waifuToggle) waifuToggle.remove()
  const waifuTool = document.getElementById('waifu-tool')
  if (waifuTool) waifuTool.remove()

  try {
    delete window.__live2dWidgetModelManager
    delete window.__expressionControlsState
    delete window.__expressionOverlayRules
    delete window.__applyOverlayStateToCore
    delete window.__applyOverlayState
    delete window.__syncExpressionState
    delete window.__applySpeechStateToCore
    delete window.__voiceLive2dHooks
    delete window.__speechMouthOpenY
    delete window.__huahuoModelPatchLoopStarted
    delete window.initWidget
    delete window.loadlive2d
  } catch (_e) {}

  try {
    window.localStorage.removeItem('waifu-display')
    window.localStorage.removeItem('modelId')
    window.localStorage.removeItem('modelTexturesId')
  } catch (_e) {}
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
  bottom: 0;
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
  border-bottom: 1px solid rgba(59, 130, 246, 0.12);
  background: #f8fafc;
  max-height: 280px;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(59, 130, 246, 0.25) transparent;
}

.expression-panel::-webkit-scrollbar { width: 4px; }
.expression-panel::-webkit-scrollbar-thumb { background: rgba(59, 130, 246, 0.25); border-radius: 2px; }

.expression-section {
  margin-bottom: 10px;
}

.expression-section:last-child {
  margin-bottom: 0;
}

.expression-section-title {
  font-size: 12px;
  color: #64748b;
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
  color: #475569;
  background: #ffffff;
  border: 1px solid rgba(59, 130, 246, 0.1);
  cursor: pointer;
  text-align: center;
  transition: all 0.2s ease;
  user-select: none;
}

.expression-item:hover {
  background: rgba(59, 130, 246, 0.08);
  border-color: rgba(59, 130, 246, 0.25);
  color: #1e293b;
}

.expression-item.active {
  background: rgba(59, 130, 246, 0.12);
  border-color: rgba(59, 130, 246, 0.35);
  color: #3b82f6;
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
  color: #475569;
  cursor: pointer;
  user-select: none;
}

.overlay-item input[type="checkbox"] {
  accent-color: #3b82f6;
  width: 14px;
  height: 14px;
  cursor: pointer;
}

.overlay-item:hover {
  color: #1e293b;
}

.chat-panel {
  position: fixed;
  bottom: 20px;
  left: 20px;
  width: 400px;
  max-height: 580px;
  background: #ffffff;
  backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid rgba(59, 130, 246, 0.15);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12), 0 0 0 1px rgba(59, 130, 246, 0.05);
  display: flex;
  flex-direction: column;
  z-index: 10000;
  overflow: hidden;
}

.panel-resize-handle {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 20px;
  height: 20px;
  cursor: nwse-resize;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
}

.resize-icon {
  width: 14px;
  height: 14px;
  pointer-events: none;
  opacity: 0.5;
  transition: opacity 0.2s;
}

.panel-resize-handle:hover .resize-icon {
  opacity: 1;
}

.panel-resize-handle:hover .resize-icon path {
  stroke: rgba(59, 130, 246, 1);
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 16px;
  background: rgba(59, 130, 246, 0.08);
  border-bottom: 1px solid rgba(59, 130, 246, 0.15);
  user-select: none;
}

.header-drag-area {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: move;
  flex: 1;
  min-width: 0;
}

.panel-title {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}

.listening-tag {
  animation: pulse 1.5s infinite;
}

.asr-tag {
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

.analysis-mode ::deep(.el-form-item) {
  margin-bottom: 12px;
}

.analysis-mode ::deep(.el-form-item__label) {
  color: #475569;
  font-size: 12px;
}

.analysis-mode ::deep(.el-input__inner),
.analysis-mode ::deep(.el-textarea__inner) {
  color: #1e293b !important;
  background-color: #ffffff !important;
  border-color: rgba(59, 130, 246, 0.3) !important;
}

.analysis-mode ::deep(.el-input__wrapper) {
  background-color: #ffffff !important;
  box-shadow: 0 0 0 1px rgba(59, 130, 246, 0.3) inset !important;
}

.analysis-mode ::deep(.el-textarea__wrapper) {
  background-color: #ffffff !important;
  box-shadow: 0 0 0 1px rgba(59, 130, 246, 0.3) inset !important;
}

.analysis-mode ::deep(.el-input__inner::placeholder),
.analysis-mode ::deep(.el-textarea__inner::placeholder) {
  color: #94a3b8 !important;
}

.analysis-mode ::deep(.el-radio-button__inner) {
  color: #475569 !important;
  background-color: #f1f5f9 !important;
  border-color: rgba(59, 130, 246, 0.2) !important;
}

.analysis-mode ::deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
  color: #fff !important;
  background-color: #3b82f6 !important;
  border-color: #3b82f6 !important;
}

.analysis-result {
  margin-top: 12px;
  background: #f8fafc;
  border-radius: 10px;
  padding: 12px 14px;
  border: 1px solid rgba(59, 130, 246, 0.12);
}

.analysis-result ::deep(.el-divider__text) {
  color: #3b82f6;
  font-size: 13px;
  font-weight: 600;
}

.analysis-result .markdown-body {
  color: #1e293b;
  font-size: 14px;
  line-height: 1.7;
}

.analysis-result .markdown-body h1,
.analysis-result .markdown-body h2,
.analysis-result .markdown-body h3,
.analysis-result .markdown-body h4,
.analysis-result .markdown-body h5,
.analysis-result .markdown-body h6 {
  color: #1e293b;
  font-size: 14px;
  font-weight: 600;
  margin: 6px 0 2px;
}

.analysis-result .markdown-body p {
  color: #1e293b;
  margin: 4px 0;
}

.analysis-result .markdown-body strong {
  color: #2563eb;
}

.analysis-result .markdown-body ul,
.analysis-result .markdown-body ol {
  color: #1e293b;
}

.analysis-result .markdown-body li {
  color: #1e293b;
}

.analysis-result .markdown-body table {
  color: #1e293b;
}

.analysis-result .markdown-body th {
  color: #3b82f6;
  background: rgba(59, 130, 246, 0.08);
}

.analysis-result .markdown-body td {
  color: #1e293b;
}

.analysis-result .markdown-body code {
  color: #2563eb;
  background: rgba(59, 130, 246, 0.08);
}

.analysis-result .markdown-body blockquote {
  color: #475569;
  border-left-color: rgba(59, 130, 246, 0.3);
}

.analysis-result .markdown-body hr {
  border-top-color: rgba(59, 130, 246, 0.1);
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
  scrollbar-width: thin;
  scrollbar-color: rgba(59, 130, 246, 0.25) transparent;
}

.chat-messages::-webkit-scrollbar { width: 4px; }
.chat-messages::-webkit-scrollbar-thumb { background: rgba(59, 130, 246, 0.25); border-radius: 2px; }

.chat-empty {
  text-align: center;
  color: #64748b;
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
  background: rgba(59, 130, 246, 0.12);
  color: #1e293b;
  border-bottom-right-radius: 4px;
}

.message-item.assistant .message-content {
  background: #f1f5f9;
  color: #1e293b;
  border-bottom-left-radius: 4px;
}

.message-item.assistant .message-content .markdown-body {
  font-size: 14px;
  line-height: 1.6;
  color: #1e293b;
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
  color: #1e293b;
}

.message-content.streaming { min-height: 20px; }

.cursor-blink {
  animation: blink 1s step-end infinite;
  color: #3b82f6;
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
  border-top: 1px solid rgba(59, 130, 246, 0.12);
  background: #f8fafc;
}

.chat-input-row {
  display: flex;
  gap: 8px;
  align-items: flex-end;
}

.chat-send-btn {
  flex-shrink: 0;
  height: 36px;
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

.markdown-body ::deep(h1), .markdown-body ::deep(h2), .markdown-body ::deep(h3),
.markdown-body ::deep(h4), .markdown-body ::deep(h5), .markdown-body ::deep(h6) {
  margin: 8px 0 4px;
  font-weight: 600;
  font-size: 14px;
  color: #1e293b;
}
.markdown-body ::deep(h1)::before { content: ''; }
.markdown-body ::deep(p) { margin: 4px 0; color: #1e293b; }
.markdown-body ::deep(ul), .markdown-body ::deep(ol) { padding-left: 16px; margin: 4px 0; color: #1e293b; }
.markdown-body ::deep(li) { margin: 2px 0; color: #1e293b; }
.markdown-body ::deep(strong) { color: #2563eb; font-weight: 600; }
.markdown-body ::deep(em) { font-style: italic; color: #475569; }
.markdown-body ::deep(blockquote) { border-left: 3px solid rgba(59, 130, 246, 0.3); padding-left: 10px; margin: 6px 0; color: #475569; }
.markdown-body ::deep(hr) { border: none; border-top: 1px solid rgba(59, 130, 246, 0.1); margin: 8px 0; }
.markdown-body ::deep(table) { width: 100%; border-collapse: collapse; margin: 6px 0; font-size: 13px; }
.markdown-body ::deep(th), .markdown-body ::deep(td) { border: 1px solid rgba(59, 130, 246, 0.15); padding: 4px 8px; text-align: left; }
.markdown-body ::deep(th) { background: rgba(59, 130, 246, 0.08); color: #3b82f6; font-weight: 600; }
.markdown-body ::deep(code) { background: rgba(59, 130, 246, 0.08); padding: 1px 5px; border-radius: 3px; font-size: 13px; color: #2563eb; }
.markdown-body ::deep(pre) { background: #f1f5f9; padding: 10px; border-radius: 6px; overflow-x: auto; margin: 6px 0; }
.markdown-body ::deep(pre code) { background: none; padding: 0; font-size: 13px; }

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
  color: #475569 !important;
  font-size: 12px !important;
}

.chat-panel .el-input__inner,
.chat-panel .el-textarea__inner {
  color: #1e293b !important;
  background-color: #ffffff !important;
  border-color: rgba(59, 130, 246, 0.3) !important;
}

.chat-panel .el-input__wrapper {
  background-color: #ffffff !important;
  box-shadow: 0 0 0 1px rgba(59, 130, 246, 0.3) inset !important;
}

.chat-panel .el-textarea__wrapper {
  background-color: #ffffff !important;
  box-shadow: 0 0 0 1px rgba(59, 130, 246, 0.3) inset !important;
}

.chat-panel .el-input__inner::placeholder,
.chat-panel .el-textarea__inner::placeholder {
  color: #94a3b8 !important;
}

.chat-panel .el-radio-button__inner {
  color: #475569 !important;
  background-color: #f1f5f9 !important;
  border-color: rgba(59, 130, 246, 0.2) !important;
}

.chat-panel .el-radio-button__original-radio:checked + .el-radio-button__inner {
  color: #fff !important;
  background-color: #3b82f6 !important;
  border-color: #3b82f6 !important;
}

.chat-panel .el-select .el-input__inner {
  color: #1e293b !important;
  background-color: #ffffff !important;
  border-color: rgba(59, 130, 246, 0.3) !important;
}

.chat-panel .el-select-dropdown {
  background-color: #ffffff !important;
  border: 1px solid rgba(59, 130, 246, 0.2) !important;
}

.chat-panel .el-select-dropdown__item {
  color: #1e293b !important;
}

.chat-panel .el-select-dropdown__item.hover,
.chat-panel .el-select-dropdown__item:hover {
  background-color: rgba(59, 130, 246, 0.08) !important;
}

.chat-panel .el-select-dropdown__item.selected {
  color: #3b82f6 !important;
  font-weight: 600;
}

.chat-panel .el-divider__text {
  color: #3b82f6 !important;
  font-size: 13px !important;
  font-weight: 600;
}

.chat-panel .el-input-group__append {
  background-color: rgba(59, 130, 246, 0.1) !important;
  border-color: rgba(59, 130, 246, 0.2) !important;
  color: #3b82f6 !important;
  box-shadow: none !important;
}
</style>
