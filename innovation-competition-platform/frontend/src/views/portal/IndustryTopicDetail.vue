<template>
  <div class="topic-detail" v-if="topic">
    <div class="detail-hero" :class="{ 'has-image': topic.posterImage }">
      <img v-if="topic.posterImage" class="hero-image" :src="topic.posterImage" :alt="topic.title" />
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <div class="breadcrumb">
          <router-link to="/portal" class="breadcrumb-link">首页</router-link>
          <el-icon size="12"><ArrowRight /></el-icon>
          <router-link to="/industry-topics" class="breadcrumb-link">产业命题</router-link>
          <el-icon size="12"><ArrowRight /></el-icon>
          <span class="breadcrumb-current">{{ topic.title }}</span>
        </div>
        <div class="hero-tags">
          <span class="hero-tag industry-tag">
            <el-icon size="12"><OfficeBuilding /></el-icon>
            {{ topic.company }}
          </span>
          <span class="hero-tag" :class="difficultyTagClass">{{ topic.difficulty }}</span>
          <span class="hero-tag status-tag">{{ topic.status }}</span>
        </div>
        <h1 class="hero-title">{{ topic.title }}</h1>
        <p class="hero-summary">{{ topic.summary }}</p>
        <div class="hero-meta">
          <span class="hero-meta-item">
            <el-icon size="14"><Timer /></el-icon>
            {{ topic.duration }}
          </span>
          <span class="hero-meta-item">
            <el-icon size="14"><Coin /></el-icon>
            {{ topic.reward }}
          </span>
          <span class="hero-meta-item">
            <el-icon size="14"><TrendCharts /></el-icon>
            {{ topic.difficulty }}
          </span>
        </div>
        <div class="hero-action">
          <el-button type="primary" size="large" class="hero-accept-btn" @click="handleAccept">
            <el-icon><MagicStick /></el-icon>
            承接命题
          </el-button>
          <el-button size="large" class="hero-back-btn" @click="$router.back()">
            <el-icon><ArrowLeft /></el-icon>
            返回列表
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
                <h2>命题背景</h2>
              </div>
              <p class="section-text">{{ topic.background }}</p>
            </section>

            <section class="detail-section">
              <div class="section-header">
                <div class="section-icon"><el-icon size="18"><List /></el-icon></div>
                <h2>需求说明</h2>
              </div>
              <ul class="section-list">
                <li v-for="(req, idx) in topic.requirements" :key="idx">
                  <span class="list-marker"></span>
                  {{ req }}
                </li>
              </ul>
            </section>

            <section class="detail-section">
              <div class="section-header">
                <div class="section-icon"><el-icon size="18"><Cpu /></el-icon></div>
                <h2>技术方向</h2>
              </div>
              <div class="tech-tags">
                <span v-for="tech in topic.techDirections" :key="tech" class="tech-tag">{{ tech }}</span>
              </div>
            </section>

            <section class="detail-section">
              <div class="section-header">
                <div class="section-icon"><el-icon size="18"><Folder /></el-icon></div>
                <h2>交付物要求</h2>
              </div>
              <ul class="section-list">
                <li v-for="(item, idx) in topic.deliverables" :key="idx">
                  <span class="list-marker"></span>
                  {{ item }}
                </li>
              </ul>
            </section>

            <section class="detail-section">
              <div class="section-header">
                <div class="section-icon"><el-icon size="18"><Clock /></el-icon></div>
                <h2>周期安排</h2>
              </div>
              <div class="timeline">
                <div
                  v-for="(item, idx) in topic.schedule"
                  :key="idx"
                  class="timeline-item"
                >
                  <div class="timeline-dot"></div>
                  <div class="timeline-line" v-if="idx < topic.schedule.length - 1"></div>
                  <div class="timeline-content">
                    <h4 class="timeline-name">{{ item.name }}</h4>
                    <span class="timeline-date">{{ item.time }}</span>
                    <p class="timeline-desc">{{ item.desc }}</p>
                  </div>
                </div>
              </div>
            </section>

            <section class="detail-section reward-section">
              <div class="section-header">
                <div class="section-icon"><el-icon size="18"><Trophy /></el-icon></div>
                <h2>奖励与支持</h2>
              </div>
              <div class="reward-highlight">
                <el-icon size="22"><Coin /></el-icon>
                <span class="reward-amount">{{ topic.reward }}</span>
              </div>
              <ul class="section-list">
                <li v-for="(item, idx) in topic.support" :key="idx">
                  <span class="list-marker"></span>
                  {{ item }}
                </li>
              </ul>
            </section>

            <section class="detail-section">
              <div class="section-header">
                <div class="section-icon"><el-icon size="18"><Avatar /></el-icon></div>
                <h2>适合团队</h2>
              </div>
              <div class="team-grid">
                <div class="team-info-item">
                  <span class="team-label">建议人数</span>
                  <span class="team-value">{{ topic.suitableTeam.members }}</span>
                </div>
                <div class="team-info-item">
                  <span class="team-label">角色构成</span>
                  <span class="team-value">{{ topic.suitableTeam.roles.join('、') }}</span>
                </div>
                <div class="team-info-item">
                  <span class="team-label">适合专业</span>
                  <span class="team-value">{{ topic.suitableTeam.majors.join('、') }}</span>
                </div>
                <div class="team-info-item">
                  <span class="team-label">指导老师</span>
                  <span class="team-value">{{ topic.suitableTeam.needAdvisor ? '建议配备' : '不强制要求' }}</span>
                </div>
              </div>
            </section>

            <section class="detail-section">
              <div class="section-header">
                <div class="section-icon"><el-icon size="18"><Checked /></el-icon></div>
                <h2>评分 / 验收标准</h2>
              </div>
              <ul class="section-list">
                <li v-for="(item, idx) in topic.evaluation" :key="idx">
                  <span class="list-marker"></span>
                  {{ item }}
                </li>
              </ul>
            </section>

            <section class="detail-section accept-bottom-section">
              <div class="accept-bottom-content">
                <h3>准备好迎接挑战了吗？</h3>
                <p>仔细阅读命题要求后，点击下方按钮正式承接命题，开启你的企业真实项目之旅。</p>
                <el-button type="primary" size="large" class="accept-bottom-btn" @click="handleAccept">
                  <el-icon><MagicStick /></el-icon>
                  承接命题
                </el-button>
              </div>
            </section>

          </div>
        </el-col>

        <el-col :span="8">
          <div class="sidebar-cards">
            <div class="sidebar-card info-card">
              <div class="sidebar-card-header">
                <el-icon size="16"><InfoFilled /></el-icon>
                <span>命题信息</span>
              </div>
              <div class="sidebar-card-body">
                <div class="info-row">
                  <span class="info-label">发布单位</span>
                  <span class="info-value highlight">{{ topic.company }}</span>
                </div>
                <div class="info-row">
                  <span class="info-label">领域</span>
                  <span class="info-value">{{ topic.category }}</span>
                </div>
                <div class="info-row">
                  <span class="info-label">难度</span>
                  <span class="info-value" :class="difficultyTextClass">{{ topic.difficulty }}</span>
                </div>
                <div class="info-row">
                  <span class="info-label">周期</span>
                  <span class="info-value">{{ topic.duration }}</span>
                </div>
                <div class="info-row">
                  <span class="info-label">预算</span>
                  <span class="info-value highlight">{{ topic.budget }}</span>
                </div>
                <div class="info-row">
                  <span class="info-label">状态</span>
                  <span class="info-value status-open">{{ topic.status }}</span>
                </div>
              </div>
            </div>

            <div class="sidebar-card action-card">
              <el-button
                type="primary"
                size="large"
                class="sidebar-accept-btn"
                @click="handleAccept"
              >
                <el-icon><MagicStick /></el-icon>
                承接命题
              </el-button>
              <el-button
                size="large"
                class="sidebar-back-btn"
                @click="$router.back()"
              >
                <el-icon><ArrowLeft /></el-icon>
                返回列表
              </el-button>
              <p class="action-tip">
                <el-icon size="14"><WarningFilled /></el-icon>
                承接命题后将为你创建关联项目
              </p>
            </div>

            <div class="sidebar-card tag-card">
              <div class="sidebar-card-header">
                <el-icon size="16"><Collection /></el-icon>
                <span>命题标签</span>
              </div>
              <div class="tag-list">
                <span v-for="tag in topic.tags" :key="tag" class="tag-item">{{ tag }}</span>
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
      <h2>未找到该产业命题</h2>
      <p>该命题可能已下架或不存在，请返回产业命题列表查看更多命题</p>
      <el-button type="primary" size="large" @click="$router.push('/industry-topics')">
        返回产业命题
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getIndustryTopicById } from '@/data/industryTopics'
import {
  ArrowRight, ArrowLeft, OfficeBuilding, Timer, Coin, TrendCharts,
  Document, List, Cpu, Folder, Clock, Trophy, Avatar, Checked,
  InfoFilled, WarningFilled, Collection, FolderOpened, MagicStick
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const topic = computed(() => getIndustryTopicById(route.params.id))

const difficultyTagClass = computed(() => {
  if (!topic.value) return ''
  const map = { '简单': 'diff-easy', '中等': 'diff-medium', '困难': 'diff-hard' }
  return map[topic.value.difficulty] || ''
})

const difficultyTextClass = computed(() => {
  if (!topic.value) return ''
  const map = { '简单': 'text-easy', '中等': 'text-medium', '困难': 'text-hard' }
  return map[topic.value.difficulty] || ''
})

function handleAccept() {
  if (!topic.value) return
  router.push({
    path: `/accept-topic/${topic.value.id}`,
    query: {
      topic_title: topic.value.title,
      topic_company: topic.value.company
    }
  })
}
</script>

<style scoped>
.topic-detail { min-height: 100vh; background: #f8fafc; }

/* ========== Hero ========== */
.detail-hero {
  position: relative;
  width: 100%;
  background: #0f172a;
}

.hero-image {
  width: 100%;
  height: auto;
  object-fit: contain;
  display: block;
  aspect-ratio: 16 / 9;
  border-radius: 0;
}

.hero-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
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

.breadcrumb-current { color: #ffffff; font-weight: 500; max-width: 300px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

.breadcrumb .el-icon { color: rgba(255, 255, 255, 0.5); }

.hero-tags { display: flex; gap: 10px; margin-bottom: 16px; flex-wrap: wrap; }

.hero-tag {
  padding: 5px 14px; border-radius: 10px;
  font-size: 12px; font-weight: 600;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(8px);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.25);
  display: flex; align-items: center; gap: 4px;
}

.industry-tag { background: rgba(255, 255, 255, 0.18); }

.status-tag { background: rgba(34, 211, 238, 0.3); }

.diff-easy { background: rgba(34, 197, 94, 0.35); }
.diff-medium { background: rgba(245, 158, 11, 0.35); }
.diff-hard { background: rgba(239, 68, 68, 0.35); }

.hero-title {
  font-size: 36px; font-weight: 800; color: #ffffff;
  margin-bottom: 14px; line-height: 1.3;
}

.hero-summary {
  font-size: 15px; color: rgba(255, 255, 255, 0.82);
  margin-bottom: 20px; line-height: 1.7; max-width: 680px;
}

.hero-meta {
  display: flex; gap: 24px; margin-bottom: 28px; flex-wrap: wrap;
}

.hero-meta-item {
  display: flex; align-items: center; gap: 6px;
  font-size: 13px; color: rgba(255, 255, 255, 0.78);
}

.hero-meta-item .el-icon { color: rgba(255, 255, 255, 0.6); }

.hero-action {
  display: flex; gap: 12px; flex-wrap: wrap;
}

.hero-accept-btn {
  display: flex; align-items: center; gap: 8px;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  border: none; color: #ffffff;
  font-weight: 600; border-radius: 14px; padding: 14px 32px;
  transition: all 0.3s ease;
}

.hero-accept-btn:hover {
  background: linear-gradient(135deg, #1d4ed8, #6d28d9);
  box-shadow: 0 8px 24px rgba(37, 99, 235, 0.4);
  transform: translateY(-2px);
}

.hero-back-btn {
  display: flex; align-items: center; gap: 8px;
  background: rgba(255, 255, 255, 0.14);
  border: 1px solid rgba(255, 255, 255, 0.25);
  color: #ffffff;
  font-weight: 500; border-radius: 14px; padding: 14px 24px;
  transition: all 0.3s ease;
}

.hero-back-btn:hover {
  background: rgba(255, 255, 255, 0.22);
  border-color: rgba(255, 255, 255, 0.4);
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

/* ========== Tech Tags ========== */
.tech-tags {
  display: flex; flex-wrap: wrap; gap: 8px;
}

.tech-tag {
  padding: 6px 14px; border-radius: 10px;
  background: linear-gradient(135deg, #eff6ff, #eef2ff);
  color: #4338ca; font-size: 13px; font-weight: 500;
  border: 1px solid #e0e7ff;
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

/* ========== Reward Section ========== */
.reward-section {
  background: linear-gradient(135deg, #fefce8, #fef9c3);
  border: 1px solid #fef08a;
}

.reward-section .section-icon {
  background: linear-gradient(135deg, #fef3c7, #fde68a);
  color: #d97706;
}

.reward-highlight {
  display: flex; align-items: center; gap: 10px;
  padding: 14px 18px; margin-bottom: 16px;
  background: #ffffff; border-radius: 12px;
  border: 2px solid #fef08a;
}

.reward-highlight .el-icon { color: #d97706; }

.reward-amount {
  font-size: 18px; font-weight: 700; color: #92400e;
}

/* ========== Team Grid ========== */
.team-grid {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.team-info-item {
  padding: 14px; border-radius: 12px;
  background: #f8fafc; border: 1px solid #e2e8f0;
}

.team-label {
  display: block; font-size: 12px; color: #94a3b8;
  margin-bottom: 6px; font-weight: 500;
}

.team-value {
  font-size: 14px; color: #0f172a; font-weight: 600;
  line-height: 1.5;
}

/* ========== Bottom Accept Section ========== */
.accept-bottom-section {
  background: linear-gradient(135deg, #eff6ff, #eef2ff);
  border: 2px solid #c7d2fe;
}

.accept-bottom-content {
  text-align: center;
}

.accept-bottom-content h3 {
  font-size: 20px; font-weight: 700; color: #0f172a; margin-bottom: 8px;
}

.accept-bottom-content p {
  font-size: 14px; color: #64748b; margin-bottom: 20px; max-width: 480px;
  margin-left: auto; margin-right: auto; line-height: 1.6;
}

.accept-bottom-btn {
  display: inline-flex; align-items: center; gap: 8px;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  border: none; color: #ffffff;
  font-weight: 600; border-radius: 14px; padding: 14px 36px;
  transition: all 0.3s ease;
}

.accept-bottom-btn:hover {
  background: linear-gradient(135deg, #1d4ed8, #6d28d9);
  box-shadow: 0 8px 24px rgba(37, 99, 235, 0.35);
  transform: translateY(-2px);
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
  color: #4f46e5; font-weight: 600;
}

.text-easy { color: #16a34a; font-weight: 600; }
.text-medium { color: #d97706; font-weight: 600; }
.text-hard { color: #dc2626; font-weight: 600; }

.status-open { color: #0ea5e9; font-weight: 600; }

/* ========== Action Card ========== */
.action-card {
  padding: 20px; text-align: center;
}

.sidebar-accept-btn {
  width: 100%; display: flex; align-items: center; justify-content: center; gap: 8px;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  border: none; color: #ffffff;
  font-weight: 600; border-radius: 12px; padding: 14px 20px;
  transition: all 0.3s ease; margin-bottom: 10px;
}

.sidebar-accept-btn:hover {
  background: linear-gradient(135deg, #1d4ed8, #6d28d9);
  box-shadow: 0 6px 20px rgba(37, 99, 235, 0.35);
  transform: translateY(-1px);
}

.sidebar-back-btn {
  width: 100%; display: flex; align-items: center; justify-content: center; gap: 8px;
  background: #f8fafc; border: 1px solid #e2e8f0;
  color: #475569; font-weight: 500; border-radius: 12px;
  padding: 12px 20px; margin-bottom: 12px;
  transition: all 0.3s ease;
}

.sidebar-back-btn:hover {
  background: #f1f5f9; border-color: #cbd5e1; color: #0f172a;
}

.action-tip {
  display: flex; align-items: center; justify-content: center; gap: 6px;
  font-size: 12px; color: #64748b;
}

.action-tip .el-icon { color: #94a3b8; }

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

  .hero-summary { font-size: 13px; }

  .hero-meta { gap: 14px; }

  .hero-action { flex-direction: column; }

  .hero-accept-btn, .hero-back-btn { width: 100%; justify-content: center; }

  .detail-body { padding: 24px 16px 48px; }

  .sidebar-cards {
    margin-top: 20px; position: static;
  }

  .detail-section { padding: 20px; }

  .team-grid { grid-template-columns: 1fr; }
}
</style>