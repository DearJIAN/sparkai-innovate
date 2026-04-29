<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <el-button link :icon="ArrowLeft" @click="$router.back()">返回</el-button>
        <h2 class="page-title">项目评审</h2>
      </div>
    </div>

    <div v-loading="loading">
      <!-- 项目基本信息 -->
      <el-card class="project-card" shadow="never">
        <template #header>
          <div class="project-header">
            <span class="project-name">{{ project.name }}</span>
            <el-tag :type="statusType(project.status)" size="small">{{ statusText(project.status) }}</el-tag>
          </div>
        </template>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="项目类别">{{ project.category || '-' }}</el-descriptions-item>
          <el-descriptions-item label="所属赛道">{{ project.track || '-' }}</el-descriptions-item>
          <el-descriptions-item label="当前阶段">{{ stageText(project.stage) }}</el-descriptions-item>
          <el-descriptions-item label="负责人">{{ project.leader?.real_name || '-' }}</el-descriptions-item>
          <el-descriptions-item label="项目简介" :span="2">{{ project.description || '暂无描述' }}</el-descriptions-item>
        </el-descriptions>
      </el-card>

      <el-row :gutter="20" class="mt-4">
        <!-- 左侧：团队、材料、任务 -->
        <el-col :span="12">
          <!-- 团队成员 -->
          <el-card shadow="never" class="mb-4">
            <template #header><span>团队成员</span></template>
            <el-empty v-if="!project.members?.length" description="暂无成员" :image-size="60" />
            <el-table v-else :data="project.members" size="small">
              <el-table-column prop="member_name" label="姓名" />
              <el-table-column prop="role_in_project" label="角色" />
              <el-table-column prop="responsibility" label="分工" show-overflow-tooltip />
            </el-table>
          </el-card>

          <!-- 材料列表 -->
          <el-card shadow="never" class="mb-4">
            <template #header><span>项目材料</span></template>
            <el-empty v-if="!project.files?.length" description="暂无材料" :image-size="60" />
            <div v-else class="file-list">
              <div v-for="file in project.files" :key="file.id" class="file-item">
                <el-icon><Document /></el-icon>
                <span class="file-name">{{ file.original_name }}</span>
                <el-tag size="small" type="info">{{ file.material_type }}</el-tag>
              </div>
            </div>
          </el-card>

          <!-- 任务进度 -->
          <el-card shadow="never">
            <template #header><span>任务进度</span></template>
            <el-empty v-if="!project.tasks?.length" description="暂无任务" :image-size="60" />
            <div v-else class="task-list">
              <div v-for="task in project.tasks.slice(0, 5)" :key="task.id" class="task-item">
                <el-icon size="14" :color="taskStatusColor(task.status)">
                  <component :is="taskStatusIcon(task.status)" />
                </el-icon>
                <span class="task-title" :class="{ 'task-done': task.status === 'done' }">{{ task.title }}</span>
                <el-tag size="small" :type="priorityType(task.priority)">{{ priorityText(task.priority) }}</el-tag>
              </div>
            </div>
          </el-card>
        </el-col>

        <!-- 右侧：评分表单 -->
        <el-col :span="12">
          <el-card shadow="never">
            <template #header>
              <span>{{ hasReviewed ? '修改评审' : '提交评审' }}</span>
            </template>

            <el-form :model="reviewForm" label-width="100px">
              <el-form-item label="创新性">
                <el-slider v-model="reviewForm.innovation_score" :max="100" show-input />
              </el-form-item>
              <el-form-item label="可行性">
                <el-slider v-model="reviewForm.feasibility_score" :max="100" show-input />
              </el-form-item>
              <el-form-item label="市场前景">
                <el-slider v-model="reviewForm.market_score" :max="100" show-input />
              </el-form-item>
              <el-form-item label="团队能力">
                <el-slider v-model="reviewForm.team_score" :max="100" show-input />
              </el-form-item>
              <el-form-item label="商业模式">
                <el-slider v-model="reviewForm.business_score" :max="100" show-input />
              </el-form-item>
              <el-form-item label="技术实现">
                <el-slider v-model="reviewForm.technology_score" :max="100" show-input />
              </el-form-item>
              <el-form-item label="路演表现">
                <el-slider v-model="reviewForm.presentation_score" :max="100" show-input />
              </el-form-item>

              <el-divider />

              <div class="total-score">
                <span class="total-label">总分</span>
                <span class="total-value">{{ totalScore }}</span>
                <span class="total-max">/ 100</span>
              </div>

              <el-form-item label="评审意见">
                <el-input
                  v-model="reviewForm.comment"
                  type="textarea"
                  :rows="4"
                  placeholder="请输入评审意见和建议"
                  maxlength="1000"
                  show-word-limit
                />
              </el-form-item>

              <el-form-item>
                <el-button type="primary" :loading="submitting" @click="handleSubmit">
                  {{ hasReviewed ? '更新评审' : '提交评审' }}
                </el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  ArrowLeft, Document, CircleCheckFilled, Loading,
  WarningFilled, CircleCloseFilled, Timer
} from '@element-plus/icons-vue'
import { getProjectForReview, submitReview } from '@/api/review'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()

const projectId = computed(() => route.params.id)
const loading = ref(false)
const submitting = ref(false)
const project = ref({})
const hasReviewed = ref(false)

const reviewForm = reactive({
  innovation_score: 60,
  feasibility_score: 60,
  market_score: 60,
  team_score: 60,
  business_score: 60,
  technology_score: 60,
  presentation_score: 60,
  comment: ''
})

const totalScore = computed(() => {
  const scores = [
    reviewForm.innovation_score,
    reviewForm.feasibility_score,
    reviewForm.market_score,
    reviewForm.team_score,
    reviewForm.business_score,
    reviewForm.technology_score,
    reviewForm.presentation_score
  ]
  return Math.round(scores.reduce((a, b) => a + b, 0) / scores.length)
})

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
  loading.value = true
  try {
    const res = await getProjectForReview(projectId.value)
    if (res.code === 200) {
      project.value = res.data.project || {}
      // 如果已有评审记录，填充表单
      if (project.value.my_review) {
        hasReviewed.value = true
        const r = project.value.my_review
        reviewForm.innovation_score = r.innovation_score || 60
        reviewForm.feasibility_score = r.feasibility_score || 60
        reviewForm.market_score = r.market_score || 60
        reviewForm.team_score = r.team_score || 60
        reviewForm.business_score = r.business_score || 60
        reviewForm.technology_score = r.technology_score || 60
        reviewForm.presentation_score = r.presentation_score || 60
        reviewForm.comment = r.comment || ''
      }
    } else {
      ElMessage.error(res.message || '获取项目失败')
    }
  } catch (error) {
    ElMessage.error('获取项目详情失败')
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  submitting.value = true
  try {
    const data = {
      innovation_score: reviewForm.innovation_score,
      feasibility_score: reviewForm.feasibility_score,
      market_score: reviewForm.market_score,
      team_score: reviewForm.team_score,
      business_score: reviewForm.business_score,
      technology_score: reviewForm.technology_score,
      presentation_score: reviewForm.presentation_score,
      comment: reviewForm.comment
    }

    const res = await submitReview(projectId.value, data)
    if (res.code === 200) {
      ElMessage.success(hasReviewed.value ? '评审更新成功' : '评审提交成功')
      hasReviewed.value = true
    } else {
      ElMessage.error(res.message || '提交失败')
    }
  } catch (error) {
    ElMessage.error('提交失败')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  fetchProject()
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

.project-card {
  margin-bottom: 16px;
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.project-name {
  font-size: 16px;
  font-weight: 600;
}

.mt-4 {
  margin-top: 16px;
}

.mb-4 {
  margin-bottom: 16px;
}

.file-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.file-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
}

.file-name {
  flex: 1;
  font-size: 13px;
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.task-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
}

.task-title {
  flex: 1;
  font-size: 13px;
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.task-title.task-done {
  text-decoration: line-through;
  color: var(--text-tertiary);
}

.total-score {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 4px;
  margin-bottom: 20px;
  padding: 16px;
  background: var(--primary-50);
  border-radius: var(--radius-lg);
}

.total-label {
  font-size: 14px;
  color: var(--text-secondary);
}

.total-value {
  font-size: 36px;
  font-weight: 700;
  color: var(--primary-600);
  line-height: 1;
}

.total-max {
  font-size: 14px;
  color: var(--text-tertiary);
}
</style>
