<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <el-button link :icon="ArrowLeft" @click="$router.back()">返回项目</el-button>
        <h2 class="page-title">任务进度管理</h2>
      </div>
      <el-button v-if="canManage" type="primary" :icon="Plus" @click="openCreateDialog">
        新增任务
      </el-button>
    </div>

    <!-- 项目信息 -->
    <el-card class="project-info-card" shadow="never">
      <div class="project-info">
        <span class="project-name">{{ projectName }}</span>
        <el-tag :type="statusType(projectStatus)" size="small">{{ statusText(projectStatus) }}</el-tag>
      </div>
    </el-card>

    <!-- 统计卡片 -->
    <el-row :gutter="16" class="stats-row">
      <el-col :span="4">
        <div class="stat-card">
          <div class="stat-value">{{ stats.total }}</div>
          <div class="stat-label">总任务</div>
        </div>
      </el-col>
      <el-col :span="4">
        <div class="stat-card" style="--stat-color: var(--warning-500)">
          <div class="stat-value">{{ stats.todo }}</div>
          <div class="stat-label">待开始</div>
        </div>
      </el-col>
      <el-col :span="4">
        <div class="stat-card" style="--stat-color: var(--primary-500)">
          <div class="stat-value">{{ stats.doing }}</div>
          <div class="stat-label">进行中</div>
        </div>
      </el-col>
      <el-col :span="4">
        <div class="stat-card" style="--stat-color: var(--success-500)">
          <div class="stat-value">{{ stats.done }}</div>
          <div class="stat-label">已完成</div>
        </div>
      </el-col>
      <el-col :span="4">
        <div class="stat-card" style="--stat-color: var(--danger-500)">
          <div class="stat-value">{{ stats.delayed }}</div>
          <div class="stat-label">已延期</div>
        </div>
      </el-col>
      <el-col :span="4">
        <div class="stat-card" style="--stat-color: var(--info-500)">
          <div class="stat-value">{{ stats.completion_rate }}%</div>
          <div class="stat-label">完成率</div>
        </div>
      </el-col>
    </el-row>

    <!-- 完成率进度条 -->
    <el-card class="progress-card" shadow="never">
      <div class="progress-header">
        <span>任务完成进度</span>
        <span class="progress-text">{{ stats.completion_rate }}%</span>
      </div>
      <el-progress
        :percentage="stats.completion_rate"
        :status="progressStatus"
        :stroke-width="16"
        :show-text="false"
      />
    </el-card>

    <!-- 筛选和操作 -->
    <el-card class="filter-card" shadow="never">
      <div class="filter-bar">
        <el-radio-group v-model="filterStatus" size="small" @change="fetchTasks">
          <el-radio-button label="">全部</el-radio-button>
          <el-radio-button label="todo">待开始</el-radio-button>
          <el-radio-button label="doing">进行中</el-radio-button>
          <el-radio-button label="done">已完成</el-radio-button>
          <el-radio-button label="delayed">已延期</el-radio-button>
          <el-radio-button label="cancelled">已取消</el-radio-button>
        </el-radio-group>
      </div>
    </el-card>

    <!-- 任务列表 -->
    <el-card class="task-list-card" shadow="never" v-loading="loading">
      <template #header>
        <span>任务列表</span>
      </template>

      <el-empty v-if="tasks.length === 0" description="暂无任务" :image-size="80" />

      <div v-else class="task-list">
        <div
          v-for="task in tasks"
          :key="task.id"
          class="task-item"
          :class="`task-${task.status}`"
        >
          <div class="task-main">
            <div class="task-status-icon">
              <el-icon v-if="task.status === 'done'" size="20" color="var(--success-500)"><CircleCheckFilled /></el-icon>
              <el-icon v-else-if="task.status === 'doing'" size="20" color="var(--primary-500)"><Loading /></el-icon>
              <el-icon v-else-if="task.status === 'delayed'" size="20" color="var(--danger-500)"><WarningFilled /></el-icon>
              <el-icon v-else-if="task.status === 'cancelled'" size="20" color="var(--text-tertiary)"><CircleCloseFilled /></el-icon>
              <el-icon v-else size="20" color="var(--warning-500)"><Timer /></el-icon>
            </div>
            <div class="task-content">
              <div class="task-title-row">
                <span class="task-title" :class="{ 'task-done': task.status === 'done' }">{{ task.title }}</span>
                <el-tag size="small" :type="priorityType(task.priority)">{{ priorityText(task.priority) }}</el-tag>
                <el-tag size="small" :type="statusTagType(task.status)">{{ statusTagText(task.status) }}</el-tag>
              </div>
              <div v-if="task.description" class="task-desc">{{ task.description }}</div>
              <div class="task-meta">
                <span v-if="task.deadline" class="task-deadline" :class="{ 'deadline-overdue': isOverdue(task) }">
                  <el-icon><Calendar /></el-icon>
                  截止: {{ formatDate(task.deadline) }}
                </span>
                <span v-if="task.completed_at" class="task-completed">
                  <el-icon><CircleCheckFilled /></el-icon>
                  完成: {{ formatDate(task.completed_at) }}
                </span>
              </div>
            </div>
          </div>
          <div class="task-actions">
            <el-select
              v-if="canManage"
              v-model="task.status"
              size="small"
              style="width: 100px"
              @change="(val) => handleStatusChange(task, val)"
            >
              <el-option label="待开始" value="todo" />
              <el-option label="进行中" value="doing" />
              <el-option label="已完成" value="done" />
              <el-option label="已延期" value="delayed" />
              <el-option label="已取消" value="cancelled" />
            </el-select>
            <el-button v-if="canManage" type="primary" link size="small" @click="openEditDialog(task)">
              <el-icon><Edit /></el-icon>
            </el-button>
            <el-button v-if="canManage" type="danger" link size="small" @click="handleDelete(task)">
              <el-icon><Delete /></el-icon>
            </el-button>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 新增/编辑任务弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑任务' : '新增任务'"
      width="560px"
      destroy-on-close
    >
      <el-form :model="taskForm" label-width="80px" :rules="rules" ref="taskFormRef">
        <el-form-item label="任务标题" prop="title">
          <el-input v-model="taskForm.title" placeholder="请输入任务标题" maxlength="100" show-word-limit />
        </el-form-item>
        <el-form-item label="任务描述">
          <el-input
            v-model="taskForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入任务描述"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
        <el-form-item label="优先级">
          <el-radio-group v-model="taskForm.priority">
            <el-radio-button label="low">低</el-radio-button>
            <el-radio-button label="medium">中</el-radio-button>
            <el-radio-button label="high">高</el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="状态">
          <el-radio-group v-model="taskForm.status">
            <el-radio-button label="todo">待开始</el-radio-button>
            <el-radio-button label="doing">进行中</el-radio-button>
            <el-radio-button label="done">已完成</el-radio-button>
            <el-radio-button label="delayed">已延期</el-radio-button>
            <el-radio-button label="cancelled">已取消</el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="截止时间">
          <el-date-picker
            v-model="taskForm.deadline"
            type="datetime"
            placeholder="选择截止时间"
            format="YYYY-MM-DD HH:mm"
            value-format="YYYY-MM-DDTHH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import {
  ArrowLeft, Plus, Edit, Delete, CircleCheckFilled, Loading,
  WarningFilled, CircleCloseFilled, Timer, Calendar
} from '@element-plus/icons-vue'
import { getTasks, createTask, updateTask, deleteTask } from '@/api/task'
import { getProject } from '@/api/project'
import { ElMessage, ElMessageBox } from 'element-plus'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const projectId = computed(() => route.params.id)
const loading = ref(false)
const submitting = ref(false)
const tasks = ref([])
const stats = ref({ total: 0, done: 0, doing: 0, todo: 0, delayed: 0, completion_rate: 0 })
const projectName = ref('')
const projectStatus = ref('')
const projectLeaderId = ref(null)
const filterStatus = ref('')

const dialogVisible = ref(false)
const isEdit = ref(false)
const editingTaskId = ref(null)
const taskFormRef = ref(null)

const taskForm = reactive({
  title: '',
  description: '',
  priority: 'medium',
  status: 'todo',
  deadline: null
})

const rules = {
  title: [{ required: true, message: '请输入任务标题', trigger: 'blur' }]
}

const statusMap = {
  draft: { text: '草稿', type: 'info' },
  submitted: { text: '已提交', type: 'primary' },
  teacher_review: { text: '审核中', type: 'warning' },
  judging: { text: '评审中', type: 'warning' },
  passed: { text: '已通过', type: 'success' },
  need_modify: { text: '需修改', type: 'danger' },
  rejected: { text: '已驳回', type: 'danger' }
}

const statusText = (status) => statusMap[status]?.text || status
const statusType = (status) => statusMap[status]?.type || 'info'

const taskStatusMap = {
  todo: '待开始',
  doing: '进行中',
  done: '已完成',
  delayed: '已延期',
  cancelled: '已取消'
}

const taskStatusTagType = {
  todo: 'info',
  doing: 'primary',
  done: 'success',
  delayed: 'danger',
  cancelled: 'info'
}

const priorityMap = {
  low: { text: '低', type: 'info' },
  medium: { text: '中', type: 'warning' },
  high: { text: '高', type: 'danger' }
}

const statusTagText = (status) => taskStatusMap[status] || status
const statusTagType = (status) => taskStatusTagType[status] || 'info'
const priorityText = (priority) => priorityMap[priority]?.text || priority
const priorityType = (priority) => priorityMap[priority]?.type || 'info'

const canManage = computed(() => {
  if (!userStore.userInfo) return false
  if (userStore.isAdmin) return true
  return projectLeaderId.value === userStore.userInfo.id
})

const progressStatus = computed(() => {
  if (stats.value.completion_rate >= 100) return 'success'
  if (stats.value.delayed > 0) return 'exception'
  return ''
})

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

const isOverdue = (task) => {
  if (!task.deadline || task.status === 'done' || task.status === 'cancelled') return false
  return new Date(task.deadline) < new Date()
}

const fetchProject = async () => {
  try {
    const res = await getProject(projectId.value)
    if (res.code === 200) {
      const project = res.data.project
      projectName.value = project.name
      projectStatus.value = project.status
      projectLeaderId.value = project.leader_id
    }
  } catch (error) {
    console.error(error)
  }
}

const fetchTasks = async () => {
  loading.value = true
  try {
    const params = {}
    if (filterStatus.value) params.status = filterStatus.value
    const res = await getTasks(projectId.value, params)
    if (res.code === 200) {
      tasks.value = res.data.tasks || []
      stats.value = res.data.stats || { total: 0, done: 0, doing: 0, todo: 0, delayed: 0, completion_rate: 0 }
    }
  } catch (error) {
    ElMessage.error('获取任务列表失败')
  } finally {
    loading.value = false
  }
}

const openCreateDialog = () => {
  isEdit.value = false
  editingTaskId.value = null
  taskForm.title = ''
  taskForm.description = ''
  taskForm.priority = 'medium'
  taskForm.status = 'todo'
  taskForm.deadline = null
  dialogVisible.value = true
}

const openEditDialog = (task) => {
  isEdit.value = true
  editingTaskId.value = task.id
  taskForm.title = task.title
  taskForm.description = task.description || ''
  taskForm.priority = task.priority
  taskForm.status = task.status
  taskForm.deadline = task.deadline
  dialogVisible.value = true
}

const handleSubmit = async () => {
  const valid = await taskFormRef.value.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    const data = {
      title: taskForm.title,
      description: taskForm.description,
      priority: taskForm.priority,
      status: taskForm.status,
      deadline: taskForm.deadline
    }

    let res
    if (isEdit.value) {
      res = await updateTask(editingTaskId.value, data)
    } else {
      res = await createTask(projectId.value, data)
    }

    if (res.code === 200 || res.code === 201) {
      ElMessage.success(isEdit.value ? '任务更新成功' : '任务创建成功')
      dialogVisible.value = false
      fetchTasks()
    } else {
      ElMessage.error(res.message || '操作失败')
    }
  } catch (error) {
    ElMessage.error('操作失败')
  } finally {
    submitting.value = false
  }
}

const handleStatusChange = async (task, newStatus) => {
  try {
    const res = await updateTask(task.id, { status: newStatus })
    if (res.code === 200) {
      ElMessage.success('状态更新成功')
      fetchTasks()
    } else {
      ElMessage.error(res.message || '更新失败')
      task.status = task.status // 恢复原状态
    }
  } catch (error) {
    ElMessage.error('更新失败')
  }
}

const handleDelete = async (task) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除任务 "${task.title}" 吗？`,
      '删除确认',
      { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' }
    )
    const res = await deleteTask(task.id)
    if (res.code === 200) {
      ElMessage.success('任务删除成功')
      fetchTasks()
    } else {
      ElMessage.error(res.message || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  fetchProject()
  fetchTasks()
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

.project-info-card {
  margin-bottom: 20px;
}

.project-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.project-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  --stat-color: var(--text-primary);
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 16px;
  text-align: center;
  transition: all var(--transition-fast);
}

.stat-card:hover {
  border-color: var(--stat-color);
  box-shadow: var(--shadow-sm);
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--stat-color);
  line-height: 1;
  margin-bottom: 6px;
}

.stat-label {
  font-size: 13px;
  color: var(--text-secondary);
}

.progress-card {
  margin-bottom: 20px;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  font-size: 14px;
  color: var(--text-primary);
}

.progress-text {
  font-weight: 600;
  color: var(--primary-600);
}

.filter-card {
  margin-bottom: 20px;
}

.filter-bar {
  display: flex;
  gap: 12px;
  align-items: center;
}

.task-list-card {
  min-height: 300px;
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.task-item {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  padding: 16px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  transition: all var(--transition-fast);
}

.task-item:hover {
  border-color: var(--primary-300);
  box-shadow: var(--shadow-sm);
}

.task-done .task-title {
  text-decoration: line-through;
  color: var(--text-tertiary);
}

.task-main {
  display: flex;
  gap: 12px;
  flex: 1;
  min-width: 0;
}

.task-status-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--bg-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.task-content {
  flex: 1;
  min-width: 0;
}

.task-title-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
  flex-wrap: wrap;
}

.task-title {
  font-size: 15px;
  font-weight: 500;
  color: var(--text-primary);
}

.task-desc {
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 8px;
  line-height: 1.5;
}

.task-meta {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.task-deadline {
  font-size: 12px;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 4px;
}

.deadline-overdue {
  color: var(--danger-500);
  font-weight: 500;
}

.task-completed {
  font-size: 12px;
  color: var(--success-500);
  display: flex;
  align-items: center;
  gap: 4px;
}

.task-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}
</style>
