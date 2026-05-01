<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">比赛管理</h2>
      <el-button type="primary" @click="showAddDialog">
        <el-icon><Plus /></el-icon> 创建比赛批次
      </el-button>
    </div>

    <el-row :gutter="16" class="stats-row">
      <el-col :span="6"><div class="mini-stat"><span class="mini-value">{{ competitions.length }}</span><span class="mini-label">全部批次</span></div></el-col>
      <el-col :span="6"><div class="mini-stat primary"><span class="mini-value">{{ activeCount }}</span><span class="mini-label">进行中</span></div></el-col>
      <el-col :span="6"><div class="mini-stat success"><span class="mini-value">{{ finishedCount }}</span><span class="mini-label">已完成</span></div></el-col>
      <el-col :span="6"><div class="mini-stat warning"><span class="mini-value">{{ totalRegistrations }}</span><span class="mini-label">总报名数</span></div></el-col>
    </el-row>

    <el-card shadow="never">
      <el-table :data="competitions" stripe style="width:100%">
        <el-table-column prop="name" label="比赛名称" min-width="200">
          <template #default="{ row }"><strong>{{ row.name }}</strong></template>
        </el-table-column>
        <el-table-column prop="year" label="届次" width="70" align="center" />
        <el-table-column prop="registration_start" label="报名开始" width="120">
          <template #default="{ row }">{{ formatDate(row.registration_start) }}</template>
        </el-table-column>
        <el-table-column prop="registration_end" label="报名截止" width="120">
          <template #default="{ row }">{{ formatDate(row.registration_end) }}</template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="compStatusType(row.status)" size="small">{{ compStatusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="registrations_count" label="报名数" width="80" align="center" />
        <el-table-column label="操作" width="240" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="$router.push(`/competitions/${row.id}`)">查看详情</el-button>
            <el-button type="success" link size="small" @click="editComp(row)">编辑</el-button>
            <el-button type="warning" link size="small" @click="toggleCompStatus(row)">
              {{ row.status === 'active' ? '停用' : '启用' }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 创建/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="editingComp ? '编辑比赛批次' : '创建比赛批次'" width="560px" destroy-on-close>
      <el-form :model="compForm" label-width="110px">
        <el-form-item label="比赛名称" required>
          <el-input v-model="compForm.name" placeholder="如：第十届全国大学生创新创业大赛" />
        </el-form-item>
        <el-form-item label="届次" required>
          <el-input-number v-model="compForm.year" :min="1" :max="99" />
        </el-form-item>
        <el-form-item label="报名时间" required>
          <el-date-picker v-model="compForm.dateRange" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="截止日期" style="width:100%" />
        </el-form-item>
        <el-form-item label="比赛时间">
          <el-date-picker v-model="compForm.compDateRange" type="daterange" range-separator="至" start-placeholder="开始" end-placeholder="结束" style="width:100%" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="compForm.description" type="textarea" :rows="3" placeholder="比赛简介..." />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="compForm.isActive" active-text="启用" inactive-text="停用" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveComp">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const dialogVisible = ref(false)
const editingComp = ref(null)

const compForm = reactive({ name: '', year: new Date().getFullYear(), dateRange: null, compDateRange: null, description: '', isActive: true })

const competitions = ref([
  { id: 1, name: '第十届全国大学生创新创业大赛', year: 10, registration_start: '2025-03-01', registration_end: '2025-04-15', competition_start: '2025-05-01', competition_end: '2025-06-15', status: 'active', registrations_count: 156, description: '面向全国高校学生的创新创业竞赛' },
  { id: 2, name: '第九届大学生创新创业大赛（往届）', year: 9, registration_start: '2024-03-01', registration_end: '2024-04-30', competition_start: '2024-05-15', competition_end: '2024-06-30', status: 'finished', registrations_count: 248, description: '第九届创新创业大赛，已结束' },
  { id: 3, name: '校级创新创业选拔赛', year: 11, registration_start: '2025-05-01', registration_end: '2025-06-01', competition_start: '2025-06-15', competition_end: '2025-07-15', status: 'upcoming', registrations_count: 32, description: '校内选拔赛，优胜者推荐参加国赛' }
])

const activeCount = computed(() => competitions.value.filter(c => c.status === 'active').length)
const finishedCount = computed(() => competitions.value.filter(c => c.status === 'finished').length)
const totalRegistrations = computed(() => competitions.value.reduce((sum, c) => sum + c.registrations_count, 0))

const compStatusMap = { upcoming: { text: '未开始', type: 'info' }, active: { text: '进行中', type: 'success' }, paused: { text: '已暂停', type: 'warning' }, finished: { text: '已结束', type: 'danger' } }
const compStatusText = (s) => compStatusMap[s]?.text || s
const compStatusType = (s) => compStatusMap[s]?.type || 'info'

function formatDate(d) { return d ? new Date(d).toLocaleDateString('zh-CN') : '-' }

function showAddDialog() {
  editingComp.value = null
  Object.assign(compForm, { name: '', year: new Date().getFullYear(), dateRange: null, compDateRange: null, description: '', isActive: true })
  dialogVisible.value = true
}

function editComp(comp) {
  editingComp.value = comp
  Object.assign(compForm, {
    name: comp.name,
    year: comp.year,
    dateRange: [comp.registration_start, comp.registration_end],
    compDateRange: [comp.competition_start, comp.competition_end],
    description: comp.description || '',
    isActive: comp.status === 'active'
  })
  dialogVisible.value = true
}

function saveComp() {
  if (!compForm.name) { ElMessage.warning('请填写比赛名称'); return }
  if (editingComp.value) {
    Object.assign(editingComp.value, { name: compForm.name, year: compForm.year, status: compForm.isActive ? 'active' : 'paused', description: compForm.description })
    ElMessage.success('比赛信息已更新')
  } else {
    competitions.value.unshift({
      id: competitions.value.length + 1,
      name: compForm.name,
      year: compForm.year,
      registration_start: compForm.dateRange?.[0] || '-',
      registration_end: compForm.dateRange?.[1] || '-',
      competition_start: compForm.compDateRange?.[0] || '-',
      competition_end: compForm.compDateRange?.[1] || '-',
      status: compForm.isActive ? 'active' : 'paused',
      registrations_count: 0,
      description: compForm.description
    })
    ElMessage.success('比赛批次创建成功')
  }
  dialogVisible.value = false
}

function toggleCompStatus(comp) {
  comp.status = comp.status === 'active' ? 'paused' : 'active'
  ElMessage.success(`已${comp.status === 'active' ? '启用' : '停用'}「${comp.name}」`)
}
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
</style>
