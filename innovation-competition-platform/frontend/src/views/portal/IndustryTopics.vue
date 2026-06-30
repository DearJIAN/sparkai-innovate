<template>
  <div class="industry-topics">
    <!-- Banner -->
    <div class="portal-hero-banner portal-hero-banner--industry">
      <div class="banner-decoration">
        <div class="deco-circle c1"></div>
        <div class="deco-circle c2"></div>
      </div>
      <div class="banner-content">
        <div class="banner-badge">
          <el-icon size="16"><HomeFilled /></el-icon>
          <span>产业命题</span>
        </div>
        <h1 class="banner-title">产业命题</h1>
        <p class="banner-subtitle">对接企业真实需求，解决实际业务问题</p>
      </div>
    </div>

    <!-- 命题列表 -->
    <div class="topics-section">
      <div class="topics-grid">
        <SparkPortalCard
          v-for="topic in topics"
          :key="topic.id"
          :gradient="topic.gradient"
          :cover-image="topic.posterImage"
          :level="topic.difficulty"
          :title="topic.title"
          :description="'命题企业：' + topic.company + ' / ' + (topic.summary || '').substring(0, 80) + '...'"
          :tags="[topic.company, topic.industry]"
          :max-tags="2"
          :meta-items="[
            { icon: Timer, text: topic.duration },
            { icon: View, text: topic.viewCount + ' 浏览' },
            { icon: User, text: topic.acceptCount + ' 人承接' }
          ]"
          :primary-action-text="canAccept ? '承接命题' : '当前角色不可承接'"
          :primary-action-icon="ArrowRight"
          :secondary-action-text="'查看详情'"
          :secondary-action-icon="View"
          :on-primary-click="() => handleAccept(topic)"
          :on-secondary-click="() => goDetail(topic)"
          :on-card-click="() => goDetail(topic)"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { Timer, ArrowRight, View, HomeFilled, User } from '@element-plus/icons-vue'
import SparkPortalCard from '@/components/portal/SparkPortalCard.vue'
import { industryTopics as topics } from '@/data/industryTopics'
import { useUserStore } from '@/stores/user'
import { computed } from 'vue'

const router = useRouter()
const userStore = useUserStore()
const canAccept = computed(() => userStore.isStudent)

const goDetail = (topic) => {
  router.push(`/industry-topics/${topic.id}`)
}

const handleAccept = (topic) => {
  router.push({
    path: `/accept-topic/${topic.id}`,
    query: {
      topic_title: topic.title,
      topic_company: topic.company
    }
  })
}
</script>

<style scoped>
.industry-topics {
  min-height: 100vh;
  background: linear-gradient(180deg, #f0f9ff 0%, #ffffff 100%);
}

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

.portal-hero-banner--industry {
  background: linear-gradient(135deg, #0f172a 0%, #0e7490 100%);
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

.topics-section {
  padding: 40px;
  max-width: 1400px;
  margin: 0 auto;
}

.topics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 24px;
}

@media (max-width: 768px) {
  .topics-grid { grid-template-columns: 1fr; }
}
</style>
