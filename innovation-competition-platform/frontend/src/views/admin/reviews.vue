<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">评审管理</h2>
    </div>

    <el-row :gutter="16" class="stats-row">
      <el-col :span="6"><div class="mini-stat"><span class="mini-value">{{ reviews.length }}</span><span class="mini-label">评审总数</span></div></el-col>
      <el-col :span="6"><div class="mini-stat primary"><span class="mini-value">{{ projectCount }}</span><span class="mini-label">已评审项目</span></div></el-col>
      <el-col :span="6"><div class="mini-stat success"><span class="mini-value">{{ avgScore }}</span><span class="mini-label">平均分</span></div></el-col>
      <el-col :span="6"><div class="mini-stat warning"><span class="mini-value">{{ judgeCount }}</span><span class="mini-label">参评评委</span></div></el-col>
    </el-row>

    <el-card shadow="never" v-loading="loading">
      <div class="toolbar">
        <el-input v-model="searchQuery" placeholder="搜索项目名称..." clearable style="width:260px" prefix-icon="Search" />
        <el-select v-model="filterJudge" placeholder="评委筛选" clearable style="width:140px">
          <el-option v-for="j in judgeList" :key="j" :label="j" :value="j" />
        </el-select>
      </div>

      <el-table :data="filteredReviews" stripe style="width:100%">
        <el-table-column prop="id" label="ID" width="55" align="center" />
        <el-table-column label="项目名称" min-width="180">
          <template #default="{ row }">
            <span class="project-link" @click="$router.push(`/projects/${row.project_id}`)">{{ row.project?.name || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column label="评委" width="100">
          <template #default="{ row }">{{ row.judge_name || '-' }}</template>
        </el-table-column>
        <el-table-column prop="total_score" label="总分" width="80" align="center">
          <template #default="{ row }">
            <span :class="{ 'score-high': row.total_score >= 85, 'score-mid': row.total_score >= 70 && row.total_score < 85, 'score-low': row.total_score < 70 }">
              {{ row.total_score ? row.total_score.toFixed(0) : '-' }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="innovation_score" label="创新" width="60" align="center" />
        <el-table-column prop="feasibility_score" label="可行" width="60" align="center" />
        <el-table-column prop="market_score" label="市场" width="60" align="center" />
        <el-table-column prop="team_score" label="团队" width="60" align="center" />
        <el-table-column prop="comment" label="评语" min-width="200" show-overflow-tooltip />
        <el-table-column prop="created_at" label="评审时间" width="140">
          <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getAllReviews } from '@/api/review'

const loading = ref(false)
const searchQuery = ref('')
const filterJudge = ref('')
const reviews = ref([])

const filteredReviews = computed(() => {
  let list = reviews.value
  if (filterJudge.value) list = list.filter(r => r.judge_name === filterJudge.value)
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(r => (r.project?.name || '').toLowerCase().includes(q))
  }
  return list
})

const projectCount = computed(() => {
  const ids = new Set(reviews.value.map(r => r.project_id))
  return ids.size
})

const avgScore = computed(() => {
  const scored = reviews.value.filter(r => r.total_score != null)
  if (!scored.length) return '-'
  return (scored.reduce((s, r) => s + r.total_score, 0) / scored.length).toFixed(1)
})

const judgeCount = computed(() => {
  const ids = new Set(reviews.value.map(r => r.judge_id))
  return ids.size
})

const judgeList = computed(() => {
  return [...new Set(reviews.value.map(r => r.judge_name).filter(Boolean))]
})

function formatDate(d) {
  if (!d) return '-'
  return new Date(d).toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
}

async function fetchReviews() {
  loading.value = true
  try {
    const res = await getAllReviews()
    if (res.code === 200) {
      reviews.value = res.data?.reviews || []
    }
  } catch (e) {
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
.page-container { padding-bottom: 20px; }

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
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
.mini-stat.success { border-color: var(--success-200); background: var(--success-50); }
.mini-stat.warning { border-color: var(--warning-200); background: var(--warning-50); }

.mini-value { font-size: 22px; font-weight: 700; color: var(--text-primary); }
.mini-label { font-size: 12px; color: var(--text-secondary); }

.toolbar {
  display: flex;
  gap: 10px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.project-link {
  cursor: pointer;
  color: var(--primary-600);
  font-weight: 600;
}
.project-link:hover { text-decoration: underline; }

.score-high { color: #67C23A; font-weight: 700; }
.score-mid { color: #E6A23C; font-weight: 600; }
.score-low { color: #F56C6C; font-weight: 600; }
</style>
