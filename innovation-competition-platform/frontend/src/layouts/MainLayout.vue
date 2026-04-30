<template>
  <div class="main-layout">
    <aside
      v-if="showSidebar"
      class="sidebar"
      :class="{ collapsed: isCollapsed }"
    >
      <div class="sidebar-header">
        <div class="logo">
          <el-icon size="28" color="var(--primary-400)"><Trophy /></el-icon>
          <span v-show="!isCollapsed" class="logo-text">创新创业平台</span>
        </div>
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
          <div class="header-logo" @click="router.push('/portal')">
            <el-icon size="28" color="var(--primary-500)"><Trophy /></el-icon>
            <span class="header-logo-text">双创竞赛服务平台</span>
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
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Trophy, User, UserFilled, HomeFilled, SwitchButton, ArrowDown,
  FolderOpened, CirclePlusFilled, MagicStick, StarFilled, DocumentChecked,
  Expand, Fold, Document, Medal, School, Briefcase, Collection,
  TrendCharts, Calendar, Setting, Edit, List
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const isCollapsed = ref(false)

const platformPages = [
  '/portal', '/competitions', '/training-camps', '/courses',
  '/ai-assistant', '/industry-topics', '/my-registrations', '/certificates'
]

const isPlatformPage = computed(() => {
  return platformPages.some(path => route.path === path || route.path.startsWith(path + '/'))
})

const showSidebar = computed(() => {
  if (isPlatformPage.value) return false
  return true
})

const topNavConfig = [
  { path: '/portal', title: '首页', roles: ['student', 'teacher', 'judge', 'admin'] },
  { path: '/competitions', title: '竞赛', roles: ['student', 'teacher', 'judge', 'admin'] },
  { path: '/my-projects', title: '项目', roles: ['student'] },
  { path: '/guide-projects', title: '项目', roles: ['teacher'] },
  { path: '/pending-reviews', title: '评审', roles: ['judge'] },
  { path: '/project-management', title: '管理', roles: ['admin'] },
  { path: '/training-camps', title: '训练营', roles: ['student', 'teacher'] },
  { path: '/courses', title: '课程', roles: ['student', 'teacher'] },
  { path: '/ai-assistant', title: 'AI 助手', roles: ['student', 'teacher', 'judge', 'admin'] }
]

const topNavItems = computed(() => {
  const role = userStore.userInfo?.role
  if (!role) return []
  return topNavConfig.filter(item => item.roles.includes(role))
})

const isTopNavActive = (path) => {
  if (path === '/portal') return route.path === '/portal'
  if (path === '/competitions') return route.path.startsWith('/competitions')
  if (path === '/my-projects') return route.path.startsWith('/my-projects') || route.path.startsWith('/create-project') || route.path.startsWith('/projects/')
  if (path === '/guide-projects') return route.path.startsWith('/guide-projects') || route.path.startsWith('/project-review')
  if (path === '/pending-reviews') return route.path.startsWith('/pending-reviews') || route.path.startsWith('/review-history')
  if (path === '/project-management') return route.path.startsWith('/project-management') || route.path.startsWith('/user-management') || route.path.startsWith('/competition-management') || route.path.startsWith('/review-management') || route.path.startsWith('/registration-management') || route.path.startsWith('/dashboard')
  if (path === '/training-camps') return route.path.startsWith('/training-camps')
  if (path === '/courses') return route.path.startsWith('/courses')
  if (path === '/ai-assistant') return route.path.startsWith('/ai-assistant')
  return route.path === path
}

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
    roles: ['student', 'admin'],
    items: [
      { path: '/my-registrations', title: '我的赛事', icon: 'Medal', roles: ['student'] },
      { path: '/competition-management', title: '比赛批次管理', icon: 'Trophy', roles: ['admin'] },
      { path: '/registration-management', title: '报名管理', icon: 'Document', roles: ['admin'] }
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
      { path: '/pending-reviews', title: '待评审项目', icon: 'StarFilled', roles: ['judge'] },
      { path: '/review-history', title: '评审记录', icon: 'List', roles: ['judge'] },
      { path: '/project-management', title: '项目管理', icon: 'FolderOpened', roles: ['admin'] },
      { path: '/review-management', title: '评审管理', icon: 'StarFilled', roles: ['admin'] }
    ]
  },
  {
    label: '学习',
    roles: ['student', 'teacher'],
    items: [
      { path: '/training-camps', title: '训练营', icon: 'School', roles: ['student', 'teacher'] },
      { path: '/courses', title: '在线课程', icon: 'Collection', roles: ['student', 'teacher'] },
      { path: '/industry-topics', title: '产业命题', icon: 'Briefcase', roles: ['student', 'teacher'] },
      { path: '/certificates', title: '证书成果', icon: 'Medal', roles: ['student'] }
    ]
  },
  {
    label: '工具',
    roles: ['student', 'teacher', 'judge', 'admin'],
    items: [
      { path: '/ai-assistant', title: 'AI 项目助手', icon: 'MagicStick', roles: ['student', 'teacher', 'judge', 'admin'] }
    ]
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
  if (path === '/my-projects' && route.path.startsWith('/projects/')) return true
  if (path === '/my-projects' && route.path === '/create-project') return true
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

const handleCommand = async (command) => {
  if (command === 'logout') {
    try {
      await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
      userStore.logout()
      router.push('/login')
      ElMessage.success('已退出登录')
    } catch {
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
}

.nav-item:hover {
  background-color: var(--bg-sidebar-hover);
  color: var(--text-inverse);
}

.nav-item.active {
  background-color: var(--bg-sidebar-active);
  color: var(--text-sidebar-active);
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

.header-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  transition: opacity var(--transition-fast);
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
}

.top-nav-item:hover {
  color: var(--primary-600);
  background-color: var(--primary-50);
}

.top-nav-item.active {
  color: var(--primary-600);
  background-color: var(--primary-50);
  font-weight: 600;
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

@media (max-width: 1024px) {
  .top-nav {
    display: none;
  }

  .header-left {
    gap: 16px;
  }
}

@media (max-width: 768px) {
  .header-logo-text {
    display: none;
  }

  .user-meta {
    display: none;
  }
}
</style>
