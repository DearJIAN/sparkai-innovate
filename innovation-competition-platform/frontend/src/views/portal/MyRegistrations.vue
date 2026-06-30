<template>
  <div class="my-registrations">
    <!-- 顶部统计 -->
    <div class="stats-header">
      <h1 class="page-title">我的赛事</h1>
      <div class="stats-grid">
        <div class="stat-item">
          <div class="stat-value">{{ stats.total }}</div>
          <div class="stat-label">已报名</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ stats.draft }}</div>
          <div class="stat-label">草稿</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ stats.submitted }}</div>
          <div class="stat-label">已提交</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ stats.approved }}</div>
          <div class="stat-label">已通过</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ stats.rejected }}</div>
          <div class="stat-label">被驳回</div>
        </div>
      </div>
    </div>

    <!-- 报名列表 -->
    <div class="registrations-list">
      <div
        v-for="reg in registrations"
        :key="reg.id"
        class="registration-card"
      >
        <div class="card-poster" :style="reg.posterStyle">
          <span class="poster-name" v-if="!reg.poster_url && !reg.localImage">{{ reg.competitionName }}</span>
        </div>
        <div class="card-body">
          <div class="card-header">
            <h3 class="competition-name">{{ reg.competitionName }}</h3>
            <el-tag :type="statusType(reg.status)" size="small">
              {{ statusText(reg.status) }}
            </el-tag>
          </div>
          <p class="track-name">赛道：{{ reg.trackName }}</p>
          <p class="team-name">队伍：{{ reg.teamName }}</p>
          <div class="card-meta">
            <span class="meta-item">
              <el-icon><Calendar /></el-icon>
              报名：{{ reg.createdAt }}
            </span>
            <span class="meta-item">
              <el-icon><User /></el-icon>
              {{ reg.memberCount }} 名队员
            </span>
            <span class="meta-item">
              <el-icon><Document /></el-icon>
              {{ reg.materialCount }} 份材料
            </span>
          </div>
          <div class="card-actions">
            <el-button
              v-if="reg.status === 'draft'"
              type="primary"
              size="small"
              @click="continueEdit(reg)"
            >
              继续完善
            </el-button>
            <el-button
              v-if="reg.status === 'withdrawn'"
              type="primary"
              size="small"
              @click="continueEdit(reg)"
            >
              重新报名
            </el-button>
            <el-button
              v-if="reg.status === 'submitted'"
              type="info"
              size="small"
              plain
            >
              等待审核
            </el-button>
            <el-button
              v-if="reg.status === 'approved'"
              type="success"
              size="small"
              plain
            >
              报名通过
            </el-button>
            <el-button
              v-if="reg.status === 'rejected'"
              type="danger"
              size="small"
              plain
            >
              报名驳回
            </el-button>
            <el-button
              v-if="['draft', 'submitted'].includes(reg.status)"
              type="danger"
              size="small"
              link
              @click="withdraw(reg)"
            >
              撤回
            </el-button>
            <el-button
              size="small"
              link
              @click="showDetail(reg)"
            >
              查看详情
            </el-button>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <el-empty
        v-if="registrations.length === 0"
        description="暂无报名记录"
        :image-size="120"
      >
        <el-button type="primary" @click="goToCompetitions">
          去报名
        </el-button>
      </el-empty>
    </div>

    <!-- 详情弹窗 -->
    <el-dialog
      v-model="detailVisible"
      title="报名详情"
      width="600px"
    >
      <el-descriptions :column="1" border v-if="selectedRegistration">
        <el-descriptions-item label="竞赛名称">
          {{ selectedRegistration.competitionName }}
        </el-descriptions-item>
        <el-descriptions-item label="赛道">
          {{ selectedRegistration.trackName }}
        </el-descriptions-item>
        <el-descriptions-item label="队伍名称">
          {{ selectedRegistration.teamName }}
        </el-descriptions-item>
        <el-descriptions-item label="学校">
          {{ selectedRegistration.school }}
        </el-descriptions-item>
        <el-descriptions-item label="学院">
          {{ selectedRegistration.college }}
        </el-descriptions-item>
        <el-descriptions-item label="指导老师">
          {{ selectedRegistration.teacherName }}
        </el-descriptions-item>
        <el-descriptions-item label="联系电话">
          {{ selectedRegistration.contactPhone }}
        </el-descriptions-item>
        <el-descriptions-item label="报名状态">
          <el-tag :type="statusType(selectedRegistration.status)">
            {{ statusText(selectedRegistration.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="审核备注" v-if="selectedRegistration.remark">
          {{ selectedRegistration.remark }}
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Calendar, User, Document } from '@element-plus/icons-vue'
import { getMyRegistrations, withdrawRegistration } from '@/api/registration'

// 导入本地竞赛图片
import imgAI from '@/assets/images/competitions/2026 AI 应用创新设计大赛.png'
import imgRural from '@/assets/images/competitions/2026 乡村振兴公益创业实践赛.png'
import imgEnterprise from '@/assets/images/competitions/2026 企业真实命题创新挑战赛.png'
import imgInnovation from '@/assets/images/competitions/2026 大学生创新创业计划训练赛.png'
import imgCareer from '@/assets/images/competitions/2026 大学生职业规划与就业能力大赛.png'
import imgDigital from '@/assets/images/competitions/2026 数字经济与商业模式创新挑战赛.png'
import imgSmartMfg from '@/assets/images/competitions/2026 智能制造与物联网应用赛.png'
import imgEcommerce from '@/assets/images/competitions/2026 校园电子商务运营挑战赛.png'
import imgSoftware from '@/assets/images/competitions/2026 软件工程创新项目挑战赛.png'
import imgRedDream from '@/assets/images/competitions/2026 青年红色筑梦公益项目赛.png'

const competitionImages = {
  'AI 应用创新设计大赛': imgAI,
  '乡村振兴公益创业实践赛': imgRural,
  '企业真实命题创新挑战赛': imgEnterprise,
  '大学生创新创业计划训练赛': imgInnovation,
  '大学生职业规划与就业能力大赛': imgCareer,
  '数字经济与商业模式创新挑战赛': imgDigital,
  '智能制造与物联网应用赛': imgSmartMfg,
  '校园电子商务运营挑战赛': imgEcommerce,
  '软件工程创新项目挑战赛': imgSoftware,
  '青年红色筑梦公益项目赛': imgRedDream
}

const getLocalImage = (name) => {
  const key = name.replace(/^2026\s*/, '')
  return competitionImages[key] || null
}

const router = useRouter()

const stats = ref({
  total: 0,
  draft: 0,
  submitted: 0,
  approved: 0,
  rejected: 0
})

const registrations = ref([])

const loadData = async () => {
  try {
    const res = await getMyRegistrations()
    if (res.code === 200) {
      const data = res.data.registrations || []
      registrations.value = data.map(reg => {
        const localImage = getLocalImage(reg.competitionName)
        return {
          ...reg,
          localImage,
          posterStyle: localImage || reg.poster_url
            ? { backgroundImage: `url(${localImage || reg.poster_url})`, backgroundSize: 'cover', backgroundPosition: 'center' }
            : { background: 'linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%)' }
        }
      })

      stats.value = {
        total: data.filter(r => r.status !== 'withdrawn').length,
        draft: data.filter(r => r.status === 'draft').length,
        submitted: data.filter(r => r.status === 'submitted').length,
        approved: data.filter(r => r.status === 'approved').length,
        rejected: data.filter(r => r.status === 'rejected').length
      }
    }
  } catch (error) {
    console.error('获取报名记录失败', error)
  }
}

onMounted(() => {
  loadData()
})

const detailVisible = ref(false)
const selectedRegistration = ref(null)

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

const goToCompetitions = () => {
  router.push('/competitions')
}

const continueEdit = (reg) => {
  router.push(`/competitions/${reg.competition_id}/register?regId=${reg.id}`)
}

const withdraw = async (reg) => {
  try {
    await ElMessageBox.confirm('确定要撤回该报名吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    const res = await withdrawRegistration(reg.id)
    if (res.code === 200) {
      ElMessage.success('报名已撤回')
      loadData()
    } else {
      ElMessage.error(res.message || '撤回失败')
    }
  } catch (e) {
    // 取消
  }
}

const showDetail = (reg) => {
  selectedRegistration.value = reg
  detailVisible.value = true
}
</script>

<style scoped>
.my-registrations {
  min-height: 100vh;
  background: linear-gradient(180deg, #f0f9ff 0%, #ffffff 100%);
  padding: 40px;
}

.stats-header {
  max-width: 1400px;
  margin: 0 auto 32px;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 24px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
}

.stat-item {
  background: #ffffff;
  border-radius: 16px;
  padding: 24px;
  text-align: center;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.stat-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #0ea5e9;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #64748b;
}

.registrations-list {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.registration-card {
  display: flex;
  background: #ffffff;
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.registration-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.card-poster {
  width: 200px;
  min-height: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  flex-shrink: 0;
}

.poster-name {
  color: #ffffff;
  font-size: 16px;
  font-weight: 600;
  text-align: center;
  line-height: 1.4;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.card-body {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.competition-name {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
}

.track-name {
  font-size: 14px;
  color: #475569;
  margin-bottom: 4px;
}

.team-name {
  font-size: 14px;
  color: #64748b;
  margin-bottom: 12px;
}

.card-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #64748b;
}

.card-actions {
  display: flex;
  gap: 8px;
  margin-top: auto;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .registration-card {
    flex-direction: column;
  }

  .card-poster {
    width: 100%;
    min-height: 120px;
  }
}
</style>
