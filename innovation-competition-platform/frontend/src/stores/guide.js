import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useGuideStore = defineStore('guide', () => {
  // State
  const isVisible = ref(false)
  const currentStep = ref(0)
  const currentRole = ref('')
  const opacity = ref(100)
  const hasShownGuide = ref(false)
  const isFirstLogin = ref(false)

  // Getters
  const opacityValue = computed(() => opacity.value / 100)

  // Actions
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
          title: '欢迎使用创新创业平台',
          content: '这里是您的创新创业项目管理助手。让我带您快速了解系统的核心功能。',
          target: null,
          position: 'center'
        },
        {
          title: '数据看板',
          content: '这里展示了您的项目概览、待办任务和最新动态，帮助您快速了解当前状态。',
          target: '.page-title',
          position: 'bottom'
        },
        {
          title: '我的项目',
          content: '在"我的项目"页面，您可以创建新的创新创业项目，管理已有项目的详细信息。',
          target: null,
          position: 'center'
        },
        {
          title: '项目详情',
          content: '点击项目卡片进入详情页，您可以编辑项目信息、提交评审、查看评审结果。',
          target: null,
          position: 'center'
        },
        {
          title: '团队成员管理',
          content: '在成员管理页面，您可以添加团队成员、分配角色和分工，打造高效协作团队。',
          target: null,
          position: 'center'
        },
        {
          title: '项目材料上传',
          content: '上传项目申报书、商业计划书、路演PPT等材料，支持多种文件格式。',
          target: null,
          position: 'center'
        },
        {
          title: '任务进度管理',
          content: '创建任务、设置优先级和截止时间，跟踪项目进度，确保按时完成。',
          target: null,
          position: 'center'
        },
        {
          title: 'AI 项目助手',
          content: '使用 AI 助手生成项目简介、商业计划书建议和风险分析，提升项目质量。',
          target: null,
          position: 'center'
        },
        {
          title: '开始您的创新创业之旅',
          content: '现在您可以开始创建自己的创新创业项目了！祝您比赛顺利！',
          target: null,
          position: 'center'
        }
      ],
      teacher: [
        {
          title: '欢迎使用创新创业平台',
          content: '作为指导老师，您可以在这里管理指导的学生项目，协助他们完善项目。',
          target: null,
          position: 'center'
        },
        {
          title: '数据看板',
          content: '查看您指导的所有项目概览，了解项目状态和进度。',
          target: '.page-title',
          position: 'bottom'
        },
        {
          title: '指导项目',
          content: '在"指导项目"页面，查看您负责指导的所有学生项目列表。',
          target: null,
          position: 'center'
        },
        {
          title: '项目详情与审核',
          content: '点击项目查看详情，您可以查看项目材料、审核项目内容、给出指导意见。',
          target: null,
          position: 'center'
        },
        {
          title: '评审结果查看',
          content: '查看项目的评审结果和评委反馈，帮助学生改进项目。',
          target: null,
          position: 'center'
        },
        {
          title: 'AI 助手辅助',
          content: '使用 AI 助手为学生的项目提供商业计划书建议和风险分析。',
          target: null,
          position: 'center'
        },
        {
          title: '开始指导学生',
          content: '现在您可以开始查看和指导学生的创新创业项目了！',
          target: null,
          position: 'center'
        }
      ],
      judge: [
        {
          title: '欢迎使用创新创业平台',
          content: '作为评委，您可以在这里查看待评审项目，进行专业评审打分。',
          target: null,
          position: 'center'
        },
        {
          title: '数据看板',
          content: '查看您的评审任务概览，了解待评审和已评审项目数量。',
          target: '.page-title',
          position: 'bottom'
        },
        {
          title: '待评审项目',
          content: '在"待评审项目"页面，查看所有需要您评审的项目列表。',
          target: null,
          position: 'center'
        },
        {
          title: '项目评审',
          content: '点击项目进入评审页面，查看项目详情、材料、任务进度，然后进行打分。',
          target: null,
          position: 'center'
        },
        {
          title: '评分维度',
          content: '从创新性、可行性、市场前景、团队能力、商业模式、技术实现、路演表现七个维度进行评分。',
          target: null,
          position: 'center'
        },
        {
          title: '评审记录',
          content: '在"评审记录"页面，查看您所有的评审历史和评分详情。',
          target: null,
          position: 'center'
        },
        {
          title: '开始评审',
          content: '现在您可以开始评审学生的创新创业项目了！感谢您的专业评审！',
          target: null,
          position: 'center'
        }
      ],
      admin: [
        {
          title: '欢迎使用创新创业平台',
          content: '作为管理员，您可以在这里管理整个比赛系统，包括用户、项目、比赛批次等。',
          target: null,
          position: 'center'
        },
        {
          title: '管理员数据看板',
          content: '这里展示了系统的核心统计数据：用户数、项目数、评审数等，以及图表可视化。',
          target: '.page-title',
          position: 'bottom'
        },
        {
          title: '用户管理',
          content: '在"用户管理"页面，查看和管理所有注册用户，可以编辑用户信息和权限。',
          target: null,
          position: 'center'
        },
        {
          title: '项目管理',
          content: '查看和管理系统中的所有项目，可以查看项目详情、审核状态。',
          target: null,
          position: 'center'
        },
        {
          title: '比赛批次管理',
          content: '创建和管理比赛批次，设置比赛时间、状态和描述信息。',
          target: null,
          position: 'center'
        },
        {
          title: '评审管理',
          content: '查看所有评审记录，监控评审进度和评分分布。',
          target: null,
          position: 'center'
        },
        {
          title: '系统管理',
          content: '您拥有系统的最高权限，可以管理所有数据和配置。',
          target: null,
          position: 'center'
        },
        {
          title: '开始管理系统',
          content: '现在您可以开始管理创新创业比赛系统了！',
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
