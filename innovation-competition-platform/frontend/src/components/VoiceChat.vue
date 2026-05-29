<template>
  <div ref="panelRef" class="voice-chat-panel" :class="{ collapsed: isCollapsed }" :style="panelStyle">
    <div class="panel-header" @mousedown="startDrag" @touchstart="startDragTouch">
      <div class="header-left">
        <span class="panel-title">🤖 AI 对话</span>
        <el-tag v-if="isListening" type="danger" size="small" effect="dark" class="listening-tag">录音中</el-tag>
      </div>
      <div class="header-actions">
        <el-button :icon="isCollapsed ? 'ArrowUp' : 'ArrowDown'" size="small" text @click.stop="isCollapsed = !isCollapsed" />
        <el-button icon="Close" size="small" text @click.stop="$emit('close')" />
      </div>
    </div>

    <div v-show="!isCollapsed" class="panel-body">
      <div ref="messagesRef" class="chat-messages">
        <div v-if="messages.length === 0" class="empty-hint">
          <p>👋 你好！我是火花，你的 AI 助手</p>
          <p>可以输入文字或点击麦克风语音对话</p>
          <div class="quick-questions">
            <el-button v-for="q in quickQuestions" :key="q" size="small" round @click="sendQuickQuestion(q)">{{ q }}</el-button>
          </div>
        </div>
        <div v-for="(msg, idx) in messages" :key="idx" class="message-item" :class="msg.role">
          <div class="message-avatar">{{ msg.role === 'user' ? '👤' : '🤖' }}</div>
          <div class="message-content">
            <div v-if="msg.role === 'assistant'" class="markdown-body" v-html="renderMarkdown(msg.content)"></div>
            <div v-else>{{ msg.content }}</div>
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
            <el-button @click="sendMessage" :loading="isStreaming" :disabled="!inputText.trim()">
              发送
            </el-button>
          </template>
        </el-input>
        <div class="voice-controls">
          <el-button
            :type="isListening ? 'danger' : 'primary'"
            :icon="isListening ? 'Microphone' : 'Microphone'"
            circle
            @click="toggleVoiceRecognition"
            :loading="isAsrProcessing"
          />
          <el-button
            v-if="currentReplyText"
            :icon="isSpeaking ? 'VideoPause' : 'VideoPlay'"
            circle
            @click="toggleSpeech"
          />
          <el-button icon="Delete" circle size="small" @click="clearMessages" title="清空对话" />
          <el-button icon="Plus" circle size="small" @click="newSession" title="新会话" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, onBeforeUnmount, watch } from 'vue'
import { marked } from 'marked'
import { chatStream, voiceChatStream, uploadAsrAudio } from '@/api/ai'
import { ElMessage } from 'element-plus'
import { useLive2d } from '@/composables/useLive2d'

const { notifyLive2dHook } = useLive2d()

const emit = defineEmits(['close', 'stream-start', 'stream-delta', 'stream-end', 'reply'])

const messages = ref([])
const inputText = ref('')
const isStreaming = ref(false)
const streamingText = ref('')
const currentReplyText = ref('')
const sessionId = ref('')
const isCollapsed = ref(false)
const isListening = ref(false)
const isAsrProcessing = ref(false)
const isSpeaking = ref(false)
const messagesRef = ref(null)
const panelRef = ref(null)

const quickQuestions = [
  '你可以做什么？',
  '帮我生成项目简介',
  '竞赛有哪些赛道？',
  '如何组建团队？',
]

let recognition = null
let speechUtterance = null
let dragState = { dragging: false, startX: 0, startY: 0, offsetX: 0, offsetY: 0 }
const panelStyle = ref({})

const panelPos = ref({ x: 0, y: 0 })

marked.setOptions({
  breaks: true,
  gfm: true,
})

function renderMarkdown(text) {
  if (!text) return ''
  try {
    return marked.parse(text)
  } catch {
    return text
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (messagesRef.value) {
      messagesRef.value.scrollTop = messagesRef.value.scrollHeight
    }
  })
}

watch(messages, () => scrollToBottom(), { deep: true })
watch(streamingText, () => scrollToBottom())

async function sendMessage(options = {}) {
  const { autoSpeak = false } = options
  const text = inputText.value.trim()
  if (!text || isStreaming.value) return

  messages.value.push({ role: 'user', content: text })
  inputText.value = ''
  isStreaming.value = true
  streamingText.value = ''
  currentReplyText.value = ''

  notifyLive2dHook('onStreamStart')

  try {
    const response = await chatStream(text, sessionId.value)
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''
    let streamServerError = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n')
      buffer = lines.pop() || ''

      for (const line of lines) {
        if (line.startsWith('sessionId:')) {
          sessionId.value = line.slice(10).trim()
        } else if (line.startsWith('delta:')) {
          const delta = line.slice(6)
          streamingText.value += delta
          currentReplyText.value += delta
          notifyLive2dHook('onDelta', { text: delta })
        } else if (line.startsWith('error:')) {
          streamServerError = line.slice(6).trim()
          ElMessage.error(streamServerError)
        }
      }
    }

    if (streamingText.value) {
      messages.value.push({ role: 'assistant', content: streamingText.value })
      emit('reply', streamingText.value)
      if (autoSpeak) {
        speakText(streamingText.value, { forceRestart: true })
      }
    } else if (streamServerError) {
      const billingError = streamServerError.includes('Arrearage') || streamServerError.includes('overdue-payment') || streamServerError.includes('Access denied')
      messages.value.push({
        role: 'assistant',
        content: billingError
          ? '当前 AI 服务账号状态异常（欠费/权限受限），本次无法生成回复。请先恢复账号状态。'
          : `本次对话失败：${streamServerError}`
      })
    }
  } catch (err) {
    ElMessage.error('发送失败：' + err.message)
  } finally {
    isStreaming.value = false
    streamingText.value = ''
    notifyLive2dHook('onStreamEnd')
  }
}

function sendQuickQuestion(question) {
  inputText.value = question
  sendMessage()
}

function toggleVoiceRecognition() {
  if (isListening.value) {
    stopVoiceRecognition()
  } else {
    startVoiceRecognition()
  }
}

function startVoiceRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
  if (SpeechRecognition) {
    recognition = new SpeechRecognition()
    recognition.lang = 'zh-CN'
    recognition.continuous = false
    recognition.interimResults = true

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
      if (interimTranscript) {
        inputText.value = interimTranscript
      }
      if (finalTranscript) {
        inputText.value = finalTranscript
        nextTick(() => sendMessage({ autoSpeak: true }))
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

async function startFirefoxVoice() {
  try {
    isListening.value = true
    isAsrProcessing.value = true
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    const mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' })
    const chunks = []

    mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) chunks.push(e.data)
    }

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
          inputText.value = result.text
          nextTick(() => sendMessage({ autoSpeak: true }))
        } else {
          ElMessage.error('语音识别失败')
        }
      } catch (err) {
        ElMessage.error('语音识别失败：' + err.message)
      } finally {
        isAsrProcessing.value = false
      }
    }

    mediaRecorder.start()
    setTimeout(() => {
      if (mediaRecorder.state === 'recording') {
        mediaRecorder.stop()
      }
    }, 5000)
  } catch (err) {
    isListening.value = false
    isAsrProcessing.value = false
    ElMessage.error('无法访问麦克风：' + err.message)
  }
}

function toggleSpeech() {
  if (isSpeaking.value) {
    window.speechSynthesis.cancel()
    isSpeaking.value = false
    notifyLive2dHook('onSpeechEnd')
    return
  }

  if (!currentReplyText.value) return

  speakText(currentReplyText.value)
}

function speakText(text, options = {}) {
  const { forceRestart = false } = options
  if (!text) return
  if (forceRestart && isSpeaking.value) {
    window.speechSynthesis.cancel()
    isSpeaking.value = false
    notifyLive2dHook('onSpeechEnd')
  }

  const utterance = new SpeechSynthesisUtterance(text)
  utterance.lang = 'zh-CN'
  utterance.rate = 1.0
  utterance.pitch = 1.0

  const voices = window.speechSynthesis.getVoices()
  const zhVoice = voices.find(v => v.lang.startsWith('zh') && v.name.includes('Female'))
    || voices.find(v => v.lang.startsWith('zh'))
  if (zhVoice) utterance.voice = zhVoice

  utterance.onstart = () => {
    isSpeaking.value = true
    notifyLive2dHook('onSpeechStart')
  }

  utterance.onend = () => {
    isSpeaking.value = false
    notifyLive2dHook('onSpeechEnd')
  }

  utterance.onerror = () => {
    isSpeaking.value = false
    notifyLive2dHook('onSpeechEnd')
  }

  window.speechSynthesis.speak(utterance)
}

function clearMessages() {
  if (window.speechSynthesis && isSpeaking.value) {
    window.speechSynthesis.cancel()
    isSpeaking.value = false
    notifyLive2dHook('onSpeechEnd')
  }
  messages.value = []
  currentReplyText.value = ''
  streamingText.value = ''
}

function newSession() {
  clearMessages()
  sessionId.value = ''
}

function startDrag(e) {
  dragState.dragging = true
  dragState.startX = e.clientX - (panelPos.value.x || 0)
  dragState.startY = e.clientY - (panelPos.value.y || 0)
  document.addEventListener('mousemove', onDrag)
  document.addEventListener('mouseup', stopDrag)
}

function startDragTouch(e) {
  const touch = e.touches[0]
  dragState.dragging = true
  dragState.startX = touch.clientX - (panelPos.value.x || 0)
  dragState.startY = touch.clientY - (panelPos.value.y || 0)
  document.addEventListener('touchmove', onDragTouch, { passive: false })
  document.addEventListener('touchend', stopDragTouch)
}

function onDrag(e) {
  if (!dragState.dragging) return
  panelPos.value.x = e.clientX - dragState.startX
  panelPos.value.y = e.clientY - dragState.startY
  panelStyle.value = {
    transform: `translate(${panelPos.value.x}px, ${panelPos.value.y}px)`,
  }
}

function onDragTouch(e) {
  if (!dragState.dragging) return
  e.preventDefault()
  const touch = e.touches[0]
  panelPos.value.x = touch.clientX - dragState.startX
  panelPos.value.y = touch.clientY - dragState.startY
  panelStyle.value = {
    transform: `translate(${panelPos.value.x}px, ${panelPos.value.y}px)`,
  }
}

function stopDrag() {
  dragState.dragging = false
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
  try {
    localStorage.setItem('voiceChatPos', JSON.stringify(panelPos.value))
  } catch (_e) {}
}

function stopDragTouch() {
  dragState.dragging = false
  document.removeEventListener('touchmove', onDragTouch)
  document.removeEventListener('touchend', stopDragTouch)
  try {
    localStorage.setItem('voiceChatPos', JSON.stringify(panelPos.value))
  } catch (_e) {}
}

onMounted(() => {
  try {
    const saved = localStorage.getItem('voiceChatPos')
    if (saved) {
      panelPos.value = JSON.parse(saved)
      panelStyle.value = {
        transform: `translate(${panelPos.value.x}px, ${panelPos.value.y}px)`,
      }
    }
  } catch (_e) {}

  if (window.speechSynthesis) {
    window.speechSynthesis.getVoices()
    window.speechSynthesis.onvoiceschanged = () => {
      window.speechSynthesis.getVoices()
    }
  }
})

onBeforeUnmount(() => {
  stopVoiceRecognition()
  if (window.speechSynthesis) {
    window.speechSynthesis.cancel()
  }
})
</script>

<style scoped>
.voice-chat-panel {
  position: fixed;
  bottom: 20px;
  right: 360px;
  width: 400px;
  max-height: 560px;
  background: rgba(15, 23, 42, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid rgba(6, 182, 212, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(6, 182, 212, 0.1);
  display: flex;
  flex-direction: column;
  z-index: 10000;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.voice-chat-panel.collapsed {
  max-height: 48px;
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
  gap: 4px;
}

.panel-body {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 12px 16px;
  max-height: 380px;
  min-height: 200px;
}

.chat-messages::-webkit-scrollbar {
  width: 4px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: rgba(6, 182, 212, 0.3);
  border-radius: 2px;
}

.empty-hint {
  text-align: center;
  color: #94a3b8;
  padding: 20px 0;
}

.empty-hint p {
  margin: 8px 0;
  font-size: 14px;
}

.quick-questions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  margin-top: 12px;
}

.message-item {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
  align-items: flex-start;
}

.message-item.user {
  flex-direction: row-reverse;
}

.message-avatar {
  font-size: 20px;
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.message-content {
  max-width: 280px;
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 13px;
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

.message-content.streaming {
  min-height: 24px;
}

.cursor-blink {
  animation: blink 1s step-end infinite;
  color: #06b6d4;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.chat-input-area {
  padding: 12px 16px;
  border-top: 1px solid rgba(6, 182, 212, 0.15);
  background: rgba(15, 23, 42, 0.8);
}

.voice-controls {
  display: flex;
  gap: 8px;
  margin-top: 8px;
  justify-content: center;
  align-items: center;
}

.markdown-body {
  font-size: 13px;
  line-height: 1.6;
}

.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3) {
  margin: 8px 0 4px;
  color: #06b6d4;
  font-weight: 600;
}

.markdown-body :deep(h1) { font-size: 16px; }
.markdown-body :deep(h2) { font-size: 15px; }
.markdown-body :deep(h3) { font-size: 14px; }

.markdown-body :deep(ul),
.markdown-body :deep(ol) {
  padding-left: 16px;
  margin: 4px 0;
}

.markdown-body :deep(li) {
  margin: 2px 0;
}

.markdown-body :deep(strong) {
  color: #22d3ee;
}

.markdown-body :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 8px 0;
  font-size: 12px;
}

.markdown-body :deep(th),
.markdown-body :deep(td) {
  border: 1px solid rgba(6, 182, 212, 0.2);
  padding: 4px 8px;
  text-align: left;
}

.markdown-body :deep(th) {
  background: rgba(6, 182, 212, 0.15);
  color: #06b6d4;
}

.markdown-body :deep(code) {
  background: rgba(6, 182, 212, 0.1);
  padding: 1px 4px;
  border-radius: 3px;
  font-size: 12px;
}

.markdown-body :deep(pre) {
  background: rgba(0, 0, 0, 0.3);
  padding: 8px;
  border-radius: 6px;
  overflow-x: auto;
  margin: 8px 0;
}

.markdown-body :deep(pre code) {
  background: none;
  padding: 0;
}
</style>
