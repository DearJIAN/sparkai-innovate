<template>
  <div class="registration-management">
    <h2 class="page-title">报名管理</h2>

    <!-- 统计卡片 -->
    <el-row :gutter="16" class="stats-row">
      <el-col :span="4">
        <div class="stat-card" style="--stat-color: #0ea5e9">
          <el-icon size="24"><Document /></el-icon>
          <div class="stat-value">{{ stats.total }}</div>
          <div class="stat-label">总报名</div>
        </div>
      </el-col>
      <el-col :span="4">
        <div class="stat-card" style="--stat-color: #f59e0b">
          <el-icon size="24"><Timer /></el-icon>
          <div class="stat-value">{{ stats.submitted }}</div>
          <div class="stat-label">待审核</div>
        </div>
      </el-col>
      <el-col :span="4">
        <div class="stat-card" style="--stat-color: #10b981">
          <el-icon size="24"><CircleCheck /></el-icon>
          <div class="stat-value">{{ stats.approved }}</div>
          <div class="stat-label">已通过</div>
        </div>
      </el-col>
      <el-col :span="4">
        <div class="stat-card" style="--stat-color: #ef4444">
          <el-icon size="24"><CircleClose /></el-icon>
          <div class="stat-value">{{ stats.rejected }}</div>
          <div class="stat-label">已驳回</div>
        </div>
      </el-col>
      <el-col :span="4">
        <div class="stat-card" style="--stat-color: #8b5cf6">
          <el-icon size="24"><EditPen /></el-icon>
          <div class="stat-value">{{ stats.draft }}</div>
          <div class="stat-label">草稿</div>
        </div>
      </el-col>
      <el-col :span="4">
        <div class="stat-card" style="--stat-color: #64748b">
          <el-icon size="24"><Trophy /></el-icon>
          <div class="stat-value">{{ competitions.length }}</div>
          <div class="stat-label">竞赛数</div>
        </div>
      </el-col>
    </el-row>

    <!-- 筛选区域 -->
    <el-card class="filter-card" shadow="never">
      <el-form :inline="true" class="filter-form">
        <el-form-item label="竞赛">
          <el-select v-model="filterCompetition" placeholder="全部竞赛" clearable style="width: 200px">
            <el-option
              v-for="comp in competitions"
              :key="comp.id"
              :label="comp.name"
              :value="comp.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="filterStatus" placeholder="全部状态" clearable style="width: 150px">
            <el-option label="草稿" value="draft" />
            <el-option label="已提交" value="submitted" />
            <el-option label="已通过" value="approved" />
            <el-option label="已驳回" value="rejected" />
            <el-option label="已撤回" value="withdrawn" />
          </el-select>
        </el-form-item>
        <el-form-item label="关键词">
          <el-input
            v-model="filterKeyword"
            placeholder="队伍名/学校"
            clearable
            style="width: 200px"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 报名列表 -->
    <el-card shadow="never">
      <el-table
        v-loading="loading"
        :data="registrations"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column label="竞赛" min-width="200">
          <template #default="{ row }">
            <span class="comp-name">{{ row.competitionName }}</span>
          </template>
        </el-table-column>
        <el-table-column label="赛道" width="120">
          <template #default="{ row }">
            <el-tag size="small">{{ row.trackName }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="队伍" min-width="150">
          <template #default="{ row }">
            <span class="team-name">{{ row.teamName }}</span>
          </template>
        </el-table-column>
        <el-table-column label="负责人" width="120">
          <template #default="{ row }">
            <span>{{ row.leaderName }}</span>
          </template>
        </el-table-column>
        <el-table-column label="学校" width="150">
          <template #default="{ row }">
            <span>{{ row.school }}</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="statusType(row.status)" size="small">
              {{ statusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="队员" width="80">
          <template #default="{ row }">
            <span>{{ row.memberCount }}人</span>
          </template>
        </el-table-column>
        <el-table-column label="材料" width="80">
          <template #default="{ row }">
            <span>{{ row.materialCount }}份</span>
          </template>
        </el-table-column>
        <el-table-column label="提交时间" width="160">
          <template #default="{ row }">
            <span>{{ row.submittedAt || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button
              v-if="row.status === 'submitted'"
              type="success"
              size="small"
              @click="handleApprove(row)"
            >
              通过
            </el-button>
            <el-button
              v-if="row.status === 'submitted'"
              type="danger"
              size="small"
              @click="handleReject(row)"
            >
              驳回
            </el-button>
            <el-button
              size="small"
              link
              @click="showDetail(row)"
            >
              详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          layout="total, prev, pager, next, jumper"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>

    <!-- 详情弹窗 -->
    <el-dialog
      v-model="detailVisible"
      title="报名详情"
      width="700px"
    >
      <el-descriptions :column="2" border v-if="selectedRegistration">
        <el-descriptions-item label="竞赛名称" :span="2">
          {{ selectedRegistration.competitionName }}
        </el-descriptions-item>
        <el-descriptions-item label="赛道">
          {{ selectedRegistration.trackName }}
        </el-descriptions-item>
        <el-descriptions-item label="报名状态">
          <el-tag :type="statusType(selectedRegistration.status)">
            {{ statusText(selectedRegistration.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="队伍名称" :span="2">
          {{ selectedRegistration.teamName }}
        </el-descriptions-item>
        <el-descriptions-item label="学校">
          {{ selectedRegistration.school }}
        </el-descriptions-item>
        <el-descriptions-item label="学院">
          {{ selectedRegistration.college }}
        </el-descriptions-item>
        <el-descriptions-item label="专业">
          {{ selectedRegistration.major }}
        </el-descriptions-item>
        <el-descriptions-item label="指导老师">
          {{ selectedRegistration.teacherName }}
        </el-descriptions-item>
        <el-descriptions-item label="联系电话">
          {{ selectedRegistration.contactPhone }}
        </el-descriptions-item>
        <el-descriptions-item label="联系邮箱">
          {{ selectedRegistration.contactEmail }}
        </el-descriptions-item>
      </el-descriptions>

      <div class="detail-section" v-if="selectedRegistration?.members?.length">
        <h4>队员信息</h4>
        <el-table :data="selectedRegistration.members" size="small" border>
          <el-table-column prop="name" label="姓名" />
          <el-table-column prop="studentNo" label="学号" />
          <el-table-column prop="college" label="学院" />
          <el-table-column prop="major" label="专业" />
          <el-table-column prop="role_in_team" label="角色" />
        </el-table>
      </div>

      <div class="detail-section" v-if="selectedRegistration?.materials?.length">
        <h4>上传材料</h4>
        <el-table :data="selectedRegistration.materials" size="small" border>
          <el-table-column prop="material_type" label="材料类型" />
          <el-table-column prop="original_name" label="文件名" />
          <el-table-column prop="file_size" label="大小" />
        </el-table>
      </div>

      <div class="detail-section" v-if="selectedRegistration?.remark">
        <h4>审核备注</h4>
        <el-alert :title="selectedRegistration.remark" type="info" :closable="false" />
      </div>
    </el-dialog>

    <!-- 驳回弹窗 -->
    <el-dialog
      v-model="rejectVisible"
      title="驳回报名"
      width="500px"
    >
      <el-form>
        <el-form-item label="驳回原因">
          <el-input
            v-model="rejectRemark"
            type="textarea"
            rows="4"
            placeholder="请输入驳回原因"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="rejectVisible = false">取消</el-button>
        <el-button type="danger" @click="confirmReject">确认驳回</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Document, Timer, CircleCheck, CircleClose,
  EditPen, Trophy, Search
} from '@element-plus/icons-vue'
import { getAdminRegistrations, approveRegistration, rejectRegistration, getRegistrationStatistics } from '@/api/registration'
import { getCompetitions } from '@/api/competition'

const loading = ref(false)
const registrations = ref([])
const competitions = ref([])
const stats = ref({
  total: 0,
  draft: 0,
  submitted: 0,
  approved: 0,
  rejected: 0
})

const filterCompetition = ref('')
const filterStatus = ref('')
const filterKeyword = ref('')
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const detailVisible = ref(false)
const selectedRegistration = ref(null)

const rejectVisible = ref(false)
const rejectRemark = ref('')
const rejectTarget = ref(null)

const statusType = (status) => {
  const map = {
    draft: 'info',
    submitted: 'warning',
    approved: 'success',
    rejected: 'danger',
    withdrawn: 'default'
  }
  return map[status] || 'info'
}

const statusText = (status) => {
  const map = {
    draft: '草稿',
    submitted: '已提交',
    approved: '已通过',
    rejected: '已驳回',
    withdrawn: '已撤回'
  }
  return map[status] || status
}

const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      per_page: pageSize.value,
      keyword: filterKeyword.value,
      status: filterStatus.value,
      competition_id: filterCompetition.value
    }
    const res = await getAdminRegistrations(params)
    if (res.code === 200) {
      registrations.value = res.data.registrations
      total.value = res.data.total
    }

    const statsRes = await getRegistrationStatistics()
    if (statsRes.code === 200) {
      stats.value = statsRes.data
    }
  } catch (error) {
    console.error('获取报名数据失败', error)
  } finally {
    loading.value = false
  }
}

const loadCompetitions = async () => {
  try {
    const res = await getCompetitions({ per_page: 100 })
    if (res.code === 200) {
      competitions.value = res.data.competitions
    }
  } catch (e) {}
}

const handleSearch = () => {
  currentPage.value = 1
  fetchData()
}

const handleReset = () => {
  filterCompetition.value = ''
  filterStatus.value = ''
  filterKeyword.value = ''
  currentPage.value = 1
  fetchData()
}

const handlePageChange = (page) => {
  currentPage.value = page
  fetchData()
}

const showDetail = (row) => {
  selectedRegistration.value = row
  detailVisible.value = true
}

const handleApprove = async (row) => {
  try {
    await ElMessageBox.confirm('确定要通过该报名吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'success'
    })
    const res = await approveRegistration(row.id)
    if (res.code === 200) {
      row.status = 'approved'
      ElMessage.success('报名已通过')
      fetchData()
    }
  } catch {
    // 取消
  }
}

const handleReject = (row) => {
  rejectTarget.value = row
  rejectRemark.value = ''
  rejectVisible.value = true
}

const confirmReject = async () => {
  if (!rejectRemark.value.trim()) {
    ElMessage.warning('请输入驳回原因')
    return
  }

  if (rejectTarget.value) {
    try {
      const res = await rejectRegistration(rejectTarget.value.id, { remark: rejectRemark.value })
      if (res.code === 200) {
        rejectTarget.value.status = 'rejected'
        rejectTarget.value.remark = rejectRemark.value
        ElMessage.success('报名已驳回')
        fetchData()
      }
    } catch (error) {
      console.error(error)
    }
  }

  rejectVisible.value = false
}

onMounted(() => {
  loadCompetitions()
  fetchData()
})
</script>

<style scoped>
.registration-management {
  padding-bottom: 20px;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 24px;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  --stat-color: var(--text-primary);
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 20px;
  text-align: center;
  transition: all var(--transition-fast);
}

.stat-card:hover {
  border-color: var(--stat-color);
  box-shadow: var(--shadow-sm);
}

.stat-card .el-icon {
  color: var(--stat-color);
  margin-bottom: 8px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--stat-color);
  line-height: 1;
  margin-bottom: 6px;
}

.stat-label {
  font-size: 13px;
  color: var(--text-secondary);
}

.filter-card {
  margin-bottom: 20px;
}

.filter-form {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.comp-name {
  font-weight: 500;
  color: var(--text-primary);
}

.team-name {
  color: var(--text-primary);
}

.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.detail-section {
  margin-top: 20px;
}

.detail-section h4 {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 12px;
}
</style>
