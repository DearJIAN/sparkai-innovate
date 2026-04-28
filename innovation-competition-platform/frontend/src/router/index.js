import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

// 公共路由
const publicRoutes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/index.vue'),
    meta: { public: true, title: '登录' }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/login/register.vue'),
    meta: { public: true, title: '注册' }
  }
]

// 学生菜单
const studentMenus = [
  { path: '/dashboard', name: 'Dashboard', component: () => import('@/views/dashboard/student.vue'), meta: { title: '工作台', icon: 'HomeFilled' } },
  { path: '/my-projects', name: 'MyProjects', component: () => import('@/views/projects/my-projects.vue'), meta: { title: '我的项目', icon: 'FolderOpened' } },
  { path: '/create-project', name: 'CreateProject', component: () => import('@/views/projects/create.vue'), meta: { title: '创建项目', icon: 'CirclePlusFilled' } },
  { path: '/projects/:id', name: 'ProjectDetail', component: () => import('@/views/projects/detail.vue'), meta: { title: '项目详情', icon: 'Document', hidden: true } },
  { path: '/projects/:id/edit', name: 'ProjectEdit', component: () => import('@/views/projects/edit.vue'), meta: { title: '编辑项目', icon: 'Edit', hidden: true } },
  { path: '/projects/:id/members', name: 'ProjectMembers', component: () => import('@/views/projects/members.vue'), meta: { title: '团队成员', icon: 'User', hidden: true } },
  { path: '/ai-assistant', name: 'AIAssistant', component: () => import('@/views/ai-assistant/index.vue'), meta: { title: 'AI 项目助手', icon: 'MagicStick' } }
]

// 教师菜单
const teacherMenus = [
  { path: '/dashboard', name: 'Dashboard', component: () => import('@/views/dashboard/teacher.vue'), meta: { title: '工作台', icon: 'HomeFilled' } },
  { path: '/guide-projects', name: 'GuideProjects', component: () => import('@/views/projects/guide-projects.vue'), meta: { title: '指导项目', icon: 'FolderOpened' } },
  { path: '/project-review', name: 'ProjectReview', component: () => import('@/views/reviews/teacher-review.vue'), meta: { title: '项目审核', icon: 'Check' } },
  { path: '/projects/:id', name: 'ProjectDetail', component: () => import('@/views/projects/detail.vue'), meta: { title: '项目详情', icon: 'Document', hidden: true } }
]

// 评委菜单
const judgeMenus = [
  { path: '/dashboard', name: 'Dashboard', component: () => import('@/views/dashboard/judge.vue'), meta: { title: '工作台', icon: 'HomeFilled' } },
  { path: '/pending-reviews', name: 'PendingReviews', component: () => import('@/views/reviews/pending.vue'), meta: { title: '待评审项目', icon: 'StarFilled' } },
  { path: '/review-history', name: 'ReviewHistory', component: () => import('@/views/reviews/history.vue'), meta: { title: '评审记录', icon: 'DocumentChecked' } },
  { path: '/projects/:id', name: 'ProjectDetail', component: () => import('@/views/projects/detail.vue'), meta: { title: '项目详情', icon: 'Document', hidden: true } }
]

// 管理员菜单
const adminMenus = [
  { path: '/dashboard', name: 'Dashboard', component: () => import('@/views/dashboard/admin.vue'), meta: { title: '数据看板', icon: 'Odometer' } },
  { path: '/user-management', name: 'UserManagement', component: () => import('@/views/admin/users.vue'), meta: { title: '用户管理', icon: 'UserFilled' } },
  { path: '/project-management', name: 'ProjectManagement', component: () => import('@/views/admin/projects.vue'), meta: { title: '项目管理', icon: 'FolderOpened' } },
  { path: '/competition-management', name: 'CompetitionManagement', component: () => import('@/views/admin/competitions.vue'), meta: { title: '比赛管理', icon: 'Trophy' } },
  { path: '/review-management', name: 'ReviewManagement', component: () => import('@/views/admin/reviews.vue'), meta: { title: '评审管理', icon: 'StarFilled' } },
  { path: '/projects/:id', name: 'ProjectDetail', component: () => import('@/views/projects/detail.vue'), meta: { title: '项目详情', icon: 'Document', hidden: true } },
  { path: '/projects/:id/edit', name: 'ProjectEdit', component: () => import('@/views/projects/edit.vue'), meta: { title: '编辑项目', icon: 'Edit', hidden: true } }
]

// 角色路由映射
const roleRoutes = {
  student: studentMenus,
  teacher: teacherMenus,
  judge: judgeMenus,
  admin: adminMenus
}

// 构建动态路由
function buildRoutes() {
  const routes = [...publicRoutes]

  // 为每个角色创建路由配置
  Object.keys(roleRoutes).forEach(role => {
    const menus = roleRoutes[role]
    routes.push({
      path: '/',
      component: () => import('@/layouts/MainLayout.vue'),
      redirect: '/dashboard',
      meta: { role },
      children: menus
    })
  })

  // 404 页面
  routes.push({
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/error/404.vue')
  })

  return routes
}

const router = createRouter({
  history: createWebHistory(),
  routes: buildRoutes()
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - 创新创业平台`
  }

  // 公共页面直接放行
  if (to.meta.public) {
    next()
    return
  }

  // 未登录跳转到登录页
  if (!userStore.token) {
    next('/login')
    return
  }

  // 检查角色权限
  if (to.meta.role && userStore.userInfo?.role !== to.meta.role) {
    // 如果用户已登录但角色不匹配，根据实际角色重定向
    const actualRole = userStore.userInfo?.role
    if (actualRole && roleRoutes[actualRole]) {
      next('/dashboard')
    } else {
      next('/login')
    }
    return
  }

  next()
})

export { roleRoutes }
export default router
