<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">我的项目</h2>
      <el-button type="primary" :icon="Plus" @click="$router.push('/create-project')">
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

        <el-button type="primary" plain @click="handleSearch">查询</el-button>
        <el-button @click="resetFilter">重置</el-button>
      </div>
    </el-card>

    <!-- 项目列表 -->
    <el-card class="list-card" shadow="never" v-loading="loading">
      <el-empty v-if="projects.length === 0" description="暂无项目" />

      <div v-else class="project-list">
        <div
          v-for="project in projects"
          :key="project.id"
          class="project-card"
          @click="goToDetail(project.id)"
        >
          <div class="project-header">
            <h3 class="project-name">{{ project.name }}</h3>
            <el-tag :type="statusType(project.status)" size="small">
              {{ statusText(project.status) }}
            </el-tag>
          </div>

          <p class="project-desc">{{ project.description || '暂无描述' }}</p>

          <div class="project-meta">
            <div class="meta-item">
              <el-icon><CollectionTag /></el-icon>
              <span>{{ project.track || '未分类' }}</span>
            </div>
            <div class="meta-item">
              <el-icon><Timer /></el-icon>
              <span>{{ stageText(project.stage) }}</span>
            </div>
            <div class="meta-item">
              <el-icon><User /></el-icon>
              <span>负责人: {{ project.leader?.real_name || project.leader?.username || '-' }}</span>
            </div>
          </div>

          <div class="project-footer">
            <span class="update-time">更新于 {{ formatDate(project.updated_at) }}</span>
            <div class="project-actions" @click.stop>
              <el-button
                v-if="project.status === 'draft' || project.status === 'need_modify'"
                type="primary"
                link
                size="small"
                @click="handleSubmit(project)"
              >
                提交评审
              </el-button>
              <el-button type="primary" link size="small" @click="goToDetail(project.id)">
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
import { Plus, Search, CollectionTag, Timer, User } from '@element-plus/icons-vue'
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
      stage: filterStage.value
    }
    const res = await getProjects(params)
    if (res.code === 200) {
      projects.value = res.data.projects || []
      total.value = res.data.total || 0
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
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 20px;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.project-card:hover {
  border-color: var(--primary-300);
  box-shadow: var(--shadow-md);
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
  gap: 24px;
  margin-bottom: 16px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--text-secondary);
}

.project-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid var(--border-light);
}

.update-time {
  font-size: 12px;
  color: var(--text-tertiary);
}

.project-actions {
  display: flex;
  gap: 8px;
}

.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid var(--border-light);
}
</style>
