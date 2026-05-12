<template>
  <div class="material-evaluation-page">
    <div class="me-hero">
      <div class="me-hero-bg"></div>
      <div class="me-hero-content">
        <div class="me-hero-badge">
          <el-icon size="16"><Cpu /></el-icon>
          <span>AI 智能分析</span>
        </div>
        <h1 class="me-hero-title">AI材料评估中心</h1>
        <p class="me-hero-subtitle">
          上传PDF材料，获取PPT表现力与项目报告质量的智能评分建议
        </p>
        <p class="me-hero-desc">
          支持路演PPT、商业计划书、项目申报书等材料导出的PDF文件
        </p>
      </div>
      <div class="me-hero-float">
        <div class="me-float-ring r1"></div>
        <div class="me-float-ring r2"></div>
        <div class="me-float-dot d1"></div>
        <div class="me-float-dot d2"></div>
        <div class="me-float-dot d3"></div>
      </div>
    </div>

    <div class="me-cards-section">
      <h2 class="me-section-title">选择评估类型</h2>
      <p class="me-section-desc">PPT评估与报告评估互不依赖，可独立使用</p>
      <div class="me-cards">
        <div class="me-card ppt-card" @click="goUpload('ppt')">
          <div class="me-card-header">
            <div class="me-card-icon-wrapper ppt-icon">
              <el-icon size="28"><Present /></el-icon>
            </div>
            <span class="me-card-badge ppt-badge">PPT评估</span>
          </div>
          <h3 class="me-card-title">PPT评估</h3>
          <p class="me-card-desc">
            评估路演PPT的结构完整性、视觉表达、逻辑叙事、创新亮点呈现与答辩说服力。
          </p>
          <div class="me-card-meta">
            <el-icon size="14"><Files /></el-icon>
            <span>路演PPT、项目展示PPT、答辩PPT导出的 PDF</span>
          </div>
          <div class="me-card-features">
            <div class="me-feature-item">
              <el-icon size="14"><Check /></el-icon>
              <span>结构完整性分析</span>
            </div>
            <div class="me-feature-item">
              <el-icon size="14"><Check /></el-icon>
              <span>视觉表达评估</span>
            </div>
            <div class="me-feature-item">
              <el-icon size="14"><Check /></el-icon>
              <span>路演说服力评分</span>
            </div>
            <div class="me-feature-item">
              <el-icon size="14"><Check /></el-icon>
              <span>创新亮点识别</span>
            </div>
          </div>
          <el-button type="primary" size="large" class="me-card-btn ppt-btn" @click.stop="goUpload('ppt')">
            <el-icon><ArrowRight /></el-icon>
            开始PPT评估
          </el-button>
        </div>

        <div class="me-card report-card" @click="goUpload('report')">
          <div class="me-card-header">
            <div class="me-card-icon-wrapper report-icon">
              <el-icon size="28"><DocumentChecked /></el-icon>
            </div>
            <span class="me-card-badge report-badge">报告评估</span>
          </div>
          <h3 class="me-card-title">报告评估</h3>
          <p class="me-card-desc">
            评估商业计划书或项目报告的内容完整度、市场论证、创新价值、实施路径与风险表达。
          </p>
          <div class="me-card-meta">
            <el-icon size="14"><Files /></el-icon>
            <span>商业计划书、项目申报书、项目报告导出的 PDF</span>
          </div>
          <div class="me-card-features">
            <div class="me-feature-item">
              <el-icon size="14"><Check /></el-icon>
              <span>市场论证深度</span>
            </div>
            <div class="me-feature-item">
              <el-icon size="14"><Check /></el-icon>
              <span>商业模式评估</span>
            </div>
            <div class="me-feature-item">
              <el-icon size="14"><Check /></el-icon>
              <span>创新价值分析</span>
            </div>
            <div class="me-feature-item">
              <el-icon size="14"><Check /></el-icon>
              <span>风险与合规审查</span>
            </div>
          </div>
          <el-button type="primary" size="large" class="me-card-btn report-btn" @click.stop="goUpload('report')">
            <el-icon><ArrowRight /></el-icon>
            开始报告评估
          </el-button>
        </div>
      </div>
    </div>

    <div class="me-bottom-info">
      <div class="me-info-card">
        <el-icon size="20"><InfoFilled /></el-icon>
        <span>PPT评估与报告评估互不绑定，您可以只评估其中一项，也可以分别上传评估</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ArrowRight, Cpu, Present, DocumentChecked, Files, Check, InfoFilled } from '@element-plus/icons-vue'

const router = useRouter()

function goUpload(type) {
  router.push(`/ai-material-evaluation/upload/${type}`)
}
</script>

<style scoped>
.material-evaluation-page {
  min-height: 100vh;
  background: #f5f8ff;
}

.me-hero {
  position: relative;
  background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 40%, #7c3aed 100%);
  padding: 60px 24px;
  overflow: hidden;
}

.me-hero-content {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
  position: relative;
  z-index: 2;
}

.me-hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 16px;
  background: rgba(255,255,255,0.12);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 20px;
  color: #a5b4fc;
  font-size: 13px;
  margin-bottom: 20px;
}

.me-hero-title {
  font-size: 38px;
  font-weight: 700;
  color: #fff;
  margin: 0 0 12px;
  letter-spacing: -0.02em;
}

.me-hero-subtitle {
  font-size: 16px;
  color: rgba(255,255,255,0.85);
  margin: 0 0 8px;
  line-height: 1.6;
}

.me-hero-desc {
  font-size: 14px;
  color: rgba(255,255,255,0.55);
  margin: 0;
}

.me-hero-bg {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 600px 400px at 20% 50%, rgba(99,102,241,0.25), transparent),
    radial-gradient(ellipse 500px 350px at 80% 30%, rgba(124,58,237,0.2), transparent);
}

.me-hero-float {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
}

.me-float-ring {
  position: absolute;
  border-radius: 50%;
  border: 1px solid rgba(255,255,255,0.1);
}

.me-float-ring.r1 {
  width: 300px;
  height: 300px;
  top: -80px;
  right: -60px;
  animation: floatRing 8s ease-in-out infinite;
}

.me-float-ring.r2 {
  width: 200px;
  height: 200px;
  bottom: -40px;
  left: 10%;
  animation: floatRing 6s ease-in-out infinite reverse;
}

.me-float-dot {
  position: absolute;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: rgba(255,255,255,0.3);
}

.me-float-dot.d1 { top: 20%; left: 15%; animation: floatDot 5s ease-in-out infinite; }
.me-float-dot.d2 { top: 60%; right: 20%; animation: floatDot 7s ease-in-out infinite 1s; }
.me-float-dot.d3 { bottom: 30%; left: 50%; animation: floatDot 6s ease-in-out infinite 2s; }

@keyframes floatRing {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(5deg); }
}

@keyframes floatDot {
  0%, 100% { transform: translateY(0); opacity: 0.3; }
  50% { transform: translateY(-15px); opacity: 0.7; }
}

.me-cards-section {
  max-width: 960px;
  margin: -40px auto 0;
  padding: 0 24px 60px;
  position: relative;
  z-index: 3;
}

.me-section-title {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  text-align: center;
  margin: 0 0 6px;
}

.me-section-desc {
  font-size: 14px;
  color: #64748b;
  text-align: center;
  margin: 0 0 32px;
}

.me-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.me-card {
  background: #fff;
  border-radius: 20px;
  padding: 32px;
  cursor: pointer;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid #e8ecf4;
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}

.me-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 40px rgba(37,99,235,0.12);
  border-color: #c7d2fe;
}

.me-card-header {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 20px;
}

.me-card-icon-wrapper {
  width: 52px;
  height: 52px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ppt-icon {
  background: linear-gradient(135deg, #dbeafe, #ede9fe);
  color: #6366f1;
}

.report-icon {
  background: linear-gradient(135deg, #d1fae5, #e0e7ff);
  color: #10b981;
}

.me-card-badge {
  font-size: 12px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 12px;
}

.ppt-badge { background: #eef2ff; color: #6366f1; }
.report-badge { background: #ecfdf5; color: #10b981; }

.me-card-title {
  font-size: 22px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 10px;
}

.me-card-desc {
  font-size: 14px;
  color: #475569;
  line-height: 1.7;
  margin: 0 0 14px;
}

.me-card-meta {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #94a3b8;
  padding: 10px 12px;
  background: #f8fafc;
  border-radius: 10px;
  margin-bottom: 18px;
}

.me-card-features {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-bottom: 24px;
}

.me-feature-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #475569;
}

.me-feature-item .el-icon {
  color: #10b981;
  flex-shrink: 0;
}

.me-card-btn {
  width: 100%;
  height: 44px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  flex-direction: row-reverse;
}

.ppt-btn { background: linear-gradient(135deg, #6366f1, #8b5cf6); border: none; }
.ppt-btn:hover { background: linear-gradient(135deg, #4f46e5, #7c3aed); }

.report-btn { background: linear-gradient(135deg, #10b981, #059669); border: none; }
.report-btn:hover { background: linear-gradient(135deg, #059669, #047857); }

.me-bottom-info {
  max-width: 960px;
  margin: 0 auto;
  padding: 0 24px 60px;
}

.me-info-card {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 16px 24px;
  background: #eef2ff;
  border-radius: 14px;
  font-size: 13px;
  color: #4f46e5;
  border: 1px solid #e0e7ff;
}

@media (max-width: 768px) {
  .me-cards {
    grid-template-columns: 1fr;
  }

  .me-hero-title {
    font-size: 28px;
  }

  .me-hero {
    padding: 40px 16px;
  }

  .me-cards-section {
    margin-top: -24px;
  }

  .me-card {
    padding: 24px;
  }
}
</style>