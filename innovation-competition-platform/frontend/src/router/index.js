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

// 所有路由配置（不带角色前缀）
const allRoutes = [
  // 学生专属
  { path: '/my-projects', name: 'MyProjects', component: () => import('@/views/projects/my-projects.vue'), meta: { title: '我的项目', icon: 'FolderOpened', roles: ['student'] } },
  { path: '/create-project', name: 'CreateProject', component: () => import('@/views/projects/create.vue'), meta: { title: '创建项目', icon: 'CirclePlusFilled', roles: ['student'] } },
  { path: '/ai-assistant', name: 'AIAssistant', component: () => import('@/views/ai-assistant/index.vue'), meta: { title: 'AI 项目助手', icon: 'MagicStick', roles: ['student'] } },

  // 教师专属
  { path: '/guide-projects', name: 'GuideProjects', component: () => import('@/views/projects/guide-projects.vue'), meta: { title: '指导项目', icon: 'FolderOpened', roles: ['teacher'] } },
  { path: '/project-review', name: 'ProjectReview', component: () => import('@/views/reviews/teacher-review.vue'), meta: { title: '项目审核', icon: 'Check', roles: ['teacher'] } },

  // 评委专属
  { path: '/pending-reviews', name: 'PendingReviews', component: () => import('@/views/reviews/pending.vue'), meta: { title: '待评审项目', icon: 'StarFilled', roles: ['judge'] } },
  { path: '/review-history', name: 'ReviewHistory', component: () => import('@/views/reviews/history.vue'), meta: { title: '评审记录', icon: 'DocumentChecked', roles: ['judge'] } },

  // 管理员专属
  { path: '/user-management', name: 'UserManagement', component: () => import('@/views/admin/users.vue'), meta: { title: '用户管理', icon: 'UserFilled', roles: ['admin'] } },
  { path: '/project-management', name: 'ProjectManagement', component: () => import('@/views/admin/projects.vue'), meta: { title: '项目管理', icon: 'FolderOpened', roles: ['admin'] } },
  { path: '/competition-management', name: 'CompetitionManagement', component: () => import('@/views/competitions/index.vue'), meta: { title: '比赛批次管理', icon: 'Trophy', roles: ['admin'] } },
  { path: '/registration-management', name: 'RegistrationManagement', component: () => import('@/views/admin/RegistrationManagement.vue'), meta: { title: '报名管理', icon: 'Document', roles: ['admin'] } },
  { path: '/review-management', name: 'ReviewManagement', component: () => import('@/views/admin/reviews.vue'), meta: { title: '评审管理', icon: 'StarFilled', roles: ['admin'] } },

  // 平台页面（所有角色可访问，不显示侧边栏）
  { path: '/portal', name: 'Portal', component: () => import('@/views/portal/PortalHome.vue'), meta: { title: '平台首页', icon: 'HomeFilled' } },
  { path: '/competitions', name: 'Competitions', component: () => import('@/views/portal/CompetitionSquare.vue'), meta: { title: '竞赛广场', icon: 'Trophy' } },
  { path: '/competitions/:id', name: 'CompetitionDetail', component: () => import('@/views/portal/CompetitionDetail.vue'), meta: { title: '竞赛详情', icon: 'Trophy', hidden: true } },
  { path: '/competitions/:id/register', name: 'CompetitionRegister', component: () => import('@/views/portal/CompetitionRegister.vue'), meta: { title: '竞赛报名', icon: 'Edit', hidden: true, roles: ['student'] } },
  { path: '/my-registrations', name: 'MyRegistrations', component: () => import('@/views/portal/MyRegistrations.vue'), meta: { title: '我的赛事', icon: 'Medal', roles: ['student'] } },
  { path: '/training-camps', name: 'TrainingCamps', component: () => import('@/views/portal/TrainingCamps.vue'), meta: { title: '训练营', icon: 'School' } },
  { path: '/courses', name: 'Courses', component: () => import('@/views/portal/Courses.vue'), meta: { title: '在线课程', icon: 'Collection' } },
  { path: '/industry-topics', name: 'IndustryTopics', component: () => import('@/views/portal/IndustryTopics.vue'), meta: { title: '产业命题', icon: 'Briefcase' } },
  { path: '/certificates', name: 'Certificates', component: () => import('@/views/portal/Certificates.vue'), meta: { title: '证书成果', icon: 'Medal', roles: ['student'] } },

  // 通用路由（所有角色可访问）
  { path: '/dashboard', name: 'Dashboard', component: () => import('@/views/dashboard/index.vue'), meta: { title: '工作台', icon: 'HomeFilled' } },
  { path: '/projects/:id', name: 'ProjectDetail', component: () => import('@/views/projects/detail.vue'), meta: { title: '项目详情', icon: 'Document', hidden: true } },
  { path: '/projects/:id/edit', name: 'ProjectEdit', component: () => import('@/views/projects/edit.vue'), meta: { title: '编辑项目', icon: 'Edit', hidden: true } },
  { path: '/projects/:id/members', name: 'ProjectMembers', component: () => import('@/views/projects/members.vue'), meta: { title: '团队成员', icon: 'User', hidden: true } },
  { path: '/projects/:id/files', name: 'ProjectFiles', component: () => import('@/views/projects/files.vue'), meta: { title: '项目材料', icon: 'Document', hidden: true } },
  { path: '/projects/:id/tasks', name: 'ProjectTasks', component: () => import('@/views/projects/tasks.vue'), meta: { title: '任务进度', icon: 'List', hidden: true } },
  { path: '/reviews/:id', name: 'ReviewDetail', component: () => import('@/views/reviews/detail.vue'), meta: { title: '项目评审', icon: 'StarFilled', hidden: true } }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes: [
    ...publicRoutes,
    {
      path: '/',
      component: () => import('@/layouts/MainLayout.vue'),
      children: allRoutes
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('@/views/error/404.vue')
    }
  ]
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
    if (userStore.token && (to.path === '/login' || to.path === '/register')) {
      next('/portal')
    } else {
      next()
    }
    return
  }

  // 未登录跳转到登录页
  if (!userStore.token) {
    next('/login')
    return
  }

  // 等待用户信息加载完成
  if (!userStore.userInfo) {
    userStore.init().then(() => {
      checkPermission(to, next, userStore)
    }).catch(() => {
      next('/login')
    })
    return
  }

  checkPermission(to, next, userStore)
})

function checkPermission(to, next, userStore) {
  const userRole = userStore.userInfo?.role

  // 检查路由是否需要特定角色
  if (to.meta.roles && !to.meta.roles.includes(userRole)) {
    // 角色无权访问，跳转到工作台
    next('/dashboard')
    return
  }

  next()
}

export default router
