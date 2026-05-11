<template>
  <div class="competition-center">
    <div class="center-banner">
      <div class="banner-gradient-bg"></div>
      <div class="banner-bg-pattern"></div>
      <div class="banner-particles">
        <div
          v-for="i in 15"
          :key="'p' + i"
          class="particle"
          :class="[`particle-${((i - 1) % 3) + 1}`]"
          :style="particleStyle(i)"
        ></div>
      </div>
      <div class="banner-content">
        <div class="banner-badge">
          <el-icon size="16"><Trophy /></el-icon>
          <span>竞赛报名中心</span>
        </div>
        <h1 class="banner-title">选择竞赛类型</h1>
        <p class="banner-subtitle">请选择你要浏览的竞赛类别，校外竞赛聚合国家级赛事资讯，校内竞赛支持平台内报名与管理</p>
      </div>
      <div class="banner-decoration">
        <div class="deco-circle c1"></div>
        <div class="deco-circle c2"></div>
        <div class="deco-circle c3"></div>
      </div>
    </div>

    <div class="center-body">
      <div class="entry-grid">
        <div class="entry-card external-card" @click="$router.push('/external-competitions')">
          <div class="card-glow"></div>
          <div class="card-badge">国家级赛事</div>
          <div class="card-icon-wrapper">
            <div class="card-icon-bg">
              <el-icon size="40"><Link /></el-icon>
            </div>
          </div>
          <h2 class="card-title">校外竞赛</h2>
          <p class="card-desc">聚合国家级创新创业赛事，提供官方资讯、赛程赛道、报名入口等参考信息</p>
          <div class="card-features">
            <div class="feature-item">
              <el-icon size="16"><Medal /></el-icon>
              <span>教育部 / 团中央主办</span>
            </div>
            <div class="feature-item">
              <el-icon size="16"><Grid /></el-icon>
              <span>多赛道分类展示</span>
            </div>
            <div class="feature-item">
              <el-icon size="16"><Clock /></el-icon>
              <span>实时赛程关注</span>
            </div>
          </div>
          <div class="card-action">
            <el-button type="primary" size="large" class="action-btn external-btn">
              浏览校外竞赛
              <el-icon><ArrowRight /></el-icon>
            </el-button>
          </div>
        </div>

        <div class="entry-card internal-card" @click="$router.push('/competitions')">
          <div class="card-glow"></div>
          <div class="card-badge">平台赛事</div>
          <div class="card-icon-wrapper">
            <div class="card-icon-bg">
              <el-icon size="40"><School /></el-icon>
            </div>
          </div>
          <h2 class="card-title">校内竞赛</h2>
          <p class="card-desc">本校及学院发布的竞赛活动，支持平台内报名、团队组建、材料上传、评审管理全流程</p>
          <div class="card-features">
            <div class="feature-item">
              <el-icon size="16"><Edit /></el-icon>
              <span>一键在线报名</span>
            </div>
            <div class="feature-item">
              <el-icon size="16"><User /></el-icon>
              <span>团队协作管理</span>
            </div>
            <div class="feature-item">
              <el-icon size="16"><Document /></el-icon>
              <span>材料上传审核</span>
            </div>
          </div>
          <div class="card-action">
            <el-button type="primary" size="large" class="action-btn internal-btn">
              进入校内竞赛
              <el-icon><ArrowRight /></el-icon>
            </el-button>
          </div>
        </div>
      </div>

      <div class="center-tips">
        <el-icon size="18"><WarningFilled /></el-icon>
        <span>校外竞赛报名、截止时间、赛道要求以主办方官网或学校通知为准</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import {
  Trophy, Link, Medal, Grid, Clock, ArrowRight,
  School, Edit, User, Document, WarningFilled
} from '@element-plus/icons-vue'

const particleStyle = (i) => {
  const left = Math.random() * 100
  const top = 60 + Math.random() * 40
  const delay = Math.random() * 8
  const duration = 8 + Math.random() * 7
  const size = 3 + Math.random() * 5
  const opacity = 0.1 + Math.random() * 0.2
  return {
    left: `${left}%`,
    top: `${top}%`,
    width: `${size}px`,
    height: `${size}px`,
    opacity: opacity,
    animationDelay: `${delay}s`,
    animationDuration: `${duration}s`
  }
}
</script>

<style scoped>
.competition-center {
  min-height: 100vh;
  background: linear-gradient(180deg, #f0f9ff 0%, #ffffff 100%);
}

/* ========== Banner ========== */
.center-banner {
  position: relative;
  background: linear-gradient(135deg, #0c4a6e 0%, #075985 50%, #0ea5e9 100%);
  padding: 48px 40px;
  overflow: hidden;
  border-radius: 0 0 32px 32px;
}

.banner-gradient-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #0c4a6e 0%, #075985 25%, #0ea5e9 50%, #06b6d4 75%, #0891b2 100%);
  background-size: 400% 400%;
  animation: gradientShift 12s ease infinite;
  z-index: 0;
}

@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.banner-bg-pattern {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image:
    radial-gradient(circle at 20% 50%, rgba(14, 165, 233, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(139, 92, 246, 0.1) 0%, transparent 50%);
  z-index: 0;
}

.banner-content {
  position: relative;
  z-index: 2;
  max-width: 800px;
}

.banner-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  padding: 6px 14px;
  border-radius: 20px;
  color: #ffffff;
  font-size: 13px;
  font-weight: 500;
  margin-bottom: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.banner-title {
  font-size: 32px;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 10px;
  letter-spacing: 1px;
}

.banner-subtitle {
  font-size: 15px;
  color: #bae6fd;
  line-height: 1.6;
  max-width: 560px;
}

.banner-particles {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  z-index: 1;
}

.particle {
  position: absolute;
  border-radius: 50%;
  animation: particleFloat linear infinite;
}

.particle-1 { background: #0ea5e9; }
.particle-2 { background: #06b6d4; }
.particle-3 { background: #0891b2; }

@keyframes particleFloat {
  0% { transform: translateY(0) translateX(0) scale(1); opacity: var(--particle-opacity, 0.2); }
  50% { transform: translateY(-50%) translateX(-5px) scale(1); opacity: var(--particle-opacity, 0.2); }
  100% { transform: translateY(-100%) translateX(0) scale(1); opacity: var(--particle-opacity, 0.2); }
}

.banner-decoration { position: absolute; right: 40px; top: 0; width: 40%; height: 100%; z-index: 1; }

.deco-circle {
  position: absolute; border-radius: 50%; opacity: 0.15;
}
.c1 { width: 250px; height: 250px; background: #7dd3fc; right: -30px; top: -20px; animation: decoFloat 8s ease-in-out infinite; }
.c2 { width: 180px; height: 180px; background: #38bdf8; right: 120px; bottom: -20px; animation: decoFloat 10s ease-in-out infinite reverse; }
.c3 { width: 120px; height: 120px; background: #0ea5e9; right: 280px; top: 50%; animation: decoFloat 7s ease-in-out infinite; }

@keyframes decoFloat {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-12px) scale(1.05); }
}

/* ========== Body ========== */
.center-body {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 24px 60px;
}

.entry-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 28px;
  margin-bottom: 32px;
}

.entry-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 36px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  border: 1px solid #e2e8f0;
  transition: transform 0.35s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.35s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.35s ease;
}

.entry-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 20px 40px -8px rgba(0, 0, 0, 0.15);
}

.external-card:hover {
  border-color: #818cf8;
  box-shadow: 0 20px 40px -8px rgba(37, 99, 235, 0.18), 0 0 0 1px rgba(124, 58, 237, 0.2);
}

.internal-card:hover {
  border-color: #22d3ee;
  box-shadow: 0 20px 40px -8px rgba(8, 145, 178, 0.18), 0 0 0 1px rgba(6, 182, 212, 0.2);
}

.card-glow {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle at center, rgba(14, 165, 233, 0.03) 0%, transparent 70%);
  pointer-events: none;
  transition: opacity 0.35s ease;
  opacity: 0;
}

.entry-card:hover .card-glow { opacity: 1; }

.card-badge {
  display: inline-block;
  padding: 4px 14px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 20px;
  letter-spacing: 0.5px;
}

.external-card .card-badge {
  background: linear-gradient(135deg, rgba(37, 99, 235, 0.12), rgba(124, 58, 237, 0.12));
  color: #2563eb;
}

.internal-card .card-badge {
  background: linear-gradient(135deg, rgba(8, 145, 178, 0.12), rgba(6, 182, 212, 0.12));
  color: #0891b2;
}

.card-icon-wrapper {
  margin-bottom: 20px;
}

.card-icon-bg {
  width: 72px;
  height: 72px;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.entry-card:hover .card-icon-bg {
  transform: scale(1.08) rotate(3deg);
}

.external-card .card-icon-bg {
  background: linear-gradient(135deg, #eff6ff 0%, #ede9fe 100%);
  color: #4f46e5;
}

.internal-card .card-icon-bg {
  background: linear-gradient(135deg, #ecfeff 0%, #f0f9ff 100%);
  color: #0891b2;
}

.card-title {
  font-size: 24px;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 10px;
}

.card-desc {
  font-size: 14px;
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 24px;
}

.card-features {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 28px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  color: #475569;
  padding: 8px 12px;
  background: #f8fafc;
  border-radius: 10px;
  transition: background 0.25s ease;
}

.external-card .feature-item { color: #475569; }
.internal-card .feature-item { color: #475569; }

.entry-card:hover .feature-item {
  background: #f1f5f9;
}

.card-action { margin-top: auto; }

.action-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 28px;
  border-radius: 14px;
  font-weight: 600;
  font-size: 15px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.entry-card:hover .action-btn {
  transform: translateY(-2px);
}

.external-btn {
  background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
  border: none;
  color: #fff;
}

.external-btn:hover {
  background: linear-gradient(135deg, #1d4ed8 0%, #6d28d9 100%);
  box-shadow: 0 8px 24px rgba(37, 99, 235, 0.3);
}

.internal-btn {
  background: linear-gradient(135deg, #0891b2 0%, #06b6d4 100%);
  border: none;
  color: #fff;
}

.internal-btn:hover {
  background: linear-gradient(135deg, #0e7490 0%, #0891b2 100%);
  box-shadow: 0 8px 24px rgba(8, 145, 178, 0.3);
}

/* ========== Tips ========== */
.center-tips {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 16px 24px;
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.06), rgba(251, 191, 36, 0.06));
  border-radius: 14px;
  color: #92400e;
  font-size: 13px;
  border: 1px solid rgba(245, 158, 11, 0.15);
}

.center-tips .el-icon { color: #f59e0b; flex-shrink: 0; }

/* ========== 响应式 ========== */
@media (max-width: 768px) {
  .center-banner {
    padding: 36px 20px;
    border-radius: 0 0 24px 24px;
  }

  .banner-title { font-size: 24px; }
  .banner-subtitle { font-size: 13px; }

  .banner-decoration { display: none; }

  .entry-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .entry-card { padding: 28px 24px; }
  .card-title { font-size: 20px; }

  .center-body { padding: 28px 16px 48px; }
}

@media (prefers-reduced-motion: reduce) {
  .banner-gradient-bg, .particle, .deco-circle { animation: none !important; }
  .entry-card, .card-icon-bg, .action-btn { transition: none !important; }
}
</style>