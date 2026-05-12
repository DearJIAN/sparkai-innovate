<template>
  <div class="progress-page">
    <div class="progress-container">
      <div class="progress-card">
        <div class="progress-header">
          <h2 class="progress-title">{{ isPPT ? 'PPT表现力评估生成中' : '项目报告评估生成中' }}</h2>
          <p class="progress-subtitle">系统正在处理您的PDF内容，请耐心等待...</p>
        </div>

        <div class="progress-visual">
          <div class="scan-ring">
            <svg viewBox="0 0 120 120" class="scan-svg">
              <circle cx="60" cy="60" r="52" fill="none" stroke="#e2e8f0" stroke-width="3" />
              <circle
                cx="60" cy="60" r="52" fill="none" stroke="url(#scanGradient)"
                stroke-width="3" stroke-linecap="round"
                :stroke-dasharray="dashArray" :stroke-dashoffset="dashOffset"
                class="scan-circle"
              />
              <defs>
                <linearGradient id="scanGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stop-color="#2563eb" />
                  <stop offset="100%" stop-color="#7c3aed" />
                </linearGradient>
              </defs>
            </svg>
            <div class="scan-percent">{{ displayProgress }}%</div>
            <div class="scan-icon">
              <el-icon size="20"><MagicStick /></el-icon>
            </div>
          </div>
        </div>

        <div class="progress-status-text">{{ currentStatusText }}</div>

        <div class="progress-bar-wrap">
          <div class="progress-bar-bg">
            <div class="progress-bar-fill" :style="{ width: displayProgress + '%' }"></div>
          </div>
        </div>

        <div class="progress-stages">
          <div
            v-for="(stage, index) in stages"
            :key="index"
            class="stage-item"
            :class="{ active: index < completedStageIndex, current: index === completedStageIndex }"
          >
            <div class="stage-dot">
              <el-icon v-if="index < completedStageIndex" size="14"><Check /></el-icon>
              <span v-else-if="index === completedStageIndex" class="stage-spinner"></span>
              <span v-else class="stage-num">{{ index + 1 }}</span>
            </div>
            <span class="stage-label">{{ stage }}</span>
          </div>
        </div>

        <div class="progress-bottom">
          <transition name="btn-scale">
            <el-button
              v-if="analysisDone"
              type="primary"
              size="large"
              class="view-report-btn"
              @click="viewReport"
            >
              查看评分
              <el-icon><ArrowRight /></el-icon>
            </el-button>
          </transition>
          <p v-if="!analysisDone" class="wait-text">
            <span class="wait-dot-pulse"></span>
            AI正在深度分析您的材料
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { MagicStick, ArrowRight, Check } from '@element-plus/icons-vue'
import { getTaskStatus, startAnalysis, completeAnalysis } from '@/api/materialEvaluation'

const route = useRoute()
const router = useRouter()

const taskId = computed(() => route.params.taskId)
const isPPT = ref(false)

const displayProgress = ref(0)
const analysisDone = ref(false)
const currentStatusText = ref('正在分析材料结构...')

const PPT_STAGES = [
  'PDF格式校验',
  '页面结构识别',
  '路演逻辑分析',
  '视觉表达评估',
  '创新亮点提取',
  '答辩说服力判断',
  '评分报告生成'
]

const REPORT_STAGES = [
  'PDF格式校验',
  '文本内容提取',
  '项目结构识别',
  '市场与痛点分析',
  '创新价值评估',
  '风险与实施路径分析',
  '评分报告生成'
]

const stages = computed(() => isPPT.value ? PPT_STAGES : REPORT_STAGES)
const dashArray = computed(() => 2 * Math.PI * 52)
const dashOffset = computed(() => dashArray.value * (1 - displayProgress.value / 100))

const STATUS_TEXTS = [
  '正在分析材料结构...',
  '正在提取关键信息...',
  '正在评估内容质量...',
  '正在比对行业标准...',
  '正在生成评分报告...'
]

const completedStageIndex = computed(() => {
  const stageCount = stages.value.length
  return Math.min(Math.floor(displayProgress.value / 100 * stageCount), stageCount)
})

let progressTimer = null
let textTimer = null
let analysisTimer = null

function startProgressAnimation() {
  const baseInterval = 120
  const totalSteps = 100
  let step = 0

  progressTimer = setInterval(() => {
    if (step >= totalSteps) {
      clearInterval(progressTimer)
      progressTimer = null
      return
    }

    step++
    const progress = step / totalSteps
    const eased = 1 - Math.pow(1 - progress, 2.5)
    displayProgress.value = Math.round(eased * 98)

    if (displayProgress.value >= 95) {
      displayProgress.value = 95
      clearInterval(progressTimer)
      progressTimer = null
    }
  }, baseInterval + Math.random() * 60)
}

function startTextRotation() {
  let index = 0
  textTimer = setInterval(() => {
    index = (index + 1) % STATUS_TEXTS.length
    currentStatusText.value = STATUS_TEXTS[index]
  }, 2000)
}

async function initAnalysis() {
  try {
    const taskRes = await getTaskStatus(taskId.value)
    if (taskRes.code !== 200 || !taskRes.data) {
      ElMessage.error('无法获取任务信息')
      return
    }

    isPPT.value = taskRes.data.evaluation_type === 'ppt'

    if (taskRes.data.status === 'completed') {
      displayProgress.value = 100
      currentStatusText.value = '分析已完成'
      analysisDone.value = true
      return
    }

    await startAnalysis(taskId.value)

    startProgressAnimation()
    startTextRotation()

    const fullDuration = 8000 + Math.random() * 4000

    analysisTimer = setTimeout(async () => {
      try {
        const completed = displayProgress.value
        const fillSteps = (100 - completed) / 5
        let fillStep = 0
        const fillTimer = setInterval(() => {
          fillStep++
          displayProgress.value = Math.min(100, completed + fillStep * (100 - completed) / 5)
          if (fillStep >= 5) {
            clearInterval(fillTimer)
          }
        }, 200)

        if (progressTimer) clearInterval(progressTimer)
        if (textTimer) clearInterval(textTimer)

        const res = await completeAnalysis(taskId.value)
        if (res.code === 200 && res.data) {
          displayProgress.value = 100
          currentStatusText.value = '分析已完成，请查看评分报告'
          analysisDone.value = true
        } else {
          currentStatusText.value = '分析出现问题，请重试'
          ElMessage.error('评估生成失败，请重试')
        }
      } catch (e) {
        currentStatusText.value = '分析出现问题，请重试'
        ElMessage.error('评估失败，请稍后重试')
      }
    }, fullDuration)
  } catch (e) {
    ElMessage.error('启动评估失败，请重试')
  }
}

function viewReport() {
  router.push(`/ai-material-evaluation/report/${taskId.value}`)
}

onMounted(() => {
  initAnalysis()
})

onBeforeUnmount(() => {
  if (progressTimer) clearInterval(progressTimer)
  if (textTimer) clearInterval(textTimer)
  if (analysisTimer) clearTimeout(analysisTimer)
})
</script>

<style scoped>
.progress-page {
  min-height: 100vh;
  background: #f5f8ff;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 24px;
}

.progress-container {
  width: 100%;
  max-width: 520px;
}

.progress-card {
  background: #fff;
  border-radius: 24px;
  padding: 48px 40px;
  box-shadow: 0 8px 40px rgba(37,99,235,0.08);
  border: 1px solid #e8ecf4;
  text-align: center;
}

.progress-header {
  margin-bottom: 36px;
}

.progress-title {
  font-size: 22px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 8px;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.progress-subtitle {
  font-size: 14px;
  color: #64748b;
  margin: 0;
}

.progress-visual {
  margin-bottom: 28px;
  display: flex;
  justify-content: center;
}

.scan-ring {
  position: relative;
  width: 140px;
  height: 140px;
}

.scan-svg {
  width: 100%;
  height: 100%;
}

.scan-circle {
  transform-origin: center;
  animation: scanRotate 2s linear infinite;
}

@keyframes scanRotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.scan-percent {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 28px;
  font-weight: 800;
  color: #1e293b;
}

.scan-icon {
  position: absolute;
  bottom: 6px;
  right: 6px;
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  animation: iconPulse 1.5s ease-in-out infinite;
}

@keyframes iconPulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(37,99,235,0.4); }
  50% { box-shadow: 0 0 0 8px rgba(37,99,235,0); }
}

.progress-status-text {
  font-size: 15px;
  color: #475569;
  margin-bottom: 20px;
  min-height: 22px;
  font-weight: 500;
}

.progress-bar-wrap {
  margin-bottom: 28px;
}

.progress-bar-bg {
  height: 6px;
  background: #e2e8f0;
  border-radius: 3px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #2563eb, #7c3aed);
  border-radius: 3px;
  transition: width 0.3s ease;
}

.progress-stages {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 32px;
  text-align: left;
  padding: 0 8px;
}

.stage-item {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 13px;
  color: #94a3b8;
  transition: all 0.3s;
}

.stage-item.active {
  color: #10b981;
}

.stage-item.current {
  color: #3b82f6;
  font-weight: 600;
}

.stage-dot {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background: #f1f5f9;
  border: 2px solid #e2e8f0;
  color: #94a3b8;
  font-size: 12px;
  font-weight: 600;
  transition: all 0.3s;
}

.stage-item.active .stage-dot {
  background: #ecfdf5;
  border-color: #10b981;
  color: #10b981;
}

.stage-item.current .stage-dot {
  background: #eff6ff;
  border-color: #3b82f6;
  color: #3b82f6;
}

.stage-spinner {
  width: 12px;
  height: 12px;
  border: 2px solid #e2e8f0;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.stage-num {
  font-size: 11px;
  font-weight: 700;
}

.stage-label {
  font-size: 13px;
}

.progress-bottom {
  min-height: 46px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.view-report-btn {
  border-radius: 14px;
  font-size: 16px;
  font-weight: 600;
  height: 46px;
  padding: 0 32px;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  border: none;
  display: flex;
  align-items: center;
  gap: 8px;
  position: relative;
  overflow: hidden;
}

.view-report-btn::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(45deg, transparent 40%, rgba(255,255,255,0.15) 50%, transparent 60%);
  animation: shimmer 2s ease-in-out infinite;
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.view-report-btn:hover {
  background: linear-gradient(135deg, #1d4ed8, #6d28d9);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(37,99,235,0.3);
}

.btn-scale-enter-active {
  animation: btnPop 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes btnPop {
  from { transform: scale(0.8); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.wait-text {
  font-size: 14px;
  color: #64748b;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.wait-dot-pulse {
  width: 8px;
  height: 8px;
  background: #3b82f6;
  border-radius: 50%;
  animation: dotPulse 1.2s ease-in-out infinite;
}

@keyframes dotPulse {
  0%, 100% { opacity: 0.3; transform: scale(0.8); }
  50% { opacity: 1; transform: scale(1.2); }
}

@media (max-width: 768px) {
  .progress-card {
    padding: 32px 24px;
  }

  .progress-title { font-size: 18px; }
}
</style>