<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">项目管理</h2>
      <div class="header-actions">
        <el-input v-model="searchQuery" placeholder="搜索项目名称..." clearable style="width:240px" prefix-icon="Search" />
        <el-select v-model="filterStage" placeholder="阶段筛选" clearable style="width:130px">
          <el-option label="创意阶段" value="idea" /><el-option label="验证阶段" value="proof" />
          <el-option label="资源整合" value="resource" /><el-option label="产品开发" value="development" />
          <el-option label="市场推广" value="market" /><el-option label="路演展示" value="roadshow" />
        </el-select>
        <el-select v-model="filterStatus" placeholder="状态筛选" clearable style="width:130px">
          <el-option label="草稿" value="draft" /><el-option label="已提交" value="submitted" />
          <el-option label="审核中" value="teacher_review" /><el-option label="评审中" value="judging" />
          <el-option label="已通过" value="passed" /><el-option label="需修改" value="need_modify" />
        </el-select>
      </div>
    </div>

    <el-row :gutter="16" class="stats-row">
      <el-col :span="4"><div class="mini-stat"><span class="mini-value">{{ filteredProjects.length }}</span><span class="mini-label">全部</span></div></el-col>
      <el-col :span="4"><div class="mini-stat primary"><span class="mini-value">{{ submittedCount }}</span><span class="mini-label">待审核</span></div></el-col>
      <el-col :span="4"><div class="mini-stat warning"><span class="mini-value">{{ judgingCount }}</span><span class="mini-label">评审中</span></div></el-col>
      <el-col :span="4"><div class="mini-stat success"><span class="mini-value">{{ passedCount }}</span><span class="mini-label">已通过</span></div></el-col>
      <el-col :span="4"><div class="mini-stat danger"><span class="mini-value">{{ rejectedCount }}</span><span class="mini-label">已驳回</span></div></el-col>
      <el-col :span="4"><div class="mini-stat info"><span class="mini-value">{{ avgScore }}</span><span class="mini-label">平均分</span></div></el-col>
    </el-row>

    <el-card shadow="never" v-loading="loading">
      <el-table :data="paginatedProjects" stripe style="width:100%">
        <el-table-column prop="id" label="ID" width="55" align="center" />
        <el-table-column prop="name" label="项目名称" min-width="180">
          <template #default="{ row }">
            <span class="project-link" @click="$router.push(`/projects/${row.id}`)">{{ row.name }}</span>
          </template>
        </el-table-column>
        <el-table-column label="负责人" width="90">
          <template #default="{ row }">{{ row.leader_name || row.leader?.real_name || '-' }}</template>
        </el-table-column>
        <el-table-column prop="category" label="类别" width="110" />
        <el-table-column prop="track" label="赛道" width="100" />
        <el-table-column prop="stage" label="阶段" width="95">
          <template #default="{ row }"><el-tag size="small" type="info">{{ stageText(row.stage) }}</el-tag></template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="105">
          <template #default="{ row }"><el-tag :type="statusType(row.status)" size="small">{{ statusText(row.status) }}</el-tag></template>
        </el-table-column>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="$router.push(`/projects/${row.id}`)">详情</el-button>
            <el-button type="danger" link size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrap">
        <el-pagination v-model:current-page="currentPage" v-model:page-size="pageSize" :total="filteredProjects.length" layout="total, sizes, prev, pager, next" :page-sizes="[10, 20, 50]" />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getProjects, deleteProject } from '@/api/project'

const loading = ref(false)
const searchQuery = ref('')
const filterStage = ref('')
const filterStatus = ref('')
const currentPage = ref(1)
const pageSize = ref(10)

const projects = ref([])

const filteredProjects = computed(() => {
  let list = projects.value
  if (filterStage.value) list = list.filter(p => p.stage === filterStage.value)
  if (filterStatus.value) list = list.filter(p => p.status === filterStatus.value)
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(p => (p.name || '').toLowerCase().includes(q))
  }
  return list
})

const paginatedProjects = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return filteredProjects.value.slice(start, start + pageSize.value)
})

const submittedCount = computed(() => filteredProjects.value.filter(p => ['submitted', 'teacher_review'].includes(p.status)).length)
const judgingCount = computed(() => filteredProjects.value.filter(p => p.status === 'judging').length)
const passedCount = computed(() => filteredProjects.value.filter(p => p.status === 'passed').length)
const rejectedCount = computed(() => filteredProjects.value.filter(p => ['rejected', 'need_modify'].includes(p.status)).length)
const avgScore = computed(() => {
  const scored = filteredProjects.value.filter(p => p.avg_score != null)
  if (!scored.length) return '-'
  return Math.round(scored.reduce((s, p) => s + p.avg_score, 0) / scored.length)
})

const statusMap = { draft: { text: '草稿', type: 'info' }, submitted: { text: '已提交', type: 'primary' }, teacher_review: { text: '审核中', type: 'warning' }, judging: { text: '评审中', type: 'warning' }, passed: { text: '已通过', type: 'success' }, need_modify: { text: '需修改', type: 'danger' }, rejected: { text: '已驳回', type: 'danger' } }
const stageMap = { idea: '创意阶段', proof: '验证阶段', resource: '资源整合', development: '产品开发', market: '市场推广', roadshow: '路演展示', incubation: '孵化运营' }
const statusText = (s) => statusMap[s]?.text || s
const statusType = (s) => statusMap[s]?.type || 'info'
const stageText = (s) => stageMap[s] || s

async function fetchProjects() {
  loading.value = true
  try {
    const res = await getProjects()
    if (res.code === 200) {
      projects.value = res.data?.projects || []
    }
  } catch (e) {
    ElMessage.error('获取项目列表失败')
  } finally {
    loading.value = false
  }
}

async function handleDelete(project) {
  await ElMessageBox.confirm(`确定要删除项目「${project.name}」吗？此操作不可恢复！`, '危险操作', { type: 'warning' })
  try {
    const res = await deleteProject(project.id)
    if (res.code === 200) {
      ElMessage.success('项目已删除')
      fetchProjects()
    } else {
      ElMessage.error(res.message || '删除失败')
    }
  } catch (e) {
    ElMessage.error('删除失败')
  }
}

onMounted(() => {
  fetchProjects()
})
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
  flex-wrap: wrap;
}

.stats-row { margin-bottom: 16px; }

.mini-stat {
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 14px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}
.mini-stat.primary { border-color: var(--primary-200); background: var(--primary-50); }
.mini-stat.warning { border-color: var(--warning-200); background: var(--warning-50); }
.mini-stat.success { border-color: var(--success-200); background: var(--success-50); }
.mini-stat.danger { border-color: var(--danger-200); background: var(--danger-50); }
.mini-stat.info { border-color: var(--info-200); background: var(--info-50); }

.mini-value { font-size: 22px; font-weight: 700; color: var(--text-primary); }
.mini-label { font-size: 12px; color: var(--text-secondary); }

.project-link {
  cursor: pointer;
  color: var(--primary-600);
  font-weight: 600;
  transition: color 0.2s;
}
.project-link:hover { color: var(--primary-400); text-decoration: underline; }

.pagination-wrap { display: flex; justify-content: flex-end; margin-top: 16px; }
</style>
