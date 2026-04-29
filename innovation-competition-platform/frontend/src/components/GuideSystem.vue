<template>
  <teleport to="body">
    <!-- 引导遮罩层 -->
    <transition name="guide-fade">
      <div
        v-if="guideStore.isVisible"
        class="guide-overlay"
        :style="{ opacity: guideStore.opacityValue }"
        @click.self="handleOverlayClick"
      >
        <!-- 高亮区域 -->
        <div
          v-if="currentStepData.target && highlightRect"
          class="guide-highlight"
          :style="highlightStyle"
        >
          <div class="highlight-border"></div>
        </div>

        <!-- 引导弹窗 - 可拖拽 -->
        <div
          ref="guideDialogRef"
          class="guide-dialog"
          :class="[`position-${currentStepData.position || 'center'}`]"
          :style="dialogPosition"
          @mousedown="startDrag"
        >
          <!-- 拖拽手柄 -->
          <div class="guide-drag-handle">
            <div class="drag-dots">
              <span></span><span></span><span></span>
            </div>
          </div>

          <!-- 步骤指示器 -->
          <div class="guide-step-indicator">
            <div
              v-for="(step, index) in totalSteps"
              :key="index"
              class="step-dot"
              :class="{ active: index === guideStore.currentStep, completed: index < guideStore.currentStep }"
              @click="guideStore.goToStep(index)"
            >
              <span v-if="index < guideStore.currentStep" class="step-check">✓</span>
              <span v-else>{{ index + 1 }}</span>
            </div>
          </div>

          <!-- 内容区域 -->
          <div class="guide-content">
            <h3 class="guide-title">{{ currentStepData.title }}</h3>
            <p class="guide-text">{{ currentStepData.content }}</p>
          </div>

          <!-- 按钮区域 -->
          <div class="guide-actions">
            <el-button
              v-if="guideStore.currentStep > 0"
              class="guide-btn-prev"
              @click="guideStore.prevStep"
            >
              <el-icon><ArrowLeft /></el-icon>
              上一步
            </el-button>
            <div class="guide-actions-spacer"></div>
            <el-button
              v-if="guideStore.currentStep < totalSteps - 1"
              type="primary"
              class="guide-btn-next"
              @click="guideStore.nextStep"
            >
              下一步
              <el-icon><ArrowRight /></el-icon>
            </el-button>
            <el-button
              v-else
              type="success"
              class="guide-btn-finish"
              @click="finishGuide"
            >
              <el-icon><CircleCheck /></el-icon>
              完成引导
            </el-button>
          </div>

          <!-- 底部工具栏 -->
          <div class="guide-toolbar">
            <div class="opacity-control">
              <el-icon size="14"><Sunny /></el-icon>
              <el-slider
                v-model="guideStore.opacity"
                :min="10"
                :max="100"
                :show-tooltip="false"
                size="small"
                class="opacity-slider"
                @change="guideStore.setOpacity"
              />
              <el-icon size="14"><Moon /></el-icon>
            </div>
            <el-button
              link
              size="small"
              class="skip-btn"
              @click="skipGuide"
            >
              暂不需要引导
            </el-button>
          </div>
        </div>
      </div>
    </transition>

    <!-- 左侧重新打开按钮 -->
    <transition name="guide-btn-slide">
      <div
        v-if="showReopenButton"
        class="guide-reopen-btn"
        @click="reopenGuide"
        title="重新打开引导"
      >
        <el-icon size="18"><Guide /></el-icon>
        <span class="reopen-text">使用引导</span>
      </div>
    </transition>

    <!-- 首次登录询问弹窗 -->
    <el-dialog
      v-model="showWelcomeDialog"
      title="欢迎使用创新创业平台"
      width="420px"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      align-center
      class="welcome-dialog"
    >
      <div class="welcome-content">
        <div class="welcome-icon">
          <el-icon size="48" color="var(--primary-500)"><Compass /></el-icon>
        </div>
        <p class="welcome-text">
          您好，{{ userStore.userInfo?.real_name || userStore.userInfo?.username }}！<br>
          是否需要引导您快速了解系统功能？
        </p>
      </div>
      <template #footer>
        <div class="welcome-actions">
          <el-button @click="handleWelcomeSkip">暂不需要</el-button>
          <el-button type="primary" @click="handleWelcomeStart">
            <el-icon><Guide /></el-icon>
            开始引导
          </el-button>
        </div>
      </template>
    </el-dialog>
  </teleport>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useGuideStore } from '@/stores/guide'
import { useUserStore } from '@/stores/user'
import { ArrowLeft, ArrowRight, CircleCheck, Guide, Compass, Sunny, Moon } from '@element-plus/icons-vue'

const guideStore = useGuideStore()
const userStore = useUserStore()

const guideDialogRef = ref(null)
const showWelcomeDialog = ref(false)
const showReopenButton = ref(false)
const highlightRect = ref(null)

// 拖拽相关
const isDragging = ref(false)
const dragOffset = ref({ x: 0, y: 0 })
const dialogPos = ref({ x: 0, y: 0 })

// 计算当前步骤数据
const currentStepData = computed(() => {
  const steps = guideStore.getStepsByRole(guideStore.currentRole)
  return steps[guideStore.currentStep] || {}
})

const totalSteps = computed(() => {
  return guideStore.getStepsByRole(guideStore.currentRole).length
})

// 高亮框样式
const highlightStyle = computed(() => {
  if (!highlightRect.value) return {}
  const padding = 8
  return {
    left: `${highlightRect.value.left - padding}px`,
    top: `${highlightRect.value.top - padding}px`,
    width: `${highlightRect.value.width + padding * 2}px`,
    height: `${highlightRect.value.height + padding * 2}px`
  }
})

// 弹窗位置
const dialogPosition = computed(() => {
  const position = currentStepData.value.position || 'center'
  const baseStyle = {}

  if (dialogPos.value.x !== 0 || dialogPos.value.y !== 0) {
    return {
      left: `${dialogPos.value.x}px`,
      top: `${dialogPos.value.y}px`,
      transform: 'none'
    }
  }

  if (position === 'center') {
    return {
      left: '50%',
      top: '50%',
      transform: 'translate(-50%, -50%)'
    }
  }

  // 如果有目标元素，计算相对位置
  if (highlightRect.value) {
    const rect = highlightRect.value
    const dialogWidth = 420
    const dialogHeight = 300
    const gap = 20

    switch (position) {
      case 'bottom':
        return {
          left: `${rect.left + rect.width / 2 - dialogWidth / 2}px`,
          top: `${rect.bottom + gap}px`,
          transform: 'none'
        }
      case 'top':
        return {
          left: `${rect.left + rect.width / 2 - dialogWidth / 2}px`,
          top: `${rect.top - dialogHeight - gap}px`,
          transform: 'none'
        }
      case 'left':
        return {
          left: `${rect.left - dialogWidth - gap}px`,
          top: `${rect.top + rect.height / 2 - dialogHeight / 2}px`,
          transform: 'none'
        }
      case 'right':
        return {
          left: `${rect.right + gap}px`,
          top: `${rect.top + rect.height / 2 - dialogHeight / 2}px`,
          transform: 'none'
        }
    }
  }

  return baseStyle
})

// 更新高亮区域
const updateHighlight = async () => {
  await nextTick()
  const target = currentStepData.value.target
  if (target) {
    const el = document.querySelector(target)
    if (el) {
      highlightRect.value = el.getBoundingClientRect()
      // 滚动到元素
      el.scrollIntoView({ behavior: 'smooth', block: 'center' })
    } else {
      highlightRect.value = null
    }
  } else {
    highlightRect.value = null
  }
  // 重置弹窗位置
  dialogPos.value = { x: 0, y: 0 }
}

// 监听步骤变化
watch(() => guideStore.currentStep, () => {
  updateHighlight()
})

watch(() => guideStore.isVisible, (visible) => {
  if (visible) {
    updateHighlight()
  }
})

// 拖拽功能
const startDrag = (e) => {
  if (e.target.closest('.guide-drag-handle')) {
    isDragging.value = true
    const rect = guideDialogRef.value.getBoundingClientRect()
    dragOffset.value = {
      x: e.clientX - rect.left,
      y: e.clientY - rect.top
    }
    document.addEventListener('mousemove', onDrag)
    document.addEventListener('mouseup', stopDrag)
  }
}

const onDrag = (e) => {
  if (isDragging.value) {
    dialogPos.value = {
      x: e.clientX - dragOffset.value.x,
      y: e.clientY - dragOffset.value.y
    }
  }
}

const stopDrag = () => {
  isDragging.value = false
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
}

// 处理遮罩点击
const handleOverlayClick = () => {
  // 点击遮罩不关闭，防止误触
}

// 跳过引导
const skipGuide = () => {
  guideStore.hideGuide()
  showReopenButton.value = true
  localStorage.setItem('guide_skipped', 'true')
}

// 完成引导
const finishGuide = () => {
  guideStore.hideGuide()
  showReopenButton.value = false
  localStorage.setItem('guide_completed', 'true')
  localStorage.setItem('guide_skipped', 'false')
}

// 重新打开引导
const reopenGuide = () => {
  guideStore.showGuide(userStore.userInfo?.role)
  showReopenButton.value = false
}

// 欢迎弹窗处理
const handleWelcomeStart = () => {
  showWelcomeDialog.value = false
  guideStore.showGuide(userStore.userInfo?.role, true)
}

const handleWelcomeSkip = () => {
  showWelcomeDialog.value = false
  showReopenButton.value = true
  localStorage.setItem('guide_skipped', 'true')
}

// 检查是否需要显示欢迎弹窗
const checkWelcome = () => {
  const isFirstTime = !localStorage.getItem('guide_completed') && !localStorage.getItem('guide_skipped')
  if (isFirstTime && userStore.isLoggedIn) {
    showWelcomeDialog.value = true
  } else if (localStorage.getItem('guide_skipped') === 'true') {
    showReopenButton.value = true
  }
}

// 监听登录状态
watch(() => userStore.isLoggedIn, (loggedIn) => {
  if (loggedIn) {
    setTimeout(checkWelcome, 500)
  }
})

onMounted(() => {
  if (userStore.isLoggedIn) {
    checkWelcome()
  }
  window.addEventListener('resize', updateHighlight)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateHighlight)
})
</script>

<style scoped>
/* 遮罩层 */
.guide-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.75);
  z-index: 9998;
  transition: opacity 0.3s ease;
}

/* 高亮区域 */
.guide-highlight {
  position: fixed;
  z-index: 9999;
  border-radius: 12px;
  pointer-events: none;
  animation: highlight-pulse 2s ease-in-out infinite;
}

.highlight-border {
  position: absolute;
  inset: 0;
  border: 3px solid var(--primary-400);
  border-radius: 12px;
  box-shadow:
    0 0 0 4px rgba(34, 211, 238, 0.2),
    0 0 20px rgba(34, 211, 238, 0.3),
    inset 0 0 20px rgba(34, 211, 238, 0.1);
}

@keyframes highlight-pulse {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(34, 211, 238, 0.4);
  }
  50% {
    box-shadow: 0 0 0 10px rgba(34, 211, 238, 0);
  }
}

/* 引导弹窗 */
.guide-dialog {
  position: fixed;
  width: 420px;
  background: linear-gradient(145deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-xl);
  box-shadow:
    0 25px 50px -12px rgba(0, 0, 0, 0.5),
    0 0 0 1px rgba(255, 255, 255, 0.05);
  z-index: 10000;
  overflow: hidden;
  cursor: default;
  user-select: none;
}

/* 拖拽手柄 */
.guide-drag-handle {
  display: flex;
  justify-content: center;
  padding: 8px 0 4px;
  cursor: grab;
  background: linear-gradient(180deg, var(--bg-tertiary) 0%, transparent 100%);
}

.guide-drag-handle:active {
  cursor: grabbing;
}

.drag-dots {
  display: flex;
  gap: 4px;
}

.drag-dots span {
  width: 4px;
  height: 4px;
  background-color: var(--text-tertiary);
  border-radius: 50%;
  opacity: 0.5;
}

/* 步骤指示器 */
.guide-step-indicator {
  display: flex;
  justify-content: center;
  gap: 8px;
  padding: 12px 24px 8px;
}

.step-dot {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  background-color: var(--bg-tertiary);
  color: var(--text-tertiary);
  border: 2px solid var(--border-light);
  cursor: pointer;
  transition: all 0.3s ease;
}

.step-dot.active {
  background-color: var(--primary-500);
  color: white;
  border-color: var(--primary-500);
  transform: scale(1.1);
}

.step-dot.completed {
  background-color: var(--success-500);
  color: white;
  border-color: var(--success-500);
}

.step-check {
  font-size: 14px;
}

/* 内容区域 */
.guide-content {
  padding: 16px 24px;
  text-align: center;
}

.guide-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 12px;
  line-height: 1.4;
}

.guide-text {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
}

/* 按钮区域 */
.guide-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px 16px;
  gap: 12px;
}

.guide-actions-spacer {
  flex: 1;
}

.guide-btn-prev,
.guide-btn-next,
.guide-btn-finish {
  display: flex;
  align-items: center;
  gap: 6px;
}

/* 底部工具栏 */
.guide-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 24px;
  background-color: var(--bg-tertiary);
  border-top: 1px solid var(--border-light);
}

.opacity-control {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-tertiary);
}

.opacity-slider {
  width: 80px;
}

.skip-btn {
  color: var(--text-tertiary);
  font-size: 12px;
}

.skip-btn:hover {
  color: var(--text-secondary);
}

/* 左侧重新打开按钮 */
.guide-reopen-btn {
  position: fixed;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  z-index: 100;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px 12px 12px;
  background: linear-gradient(135deg, var(--primary-600) 0%, var(--primary-700) 100%);
  color: white;
  border-radius: 0 var(--radius-lg) var(--radius-lg) 0;
  cursor: pointer;
  box-shadow: 4px 0 16px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  writing-mode: horizontal-tb;
}

.guide-reopen-btn:hover {
  padding-left: 16px;
  box-shadow: 4px 0 24px rgba(34, 211, 238, 0.3);
}

.reopen-text {
  font-size: 13px;
  font-weight: 500;
  white-space: nowrap;
}

/* 欢迎弹窗 */
.welcome-content {
  text-align: center;
  padding: 20px 0;
}

.welcome-icon {
  margin-bottom: 20px;
}

.welcome-text {
  font-size: 15px;
  color: var(--text-secondary);
  line-height: 1.8;
}

.welcome-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
}

/* 过渡动画 */
.guide-fade-enter-active,
.guide-fade-leave-active {
  transition: opacity 0.3s ease;
}

.guide-fade-enter-from,
.guide-fade-leave-to {
  opacity: 0;
}

.guide-btn-slide-enter-active,
.guide-btn-slide-leave-active {
  transition: all 0.3s ease;
}

.guide-btn-slide-enter-from,
.guide-btn-slide-leave-to {
  opacity: 0;
  transform: translateY(-50%) translateX(-100%);
}

/* 响应式 */
@media (max-width: 768px) {
  .guide-dialog {
    width: 90%;
    max-width: 360px;
  }
}
</style>

<style>
/* 全局样式 - 欢迎弹窗 */
.welcome-dialog .el-dialog__header {
  text-align: center;
  padding-bottom: 0;
}

.welcome-dialog .el-dialog__title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
}

.welcome-dialog .el-dialog__body {
  padding: 10px 20px 0;
}

.welcome-dialog .el-dialog__footer {
  padding: 16px 20px 20px;
}
</style>
