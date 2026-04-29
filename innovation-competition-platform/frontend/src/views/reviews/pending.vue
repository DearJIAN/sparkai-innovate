<template>
  <div class="page-container">
    <h2 class="page-title">待评审项目</h2>

    <el-card shadow="never" v-loading="loading">
      <el-empty v-if="projects.length === 0" description="暂无待评审项目" :image-size="80" />

      <div v-else class="project-list">
        <div
          v-for="project in projects"
          :key="project.id"
          class="project-card"
          @click="goToReview(project.id)"
        >
          <div class="project-header">
            <span class="project-name">{{ project.name }}</span>
            <el-tag :type="statusType(project.status)" size="small">{{ statusText(project.status) }}</el-tag>
          </div>
          <div class="project-meta">
            <span>阶段: {{ stageText(project.stage) }}</span>
            <span>赛道: {{ project.track || '-' }}</span>
            <span>类别: {{ project.category || '-' }}</span>
          </div>
          <div class="project-desc">{{ project.description || '暂无描述' }}</div>
          <div class="project-footer">
            <span>提交时间: {{ formatDate(project.created_at) }}</span>
            <el-button type="primary" size="small">开始评审</el-button>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getPendingProjects } from '@/api/review'
import { ElMessage } from 'element-plus'

const router = useRouter()
const loading = ref(false)
const projects = ref([])

const statusMap = {
  draft: { text: '草稿', type: 'info' },
  submitted: { text: '已提交', type: 'primary' },
  teacher_review: { text: '审核中', type: 'warning' },
  judging: { text: '评审中', type: 'warning' },
  passed: { text: '已通过', type: 'success' },
  need_modify: { text: '需修改', type: 'danger' },
  rejected: { text: '已驳回', type: 'danger' }
}

const stageMap = {
  idea: '创意阶段',
  proof: '验证阶段',
  resource: '资源整合',
  development: '产品开发',
  market: '市场推广',
  roadshow: '路演展示',
  incubation: '孵化运营'
}

const statusText = (status) => statusMap[status]?.text || status
const statusType = (status) => statusMap[status]?.type || 'info'
const stageText = (stage) => stageMap[stage] || stage

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

const fetchProjects = async () => {
  loading.value = true
  try {
    const res = await getPendingProjects()
    if (res.code === 200) {
      projects.value = res.data.projects || []
    }
  } catch (error) {
    ElMessage.error('获取待评审项目失败')
  } finally {
    loading.value = false
  }
}

const goToReview = (projectId) => {
  router.push(`/reviews/${projectId}`)
}

onMounted(() => {
  fetchProjects()
})
</script>

<style scoped>
.page-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 24px;
}

.project-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.project-card {
  padding: 20px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.project-card:hover {
  border-color: var(--primary-300);
  box-shadow: var(--shadow-sm);
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.project-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.project-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 8px;
  font-size: 13px;
  color: var(--text-secondary);
}

.project-desc {
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 12px;
  line-height: 1.5;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.project-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: var(--text-tertiary);
}
</style>
