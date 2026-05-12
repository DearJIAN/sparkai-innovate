<template>
  <div class="detail-page">
    <div v-if="errorMsg" class="detail-empty">
      <el-icon size="64"><Warning /></el-icon>
      <p>{{ errorMsg }}</p>
      <el-button type="primary" @click="router.push('/assessment')">返回测评中心</el-button>
    </div>

    <template v-else-if="questionnaire">
      <header class="detail-header">
        <div class="header-left">
          <span class="header-logo" @click="router.push('/assessment')">在线测评</span>
          <span class="header-divider">|</span>
          <span class="header-name">{{ questionnaire.title }}</span>
        </div>
        <div class="header-progress">
          <span class="progress-text">{{ currentIndex + 1 }}/{{ questions.length }}</span>
          <div class="progress-bar-wrap">
            <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
          </div>
        </div>
        <div class="header-extra">
          <span class="header-badge" v-if="currentQuestion.dimension">{{ currentQuestion.dimension }}</span>
        </div>
      </header>

      <div class="detail-body">
        <div class="detail-main">
          <Transition name="slide-fade" mode="out-in">
            <div class="question-card" :key="currentIndex">
              <div class="q-number">第 {{ currentIndex + 1 }} 题</div>
              <p class="q-stem">{{ currentQuestion.stem }}</p>
              <div class="q-options">
                <div
                  v-for="opt in currentQuestion.options"
                  :key="opt.key"
                  class="q-option"
                  :class="{ selected: selectedKey === opt.key }"
                  @click="selectOption(opt)"
                >
                  <div class="q-radio">
                    <span class="q-key">{{ opt.key }}</span>
                  </div>
                  <span class="q-text">{{ opt.text }}</span>
                </div>
              </div>
              <div class="q-tip" v-if="highlightTip && !selectedKey">
                <el-icon><Warning /></el-icon>
                <span>请选择一个选项后继续</span>
              </div>
            </div>
          </Transition>

          <div class="q-actions">
            <el-button size="large" :disabled="currentIndex === 0" @click="prevQuestion">
              <el-icon><ArrowLeft /></el-icon>
              上一题
            </el-button>
            <el-button
              size="large"
              v-if="currentIndex < questions.length - 1"
              type="primary"
              @click="nextQuestion"
            >
              下一题
              <el-icon><ArrowRight /></el-icon>
            </el-button>
            <el-button
              size="large"
              v-else
              type="success"
              @click="handleSubmit"
            >
              <el-icon><Finished /></el-icon>
              提交测评
            </el-button>
            <el-button size="large" plain @click="handleBack">
              返回中心
            </el-button>
          </div>
        </div>

        <aside class="detail-side">
          <div class="side-card">
            <div class="side-title">答题进度</div>
            <div class="progress-stats">
              <div class="stat-row">
                <span class="stat-lbl">已答题</span>
                <span class="stat-val">{{ answeredCount }}/{{ questions.length }}</span>
              </div>
              <div class="stat-row">
                <span class="stat-lbl">完成率</span>
                <span class="stat-val highlight">{{ progressPercent }}%</span>
              </div>
            </div>
          </div>

          <div class="side-card">
            <div class="side-title">题号导航</div>
            <div class="nav-grid">
              <button
                v-for="(q, i) in questions"
                :key="q.id"
                class="nav-btn"
                :class="{
                  current: i === currentIndex,
                  done: answers[q.id]
                }"
                @click="goTo(i)"
              >{{ i + 1 }}</button>
            </div>
            <div class="nav-legend">
              <span><span class="dot current-dot"></span>当前题</span>
              <span><span class="dot done-dot"></span>已答</span>
              <span><span class="dot"></span>未答</span>
            </div>
          </div>
        </aside>
      </div>
    </template>

    <el-dialog v-model="submitVisible" title="确认提交" width="400px" :close-on-click-modal="false">
      <div class="dialog-body">
        <div v-if="!allAnswered" class="dialog-warn">
          <el-icon size="28" color="#f59e0b"><Warning /></el-icon>
          <p>还有 <strong>{{ questions.length - answeredCount }}</strong> 道题未作答，提交后将无法修改。</p>
        </div>
        <div v-else class="dialog-ok">
          <el-icon size="28" color="#10b981"><CircleCheck /></el-icon>
          <p>所有题目已作答，确认提交测评？</p>
        </div>
      </div>
      <template #footer>
        <el-button @click="submitVisible = false">继续答题</el-button>
        <el-button type="primary" @click="doSubmit" :loading="submitting">确认提交</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Warning, ArrowLeft, ArrowRight, Finished, CircleCheck } from '@element-plus/icons-vue'
import { getAssessmentById } from '@/data/assessmentBank'
import { getQuestionnaireById, validateQuestionnaire } from '@/data/assessmentQuestionnaires'
import { calculateScore, saveResult, clearResult, persistTempAnswers, getTempAnswers, clearTempAnswers } from '@/utils/assessmentScoring'

const route = useRoute()
const router = useRouter()

const questionnaire = ref(null)
const questions = ref([])
const currentIndex = ref(0)
const answers = ref({})
const errorMsg = ref('')
const submitting = ref(false)
const submitVisible = ref(false)
const highlightTip = ref(false)

const currentQuestion = computed(() => questions.value[currentIndex.value] || {})
const selectedKey = computed(() => {
  const q = currentQuestion.value
  if (!q || !q.options) return ''
  const entry = Object.entries(answers.value).find(([qid]) => qid === q.id)
  if (!entry) return ''
  const val = entry[1]
  const opt = q.options.find(o => o.score === val)
  return opt ? opt.key : ''
})
const answeredCount = computed(() => questions.value.filter(q => answers.value[q.id] != null).length)
const allAnswered = computed(() => answeredCount.value === questions.value.length)
const progressPercent = computed(() => {
  if (!questions.value.length) return 0
  return Math.round((answeredCount.value / questions.value.length) * 100)
})

function selectOption(opt) {
  if (submitting.value) return
  answers.value = { ...answers.value, [currentQuestion.value.id]: opt.score }
  highlightTip.value = false
  persistTempAnswers(questionnaire.value.id, answers.value)
}

function nextQuestion() {
  if (!answers.value[currentQuestion.value.id]) {
    highlightTip.value = true
    return
  }
  highlightTip.value = false
  if (currentIndex.value < questions.value.length - 1) {
    currentIndex.value++
  }
}

function prevQuestion() {
  highlightTip.value = false
  if (currentIndex.value > 0) {
    currentIndex.value--
  }
}

function goTo(idx) {
  highlightTip.value = false
  currentIndex.value = idx
}

function handleSubmit() {
  if (!allAnswered.value) {
    submitVisible.value = true
  } else {
    doSubmit()
  }
}

async function doSubmit() {
  submitVisible.value = false
  if (submitting.value) return
  submitting.value = true
  try {
    const result = calculateScore(questionnaire.value, answers.value)
    saveResult(questionnaire.value.id, result)
    clearTempAnswers(questionnaire.value.id)
    ElMessage.success('测评提交成功！')
    router.push(`/assessment/${questionnaire.value.id}/result`)
  } catch {
    ElMessage.error('提交失败，请重试')
  } finally {
    submitting.value = false
  }
}

function handleBack() {
  if (answeredCount.value > 0) {
    persistTempAnswers(questionnaire.value.id, answers.value)
  }
  router.push('/assessment')
}

onMounted(() => {
  const id = route.params.id
  const card = getAssessmentById(id)
  if (!card) {
    errorMsg.value = '测评不存在或 ID 无效'
    return
  }
  if (!card.real) {
    router.replace(`/assessment/${id}/coming-soon`)
    return
  }
  const qn = getQuestionnaireById(id)
  if (!qn || !validateQuestionnaire(qn)) {
    errorMsg.value = '问卷配置异常，请联系管理员检查题库。'
    return
  }
  questionnaire.value = qn
  questions.value = qn.questions
  clearResult(id)
  const saved = getTempAnswers(id)
  if (saved && Object.keys(saved).length > 0) {
    answers.value = saved
  }
})
</script>

<style scoped>
.detail-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
}

.detail-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  color: #94a3b8;
  gap: 16px;
}
.detail-empty p { font-size: 16px; color: #64748b; margin: 0; }

.detail-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  padding: 12px 32px;
  position: sticky;
  top: 0;
  z-index: 40;
  box-shadow: 0 1px 3px rgba(15,23,42,0.04);
}

.header-left { display: flex; align-items: center; gap: 10px; }
.header-logo { font-size: 15px; font-weight: 600; color: #2563eb; cursor: pointer; }
.header-logo:hover { color: #1d4ed8; }
.header-divider { color: #cbd5e1; }
.header-name { font-size: 15px; font-weight: 500; color: #475569; }

.header-progress { display: flex; align-items: center; gap: 10px; min-width: 160px; }
.progress-text { font-size: 14px; font-weight: 600; color: #334155; min-width: 40px; }
.progress-bar-wrap { width: 120px; height: 6px; background: #f1f5f9; border-radius: 3px; overflow: hidden; }
.progress-fill { height: 100%; background: linear-gradient(90deg, #2563eb, #3b82f6); border-radius: 3px; transition: width 0.35s ease; }

.header-extra { display: flex; align-items: center; gap: 8px; }
.header-badge { font-size: 12px; font-weight: 500; padding: 3px 10px; background: #eff6ff; color: #2563eb; border-radius: 6px; }

.detail-body { max-width: 1000px; margin: 0 auto; padding: 24px 32px 40px; display: flex; gap: 24px; align-items: flex-start; }
.detail-main { flex: 1; min-width: 0; }

.question-card { background: #ffffff; border-radius: 16px; padding: 32px; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(15,23,42,0.04); }

.q-number { display: inline-block; font-size: 12px; font-weight: 600; padding: 4px 12px; background: #eff6ff; color: #2563eb; border-radius: 6px; margin-bottom: 16px; }
.q-stem { font-size: 18px; font-weight: 500; color: #1e293b; line-height: 1.7; margin-bottom: 28px; }

.q-options { display: flex; flex-direction: column; gap: 12px; }

.q-option {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.q-option:hover { border-color: #93c5fd; background: #f8faff; transform: scale(1.01); }
.q-option:active { transform: scale(0.99); }
.q-option.selected { border-color: #2563eb; background: #eff6ff; transform: translateX(6px); }

.q-radio {
  width: 36px; height: 36px;
  border-radius: 50%;
  border: 2px solid #cbd5e1;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
  transition: all 0.2s ease;
}
.q-option.selected .q-radio { border-color: #2563eb; background: #2563eb; }
.q-option.selected .q-key { color: #ffffff; }

.q-key { font-size: 14px; font-weight: 700; color: #64748b; transition: color 0.2s; }
.q-text { font-size: 15px; color: #475569; line-height: 1.5; flex: 1; }
.q-option.selected .q-text { color: #1e293b; font-weight: 500; }

.q-tip { display: flex; align-items: center; gap: 6px; margin-top: 16px; font-size: 13px; color: #f59e0b; animation: fadeIn 0.2s ease; }

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

.q-actions { display: flex; align-items: center; justify-content: space-between; margin-top: 24px; gap: 12px; }

.detail-side { width: 240px; flex-shrink: 0; position: sticky; top: 72px; }

.side-card { background: #ffffff; border-radius: 12px; padding: 20px; border: 1px solid #e2e8f0; margin-bottom: 16px; box-shadow: 0 1px 3px rgba(15,23,42,0.04); }
.side-title { font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 14px; padding-bottom: 10px; border-bottom: 1px solid #f1f5f9; }

.progress-stats { display: flex; flex-direction: column; gap: 10px; }
.stat-row { display: flex; justify-content: space-between; font-size: 13px; }
.stat-lbl { color: #94a3b8; }
.stat-val { color: #1e293b; font-weight: 500; }
.stat-val.highlight { color: #2563eb; }

.nav-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px; }
.nav-btn {
  aspect-ratio: 1;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  background: #ffffff;
  font-size: 13px; font-weight: 500;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex; align-items: center; justify-content: center;
  padding: 0;
}
.nav-btn:hover { border-color: #93c5fd; }
.nav-btn.current { border-color: #2563eb; color: #2563eb; background: #eff6ff; font-weight: 700; }
.nav-btn.done { background: #dbeafe; border-color: #93c5fd; color: #2563eb; }
.nav-btn.current.done { background: #eff6ff; border-color: #2563eb; }

.nav-legend { display: flex; gap: 14px; margin-top: 12px; font-size: 12px; color: #94a3b8; }
.nav-legend span { display: flex; align-items: center; gap: 4px; }
.dot { width: 10px; height: 10px; border-radius: 3px; border: 1px solid #e2e8f0; background: #ffffff; }
.current-dot { border-color: #2563eb; background: #eff6ff; }
.done-dot { border-color: #93c5fd; background: #dbeafe; }

.dialog-body { text-align: center; padding: 16px 0; }
.dialog-body p { margin: 12px 0; font-size: 15px; color: #475569; }
.dialog-body strong { color: #ef4444; }

/* transition */
.slide-fade-enter-active { transition: all 0.23s cubic-bezier(0.4, 0, 0.2, 1); }
.slide-fade-leave-active { transition: all 0.18s cubic-bezier(0.4, 0, 0.2, 1); }
.slide-fade-enter-from { opacity: 0; transform: translateX(30px); }
.slide-fade-leave-to { opacity: 0; transform: translateX(-20px); }

@media (max-width: 1024px) {
  .detail-body { flex-direction: column; padding: 16px; }
  .detail-side { width: 100%; position: static; display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  .side-card { margin-bottom: 0; }
}

@media (max-width: 768px) {
  .detail-header { padding: 12px 16px; flex-wrap: wrap; gap: 8px; }
  .question-card { padding: 20px; }
  .q-stem { font-size: 16px; }
  .q-option { padding: 12px 16px; }
  .q-text { font-size: 14px; }
  .q-actions { flex-wrap: wrap; }
  .detail-side { grid-template-columns: 1fr; }
}
</style>