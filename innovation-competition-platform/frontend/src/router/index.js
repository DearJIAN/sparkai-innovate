import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

// 公共路由
const publicRoutes = [
  {
    path: '/',
    name: 'Root',
    redirect: '/login',
    meta: { public: true }
  },
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

const platformMeta = { platformPage: true }
const withPlatformMeta = (meta = {}) => ({ ...meta, ...platformMeta })

// 所有路由配置（不带角色前缀）
const allRoutes = [
  // 学生专属
  { path: '/my-projects', name: 'MyProjects', component: () => import('@/views/projects/my-projects.vue'), meta: { title: '我的项目', icon: 'FolderOpened', roles: ['student'] } },
  { path: '/create-project', name: 'CreateProject', component: () => import('@/views/projects/create.vue'), meta: { title: '创建项目', icon: 'CirclePlusFilled', roles: ['student'] } },

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
  // 门户列表页面 - 公开访问（无需登录）
  { path: '/portal', name: 'Portal', component: () => import('@/views/portal/PortalHome.vue'), meta: withPlatformMeta({ title: '平台首页', icon: 'HomeFilled', public: true }) },
  { path: '/competition-center', name: 'CompetitionCenter', component: () => import('@/views/portal/CompetitionCenter.vue'), meta: withPlatformMeta({ title: '竞赛报名中心', icon: 'Trophy', public: true }) },
  { path: '/external-competitions', name: 'ExternalCompetitions', component: () => import('@/views/portal/ExternalCompetitions.vue'), meta: withPlatformMeta({ title: '校外竞赛', icon: 'Link', public: true }) },
  { path: '/external-competitions/:slug', name: 'ExternalCompetitionDetail', component: () => import('@/views/portal/ExternalCompetitionDetail.vue'), meta: withPlatformMeta({ title: '校外竞赛详情', icon: 'Link', hidden: true, public: true }) },
  { path: '/competitions', name: 'Competitions', component: () => import('@/views/portal/CompetitionSquare.vue'), meta: withPlatformMeta({ title: '校内竞赛', icon: 'Trophy', public: true }) },
  { path: '/competitions/:id', name: 'CompetitionDetail', component: () => import('@/views/portal/CompetitionDetail.vue'), meta: withPlatformMeta({ title: '校内竞赛详情', icon: 'Trophy', hidden: true, public: true }) },
  { path: '/competitions/:id/register', name: 'CompetitionRegister', component: () => import('@/views/portal/CompetitionRegister.vue'), meta: withPlatformMeta({ title: '竞赛报名', icon: 'Edit', hidden: true, roles: ['student'] }) },
  { path: '/my-registrations', name: 'MyRegistrations', component: () => import('@/views/portal/MyRegistrations.vue'), meta: withPlatformMeta({ title: '我的赛事', icon: 'Medal', roles: ['student'] }) },
  { path: '/training-camps', name: 'TrainingCamps', component: () => import('@/views/portal/TrainingCamps.vue'), meta: withPlatformMeta({ title: '训练营', icon: 'School', public: true }) },
  { path: '/training-camps/:id', name: 'TrainingCampDetail', component: () => import('@/views/portal/TrainingCampDetail.vue'), meta: withPlatformMeta({ title: '训练营详情', icon: 'School', hidden: true, public: true }) },
  { path: '/courses', name: 'Courses', component: () => import('@/views/portal/Courses.vue'), meta: withPlatformMeta({ title: '在线课程', icon: 'Collection', public: true }) },
  { path: '/courses/:id', name: 'CourseDetail', component: () => import('@/views/portal/CourseDetail.vue'), meta: withPlatformMeta({ title: '课程详情', icon: 'Collection', hidden: true, public: true }) },
  { path: '/industry-topics', name: 'IndustryTopics', component: () => import('@/views/portal/IndustryTopics.vue'), meta: withPlatformMeta({ title: '产业命题', icon: 'Briefcase', public: true }) },
  { path: '/industry-topics/:id', name: 'IndustryTopicDetail', component: () => import('@/views/portal/IndustryTopicDetail.vue'), meta: withPlatformMeta({ title: '产业命题详情', icon: 'Briefcase', hidden: true, public: true }) },
  { path: '/accept-topic/:id', name: 'AcceptTopic', component: () => import('@/views/portal/AcceptTopic.vue'), meta: withPlatformMeta({ title: '承接命题', icon: 'Briefcase', hidden: true, roles: ['student'] }) },
  { path: '/certificates', name: 'Certificates', component: () => import('@/views/portal/Certificates.vue'), meta: withPlatformMeta({ title: '证书成果', icon: 'Medal', roles: ['student'] }) },
  { path: '/assessment', name: 'OnlineAssessment', component: () => import('@/views/portal/OnlineAssessment.vue'), meta: withPlatformMeta({ title: '在线测评', icon: 'TrendCharts', public: true }) },
  { path: '/assessment/:id', name: 'AssessmentDetail', component: () => import('@/views/portal/AssessmentDetail.vue'), meta: withPlatformMeta({ title: '开始测评', icon: 'TrendCharts', hidden: true, public: true }) },
  { path: '/assessment/:id/result', name: 'AssessmentResult', component: () => import('@/views/portal/AssessmentResult.vue'), meta: withPlatformMeta({ title: '测评结果', icon: 'TrendCharts', hidden: true, public: true }) },
  { path: '/assessment/:id/coming-soon', name: 'AssessmentComingSoon', component: () => import('@/views/portal/AssessmentComingSoon.vue'), meta: withPlatformMeta({ title: '建设中', icon: 'TrendCharts', hidden: true, public: true }) },

  // AI材料评估
  { path: '/ai-material-evaluation', name: 'AIMaterialEvaluation', component: () => import('@/views/portal/AIMaterialEvaluation.vue'), meta: withPlatformMeta({ title: 'AI材料评估', icon: 'DataAnalysis', public: true }) },
  { path: '/ai-material-evaluation/upload/:type', name: 'AIMaterialEvaluationUpload', component: () => import('@/views/portal/AIMaterialEvaluationUpload.vue'), meta: withPlatformMeta({ title: '上传材料', icon: 'DataAnalysis', hidden: true, public: true }) },
  { path: '/ai-material-evaluation/progress/:taskId', name: 'AIMaterialEvaluationProgress', component: () => import('@/views/portal/AIMaterialEvaluationProgress.vue'), meta: withPlatformMeta({ title: 'AI分析进度', icon: 'DataAnalysis', hidden: true, public: true }) },
  { path: '/ai-material-evaluation/report/:taskId', name: 'AIMaterialEvaluationReport', component: () => import('@/views/portal/AIMaterialEvaluationReport.vue'), meta: withPlatformMeta({ title: '评估报告', icon: 'DataAnalysis', hidden: true, public: true }) },

  // 通用路由（所有角色可访问）
  { path: '/dashboard', name: 'Dashboard', component: () => import('@/views/dashboard/index.vue'), meta: { title: '工作台', icon: 'HomeFilled' } },
  { path: '/projects/:id', name: 'ProjectDetail', component: () => import('@/views/projects/detail.vue'), meta: { title: '项目详情', icon: 'Document', hidden: true } },
  { path: '/projects/:id/edit', name: 'ProjectEdit', component: () => import('@/views/projects/edit.vue'), meta: { title: '编辑项目', icon: 'Edit', hidden: true } },
  { path: '/projects/:id/members', name: 'ProjectMembers', component: () => import('@/views/projects/members.vue'), meta: { title: '团队成员', icon: 'User', hidden: true } },
  { path: '/projects/:id/files', name: 'ProjectFiles', component: () => import('@/views/projects/files.vue'), meta: { title: '项目材料', icon: 'Document', hidden: true } },
  { path: '/projects/:id/tasks', name: 'ProjectTasks', component: () => import('@/views/projects/tasks.vue'), meta: { title: '任务进度', icon: 'List', hidden: true } },
  { path: '/reviews/:id', name: 'ReviewDetail', component: () => import('@/views/reviews/detail.vue'), meta: { title: '项目评审', icon: 'StarFilled', hidden: true } },
  { path: '/ai-assistant', name: 'AiAssistant', component: () => import('@/views/ai-assistant/index.vue'), meta: { title: 'AI 助手（备用）', icon: 'MagicStick', hidden: true } }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes: [
    ...publicRoutes,
    {
      path: '/',
      component: () => import('@/layouts/MainLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        { path: '', redirect: '/portal' },
        ...allRoutes
      ]
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
    document.title = `${to.meta.title} - 火花智创`
  }

  // 公共页面处理
  if (to.meta.public) {
    // 如果用户已登录（有token且有userInfo），访问登录/注册页时重定向到首页
    if (userStore.token && userStore.userInfo && (to.path === '/login' || to.path === '/register')) {
      next('/portal')
    } else {
      next()
    }
    return
  }

  // 未登录跳转到登录页
  if (!userStore.token) {
    next({ path: '/login', query: { redirect: to.fullPath } })
    return
  }

  // 等待用户信息加载完成
  if (!userStore.userInfo) {
    userStore.init().then((success) => {
      // 如果初始化失败（token无效），跳转到登录页
      if (!success && !userStore.userInfo) {
        next({ path: '/login', query: { redirect: to.fullPath } })
      } else {
        checkPermission(to, next, useUserStore())
      }
    }).catch(() => {
      next({ path: '/login', query: { redirect: to.fullPath } })
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
