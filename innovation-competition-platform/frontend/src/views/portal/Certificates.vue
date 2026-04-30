<template>
  <div class="certificates-page">
    <!-- Banner -->
    <div class="certificates-banner">
      <div class="banner-content">
        <h1 class="banner-title">证书与成果</h1>
        <p class="banner-subtitle">记录你的成长轨迹，展示你的竞赛成果</p>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-section">
      <div class="stats-grid">
        <div class="stat-card">
          <el-icon size="32" color="#0ea5e9"><Trophy /></el-icon>
          <div class="stat-value">{{ stats.competitions }}</div>
          <div class="stat-label">参赛次数</div>
        </div>
        <div class="stat-card">
          <el-icon size="32" color="#10b981"><Medal /></el-icon>
          <div class="stat-value">{{ stats.awards }}</div>
          <div class="stat-label">获奖次数</div>
        </div>
        <div class="stat-card">
          <el-icon size="32" color="#8b5cf6"><DocumentChecked /></el-icon>
          <div class="stat-value">{{ stats.certificates }}</div>
          <div class="stat-label">获得证书</div>
        </div>
        <div class="stat-card">
          <el-icon size="32" color="#f59e0b"><Star /></el-icon>
          <div class="stat-value">{{ stats.points }}</div>
          <div class="stat-label">积分</div>
        </div>
      </div>
    </div>

    <!-- 证书列表 -->
    <div class="certificates-section">
      <h2 class="section-title">我的证书</h2>
      <div class="certificates-grid">
        <div
          v-for="cert in certificates"
          :key="cert.id"
          class="certificate-card"
        >
          <div class="cert-icon" :style="{ background: cert.gradient }">
            <el-icon size="32"><component :is="cert.icon" /></el-icon>
          </div>
          <div class="cert-body">
            <h3 class="cert-title">{{ cert.title }}</h3>
            <p class="cert-issuer">颁发机构：{{ cert.issuer }}</p>
            <p class="cert-date">获得时间：{{ cert.date }}</p>
            <el-tag :type="cert.statusType" size="small">{{ cert.status }}</el-tag>
          </div>
        </div>
      </div>

      <el-empty
        v-if="certificates.length === 0"
        description="暂无证书"
        :image-size="120"
      />
    </div>

    <!-- 获奖记录 -->
    <div class="awards-section">
      <h2 class="section-title">获奖记录</h2>
      <div class="awards-list">
        <div
          v-for="award in awards"
          :key="award.id"
          class="award-card"
        >
          <div class="award-badge" :class="`award-${award.level}`">
            {{ award.levelText }}
          </div>
          <div class="award-body">
            <h4 class="award-title">{{ award.competition }}</h4>
            <p class="award-project">项目：{{ award.project }}</p>
            <p class="award-date">获奖时间：{{ award.date }}</p>
          </div>
        </div>
      </div>

      <el-empty
        v-if="awards.length === 0"
        description="暂无获奖记录"
        :image-size="120"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Trophy, Medal, DocumentChecked, Star } from '@element-plus/icons-vue'

const stats = ref({
  competitions: 5,
  awards: 2,
  certificates: 3,
  points: 1280
})

const certificates = ref([
  {
    id: 1,
    title: '创新创业基础训练营结业证书',
    issuer: '校团委创新创业中心',
    date: '2026-03-15',
    status: '已发放',
    statusType: 'success',
    icon: 'DocumentChecked',
    gradient: 'linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%)'
  },
  {
    id: 2,
    title: 'AI 项目孵化训练营结业证书',
    issuer: '人工智能学院',
    date: '2026-02-28',
    status: '已发放',
    statusType: 'success',
    icon: 'DocumentChecked',
    gradient: 'linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%)'
  },
  {
    id: 3,
    title: '商业计划书写作训练营结业证书',
    issuer: '经济管理学院',
    date: '2026-01-20',
    status: '已发放',
    statusType: 'success',
    icon: 'DocumentChecked',
    gradient: 'linear-gradient(135deg, #10b981 0%, #14b8a6 100%)'
  }
])

const awards = ref([
  {
    id: 1,
    competition: '2025 大学生创新创业计划训练赛',
    project: '智慧校园服务平台',
    level: 'second',
    levelText: '二等奖',
    date: '2025-07-15'
  },
  {
    id: 2,
    competition: '2025 校园电子商务运营挑战赛',
    project: '校园二手交易平台',
    level: 'third',
    levelText: '三等奖',
    date: '2025-05-20'
  }
])
</script>

<style scoped>
.certificates-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #f0f9ff 0%, #ffffff 100%);
}

.certificates-banner {
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

.stats-section {
  padding: 32px 40px;
  max-width: 1400px;
  margin: 0 auto;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.stat-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 24px;
  text-align: center;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.stat-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #1e293b;
  margin: 8px 0;
}

.stat-label {
  font-size: 14px;
  color: #64748b;
}

.certificates-section,
.awards-section {
  padding: 0 40px 32px;
  max-width: 1400px;
  margin: 0 auto;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 20px;
}

.certificates-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.certificate-card {
  display: flex;
  background: #ffffff;
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.certificate-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.cert-icon {
  width: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  flex-shrink: 0;
}

.cert-body {
  padding: 16px;
  flex: 1;
}

.cert-title {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 8px;
}

.cert-issuer,
.cert-date {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 4px;
}

.awards-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.award-card {
  display: flex;
  align-items: center;
  gap: 16px;
  background: #ffffff;
  border-radius: 12px;
  padding: 16px 20px;
  border: 1px solid #e2e8f0;
}

.award-badge {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  color: #ffffff;
  min-width: 60px;
  text-align: center;
}

.award-first {
  background: linear-gradient(135deg, #f59e0b, #fbbf24);
}

.award-second {
  background: linear-gradient(135deg, #94a3b8, #cbd5e1);
}

.award-third {
  background: linear-gradient(135deg, #b45309, #d97706);
}

.award-title {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 4px;
}

.award-project,
.award-date {
  font-size: 13px;
  color: #64748b;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
