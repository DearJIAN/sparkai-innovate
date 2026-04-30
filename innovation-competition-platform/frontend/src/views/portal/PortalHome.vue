<template>
  <div class="portal-page">
    <!-- Banner 区域 -->
    <div class="portal-banner">
      <div class="banner-bg-pattern"></div>
      <div class="banner-particles">
        <div v-for="i in 20" :key="i" class="particle" :style="particleStyle(i)"></div>
      </div>
      <div class="banner-content">
        <div class="banner-badge">
          <el-icon size="16"><Trophy /></el-icon>
          <span>2026 创新创业季</span>
        </div>
        <h1 class="banner-title">
          <span class="title-highlight">双创竞赛</span>服务平台
        </h1>
        <p class="banner-subtitle">聚合竞赛资源，助力项目成长</p>
        <p class="banner-desc">覆盖创新创业、人工智能、数字经济、乡村振兴、产业命题等方向</p>
        <div class="banner-stats">
          <div class="banner-stat">
            <span class="stat-num">50+</span>
            <span class="stat-text">竞赛活动</span>
          </div>
          <div class="banner-stat">
            <span class="stat-num">1000+</span>
            <span class="stat-text">参赛团队</span>
          </div>
          <div class="banner-stat">
            <span class="stat-num">10+</span>
            <span class="stat-text">赛道方向</span>
          </div>
        </div>
        <div class="banner-actions">
          <el-button type="primary" size="large" class="banner-btn-primary" @click="navigateTo('/competitions')">
            <el-icon><Trophy /></el-icon>
            浏览竞赛
          </el-button>
          <el-button size="large" class="banner-btn-secondary" @click="navigateTo('/create-project')">
            <el-icon><FolderOpened /></el-icon>
            创建项目
          </el-button>
        </div>
      </div>
      <div class="banner-decoration">
        <div class="deco-circle c1"></div>
        <div class="deco-circle c2"></div>
        <div class="deco-circle c3"></div>
        <div class="deco-hexagon"></div>
        <div class="deco-dots"></div>
      </div>
    </div>

    <!-- 功能卡片区域 -->
    <div class="portal-section">
      <h2 class="section-title">功能入口</h2>
      <div class="card-grid">
        <div
          v-for="card in visibleCards"
          :key="card.key"
          class="portal-card"
          :class="[`card-${card.color}`]"
          @click="navigateTo(card.path)"
        >
          <div class="card-icon">
            <el-icon size="32">
              <component :is="card.icon" />
            </el-icon>
          </div>
          <h3 class="card-title">{{ card.title }}</h3>
          <p class="card-desc">{{ card.desc }}</p>
          <div class="card-arrow">
            <el-icon><ArrowRight /></el-icon>
          </div>
        </div>
      </div>
    </div>

    <!-- 推荐竞赛区域 -->
    <div class="portal-section" v-if="recommendedCompetitions.length > 0">
      <div class="section-header">
        <h2 class="section-title">推荐竞赛</h2>
        <el-button link type="primary" @click="navigateTo('/competitions')">
          查看更多 <el-icon><ArrowRight /></el-icon>
        </el-button>
      </div>
      <div class="competition-list">
        <div
          v-for="comp in recommendedCompetitions"
          :key="comp.id"
          class="competition-item"
          @click="navigateTo(`/competitions/${comp.id}`)"
        >
          <div class="comp-poster" :style="{ background: comp.gradient }">
            <span class="comp-name">{{ comp.name }}</span>
          </div>
          <div class="comp-info">
            <el-tag size="small" :type="comp.levelType">{{ comp.level }}</el-tag>
            <el-tag size="small" class="comp-category">{{ comp.category }}</el-tag>
            <p class="comp-time">报名截止：{{ comp.endDate }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 快捷入口区域 -->
    <div class="portal-section">
      <h2 class="section-title">快捷操作</h2>
      <div class="quick-actions">
        <el-button
          v-for="action in quickActions"
          :key="action.key"
          class="quick-btn"
          :type="action.type"
          size="large"
          @click="navigateTo(action.path)"
        >
          <el-icon size="18"><component :is="action.icon" /></el-icon>
          {{ action.label }}
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import {
  Trophy, FolderOpened, User, Document, StarFilled,
  MagicStick, TrendCharts, ArrowRight, Medal, School,
  Briefcase, Collection, Calendar
} from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const navigateTo = (path) => {
  if (path) router.push(path)
}

// 粒子样式生成
const particleStyle = (i) => {
  const left = Math.random() * 100
  const top = Math.random() * 100
  const delay = Math.random() * 6
  const duration = 4 + Math.random() * 4
  return {
    left: `${left}%`,
    top: `${top}%`,
    animationDelay: `${delay}s`,
    animationDuration: `${duration}s`
  }
}

// 功能卡片配置
const allCards = [
  {
    key: 'competition',
    title: '竞赛报名',
    desc: '浏览并报名各类创新创业竞赛',
    icon: Trophy,
    path: '/competitions',
    color: 'blue',
    roles: ['student', 'teacher', 'judge', 'admin']
  },
  {
    key: 'my-competitions',
    title: '我的赛事',
    desc: '查看我报名的竞赛和进度',
    icon: Medal,
    path: '/my-registrations',
    color: 'cyan',
    roles: ['student']
  },
  {
    key: 'projects',
    title: '项目工作室',
    desc: '管理我的创新创业项目',
    icon: FolderOpened,
    path: '/my-projects',
    color: 'green',
    roles: ['student']
  },
  {
    key: 'guide-projects',
    title: '指导项目',
    desc: '查看我指导的学生项目',
    icon: School,
    path: '/guide-projects',
    color: 'green',
    roles: ['teacher']
  },
  {
    key: 'team',
    title: '团队管理',
    desc: '管理项目团队成员',
    icon: User,
    path: '/my-projects',
    color: 'purple',
    roles: ['student']
  },
  {
    key: 'materials',
    title: '材料中心',
    desc: '上传和管理项目材料',
    icon: Document,
    path: '/my-projects',
    color: 'orange',
    roles: ['student', 'teacher']
  },
  {
    key: 'reviews',
    title: '评审中心',
    desc: '查看待评审项目',
    icon: StarFilled,
    path: '/pending-reviews',
    color: 'red',
    roles: ['judge']
  },
  {
    key: 'review-history',
    title: '评审记录',
    desc: '查看我的评审历史',
    icon: Collection,
    path: '/review-history',
    color: 'pink',
    roles: ['judge']
  },
  {
    key: 'ai',
    title: 'AI 项目助手',
    desc: '智能辅助项目创作',
    icon: MagicStick,
    path: '/ai-assistant',
    color: 'indigo',
    roles: ['student', 'teacher', 'judge', 'admin']
  },
  {
    key: 'dashboard',
    title: '数据看板',
    desc: '查看系统统计数据',
    icon: TrendCharts,
    path: '/dashboard',
    color: 'teal',
    roles: ['admin']
  },
  {
    key: 'user-management',
    title: '用户管理',
    desc: '管理系统用户',
    icon: User,
    path: '/user-management',
    color: 'blue',
    roles: ['admin']
  },
  {
    key: 'project-management',
    title: '项目管理',
    desc: '管理所有项目',
    icon: FolderOpened,
    path: '/project-management',
    color: 'cyan',
    roles: ['admin']
  },
  {
    key: 'competition-management',
    title: '赛事管理',
    desc: '管理竞赛批次',
    icon: Trophy,
    path: '/competition-management',
    color: 'green',
    roles: ['admin']
  },
  {
    key: 'training',
    title: '训练营',
    desc: '参加创新创业训练营',
    icon: School,
    path: '/training-camps',
    color: 'yellow',
    roles: ['student', 'teacher']
  },
  {
    key: 'courses',
    title: '在线课程',
    desc: '学习创新创业课程',
    icon: Collection,
    path: '/courses',
    color: 'purple',
    roles: ['student', 'teacher']
  },
  {
    key: 'industry',
    title: '产业命题',
    desc: '查看企业真实命题',
    icon: Briefcase,
    path: '/industry-topics',
    color: 'orange',
    roles: ['student', 'teacher']
  },
  {
    key: 'certificates',
    title: '证书成果',
    desc: '查看我的证书和成果',
    icon: Medal,
    path: '/certificates',
    color: 'red',
    roles: ['student']
  }
]

const visibleCards = computed(() => {
  const role = userStore.userInfo?.role
  return allCards.filter(card => card.roles.includes(role))
})

// 快捷操作
const quickActions = computed(() => {
  const role = userStore.userInfo?.role
  const actions = []
  if (role === 'student') {
    actions.push({ key: 'create-project', label: '创建项目', icon: FolderOpened, path: '/create-project', type: 'primary' })
    actions.push({ key: 'competition', label: '去报名', icon: Trophy, path: '/competitions', type: 'success' })
  }
  if (role === 'teacher') {
    actions.push({ key: 'review', label: '项目审核', icon: StarFilled, path: '/project-review', type: 'primary' })
  }
  if (role === 'judge') {
    actions.push({ key: 'pending', label: '待评审', icon: StarFilled, path: '/pending-reviews', type: 'primary' })
  }
  if (role === 'admin') {
    actions.push({ key: 'dashboard', label: '数据看板', icon: TrendCharts, path: '/dashboard', type: 'primary' })
  }
  return actions
})

// 推荐竞赛（Mock 数据，后续接后端）
const recommendedCompetitions = ref([
  {
    id: 1,
    name: '2026 大学生创新创业计划训练赛',
    level: '校级',
    levelType: 'success',
    category: '创新创业',
    endDate: '2026-05-30',
    gradient: 'linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%)'
  },
  {
    id: 2,
    name: '2026 AI 应用创新设计大赛',
    level: '省级',
    levelType: 'warning',
    category: '人工智能',
    endDate: '2026-06-15',
    gradient: 'linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%)'
  },
  {
    id: 3,
    name: '2026 数字经济与商业模式创新挑战赛',
    level: '省级',
    levelType: 'warning',
    category: '数字经济',
    endDate: '2026-05-20',
    gradient: 'linear-gradient(135deg, #10b981 0%, #14b8a6 100%)'
  },
  {
    id: 4,
    name: '2026 乡村振兴公益创业实践赛',
    level: '国家级',
    levelType: 'danger',
    category: '乡村振兴',
    endDate: '2026-07-01',
    gradient: 'linear-gradient(135deg, #f59e0b 0%, #ef4444 100%)'
  }
])
</script>

<style scoped>
.portal-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #f0f9ff 0%, #ffffff 100%);
}

/* Banner */
.portal-banner {
  position: relative;
  background: linear-gradient(135deg, #0c4a6e 0%, #075985 50%, #0ea5e9 100%);
  padding: 60px 40px;
  overflow: hidden;
  border-radius: 0 0 40px 40px;
}

.banner-content {
  position: relative;
  z-index: 2;
  max-width: 600px;
}

.banner-title {
  font-size: 36px;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 12px;
  letter-spacing: 2px;
}

.banner-subtitle {
  font-size: 20px;
  color: #7dd3fc;
  margin-bottom: 8px;
  font-weight: 500;
}

.banner-desc {
  font-size: 14px;
  color: #bae6fd;
  line-height: 1.6;
  margin-bottom: 24px;
}

/* Banner Badge */
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

.title-highlight {
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Banner Stats */
.banner-stats {
  display: flex;
  gap: 32px;
  margin: 24px 0;
}

.banner-stat {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-num {
  font-size: 28px;
  font-weight: 700;
  color: #ffffff;
  line-height: 1;
}

.stat-text {
  font-size: 13px;
  color: #7dd3fc;
}

/* Banner Actions */
.banner-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.banner-btn-primary {
  background: linear-gradient(135deg, #f59e0b, #fbbf24);
  border: none;
  color: #1e293b;
  font-weight: 600;
  padding: 12px 28px;
}

.banner-btn-primary:hover {
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  color: #1e293b;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(245, 158, 11, 0.3);
}

.banner-btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #ffffff;
  font-weight: 500;
  padding: 12px 28px;
}

.banner-btn-secondary:hover {
  background: rgba(255, 255, 255, 0.2);
  color: #ffffff;
  border-color: rgba(255, 255, 255, 0.5);
}

/* Background Pattern */
.banner-bg-pattern {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image:
    radial-gradient(circle at 20% 50%, rgba(14, 165, 233, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(139, 92, 246, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 40% 80%, rgba(16, 185, 129, 0.08) 0%, transparent 50%);
  z-index: 0;
}

/* Particles */
.banner-particles {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  z-index: 0;
}

.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) scale(1);
    opacity: 0.3;
  }
  50% {
    transform: translateY(-20px) scale(1.2);
    opacity: 0.6;
  }
}

/* Banner Decoration */
.banner-decoration {
  position: absolute;
  right: 0;
  top: 0;
  width: 50%;
  height: 100%;
  z-index: 1;
}

.deco-circle {
  position: absolute;
  border-radius: 50%;
  opacity: 0.15;
}

.c1 {
  width: 300px;
  height: 300px;
  background: #7dd3fc;
  right: -50px;
  top: -50px;
}

.c2 {
  width: 200px;
  height: 200px;
  background: #38bdf8;
  right: 100px;
  bottom: -30px;
}

.c3 {
  width: 150px;
  height: 150px;
  background: #0ea5e9;
  right: 250px;
  top: 50%;
}

.deco-hexagon {
  position: absolute;
  width: 80px;
  height: 80px;
  right: 180px;
  top: 30%;
  background: rgba(255, 255, 255, 0.05);
  clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
  animation: rotate 20s linear infinite;
}

.deco-dots {
  position: absolute;
  right: 60px;
  bottom: 60px;
  width: 100px;
  height: 100px;
  background-image: radial-gradient(circle, rgba(255, 255, 255, 0.2) 1px, transparent 1px);
  background-size: 12px 12px;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Section */
.portal-section {
  padding: 40px;
  max-width: 1400px;
  margin: 0 auto;
}

.section-title {
  font-size: 22px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

/* Card Grid */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
}

.portal-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 28px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e2e8f0;
  position: relative;
  overflow: hidden;
}

.portal-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 20px 40px -12px rgba(0, 0, 0, 0.15);
}

.portal-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  border-radius: 16px 16px 0 0;
}

.card-blue::before { background: linear-gradient(90deg, #0ea5e9, #38bdf8); }
.card-blue .card-icon { color: #0ea5e9; }

.card-cyan::before { background: linear-gradient(90deg, #06b6d4, #22d3ee); }
.card-cyan .card-icon { color: #06b6d4; }

.card-green::before { background: linear-gradient(90deg, #10b981, #34d399); }
.card-green .card-icon { color: #10b981; }

.card-purple::before { background: linear-gradient(90deg, #8b5cf6, #a78bfa); }
.card-purple .card-icon { color: #8b5cf6; }

.card-orange::before { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
.card-orange .card-icon { color: #f59e0b; }

.card-red::before { background: linear-gradient(90deg, #ef4444, #f87171); }
.card-red .card-icon { color: #ef4444; }

.card-pink::before { background: linear-gradient(90deg, #ec4899, #f472b6); }
.card-pink .card-icon { color: #ec4899; }

.card-indigo::before { background: linear-gradient(90deg, #6366f1, #818cf8); }
.card-indigo .card-icon { color: #6366f1; }

.card-teal::before { background: linear-gradient(90deg, #14b8a6, #2dd4bf); }
.card-teal .card-icon { color: #14b8a6; }

.card-yellow::before { background: linear-gradient(90deg, #eab308, #facc15); }
.card-yellow .card-icon { color: #eab308; }

.card-icon {
  margin-bottom: 16px;
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
  line-height: 1.5;
  margin-bottom: 16px;
}

.card-arrow {
  position: absolute;
  right: 20px;
  bottom: 20px;
  color: #94a3b8;
  transition: all 0.3s ease;
}

.portal-card:hover .card-arrow {
  color: #0ea5e9;
  transform: translateX(4px);
}

/* Competition List */
.competition-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.competition-item {
  background: #ffffff;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e2e8f0;
}

.competition-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 32px -8px rgba(0, 0, 0, 0.12);
}

.comp-poster {
  height: 140px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.comp-name {
  color: #ffffff;
  font-size: 16px;
  font-weight: 600;
  text-align: center;
  line-height: 1.4;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.comp-info {
  padding: 16px;
}

.comp-category {
  margin-left: 8px;
}

.comp-time {
  margin-top: 8px;
  font-size: 13px;
  color: #64748b;
}

/* Quick Actions */
.quick-actions {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.quick-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 500;
}
</style>
