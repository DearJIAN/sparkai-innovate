<template>
  <div class="portal-page">
    <!-- 全屏数字雨背景 -->
    <canvas ref="globalRainCanvas" class="global-rain-canvas"></canvas>

    <!-- Banner 区域 -->
    <div class="portal-banner">
      <div class="banner-gradient-bg"></div>
      <div class="banner-bg-pattern"></div>
      <div class="banner-particles" ref="particleContainer">
        <div
          v-for="i in 20"
          :key="'p' + i"
          class="particle"
          :class="[`particle-${((i - 1) % 3) + 1}`]"
          :style="particleStyle(i)"
        ></div>
      </div>
      <div class="banner-content">
        <div class="banner-badge">
          <el-icon size="16"><Trophy /></el-icon>
          <span>2026 创新创业季</span>
        </div>
        <h1 class="banner-title">
          <span class="title-highlight">火花智创</span> SparkAI
        </h1>
        <p class="banner-subtitle">聚合竞赛资源，助力项目成长</p>
        <p class="banner-desc">覆盖创新创业、人工智能、数字经济、乡村振兴、产业命题等方向</p>
        <div class="banner-stats">
          <div class="banner-stat">
            <span class="stat-num">{{ homeStats.competitions }}+</span>
            <span class="stat-text">竞赛活动</span>
          </div>
          <div class="banner-stat">
            <span class="stat-num">{{ homeStats.teams }}+</span>
            <span class="stat-text">参赛团队</span>
          </div>
          <div class="banner-stat">
            <span class="stat-num">{{ homeStats.tracks }}+</span>
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
    <div class="portal-section section-features" ref="cardSection">
      <h2 class="section-title">功能入口</h2>
      <div class="card-grid">
        <div
          v-for="card in visibleCards"
          :key="card.key"
          class="portal-card"
          :class="[`card-${card.color}`]"
          @click="navigateTo(card.path, card.action)"
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
    <div class="portal-section section-competitions" v-if="recommendedCompetitions.length > 0" ref="compSection">
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
          <div class="comp-poster">
            <img
              v-if="getLocalImage(comp.name)"
              :src="getLocalImage(comp.name)"
              :alt="comp.name"
              class="comp-poster-img"
            />
            <div v-else class="comp-poster-fallback" :style="{ background: comp.gradient }"></div>
          </div>
          <div class="comp-info">
            <h4 class="comp-name">{{ comp.name }}</h4>
            <div class="comp-tags">
              <el-tag size="small" :type="comp.levelType">{{ comp.level }}</el-tag>
              <el-tag size="small" class="comp-category">{{ comp.category }}</el-tag>
            </div>
            <p class="comp-time">报名截止：{{ comp.endDate }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 快捷入口区域 -->
    <div class="portal-section section-quick" ref="quickSection">
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
import { computed, ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import {
  Trophy, FolderOpened, User, Document, StarFilled,
  MagicStick, TrendCharts, ArrowRight, Medal, School,
  Briefcase, Collection, Calendar, DataAnalysis
} from '@element-plus/icons-vue'
import { getPublicStats } from '@/api/dashboard'

// 导入本地竞赛图片
import imgAI from '@/assets/images/competitions/2026 AI 应用创新设计大赛.png'
import imgRural from '@/assets/images/competitions/2026 乡村振兴公益创业实践赛.png'
import imgEnterprise from '@/assets/images/competitions/2026 企业真实命题创新挑战赛.png'
import imgInnovation from '@/assets/images/competitions/2026 大学生创新创业计划训练赛.png'
import imgCareer from '@/assets/images/competitions/2026 大学生职业规划与就业能力大赛.png'
import imgDigital from '@/assets/images/competitions/2026 数字经济与商业模式创新挑战赛.png'
import imgSmartMfg from '@/assets/images/competitions/2026 智能制造与物联网应用赛.png'
import imgEcommerce from '@/assets/images/competitions/2026 校园电子商务运营挑战赛.png'
import imgSoftware from '@/assets/images/competitions/2026 软件工程创新项目挑战赛.png'
import imgRedDream from '@/assets/images/competitions/2026 青年红色筑梦公益项目赛.png'

const competitionImages = {
  'AI 应用创新设计大赛': imgAI,
  '乡村振兴公益创业实践赛': imgRural,
  '企业真实命题创新挑战赛': imgEnterprise,
  '大学生创新创业计划训练赛': imgInnovation,
  '大学生职业规划与就业能力大赛': imgCareer,
  '数字经济与商业模式创新挑战赛': imgDigital,
  '智能制造与物联网应用赛': imgSmartMfg,
  '校园电子商务运营挑战赛': imgEcommerce,
  '软件工程创新项目挑战赛': imgSoftware,
  '青年红色筑梦公益项目赛': imgRedDream
}

const getLocalImage = (name) => {
  const key = name.replace(/^2026\s*/, '')
  return competitionImages[key] || null
}

const router = useRouter()
const userStore = useUserStore()

// Refs for IntersectionObserver
const particleContainer = ref(null)
const cardSection = ref(null)
const compSection = ref(null)
const quickSection = ref(null)
const particleCanvas = ref(null)
const particleCanvas2 = ref(null)
const particleCanvas3 = ref(null)
const globalRainCanvas = ref(null)

// 非首屏区域可见性控制
const cardSectionVisible = ref(false)
const compSectionVisible = ref(false)
const quickSectionVisible = ref(false)

// 首页统计数据（动态加载）
const homeStats = ref({
  competitions: 0,
  teams: 0,
  tracks: 0
})

const navigateTo = (path, action) => {
  if (action === 'open-huahuo-agent') {
    window.dispatchEvent(new CustomEvent('open-huahuo-agent', {
      detail: { source: 'portal' }
    }))
    return
  }
  if (path) router.push(path)
}

// 粒子样式生成 - 使用primary色系，大小3-8px，透明度0.1-0.3
const particleStyle = (i) => {
  const left = Math.random() * 100
  const top = 60 + Math.random() * 40 // 从下方开始上浮
  const delay = Math.random() * 8
  const duration = 8 + Math.random() * 7 // 8-15秒周期
  const size = 3 + Math.random() * 5 // 3-8px
  const opacity = 0.1 + Math.random() * 0.2 // 0.1-0.3
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

// IntersectionObserver 懒加载非首屏粒子/区域
let observer = null

const loadHomeStats = async () => {
  try {
    const res = await getPublicStats()
    if (res.code === 200 && res.data) {
      homeStats.value = {
        competitions: res.data.competition_count || 0,
        teams: res.data.team_count || 0,
        tracks: res.data.track_count || 7
      }
    }
  } catch (e) {
    homeStats.value = { competitions: 50, teams: 1000, tracks: 10 }
  }
}

onMounted(() => {
  // 启动全局数字雨背景（铺满整个页面宽度）
  initGlobalRain(globalRainCanvas)

  // 加载首页统计数据
  loadHomeStats()

  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const target = entry.target
          if (target === cardSection.value) { cardSectionVisible.value = true }
          if (target === compSection.value) { compSectionVisible.value = true }
          if (target === quickSection.value) { quickSectionVisible.value = true }
        }
      })
    },
    { threshold: 0.1, rootMargin: '100px' }
  )

  if (cardSection.value) observer.observe(cardSection.value)
  if (compSection.value) observer.observe(compSection.value)
  if (quickSection.value) observer.observe(quickSection.value)

  window.addEventListener('resize', handleResize)
})

const flowAnimFrames = []

function handleResize() {
  flowAnimFrames.forEach(f => { if (typeof f === 'function') f() })
}

// 全局数字雨背景 - 铺满整个页面宽度
function initGlobalRain(canvasRef) {
  const canvas = canvasRef?.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')

  function resizeCanvas() {
    const pageWidth = document.documentElement.scrollWidth || window.innerWidth
    const pageHeight = document.documentElement.scrollHeight || window.innerHeight
    canvas.width = pageWidth
    canvas.height = pageHeight
    return { w: pageWidth, h: pageHeight }
  }

  let { w, h } = resizeCanvas()

  // 科幻数字雨风格的数据流
  const fontSize = 14
  let columns = Math.floor(w / fontSize)

  // 数字和符号字符集（科幻感）
  const chars = '0123456789ABCDEF'.split('')
  const symbols = ['+', '-', '*', '/', '=', '<', '>', '{', '}', '[', ']', '|', '&', '%', '$', '#', '@']
  const allChars = [...chars, ...symbols]

  // 每列的状态
  const drops = []
  function initDrops() {
    drops.length = 0
    columns = Math.floor(w / fontSize)
    for (let i = 0; i < columns; i++) {
      drops.push({
        x: i * fontSize,
        y: Math.random() * h * 0.8 - h * 0.3,
        speed: 0.8 + Math.random() * 1.5,
        length: 8 + Math.floor(Math.random() * 18),
        chars: [],
        opacity: 0.03 + Math.random() * 0.06,
        active: Math.random() > 0.6,
        timer: Math.random() * 200
      })
    }
    // 初始化每列的字符
    drops.forEach(drop => {
      drop.chars = []
      for (let j = 0; j < drop.length; j++) {
        drop.chars.push(allChars[Math.floor(Math.random() * allChars.length)])
      }
    })
  }
  initDrops()

  // 偶尔出现的水平扫描线
  const scanLines = []
  let lastScanTime = 0

  function createScanLine() {
    scanLines.push({
      y: Math.random() * h,
      speed: 0.8 + Math.random() * 1.5,
      opacity: 0.03 + Math.random() * 0.04,
      width: 40 + Math.random() * 120,
      life: 1.0,
      decay: 0.003 + Math.random() * 0.005
    })
  }

  function draw() {
    // 检测页面高度变化（内容动态加载可能导致高度变化）
    const currentHeight = document.documentElement.scrollHeight
    if (currentHeight !== h) {
      h = currentHeight
      canvas.height = h
    }

    // 使用半透明覆盖，产生拖尾效果
    ctx.fillStyle = 'rgba(248, 250, 252, 0.12)'
    ctx.fillRect(0, 0, w, h)

    // 绘制数字雨列
    drops.forEach(drop => {
      if (!drop.active) {
        drop.timer--
        if (drop.timer <= 0) {
          drop.active = true
          drop.timer = 100 + Math.random() * 300
        }
        return
      }

      drop.y += drop.speed

      // 如果超出底部，重置到顶部
      if (drop.y - drop.length * fontSize > h) {
        drop.y = -drop.length * fontSize
        drop.speed = 0.8 + Math.random() * 1.5
        drop.length = 8 + Math.floor(Math.random() * 18)
        drop.opacity = 0.03 + Math.random() * 0.06
        // 随机停用一些列
        if (Math.random() > 0.7) {
          drop.active = false
          drop.timer = 50 + Math.random() * 200
        }
        // 重新生成字符
        drop.chars = []
        for (let j = 0; j < drop.length; j++) {
          drop.chars.push(allChars[Math.floor(Math.random() * allChars.length)])
        }
      }

      // 绘制该列的字符
      for (let j = 0; j < drop.length; j++) {
        const cy = drop.y - j * fontSize
        if (cy < -fontSize || cy > h + fontSize) continue

        // 头部字符最亮（青色/蓝色）
        let alpha, color
        if (j === 0) {
          alpha = drop.opacity * 3
          color = '#22d3ee'
        } else if (j < 3) {
          alpha = drop.opacity * 2
          color = '#0ea5e9'
        } else {
          alpha = drop.opacity * (1 - j / drop.length)
          color = '#64748b'
        }

        // 偶尔闪烁变化字符
        if (Math.random() > 0.995) {
          drop.chars[j] = allChars[Math.floor(Math.random() * allChars.length)]
        }

        ctx.font = `${fontSize}px 'Courier New', monospace`
        ctx.fillStyle = color
        ctx.globalAlpha = Math.max(0, Math.min(1, alpha))
        ctx.fillText(drop.chars[j], drop.x, cy)
      }
    })

    // 偶尔生成水平扫描线
    const now = Date.now()
    if (now - lastScanTime > 4000 + Math.random() * 6000) {
      createScanLine()
      lastScanTime = now
    }

    // 绘制扫描线
    for (let si = scanLines.length - 1; si >= 0; si--) {
      const sl = scanLines[si]
      sl.y += sl.speed
      sl.life -= sl.decay

      if (sl.life <= 0 || sl.y > h) {
        scanLines.splice(si, 1)
        continue
      }

      const sx = Math.random() * (w - sl.width)
      ctx.fillStyle = '#0ea5e9'
      ctx.globalAlpha = sl.opacity * sl.life
      ctx.fillRect(sx, sl.y, sl.width, 1)

      // 扫描线上的小光点
      if (Math.random() > 0.5) {
        ctx.fillStyle = '#22d3ee'
        ctx.globalAlpha = sl.opacity * sl.life * 2
        ctx.fillRect(sx + Math.random() * sl.width, sl.y, 2, 1)
      }
    }

    ctx.globalAlpha = 1
    flowAnimFrames[flowAnimFrames.indexOf(draw)] = requestAnimationFrame(draw)
  }
  flowAnimFrames.push(draw)
  draw()

  const cleanup = () => {
    const idx = flowAnimFrames.indexOf(draw)
    if (idx >= 0) cancelAnimationFrame(flowAnimFrames.splice(idx, 1)[0])
  }
  flowAnimFrames.push(cleanup)
}

// 兼容旧函数名（不再使用）
function initDataFlow(canvasRef) {
  // 已废弃，数字雨现在由 initGlobalRain 统一管理
}

onBeforeUnmount(() => {
  if (observer) {
    observer.disconnect()
    observer = null
  }
  window.removeEventListener('resize', handleResize)
  flowAnimFrames.forEach((f, i) => {
    if (typeof f === 'number') cancelAnimationFrame(f)
  })
})

// 功能卡片配置
const allCards = [
  {
    key: 'competition',
    title: '竞赛报名',
    desc: '浏览并报名各类创新创业竞赛',
    icon: Trophy,
    path: '/competition-center',
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
    path: null,
    action: 'open-huahuo-agent',
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
  },
  {
    key: 'assessment',
    title: '在线测评',
    desc: '获取创业能力、团队协作等能力画像',
    icon: TrendCharts,
    path: '/assessment',
    color: 'indigo',
    roles: ['student', 'teacher', 'judge', 'admin']
  },
  {
    key: 'material-evaluation',
    title: 'AI材料评估',
    desc: '智能评估PPT与项目报告',
    icon: DataAnalysis,
    path: '/ai-material-evaluation',
    color: 'violet',
    roles: ['student', 'teacher', 'judge', 'admin']
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
  position: relative;
}

.global-rain-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.portal-banner,
.portal-section {
  position: relative;
  z-index: 1;
}

/* Banner */
.portal-banner {
  position: relative;
  background: linear-gradient(135deg, #0c4a6e 0%, #075985 50%, #0ea5e9 100%);
  padding: 60px 40px;
  overflow: hidden;
  border-radius: 0 0 40px 40px;
}

/* 渐变动画背景 - 10-15秒周期缓慢变化 */
.banner-gradient-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    135deg,
    #0c4a6e 0%,
    #075985 25%,
    #0ea5e9 50%,
    #06b6d4 75%,
    #0891b2 100%
  );
  background-size: 400% 400%;
  animation: gradientShift 12s ease infinite;
  z-index: 0;
}

@keyframes gradientShift {
  0% {
    background-position: 0% 50%;
  }
  25% {
    background-position: 50% 0%;
  }
  50% {
    background-position: 100% 50%;
  }
  75% {
    background-position: 50% 100%;
  }
  100% {
    background-position: 0% 50%;
  }
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

.banner-system-title {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 8px;
  letter-spacing: 1px;
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
  background: linear-gradient(135deg, #ef4444 0%, #f97316 20%, #f59e0b 40%, #ec4899 60%, #8b5cf6 80%, #3b82f6 100%);
  background-size: 300% 300%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: fireworkGradient 4s ease infinite, textFireGlow 2s ease-in-out infinite alternate;
  display: inline-block;
}

@keyframes fireworkGradient {
  0%, 100% { background-position: 0% 50%; }
  25% { background-position: 100% 0%; }
  50% { background-position: 100% 100%; }
  75% { background-position: 0% 100%; }
}

@keyframes textFireGlow {
  from {
    filter: drop-shadow(0 0 8px rgba(245, 158, 11, 0.5)) drop-shadow(0 0 16px rgba(239, 68, 68, 0.3));
  }
  to {
    filter: drop-shadow(0 0 16px rgba(245, 158, 11, 0.8)) drop-shadow(0 0 32px rgba(239, 68, 68, 0.5)) drop-shadow(0 0 48px rgba(236, 72, 153, 0.3));
  }
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
  will-change: transform, box-shadow;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
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
  will-change: transform, box-shadow;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
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

/* Particles - 纯CSS粒子动画 */
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
  will-change: transform, opacity;
  animation: particleFloat linear infinite;
}

/* 粒子颜色 - primary色系 */
.particle-1 {
  background: #0ea5e9;
}

.particle-2 {
  background: #06b6d4;
}

.particle-3 {
  background: #0891b2;
}

/* 粒子缓慢上浮动画 - GPU加速 */
@keyframes particleFloat {
  0% {
    transform: translateY(0) translateX(0) scale(1);
    opacity: var(--particle-opacity, 0.2);
  }
  25% {
    transform: translateY(-25%) translateX(10px) scale(1.1);
    opacity: calc(var(--particle-opacity, 0.2) * 1.2);
  }
  50% {
    transform: translateY(-50%) translateX(-5px) scale(1);
    opacity: var(--particle-opacity, 0.2);
  }
  75% {
    transform: translateY(-75%) translateX(8px) scale(0.9);
    opacity: calc(var(--particle-opacity, 0.2) * 0.8);
  }
  100% {
    transform: translateY(-100%) translateX(0) scale(1);
    opacity: var(--particle-opacity, 0.2);
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
  will-change: transform;
}

.c1 {
  width: 300px;
  height: 300px;
  background: #7dd3fc;
  right: -50px;
  top: -50px;
  animation: decoFloat1 8s ease-in-out infinite;
}

.c2 {
  width: 200px;
  height: 200px;
  background: #38bdf8;
  right: 100px;
  bottom: -30px;
  animation: decoFloat2 10s ease-in-out infinite;
}

.c3 {
  width: 150px;
  height: 150px;
  background: #0ea5e9;
  right: 250px;
  top: 50%;
  animation: decoFloat3 7s ease-in-out infinite;
}

@keyframes decoFloat1 {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-15px) scale(1.05); }
}

@keyframes decoFloat2 {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(10px) scale(1.03); }
}

@keyframes decoFloat3 {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-10px) scale(0.95); }
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
  will-change: transform;
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
  position: relative;
  overflow: hidden;
}

.data-flow-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.section-title {
  font-size: 22px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 24px;
  position: relative;
  z-index: 1;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  position: relative;
  z-index: 1;
}

/* Card Grid */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
  position: relative;
  z-index: 1;
}

.portal-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 28px;
  cursor: pointer;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid #e2e8f0;
  position: relative;
  overflow: hidden;
  will-change: transform, box-shadow;
}

/* 卡片hover微动效 - 上浮4px + 阴影增强 */
.portal-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 32px -8px rgba(0, 0, 0, 0.12), 0 4px 12px -2px rgba(0, 0, 0, 0.06);
}

/* 卡片图标hover微动效 - 旋转缩放 */
.portal-card:hover .card-icon {
  transform: scale(1.15) rotate(5deg);
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

.card-violet::before { background: linear-gradient(90deg, #7c3aed, #a78bfa); }
.card-violet .card-icon { color: #7c3aed; }

.card-teal::before { background: linear-gradient(90deg, #14b8a6, #2dd4bf); }
.card-teal .card-icon { color: #14b8a6; }

.card-yellow::before { background: linear-gradient(90deg, #eab308, #facc15); }
.card-yellow .card-icon { color: #eab308; }

.card-icon {
  margin-bottom: 16px;
  will-change: transform;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
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
  will-change: transform;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), color 0.3s ease;
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
  position: relative;
  z-index: 1;
}

.competition-item {
  background: #ffffff;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid #e2e8f0;
  will-change: transform, box-shadow;
}

.competition-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 32px -8px rgba(0, 0, 0, 0.12);
}

.comp-poster {
  aspect-ratio: 16 / 9;
  overflow: hidden;
  background: #0f172a;
}

.comp-poster-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.comp-poster-fallback {
  width: 100%;
  height: 100%;
}

.comp-info {
  padding: 16px;
}

.comp-name {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 8px;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.comp-tags {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
}

.comp-category {
  background-color: #f1f5f9;
  color: #475569;
  border: none;
}

.comp-time {
  font-size: 13px;
  color: #64748b;
}

/* Quick Actions */
.quick-actions {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  position: relative;
  z-index: 1;
}

.quick-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 500;
  will-change: transform;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.quick-btn:hover {
  transform: translateY(-2px);
}

/* 减少动画偏好 */
@media (prefers-reduced-motion: reduce) {
  .particle,
  .banner-gradient-bg,
  .deco-circle,
  .deco-hexagon {
    animation: none !important;
  }
  .portal-card,
  .competition-item,
  .quick-btn,
  .card-icon,
  .card-arrow,
  .banner-btn-primary,
  .banner-btn-secondary {
    transition: none !important;
  }
}
</style>
