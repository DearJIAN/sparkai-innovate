<template>
  <div class="external-competitions">
    <div class="portal-hero-banner portal-hero-banner--external">
      <div class="banner-decoration">
        <div class="deco-circle c1"></div>
        <div class="deco-circle c2"></div>
      </div>
      <div class="banner-content">
        <div class="banner-badge">
          <el-icon size="16"><Link /></el-icon>
          <span>校外竞赛</span>
        </div>
        <h1 class="banner-title">校外竞赛</h1>
        <p class="banner-subtitle">聚合国家级创新创业赛事，帮助团队提前规划参赛路径。各赛事信息以官网最新通知为准。</p>
      </div>
    </div>

    <div class="page-body">
      <div class="filter-section">
        <button
          v-for="cat in categories"
          :key="cat.value"
          class="filter-chip"
          :class="{ active: activeCategory === cat.value }"
          @click="activeCategory = cat.value"
        >
          {{ cat.label }}
        </button>
      </div>

      <div class="competition-grid">
        <div
          v-for="comp in filteredCompetitions"
          :key="comp.slug"
          class="competition-card"
        >
          <div class="card-cover">
            <img v-if="comp.posterImage" class="cover-poster" :src="comp.posterImage" :alt="`${comp.title} 官方海报`" loading="lazy" />
            <div v-if="!comp.posterImage" class="cover-placeholder" :style="{ background: comp.coverGradient }">
              <div class="cover-placeholder-pattern"></div>
            </div>
            <div class="cover-badge">{{ comp.level }}</div>
          </div>
          <div class="card-body">
            <div class="card-tags">
              <span
                v-for="tag in comp.tags.slice(0, 3)"
                :key="tag"
                class="card-tag"
              >{{ tag }}</span>
              <span v-if="comp.tags.length > 3" class="card-tag more">+{{ comp.tags.length - 3 }}</span>
            </div>
            <h3 class="card-title">{{ comp.title }}</h3>
            <p class="card-summary">{{ comp.summary }}</p>
            <div class="card-meta">
              <div class="meta-item">
                <el-icon size="14"><OfficeBuilding /></el-icon>
                <span>{{ comp.organizer }}</span>
              </div>
              <div class="meta-item">
                <el-icon size="14"><Clock /></el-icon>
                <span>{{ comp.timeText }}</span>
              </div>
            </div>
            <div class="card-actions">
              <el-button
                type="primary"
                size="default"
                class="detail-btn"
                @click="$router.push(`/external-competitions/${comp.slug}`)"
              >
                查看详情
                <el-icon><ArrowRight /></el-icon>
              </el-button>
              <el-button
                size="default"
                class="official-btn"
                @click.stop="openOfficial(comp.officialUrl)"
              >
                <el-icon><Link /></el-icon>
                前往官网
              </el-button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="filteredCompetitions.length === 0" class="empty-state">
        <el-icon size="48"><FolderOpened /></el-icon>
        <p>暂无该分类的校外竞赛</p>
      </div>

      <div class="page-tips">
        <el-icon size="16"><WarningFilled /></el-icon>
        <span>校外竞赛报名、截止时间、赛道要求以主办方官网或学校通知为准。本平台仅提供赛事资讯参考，不代理报名。</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { externalCompetitions, externalCategories } from '@/data/externalCompetitions'
import {
  Link, ArrowRight, OfficeBuilding, Clock,
  FolderOpened, WarningFilled
} from '@element-plus/icons-vue'

const categories = externalCategories
const activeCategory = ref('all')

const filteredCompetitions = computed(() => {
  if (activeCategory.value === 'all') return externalCompetitions
  return externalCompetitions.filter(c => c.category === activeCategory.value)
})

function openOfficial(url) {
  window.open(url, '_blank', 'noopener,noreferrer')
}
</script>

<style scoped>
.external-competitions {
  min-height: 100vh;
  background: linear-gradient(180deg, #f0f9ff 0%, #ffffff 100%);
}

/* ========== Banner ========== */
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

.portal-hero-banner--external {
  background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
}

.banner-decoration { position: absolute; right: 48px; top: 0; width: 35%; height: 100%; z-index: 1; }

.deco-circle { position: absolute; border-radius: 50%; opacity: 0.12; }
.c1 { width: 220px; height: 220px; background: #818cf8; right: -20px; top: -20px; animation: decoFloat 8s ease-in-out infinite; }
.c2 { width: 150px; height: 150px; background: #a78bfa; right: 140px; bottom: -20px; animation: decoFloat 10s ease-in-out infinite reverse; }

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

/* ========== Body ========== */
.page-body { max-width: 1200px; margin: 0 auto; padding: 36px 24px 60px; }

/* ========== Filter ========== */
.filter-section {
  display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 32px;
}

.filter-chip {
  padding: 8px 20px;
  border-radius: 20px;
  border: 1px solid #e2e8f0;
  background: #ffffff;
  color: #475569;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s ease;
}

.filter-chip:hover {
  border-color: #818cf8;
  color: #4f46e5;
  background: #f5f3ff;
}

.filter-chip.active {
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  color: #ffffff;
  border-color: transparent;
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25);
}

/* ========== Competition Grid ========== */
.competition-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.competition-card {
  background: #ffffff;
  border-radius: 20px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.competition-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 32px -8px rgba(0, 0, 0, 0.12), 0 4px 12px -2px rgba(0, 0, 0, 0.06);
}

.card-cover {
  position: relative;
  height: 180px;
  overflow: hidden;
  border-radius: 20px 20px 0 0;
  padding: 0;
}

.cover-poster {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.55s cubic-bezier(0.16, 1, 0.3, 1);
}

.competition-card:hover .cover-poster {
  transform: scale(1.03);
}

.cover-placeholder {
  position: absolute;
  inset: 0;
  background-size: 300% 300%;
  animation: sparkGradientFlow 8s ease infinite;
}

.cover-placeholder-pattern {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background-image:
    radial-gradient(circle at 30% 40%, rgba(255,255,255,0.1) 0%, transparent 50%),
    radial-gradient(circle at 70% 60%, rgba(255,255,255,0.06) 0%, transparent 50%);
}

.cover-badge {
  position: absolute; top: 16px; right: 16px;
  padding: 4px 12px; border-radius: 10px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(8px);
  color: #ffffff; font-size: 12px; font-weight: 600;
  border: 1px solid rgba(255, 255, 255, 0.25);
  z-index: 1;
}

.card-body { padding: 20px 24px 24px; }

.card-tags {
  display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 12px;
}

.card-tag {
  padding: 3px 10px; border-radius: 8px;
  background: #f1f5f9; color: #475569;
  font-size: 11px; font-weight: 500;
}

.card-tag.more {
  background: #e2e8f0; color: #64748b;
}

.card-title {
  font-size: 17px; font-weight: 600; color: #0f172a;
  margin-bottom: 8px; line-height: 1.5;
}

.card-summary {
  font-size: 13px; color: #64748b; line-height: 1.6;
  margin-bottom: 14px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-meta {
  display: flex; flex-direction: column; gap: 6px; margin-bottom: 18px;
}

.meta-item {
  display: flex; align-items: center; gap: 6px;
  font-size: 12px; color: #64748b;
}

.meta-item .el-icon { color: #94a3b8; flex-shrink: 0; }

.card-actions {
  display: flex; gap: 10px;
}

.detail-btn {
  flex: 1;
  display: flex; align-items: center; justify-content: center; gap: 6px;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  border: none; color: #fff; border-radius: 12px;
  font-weight: 500; padding: 10px 20px;
  transition: all 0.3s ease;
}

.detail-btn:hover {
  background: linear-gradient(135deg, #1d4ed8, #6d28d9);
  box-shadow: 0 6px 18px rgba(37, 99, 235, 0.3);
  transform: translateY(-1px);
}

.official-btn {
  display: flex; align-items: center; gap: 6px;
  background: #f8fafc; border: 1px solid #e2e8f0; color: #475569;
  border-radius: 12px; font-weight: 500; padding: 10px 18px;
  transition: all 0.3s ease;
}

.official-btn:hover {
  background: #f1f5f9; border-color: #cbd5e1; color: #0f172a;
}

/* ========== Empty State ========== */
.empty-state {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  padding: 60px 20px; color: #94a3b8;
}

.empty-state .el-icon { margin-bottom: 12px; opacity: 0.5; }
.empty-state p { font-size: 14px; }

/* ========== Tips ========== */
.page-tips {
  display: flex; align-items: center; justify-content: center; gap: 8px;
  padding: 16px 24px;
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.06), rgba(251, 191, 36, 0.06));
  border-radius: 14px; color: #92400e; font-size: 13px;
  border: 1px solid rgba(245, 158, 11, 0.15);
}

.page-tips .el-icon { color: #f59e0b; flex-shrink: 0; }

/* ========== 响应式 ========== */
@media (max-width: 768px) {
  .portal-hero-banner {
    min-height: 220px;
    padding: 40px 24px;
    border-radius: 0 0 28px 28px;
  }
  .banner-title { font-size: 30px; }
  .banner-subtitle { font-size: 15px; }
  .banner-decoration { display: none; }

  .competition-grid {
    grid-template-columns: 1fr;
  }

  .card-cover { height: 180px; }
  .cover-title { font-size: 17px; }

  .card-actions { flex-direction: column; }
  .page-body { padding: 28px 16px 48px; }
}

@keyframes sparkGradientFlow {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

@media (prefers-reduced-motion: reduce) {
  .banner-gradient-bg, .deco-circle { animation: none !important; }
  .competition-card { transition: none !important; }
  .cover-placeholder { animation: none !important; }
}
</style>