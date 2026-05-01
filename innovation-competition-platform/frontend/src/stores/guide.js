import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useGuideStore = defineStore('guide', () => {
  const isVisible = ref(false)
  const currentStep = ref(0)
  const currentRole = ref('')
  const opacity = ref(100)
  const hasShownGuide = ref(false)
  const isFirstLogin = ref(false)

  const opacityValue = computed(() => opacity.value / 100)

  const showGuide = (role, firstLogin = false) => {
    currentRole.value = role
    currentStep.value = 0
    isVisible.value = true
    isFirstLogin.value = firstLogin
    hasShownGuide.value = true
  }

  const hideGuide = () => {
    isVisible.value = false
  }

  const nextStep = () => {
    const steps = getStepsByRole(currentRole.value)
    if (currentStep.value < steps.length - 1) {
      currentStep.value++
    }
  }

  const prevStep = () => {
    if (currentStep.value > 0) {
      currentStep.value--
    }
  }

  const goToStep = (step) => {
    currentStep.value = step
  }

  const setOpacity = (value) => {
    opacity.value = Math.max(10, Math.min(100, value))
  }

  const reset = () => {
    isVisible.value = false
    currentStep.value = 0
    currentRole.value = ''
    opacity.value = 100
    hasShownGuide.value = false
    isFirstLogin.value = false
  }

  const getStepsByRole = (role) => {
    const steps = {
      student: [
        {
          title: '欢迎使用创新创业平台 v3.0',
          content: '欢迎来到双创竞赛服务平台！本平台集竞赛报名、项目管理、AI助手、训练营、在线课程、产业命题、证书成果于一体。让我带你快速了解所有功能。',
          target: null,
          position: 'center'
        },
        {
          title: '平台首页',
          content: '首页展示平台数据统计、功能入口快捷导航、推荐竞赛和快捷操作。点击功能卡片可快速跳转到对应模块。',
          target: '.portal-banner',
          position: 'bottom',
          routePath: '/'
        },
        {
          title: '竞赛广场',
          content: '浏览所有可用赛事，查看竞赛详情页的时间安排、奖项设置、赛道信息。点击"立即报名"参与比赛，支持团队报名。',
          target: '.top-nav-item[href="/competitions"]',
          position: 'bottom',
          routePath: '/competitions'
        },
        {
          title: '我的赛事',
          content: '查看你已报名的所有竞赛，跟踪报名状态、团队信息和材料提交进度。',
          target: '.top-nav-item[href="/my-registrations"]',
          position: 'bottom',
          routePath: '/my-registrations'
        },
        {
          title: '创新创业训练营',
          content: '提供4大主题训练营：创新基础、商业计划书写作、路演表达、AI项目孵化。每个训练营包含完整大纲、章节视频和讲师信息。点击"开始学习"进入学习。',
          target: '.top-nav-item[href="/training-camps"]',
          position: 'bottom',
          routePath: '/training-camps'
        },
        {
          title: '在线课程中心',
          content: '系统化课程体系：创业基础、市场调研、商业模式设计、路演技巧、法律知识等。支持视频学习和进度跟踪。',
          target: '.top-nav-item[href="/courses"]',
          position: 'bottom',
          routePath: '/courses'
        },
        {
          title: '产业命题',
          content: '查看企业发布的真实命题，了解命题需求、周期和奖励。点击"承接命题"即可开始项目对接。',
          target: '.top-nav-item[href="/industry-topics"]',
          position: 'bottom',
          routePath: '/industry-topics'
        },
        {
          title: '项目管理',
          content: '创建和管理你的创新创业项目。填写项目信息、选择赛道和阶段，邀请团队成员协作。',
          target: '.top-nav-item[href="/my-projects"]',
          position: 'bottom',
          routePath: '/my-projects'
        },
        {
          title: '证书与成果',
          content: '查看你获得的训练营结业证书和竞赛获奖记录。所有证书支持查看详情和下载。',
          target: '.top-nav-item[href="/certificates"]',
          position: 'bottom',
          routePath: '/certificates'
        },
        {
          title: 'AI 助手「火花」',
          content: '左下角的 Live2D 看板娘「火花」是你的 AI 助手！点击打开对话面板，支持文字/语音输入、AI 流式对话、语音朗读。还可切换"AI 分析"模式生成项目简介、商业建议和风险分析。',
          target: '#waifu',
          position: 'right'
        },
        {
          title: '开始你的创新创业之旅',
          content: '现在你已经了解了平台的所有核心功能！从浏览竞赛开始，利用 AI 助手优化方案，参加训练营提升能力，创建项目参与竞赛，最终获得证书和奖项。祝你好运！',
          target: null,
          position: 'center'
        }
      ],
      teacher: [
        {
          title: '欢迎使用创新创业平台 v2.0',
          content: '欢迎老师！平台已升级至 v2.0，新增 AI 对话、Live2D 虚拟形象、训练营、课程等功能。让我带你快速了解指导老师视角的功能。',
          target: null,
          position: 'center'
        },
        {
          title: '导航与工作台',
          content: '通过顶部导航或左侧菜单访问各模块。工作台展示你指导的所有学生项目概览。',
          target: '.top-header',
          position: 'bottom',
          routePath: '/dashboard'
        },
        {
          title: '指导项目管理',
          content: '在"指导项目"页面查看你负责的所有学生项目列表，点击进入详情页审核内容、给出指导意见。',
          target: '.nav-item[href="/guide-projects"], .top-nav-item[href*="guide"]',
          position: 'right',
          routePath: '/guide-projects'
        },
        {
          title: '项目审核功能',
          content: '对学生提交的项目进行审核，检查项目信息的完整性和可行性，给出专业反馈意见帮助学生改进。',
          target: null,
          position: 'center'
        },
        {
          title: '训练营与课程资源',
          content: '推荐学生使用训练营和课程资源提升能力。训练营涵盖创新基础、BP写作、路演表达、AI孵化四大方向。',
          target: '.top-nav-item[href="/training-camps"]',
          position: 'bottom',
          routePath: '/training-camps'
        },
        {
          title: 'AI 助手「火花」',
          content: '左下角的 Live2D 看板娘「火花」是你的 AI 助手入口！点击她打开对话面板，可为学生的项目生成商业计划书建议和风险分析报告，辅助你进行更专业的指导。',
          target: '#waifu',
          position: 'right'
        },
        {
          title: '评审结果查看',
          content: '查看项目的评审结果和评委反馈，协助学生根据反馈改进项目方案。',
          target: null,
          position: 'center'
        },
        {
          title: '开始指导学生',
          content: '现在你可以开始查看和指导学生的创新创业项目了！善用 AI 工具提升效率，祝指导顺利！',
          target: null,
          position: 'center'
        }
      ],
      judge: [
        {
          title: '欢迎使用创新创业平台 v2.0',
          content: '欢迎评委老师！平台已升级，新增多项功能。让我带你快速了解评委视角的核心操作。',
          target: null,
          position: 'center'
        },
        {
          title: '导航与数据看板',
          content: '顶部导航快速切换模块，工作台展示待评审和已评审的项目数量统计。',
          target: '.top-header',
          position: 'bottom',
          routePath: '/dashboard'
        },
        {
          title: '待评审项目列表',
          content: '在"待评审项目"页面查看所有分配给你的评审任务，按优先级和时间安排进行评审。',
          target: '.nav-item[href="/pending-reviews"], .top-nav-item[href*="pending"]',
          position: 'right',
          routePath: '/pending-reviews'
        },
        {
          title: '项目评审打分',
          content: '点击项目进入评审详情页，查看项目信息、材料、任务进度，然后从创新性、可行性、市场前景、团队能力、商业模式、技术实现、路演表现七个维度进行评分。',
          target: null,
          position: 'center'
        },
        {
          title: '评审记录查询',
          content: '在"评审记录"页面查看所有历史评审记录和评分详情，支持按时间、状态筛选。',
          target: null,
          position: 'center'
        },
        {
          title: 'AI 辅助参考',
          content: '左下角的 Live2D 看板娘「火花」是你的 AI 助手入口！点击她打开对话面板，可为项目生成风险分析和建议报告，作为评审参考依据。',
          target: '#waifu',
          position: 'right'
        },
        {
          title: '开始评审',
          content: '现在你可以开始评审学生的创新创业项目了！感谢您的专业评审！',
          target: null,
          position: 'center'
        }
      ],
      admin: [
        {
          title: '欢迎使用创新创业平台 v2.0',
          content: '欢迎管理员！平台已全面升级至 v2.0，新增 Live2D 形象、AI 对话、训练营、课程等功能模块。让我带你了解管理员后台的全部功能。',
          target: null,
          position: 'center'
        },
        {
          title: '管理员数据看板',
          content: '这里展示系统的核心统计数据：用户总数、项目数、评审数、竞赛批次等，配有图表可视化展示。',
          target: '.page-title',
          position: 'bottom',
          routePath: '/dashboard'
        },
        {
          title: '用户管理',
          content: '在"用户管理"页面查看和管理所有注册用户，编辑用户信息和角色权限（学生/教师/评委/管理员）。',
          target: '.nav-item[href="/user-management"]',
          position: 'right',
          routePath: '/user-management'
        },
        {
          title: '比赛批次管理',
          content: '创建和管理比赛批次，设置比赛名称、时间范围、状态描述等信息，控制比赛的报名和评审流程。',
          target: '.nav-item[href="/competition-management"]',
          position: 'right',
          routePath: '/competition-management'
        },
        {
          title: '报名管理与审核',
          content: '查看所有参赛报名信息，审核报名材料的完整性和合规性。',
          target: '.nav-item[href="/registration-management"]',
          position: 'right'
        },
        {
          title: '项目管理总览',
          content: '管理系统中的所有项目，查看项目详情、审核状态、团队信息等。',
          target: '.nav-item[href="/project-management"]',
          position: 'right',
          routePath: '/project-management'
        },
        {
          title: '评审管理与监控',
          content: '监控所有评审进度和评分分布情况，确保评审工作的公平性和及时性。',
          target: '.nav-item[href="/review-management"]',
          position: 'right'
        },
        {
          title: '新功能：训练营与课程',
          content: 'v2.0 新增的训练营和课程模块为学生提供系统化学习资源，可在管理后台查看相关数据统计。',
          target: '.top-nav-item[href="/training-camps"]',
          position: 'bottom',
          routePath: '/training-camps'
        },
        {
          title: 'AI 助手「火花」',
          content: '左下角的 Live2D 看板娘「火花」是平台的 AI 助手入口！点击她打开对话面板，支持智能对话和 AI 分析功能（项目简介/商业建议/风险分析）。',
          target: '#waifu',
          position: 'right'
        },
        {
          title: '开始管理系统',
          content: '现在你已经了解了管理员后台的全部功能模块。祝你管理工作顺利！',
          target: null,
          position: 'center'
        }
      ]
    }
    return steps[role] || steps.student
  }

  return {
    isVisible,
    currentStep,
    currentRole,
    opacity,
    hasShownGuide,
    isFirstLogin,
    opacityValue,
    showGuide,
    hideGuide,
    nextStep,
    prevStep,
    goToStep,
    setOpacity,
    reset,
    getStepsByRole
  }
})
