<template>
  <teleport to="body">
    <div ref="waifuContainer" class="live2d-widget-container">
      <div id="waifu" class="waifu">
        <div class="waifu-tips" v-show="showTips" @click="showTips = false">
          <span>{{ tipText }}</span>
        </div>
        <canvas id="live2d" width="320" height="400"></canvas>
        <div class="waifu-tool">
          <span v-for="tool in tools" :key="tool.name" @click="tool.action" :title="tool.name">
            {{ tool.icon }}
          </span>
        </div>
      </div>
    </div>
  </teleport>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const showTips = ref(false)
const tipText = ref('')
const waifuContainer = ref(null)

const tools = [
  { name: '切换表情', icon: '😊', action: () => switchExpression() },
  { name: '切换模型', icon: '👗', action: () => switchModel() },
  { name: '隐藏', icon: '✖', action: () => hideWaifu() },
]

const visible = ref(true)

function switchExpression() {
  if (window.__expressionControlsState) {
    const state = window.__expressionControlsState
    const expressions = state.baseExpressions || []
    if (expressions.length > 0) {
      const randomExpr = expressions[Math.floor(Math.random() * expressions.length)]
      if (window.__syncExpressionState) {
        window.__syncExpressionState(randomExpr)
      }
    }
  }
}

function switchModel() {
  if (window.loadlive2d) {
    window.loadlive2d('live2d', '/live2d/huahuo/火花.model3.json')
  }
}

function hideWaifu() {
  const waifuEl = document.getElementById('waifu')
  if (waifuEl) {
    waifuEl.style.display = 'none'
  }
  visible.value = false
}

function showWaifu() {
  const waifuEl = document.getElementById('waifu')
  if (waifuEl) {
    waifuEl.style.display = 'block'
  }
  visible.value = true
}

function initLive2D() {
  const existingLink = document.querySelector('link[href*="waifu.css"]')
  if (!existingLink) {
    const link = document.createElement('link')
    link.rel = 'stylesheet'
    link.href = '/live2d-widget-dist/waifu.css'
    document.head.appendChild(link)
  }

  const existingScript = document.querySelector('script[src*="waifu-tips"]')
  if (!existingScript) {
    const script = document.createElement('script')
    script.src = '/live2d-widget-dist/waifu-tips.js'
    script.onload = () => {
      setTimeout(() => {
        if (window.initWidget) {
          window.initWidget({
            cdnPath: '/live2d/huahuo/',
            waifuPath: '/live2d-widget-dist/waifu-huahuo.json',
          })
        }
      }, 500)
    }
    document.body.appendChild(script)
  }
}

function setupExpressionControls() {
  window.__expressionControlsState = {
    baseExpressions: [
      '01黑脸', '02 脸红爱心', '03 生气', '04 晕', '05 ＞＜',
      '06 0.0', '07 星星眼', '08 流泪', '10 捧心', '11 要饭'
    ],
    overlayExpressions: ['月卡', '水印'],
    currentBase: '',
    currentOverlays: [],
  }

  window.__syncExpressionState = (expressionName) => {
    const model = window.__live2dModel
    if (model && model.setExpression) {
      model.setExpression(expressionName)
    }
    window.__expressionControlsState.currentBase = expressionName
  }
}

function setupVoiceHooks() {
  window.__voiceLive2dHooks = {
    onStreamStart: () => {
      window.__syncExpressionState && window.__syncExpressionState('07 星星眼')
    },
    onDelta: (payload) => {
      const textLen = (payload?.text || payload || '').length
      const openY = Math.min(1, textLen / 20)
      if (window.__applySpeechStateToCore) {
        window.__applySpeechStateToCore({ mouthOpenY: openY })
      }
    },
    onStreamEnd: () => {
      window.__syncExpressionState && window.__syncExpressionState('06 0.0')
      if (window.__applySpeechStateToCore) {
        window.__applySpeechStateToCore({ mouthOpenY: 0 })
      }
    },
    onSpeechStart: (payload) => {
      window.__syncExpressionState && window.__syncExpressionState('07 星星眼')
    },
    onSpeechPulse: (payload) => {
      const intensity = payload?.intensity || 0.5
      if (window.__applySpeechStateToCore) {
        window.__applySpeechStateToCore({ mouthOpenY: intensity })
      }
    },
    onSpeechEnd: () => {
      window.__syncExpressionState && window.__syncExpressionState('06 0.0')
      if (window.__applySpeechStateToCore) {
        window.__applySpeechStateToCore({ mouthOpenY: 0 })
      }
    },
  }
}

function detectEmotionByText(text) {
  const lower = (text || '').toLowerCase()
  if (/开心|高兴|太好了|哈哈|棒|厉害|优秀|成功|恭喜/.test(lower)) return 'happy'
  if (/害羞|脸红|不好意思|羞/.test(lower)) return 'shy'
  if (/生气|愤怒|烦|讨厌|气死/.test(lower)) return 'angry'
  if (/难过|伤心|失望|遗憾|抱歉/.test(lower)) return 'sad'
  if (/晕|头晕|困惑|迷茫|不懂/.test(lower)) return 'dizzy'
  if (/惊讶|天哪|哇|震惊|意外/.test(lower)) return 'surprise'
  return null
}

function getExpressionByEmotion(emotion) {
  const map = {
    happy: '02 脸红爱心',
    shy: '02 脸红爱心',
    angry: '03 生气',
    sad: '08 流泪',
    dizzy: '04 晕',
    surprise: '07 星星眼',
  }
  return map[emotion] || '06 0.0'
}

function notifyLive2dHook(name, payload) {
  try {
    const hooks = window.__voiceLive2dHooks
    const fn = hooks && typeof hooks[name] === 'function' ? hooks[name] : null
    if (fn) fn(payload)
  } catch (_error) {}
}

function updateExpressionByText(text) {
  const emotion = detectEmotionByText(text)
  if (emotion) {
    const expression = getExpressionByEmotion(emotion)
    window.__syncExpressionState && window.__syncExpressionState(expression)
  }
}

defineExpose({
  showWaifu,
  hideWaifu,
  switchExpression,
  updateExpressionByText,
  notifyLive2dHook,
})

onMounted(() => {
  setupExpressionControls()
  setupVoiceHooks()
  initLive2D()
})

onBeforeUnmount(() => {
  const scripts = document.querySelectorAll('script[src*="live2d"]')
  scripts.forEach(s => s.remove())
})
</script>

<style>
.live2d-widget-container {
  z-index: 9999;
}

#waifu {
  position: fixed;
  bottom: 0;
  right: 20px;
  z-index: 9999;
  cursor: grab;
  user-select: none;
}

#waifu:active {
  cursor: grabbing;
}

.waifu-tool {
  display: flex;
  gap: 8px;
  justify-content: center;
  padding: 4px 8px;
  opacity: 0;
  transition: opacity 0.3s;
}

#waifu:hover .waifu-tool {
  opacity: 1;
}

.waifu-tool span {
  cursor: pointer;
  font-size: 16px;
  padding: 2px 6px;
  border-radius: 4px;
  transition: background 0.2s;
}

.waifu-tool span:hover {
  background: rgba(255, 255, 255, 0.3);
}

.waifu-tips {
  position: absolute;
  top: -60px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.7);
  color: #fff;
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 13px;
  white-space: nowrap;
  cursor: pointer;
  max-width: 280px;
  white-space: normal;
  text-align: center;
}
</style>
