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

          <!-- 主体：左右布局 -->
          <div class="guide-body">
            <!-- 左侧：步骤进度指示器 -->
            <div class="guide-stepper">
              <div class="stepper-track">
                <div
                  v-for="(step, index) in totalSteps"
                  :key="index"
                  class="stepper-node-wrapper"
                >
                  <!-- 连接线 -->
                  <div
                    v-if="index > 0"
                    class="stepper-line"
                    :class="{ completed: index <= guideStore.currentStep }"
                  ></div>
                  <!-- 节点 -->
                  <div
                    class="stepper-node"
                    :class="{
                      active: index === guideStore.currentStep,
                      completed: index < guideStore.currentStep,
                      pending: index > guideStore.currentStep
                    }"
                    @click="guideStore.goToStep(index)"
                  >
                    <transition name="step-icon" mode="out-in">
                      <svg
                        v-if="index < guideStore.currentStep"
                        key="check"
                        class="step-icon-check"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="3"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      >
                        <polyline points="20 6 9 17 4 12" />
                      </svg>
                      <span v-else key="num" class="step-number">{{ index + 1 }}</span>
                    </transition>
                  </div>
                </div>
              </div>
            </div>

            <!-- 右侧：内容区域 -->
            <div class="guide-content-wrapper">
              <!-- 步骤计数器 -->
              <div class="step-counter">
                {{ guideStore.currentStep + 1 }} / {{ totalSteps }}
              </div>

              <!-- 内容区域（带过渡动画） -->
              <transition name="content-fade" mode="out-in">
                <div class="guide-content" :key="guideStore.currentStep">
                  <h3 class="guide-title">{{ currentStepData.title }}</h3>
                  <p class="guide-text">{{ currentStepData.content }}</p>
                  <!-- 提示信息区域 -->
                  <div v-if="currentStepData.tip" class="guide-tip">
                    <svg class="tip-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <circle cx="12" cy="12" r="10" />
                      <line x1="12" y1="16" x2="12" y2="12" />
                      <line x1="12" y1="8" x2="12.01" y2="8" />
                    </svg>
                    <span>{{ currentStepData.tip }}</span>
                  </div>
                </div>
              </transition>
            </div>
          </div>

          <!-- 分隔线 + 按钮区域 -->
          <div class="guide-footer">
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
                type="primary"
                class="guide-btn-finish"
                @click="finishGuide"
              >
                <el-icon><CircleCheck /></el-icon>
                完成
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
                跳过引导
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- 左侧重新打开按钮 -->
    <transition name="guide-btn-slide">
      <div
        v-if="showReopenButton"
        class="guide-reopen-btn"
        :class="{ 'is-hovered': btnHovered }"
        :style="{ top: btnPos.top + 'px' }"
        @mouseenter="btnHovered = true"
        @mouseleave="btnHovered = false"
        @mousedown="startBtnDrag"
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
      title="欢迎使用火花智创"
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
import { useRouter } from 'vue-router'
import { useGuideStore } from '@/stores/guide'
import { useUserStore } from '@/stores/user'
import { ArrowLeft, ArrowRight, CircleCheck, Guide, Compass, Sunny, Moon } from '@element-plus/icons-vue'

const router = useRouter()
const guideStore = useGuideStore()
const userStore = useUserStore()

const guideDialogRef = ref(null)
const showWelcomeDialog = ref(false)
const showReopenButton = ref(false)
const highlightRect = ref(null)
const btnHovered = ref(false)
const btnPos = ref({ top: window.innerHeight / 2 - 40 })
const btnDragging = ref(false)
const btnDragStartY = ref(0)
const btnDragStartTop = ref(0)

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
    const dialogWidth = 820
    const dialogHeight = 400
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
  const stepData = currentStepData.value

  if (stepData.routePath && router.currentRoute.value.path !== stepData.routePath) {
    await router.push(stepData.routePath)
    await nextTick()
    await new Promise(r => setTimeout(r, 500))
  }

  await nextTick()
  const target = stepData.target
  if (target) {
    const el = document.querySelector(target)
    if (el) {
      highlightRect.value = el.getBoundingClientRect()
      el.scrollIntoView({ behavior: 'smooth', block: 'center' })
    } else {
      highlightRect.value = null
    }
  } else {
    highlightRect.value = null
  }
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

// 引导按钮垂直拖拽
const startBtnDrag = (e) => {
  btnDragging.value = true
  btnDragStartY.value = e.clientY
  btnDragStartTop.value = btnPos.value.top
  document.addEventListener('mousemove', onBtnDrag)
  document.addEventListener('mouseup', stopBtnDrag)
}

const onBtnDrag = (e) => {
  if (!btnDragging.value) return
  const dy = e.clientY - btnDragStartY.value
  const newTop = Math.max(60, Math.min(window.innerHeight - 60, btnDragStartTop.value + dy))
  btnPos.value.top = newTop
}

const stopBtnDrag = () => {
  btnDragging.value = false
  document.removeEventListener('mousemove', onBtnDrag)
  document.removeEventListener('mouseup', stopBtnDragFn)
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
/* ==================== 遮罩层 ==================== */
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

/* ==================== 高亮区域 ==================== */
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

/* ==================== 引导弹窗 ==================== */
.guide-dialog {
  position: fixed;
  width: 820px;
  max-height: 80vh;
  background: rgba(15, 23, 42, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(34, 211, 238, 0.25);
  border-radius: 16px;
  box-shadow:
    0 25px 60px -12px rgba(0, 0, 0, 0.6),
    0 0 0 1px rgba(255, 255, 255, 0.06),
    0 0 40px rgba(34, 211, 238, 0.08);
  z-index: 10000;
  overflow: hidden;
  cursor: default;
  user-select: none;
  display: flex;
  flex-direction: column;
}

/* ==================== 拖拽手柄 ==================== */
.guide-drag-handle {
  display: flex;
  justify-content: center;
  padding: 10px 0 6px;
  cursor: grab;
  flex-shrink: 0;
}

.guide-drag-handle:active {
  cursor: grabbing;
}

.drag-dots {
  display: flex;
  gap: 5px;
}

.drag-dots span {
  width: 5px;
  height: 5px;
  background-color: rgba(255, 255, 255, 0.25);
  border-radius: 50%;
}

/* ==================== 主体左右布局 ==================== */
.guide-body {
  display: flex;
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

/* ==================== 左侧步骤进度指示器 ==================== */
.guide-stepper {
  display: flex;
  align-items: stretch;
  padding: 24px 20px 24px 28px;
  flex-shrink: 0;
  border-right: 1px solid rgba(255, 255, 255, 0.06);
}

.stepper-track {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0;
}

.stepper-node-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 连接线 */
.stepper-line {
  width: 2px;
  height: 20px;
  background: rgba(255, 255, 255, 0.1);
  transition: background 0.4s ease;
}

.stepper-line.completed {
  background: linear-gradient(180deg, var(--primary-500), var(--primary-400));
}

/* 节点 */
.stepper-node {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.06);
  color: rgba(255, 255, 255, 0.3);
  border: 2px solid rgba(255, 255, 255, 0.1);
  cursor: pointer;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  flex-shrink: 0;
}

.stepper-node:hover {
  border-color: rgba(34, 211, 238, 0.4);
  background: rgba(34, 211, 238, 0.08);
}

.stepper-node.active {
  background: linear-gradient(135deg, var(--primary-500), var(--primary-400));
  color: #fff;
  border-color: transparent;
  transform: scale(1.15);
  box-shadow: 0 0 20px rgba(34, 211, 238, 0.35), 0 0 0 4px rgba(34, 211, 238, 0.12);
}

.stepper-node.completed {
  background: linear-gradient(135deg, #10b981, #34d399);
  color: #fff;
  border-color: transparent;
  box-shadow: 0 0 12px rgba(16, 185, 129, 0.25);
}

.stepper-node.pending {
  background: rgba(255, 255, 255, 0.04);
  color: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.08);
}

.step-number {
  font-size: 13px;
  font-weight: 700;
  line-height: 1;
}

.step-icon-check {
  width: 18px;
  height: 18px;
  color: #fff;
}

/* 步骤图标过渡 */
.step-icon-enter-active,
.step-icon-leave-active {
  transition: all 0.25s ease;
}

.step-icon-enter-from {
  opacity: 0;
  transform: scale(0.5);
}

.step-icon-leave-to {
  opacity: 0;
  transform: scale(1.5);
}

/* ==================== 右侧内容区域 ==================== */
.guide-content-wrapper {
  flex: 1;
  padding: 28px 32px 24px;
  display: flex;
  flex-direction: column;
  min-width: 0;
  overflow-y: auto;
}

/* 步骤计数器 */
.step-counter {
  font-size: 13px;
  font-weight: 500;
  color: var(--primary-400);
  letter-spacing: 1px;
  margin-bottom: 16px;
  font-variant-numeric: tabular-nums;
}

/* 内容区域 */
.guide-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.guide-title {
  font-size: 20px;
  font-weight: 700;
  color: #f1f5f9;
  margin-bottom: 16px;
  line-height: 1.4;
  letter-spacing: -0.01em;
}

.guide-text {
  font-size: 15px;
  color: rgba(203, 213, 225, 0.9);
  line-height: 1.7;
  margin: 0 0 20px;
}

/* 提示信息区域 */
.guide-tip {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 14px 16px;
  background: linear-gradient(135deg, rgba(34, 211, 238, 0.08), rgba(34, 211, 238, 0.04));
  border: 1px solid rgba(34, 211, 238, 0.15);
  border-radius: 10px;
  font-size: 13px;
  color: rgba(34, 211, 238, 0.85);
  line-height: 1.6;
}

.tip-icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  margin-top: 1px;
  opacity: 0.7;
}

/* 内容切换过渡动画 */
.content-fade-enter-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.content-fade-leave-active {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.content-fade-enter-from {
  opacity: 0;
  transform: translateX(16px);
}

.content-fade-leave-to {
  opacity: 0;
  transform: translateX(-16px);
}

/* ==================== 底部区域 ==================== */
.guide-footer {
  flex-shrink: 0;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

/* 按钮区域 */
.guide-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 32px;
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
  border-radius: 8px;
  font-weight: 500;
}

.guide-btn-prev {
  color: rgba(203, 213, 225, 0.8);
}

.guide-btn-next,
.guide-btn-finish {
  min-width: 100px;
}

/* 底部工具栏 */
.guide-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 32px 14px;
  background: rgba(0, 0, 0, 0.15);
}

.opacity-control {
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(148, 163, 184, 0.7);
}

.opacity-slider {
  width: 80px;
}

.skip-btn {
  color: rgba(148, 163, 184, 0.6);
  font-size: 13px;
}

.skip-btn:hover {
  color: rgba(203, 213, 225, 0.9);
}

/* ==================== 左侧重新打开按钮 ==================== */
.guide-reopen-btn {
  position: fixed;
  left: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 10px 12px 10px;
  background: linear-gradient(135deg, var(--primary-600) 0%, var(--primary-700) 100%);
  color: white;
  border-radius: 0 var(--radius-lg) var(--radius-lg) 0;
  cursor: pointer;
  box-shadow: 4px 0 16px rgba(0, 0, 0, 0.2);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  writing-mode: horizontal-tb;
  overflow: hidden;
  width: 44px;
}

.guide-reopen-btn.is-hovered {
  padding-left: 16px;
  width: auto;
  box-shadow: 4px 0 24px rgba(34, 211, 238, 0.35);
}

.guide-reopen-btn:hover {
  padding-left: 16px;
  width: auto;
  box-shadow: 4px 0 24px rgba(34, 211, 238, 0.35);
}

.reopen-text {
  font-size: 13px;
  font-weight: 500;
  white-space: nowrap;
  opacity: 0;
  transform: translateX(-8px);
  transition: all 0.25s ease;
  max-width: 0;
  overflow: hidden;
}

.guide-reopen-btn.is-hovered .reopen-text,
.guide-reopen-btn:hover .reopen-text {
  opacity: 1;
  transform: translateX(0);
  max-width: 80px;
}

/* ==================== 欢迎弹窗 ==================== */
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

/* ==================== 过渡动画 ==================== */
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

/* ==================== 响应式 ==================== */
@media (max-width: 900px) {
  .guide-dialog {
    width: 92vw;
    max-width: 600px;
  }

  .guide-body {
    flex-direction: column;
  }

  .guide-stepper {
    flex-direction: row;
    padding: 16px 24px;
    border-right: none;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    overflow-x: auto;
  }

  .stepper-track {
    flex-direction: row;
    gap: 0;
  }

  .stepper-node-wrapper {
    flex-direction: row;
  }

  .stepper-line {
    width: 20px;
    height: 2px;
  }

  .stepper-node.active {
    transform: scale(1.1);
  }

  .guide-content-wrapper {
    padding: 20px 24px 16px;
  }

  .guide-actions {
    padding: 14px 24px;
  }

  .guide-toolbar {
    padding: 10px 24px 12px;
  }
}

@media (max-width: 480px) {
  .guide-dialog {
    width: 96vw;
    max-width: none;
    border-radius: 12px;
  }

  .guide-stepper {
    padding: 12px 16px;
  }

  .stepper-node {
    width: 30px;
    height: 30px;
    font-size: 12px;
  }

  .stepper-line {
    width: 14px;
  }

  .guide-content-wrapper {
    padding: 16px;
  }

  .guide-title {
    font-size: 17px;
  }

  .guide-text {
    font-size: 14px;
  }

  .guide-actions {
    padding: 12px 16px;
  }

  .guide-toolbar {
    padding: 8px 16px 10px;
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
