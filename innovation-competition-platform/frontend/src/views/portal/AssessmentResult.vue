<template>
  <div class="result-page">
    <div v-if="!result" class="result-empty">
      <el-icon size="64"><Warning /></el-icon>
      <p>暂无测评结果</p>
      <span>请先完成测评后再查看分析报告</span>
      <el-button type="primary" size="large" @click="router.push(`/assessment/${route.params.id}`)">开始测评</el-button>
      <el-button size="large" @click="router.push('/assessment')">返回测评中心</el-button>
    </div>

    <template v-else>
      <div class="result-hero">
        <div class="hero-bg"></div>
        <div class="hero-inner">
          <h1 class="hero-title">测评结果</h1>
          <p class="hero-subtitle">{{ result.title }}</p>
        </div>
      </div>

      <div class="result-body">
        <div class="result-card score-card">
          <div class="score-top">
            <h3 class="section-title">综合评分</h3>
            <span class="level-tag" :class="levelClass">{{ result.levelText }}</span>
          </div>
          <div class="score-main">
            <div class="score-ring">
              <svg viewBox="0 0 120 120" class="ring-svg">
                <circle cx="60" cy="60" r="52" fill="none" stroke="#f1f5f9" stroke-width="8" />
                <circle cx="60" cy="60" r="52" fill="none" stroke="url(#grad)" stroke-width="8" stroke-linecap="round" :stroke-dasharray="circ" :stroke-dashoffset="offset" transform="rotate(-90 60 60)" class="ring-progress" />
                <defs><linearGradient id="grad" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#2563eb" /><stop offset="100%" stop-color="#06b6d4" /></linearGradient></defs>
              </svg>
              <div class="ring-center">
                <span class="ring-number">{{ animatedScore }}</span>
                <span class="ring-label">分</span>
              </div>
            </div>
            <div class="score-meta">
              <div class="meta-row"><span class="meta-lbl">总分</span><span class="meta-val"><strong>{{ result.totalScore }}</strong> / {{ result.maxScore }}</span></div>
              <div class="meta-row"><span class="meta-lbl">得分率</span><span class="meta-val highlight">{{ result.scoreRate }}%</span></div>
              <div class="meta-row"><span class="meta-lbl">完成率</span><span class="meta-val highlight">{{ result.completedRate }}%</span></div>
              <div class="meta-row"><span class="meta-lbl">等级</span><span class="meta-val level-label" :class="levelClass">{{ result.levelText }}</span></div>
            </div>
          </div>
        </div>

        <div class="result-card" v-if="result.summary">
          <h3 class="section-title">综合评价</h3>
          <p class="summary-text">{{ result.summary }}</p>
          <p class="level-desc">{{ result.levelDesc }}</p>
        </div>

        <div class="result-card" v-if="result.suggestions && result.suggestions.length > 0">
          <h3 class="section-title">改进建议</h3>
          <ul class="suggestions">
            <li v-for="(tip, i) in result.suggestions" :key="i" class="sugg-item">
              <span class="sugg-num">{{ i + 1 }}</span>
              <span>{{ tip }}</span>
            </li>
          </ul>
        </div>

        <div class="result-card" v-if="result.dimensions && result.dimensions.length > 0">
          <h3 class="section-title">维度分析</h3>
          <div class="dim-list">
            <div v-for="dim in result.dimensions" :key="dim.name" class="dim-item">
              <div class="dim-header">
                <span class="dim-name">{{ dim.name }}</span>
                <span class="dim-score">{{ dim.score }}/{{ dim.maxScore }}（{{ dim.percent }}%）</span>
              </div>
              <div class="dim-bar">
                <div class="dim-fill" :style="{ width: dim.percent + '%' }" :class="dimClass(dim.percent)"></div>
              </div>
            </div>
          </div>
        </div>

        <div class="result-actions">
          <el-button type="primary" size="large" @click="retake">
            <el-icon><RefreshRight /></el-icon>
            重新测评
          </el-button>
          <el-button size="large" @click="router.push('/assessment')">返回测评中心</el-button>
          <el-button size="large" @click="router.push('/portal')">返回首页</el-button>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Warning, RefreshRight } from '@element-plus/icons-vue'
import { getResult, clearResult } from '@/utils/assessmentScoring'

const route = useRoute()
const router = useRouter()
const result = ref(null)
const animatedScore = ref(0)
const circ = 2 * Math.PI * 52

const offset = computed(() => {
  if (!result.value) return circ
  const pct = Math.min(result.value.scoreRate, 100) / 100
  return circ * (1 - pct)
})

const levelClass = computed(() => {
  if (!result.value) return ''
  const map = { excellent: 'level-excellent', good: 'level-good', medium: 'level-medium', improve: 'level-improve' }
  return map[result.value.level] || 'level-improve'
})

function dimClass(p) {
  if (p >= 75) return 'dim-high'
  if (p >= 50) return 'dim-mid'
  return 'dim-low'
}

function retake() {
  if (result.value) clearResult(result.value.assessmentId)
  router.push(`/assessment/${route.params.id}`)
}

onMounted(() => {
  const data = getResult(route.params.id)
  result.value = data
  if (data) {
    const target = data.totalScore
    const step = Math.max(1, Math.ceil(target / 30))
    const t = setInterval(() => {
      if (animatedScore.value >= target) { animatedScore.value = target; clearInterval(t) }
      else animatedScore.value = Math.min(animatedScore.value + step, target)
    }, 30)
  }
})
</script>

<style scoped>
.result-page { min-height: 100vh; background: linear-gradient(180deg, #eff6ff 0%, #f8fafc 100%); }

.result-empty { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 60vh; color: #94a3b8; gap: 12px; }
.result-empty p { font-size: 16px; color: #64748b; margin: 0; font-weight: 500; }
.result-empty span { font-size: 13px; margin-bottom: 16px; }

.result-hero { position: relative; background: linear-gradient(135deg, #1e40af, #2563eb, #06b6d4); padding: 36px 40px; overflow: hidden; }
.hero-bg { position: absolute; inset: 0; background: radial-gradient(circle at 20% 50%, rgba(14,165,233,0.12) 0%, transparent 50%), radial-gradient(circle at 80% 30%, rgba(139,92,246,0.08) 0%, transparent 50%); }
.hero-inner { position: relative; z-index: 2; max-width: 860px; margin: 0 auto; }
.hero-title { font-size: 26px; font-weight: 700; color: #ffffff; margin-bottom: 4px; }
.hero-subtitle { font-size: 14px; color: #93c5fd; }

.result-body { max-width: 860px; margin: 0 auto; padding: 28px 40px 48px; }

.result-card { background: #ffffff; border-radius: 16px; padding: 28px; margin-bottom: 20px; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(15,23,42,0.04); animation: fadeUp 0.5s ease; }
@keyframes fadeUp { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: translateY(0); } }

.section-title { font-size: 16px; font-weight: 600; color: #1e293b; margin: 0 0 16px 0; }
.score-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.score-top .section-title { margin: 0; }

.level-tag { font-size: 13px; font-weight: 600; padding: 5px 14px; border-radius: 20px; }
.level-excellent { background: #d1fae5; color: #059669; }
.level-good { background: #dbeafe; color: #2563eb; }
.level-medium { background: #fef3c7; color: #d97706; }
.level-improve { background: #fff7ed; color: #ea580c; }

.score-main { display: flex; gap: 40px; align-items: center; }
.score-ring { position: relative; flex-shrink: 0; }
.ring-svg { width: 120px; height: 120px; }
.ring-progress { transition: stroke-dashoffset 1.2s cubic-bezier(0.4, 0, 0.2, 1); }
.ring-center { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.ring-number { font-size: 28px; font-weight: 700; color: #1e293b; line-height: 1; }
.ring-label { font-size: 12px; color: #64748b; }

.score-meta { flex: 1; display: flex; flex-direction: column; gap: 8px; }
.meta-row { display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #f8fafc; }
.meta-row:last-child { border-bottom: none; }
.meta-lbl { font-size: 14px; color: #64748b; }
.meta-val { font-size: 14px; color: #1e293b; }
.meta-val strong { font-size: 16px; color: #2563eb; }
.meta-val.highlight { color: #2563eb; font-weight: 600; }
.level-label { font-weight: 600; }

.summary-text { font-size: 15px; color: #334155; line-height: 1.7; margin: 0; }
.level-desc { font-size: 13px; color: #64748b; margin: 12px 0 0; }

.suggestions { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 12px; }
.sugg-item { display: flex; gap: 10px; font-size: 14px; color: #334155; line-height: 1.7; }
.sugg-num { width: 22px; height: 22px; background: #eff6ff; color: #2563eb; font-size: 12px; font-weight: 600; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 2px; }

.dim-list { display: flex; flex-direction: column; gap: 16px; }
.dim-item { display: flex; flex-direction: column; gap: 8px; }
.dim-header { display: flex; justify-content: space-between; }
.dim-name { font-size: 14px; font-weight: 500; color: #334155; }
.dim-score { font-size: 12px; color: #64748b; }
.dim-bar { height: 8px; background: #f1f5f9; border-radius: 4px; overflow: hidden; }
.dim-fill { height: 100%; border-radius: 4px; transition: width 1s ease; }
.dim-high { background: linear-gradient(90deg, #10b981, #34d399); }
.dim-mid { background: linear-gradient(90deg, #2563eb, #3b82f6); }
.dim-low { background: linear-gradient(90deg, #f59e0b, #fbbf24); }

.result-actions { display: flex; gap: 12px; justify-content: center; padding: 8px 0 24px; flex-wrap: wrap; }

@media (max-width: 768px) {
  .result-hero { padding: 28px 20px; }
  .hero-title { font-size: 22px; }
  .result-body { padding: 20px 16px; }
  .score-main { flex-direction: column; align-items: center; gap: 20px; }
  .score-meta { width: 100%; }
  .result-actions { flex-direction: column; align-items: center; }
}
</style>