<template>
  <div class="page-container">
    <!-- 顶部统计 -->
    <div class="stats-header">
      <div class="stats-content">
        <div class="stat-item">
          <el-icon size="28" color="#0ea5e9"><FolderOpened /></el-icon>
          <div class="stat-info">
            <div class="stat-value">{{ stats.total }}</div>
            <div class="stat-label">项目总数</div>
          </div>
        </div>
        <div class="stat-item">
          <el-icon size="28" color="#f59e0b"><Timer /></el-icon>
          <div class="stat-info">
            <div class="stat-value">{{ stats.inProgress }}</div>
            <div class="stat-label">进行中</div>
          </div>
        </div>
        <div class="stat-item">
          <el-icon size="28" color="#10b981"><CircleCheck /></el-icon>
          <div class="stat-info">
            <div class="stat-value">{{ stats.completed }}</div>
            <div class="stat-label">已完成</div>
          </div>
        </div>
        <div class="stat-item">
          <el-icon size="28" color="#8b5cf6"><Medal /></el-icon>
          <div class="stat-info">
            <div class="stat-value">{{ stats.registered }}</div>
            <div class="stat-label">已报名</div>
          </div>
        </div>
      </div>
      <el-button type="primary" :icon="Plus" size="large" @click="$router.push('/create-project')">
        创建项目
      </el-button>
    </div>

    <!-- 搜索和筛选 -->
    <el-card class="filter-card" shadow="never">
      <div class="filter-row">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索项目名称"
          clearable
          style="width: 280px"
          @keyup.enter="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>

        <el-select v-model="filterStatus" placeholder="项目状态" clearable style="width: 160px" @change="handleSearch">
          <el-option label="草稿" value="draft" />
          <el-option label="已提交" value="submitted" />
          <el-option label="审核中" value="teacher_review" />
          <el-option label="评审中" value="judging" />
          <el-option label="已通过" value="passed" />
          <el-option label="需修改" value="need_modify" />
          <el-option label="已驳回" value="rejected" />
        </el-select>

        <el-select v-model="filterStage" placeholder="项目阶段" clearable style="width: 160px" @change="handleSearch">
          <el-option label="创意阶段" value="idea" />
          <el-option label="验证阶段" value="proof" />
          <el-option label="资源整合" value="resource" />
          <el-option label="产品开发" value="development" />
          <el-option label="市场推广" value="market" />
          <el-option label="路演展示" value="roadshow" />
          <el-option label="孵化运营" value="incubation" />
        </el-select>

        <el-select v-model="filterCompetition" placeholder="关联竞赛" clearable style="width: 200px" @change="handleSearch">
          <el-option
            v-for="comp in competitions"
            :key="comp.id"
            :label="comp.name"
            :value="comp.id"
          />
        </el-select>

        <el-button type="primary" plain @click="handleSearch">查询</el-button>
        <el-button @click="resetFilter">重置</el-button>
      </div>
    </el-card>

    <!-- 项目列表 -->
    <el-card class="list-card" shadow="never" v-loading="loading">
      <el-empty v-if="projects.length === 0" description="暂无项目">
        <el-button type="primary" @click="$router.push('/create-project')">
          创建第一个项目
        </el-button>
      </el-empty>

      <div v-else class="project-list">
        <div
          v-for="project in projects"
          :key="project.id"
          class="project-card"
          @click="goToDetail(project.id)"
        >
          <div class="project-main">
            <div class="project-header">
              <h3 class="project-name">{{ project.name }}</h3>
              <div class="project-badges">
                <el-tag :type="statusType(project.status)" size="small">
                  {{ statusText(project.status) }}
                </el-tag>
                <el-tag size="small" class="stage-tag">
                  {{ stageText(project.stage) }}
                </el-tag>
              </div>
            </div>

            <p class="project-desc">{{ project.description || '暂无描述' }}</p>

            <div class="project-meta">
              <div class="meta-item">
                <el-icon><CollectionTag /></el-icon>
                <span>{{ project.track || '未分类' }}</span>
              </div>
              <div class="meta-item">
                <el-icon><Trophy /></el-icon>
                <span>{{ project.competition?.name || '未关联竞赛' }}</span>
              </div>
              <div class="meta-item">
                <el-icon><User /></el-icon>
                <span>{{ project.member_count || 1 }} 名成员</span>
              </div>
              <div class="meta-item">
                <el-icon><Document /></el-icon>
                <span>{{ project.file_count || 0 }} 份材料</span>
              </div>
            </div>

            <!-- 进度条 -->
            <div class="project-progress" v-if="project.progress !== undefined">
              <div class="progress-header">
                <span class="progress-label">项目进度</span>
                <span class="progress-value">{{ project.progress }}%</span>
              </div>
              <el-progress
                :percentage="project.progress"
                :status="project.progress === 100 ? 'success' : ''"
                :stroke-width="8"
                :show-text="false"
              />
            </div>
          </div>

          <div class="project-sidebar">
            <div class="sidebar-section">
              <span class="sidebar-label">负责人</span>
              <span class="sidebar-value">{{ project.leader?.real_name || project.leader?.username || '-' }}</span>
            </div>
            <div class="sidebar-section">
              <span class="sidebar-label">更新时间</span>
              <span class="sidebar-value">{{ formatDate(project.updated_at) }}</span>
            </div>
            <div class="sidebar-section">
              <span class="sidebar-label">创建时间</span>
              <span class="sidebar-value">{{ formatDate(project.created_at) }}</span>
            </div>
            <div class="sidebar-actions" @click.stop>
              <el-button
                v-if="project.status === 'draft' || project.status === 'need_modify'"
                type="primary"
                size="small"
                @click="handleSubmit(project)"
              >
                提交评审
              </el-button>
              <el-button
                type="primary"
                size="small"
                plain
                @click="goToDetail(project.id)"
              >
                查看详情
              </el-button>
            </div>
          </div>
        </div>
      </div>

      <!-- 分页 -->
      <div class="pagination-wrapper" v-if="total > 0">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          layout="total, prev, pager, next"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  Plus, Search, CollectionTag, Timer, User,
  FolderOpened, CircleCheck, Medal, Document, Trophy
} from '@element-plus/icons-vue'
import { getProjects, submitProject } from '@/api/project'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()

const loading = ref(false)
const projects = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

const searchKeyword = ref('')
const filterStatus = ref('')
const filterStage = ref('')
const filterCompetition = ref('')

const competitions = ref([
  { id: 1, name: '2026 大学生创新创业计划训练赛' },
  { id: 2, name: '2026 AI 应用创新设计大赛' },
  { id: 3, name: '2026 数字经济与商业模式创新挑战赛' }
])

const stats = ref({
  total: 0,
  inProgress: 0,
  completed: 0,
  registered: 0
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

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}

const fetchProjects = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      per_page: pageSize.value,
      keyword: searchKeyword.value,
      status: filterStatus.value,
      stage: filterStage.value,
      competition_id: filterCompetition.value
    }
    const res = await getProjects(params)
    if (res.code === 200) {
      projects.value = res.data.projects || []
      total.value = res.data.total || 0

      // 更新统计
      stats.value = {
        total: res.data.total || 0,
        inProgress: projects.value.filter(p => ['draft', 'submitted', 'teacher_review', 'judging'].includes(p.status)).length,
        completed: projects.value.filter(p => p.status === 'passed').length,
        registered: projects.value.filter(p => p.competition_id).length
      }
    }
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchProjects()
}

const resetFilter = () => {
  searchKeyword.value = ''
  filterStatus.value = ''
  filterStage.value = ''
  filterCompetition.value = ''
  currentPage.value = 1
  fetchProjects()
}

const handlePageChange = () => {
  fetchProjects()
}

const goToDetail = (id) => {
  router.push(`/projects/${id}`)
}

const handleSubmit = async (project) => {
  try {
    await ElMessageBox.confirm(
      `确定要提交项目 "${project.name}" 进入评审吗？`,
      '提交确认',
      { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' }
    )
    const res = await submitProject(project.id)
    if (res.code === 200) {
      ElMessage.success('项目提交成功')
      fetchProjects()
    } else {
      ElMessage.error(res.message || '提交失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      const message = error.response?.data?.message || '提交失败'
      ElMessage.error(message)
    }
  }
}

onMounted(() => {
  fetchProjects()
})
</script>

<style scoped>
.page-container {
  padding-bottom: 20px;
}

/* 统计头部 */
.stats-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 20px 24px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
}

.stats-content {
  display: flex;
  gap: 40px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1;
}

.stat-label {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: 4px;
}

.filter-card {
  margin-bottom: 20px;
}

.filter-row {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}

.list-card {
  min-height: 400px;
}

.project-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.project-card {
  display: flex;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  overflow: hidden;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.project-card:hover {
  border-color: var(--primary-300);
  box-shadow: var(--shadow-md);
}

.project-main {
  flex: 1;
  padding: 20px;
}

.project-sidebar {
  width: 200px;
  padding: 20px;
  background: var(--bg-secondary);
  border-left: 1px solid var(--border-light);
  display: flex;
  flex-direction: column;
  gap: 12px;
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
  margin: 0;
}

.project-badges {
  display: flex;
  gap: 8px;
}

.stage-tag {
  background-color: #f1f5f9;
  color: #475569;
  border: none;
}

.project-desc {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 16px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.project-meta {
  display: flex;
  gap: 20px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--text-secondary);
}

/* 进度条 */
.project-progress {
  margin-top: 12px;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 6px;
}

.progress-label {
  font-size: 13px;
  color: var(--text-secondary);
}

.progress-value {
  font-size: 13px;
  font-weight: 600;
  color: var(--primary-600);
}

/* 侧边栏 */
.sidebar-section {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.sidebar-label {
  font-size: 12px;
  color: var(--text-tertiary);
}

.sidebar-value {
  font-size: 13px;
  color: var(--text-primary);
  font-weight: 500;
}

.sidebar-actions {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid var(--border-light);
}

@media (max-width: 768px) {
  .stats-header {
    flex-direction: column;
    gap: 16px;
  }

  .stats-content {
    flex-wrap: wrap;
    gap: 20px;
  }

  .project-card {
    flex-direction: column;
  }

  .project-sidebar {
    width: 100%;
    border-left: none;
    border-top: 1px solid var(--border-light);
  }
}
</style>
