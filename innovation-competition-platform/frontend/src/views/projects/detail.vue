<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <el-button link :icon="ArrowLeft" @click="$router.back()">返回</el-button>
        <h2 class="page-title">{{ project.name || '项目详情' }}</h2>
        <el-tag :type="statusType(project.status)" size="small">
          {{ statusText(project.status) }}
        </el-tag>
      </div>
      <div class="header-right">
        <el-button
          v-if="canEdit"
          type="primary"
          plain
          :icon="Edit"
          @click="$router.push(`/projects/${project.id}/edit`)"
        >
          编辑项目
        </el-button>
        <el-button
          v-if="canSubmit"
          type="primary"
          :icon="Upload"
          @click="handleSubmit"
        >
          提交评审
        </el-button>
      </div>
    </div>

    <div v-loading="loading">
      <!-- 项目阶段进度 -->
      <el-card class="stage-card" shadow="never">
        <div class="stage-header">
          <span class="stage-title">项目阶段</span>
          <span class="stage-current">当前: {{ stageText(project.stage) }}</span>
        </div>
        <el-steps :active="stageIndex(project.stage)" finish-status="success" simple>
          <el-step title="创意" />
          <el-step title="验证" />
          <el-step title="资源" />
          <el-step title="开发" />
          <el-step title="市场" />
          <el-step title="路演" />
          <el-step title="孵化" />
        </el-steps>
      </el-card>

      <el-row :gutter="20" class="mt-4">
        <!-- 左侧：项目信息 -->
        <el-col :span="16">
          <el-card shadow="never">
            <template #header>
              <span>项目信息</span>
            </template>
            <el-descriptions :column="2" border>
              <el-descriptions-item label="项目名称">{{ project.name }}</el-descriptions-item>
              <el-descriptions-item label="项目类别">{{ project.category || '-' }}</el-descriptions-item>
              <el-descriptions-item label="所属赛道">{{ project.track || '-' }}</el-descriptions-item>
              <el-descriptions-item label="当前阶段">{{ stageText(project.stage) }}</el-descriptions-item>
              <el-descriptions-item label="负责人">
                {{ project.leader?.real_name || project.leader?.username || '-' }}
              </el-descriptions-item>
              <el-descriptions-item label="指导老师">
                {{ project.teacher?.real_name || project.teacher?.username || '-' }}
              </el-descriptions-item>
              <el-descriptions-item label="开始时间">{{ formatDate(project.start_date) }}</el-descriptions-item>
              <el-descriptions-item label="预计结束">{{ formatDate(project.end_date) }}</el-descriptions-item>
              <el-descriptions-item label="创建时间">{{ formatDate(project.created_at) }}</el-descriptions-item>
              <el-descriptions-item label="更新时间">{{ formatDate(project.updated_at) }}</el-descriptions-item>
              <el-descriptions-item label="项目简介" :span="2">
                {{ project.description || '暂无描述' }}
              </el-descriptions-item>
            </el-descriptions>
          </el-card>

          <!-- 操作区域 -->
          <el-card class="mt-4" shadow="never">
            <template #header>
              <span>项目管理</span>
            </template>
            <div class="action-grid">
              <div class="action-item" @click="goToMaterials">
                <div class="action-icon" style="background: var(--primary-50); color: var(--primary-600);">
                  <el-icon size="24"><Document /></el-icon>
                </div>
                <div class="action-info">
                  <div class="action-title">材料管理</div>
                  <div class="action-desc">上传项目材料、文档、PPT 等</div>
                </div>
                <el-icon class="action-arrow"><ArrowRight /></el-icon>
              </div>

              <div class="action-item" @click="goToTasks">
                <div class="action-icon" style="background: var(--warning-50); color: var(--warning-600);">
                  <el-icon size="24"><List /></el-icon>
                </div>
                <div class="action-info">
                  <div class="action-title">任务进度</div>
                  <div class="action-desc">管理项目任务和里程碑</div>
                </div>
                <el-icon class="action-arrow"><ArrowRight /></el-icon>
              </div>

              <div class="action-item" @click="goToTeam">
                <div class="action-icon" style="background: var(--success-50); color: var(--success-600);">
                  <el-icon size="24"><User /></el-icon>
                </div>
                <div class="action-info">
                  <div class="action-title">团队成员</div>
                  <div class="action-desc">管理项目成员和分工</div>
                </div>
                <el-icon class="action-arrow"><ArrowRight /></el-icon>
              </div>
            </div>
          </el-card>
        </el-col>

        <!-- 右侧：统计信息 -->
        <el-col :span="8">
          <el-card shadow="never">
            <template #header>
              <span>项目统计</span>
            </template>
            <div class="stat-list">
              <div class="stat-item">
                <div class="stat-icon-small" style="background: var(--primary-50); color: var(--primary-600);">
                  <el-icon><User /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-value">{{ project.members?.length || 0 }}</div>
                  <div class="stat-label">团队成员</div>
                </div>
              </div>
              <div class="stat-item">
                <div class="stat-icon-small" style="background: var(--info-50); color: var(--info-600);">
                  <el-icon><Document /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-value">{{ project.files_count || 0 }}</div>
                  <div class="stat-label">材料文件</div>
                </div>
              </div>
              <div class="stat-item">
                <div class="stat-icon-small" style="background: var(--warning-50); color: var(--warning-600);">
                  <el-icon><List /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-value">{{ project.tasks_count || 0 }}</div>
                  <div class="stat-label">任务数量</div>
                </div>
              </div>
            </div>
          </el-card>

          <!-- 任务进度 -->
          <el-card class="mt-4" shadow="never">
            <template #header>
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <span>任务进度</span>
                <el-button v-if="taskStats.total > 0" link size="small" @click="goToTasks">
                  查看全部
                </el-button>
              </div>
            </template>
            <div v-if="taskStats.total > 0">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <span style="font-size: 13px; color: var(--text-secondary);">
                  已完成 {{ taskStats.done }} / {{ taskStats.total }}
                </span>
                <span style="font-size: 13px; font-weight: 600; color: var(--primary-600);">
                  {{ taskStats.completion_rate }}%
                </span>
              </div>
              <el-progress :percentage="taskStats.completion_rate" :stroke-width="8" :show-text="false" />
              <div class="recent-tasks">
                <div
                  v-for="task in recentTasks.slice(0, 3)"
                  :key="task.id"
                  class="recent-task-item"
                >
                  <el-icon size="14" :color="taskStatusColor(task.status)">
                    <component :is="taskStatusIcon(task.status)" />
                  </el-icon>
                  <span class="recent-task-title" :class="{ 'task-done': task.status === 'done' }">
                    {{ task.title }}
                  </span>
                  <el-tag size="small" :type="priorityType(task.priority)">{{ priorityText(task.priority) }}</el-tag>
                </div>
              </div>
            </div>
            <el-empty v-else description="暂无任务" :image-size="60">
              <el-button v-if="canManage" type="primary" size="small" @click="goToTasks">创建任务</el-button>
            </el-empty>
          </el-card>

          <!-- 评审结果 -->
          <el-card class="mt-4" shadow="never">
            <template #header>
              <span>评审结果</span>
            </template>
            <div v-if="reviews.length > 0">
              <div class="review-summary">
                <div class="review-score">
                  <span class="score-value">{{ averageScore }}</span>
                  <span class="score-label">平均分</span>
                </div>
              </div>
              <div class="review-list">
                <div v-for="review in reviews" :key="review.id" class="review-item">
                  <div class="review-header">
                    <span class="reviewer">{{ review.judge?.real_name || review.judge?.username || '评委' }}</span>
                    <span class="review-score-tag">{{ review.total_score }}分</span>
                  </div>
                  <div class="review-scores">
                    <span>创新 {{ review.innovation_score }}</span>
                    <span>可行 {{ review.feasibility_score }}</span>
                    <span>市场 {{ review.market_score }}</span>
                    <span>团队 {{ review.team_score }}</span>
                    <span>商业 {{ review.business_score }}</span>
                    <span>技术 {{ review.technology_score }}</span>
                    <span>路演 {{ review.presentation_score }}</span>
                  </div>
                  <div v-if="review.comment" class="review-comment">{{ review.comment }}</div>
                </div>
              </div>
            </div>
            <el-empty v-else-if="['passed', 'rejected', 'judging'].includes(project.status)" description="评审进行中，暂无结果" :image-size="80" />
            <el-empty v-else description="暂无评审结果" :image-size="80" />
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import {
  ArrowLeft, Edit, Upload, Document, List, User, ArrowRight,
  CircleCheckFilled, Loading, WarningFilled, CircleCloseFilled, Timer
} from '@element-plus/icons-vue'
import { getProject, submitProject } from '@/api/project'
import { getTasks } from '@/api/task'
import { getProjectReviews } from '@/api/review'
import { ElMessage, ElMessageBox } from 'element-plus'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const project = ref({})
const taskStats = ref({ total: 0, done: 0, doing: 0, todo: 0, delayed: 0, completion_rate: 0 })
const recentTasks = ref([])
const reviews = ref([])
const averageScore = ref(0)

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

const stageList = ['idea', 'proof', 'resource', 'development', 'market', 'roadshow', 'incubation']

const statusText = (status) => statusMap[status]?.text || status
const statusType = (status) => statusMap[status]?.type || 'info'
const stageText = (stage) => stageMap[stage] || stage
const stageIndex = (stage) => stageList.indexOf(stage) + 1

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

const canEdit = computed(() => {
  if (!project.value.id) return false
  if (userStore.isAdmin) return true
  if (project.value.leader_id === userStore.userInfo?.id) {
    return ['draft', 'need_modify'].includes(project.value.status)
  }
  return false
})

const canSubmit = computed(() => {
  if (!project.value.id) return false
  if (project.value.leader_id !== userStore.userInfo?.id && !userStore.isAdmin) return false
  return ['draft', 'need_modify'].includes(project.value.status)
})

const canManage = computed(() => {
  if (!project.value.id) return false
  if (userStore.isAdmin) return true
  return project.value.leader_id === userStore.userInfo?.id
})

const priorityMap = {
  low: { text: '低', type: 'info' },
  medium: { text: '中', type: 'warning' },
  high: { text: '高', type: 'danger' }
}
const priorityText = (p) => priorityMap[p]?.text || p
const priorityType = (p) => priorityMap[p]?.type || 'info'

const taskStatusIcon = (status) => {
  const map = { done: CircleCheckFilled, doing: Loading, delayed: WarningFilled, cancelled: CircleCloseFilled, todo: Timer }
  return map[status] || Timer
}
const taskStatusColor = (status) => {
  const map = { done: '#67C23A', doing: '#409EFF', delayed: '#F56C6C', cancelled: '#909399', todo: '#E6A23C' }
  return map[status] || '#909399'
}

const fetchProject = async () => {
  const id = route.params.id
  if (!id) return

  loading.value = true
  try {
    const res = await getProject(id)
    if (res.code === 200) {
      project.value = res.data.project || {}
    } else {
      ElMessage.error(res.message || '获取项目失败')
    }
  } catch (error) {
    ElMessage.error('获取项目详情失败')
  } finally {
    loading.value = false
  }
}

const fetchTasks = async () => {
  try {
    const res = await getTasks(route.params.id)
    if (res.code === 200) {
      taskStats.value = res.data.stats || { total: 0, done: 0, doing: 0, todo: 0, delayed: 0, completion_rate: 0 }
      recentTasks.value = res.data.tasks || []
    }
  } catch (error) {
    console.error('获取任务失败', error)
  }
}

const fetchReviews = async () => {
  try {
    const res = await getProjectReviews(route.params.id)
    if (res.code === 200) {
      reviews.value = res.data.reviews || []
      averageScore.value = res.data.average_score || 0
    }
  } catch (error) {
    console.error('获取评审失败', error)
  }
}

const handleSubmit = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要提交项目 "${project.value.name}" 进入评审吗？`,
      '提交确认',
      { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' }
    )
    const res = await submitProject(project.value.id)
    if (res.code === 200) {
      ElMessage.success('项目提交成功')
      fetchProject()
    } else {
      ElMessage.error(res.message || '提交失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.message || '提交失败')
    }
  }
}

const goToMaterials = () => {
  router.push(`/projects/${project.value.id}/files`)
}

const goToTasks = () => {
  router.push(`/projects/${project.value.id}/tasks`)
}

const goToTeam = () => {
  router.push(`/projects/${project.value.id}/members`)
}

onMounted(() => {
  fetchProject()
  fetchTasks()
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

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.header-right {
  display: flex;
  gap: 12px;
}

.mt-4 {
  margin-top: 16px;
}

.stage-card {
  margin-bottom: 16px;
}

.stage-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.stage-title {
  font-weight: 600;
  color: var(--text-primary);
}

.stage-current {
  font-size: 13px;
  color: var(--primary-600);
  font-weight: 500;
}

.action-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.action-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.action-item:hover {
  border-color: var(--primary-300);
  background: var(--bg-secondary);
}

.action-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.action-info {
  flex: 1;
}

.action-title {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.action-desc {
  font-size: 13px;
  color: var(--text-secondary);
}

.action-arrow {
  color: var(--text-tertiary);
}

.stat-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.stat-icon-small {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1;
}

.stat-label {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: 4px;
}

.recent-tasks {
  margin-top: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.recent-task-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
}

.recent-task-title {
  flex: 1;
  font-size: 13px;
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.recent-task-title.task-done {
  text-decoration: line-through;
  color: var(--text-tertiary);
}

.review-summary {
  display: flex;
  justify-content: center;
  margin-bottom: 16px;
}

.review-score {
  text-align: center;
  padding: 16px 32px;
  background: var(--primary-50);
  border-radius: var(--radius-lg);
}

.score-value {
  font-size: 36px;
  font-weight: 700;
  color: var(--primary-600);
  line-height: 1;
}

.score-label {
  display: block;
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: 4px;
}

.review-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.review-item {
  padding: 12px;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.reviewer {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.review-score-tag {
  font-size: 14px;
  font-weight: 600;
  color: var(--primary-600);
}

.review-scores {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 8px;
}

.review-scores span {
  font-size: 12px;
  color: var(--text-secondary);
  background: var(--bg-primary);
  padding: 2px 8px;
  border-radius: var(--radius-sm);
}

.review-comment {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
  padding-top: 8px;
  border-top: 1px solid var(--border-light);
}
</style>
