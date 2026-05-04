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
          title: '欢迎使用火花智创',
          content: '欢迎来到火花智创 SparkAI Innovate！本平台集竞赛报名、项目管理、AI 智能体、AI 对话助手、语音交互、训练营、在线课程、产业命题、证书成果于一体。让我带你快速了解所有功能。',
          target: null,
          position: 'center'
        },
        {
          title: '平台首页',
          content: '首页展示平台数据统计、功能入口快捷导航、智能竞赛推荐和快捷操作。点击功能卡片可快速跳转到对应模块，AI 智能体根据你的项目自动推荐合适竞赛。',
          target: '.portal-banner',
          position: 'bottom',
          routePath: '/portal'
        },
        {
          title: '竞赛广场',
          content: '浏览所有可用赛事，查看竞赛详情页的时间安排、奖项设置、赛道信息。点击"立即报名"参与比赛，支持团队报名和材料上传。',
          target: '.top-nav-item[href="/competitions"]',
          position: 'bottom',
          routePath: '/competitions'
        },
        {
          title: '我的赛事',
          content: '查看你已报名的所有竞赛，跟踪报名状态、团队信息和材料提交进度。支持在线修改报名信息和更换团队成员。',
          target: '.top-nav-item[href="/my-registrations"]',
          position: 'bottom',
          routePath: '/my-registrations'
        },
        {
          title: '创新创业训练营',
          content: '提供4大主题训练营：创新基础、商业计划书写作、路演表达、AI项目孵化。每个训练营包含完整大纲、章节视频和讲师信息。完成训练营可获得结业证书。',
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
          content: '查看企业发布的真实命题，了解命题需求、周期和奖励。点击"承接命题"即可开始项目对接，填写承接信息参与产业赛道。',
          target: '.top-nav-item[href="/industry-topics"]',
          position: 'bottom',
          routePath: '/industry-topics'
        },
        {
          title: '项目管理',
          content: '创建和管理你的创新创业项目。填写项目信息、选择赛道和阶段，邀请团队成员协作。项目详情页可查看 AI 智能体分析结果和建议。',
          target: '.top-nav-item[href="/my-projects"]',
          position: 'bottom',
          routePath: '/my-projects'
        },
        {
          title: 'AI 项目智能体（核心能力）',
          content: '点击左下角「火花」→ 切换到"智能体"标签页，可解锁专属 AI 能力：🎯 智能引航（语音/文字导航）、📄 AI 材料问答（上传材料后随时提问）、📋 AI 商业计划书体检（自动检查完整性）、🎤 AI 路演稿生成（一键生成路演答辩稿）、🎬 AI 模拟路演答辩（AI 扮演评委提问）、💡 AI 项目创意生成（帮你头脑风暴）、🎯 AI 智能竞赛推荐（根据项目自动匹配赛事）。',
          target: '#waifu',
          position: 'right',
          tip: '提示：首页"竞赛推荐"卡片可直接唤起智能体，无需手动切换。'
        },
        {
          title: '证书与成果',
          content: '查看你获得的训练营结业证书和竞赛获奖记录。所有证书支持查看详情和下载 PDF 版本。',
          target: '.top-nav-item[href="/certificates"]',
          position: 'bottom',
          routePath: '/certificates'
        },
        {
          title: 'AI 助手「火花」',
          content: '左下角的 Live2D 看板娘「火花」是你的 AI 伙伴！支持文字/语音对话、AI 流式回复、语音朗读，火花会根据对话内容自动切换表情。在 AI 分析模式下可为项目生成简介、商业建议和风险分析报告。支持拖拽调整窗口大小。',
          target: '#waifu',
          position: 'right'
        },
        {
          title: '开始你的创新创业之旅',
          content: '现在你已经了解了平台的所有核心功能！从浏览竞赛开始，利用 AI 智能体优化方案，参加训练营提升能力，创建项目参与竞赛，最终获得证书和奖项。祝你好运！',
          target: null,
          position: 'center'
        }
      ],
      teacher: [
        {
          title: '欢迎使用火花智创',
          content: '欢迎老师！平台集竞赛管理、项目指导、AI 智能体、AI 对话助手、语音交互、训练营、在线课程等功能于一体。让我带你快速了解指导老师视角的全部功能。',
          target: null,
          position: 'center'
        },
        {
          title: '导航与工作台',
          content: '通过顶部导航或左侧菜单访问各模块。工作台展示你指导的所有学生项目概览、审核进度和统计数据。',
          target: '.top-header',
          position: 'bottom',
          routePath: '/dashboard'
        },
        {
          title: '指导项目管理',
          content: '在"指导项目"页面查看你负责的所有学生项目列表，点击进入详情页查看项目材料、审核内容、给出指导意见。',
          target: '.top-nav-item[href="/guide-projects"]',
          position: 'right',
          routePath: '/guide-projects'
        },
        {
          title: '项目审核功能',
          content: '对学生提交的项目进行详细审核，检查项目信息的完整性和可行性，给出专业的书面反馈意见帮助学生改进方案。',
          target: null,
          position: 'center',
          routePath: '/project-review'
        },
        {
          title: 'AI 项目智能体',
          content: '点击左下角「火花」→ 切换到"智能体"标签页，可使用：📄 AI 材料问答（快速查阅学生材料）、📋 AI 商业计划书体检（帮学生检查 BP 完整性）、📝 AI 评审辅助（AI 辅助分析项目质量）、✅ AI 批量审核助手（批量生成审核意见）、💬 AI 智能反馈生成（自动生成专业反馈），极大提升指导效率。',
          target: '#waifu',
          position: 'right',
          tip: '提示：指导项目详情页可直接上传材料建立智能体索引。'
        },
        {
          title: '训练营与课程资源',
          content: '推荐学生使用训练营和课程资源提升能力。训练营涵盖创新基础、BP写作、路演表达、AI孵化四大方向，学生完成学习后可获得结业证书。',
          target: '.top-nav-item[href="/training-camps"]',
          position: 'bottom',
          routePath: '/training-camps'
        },
        {
          title: '评审结果查看',
          content: '在项目详情页查看评审结果和评委反馈，协助学生根据反馈改进项目方案，为下次参赛做好准备。',
          target: null,
          position: 'center'
        },
        {
          title: 'AI 助手「火花」',
          content: '左下角的 Live2D 看板娘「火花」是你的 AI 助手入口！支持文字/语音对话、AI 流式回复、语音朗读，火花会根据对话内容自动切换表情。在 AI 分析模式下可为学生项目生成商业计划书建议和风险分析报告。支持拖拽调整窗口大小。',
          target: '#waifu',
          position: 'right'
        },
        {
          title: '开始指导学生',
          content: '现在你已经了解了全部指导功能！善用 AI 智能体和对话助手提升指导效率，祝指导顺利！',
          target: null,
          position: 'center'
        }
      ],
      judge: [
        {
          title: '欢迎使用火花智创',
          content: '欢迎评委老师！平台集项目评审、AI 智能体辅助、AI 对话助手、语音交互、训练营、在线课程等功能于一体。让我带你快速了解评委视角的核心操作。',
          target: null,
          position: 'center'
        },
        {
          title: '导航与数据看板',
          content: '顶部导航快速切换模块，工作台展示待评审和已评审的项目数量统计，以及评审进度概览。',
          target: '.top-header',
          position: 'bottom',
          routePath: '/dashboard'
        },
        {
          title: '待评审项目列表',
          content: '在"待评审项目"页面查看所有分配给你的评审任务，按优先级和时间安排进行评审。支持筛选和排序，提高评审效率。',
          target: '.top-nav-item[href="/pending-reviews"]',
          position: 'right',
          routePath: '/pending-reviews'
        },
        {
          title: '项目评审打分',
          content: '点击项目进入评审详情页，查看项目信息、材料和任务进度。从创新性、可行性、市场前景、团队能力、商业模式、技术实现、路演表现七个维度进行评分，支持添加文字评语。',
          target: null,
          position: 'center'
        },
        {
          title: '评审记录查询',
          content: '在"评审记录"页面查看所有历史评审记录和评分详情，包括各维度评分、总分、评审意见和评审时间，支持查看项目详情。',
          target: '.top-nav-item[href="/review-history"]',
          position: 'right',
          routePath: '/review-history'
        },
        {
          title: 'AI 项目智能体',
          content: '点击左下角「火花」→ 切换到"智能体"标签页，可使用：📄 AI 材料问答（快速查阅项目材料）、📋 AI 商业计划书体检（AI 辅助分析 BP 质量）、📝 AI 评审辅助（AI 生成辅助分析报告作为评审参考）、📝 AI 评审意见草稿（AI 生成评审意见草稿）、📊 AI 评分一致性检查（检查评分合理性），让评审更有依据。',
          target: '#waifu',
          position: 'right',
          tip: '注意：AI 评审辅助仅返回定性分析，不输出具体评分。'
        },
        {
          title: 'AI 助手「火花」',
          content: '左下角的 Live2D 看板娘「火花」是你的 AI 助手入口！支持文字/语音对话、AI 流式回复、语音朗读，火花会根据对话内容自动切换表情。可为项目生成风险分析和建议报告，作为评审参考依据。支持拖拽调整窗口大小。',
          target: '#waifu',
          position: 'right'
        },
        {
          title: '开始评审',
          content: '现在你可以开始评审学生的创新创业项目了！善用 AI 智能体辅助分析，感谢你的专业评审！',
          target: null,
          position: 'center'
        }
      ],
      admin: [
        {
          title: '欢迎使用火花智创',
          content: '欢迎管理员！平台集用户管理、竞赛管理、报名管理、项目管理、评审管理、AI 智能体、AI 对话助手、语音交互、训练营、课程等功能于一体。让我带你了解管理员后台的全部功能。',
          target: null,
          position: 'center'
        },
        {
          title: '管理员数据看板',
          content: '这里展示系统的核心统计数据：用户总数、项目数、评审数、竞赛批次等，配有图表可视化展示，一目了然掌握全局。',
          target: '.page-title',
          position: 'bottom',
          routePath: '/dashboard'
        },
        {
          title: '用户管理',
          content: '在"用户管理"页面查看和管理所有注册用户，编辑用户信息和角色权限（学生/教师/评委/管理员），停用/启用账号。',
          target: '.nav-item[href="/user-management"]',
          position: 'right',
          routePath: '/user-management'
        },
        {
          title: '比赛批次管理',
          content: '创建和管理比赛批次，设置比赛名称、时间范围、状态描述等信息，控制比赛的报名起止和评审流程节点。支持赛道管理。',
          target: '.nav-item[href="/competition-management"]',
          position: 'right',
          routePath: '/competition-management'
        },
        {
          title: '报名管理与审核',
          content: '查看所有参赛报名信息，审核报名材料的完整性和合规性，管理报名状态（待审核/已通过/已驳回）。支持统计分析和批量操作。',
          target: '.nav-item[href="/registration-management"]',
          position: 'right',
          routePath: '/registration-management'
        },
        {
          title: '项目管理总览',
          content: '管理系统中的所有项目，查看项目详情、审核状态、团队信息等，支持对项目进行增删改查操作。',
          target: '.nav-item[href="/project-management"]',
          position: 'right',
          routePath: '/project-management'
        },
        {
          title: '评审管理与监控',
          content: '监控所有评审进度和评分分布情况，分配评审任务给评委，确保评审工作的公平性和及时性。',
          target: '.nav-item[href="/review-management"]',
          position: 'right',
          routePath: '/review-management'
        },
        {
          title: '训练营与课程管理',
          content: '查看训练营和课程模块的学习数据统计，学生参与度和完成率，为平台运营决策提供数据支持。',
          target: '.top-nav-item[href="/training-camps"]',
          position: 'bottom',
          routePath: '/training-camps'
        },
        {
          title: 'AI 项目智能体',
          content: '点击左下角「火花」→ 切换到"智能体"标签页，管理员可使用全部 12 大 AI 能力：智能引航、AI 材料问答、AI BP体检、AI 路演稿生成、AI 模拟路演答辩、AI 评审辅助、AI 智能竞赛推荐、AI 项目创意生成、AI 批量审核助手、AI 智能反馈生成、AI 评审意见草稿、AI 评分一致性检查。可帮助测试和审核平台的 AI 服务质量。',
          target: '#waifu',
          position: 'right'
        },
        {
          title: 'AI 助手「火花」',
          content: '左下角的 Live2D 看板娘「火花」是平台的 AI 助手入口！支持文字/语音对话、AI 流式回复、语音朗读，火花会根据对话内容自动切换表情。在 AI 分析模式下可生成项目简介、商业建议和风险分析报告。支持拖拽调整窗口大小。',
          target: '#waifu',
          position: 'right'
        },
        {
          title: '开始管理系统',
          content: '现在你已经了解了管理员后台的全部功能模块。善用 AI 智能体提升管理效率，祝你管理工作顺利！',
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
