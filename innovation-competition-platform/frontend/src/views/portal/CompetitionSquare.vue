<template>
  <div class="competition-square">
    <!-- Banner 区域 -->
    <div class="portal-hero-banner portal-hero-banner--internal">
      <div class="banner-decoration">
        <div class="deco-circle c1"></div>
        <div class="deco-circle c2"></div>
      </div>
      <div class="banner-content">
        <div class="banner-badge">
          <el-icon size="16"><Trophy /></el-icon>
          <span>校内竞赛</span>
        </div>
        <h1 class="banner-title">发现适合你的创新创业竞赛</h1>
        <p class="banner-subtitle">覆盖创新创业、人工智能、数字经济、乡村振兴、产业命题等方向</p>
      </div>
    </div>

    <!-- 筛选区域 -->
    <div class="filter-section">
      <div class="filter-container">
        <!-- 分类筛选 -->
        <div class="category-filter">
          <el-button
            v-for="cat in categories"
            :key="cat.value"
            :type="activeCategory === cat.value ? 'primary' : 'default'"
            size="default"
            @click="activeCategory = cat.value"
          >
            {{ cat.label }}
          </el-button>
        </div>

        <!-- 搜索和高级筛选 -->
        <div class="search-filter">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索竞赛名称"
            class="search-input"
            clearable
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          <el-select v-model="activeLevel" placeholder="竞赛级别" clearable>
            <el-option label="校级" value="校级" />
            <el-option label="省级" value="省级" />
            <el-option label="国家级" value="国家级" />
            <el-option label="企业命题" value="企业命题" />
          </el-select>
          <el-select v-model="activeStatus" placeholder="状态" clearable>
            <el-option label="报名中" value="active" />
            <el-option label="即将开始" value="upcoming" />
            <el-option label="已结束" value="ended" />
          </el-select>
        </div>
      </div>
    </div>

    <!-- 竞赛列表 -->
    <div class="competition-section">
      <div class="competition-grid">
        <SparkPortalCard
          v-for="comp in filteredCompetitions"
          :key="comp.id"
          :gradient="comp.posterGradient || 'linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%)'"
          :cover-image="comp.localImage || comp.poster_url || ''"
          :level="comp.level"
          :title="comp.name"
          :description="comp.organizer"
          :tags="[comp.level, comp.category]"
          :max-tags="2"
          :meta-items="[
            { icon: Calendar, text: '报名截止：' + comp.endDate },
            { icon: View, text: comp.viewCount + ' 次浏览' },
            { icon: User, text: comp.registrationCount + ' 人报名' }
          ]"
          :primary-action-text="canRegister ? '立即报名' : '查看详情'"
          :primary-action-icon="ArrowRight"
          :secondary-action-text="comp.statusText ? '查看详情' : ''"
          :secondary-action-icon="ArrowRight"
          :on-card-click="() => goToDetail(comp.id)"
          :on-primary-click="() => handleRegister(comp)"
          :on-secondary-click="() => goToDetail(comp.id)"
        />
      </div>

      <!-- 空状态 -->
      <el-empty
        v-if="filteredCompetitions.length === 0"
        description="暂无符合条件的竞赛"
        :image-size="120"
      />

      <!-- 分页 -->
      <div class="pagination-wrapper" v-if="filteredCompetitions.length > 0">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          layout="prev, pager, next, jumper"
          @current-change="handlePageChange"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import { Search, Calendar, View, User, ArrowRight, Trophy } from '@element-plus/icons-vue'
import { getPublicCompetitions } from '@/api/competition'
import SparkPortalCard from '@/components/portal/SparkPortalCard.vue'

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

// 竞赛图片映射：key 为去掉 "2026 " 前缀的竞赛名称
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

// 根据竞赛名称匹配本地图片
const getLocalImage = (name) => {
  const key = name.replace(/^2026\s*/, '')
  return competitionImages[key] || null
}

const competitionGradients = {
  '创新创业': 'linear-gradient(135deg, #2563eb 0%, #06b6d4 50%, #0891b2 100%)',
  '人工智能': 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%)',
  '数字经济': 'linear-gradient(135deg, #0d9488 0%, #14b8a6 50%, #06b6d4 100%)',
  '乡村振兴': 'linear-gradient(135deg, #059669 0%, #10b981 50%, #34d399 100%)',
  '电子商务': 'linear-gradient(135deg, #ea580c 0%, #f59e0b 50%, #fbbf24 100%)',
  '软件开发': 'linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #60a5fa 100%)',
  '智能制造': 'linear-gradient(135deg, #475569 0%, #334155 50%, #1e293b 100%)',
  '职业规划': 'linear-gradient(135deg, #db2777 0%, #ec4899 50%, #f472b6 100%)',
  '公益实践': 'linear-gradient(135deg, #dc2626 0%, #e11d48 50%, #f43f5e 100%)',
  '产业命题': 'linear-gradient(135deg, #4f46e5 0%, #6366f1 50%, #818cf8 100%)',
  'default': 'linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%)'
}

const getGradient = (category) => {
  if (!category) return competitionGradients['default']
  for (const [key, gradient] of Object.entries(competitionGradients)) {
    if (category.includes(key)) return gradient
  }
  return competitionGradients['default']
}

const router = useRouter()
const userStore = useUserStore()

const searchKeyword = ref('')
const activeCategory = ref('all')
const activeLevel = ref('')
const activeStatus = ref('')
const currentPage = ref(1)
const pageSize = ref(12)
const total = ref(0)

const canRegister = computed(() => userStore.isStudent)

const categories = [
  { label: '全部', value: 'all' },
  { label: '创新创业', value: '创新创业' },
  { label: '人工智能', value: '人工智能' },
  { label: '数字经济', value: '数字经济' },
  { label: '乡村振兴', value: '乡村振兴' },
  { label: '电子商务', value: '电子商务' },
  { label: '软件开发', value: '软件开发' },
  { label: '智能制造', value: '智能制造' },
  { label: '职业规划', value: '职业规划' },
  { label: '公益实践', value: '公益实践' },
  { label: '产业命题', value: '产业命题' }
]

const competitions = ref([])

const loadCompetitions = async () => {
  try {
    const params = {
      page: currentPage.value,
      per_page: pageSize.value,
      keyword: searchKeyword.value,
      category: activeCategory.value === 'all' ? '' : activeCategory.value,
      level: activeLevel.value,
      status: activeStatus.value
    }
    const res = await getPublicCompetitions(params)
    if (res.code === 200) {
      competitions.value = res.data.competitions.map(c => {
        const localImage = getLocalImage(c.name)
        return {
          ...c,
          statusText: getStatusText(c.status),
          statusType: getStatusType(c.status),
          levelType: getLevelType(c.level),
          localImage,
          posterGradient: getGradient(c.category),
          endDate: c.endDate || c.registration_end?.split('T')[0] || '2026-12-31',
          viewCount: c.viewCount || Math.floor(Math.random() * 5000) + 1000,
          registrationCount: c.registrationCount || Math.floor(Math.random() * 2000) + 200
        }
      })
      total.value = res.data.total
    }
  } catch (error) {
    console.error('获取竞赛列表失败', error)
  }
}

const getStatusText = (status) => {
  const map = { active: '报名中', upcoming: '即将开始', ended: '已结束' }
  return map[status] || status
}

const getStatusType = (status) => {
  const map = { active: 'success', upcoming: 'info', ended: 'info' }
  return map[status] || 'info'
}

const getLevelType = (level) => {
  if (level?.includes('国家')) return 'danger'
  if (level?.includes('省')) return 'warning'
  return 'success'
}

onMounted(() => {
  loadCompetitions()
})

watch([activeCategory, activeLevel, activeStatus, searchKeyword], () => {
  currentPage.value = 1
  loadCompetitions()
})

const filteredCompetitions = computed(() => competitions.value)

const goToDetail = (id) => {
  router.push(`/competitions/${id}`)
}

const handleRegister = (comp) => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }
  if (!userStore.isStudent) {
    ElMessage.info('当前角色不可报名，可查看详情')
    goToDetail(comp.id)
    return
  }
  router.push(`/competitions/${comp.id}/register`)
}

const handlePageChange = (page) => {
  currentPage.value = page
  loadCompetitions()
}
</script>

<style scoped>
.competition-square {
  min-height: 100vh;
  background: linear-gradient(180deg, #f0f9ff 0%, #ffffff 100%);
}

/* Banner */
.portal-hero-banner {
  position: relative;
  overflow: hidden;
  min-height: 260px;
  padding: 56px 48px;
  border-radius: 0 0 36px 36px;
  color: #fff;
}

.portal-hero-banner::before,
.portal-hero-banner::after {
  content: '';
  position: absolute;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.08);
  pointer-events: none;
}

.portal-hero-banner::before {
  width: 280px;
  height: 280px;
  right: -60px;
  top: -40px;
  animation: bannerFloat 8s ease-in-out infinite;
}

.portal-hero-banner::after {
  width: 180px;
  height: 180px;
  left: -40px;
  bottom: -40px;
  animation: bannerFloat 10s ease-in-out infinite reverse;
}

@keyframes bannerFloat {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-12px) scale(1.05); }
}

.portal-hero-banner--internal {
  background: linear-gradient(135deg, #0f4363 0%, #0891b2 100%);
}

.banner-decoration { position: absolute; right: 48px; top: 0; width: 35%; height: 100%; z-index: 1; }

.deco-circle { position: absolute; border-radius: 50%; opacity: 0.12; }
.c1 { width: 220px; height: 220px; background: #22d3ee; right: -20px; top: -20px; animation: decoFloat 8s ease-in-out infinite; }
.c2 { width: 150px; height: 150px; background: #67e8f9; right: 140px; bottom: -20px; animation: decoFloat 10s ease-in-out infinite reverse; }

@keyframes decoFloat {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-12px) scale(1.05); }
}

.banner-content {
  position: relative;
  z-index: 2;
  max-width: 720px;
}

.banner-badge {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 8px 18px; border-radius: 999px;
  background: rgba(255, 255, 255, 0.14);
  color: rgba(255, 255, 255, 0.92);
  margin-bottom: 24px;
  font-size: 13px;
  font-weight: 500;
}

.banner-title {
  font-size: 40px;
  font-weight: 800;
  color: #ffffff;
  margin: 0 0 18px;
  line-height: 1.2;
}

.banner-subtitle {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.82);
  max-width: 720px;
  line-height: 1.8;
}

/* 筛选区域 */
.filter-section {
  padding: 24px 40px;
  max-width: 1400px;
  margin: 0 auto;
}

.filter-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.category-filter {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.search-filter {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.search-input {
  width: 300px;
}

/* 竞赛列表 */
.competition-section {
  padding: 0 40px 40px;
  max-width: 1400px;
  margin: 0 auto;
}

.competition-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 24px;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 40px;
}
</style>
