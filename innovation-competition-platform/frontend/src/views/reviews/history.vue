<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">评审记录</h2>
      <el-button type="primary" @click="$router.push('/pending-reviews')">返回待评审</el-button>
    </div>

    <div v-loading="loading">
      <el-empty v-if="!loading && reviews.length === 0" description="暂无评审记录" />
      <div v-else class="review-list">
        <el-card v-for="review in reviews" :key="review.id" class="review-card" shadow="never">
          <template #header>
            <div class="review-header">
              <div class="review-project">
                <span class="project-name">{{ review.project?.name || '未知项目' }}</span>
                <el-tag v-if="review.project" :type="statusType(review.project.status)" size="small">
                  {{ statusText(review.project.status) }}
                </el-tag>
              </div>
              <div class="review-meta">
                <span class="review-time">{{ formatDate(review.created_at) }}</span>
                <el-tag :type="scoreType(review.total_score)" size="small" effect="dark">
                  {{ review.total_score?.toFixed(0) || '-' }} 分
                </el-tag>
              </div>
            </div>
          </template>

          <el-row :gutter="16">
            <el-col :span="16">
              <div class="score-bars">
                <div v-for="item in scoreItems(review)" :key="item.label" class="score-bar-item">
                  <span class="score-label">{{ item.label }}</span>
                  <div class="score-bar-bg">
                    <div class="score-bar-fill" :style="{ width: item.percent + '%', background: item.color }"></div>
                  </div>
                  <span class="score-value">{{ item.score }}</span>
                </div>
              </div>
            </el-col>
            <el-col :span="8">
              <div v-if="review.comment" class="review-comment">
                <div class="comment-label">评审意见</div>
                <p class="comment-text">{{ review.comment }}</p>
              </div>
              <div v-else class="review-comment">
                <div class="comment-label">评审意见</div>
                <p class="comment-text empty">未填写评审意见</p>
              </div>
              <el-button
                v-if="review.project"
                type="primary"
                size="small"
                plain
                class="mt-3"
                @click="$router.push(`/reviews/${review.project_id}`)"
              >
                查看详情
              </el-button>
            </el-col>
          </el-row>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getMyReviews } from '@/api/review'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const reviews = ref([])

const statusMap = {
  draft: { text: '草稿', type: 'info' },
  submitted: { text: '已提交', type: 'primary' },
  teacher_review: { text: '审核中', type: 'warning' },
  judging: { text: '评审中', type: 'warning' },
  passed: { text: '已通过', type: 'success' },
  need_modify: { text: '需修改', type: 'danger' },
  rejected: { text: '已驳回', type: 'danger' }
}

const statusText = (s) => statusMap[s]?.text || s
const statusType = (s) => statusMap[s]?.type || 'info'

const scoreType = (score) => {
  if (!score) return 'info'
  if (score >= 90) return 'success'
  if (score >= 80) return 'primary'
  if (score >= 70) return 'warning'
  return 'danger'
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const d = new Date(dateStr)
  return d.toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
}

const scoreItems = (review) => {
  const items = [
    { label: '创新性', key: 'innovation_score', score: review.innovation_score, color: '#409EFF' },
    { label: '可行性', key: 'feasibility_score', score: review.feasibility_score, color: '#67C23A' },
    { label: '市场前景', key: 'market_score', score: review.market_score, color: '#E6A23C' },
    { label: '团队能力', key: 'team_score', score: review.team_score, color: '#F56C6C' },
    { label: '商业模式', key: 'business_score', score: review.business_score, color: '#909399' },
    { label: '技术实现', key: 'technology_score', score: review.technology_score, color: '#9B59B6' },
    { label: '路演表现', key: 'presentation_score', score: review.presentation_score, color: '#1ABC9C' }
  ]
  return items.map(item => ({
    ...item,
    percent: item.score ? Math.round(item.score) : 0,
    score: item.score ? Math.round(item.score) : '-'
  }))
}

const fetchReviews = async () => {
  loading.value = true
  try {
    const res = await getMyReviews()
    if (res.code === 200) {
      reviews.value = res.data?.reviews || []
    } else {
      ElMessage.error(res.message || '获取评审记录失败')
    }
  } catch (error) {
    ElMessage.error('获取评审记录失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchReviews()
})
</script>

<style scoped>
.page-container {
  padding-bottom: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.review-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.review-card {
  transition: box-shadow 0.2s;
}

.review-card:hover {
  box-shadow: var(--shadow-md);
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.review-project {
  display: flex;
  align-items: center;
  gap: 10px;
}

.project-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
}

.review-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.review-time {
  font-size: 13px;
  color: var(--text-tertiary);
}

.score-bars {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.score-bar-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
}

.score-label {
  width: 60px;
  flex-shrink: 0;
  color: var(--text-secondary);
}

.score-bar-bg {
  flex: 1;
  height: 8px;
  background: var(--bg-secondary);
  border-radius: 4px;
  overflow: hidden;
}

.score-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
}

.score-value {
  width: 30px;
  text-align: right;
  color: var(--text-primary);
  font-weight: 600;
  flex-shrink: 0;
}

.review-comment {
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  padding: 12px;
}

.comment-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-tertiary);
  margin-bottom: 6px;
}

.comment-text {
  font-size: 13px;
  color: var(--text-primary);
  line-height: 1.6;
  margin: 0;
  white-space: pre-wrap;
}

.comment-text.empty {
  color: var(--text-tertiary);
  font-style: italic;
}

.mt-3 {
  margin-top: 12px;
}
</style>
