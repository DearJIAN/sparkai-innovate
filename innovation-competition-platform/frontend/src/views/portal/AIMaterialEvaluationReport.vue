<template>
  <div class="report-page" v-if="reportData">
    <div class="report-hero" :class="{ visible: phaseCount >= 0 }">
      <div class="report-hero-bg"></div>
      <div class="report-hero-content">
        <h1 class="report-hero-title">{{ isPPT ? '路演PPT评估报告' : '项目报告评估报告' }}</h1>
        <p class="report-hero-subtitle">数据驱动 · 智能分析 · 精准优化</p>
        <el-button class="download-btn-top" @click="downloadPDF" :loading="downloadingPDF" :disabled="downloadingPDF">
          <el-icon><Download /></el-icon>
          下载PDF
        </el-button>
      </div>
    </div>

    <div class="report-body">
      <div class="report-section from-top" :class="{ visible: phaseCount >= 1 }">
        <div class="score-card">
          <div class="score-left">
            <div class="score-ring">
              <svg viewBox="0 0 140 140">
                <circle cx="70" cy="70" r="60" fill="none" stroke="#e2e8f0" stroke-width="8" />
                <circle cx="70" cy="70" r="60" fill="none" :stroke="scoreColor" stroke-width="8"
                  stroke-linecap="round" :stroke-dasharray="dashLength" :stroke-dashoffset="dashGap"
                  class="score-circle"
                />
              </svg>
              <div class="score-ring-text">
                <span class="score-number" :style="{ color: scoreColor }">{{ reportData.total_score }}</span>
                <span class="score-unit">分</span>
              </div>
            </div>
          </div>
          <div class="score-right">
            <el-tag :type="levelType" size="large" class="level-tag">{{ reportData.level }}</el-tag>
            <p class="score-one-liner">{{ scoreOneLiner }}</p>
            <div class="score-meta">
              <div class="score-meta-item">
                <span class="meta-label">文件名</span>
                <span class="meta-value">{{ reportData.file_name }}</span>
              </div>
              <div class="score-meta-item">
                <span class="meta-label">评估类型</span>
                <span class="meta-value">{{ isPPT ? 'PPT评估' : '报告评估' }}</span>
              </div>
              <div class="score-meta-item">
                <span class="meta-label">生成时间</span>
                <span class="meta-value">{{ formatTime(reportData.completed_at) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="report-section from-right" :class="{ visible: phaseCount >= 2 }">
        <div class="section-card">
          <h3 class="section-heading">
            <el-icon size="22"><TrendCharts /></el-icon>
            评分维度
          </h3>
          <div class="dimension-chart" ref="chartRef"></div>
        </div>
      </div>

      <div class="report-section from-bottom" :class="{ visible: phaseCount >= 3 }">
        <div class="section-card">
          <h3 class="section-heading">
            <el-icon size="22"><List /></el-icon>
            评分明细
          </h3>
          <div class="dimension-table-wrap">
            <table class="dimension-table">
              <thead>
                <tr>
                  <th class="col-name">评分维度</th>
                  <th class="col-score">得分</th>
                  <th class="col-max">满分</th>
                  <th class="col-bar">得分率</th>
                  <th class="col-comment">评估说明</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="dim in dimensionScores" :key="dim.key">
                  <td class="col-name">{{ dim.name }}</td>
                  <td class="col-score">
                    <span class="dim-score-val">{{ dim.score }}</span>
                  </td>
                  <td class="col-max">{{ dim.max_score }}</td>
                  <td class="col-bar">
                    <div class="dim-bar-bg">
                      <div class="dim-bar-fill" :style="{ width: (dim.score / dim.max_score * 100) + '%', background: barColor(dim.score, dim.max_score) }"></div>
                    </div>
                  </td>
                  <td class="col-comment">{{ dim.comment }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="report-section from-left" :class="{ visible: phaseCount >= 4 }">
        <div class="section-card">
          <h3 class="section-heading">
            <el-icon size="22"><ChatDotSquare /></el-icon>
            核心评价
          </h3>
          <p class="core-comment">{{ reportData.core_comment }}</p>
        </div>
      </div>

      <div class="report-section from-left" :class="{ visible: phaseCount >= 5 }">
        <div class="section-card">
          <h3 class="section-heading">
            <el-icon size="22"><Star /></el-icon>
            主要优势
          </h3>
          <div class="item-list">
            <div v-for="(item, i) in reportData.advantages" :key="'adv' + i" class="item-row good">
              <el-icon size="16"><Check /></el-icon>
              <span>{{ item }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="report-section from-right" :class="{ visible: phaseCount >= 5 }">
        <div class="section-card">
          <h3 class="section-heading">
            <el-icon size="22"><Warning /></el-icon>
            关键问题
          </h3>
          <div class="item-list">
            <div v-for="(item, i) in reportData.problems" :key="'prob' + i" class="item-row warn">
              <el-icon size="16"><InfoFilled /></el-icon>
              <span>{{ item }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="report-section from-bottom" :class="{ visible: phaseCount >= 6 }">
        <div class="section-card">
          <h3 class="section-heading">
            <el-icon size="22"><Opportunity /></el-icon>
            优化建议
          </h3>
          <div class="suggestions-list">
            <div v-for="(item, i) in reportData.suggestions" :key="'sug' + i" class="sug-item">
              <span class="sug-num">{{ i + 1 }}</span>
              <span class="sug-text">{{ item }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="report-section from-bottom" :class="{ visible: phaseCount >= 6 }">
        <div class="section-card next-actions-card">
          <h3 class="section-heading">
            <el-icon size="22"><Pointer /></el-icon>
            下一步行动
          </h3>
          <div class="actions-grid">
            <div v-for="(item, i) in reportData.next_actions" :key="'act' + i" class="action-item">
              <div class="action-item-num">{{ i + 1 }}</div>
              <span>{{ item }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="report-footer">
      <el-button type="primary" size="large" class="download-btn-bottom" @click="downloadPDF" :loading="downloadingPDF" :disabled="downloadingPDF">
        <el-icon><Download /></el-icon>
        下载完整评估报告 (PDF)
      </el-button>
      <el-button size="large" class="back-btn" @click="goBack">
        <el-icon><ArrowLeft /></el-icon>
        返回评估中心
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  Download, TrendCharts, List, ChatDotSquare, Star, Warning,
  InfoFilled, Opportunity, Pointer, Check, ArrowLeft
} from '@element-plus/icons-vue'
import { getReport, downloadReportPdf } from '@/api/materialEvaluation'
import * as echarts from 'echarts'

const route = useRoute()
const router = useRouter()

const taskId = computed(() => route.params.taskId)
const reportData = ref(null)
const isPPT = ref(false)
const downloadingPDF = ref(false)
const phaseCount = ref(0)
const chartRef = ref(null)
let chartInstance = null

const scoreColor = computed(() => {
  if (!reportData.value) return '#2563eb'
  const s = reportData.value.total_score
  if (s >= 90) return '#10b981'
  if (s >= 80) return '#3b82f6'
  return '#f59e0b'
})

const levelType = computed(() => {
  if (!reportData.value) return 'primary'
  if (reportData.value.total_score >= 90) return 'success'
  if (reportData.value.total_score >= 80) return 'primary'
  return 'warning'
})

const scoreOneLiner = computed(() => {
  if (!reportData.value) return ''
  const s = reportData.value.total_score
  if (s >= 90) return '该材料整体表现优秀，在多个维度上达到了较高水准'
  if (s >= 80) return '该材料整体表现良好，具备较强的参赛展示基础'
  return '该材料具备基础框架，但在深度和细节方面有提升空间'
})

const dashLength = 2 * Math.PI * 60
const dashGap = computed(() => {
  if (!reportData.value) return dashLength
  return dashLength * (1 - reportData.value.total_score / 100)
})

const dimensionScores = computed(() => reportData.value?.dimension_scores || [])

function barColor(score, max) {
  const ratio = score / max
  if (ratio >= 0.85) return '#10b981'
  if (ratio >= 0.7) return '#3b82f6'
  return '#f59e0b'
}

function formatTime(iso) {
  if (!iso) return '-'
  const d = new Date(iso)
  return d.toLocaleString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
}

function initChart() {
  if (!chartRef.value || !reportData.value) return
  const dims = dimensionScores.value
  if (!dims.length) return

  if (chartInstance) chartInstance.dispose()

  chartInstance = echarts.init(chartRef.value)
  const option = {
    tooltip: {
      trigger: 'axis',
      backgroundColor: '#fff',
      borderColor: '#e2e8f0',
      textStyle: { color: '#1e293b', fontSize: 13 },
      formatter: (params) => {
        const p = params[0]
        return `<b>${p.name}</b><br/>得分: <b>${p.value}</b> / ${dims[p.dataIndex].max_score}`
      }
    },
    grid: { left: '3%', right: '8%', bottom: '3%', top: 12, containLabel: true },
    xAxis: {
      type: 'value',
      max: 100,
      axisLabel: { show: false },
      axisTick: { show: false },
      splitLine: { show: false }
    },
    yAxis: {
      type: 'category',
      data: dims.map(d => d.name),
      axisTick: { show: false },
      axisLine: { show: false },
      axisLabel: { color: '#475569', fontSize: 12 },
      inverse: true
    },
    series: [{
      type: 'bar',
      data: dims.map(d => ({
        value: Math.round(d.score / d.max_score * 100),
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: '#6366f1' },
            { offset: 1, color: '#7c3aed' }
          ]),
          borderRadius: [0, 6, 6, 0]
        }
      })),
      barWidth: 18,
      label: {
        show: true,
        position: 'right',
        formatter: (p) => `${dims[p.dataIndex].score}/${dims[p.dataIndex].max_score}`,
        color: '#64748b',
        fontSize: 11
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 12,
          shadowColor: 'rgba(99,102,241,0.3)'
        }
      }
    }]
  }
  chartInstance.setOption(option)

  window.addEventListener('resize', () => chartInstance?.resize())
}

function startAnimation() {
  const phases = [1, 2, 3, 4, 5, 6]
  phases.forEach((p, i) => {
    setTimeout(() => {
      phaseCount.value = p
    }, i * 180 + 400)
  })
}

async function downloadPDF() {
  if (downloadingPDF.value) return
  downloadingPDF.value = true
  try {
    const blob = await downloadReportPdf(taskId.value)

    if (!blob || !(blob instanceof Blob)) {
      ElMessage.error('PDF文件格式异常，请稍后重试')
      return
    }

    if (blob.size === 0) {
      ElMessage.error('PDF文件内容为空，无法下载')
      return
    }

    const contentType = blob.type || ''
    if (!contentType.includes('pdf') && !contentType.includes('octet-stream') && contentType !== '') {
      ElMessage.error('下载内容格式异常，请稍后重试')
      return
    }

    const blobUrl = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = blobUrl
    a.download = `AI评估报告_${isPPT.value ? 'PPT' : '报告'}_${taskId.value}.pdf`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    setTimeout(() => URL.revokeObjectURL(blobUrl), 10000)
    ElMessage.success('PDF报告下载成功')
  } catch (e) {
    ElMessage.error('PDF下载失败，请稍后重试')
  } finally {
    downloadingPDF.value = false
  }
}

function goBack() {
  router.push('/ai-material-evaluation')
}

onMounted(async () => {
  try {
    const res = await getReport(taskId.value)
    if (res.code === 200 && res.data) {
      reportData.value = res.data
      isPPT.value = res.data.evaluation_type === 'ppt'
      startAnimation()
      setTimeout(() => {
        nextTick(() => initChart())
      }, 2000)
    } else {
      ElMessage.error('未找到对应的评估报告')
      router.push('/ai-material-evaluation')
    }
  } catch (e) {
    ElMessage.error('加载报告失败')
    router.push('/ai-material-evaluation')
  }
})
</script>

<style scoped>
.report-page {
  min-height: 100vh;
  background: #f5f8ff;
  padding-bottom: 60px;
}

.report-hero {
  background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 40%, #7c3aed 100%);
  position: relative;
  overflow: hidden;
  padding: 40px 24px 32px;
}

.report-hero-bg {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 500px 300px at 25% 50%, rgba(99,102,241,0.2), transparent),
    radial-gradient(ellipse 400px 250px at 75% 40%, rgba(124,58,237,0.15), transparent);
}

.report-hero-content {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
  position: relative;
  z-index: 2;
}

.report-hero-title {
  font-size: 32px;
  font-weight: 700;
  color: #fff;
  margin: 0 0 8px;
}

.report-hero-subtitle {
  font-size: 14px;
  color: rgba(255,255,255,0.65);
  margin: 0 0 20px;
}

.download-btn-top {
  background: rgba(255,255,255,0.12);
  border: 1px solid rgba(255,255,255,0.2);
  color: #fff;
  border-radius: 12px;
  backdrop-filter: blur(10px);
  height: 38px;
  font-size: 13px;
}

.download-btn-top:hover {
  background: rgba(255,255,255,0.2);
  border-color: rgba(255,255,255,0.35);
}

.report-body {
  max-width: 860px;
  margin: 0 auto;
  padding: 40px 24px;
}

.report-section {
  opacity: 0;
  transition: all 0.65s cubic-bezier(0.22, 1, 0.36, 1);
  margin-bottom: 20px;
}

.report-section.visible {
  opacity: 1;
  transform: translate(0, 0) scale(1) !important;
}

/* 飞入方向 */
.from-top { transform: translateY(-48px); }
.from-left { transform: translateX(-64px); }
.from-right { transform: translateX(64px); }
.from-bottom { transform: translateY(48px); }

.section-card {
  background: #fff;
  border-radius: 20px;
  padding: 28px 32px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.04);
  border: 1px solid #e8ecf4;
}

.section-heading {
  font-size: 17px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.section-heading .el-icon { color: #6366f1; }

/* 综合评分卡片 */
.score-card {
  display: flex;
  gap: 32px;
  align-items: center;
  padding: 8px 0;
}

.score-left { flex-shrink: 0; }

.score-ring {
  width: 140px;
  height: 140px;
  position: relative;
}

.score-ring svg { width: 100%; height: 100%; }

.score-circle {
  transition: stroke-dashoffset 1.5s cubic-bezier(0.22, 1, 0.36, 1);
}

.score-ring-text {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.score-number {
  font-size: 42px;
  font-weight: 800;
  line-height: 1;
  animation: scoreCountUp 1.5s ease-out;
}

.score-unit {
  font-size: 13px;
  color: #94a3b8;
  margin-top: 2px;
}

@keyframes scoreCountUp {
  from { opacity: 0; transform: translateY(8px) scale(0.9); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

.score-right { flex: 1; min-width: 0; }

.level-tag {
  font-size: 15px;
  font-weight: 700;
  padding: 6px 18px;
  border-radius: 10px;
  margin-bottom: 12px;
}

.score-one-liner {
  font-size: 15px;
  color: #475569;
  margin: 0 0 16px;
  line-height: 1.6;
}

.score-meta {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.score-meta-item {
  display: flex;
  gap: 12px;
  font-size: 13px;
}

.meta-label { color: #94a3b8; flex-shrink: 0; min-width: 56px; }
.meta-value { color: #475569; }

/* 维度图 */
.dimension-chart { width: 100%; height: 260px; }

/* 评分明细表 */
.dimension-table-wrap { overflow-x: auto; }

.dimension-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 13px;
}

.dimension-table thead th {
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  color: #fff;
  font-weight: 600;
  font-size: 12px;
  padding: 10px 14px;
  text-align: left;
  white-space: nowrap;
}

.dimension-table thead th:first-child { border-radius: 10px 0 0 0; }
.dimension-table thead th:last-child { border-radius: 0 10px 0 0; }

.dimension-table tbody td {
  padding: 12px 14px;
  border-bottom: 1px solid #f1f5f9;
  color: #475569;
  vertical-align: middle;
}

.dimension-table tbody tr:nth-child(even) td { background: #f8fafc; }
.dimension-table tbody tr:hover td { background: #f0f4ff; }

.col-name { font-weight: 600; color: #1e293b; min-width: 120px; }
.col-score, .col-max { text-align: center; width: 60px; }

.dim-score-val {
  font-weight: 700;
  font-size: 15px;
  color: #2563eb;
}

.col-bar { width: 120px; min-width: 80px; }

.dim-bar-bg {
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
}

.dim-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 1s ease;
}

.col-comment { color: #64748b; font-size: 12px; line-height: 1.5; }

/* 核心评价 */
.core-comment {
  font-size: 15px;
  color: #475569;
  line-height: 1.8;
  margin: 0;
}

/* 优势/问题列表 */
.item-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.item-row {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 14px;
  line-height: 1.6;
  padding: 10px 14px;
  border-radius: 10px;
}

.item-row.good {
  background: #f0fdf4;
  color: #166534;
}

.item-row.good .el-icon { color: #10b981; flex-shrink: 0; margin-top: 2px; }

.item-row.warn {
  background: #fffbeb;
  color: #92400e;
}

.item-row.warn .el-icon { color: #f59e0b; flex-shrink: 0; margin-top: 2px; }

/* 优化建议 */
.suggestions-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.sug-item {
  display: flex;
  gap: 14px;
  align-items: flex-start;
  font-size: 14px;
  line-height: 1.6;
  color: #475569;
}

.sug-num {
  width: 26px;
  height: 26px;
  border-radius: 8px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: #fff;
  font-weight: 700;
  font-size: 13px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

/* 下一步行动 */
.next-actions-card {
  background: linear-gradient(135deg, #f8faff, #f0f4ff);
  border-color: #dbeafe;
}

.actions-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.action-item {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  font-size: 14px;
  line-height: 1.6;
  color: #475569;
  padding: 14px 16px;
  background: #fff;
  border-radius: 12px;
  border: 1px solid #e0e7ff;
}

.action-item-num {
  width: 24px;
  height: 24px;
  border-radius: 7px;
  background: #eef2ff;
  color: #6366f1;
  font-weight: 700;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

/* 底部按钮 */
.report-footer {
  max-width: 860px;
  margin: 0 auto;
  padding: 32px 24px 0;
  display: flex;
  gap: 14px;
  justify-content: center;
  flex-wrap: wrap;
}

.download-btn-bottom {
  border-radius: 14px;
  font-size: 15px;
  font-weight: 600;
  height: 48px;
  padding: 0 28px;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  border: none;
  display: flex;
  align-items: center;
  gap: 8px;
}

.download-btn-bottom:hover {
  background: linear-gradient(135deg, #1d4ed8, #6d28d9);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(37,99,235,0.3);
}

.back-btn {
  border-radius: 14px;
  font-size: 15px;
  height: 48px;
  padding: 0 28px;
  border-color: #e2e8f0;
  color: #64748b;
}

@media (max-width: 768px) {
  .score-card { flex-direction: column; text-align: center; }
  .score-meta-item { justify-content: center; }
  .report-hero-title { font-size: 24px; }
  .section-card { padding: 20px 20px; }
  .actions-grid { grid-template-columns: 1fr; }
  .dimension-table thead th,
  .dimension-table tbody td { padding: 8px 10px; font-size: 12px; }
}
</style>