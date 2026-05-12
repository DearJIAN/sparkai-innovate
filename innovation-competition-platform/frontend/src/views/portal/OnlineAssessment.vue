<template>
  <div class="assessment-page">
    <div class="assessment-banner">
      <div class="banner-bg"></div>
      <div class="banner-content">
        <h1 class="banner-title">在线测评中心</h1>
        <p class="banner-subtitle">探索创业潜能、团队协作与职业发展画像</p>
      </div>
    </div>

    <div class="assessment-layout">
      <aside class="sidebar">
        <div class="sidebar-title">测评分类</div>
        <div
          v-for="cat in categories"
          :key="cat.key"
          class="sidebar-item"
          :class="{ active: activeCategory === cat.key }"
          @click="selectCategory(cat.key)"
        >
          <span class="sidebar-label">{{ cat.name }}</span>
          <span class="sidebar-count">{{ getCategoryCount(cat.key) }}</span>
        </div>
      </aside>

      <div class="main-area">
        <div class="main-header">
          <h2 class="main-title">{{ currentCategoryName }}</h2>
          <div class="main-search">
            <el-input
              v-model="searchKeyword"
              placeholder="搜索测评名称、描述或标签..."
              clearable
              size="large"
              class="search-input"
              @input="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </div>
        </div>

        <div v-if="filteredList.length === 0" class="empty-state">
          <el-icon size="64"><Search /></el-icon>
          <p>没有找到匹配的测评</p>
          <span>试试其他关键词或切换分类</span>
        </div>

        <TransitionGroup name="card-list" tag="div" class="assessment-grid">
          <div
            v-for="item in filteredList"
            :key="item.id"
            class="assessment-card"
            @click="handleStart(item)"
          >
            <div class="card-cover" :style="{ background: `linear-gradient(135deg, ${item.gradient[0]}, ${item.gradient[1]})` }">
              <div class="card-cover-art">
                <span class="cover-art-text">{{ getCoverText(item) }}</span>
              </div>
            </div>
            <div class="card-body">
              <h3 class="card-title">{{ item.title }}</h3>
              <p class="card-desc">{{ item.description }}</p>
              <div class="card-meta">
                <span class="meta-item">
                  <el-icon size="14"><Clock /></el-icon>
                  {{ item.duration }}分钟
                </span>
                <span class="meta-item">
                  <el-icon size="14"><Document /></el-icon>
                  {{ item.questionCount }}题
                </span>
                <span class="meta-item">
                  <el-icon size="14"><View /></el-icon>
                  {{ item.heat }}
                </span>
              </div>
              <div class="card-footer">
                <el-button
                  :type="item.real ? 'primary' : 'default'"
                  size="small"
                  round
                  class="card-btn"
                  :class="{ 'btn-real': item.real }"
                  @click.stop="handleStart(item)"
                >
                  {{ item.real ? '开始测评' : '查看详情' }}
                  <el-icon><ArrowRight /></el-icon>
                </el-button>
              </div>
            </div>
          </div>
        </TransitionGroup>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Search, Clock, Document, View, ArrowRight } from '@element-plus/icons-vue'
import {
  assessmentCategories,
  assessmentList,
  getAssessmentsByCategory,
  getAssessmentsBySearch
} from '@/data/assessmentBank'

const router = useRouter()
const activeCategory = ref('all')
const searchKeyword = ref('')

const categories = assessmentCategories

const filteredList = computed(() => {
  const byCategory = getAssessmentsByCategory(activeCategory.value)
  const bySearch = getAssessmentsBySearch(searchKeyword.value)
  const ids = new Set(bySearch.map(item => item.id))
  return byCategory.filter(item => ids.has(item.id))
})

const currentCategoryName = computed(() => {
  const cat = categories.find(c => c.key === activeCategory.value)
  return cat ? (cat.key === 'all' ? '全部测评' : cat.name) : '全部测评'
})

const coverTextMap = {
  'entrepreneurial-spirit': '创 业 精 神',
  'entrepreneurial-personality': '创 业 性 格',
  'entrepreneurial-interest': '创 业 兴 趣',
  'entrepreneurial-ability': '创 业 能 力',
  'career-temperament': '职 业 气 质',
  'career-values': '职 业 价 值',
  'career-interest': '职 业 兴 趣',
  'career-personality': '职 业 性 格',
  'teamwork-ability': '团 队 合 作',
  'self-learning-ability': '自 主 学 习',
  'communication-ability': '沟 通 交 际',
  'emotion-control-ability': '情 绪 控 制'
}

function getCoverText(item) {
  return coverTextMap[item.id] || ''
}

function selectCategory(key) {
  activeCategory.value = key
}

function getCategoryCount(key) {
  if (key === 'all') return assessmentList.length
  const cat = categories.find(c => c.key === key)
  if (!cat || !cat.children) return 0
  return assessmentList.filter(item => cat.children.includes(item.id)).length
}

function handleSearch() {
}

function handleStart(item) {
  if (item.real) {
    router.push(`/assessment/${item.id}`)
  } else {
    router.push(`/assessment/${item.id}/coming-soon`)
  }
}
</script>

<style scoped>
.assessment-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #eff6ff 0%, #f8fafc 100%);
}

.assessment-banner {
  position: relative;
  background: linear-gradient(135deg, #1e40af 0%, #2563eb 50%, #06b6d4 100%);
  padding: 48px 40px 40px;
  overflow: hidden;
}

.banner-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background:
    radial-gradient(circle at 20% 50%, rgba(14, 165, 233, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 80% 30%, rgba(139, 92, 246, 0.1) 0%, transparent 50%);
}

.banner-content {
  position: relative;
  z-index: 2;
  max-width: 1200px;
  margin: 0 auto;
}

.banner-title {
  font-size: 32px;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 8px;
}

.banner-subtitle {
  font-size: 16px;
  color: #93c5fd;
}

.assessment-layout {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  gap: 0;
  padding: 24px 40px 40px;
}

.sidebar {
  width: 220px;
  flex-shrink: 0;
  background: #ffffff;
  border-radius: 12px;
  padding: 16px 0;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
  align-self: flex-start;
  position: sticky;
  top: 80px;
}

.sidebar-title {
  font-size: 14px;
  font-weight: 600;
  color: #475569;
  padding: 8px 20px 12px;
  border-bottom: 1px solid #f1f5f9;
  margin-bottom: 4px;
}

.sidebar-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
  color: #475569;
  border-left: 3px solid transparent;
}

.sidebar-item:hover {
  background: #f8fafc;
  color: #2563eb;
}

.sidebar-item.active {
  background: #eff6ff;
  color: #2563eb;
  font-weight: 600;
  border-left-color: #2563eb;
}

.sidebar-count {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 10px;
  background: #f1f5f9;
  color: #64748b;
}

.sidebar-item.active .sidebar-count {
  background: #dbeafe;
  color: #2563eb;
}

.main-area {
  flex: 1;
  margin-left: 24px;
  min-width: 0;
}

.main-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
  gap: 16px;
}

.main-title {
  font-size: 20px;
  font-weight: 600;
  color: #1e293b;
  white-space: nowrap;
}

.main-search {
  width: 320px;
}

.search-input :deep(.el-input__wrapper) {
  border-radius: 24px;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.08);
}

.assessment-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.empty-state {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 64px 0;
  color: #94a3b8;
}

.empty-state p {
  font-size: 16px;
  font-weight: 500;
  color: #64748b;
  margin: 16px 0 4px;
}

.empty-state span {
  font-size: 13px;
  color: #94a3b8;
}

.assessment-card {
  background: #ffffff;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
}

.assessment-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(15, 23, 42, 0.1);
}

.card-cover {
  height: 160px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.card-cover-art {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 0 16px;
}

.cover-art-text {
  font-size: 28px;
  font-weight: 900;
  letter-spacing: 0.12em;
  color: rgba(255, 255, 255, 0.92);
  text-shadow:
    0 2px 12px rgba(0, 0, 0, 0.18),
    0 0 40px rgba(255, 255, 255, 0.08);
  text-align: center;
  line-height: 1.3;
  word-break: keep-all;
  -webkit-font-smoothing: antialiased;
}

.card-body {
  padding: 20px;
}

.card-title {
  font-size: 17px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 8px;
}

.card-desc {
  font-size: 13px;
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 14px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 14px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #94a3b8;
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
}



.card-btn {
  flex-shrink: 0;
}

.btn-real {
  background: linear-gradient(135deg, #2563eb, #3b82f6);
  border-color: #2563eb;
  color: #ffffff;
}

.btn-real:hover {
  background: linear-gradient(135deg, #1d4ed8, #2563eb);
  border-color: #1d4ed8;
  color: #ffffff;
}

/* card list transition */
.card-list-enter-active {
  transition: all 0.4s ease;
}

.card-list-leave-active {
  transition: all 0.3s ease;
}

.card-list-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.card-list-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* responsive */
@media (max-width: 1024px) {
  .assessment-layout {
    flex-direction: column;
    padding: 16px;
  }

  .sidebar {
    width: 100%;
    position: static;
    display: flex;
    overflow-x: auto;
    padding: 8px;
    gap: 0;
    border-radius: 12px;
    margin-bottom: 16px;
  }

  .sidebar-title {
    display: none;
  }

  .sidebar-item {
    border-left: none;
    white-space: nowrap;
    padding: 8px 14px;
    font-size: 13px;
    border-radius: 8px;
    flex-shrink: 0;
  }

  .sidebar-item.active {
    border-left: none;
  }

  .sidebar-count {
    display: none;
  }

  .main-area {
    margin-left: 0;
  }

  .main-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .main-search {
    width: 100%;
  }

  .assessment-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .assessment-banner {
    padding: 32px 20px;
  }

  .banner-title {
    font-size: 24px;
  }

  .banner-subtitle {
    font-size: 14px;
  }
}
</style>