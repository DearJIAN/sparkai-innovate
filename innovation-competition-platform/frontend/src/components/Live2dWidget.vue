<template>
  <teleport to="body">
    <div ref="waifuContainer" class="live2d-widget-container">
      <div id="waifu" class="waifu" v-show="visible">
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
      <div v-if="!loaded && !loadError" class="live2d-loading">
        <el-icon class="is-loading" size="32"><Loading /></el-icon>
        <span>火花加载中...</span>
      </div>
      <div v-if="loadError" class="live2d-error" @click="retryInit">
        <el-icon size="24"><WarningFilled /></el-icon>
        <span>加载失败，点击重试</span>
      </div>
    </div>
  </teleport>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { Loading, WarningFilled } from '@element-plus/icons-vue'
import { useLive2d } from '@/composables/useLive2d'

const { detectEmotionByText, getExpressionByEmotion, updateExpressionByText, notifyLive2dHook } = useLive2d()

const showTips = ref(false)
const tipText = ref('')
const waifuContainer = ref(null)
const visible = ref(true)
const loaded = ref(false)
const loadError = ref(false)
let retryCount = 0

const tools = [
  { name: '切换表情', icon: '😊', action: () => switchExpression() },
  { name: '隐藏', icon: '✖', action: () => hideWaifu() },
]

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

  window.__applySpeechStateToCore = (state) => {
    const model = window.__live2dModel
    if (!model) return
    if (model.coreModel && model.coreModel.internalModel) {
      const core = model.coreModel.internalModel
      if (core.setParameterValueById) {
        const mouthOpenY = state.mouthOpenY !== undefined ? state.mouthOpenY : 0
        core.setParameterValueById('ParamMouthOpenY', mouthOpenY)
      }
    }
  }

  window.__applyOverlayStateToCore = (overlayNames) => {
    const model = window.__live2dModel
    if (model && model.setExpression) {
      overlayNames.forEach(name => model.setExpression(name))
    }
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
    onSpeechStart: () => {
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

async function loadLive2DLibraries() {
  return new Promise((resolve, reject) => {
    const TIMEOUT_MS = 15000
    let resolved = false
    const timer = setTimeout(() => {
      if (!resolved) {
        resolved = true
        reject(new Error('Live2D library load timeout'))
      }
    }, TIMEOUT_MS)

    const checkAndResolve = () => {
      if (!resolved) {
        resolved = true
        clearTimeout(timer)
        resolve()
      }
    }

    const existingCss = document.querySelector('link[href*="waifu.css"]')
    if (!existingCss) {
      const link = document.createElement('link')
      link.rel = 'stylesheet'
      link.href = '/live2d-widget-dist/waifu.css'
      link.onload = checkAndResolve
      document.head.appendChild(link)
    }

    const existingScript = document.querySelector('script[src*="live2d-widget-dist/chunk/index"]')
    if (!existingScript) {
      const script1 = document.createElement('script')
      script1.src = '/live2d-widget-dist/chunk/index.js'
      script1.onload = checkAndResolve
      script1.onerror = () => { if (!resolved) { resolved = true; clearTimeout(timer); reject(new Error('Failed to load index.js')) } }
      document.body.appendChild(script1)

      const script2 = document.createElement('script')
      script2.src = '/live2d-widget-dist/chunk/index2.js'
      script2.onload = checkAndResolve
      script2.onerror = () => { if (!resolved) { resolved = true; clearTimeout(timer); reject(new Error('Failed to load index2.js')) } }
      document.body.appendChild(script2)
    }

    const existingTipsScript = document.querySelector('script[src*="waifu-tips"]')
    if (!existingTipsScript) {
      const tipsScript = document.createElement('script')
      tipsScript.src = '/live2d-widget-dist/waifu-tips.js'
      tipsScript.onload = checkAndResolve
      tipsScript.onerror = () => { if (!resolved) { resolved = true; clearTimeout(timer); reject(new Error('Failed to load waifu-tips.js')) } }
      document.body.appendChild(tipsScript)
    }

    setTimeout(checkAndResolve, 2000)
  })
}

async function initLive2D() {
  try {
    loadError.value = false
    await loadLive2DLibraries()

    await new Promise((resolve, reject) => {
      let attempts = 0
      const maxAttempts = 20
      const interval = setInterval(() => {
        attempts++
        if (window.initWidget) {
          clearInterval(interval)
          resolve()
        } else if (attempts >= maxAttempts) {
          clearInterval(interval)
          reject(new Error('initWidget not found after waiting'))
        }
      }, 300)
    })

    if (window.initWidget) {
      window.initWidget({
        cdnPath: '/live2d/huahuo/',
        waifuPath: '/live2d-widget-dist/waifu-huahuo.json',
      })
    }

    await new Promise((resolve) => {
      let attempts = 0
      const maxAttempts = 30
      const interval = setInterval(() => {
        attempts++
        const canvas = document.getElementById('live2d')
        if (canvas && canvas.getContext('2d') && canvas.width > 0) {
          const ctx = canvas.getContext('2d')
          const imageData = ctx.getImageData(0, 0, 1, 1)
          if (imageData.data[3] > 0) {
            clearInterval(interval)
            loaded.value = true
            resolve()
          }
        }
        if (attempts >= maxAttempts) {
          clearInterval(interval)
          loaded.value = true
          resolve()
        }
      }, 300)
    })

  } catch (err) {
    console.warn('Live2D init error:', err.message)
    loadError.value = true
  }
}

function retryInit() {
  if (retryCount >= 3) {
    loadError.value = false
    return
  }
  retryCount++
  loadError.value = false
  loaded.value = false
  initLive2D()
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
  const scripts = document.querySelectorAll('script[src*="live2d"], script[src*="waifu-tips"], script[src*="chunk/index"]')
  scripts.forEach(s => s.remove())
  const links = document.querySelectorAll('link[href*="waifu"]')
  links.forEach(l => l.remove())
  const waifuEl = document.getElementById('waifu')
  if (waifuEl) waifuEl.remove()
  try {
    delete window.__expressionControlsState
    delete window.__voiceLive2dHooks
    delete window.__syncExpressionState
    delete window.__live2dModel
    delete window.__applySpeechStateToCore
    delete window.__applyOverlayStateToCore
    delete window.initWidget
    delete window.loadlive2d
  } catch (_e) {}
})
</script>

<style>
.live2d-widget-container {
  z-index: 9999;
  position: fixed;
  bottom: 0;
  right: 20px;
}

#waifu {
  position: relative;
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

#wafu:hover .waifu-tool,
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
  text-align: center;
}

.live2d-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: var(--primary-500);
  font-size: 13px;
  padding: 12px 20px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.live2d-error {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #ef4444;
  font-size: 13px;
  padding: 10px 16px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 10px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: background 0.2s;
}

.live2d-error:hover {
  background: rgba(255, 255, 255, 1);
}
</style>
