<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">指导项目</h2>
      <div class="header-actions">
        <el-input v-model="searchQuery" placeholder="搜索项目名称..." clearable style="width:240px" prefix-icon="Search">
          <template #prefix><el-icon><Search /></el-icon></template>
        </el-input>
        <el-select v-model="filterStatus" placeholder="状态筛选" clearable style="width:140px">
          <el-option label="已提交" value="submitted" />
          <el-option label="审核中" value="teacher_review" />
          <el-option label="评审中" value="judging" />
          <el-option label="已通过" value="passed" />
          <el-option label="需修改" value="need_modify" />
        </el-select>
      </div>
    </div>

    <el-row :gutter="16" class="stats-row">
      <el-col :span="6">
        <div class="mini-stat">
          <span class="mini-value">{{ filteredProjects.length }}</span>
          <span class="mini-label">全部项目</span>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="mini-stat primary">
          <span class="mini-value">{{ pendingCount }}</span>
          <span class="mini-label">待审核</span>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="mini-stat success">
          <span class="mini-value">{{ passedCount }}</span>
          <span class="mini-label">已通过</span>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="mini-stat warning">
          <span class="mini-value">{{ modifyCount }}</span>
          <span class="mini-label">需修改</span>
        </div>
      </el-col>
    </el-row>

    <el-card shadow="never" class="project-table-card">
      <el-table :data="filteredProjects" stripe style="width:100%">
        <el-table-column prop="name" label="项目名称" min-width="180">
          <template #default="{ row }">
            <span class="project-link" @click="$router.push(`/projects/${row.id}`)">{{ row.name }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="leader" label="负责人" width="100" />
        <el-table-column prop="category" label="类别" width="120" />
        <el-table-column prop="stage" label="阶段" width="100">
          <template #default="{ row }"><el-tag size="small" type="info">{{ stageText(row.stage) }}</el-tag></template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="110">
          <template #default="{ row }">
            <el-tag :type="statusType(row.status)" size="small">{{ statusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="members_count" label="成员数" width="80" align="center" />
        <el-table-column prop="updated_at" label="最后更新" width="140">
          <template #default="{ row }">{{ formatDate(row.updated_at) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="$router.push(`/projects/${row.id}`)">查看详情</el-button>
            <el-button type="success" link size="small" @click="openReviewDialog(row)">审核</el-button>
            <el-button type="warning" link size="small" @click="openFeedbackDialog(row)">反馈</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 审核弹窗 -->
    <el-dialog v-model="reviewVisible" title="项目审核" width="520px" destroy-on-close>
      <template v-if="currentProject">
        <el-descriptions :column="1" border class="mb-4">
          <el-descriptions-item label="项目名称">{{ currentProject.name }}</el-descriptions-item>
          <el-descriptions-item label="负责人">{{ currentProject.leader }}</el-descriptions-item>
          <el-descriptions-item label="当前状态">{{ statusText(currentProject.status) }}</el-descriptions-item>
        </el-descriptions>
        <el-form :model="reviewForm" label-width="90px">
          <el-form-item label="审核结果">
            <el-radio-group v-model="reviewForm.result">
              <el-radio value="passed">通过</el-radio>
              <el-radio value="need_modify">需修改</el-radio>
              <el-radio value="rejected">驳回</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="审核意见">
            <el-input v-model="reviewForm.comment" type="textarea" :rows="4" placeholder="请输入审核意见..." maxlength="500" show-word-limit />
          </el-form-item>
        </el-form>
      </template>
      <template #footer>
        <el-button @click="reviewVisible = false">取消</el-button>
        <el-button type="primary" @click="submitReview">提交审核</el-button>
      </template>
    </el-dialog>

    <!-- 反馈弹窗 -->
    <el-dialog v-model="feedbackVisible" title="指导意见" width="480px" destroy-on-close>
      <template v-if="currentProject">
        <p style="margin-bottom:16px;color:#606266;">为「{{ currentProject.name }}」提供指导意见：</p>
        <el-form :model="feedbackForm" label-position="top">
          <el-form-item label="改进建议">
            <el-input v-model="feedbackForm.suggestion" type="textarea" :rows="3" placeholder="针对项目的改进方向提出建议..." />
          </el-form-item>
          <el-form-item label="推荐资源">
            <el-checkbox-group v-model="feedbackForm.resources">
              <el-checkbox label="创新基础训练营" value="camp1" />
              <el-checkbox label="商业计划书写作营" value="camp2" />
              <el-checkbox label="路演表达训练营" value="camp3" />
              <el-checkbox label="AI 项目孵化训练营" value="camp4" />
              <el-checkbox label="创业基础课程" value="course1" />
              <el-checkbox label="市场调研方法课程" value="course2" />
            </el-checkbox-group>
          </el-form-item>
        </el-form>
      </template>
      <template #footer>
        <el-button @click="feedbackVisible = false">取消</el-button>
        <el-button type="primary" @click="submitFeedback">发送反馈</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { Search } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const searchQuery = ref('')
const filterStatus = ref('')
const reviewVisible = ref(false)
const feedbackVisible = ref(false)
const currentProject = ref(null)

const reviewForm = reactive({ result: 'passed', comment: '' })
const feedbackForm = reactive({ suggestion: '', resources: [] })

const projects = ref([
  { id: 1, name: '智慧校园服务平台', leader: '张三', category: '信息技术', stage: 'development', status: 'submitted', members_count: 4, updated_at: '2025-05-01' },
  { id: 2, name: 'AI 辅助学习系统', leader: '李四', category: '人工智能', stage: 'proof', status: 'teacher_review', members_count: 3, updated_at: '2025-04-30' },
  { id: 3, name: '绿色物流配送平台', leader: '王五', category: '绿色科技', stage: 'market', status: 'passed', members_count: 5, updated_at: '2025-04-28' },
  { id: 4, name: '乡村振兴电商助农', leader: '赵六', category: '乡村振兴', stage: 'resource', status: 'submitted', members_count: 4, updated_at: '2025-04-27' },
  { id: 5, name: '智能健康监测手环', leader: '钱七', category: '医疗健康', stage: 'idea', status: 'need_modify', members_count: 3, updated_at: '2025-04-25' },
  { id: 6, name: '校园二手交易平台', leader: '孙八', category: '校园服务', stage: 'roadshow', status: 'judging', members_count: 2, updated_at: '2025-04-24' },
  { id: 7, name: '非遗文化数字化传播', leader: '周九', category: '文化创意', stage: 'development', status: 'submitted', members_count: 6, updated_at: '2025-04-22' },
  { id: 8, name: '社区养老服务平台', leader: '吴十', category: '社会公益', stage: 'proof', status: 'submitted', members_count: 4, updated_at: '2025-04-20' }
])

const filteredProjects = computed(() => {
  let list = projects.value
  if (filterStatus.value) {
    list = list.filter(p => p.status === filterStatus.value)
  }
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(p => p.name.toLowerCase().includes(q))
  }
  return list
})

const pendingCount = computed(() => projects.value.filter(p => ['submitted', 'teacher_review'].includes(p.status)).length)
const passedCount = computed(() => projects.value.filter(p => p.status === 'passed').length)
const modifyCount = computed(() => projects.value.filter(p => p.status === 'need_modify').length)

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
  idea: '创意阶段', proof: '验证阶段', resource: '资源整合',
  development: '产品开发', market: '市场推广', roadshow: '路演展示', incubation: '孵化运营'
}

const statusText = (s) => statusMap[s]?.text || s
const statusType = (s) => statusMap[s]?.type || 'info'
const stageText = (s) => stageMap[s] || s

const formatDate = (d) => d ? new Date(d).toLocaleDateString('zh-CN') : '-'

function openReviewDialog(project) {
  currentProject.value = project
  reviewForm.result = 'passed'
  reviewForm.comment = ''
  reviewVisible.value = true
}

function openFeedbackDialog(project) {
  currentProject.value = project
  feedbackForm.suggestion = ''
  feedbackForm.resources = []
  feedbackVisible.value = true
}

function submitReview() {
  ElMessage.success(`已对「${currentProject.value.name}」完成审核：${reviewForm.result === 'passed' ? '通过' : reviewForm.result === 'need_modify' ? '需修改' : '驳回'}`)
  reviewVisible.value = false
}

function submitFeedback() {
  ElMessage.success(`已向「${currentProject.value.name}」的团队发送指导意见和${feedbackForm.resources.length}项推荐资源`)
  feedbackVisible.value = false
}
</script>

<style scoped>
.page-container { padding-bottom: 20px; }

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 12px;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.stats-row { margin-bottom: 16px; }

.mini-stat {
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.mini-stat.primary { border-color: var(--primary-200); background: var(--primary-50); }
.mini-stat.success { border-color: var(--success-200); background: var(--success-50); }
.mini-stat.warning { border-color: var(--warning-200); background: var(--warning-50); }

.mini-value { font-size: 24px; font-weight: 700; color: var(--text-primary); }
.mini-label { font-size: 12px; color: var(--text-secondary); }

.project-table-card { margin-top: 0; }

.project-link {
  cursor: pointer;
  color: var(--primary-600);
  font-weight: 600;
  transition: color 0.2s;
}
.project-link:hover { color: var(--primary-400); text-decoration: underline; }

.mb-4 { margin-bottom: 16px; }
</style>
