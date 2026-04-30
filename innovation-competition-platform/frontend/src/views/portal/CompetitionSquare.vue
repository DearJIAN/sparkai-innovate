<template>
  <div class="competition-square">
    <!-- Banner 区域 -->
    <div class="square-banner">
      <div class="banner-content">
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
        <div
          v-for="comp in filteredCompetitions"
          :key="comp.id"
          class="competition-card"
          @click="goToDetail(comp.id)"
        >
          <div class="card-poster" :style="comp.posterStyle">
            <div class="poster-content" v-if="!comp.poster_url">
              <span class="poster-name">{{ comp.name }}</span>
            </div>
            <div class="poster-badge">{{ comp.level }}</div>
          </div>
          <div class="card-body">
            <div class="card-tags">
              <el-tag size="small" :type="comp.levelType">{{ comp.level }}</el-tag>
              <el-tag size="small" class="category-tag">{{ comp.category }}</el-tag>
            </div>
            <h3 class="card-title">{{ comp.name }}</h3>
            <p class="card-organizer">{{ comp.organizer }}</p>
            <div class="card-meta">
              <span class="meta-item">
                <el-icon><Calendar /></el-icon>
                报名截止：{{ comp.endDate }}
              </span>
              <span class="meta-item">
                <el-icon><View /></el-icon>
                {{ comp.viewCount }}
              </span>
              <span class="meta-item">
                <el-icon><User /></el-icon>
                {{ comp.registrationCount }}人报名
              </span>
            </div>
            <div class="card-footer">
              <el-tag :type="comp.statusType" size="small">{{ comp.statusText }}</el-tag>
              <el-button
                type="primary"
                size="small"
                @click.stop="handleRegister(comp)"
              >
                {{ canRegister ? '立即报名' : '查看详情' }}
              </el-button>
            </div>
          </div>
        </div>
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
import { Search, Calendar, View, User } from '@element-plus/icons-vue'
import { getPublicCompetitions } from '@/api/competition'

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
      competitions.value = res.data.competitions.map(c => ({
        ...c,
        statusText: getStatusText(c.status),
        statusType: getStatusType(c.status),
        levelType: getLevelType(c.level),
        gradient: c.poster_url ? '' : 'linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%)',
        posterStyle: c.poster_url 
          ? { backgroundImage: `url(${c.poster_url})`, backgroundSize: 'cover', backgroundPosition: 'center' }
          : { background: 'linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%)' }
      }))
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
.square-banner {
  background: linear-gradient(135deg, #0c4a6e 0%, #075985 50%, #0ea5e9 100%);
  padding: 50px 40px;
  border-radius: 0 0 40px 40px;
}

.banner-content {
  max-width: 1400px;
  margin: 0 auto;
}

.banner-title {
  font-size: 32px;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 12px;
}

.banner-subtitle {
  font-size: 16px;
  color: #bae6fd;
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
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
}

.competition-card {
  background: #ffffff;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e2e8f0;
}

.competition-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 20px 40px -12px rgba(0, 0, 0, 0.15);
}

.card-poster {
  height: 160px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.poster-content {
  text-align: center;
}

.poster-name {
  color: #ffffff;
  font-size: 18px;
  font-weight: 600;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  line-height: 1.4;
}

.poster-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  background: rgba(255, 255, 255, 0.9);
  color: #1e293b;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.card-body {
  padding: 20px;
}

.card-tags {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.category-tag {
  background-color: #f1f5f9;
  color: #475569;
  border: none;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 8px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-organizer {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 12px;
}

.card-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 16px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #64748b;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 40px;
}
</style>
