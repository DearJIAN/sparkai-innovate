<template>
  <div class="ai-assistant-page">
    <el-alert
      type="info"
      :closable="false"
      show-icon
      style="margin-bottom: 16px"
    >
      备用 AI 页面：推荐使用右下角火花助手。此页面用于调试和完整结果查看。
    </el-alert>

    <div class="page-header">
      <div class="header-content">
        <h2 class="page-title">
          <el-icon><MagicStick /></el-icon>
          AI 项目助手
        </h2>
        <p class="page-subtitle">基于 AI 技术，为竞赛项目提供智能化辅助分析</p>
      </div>
      <div class="header-actions"></div>
    </div>

    <el-tabs v-model="activeTab" class="ai-tabs">
      <el-tab-pane label="AI 分析工具" name="tools">
        <el-row :gutter="24">
          <el-col :span="10">
            <el-card shadow="never" class="input-card">
              <template #header>
                <div class="card-header">
                  <span>项目信息</span>
                  <el-tag size="small" type="success">AI 驱动</el-tag>
                </div>
              </template>
              <el-form :model="form" label-position="top">
                <el-form-item label="项目名称">
                  <el-input v-model="form.project_name" placeholder="请输入项目名称" />
                </el-form-item>
                <el-form-item label="项目简介">
                  <el-input v-model="form.description" type="textarea" :rows="4" placeholder="简要描述你的项目想法、目标用户、核心功能" />
                </el-form-item>
                <el-form-item label="项目类别">
                  <el-input v-model="form.category" placeholder="例如：互联网+、人工智能、社会公益" />
                </el-form-item>
                <el-form-item label="所属赛道">
                  <el-input v-model="form.track" placeholder="例如：高教主赛道、青年红色筑梦之旅" />
                </el-form-item>
                <el-form-item label="选择 AI 功能">
                  <el-radio-group v-model="form.ai_type">
                    <el-radio-button label="summary">生成项目简介</el-radio-button>
                    <el-radio-button label="business_advice">商业计划书建议</el-radio-button>
                    <el-radio-button label="risk_analysis">风险分析</el-radio-button>
                  </el-radio-group>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" :loading="loading" :icon="MagicStick" @click="handleGenerate" style="width: 100%">
                    {{ loading ? 'AI 生成中...' : '开始生成' }}
                  </el-button>
                </el-form-item>
              </el-form>
            </el-card>

            <el-card class="mt-4" shadow="never">
              <template #header><span>历史记录</span></template>
              <el-empty v-if="records.length === 0" description="暂无记录" :image-size="60" />
              <div v-else class="record-list">
                <div v-for="record in records.slice(0, 5)" :key="record.id" class="record-item" @click="showRecord(record)">
                  <el-icon size="16" color="var(--primary-500)"><MagicStick /></el-icon>
                  <span class="record-type">{{ typeText(record.type) }}</span>
                  <span class="record-time">{{ formatDate(record.created_at) }}</span>
                </div>
              </div>
            </el-card>
          </el-col>

          <el-col :span="14">
            <el-card shadow="never" class="output-card">
              <template #header>
                <div class="output-header">
                  <span>AI 输出结果</span>
                  <div v-if="result" class="output-actions">
                    <el-button type="primary" link size="small" :icon="CopyDocument" @click="copyResult">复制</el-button>
                    <el-button type="primary" link size="small" :icon="VideoPlay" @click="speakResult">朗读</el-button>
                  </div>
                </div>
              </template>
              <div v-if="!result" class="output-placeholder">
                <el-icon size="48" color="var(--text-tertiary)"><MagicStick /></el-icon>
                <p>在左侧输入项目信息，选择 AI 功能，点击开始生成</p>
              </div>
              <div v-else class="output-content">
                <div class="result-type-tag">
                  <el-tag :type="resultTypeTag.type" size="small">{{ resultTypeTag.text }}</el-tag>
                </div>
                <div class="markdown-result" v-html="renderMarkdown(result)"></div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-tab-pane>

      <el-tab-pane label="AI 对话" name="chat">
        <div class="chat-container">
          <div ref="chatMessagesRef" class="chat-messages-full">
            <div v-if="chatMessages.length === 0" class="chat-empty">
              <div class="chat-empty-icon">🤖</div>
              <h3>你好，我是火花 AI 助手</h3>
              <p>我可以帮你分析项目、提供竞赛建议、解答创业问题</p>
              <div class="chat-quick-actions">
                <el-button v-for="q in chatQuickQuestions" :key="q.text" @click="sendChatMessage(q.text)" round>
                  {{ q.icon }} {{ q.text }}
                </el-button>
              </div>
            </div>
            <div v-for="(msg, idx) in chatMessages" :key="idx" class="chat-msg" :class="msg.role">
              <div class="chat-msg-avatar">{{ msg.role === 'user' ? '👤' : '🤖' }}</div>
              <div class="chat-msg-body">
                <div v-if="msg.role === 'assistant'" class="markdown-body" v-html="renderMarkdown(msg.content)"></div>
                <div v-else>{{ msg.content }}</div>
              </div>
            </div>
            <div v-if="isChatStreaming" class="chat-msg assistant">
              <div class="chat-msg-avatar">🤖</div>
              <div class="chat-msg-body streaming">
                <div class="markdown-body" v-html="renderMarkdown(chatStreamingText)"></div>
                <span class="cursor-blink">▌</span>
              </div>
            </div>
          </div>

          <div class="chat-input-full">
            <div class="chat-input-row">
              <el-button
                :type="isListening ? 'danger' : 'default'"
                :icon="Microphone"
                circle
                @click="toggleVoice"
                :loading="isAsrProcessing"
                :title="isListening ? `录音中 ${voiceRemainingSeconds}s` : '语音输入'"
              />
              <span v-if="isListening" class="listening-countdown">剩余 {{ voiceRemainingSeconds }}s</span>
              <el-input
                v-model="chatInput"
                placeholder="输入你的问题..."
                @keyup.enter="sendChatMessage"
                :disabled="isChatStreaming"
                size="large"
                clearable
              />
              <el-button type="primary" :icon="Promotion" @click="sendChatMessage" :loading="isChatStreaming" :disabled="!chatInput.trim()" size="large">
                发送
              </el-button>
            </div>
          </div>
        </div>
      </el-tab-pane>

      <el-tab-pane label="AI 智能体" name="agent">
        <AgentPanel
          :user-role="userRole"
          :initial-context="{}"
        />
      </el-tab-pane>
    </el-tabs>

  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, nextTick, watch } from 'vue'
import { MagicStick, CopyDocument, VideoPlay, Microphone, Promotion } from '@element-plus/icons-vue'
import {
  generateProjectSummary, generateBusinessAdvice, generateRiskAnalysis, getAiRecords,
  chatStream, uploadAsrAudio,
} from '@/api/ai'
import { marked } from 'marked'
import { ElMessage } from 'element-plus'
import { useLive2d } from '@/composables/useLive2d'
import AgentPanel from '@/views/ai-assistant/AgentPanel.vue'
import { useUserStore } from '@/stores/user'

const { notifyLive2dHook, updateExpressionByText } = useLive2d()
const userStore = useUserStore()
const userRole = computed(() => userStore.currentRole || 'student')

marked.setOptions({ breaks: true, gfm: true })

function renderMarkdown(text) {
  if (!text) return ''
  try { return marked.parse(text) } catch { return text }
}

const activeTab = ref('tools')
const loading = ref(false)
const result = ref('')
const currentType = ref('')
const records = ref([])

const form = reactive({
  project_name: '',
  description: '',
  category: '',
  track: '',
  ai_type: 'summary',
})

const typeMap = {
  summary: { text: '项目简介', type: 'primary' },
  business_advice: { text: '商业计划书建议', type: 'success' },
  risk_analysis: { text: '风险分析', type: 'warning' },
}

const resultTypeTag = computed(() => typeMap[currentType.value] || typeMap.summary)

const handleGenerate = async () => {
  if (!form.project_name.trim()) {
    ElMessage.warning('请输入项目名称')
    return
  }
  loading.value = true
  currentType.value = form.ai_type
  try {
    const data = {
      project_name: form.project_name,
      description: form.description,
      category: form.category,
      track: form.track,
    }
    let res
    switch (form.ai_type) {
      case 'summary': res = await generateProjectSummary(data); break
      case 'business_advice': res = await generateBusinessAdvice(data); break
      case 'risk_analysis': res = await generateRiskAnalysis(data); break
      default: res = await generateProjectSummary(data)
    }
    if (res.code === 200) {
      result.value = res.data.result
      ElMessage.success('生成成功')
      fetchRecords()
    } else {
      ElMessage.error(res.message || '生成失败')
    }
  } catch (err) {
    ElMessage.error('生成失败')
  } finally {
    loading.value = false
  }
}

const copyResult = () => {
  navigator.clipboard.writeText(result.value).then(() => {
    ElMessage.success('已复制到剪贴板')
  })
}

const speakResult = () => {
  if (!result.value) return
  window.speechSynthesis.cancel()
  const utterance = new SpeechSynthesisUtterance(result.value)
  utterance.lang = 'zh-CN'
  const voices = window.speechSynthesis.getVoices()
  const zhVoice = voices.find(v => v.lang.startsWith('zh'))
  if (zhVoice) utterance.voice = zhVoice
  window.speechSynthesis.speak(utterance)
}

const showRecord = (record) => {
  result.value = record.result
  currentType.value = record.type
}

const typeText = (type) => (typeMap[type] || {}).text || type

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return `${d.getMonth() + 1}/${d.getDate()} ${d.getHours()}:${String(d.getMinutes()).padStart(2, '0')}`
}

const fetchRecords = async () => {
  try {
    const res = await getAiRecords()
    if (res.code === 200) {
      records.value = res.data.records
    }
  } catch (_e) {}
}

onMounted(() => { fetchRecords() })

const chatMessages = ref([])
const chatInput = ref('')
const isChatStreaming = ref(false)
const chatStreamingText = ref('')
const chatSessionId = ref('')
const chatMessagesRef = ref(null)
const isListening = ref(false)
const isAsrProcessing = ref(false)
let chatRecognition = null
let recognitionStartAt = 0
let recognitionFinalText = ''
let recognitionManualStop = false
let recognitionStopTimer = null
let recognitionForceFinalizeTimer = null
let recognitionActive = false
let suppressAutoSendOnFinalize = false
let listeningCountdownTimer = null
let listeningWindowStartAt = 0
const VOICE_LISTEN_MAX_MS = 60000
const voiceRemainingSeconds = ref(Math.ceil(VOICE_LISTEN_MAX_MS / 1000))

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

function finalizeRecognitionAndSend() {
  if (recognitionStopTimer) { clearTimeout(recognitionStopTimer); recognitionStopTimer = null }
  if (recognitionForceFinalizeTimer) { clearTimeout(recognitionForceFinalizeTimer); recognitionForceFinalizeTimer = null }
  stopListeningCountdown()
  recognitionActive = false
  isListening.value = false
  const finalText = (recognitionFinalText || chatInput.value || '').trim()
  recognitionFinalText = ''
  chatRecognition = null
  if (finalText && !suppressAutoSendOnFinalize) {
    chatInput.value = finalText
    nextTick(() => sendChatMessage())
  }
  suppressAutoSendOnFinalize = false
}

const chatQuickQuestions = [
  { icon: '💡', text: '帮我分析项目创新性' },
  { icon: '📋', text: '如何写好商业计划书' },
  { icon: '🎯', text: '竞赛评审关注什么' },
  { icon: '👥', text: '如何组建优秀团队' },
]

async function sendChatMessage(text) {
  if (isListening.value) {
    suppressAutoSendOnFinalize = true
    stopVoice(true)
  }
  const message = text || chatInput.value.trim()
  if (!message || isChatStreaming.value) return

  chatMessages.value.push({ role: 'user', content: message })
  chatInput.value = ''
  isChatStreaming.value = true
  chatStreamingText.value = ''

  notifyLive2dHook('onStreamStart')

  try {
    const response = await chatStream(message, chatSessionId.value)
    if (!response.ok) throw new Error(`HTTP ${response.status}`)

    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''
    let fullText = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n')
      buffer = lines.pop() || ''

      for (const line of lines) {
        if (line.startsWith('sessionId:')) {
          chatSessionId.value = line.slice(10).trim()
        } else if (line.startsWith('delta:')) {
          const delta = line.slice(6).replace(/\\n/g, '\n')
          chatStreamingText.value += delta
          fullText += delta
          notifyLive2dHook('onDelta', { text: delta })
        } else if (line.startsWith('error:')) {
          ElMessage.error(line.slice(6))
        }
      }
    }

    if (chatStreamingText.value) {
      chatMessages.value.push({ role: 'assistant', content: chatStreamingText.value })
      updateExpressionByText(chatStreamingText.value)
    }
  } catch (err) {
    ElMessage.error('发送失败：' + err.message)
  } finally {
    isChatStreaming.value = false
    chatStreamingText.value = ''
    notifyLive2dHook('onStreamEnd')
    scrollToChatBottom()
  }
}

function scrollToChatBottom() {
  nextTick(() => {
    if (chatMessagesRef.value) {
      chatMessagesRef.value.scrollTop = chatMessagesRef.value.scrollHeight
    }
  })
}

watch(chatMessages, () => scrollToChatBottom(), { deep: true })
watch(chatStreamingText, () => scrollToChatBottom())

function toggleVoice() {
  if (isListening.value) {
    stopVoice()
  } else {
    startVoice()
  }
}

function startVoice() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
  if (SpeechRecognition) {
    chatRecognition = new SpeechRecognition()
    chatRecognition.lang = 'zh-CN'
    chatRecognition.continuous = true
    chatRecognition.interimResults = true
    recognitionFinalText = ''
    recognitionManualStop = false
    recognitionActive = true
    recognitionStartAt = Date.now()
    listeningWindowStartAt = recognitionStartAt
    startListeningCountdown()
    if (recognitionStopTimer) clearTimeout(recognitionStopTimer)
    recognitionStopTimer = setTimeout(() => {
      if (isListening.value) stopVoice(false)
    }, VOICE_LISTEN_MAX_MS)

    chatRecognition.onresult = (event) => {
      let finalTranscript = ''
      let interimTranscript = ''
      for (let i = event.resultIndex; i < event.results.length; i++) {
        if (event.results[i].isFinal) {
          finalTranscript += event.results[i][0].transcript
        } else {
          interimTranscript += event.results[i][0].transcript
        }
      }
      if (interimTranscript) chatInput.value = interimTranscript
      if (finalTranscript) {
        recognitionFinalText += finalTranscript
        chatInput.value = recognitionFinalText
      }
    }

    chatRecognition.onerror = (event) => {
      if (event.error === 'no-speech') return
      recognitionActive = false
      ElMessage.error('语音识别出错：' + event.error)
      finalizeRecognitionAndSend()
    }

    chatRecognition.onend = () => {
      const shouldContinue = recognitionActive && !recognitionManualStop && (Date.now() - recognitionStartAt < VOICE_LISTEN_MAX_MS)
      if (shouldContinue) {
        try { chatRecognition.start() } catch (_e) { isListening.value = false }
        return
      }
      finalizeRecognitionAndSend()
    }
    chatRecognition.start()
    isListening.value = true
  } else {
    startFirefoxVoice()
  }
}

function stopVoice(manual = true) {
  recognitionManualStop = manual
  recognitionActive = false
  if (manual) suppressAutoSendOnFinalize = true
  if (recognitionStopTimer) { clearTimeout(recognitionStopTimer); recognitionStopTimer = null }
  if (chatRecognition) {
    try { chatRecognition.stop() } catch (_e) {}
    if (recognitionForceFinalizeTimer) clearTimeout(recognitionForceFinalizeTimer)
    recognitionForceFinalizeTimer = setTimeout(() => {
      if (isListening.value) finalizeRecognitionAndSend()
    }, 1200)
  }
  if (!chatRecognition) isListening.value = false
  if (!chatRecognition) stopListeningCountdown()
}

async function startFirefoxVoice() {
  try {
    isListening.value = true
    isAsrProcessing.value = true
    listeningWindowStartAt = Date.now()
    startListeningCountdown()
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    const mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' })
    const chunks = []

    mediaRecorder.ondataavailable = (e) => { if (e.data.size > 0) chunks.push(e.data) }
    mediaRecorder.onstop = async () => {
      stream.getTracks().forEach(t => t.stop())
      isListening.value = false
      const blob = new Blob(chunks, { type: 'audio/webm' })
      const formData = new FormData()
      formData.append('audio', blob, 'recording.webm')
      try {
        const response = await uploadAsrAudio(formData)
        const result = await response.json()
        if (result.text) {
          chatInput.value = result.text
          nextTick(() => sendChatMessage())
        } else {
          ElMessage.error('语音识别失败')
        }
      } catch (err) {
        ElMessage.error('语音识别失败')
      } finally {
        isAsrProcessing.value = false
      }
    }
    mediaRecorder.start()
    setTimeout(() => { if (mediaRecorder.state === 'recording') mediaRecorder.stop() }, VOICE_LISTEN_MAX_MS)
  } catch (err) {
    isListening.value = false
    isAsrProcessing.value = false
    stopListeningCountdown()
    ElMessage.error('无法访问麦克风')
  }
}

</script>

<style scoped>
.ai-assistant-page {
  padding: 0;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.page-subtitle {
  color: var(--text-secondary);
  font-size: 14px;
  margin-top: 4px;
}

.input-card :deep(.el-card__header) {
  padding: 12px 20px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.output-card {
  min-height: 500px;
}

.output-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.output-actions {
  display: flex;
  gap: 8px;
}

.listening-countdown {
  font-size: 12px;
  color: #dc2626;
  font-weight: 600;
  min-width: 64px;
}

.output-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  color: var(--text-tertiary);
}

.output-placeholder p {
  margin-top: 16px;
  font-size: 14px;
}

.output-content {
  padding: 8px 0;
}

.result-type-tag {
  margin-bottom: 12px;
}

.markdown-result {
  font-size: 14px;
  line-height: 1.8;
  color: var(--text-primary);
}

.markdown-result :deep(h1),
.markdown-result :deep(h2),
.markdown-result :deep(h3) {
  margin: 16px 0 8px;
  color: var(--primary-600);
  font-weight: 600;
}

.markdown-result :deep(h1) { font-size: 20px; }
.markdown-result :deep(h2) { font-size: 18px; }
.markdown-result :deep(h3) { font-size: 16px; }

.markdown-result :deep(ul),
.markdown-result :deep(ol) {
  padding-left: 20px;
  margin: 8px 0;
}

.markdown-result :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 12px 0;
}

.markdown-result :deep(th),
.markdown-result :deep(td) {
  border: 1px solid var(--gray-200);
  padding: 8px 12px;
  text-align: left;
}

.markdown-result :deep(th) {
  background: var(--primary-50);
  color: var(--primary-700);
  font-weight: 600;
}

.markdown-result :deep(strong) {
  color: var(--primary-600);
}

.markdown-result :deep(code) {
  background: var(--gray-100);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 13px;
}

.markdown-result :deep(pre) {
  background: var(--gray-50);
  padding: 12px;
  border-radius: 8px;
  overflow-x: auto;
}

.markdown-result :deep(blockquote) {
  border-left: 4px solid var(--primary-300);
  padding-left: 16px;
  color: var(--text-secondary);
  margin: 12px 0;
}

.record-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.record-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.record-item:hover {
  background: var(--gray-50);
}

.record-type {
  flex: 1;
  font-size: 13px;
  color: var(--text-primary);
}

.record-time {
  font-size: 12px;
  color: var(--text-tertiary);
}

.ai-tabs :deep(.el-tabs__header) {
  margin-bottom: 20px;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 240px);
  min-height: 500px;
  background: var(--bg-secondary);
  border-radius: 12px;
  border: 1px solid var(--gray-200);
  overflow: hidden;
}

.chat-messages-full {
  flex: 1;
  overflow-y: auto;
  padding: 20px 24px;
}

.chat-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--text-secondary);
}

.chat-empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.chat-empty h3 {
  font-size: 20px;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.chat-empty p {
  font-size: 14px;
  margin-bottom: 24px;
}

.chat-quick-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

.chat-msg {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
  align-items: flex-start;
}

.chat-msg.user {
  flex-direction: row-reverse;
}

.chat-msg-avatar {
  font-size: 24px;
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-primary);
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.chat-msg-body {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 16px;
  font-size: 14px;
  line-height: 1.7;
  word-break: break-word;
}

.chat-msg.user .chat-msg-body {
  background: var(--primary-500);
  color: white;
  border-bottom-right-radius: 4px;
}

.chat-msg.assistant .chat-msg-body {
  background: var(--bg-primary);
  color: var(--text-primary);
  border-bottom-left-radius: 4px;
  border: 1px solid var(--gray-200);
}

.chat-msg-body.streaming {
  min-height: 24px;
}

.cursor-blink {
  animation: blink 1s step-end infinite;
  color: var(--primary-500);
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.chat-input-full {
  padding: 16px 24px;
  border-top: 1px solid var(--gray-200);
  background: var(--bg-primary);
}

.chat-input-row {
  display: flex;
  gap: 12px;
  align-items: center;
}

.chat-input-row .el-input {
  flex: 1;
}

.markdown-body {
  font-size: 14px;
  line-height: 1.7;
}

.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3) {
  margin: 8px 0 4px;
  color: var(--primary-600);
  font-weight: 600;
}

.markdown-body :deep(ul),
.markdown-body :deep(ol) {
  padding-left: 16px;
  margin: 4px 0;
}

.markdown-body :deep(strong) {
  color: var(--primary-600);
}

.markdown-body :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 8px 0;
  font-size: 13px;
}

.markdown-body :deep(th),
.markdown-body :deep(td) {
  border: 1px solid var(--gray-200);
  padding: 4px 8px;
  text-align: left;
}

.markdown-body :deep(th) {
  background: var(--primary-50);
  color: var(--primary-700);
}

.mt-4 {
  margin-top: 16px;
}
</style>
