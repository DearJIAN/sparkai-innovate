<template>
  <div class="external-detail" v-if="competition">
    <div class="detail-hero">
      <img v-if="competition.posterImage" class="hero-image" :src="competition.posterImage" :alt="`${competition.title} 官方海报`" />
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <div class="breadcrumb">
          <router-link to="/portal" class="breadcrumb-link">首页</router-link>
          <el-icon size="12"><ArrowRight /></el-icon>
          <router-link to="/external-competitions" class="breadcrumb-link">校外竞赛</router-link>
          <el-icon size="12"><ArrowRight /></el-icon>
          <span class="breadcrumb-current">{{ competition.shortTitle }}</span>
        </div>
        <div class="hero-tags">
          <span class="hero-tag level-tag">{{ competition.level }}</span>
          <span class="hero-tag type-tag">校外竞赛</span>
          <span class="hero-tag status-tag">{{ competition.statusText }}</span>
        </div>
        <h1 class="hero-title">{{ competition.title }}</h1>
        <p class="hero-organizer">主办/组织：{{ competition.organizer }}</p>
        <p class="hero-time">{{ competition.timeText }}</p>
        <div class="hero-action">
          <el-button type="primary" size="large" class="official-hero-btn" @click="openOfficial(competition.officialUrl)">
            前往官网
            <el-icon><Link /></el-icon>
          </el-button>
        </div>
      </div>
    </div>

    <div class="detail-body">
      <el-row :gutter="24">
        <el-col :span="16">
          <div class="content-sections">
            <section class="detail-section">
              <div class="section-header">
                <div class="section-icon"><el-icon size="18"><Document /></el-icon></div>
                <h2>赛事简介</h2>
              </div>
              <p class="section-text">{{ competition.summary }}</p>
            </section>

            <section class="detail-section">
              <div class="section-header">
                <div class="section-icon"><el-icon size="18"><Grid /></el-icon></div>
                <h2>赛道 / 类别</h2>
              </div>
              <ul class="section-list">
                <li v-for="(track, idx) in competition.tracks" :key="idx">
                  <span class="list-marker"></span>
                  {{ track }}
                </li>
              </ul>
            </section>

            <section class="detail-section">
              <div class="section-header">
                <div class="section-icon"><el-icon size="18"><Clock /></el-icon></div>
                <h2>时间安排</h2>
              </div>
              <div class="timeline">
                <div
                  v-for="(item, idx) in competition.schedule"
                  :key="idx"
                  class="timeline-item"
                >
                  <div class="timeline-dot"></div>
                  <div class="timeline-line" v-if="idx < competition.schedule.length - 1"></div>
                  <div class="timeline-content">
                    <h4 class="timeline-name">{{ item.name }}</h4>
                    <span class="timeline-date">{{ item.date }}</span>
                    <p class="timeline-desc">{{ item.desc }}</p>
                  </div>
                </div>
              </div>
            </section>

            <section class="detail-section">
              <div class="section-header">
                <div class="section-icon"><el-icon size="18"><Trophy /></el-icon></div>
                <h2>奖项设置</h2>
              </div>
              <ul class="section-list">
                <li v-for="(award, idx) in competition.awards" :key="idx">
                  <span class="list-marker"></span>
                  {{ award }}
                </li>
              </ul>
            </section>

            <section class="detail-section">
              <div class="section-header">
                <div class="section-icon"><el-icon size="18"><List /></el-icon></div>
                <h2>参赛要求</h2>
              </div>
              <ul class="section-list">
                <li v-for="(req, idx) in competition.requirements" :key="idx">
                  <span class="list-marker"></span>
                  {{ req }}
                </li>
              </ul>
            </section>

            <section class="detail-section">
              <div class="section-header">
                <div class="section-icon"><el-icon size="18"><Folder /></el-icon></div>
                <h2>材料要求</h2>
              </div>
              <ul class="section-list">
                <li v-for="(mat, idx) in competition.materials" :key="idx">
                  <span class="list-marker"></span>
                  {{ mat }}
                </li>
              </ul>
            </section>

            <section class="detail-section official-section">
              <div class="section-header">
                <div class="section-icon"><el-icon size="18"><Link /></el-icon></div>
                <h2>官方入口</h2>
              </div>
              <p class="section-text">请通过官方网站获取最新赛事通知、报名入口和详细要求。</p>
              <el-button type="warning" size="large" class="official-section-btn" @click="openOfficial(competition.officialUrl)">
                <el-icon><Link /></el-icon>
                前往官网
              </el-button>
            </section>
          </div>
        </el-col>

        <el-col :span="8">
          <div class="sidebar-cards">
            <div class="sidebar-card info-card">
              <div class="sidebar-card-header">
                <el-icon size="16"><InfoFilled /></el-icon>
                <span>赛事信息</span>
              </div>
              <div class="sidebar-card-body">
                <div class="info-row">
                  <span class="info-label">赛事级别</span>
                  <span class="info-value highlight">{{ competition.level }}</span>
                </div>
                <div class="info-row">
                  <span class="info-label">主办/组织</span>
                  <span class="info-value">{{ competition.organizer }}</span>
                </div>
                <div class="info-row">
                  <span class="info-label">关注时间</span>
                  <span class="info-value">{{ competition.timeText }}</span>
                </div>
                <div class="info-row">
                  <span class="info-label">赛事类别</span>
                  <span class="info-value">{{ competition.category }}</span>
                </div>
                <div class="info-row">
                  <span class="info-label">报名方式</span>
                  <span class="info-value">官网报名 / 学校组织推荐</span>
                </div>
              </div>
            </div>

            <div class="sidebar-card action-card">
              <el-button
                type="warning"
                size="large"
                class="sidebar-official-btn"
                @click="openOfficial(competition.officialUrl)"
              >
                <el-icon><Link /></el-icon>
                前往官网
              </el-button>
              <p class="action-tip">
                <el-icon size="14"><WarningFilled /></el-icon>
                校外竞赛报名以主办方官网或学校通知为准
              </p>
            </div>

            <div class="sidebar-card tag-card">
              <div class="sidebar-card-header">
                <el-icon size="16"><Collection /></el-icon>
                <span>赛事标签</span>
              </div>
              <div class="tag-list">
                <span v-for="tag in competition.tags" :key="tag" class="tag-item">{{ tag }}</span>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>

  <div v-else class="not-found">
    <div class="not-found-content">
      <el-icon size="64"><FolderOpened /></el-icon>
      <h2>未找到该校外竞赛</h2>
      <p>该赛事可能已下架或不存在</p>
      <el-button type="primary" size="large" @click="$router.push('/external-competitions')">
        返回校外竞赛
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { getCompetitionBySlug } from '@/data/externalCompetitions'
import {
  ArrowRight, Link, Document, Grid, Clock, Trophy,
  List, Folder, InfoFilled, WarningFilled, Collection, FolderOpened
} from '@element-plus/icons-vue'

const route = useRoute()
const competition = computed(() => getCompetitionBySlug(route.params.slug))

function openOfficial(url) {
  window.open(url, '_blank', 'noopener,noreferrer')
}
</script>

<style scoped>
.external-detail { min-height: 100vh; background: #f8fafc; }

/* ========== Hero ========== */
.detail-hero {
  position: relative;
  width: 100%;
  min-height: 520px;
  overflow: hidden;
}

.hero-image {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    180deg,
    rgba(15, 23, 42, 0.08) 0%,
    rgba(15, 23, 42, 0.28) 48%,
    rgba(15, 23, 42, 0.72) 100%
  );
  pointer-events: none;
}

.hero-content {
  position: absolute;
  left: 48px;
  right: 48px;
  bottom: 40px;
  z-index: 2;
  max-width: 800px;
}

.breadcrumb {
  display: flex; align-items: center; gap: 8px; margin-bottom: 20px;
  font-size: 13px;
}

.breadcrumb-link {
  color: rgba(255, 255, 255, 0.7); text-decoration: none;
  transition: color 0.2s ease;
}

.breadcrumb-link:hover { color: #ffffff; }

.breadcrumb-current { color: #ffffff; font-weight: 500; }

.breadcrumb .el-icon { color: rgba(255, 255, 255, 0.5); }

.hero-tags { display: flex; gap: 10px; margin-bottom: 16px; }

.hero-tag {
  padding: 5px 14px; border-radius: 10px;
  font-size: 12px; font-weight: 600;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(8px);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.25);
}

.level-tag { background: rgba(245, 158, 11, 0.3); }

.hero-title {
  font-size: 32px; font-weight: 700; color: #ffffff;
  margin-bottom: 12px; line-height: 1.4;
}

.hero-organizer {
  font-size: 15px; color: rgba(255, 255, 255, 0.85); margin-bottom: 6px;
}

.hero-time {
  font-size: 13px; color: rgba(255, 255, 255, 0.65); margin-bottom: 24px;
}

.hero-action { margin-top: 8px; }

.official-hero-btn {
  display: flex; align-items: center; gap: 8px;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  border: none; color: #ffffff;
  font-weight: 600; border-radius: 14px; padding: 14px 32px;
  transition: all 0.3s ease;
}

.official-hero-btn:hover {
  background: linear-gradient(135deg, #1d4ed8, #6d28d9);
  box-shadow: 0 8px 24px rgba(37, 99, 235, 0.35);
  transform: translateY(-2px);
}

/* ========== Body ========== */
.detail-body {
  max-width: 1200px; margin: 0 auto; padding: 32px 24px 60px;
}

.content-sections { display: flex; flex-direction: column; gap: 20px; }

/* ========== Section ========== */
.detail-section {
  background: #ffffff; border-radius: 18px;
  padding: 28px; border: 1px solid #e2e8f0;
}

.section-header {
  display: flex; align-items: center; gap: 12px; margin-bottom: 18px;
}

.section-icon {
  width: 36px; height: 36px; border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  background: linear-gradient(135deg, #eff6ff, #eef2ff);
  color: #4f46e5;
}

.section-header h2 {
  font-size: 18px; font-weight: 700; color: #0f172a;
}

.section-text {
  font-size: 14px; color: #475569; line-height: 1.8;
}

.section-list {
  list-style: none; padding: 0; margin: 0;
  display: flex; flex-direction: column; gap: 12px;
}

.section-list li {
  display: flex; align-items: flex-start; gap: 10px;
  font-size: 14px; color: #475569; line-height: 1.6;
}

.list-marker {
  width: 6px; height: 6px; border-radius: 50%;
  background: #4f46e5; margin-top: 8px; flex-shrink: 0;
}

/* ========== Timeline ========== */
.timeline {
  position: relative; padding-left: 8px;
}

.timeline-item {
  position: relative; padding-left: 28px; padding-bottom: 20px;
}

.timeline-item:last-child { padding-bottom: 0; }

.timeline-dot {
  position: absolute; left: 0; top: 6px;
  width: 12px; height: 12px; border-radius: 50%;
  background: #4f46e5; border: 2px solid #eef2ff;
  z-index: 1;
}

.timeline-line {
  position: absolute; left: 5px; top: 18px; bottom: 0;
  width: 2px; background: #e2e8f0;
}

.timeline-content { }

.timeline-name {
  font-size: 15px; font-weight: 600; color: #0f172a; margin-bottom: 4px;
}

.timeline-date {
  display: inline-block; font-size: 12px; color: #6366f1;
  background: #eef2ff; padding: 2px 10px; border-radius: 8px;
  margin-bottom: 6px;
}

.timeline-desc {
  font-size: 13px; color: #64748b; line-height: 1.5;
}

/* ========== Official Section ========== */
.official-section {
  background: linear-gradient(135deg, #fffbeb, #fef3c7);
  border: 1px solid #fde68a;
}

.official-section .section-icon {
  background: linear-gradient(135deg, #fef3c7, #fde68a);
  color: #d97706;
}

.official-section-btn {
  display: flex; align-items: center; gap: 8px; margin-top: 14px;
  background: #f59e0b; border: none; color: #1e293b;
  font-weight: 600; border-radius: 12px; padding: 12px 28px;
  transition: all 0.3s ease;
}

.official-section-btn:hover {
  background: #fbbf24;
  box-shadow: 0 6px 20px rgba(245, 158, 11, 0.3);
  transform: translateY(-1px);
}

/* ========== Sidebar ========== */
.sidebar-cards {
  display: flex; flex-direction: column; gap: 16px;
  position: sticky; top: 80px;
}

.sidebar-card {
  background: #ffffff; border-radius: 16px;
  border: 1px solid #e2e8f0; overflow: hidden;
}

.sidebar-card-header {
  display: flex; align-items: center; gap: 8px;
  padding: 16px 20px; border-bottom: 1px solid #f1f5f9;
  font-size: 14px; font-weight: 600; color: #0f172a;
}

.sidebar-card-header .el-icon { color: #4f46e5; }

.sidebar-card-body { padding: 16px 20px; }

.info-row {
  display: flex; justify-content: space-between; align-items: flex-start;
  padding: 8px 0; border-bottom: 1px solid #f8fafc;
}

.info-row:last-child { border-bottom: none; }

.info-label {
  font-size: 13px; color: #94a3b8; flex-shrink: 0;
}

.info-value {
  font-size: 13px; color: #475569; text-align: right;
  max-width: 60%; line-height: 1.5;
}

.info-value.highlight {
  color: #d97706; font-weight: 600;
}

/* ========== Action Card ========== */
.action-card {
  padding: 20px; text-align: center;
}

.sidebar-official-btn {
  width: 100%; display: flex; align-items: center; justify-content: center; gap: 8px;
  background: #f59e0b; border: none; color: #1e293b;
  font-weight: 600; border-radius: 12px; padding: 14px 20px;
  transition: all 0.3s ease;
}

.sidebar-official-btn:hover {
  background: #fbbf24;
  box-shadow: 0 6px 20px rgba(245, 158, 11, 0.3);
}

.action-tip {
  display: flex; align-items: center; justify-content: center; gap: 6px;
  margin-top: 12px; font-size: 12px; color: #92400e;
}

.action-tip .el-icon { color: #f59e0b; }

/* ========== Tag Card ========== */
.tag-list {
  padding: 12px 20px 16px; display: flex; flex-wrap: wrap; gap: 8px;
}

.tag-item {
  padding: 5px 12px; border-radius: 10px;
  background: #f1f5f9; color: #475569;
  font-size: 12px; font-weight: 500;
}

/* ========== Not Found ========== */
.not-found {
  min-height: 80vh;
  display: flex; align-items: center; justify-content: center;
  background: #f8fafc;
}

.not-found-content {
  text-align: center;
}

.not-found-content .el-icon {
  color: #cbd5e1; margin-bottom: 16px;
}

.not-found-content h2 {
  font-size: 22px; color: #0f172a; margin-bottom: 8px;
}

.not-found-content p {
  font-size: 14px; color: #64748b; margin-bottom: 24px;
}

/* ========== 响应式 ========== */
@media (max-width: 768px) {
  .detail-hero { min-height: 420px; }
  .hero-content { left: 24px; right: 24px; bottom: 32px; }
  .hero-title { font-size: 24px; }

  .detail-body { padding: 24px 16px 48px; }

  .sidebar-cards {
    margin-top: 20px; position: static;
  }

  .detail-section { padding: 20px; }

  .official-hero-btn { width: 100%; justify-content: center; }
}
</style>