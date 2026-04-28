<template>
  <div class="main-layout">
    <!-- 侧边栏 -->
    <aside class="sidebar" :class="{ collapsed: isCollapsed }">
      <div class="sidebar-header">
        <div class="logo">
          <el-icon size="28" color="var(--primary-400)"><Trophy /></el-icon>
          <span v-show="!isCollapsed" class="logo-text">创新创业平台</span>
        </div>
      </div>

      <nav class="sidebar-nav">
        <router-link
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ active: $route.path === item.path }"
        >
          <el-icon size="18">
            <component :is="item.icon" />
          </el-icon>
          <span v-show="!isCollapsed" class="nav-text">{{ item.title }}</span>
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <button class="collapse-btn" @click="toggleCollapse">
          <el-icon size="16">
            <component :is="isCollapsed ? 'Expand' : 'Fold'" />
          </el-icon>
        </button>
      </div>
    </aside>

    <!-- 主内容区 -->
    <div class="main-content" :class="{ expanded: isCollapsed }">
      <!-- 顶部导航 -->
      <header class="top-header">
        <div class="header-left">
          <h2 class="page-title">{{ currentPageTitle }}</h2>
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
                <el-dropdown-item command="profile">
                  <el-icon><User /></el-icon>个人中心
                </el-dropdown-item>
                <el-dropdown-item divided command="logout">
                  <el-icon><SwitchButton /></el-icon>退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </header>

      <!-- 页面内容 -->
      <main class="page-content">
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
import { roleRoutes } from '@/router'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const isCollapsed = ref(false)

const menuItems = computed(() => {
  const role = userStore.userInfo?.role
  return role && roleRoutes[role] ? roleRoutes[role] : []
})

const currentPageTitle = computed(() => {
  const current = menuItems.value.find(item => item.path === route.path)
  return current?.meta?.title || '工作台'
})

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
      // 取消
    }
  } else if (command === 'profile') {
    // TODO: 个人中心
  }
}
</script>

<style scoped>
.main-layout {
  display: flex;
  min-height: 100vh;
  background-color: var(--bg-secondary);
}

/* 侧边栏 */
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

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  margin-bottom: 4px;
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

/* 主内容区 */
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

/* 顶部导航 */
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

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
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

/* 页面内容 */
.page-content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}
</style>
