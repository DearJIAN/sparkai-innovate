<template>
  <div class="main-layout">
    <!-- 移动端遮罩层 -->
    <transition name="fade-overlay">
      <div
        v-if="mobileMenuOpen"
        class="mobile-overlay"
        @click="closeMobileMenu"
      />
    </transition>

    <!-- 移动端侧滑菜单 -->
    <transition name="slide-menu">
      <aside
        v-if="mobileMenuOpen"
        class="mobile-sidebar"
      >
        <div class="mobile-sidebar-header">
          <SparkLogo size="small" />
          <button class="mobile-close-btn" @click="closeMobileMenu">
            <el-icon size="20"><Close /></el-icon>
          </button>
        </div>

        <nav class="mobile-sidebar-nav">
          <template v-for="group in visibleMenuGroups" :key="group.label">
            <div class="nav-group-label">{{ group.label }}</div>
            <router-link
              v-for="item in group.items"
              :key="item.path"
              :to="item.path"
              class="nav-item"
              :class="{ active: isMenuActive(item.path) }"
              @click="closeMobileMenu"
            >
              <el-icon size="18">
                <component :is="item.icon" />
              </el-icon>
              <span class="nav-text">{{ item.title }}</span>
            </router-link>
          </template>
        </nav>
      </aside>
    </transition>

    <!-- 桌面端侧边栏 -->
    <aside
      v-if="showSidebar"
      class="sidebar"
      :class="{ collapsed: isCollapsed }"
    >
      <div class="sidebar-header">
        <SparkLogo :size="isCollapsed ? 'small' : 'normal'" />
      </div>

      <nav class="sidebar-nav">
        <template v-for="group in visibleMenuGroups" :key="group.label">
          <div v-show="!isCollapsed" class="nav-group-label">{{ group.label }}</div>
          <router-link
            v-for="item in group.items"
            :key="item.path"
            :to="item.path"
            class="nav-item"
            :class="{ active: isMenuActive(item.path) }"
          >
            <el-icon size="18">
              <component :is="item.icon" />
            </el-icon>
            <span v-show="!isCollapsed" class="nav-text">{{ item.title }}</span>
          </router-link>
        </template>
      </nav>

      <div class="sidebar-footer">
        <button class="collapse-btn" @click="toggleCollapse">
          <el-icon size="16">
            <component :is="isCollapsed ? 'Expand' : 'Fold'" />
          </el-icon>
        </button>
      </div>
    </aside>

    <div
      class="main-content"
      :class="{ expanded: isCollapsed, 'no-sidebar': !showSidebar }"
    >
      <header class="top-header" :class="{ 'platform-header': !showSidebar }">
        <div class="header-left">
          <!-- 汉堡菜单按钮（平板/移动端） -->
          <button class="hamburger-btn" @click="toggleMobileMenu">
            <el-icon size="22"><Operation /></el-icon>
          </button>

          <div class="header-logo" @click="router.push('/portal')">
            <SparkLogo size="small" />
          </div>

          <nav class="top-nav">
            <router-link
              v-for="item in topNavItems"
              :key="item.path"
              :to="item.path"
              class="top-nav-item"
              :class="{ active: isTopNavActive(item.path) }"
            >
              {{ item.title }}
            </router-link>
          </nav>
        </div>

        <div class="header-right">
          <el-dropdown @command="handleCommand" trigger="click">
            <div class="user-info">
              <el-avatar :size="36" :icon="UserFilled" class="user-avatar" />
              <div class="user-meta">
                <span class="user-name">{{ userStore.userInfo?.real_name || userStore.userInfo?.username }}</span>
                <span class="user-role">{{ roleText }}</span>
              </div>
              <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="portal">
                  <el-icon><HomeFilled /></el-icon>平台首页
                </el-dropdown-item>
                <el-dropdown-item divided command="logout">
                  <el-icon><SwitchButton /></el-icon>退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </header>

      <main class="page-content" :class="{ 'platform-page': isPlatformPage }">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
    <HuahuoAssistant :key="huahuoInstanceKey" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage, ElMessageBox } from 'element-plus'
import HuahuoAssistant from '@/components/HuahuoAssistant.vue'
import SparkLogo from '@/components/SparkLogo.vue'
import {
  Trophy, User, UserFilled, HomeFilled, SwitchButton, ArrowDown,
  FolderOpened, CirclePlusFilled, MagicStick, StarFilled, DocumentChecked,
  Expand, Fold, Document, Medal, School, Briefcase, Collection,
  TrendCharts, Calendar, Setting, Edit, List, Close, Operation
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const isCollapsed = ref(false)
const mobileMenuOpen = ref(false)

const platformPages = [
  '/portal', '/competition-center', '/external-competitions',
  '/competitions', '/training-camps', '/courses',
  '/industry-topics', '/my-registrations', '/certificates'
]

const isPlatformPage = computed(() => {
  if (route.meta?.platformPage) return true
  return platformPages.some(path => route.path === path || route.path.startsWith(path + '/'))
})

const huahuoInstanceKey = computed(() => {
  const user = userStore.userInfo
  return `${user?.id || user?.user_id || user?.username || 'guest'}-${user?.role || 'none'}`
})

const showSidebar = computed(() => {
  if (isPlatformPage.value) return false
  return true
})

// 顶部导航配置 - 所有角色都能看到核心功能入口，按使用习惯排序
const topNavConfig = [
  { path: '/portal', title: '首页', roles: ['student', 'teacher', 'judge', 'admin'] },
  { path: '/external-competitions', title: '校外竞赛', roles: ['student', 'teacher', 'judge', 'admin'] },
  { path: '/competitions', title: '校内竞赛', roles: ['student', 'teacher', 'judge', 'admin'] },
  { path: '/training-camps', title: '训练营', roles: ['student', 'teacher', 'judge', 'admin'] },
  { path: '/courses', title: '课程', roles: ['student', 'teacher', 'judge', 'admin'] },
  { path: '/industry-topics', title: '产业命题', roles: ['student', 'teacher', 'judge', 'admin'] },
  { path: '/my-projects', title: '我的项目', roles: ['student'] },
  { path: '/guide-projects', title: '指导项目', roles: ['teacher'] },
  { path: '/pending-reviews', title: '评审', roles: ['judge'] },
  { path: '/certificates', title: '证书', roles: ['student'] },
  { path: '/project-management', title: '管理', roles: ['admin'] }
]

const topNavItems = computed(() => {
  const role = userStore.userInfo?.role
  if (!role) return []
  return topNavConfig.filter(item => item.roles.includes(role))
})

const isTopNavActive = (path) => {
  if (path === '/portal') return route.path === '/portal'
  if (path === '/external-competitions') return route.path.startsWith('/external-competitions')
  if (path === '/competitions') return route.path.startsWith('/competitions') || route.path.startsWith('/competition-center')
  if (path === '/training-camps') return route.path.startsWith('/training-camps')
  if (path === '/courses') return route.path.startsWith('/courses')
  if (path === '/industry-topics') return route.path.startsWith('/industry-topics')
  if (path === '/my-projects') return route.path.startsWith('/my-projects') || route.path.startsWith('/create-project') || route.path.startsWith('/projects/')
  if (path === '/guide-projects') return route.path.startsWith('/guide-projects') || route.path.startsWith('/project-review')
  if (path === '/pending-reviews') return route.path.startsWith('/pending-reviews') || route.path.startsWith('/review-history')
  if (path === '/certificates') return route.path.startsWith('/certificates')
  if (path === '/project-management') return route.path.startsWith('/project-management') || route.path.startsWith('/user-management') || route.path.startsWith('/competition-management') || route.path.startsWith('/review-management') || route.path.startsWith('/registration-management') || route.path.startsWith('/dashboard')
  return route.path === path
}

// 侧边栏菜单配置 - 分组顺序：概览 -> 竞赛 -> 项目 -> 学习 -> 管理
const menuGroups = [
  {
    label: '概览',
    roles: ['student', 'teacher', 'judge', 'admin'],
    items: [
      { path: '/dashboard', title: '工作台', icon: 'HomeFilled', roles: ['student', 'teacher', 'judge', 'admin'] }
    ]
  },
  {
    label: '竞赛',
    roles: ['student', 'teacher', 'judge', 'admin'],
    items: [
      { path: '/competitions', title: '校内竞赛', icon: 'Trophy', roles: ['student', 'teacher', 'judge', 'admin'] },
      { path: '/my-registrations', title: '我的赛事', icon: 'Medal', roles: ['student'] },
      { path: '/competition-management', title: '比赛批次管理', icon: 'Trophy', roles: ['admin'] },
      { path: '/registration-management', title: '报名管理', icon: 'Document', roles: ['admin'] },
      { path: '/pending-reviews', title: '待评审项目', icon: 'StarFilled', roles: ['judge'] },
      { path: '/review-history', title: '评审记录', icon: 'List', roles: ['judge'] }
    ]
  },
  {
    label: '项目',
    roles: ['student', 'teacher', 'judge', 'admin'],
    items: [
      { path: '/my-projects', title: '我的项目', icon: 'FolderOpened', roles: ['student'] },
      { path: '/create-project', title: '创建项目', icon: 'CirclePlusFilled', roles: ['student'] },
      { path: '/guide-projects', title: '指导项目', icon: 'FolderOpened', roles: ['teacher'] },
      { path: '/project-review', title: '项目审核', icon: 'DocumentChecked', roles: ['teacher'] },
      { path: '/project-management', title: '项目管理', icon: 'FolderOpened', roles: ['admin'] },
      { path: '/review-management', title: '评审管理', icon: 'StarFilled', roles: ['admin'] }
    ]
  },
  {
    label: '学习',
    roles: ['student', 'teacher', 'judge', 'admin'],
    items: [
      { path: '/training-camps', title: '训练营', icon: 'School', roles: ['student', 'teacher', 'judge', 'admin'] },
      { path: '/courses', title: '在线课程', icon: 'Collection', roles: ['student', 'teacher', 'judge', 'admin'] },
      { path: '/industry-topics', title: '产业命题', icon: 'Briefcase', roles: ['student', 'teacher', 'judge', 'admin'] },
      { path: '/certificates', title: '证书成果', icon: 'Medal', roles: ['student'] }
    ]
  },
  {
    label: '工具',
    roles: ['student', 'teacher', 'judge', 'admin'],
    items: []
  },
  {
    label: '管理',
    roles: ['admin'],
    items: [
      { path: '/user-management', title: '用户管理', icon: 'UserFilled', roles: ['admin'] },
      { path: '/dashboard', title: '数据看板', icon: 'TrendCharts', roles: ['admin'] }
    ]
  }
]

const visibleMenuGroups = computed(() => {
  const role = userStore.userInfo?.role
  if (!role) return []
  return menuGroups
    .filter(group => group.roles.includes(role))
    .map(group => ({
      ...group,
      items: group.items.filter(item => item.roles.includes(role))
    }))
    .filter(group => group.items.length > 0)
})

const isMenuActive = (path) => {
  if (route.path === path) return true
  // /create-project 只匹配自身，不匹配 /my-projects
  if (path === '/create-project' && route.path === '/create-project') return true
  // /my-projects 匹配项目相关页面，但不匹配 /create-project
  if (path === '/my-projects' && route.path.startsWith('/projects/')) return true
  if (path === '/my-projects' && route.path === '/my-projects') return true
  return false
}

const roleText = computed(() => {
  const map = {
    student: '学生',
    teacher: '指导老师',
    judge: '评委',
    admin: '管理员'
  }
  return map[userStore.userInfo?.role] || ''
})

const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value
}

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
  if (mobileMenuOpen.value) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
}

const closeMobileMenu = () => {
  mobileMenuOpen.value = false
  document.body.style.overflow = ''
}

// 监听窗口大小变化，自动关闭移动菜单
const handleResize = () => {
  if (window.innerWidth > 1024 && mobileMenuOpen.value) {
    closeMobileMenu()
  }
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  document.body.style.overflow = ''
})

const handleCommand = async (command) => {
  if (command === 'logout') {
    try {
      await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
      userStore.logout()
      ElMessage.success('已退出登录')
      // 使用 window.location.href 强制刷新跳转到登录页，确保所有状态完全重置
      window.location.href = '/login'
    } catch {
      // 用户点击取消，不做任何操作
    }
  } else if (command === 'portal') {
    router.push('/portal')
  }
}
</script>

<style scoped>
.main-layout {
  display: flex;
  min-height: 100vh;
  background-color: var(--bg-secondary);
}

/* ========== 移动端遮罩层 ========== */
.mobile-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 200;
}

.fade-overlay-enter-active,
.fade-overlay-leave-active {
  transition: opacity 0.3s ease;
}

.fade-overlay-enter-from,
.fade-overlay-leave-to {
  opacity: 0;
}

/* ========== 移动端侧滑菜单 ========== */
.mobile-sidebar {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  width: 280px;
  background-color: var(--bg-sidebar);
  z-index: 300;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.slide-menu-enter-active,
.slide-menu-leave-active {
  transition: transform 0.3s ease;
}

.slide-menu-enter-from,
.slide-menu-leave-to {
  transform: translateX(-100%);
}

.mobile-sidebar-header {
  padding: 20px 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.mobile-close-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: transparent;
  border: none;
  color: var(--text-sidebar);
  cursor: pointer;
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

.mobile-close-btn:hover {
  background-color: var(--bg-sidebar-hover);
  color: var(--text-inverse);
}

.mobile-sidebar-nav {
  flex: 1;
  padding: 12px 8px;
  overflow-y: auto;
}

/* ========== 桌面端侧边栏 ========== */
.sidebar {
  width: var(--sidebar-width);
  background-color: var(--bg-sidebar);
  display: flex;
  flex-direction: column;
  transition: width var(--transition-normal);
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 100;
  overflow-y: auto;
}

.sidebar.collapsed {
  width: var(--sidebar-collapsed-width);
}

.sidebar-header {
  padding: 20px 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-text {
  font-family: var(--font-heading);
  font-size: 18px;
  font-weight: 600;
  color: var(--text-inverse);
  white-space: nowrap;
}

.sidebar-nav {
  flex: 1;
  padding: 12px 8px;
  overflow-y: auto;
}

.nav-group-label {
  padding: 16px 16px 6px;
  font-size: 11px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.35);
  text-transform: uppercase;
  letter-spacing: 1px;
  white-space: nowrap;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  margin-bottom: 2px;
  border-radius: var(--radius-md);
  color: var(--text-sidebar);
  text-decoration: none;
  transition: all var(--transition-fast);
  cursor: pointer;
  position: relative;
}

.nav-item:hover {
  background-color: var(--bg-sidebar-hover);
  color: var(--text-inverse);
}

/* 侧边栏活跃项 - 左侧边框指示器 */
.nav-item.active {
  background-color: var(--bg-sidebar-active);
  color: var(--text-sidebar-active);
}

.nav-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 4px;
  bottom: 4px;
  width: 3px;
  background-color: var(--primary-500);
  border-radius: 0 2px 2px 0;
}

.nav-text {
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
}

.sidebar-footer {
  padding: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.collapse-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px;
  background: transparent;
  border: none;
  color: var(--text-sidebar);
  cursor: pointer;
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

.collapse-btn:hover {
  background-color: var(--bg-sidebar-hover);
  color: var(--text-inverse);
}

/* ========== 主内容区 ========== */
.main-content {
  flex: 1;
  margin-left: var(--sidebar-width);
  transition: margin-left var(--transition-normal);
  display: flex;
  flex-direction: column;
}

.main-content.expanded {
  margin-left: var(--sidebar-collapsed-width);
}

.main-content.no-sidebar {
  margin-left: 0;
}

/* ========== 顶部导航栏 ========== */
.top-header {
  height: var(--header-height);
  background-color: var(--bg-primary);
  border-bottom: 1px solid var(--border-light);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  position: sticky;
  top: 0;
  z-index: 50;
}

.top-header.platform-header {
  background-color: #ffffff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 40px;
}

/* 汉堡菜单按钮 - 默认隐藏 */
.hamburger-btn {
  display: none;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: transparent;
  border: none;
  color: var(--text-primary);
  cursor: pointer;
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
  flex-shrink: 0;
}

.hamburger-btn:hover {
  background-color: var(--bg-tertiary);
}

.header-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  transition: opacity var(--transition-fast);
  flex-shrink: 0;
}

.header-logo:hover {
  opacity: 0.8;
}

.header-logo-text {
  font-family: var(--font-heading);
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  white-space: nowrap;
}

.top-nav {
  display: flex;
  align-items: center;
  gap: 4px;
}

.top-nav-item {
  padding: 8px 16px;
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all var(--transition-fast);
  white-space: nowrap;
  position: relative;
}

.top-nav-item:hover {
  color: var(--primary-600);
  background-color: var(--primary-50);
}

/* 顶部导航活跃项 - 底部边框指示器 + 颜色 */
.top-nav-item.active {
  color: var(--primary-600);
  background-color: var(--primary-50);
  font-weight: 600;
}

.top-nav-item.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 16px;
  right: 16px;
  height: 2px;
  background-color: var(--primary-500);
  border-radius: 1px 1px 0 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 12px;
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: background-color var(--transition-fast);
}

.user-info:hover {
  background-color: var(--bg-tertiary);
}

.user-avatar {
  background-color: var(--primary-100);
  color: var(--primary-600);
}

.user-meta {
  display: flex;
  flex-direction: column;
  line-height: 1.3;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.user-role {
  font-size: 12px;
  color: var(--text-tertiary);
}

.dropdown-icon {
  color: var(--text-tertiary);
  margin-left: 4px;
}

.page-content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

.page-content.platform-page {
  padding: 0;
}

/* ========== 响应式：平板端 (768px - 1024px) ========== */
@media (max-width: 1024px) {
  .hamburger-btn {
    display: flex;
  }

  .top-nav {
    display: none;
  }

  .header-left {
    gap: 12px;
  }

  /* 平板端隐藏桌面侧边栏，使用移动端侧滑菜单替代 */
  .sidebar {
    display: none;
  }

  .main-content {
    margin-left: 0 !important;
  }
}

/* ========== 响应式：移动端 (< 768px) ========== */
@media (max-width: 768px) {
  .header-logo-text {
    display: none;
  }

  .user-meta {
    display: none;
  }

  .top-header {
    padding: 0 12px;
  }

  .mobile-sidebar {
    width: 260px;
  }
}
</style>
