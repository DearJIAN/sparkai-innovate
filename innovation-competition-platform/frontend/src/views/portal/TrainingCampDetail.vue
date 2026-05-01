<template>
  <div class="camp-detail">
    <div class="detail-poster" :class="{ 'has-image': camp.cover }">
      <img
        v-if="camp.cover"
        :src="camp.cover"
        :alt="camp.title"
        class="poster-img"
        @error="handleCoverError"
      />
      <div v-else class="poster-fallback" :style="{ background: camp.gradient }">
        <div class="poster-fallback-content">
          <el-icon size="60" style="color:#fff;margin-bottom:16px;"><component :is="camp.icon" /></el-icon>
          <h1 class="poster-title">{{ camp.title }}</h1>
        </div>
      </div>
      <div class="poster-overlay">
        <div class="poster-info">
          <div class="poster-tags" v-if="camp.cover">
            <el-tag type="warning" size="large">{{ camp.difficulty }}</el-tag>
            <el-tag size="large" class="category-tag">训练营</el-tag>
          </div>
          <h1 class="poster-title" v-if="camp.cover">{{ camp.title }}</h1>
          <p class="poster-desc">{{ camp.description }}</p>
          <div class="poster-stats">
            <span class="stat"><el-icon><Clock /></el-icon>{{ camp.hours }} 课时</span>
            <span class="stat"><el-icon><User /></el-icon>{{ camp.students }} 人学习</span>
            <span class="stat"><el-icon><Star /></el-icon>{{ camp.difficulty }}</span>
          </div>
        </div>
        <div class="poster-action">
          <el-button type="primary" size="large" @click="startLearning">
            <el-icon><VideoPlay /></el-icon> 开始学习
          </el-button>
        </div>
      </div>
    </div>

    <div class="detail-body">
      <el-row :gutter="24">
        <el-col :span="16">
          <el-card class="detail-card" shadow="never">
            <template #header>
              <div class="card-header">
                <el-icon><InfoFilled /></el-icon>
                <span>训练营简介</span>
              </div>
            </template>
            <p class="description">{{ camp.description }}</p>
            <div class="info-list">
              <div class="info-item">
                <span class="info-label">适合对象</span>
                <span class="info-value">{{ camp.target }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">课程难度</span>
                <span class="info-value">{{ camp.difficulty }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">总课时</span>
                <span class="info-value">{{ camp.hours }} 课时</span>
              </div>
            </div>
          </el-card>

          <el-card class="detail-card" shadow="never">
            <template #header>
              <div class="card-header">
                <el-icon><Notebook /></el-icon>
                <span>课程大纲</span>
              </div>
            </template>
            <div class="chapter-list">
              <div v-for="(chapter, idx) in camp.chapters" :key="idx" class="chapter-item">
                <div class="chapter-header" @click="toggleChapter(idx)">
                  <div class="chapter-left">
                    <el-icon class="chapter-arrow" :class="{ expanded: expandedChapter === idx }"><ArrowRight /></el-icon>
                    <span class="chapter-index">{{ String(idx + 1).padStart(2, '0') }}</span>
                    <span class="chapter-name">{{ chapter.name }}</span>
                  </div>
                  <span class="chapter-duration">{{ chapter.duration }} 分钟</span>
                </div>
                <transition name="chapter-expand">
                  <div v-show="expandedChapter === idx" class="chapter-lessons">
                    <div v-for="(lesson, lIdx) in chapter.lessons" :key="lIdx" class="lesson-item">
                      <el-icon class="lesson-icon"><VideoPlay /></el-icon>
                      <span class="lesson-name">{{ lesson.name }}</span>
                      <span class="lesson-time">{{ lesson.time }}分钟</span>
                      <el-button type="primary" link size="small" @click="playLesson(lesson)">播放</el-button>
                    </div>
                  </div>
                </transition>
              </div>
            </div>
          </el-card>

          <el-card class="detail-card" shadow="never">
            <template #header>
              <div class="card-header">
                <el-icon><Calendar /></el-icon>
                <span>学习安排</span>
              </div>
            </template>
            <el-timeline>
              <el-timeline-item
                v-for="(item, index) in camp.schedule"
                :key="index"
                :type="item.type"
              >
                <h4>{{ item.title }}</h4>
                <p class="timeline-time">{{ item.time }}</p>
                <p v-if="item.desc" class="timeline-desc">{{ item.desc }}</p>
              </el-timeline-item>
            </el-timeline>
          </el-card>

          <el-card class="detail-card" shadow="never">
            <template #header>
              <div class="card-header">
                <el-icon><Trophy /></el-icon>
                <span>结业奖励</span>
              </div>
            </template>
            <div class="award-list">
              <div v-for="award in camp.awards" :key="award.level" class="award-item">
                <div class="award-badge" :class="`award-${award.level}`">{{ award.name }}</div>
                <div class="award-detail">
                  <p class="award-prize">{{ award.prize }}</p>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>

        <el-col :span="8">
          <el-card class="sidebar-card" shadow="never">
            <template #header>
              <span>讲师团队</span>
            </template>
            <div class="teacher-list">
              <div v-for="(teacher, tIdx) in camp.teachers" :key="tIdx" class="teacher-card">
                <el-avatar :size="48" :style="{ background: teacher.color }">{{ teacher.name[0] }}</el-avatar>
                <div class="teacher-info">
                  <h4 class="teacher-name">{{ teacher.name }}</h4>
                  <p class="teacher-title">{{ teacher.title }}</p>
                </div>
              </div>
            </div>
          </el-card>

          <el-card class="sidebar-card" shadow="never">
            <template #header>
              <span>训练营信息</span>
            </template>
            <div class="sidebar-info">
              <div class="sidebar-item">
                <span class="sidebar-label">课程类型</span>
                <span class="sidebar-value">训练营</span>
              </div>
              <div class="sidebar-item">
                <span class="sidebar-label">难度等级</span>
                <span class="sidebar-value">{{ camp.difficulty }}</span>
              </div>
              <div class="sidebar-item">
                <span class="sidebar-label">总课时</span>
                <span class="sidebar-value">{{ camp.hours }} 课时</span>
              </div>
              <div class="sidebar-item">
                <span class="sidebar-label">学习人数</span>
                <span class="sidebar-value">{{ camp.students }} 人</span>
              </div>
              <div class="sidebar-item">
                <span class="sidebar-label">适合对象</span>
                <span class="sidebar-value">{{ camp.target }}</span>
              </div>
            </div>
          </el-card>

          <el-card class="sidebar-card action-card" shadow="never">
            <el-button type="primary" size="large" class="register-btn" @click="startLearning">
              <el-icon><VideoPlay /></el-icon> 开始学习
            </el-button>
            <p class="register-tip">{{ camp.difficulty }} · {{ camp.hours }}课时 · {{ camp.students }}人已学</p>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Clock, User, Star, ArrowRight, VideoPlay, InfoFilled, Calendar, Trophy, Notebook } from '@element-plus/icons-vue'

import coverChuangxin from '@/assets/images/training-camps/创新创业基础训练营.png'
import coverShangye from '@/assets/images/training-camps/商业计划书写作训练营.png'
import coverLuyan from '@/assets/images/training-camps/路演表达训练营.png'
import coverAI from '@/assets/images/training-camps/AI项目孵化训练营.png'

const campCoverMap = {
  '创新创业基础训练营': coverChuangxin,
  '商业计划书写作训练营': coverShangye,
  '路演表达训练营': coverLuyan,
  'AI 项目孵化训练营': coverAI
}

const route = useRoute()
const expandedChapter = ref(0)

const camp = ref({
  id: 0,
  title: '',
  cover: null,
  description: '',
  hours: 0,
  students: 0,
  difficulty: '',
  tags: [],
  target: '',
  icon: 'Opportunity',
  gradient: 'linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%)',
  teachers: [],
  chapters: [],
  schedule: [],
  awards: []
})

const allCamps = [
  {
    id: 1,
    title: '创新创业基础训练营',
    cover: campCoverMap['创新创业基础训练营'],
    description: '从零开始学习创新创业基础知识，掌握创业思维和方法论，了解创业全流程。本训练营通过系统化的课程设计，帮助学员建立完整的创业认知框架，从创意产生到商业模式验证，从团队组建到融资路演，全面覆盖创业核心环节。',
    hours: 24,
    students: 1256,
    difficulty: '入门',
    tags: ['创业基础', '商业模式', '市场调研'],
    target: '零基础学生',
    icon: 'Opportunity',
    gradient: 'linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%)',
    teachers: [
      { name: '张教授', title: '创新创业学院院长 / 博士生导师', color: '#0ea5e9' },
      { name: '李副教授', title: '创业管理系主任 / 创业导师', color: '#06b6d4' }
    ],
    chapters: [
      { name: '第一章 创新思维与创业意识', duration: 120, lessons: [{ name: '什么是创新创业？', time: 20 }, { name: '创新思维的培养方法', time: 25 }, { name: '识别商业机会的技巧', time: 25 }, { name: '创业者必备素质', time: 25 }, { name: '本章小结与思考题', time: 25 }] },
      { name: '第二章 商业模式设计', duration: 150, lessons: [{ name: '商业模式画布详解', time: 30 }, { name: '价值主张设计', time: 30 }, { name: '客户细分与渠道策略', time: 30 }, { name: '收入来源与成本结构', time: 30 }, { name: '实战：设计你的商业模式', time: 30 }] },
      { name: '第三章 市场调研与用户分析', duration: 130, lessons: [{ name: '市场调研方法论', time: 25 }, { name: '用户画像构建技巧', time: 25 }, { name: '竞品分析方法', time: 30 }, { name: '数据收集与分析工具', time: 25 }, { name: '案例：成功产品的市场洞察', time: 25 }] },
      { name: '第四章 创业团队组建与管理', duration: 140, lessons: [{ name: '理想团队成员画像', time: 25 }, { name: '股权分配与激励机制', time: 30 }, { name: '高效协作的方法与工具', time: 28 }, { name: '冲突管理与沟通技巧', time: 27 }, { name: '从0到1组建你的创始团队', time: 30 }] }
    ],
    schedule: [
      { title: '开营仪式', time: '第1天', type: 'primary', desc: '线上开营，介绍训练营目标、学习路径和考核方式' },
      { title: '理论学习阶段', time: '第1-2周', type: '', desc: '完成创新思维、商业模式、市场调研、团队管理四大模块学习' },
      { title: '实战演练阶段', time: '第3周', type: '', desc: '分组完成商业模式设计和市场调研实战项目' },
      { title: '导师辅导', time: '第4周', type: 'warning', desc: '导师一对一辅导，优化项目方案，准备路演' },
      { title: '结营路演', time: '第5周', type: 'danger', desc: '各小组进行项目路演，评委打分评选优秀项目' },
      { title: '结业颁奖', time: '第6周', type: 'success', desc: '公布成绩，颁发结业证书和优秀学员奖励' }
    ],
    awards: [
      { level: 'first', name: '优秀学员', prize: '荣誉证书 + 推荐参加省级创新创业大赛 + 创业孵化入驻资格' },
      { level: 'second', name: '最佳项目', prize: '荣誉证书 + 导师持续指导3个月 + 创业资源对接' },
      { level: 'excellent', name: '结业证书', prize: '完成全部课程学习和考核后颁发训练营结业证书' }
    ]
  },
  {
    id: 2,
    title: '商业计划书写作训练营',
    cover: campCoverMap['商业计划书写作训练营'],
    description: '系统学习商业计划书的撰写方法，包括市场分析、财务预测、团队介绍等核心模块。通过大量真实案例拆解和实战写作练习，帮助你写出专业级商业计划书，打动投资人和评委。',
    hours: 18,
    students: 987,
    difficulty: '中级',
    tags: ['商业计划书', '财务分析', '市场预测'],
    target: '有创业想法的学生',
    icon: 'EditPen',
    gradient: 'linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%)',
    teachers: [
      { name: '王教授', title: '商学院副院长 / 资深投资人顾问', color: '#8b5cf6' },
      { name: '刘导师', title: '连续创业者 / 天使投资人', color: '#ec4899' }
    ],
    chapters: [
      { name: '第一章 商业计划书概述', duration: 90, lessons: [{ name: '为什么需要商业计划书？', time: 18 }, { name: '优秀BP的核心要素', time: 18 }, { name: '投资人关注什么？', time: 18 }, { name: '常见错误与避坑指南', time: 18 }, { name: '模板解析与结构设计', time: 18 }] },
      { name: '第二章 核心模块撰写技巧', duration: 180, lessons: [{ name: '执行摘要：一页纸打动投资人', time: 30 }, { name: '市场分析与行业研究', time: 35 }, { name: '产品/服务描述与竞争优势', time: 30 }, { name: '财务模型与盈利预测', time: 35 }, { name: '团队介绍与融资需求', time: 30 }, { name: '实战：完成你的BP初稿', time: 20 }] },
      { name: '第三章 BP优化与路演准备', duration: 110, lessons: [{ name: '视觉设计与排版美学', time: 22 }, { name: '数据可视化呈现技巧', time: 22 }, { name: '从文字到PPT的转化', time: 22 }, { name: '模拟答辩与反馈改进', time: 22 }, { name: '最终打磨与提交指南', time: 22 }] }
    ],
    schedule: [
      { title: '开营仪式', time: '第1天', type: 'primary', desc: '了解BP写作训练营学习路径，领取BP模板和参考资料' },
      { title: '理论学习', time: '第1-2周', type: '', desc: '系统学习BP各模块撰写方法和投资人视角' },
      { title: '实战写作', time: '第3周', type: '', desc: '完成个人商业计划书初稿，导师在线答疑' },
      { title: '互评优化', time: '第4周', type: 'warning', desc: '学员互评BP，导师逐一点评修改建议' },
      { title: '模拟路演', time: '第5周', type: 'danger', desc: '模拟投资人路演，5分钟Pitch + 3分钟答辩' },
      { title: '结业', time: '第6周', type: 'success', desc: '提交最终版BP，评选优秀商业计划书' }
    ],
    awards: [
      { level: 'first', name: '最佳商业计划书', prize: '荣誉证书 + 投资人对接机会 + 创业孵化绿色通道' },
      { level: 'second', name: '优秀学员', prize: '荣誉证书 + BP优化指导 + 创业导师1对1辅导' },
      { level: 'excellent', name: '结业证书', prize: '完成全部课程和BP提交后颁发结业证书' }
    ]
  },
  {
    id: 3,
    title: '路演表达训练营',
    cover: campCoverMap['路演表达训练营'],
    description: '提升路演演讲能力，学习PPT制作技巧，掌握答辩应对策略，让你的项目脱颖而出。本训练营注重实战演练，每位学员都将获得多次上台路演和导师点评的机会。',
    hours: 12,
    students: 1567,
    difficulty: '中级',
    tags: ['演讲技巧', 'PPT制作', '答辩技巧'],
    target: '准备参赛的学生',
    icon: 'Mic',
    gradient: 'linear-gradient(135deg, #f59e0b 0%, #ef4444 100%)',
    teachers: [
      { name: '赵讲师', title: '演讲与口才教练 / 多次国赛评委', color: '#f59e0b' },
      { name: '陈教练', title: '表达力训练专家 / TEDx演讲者', color: '#ef4444' }
    ],
    chapters: [
      { name: '第一章 路演演讲基础', duration: 80, lessons: [{ name: '路演演讲的特点与要求', time: 16 }, { name: '开场白的黄金法则', time: 16 }, { name: '故事化表达的魔力', time: 16 }, { name: '肢体语言与舞台表现', time: 16 }, { name: '声音控制与节奏把握', time: 16 }] },
      { name: '第二章 PPT制作与视觉呈现', duration: 100, lessons: [{ name: '路演PPT的设计原则', time: 20 }, { name: '每页PPT的信息架构', time: 20 }, { name: '图表与数据的艺术表达', time: 20 }, { name: '动画效果的正确使用', time: 20 }, { name: '实战：打造你的路演PPT', time: 20 }] },
      { name: '第三章 答辩技巧与临场应变', duration: 90, lessons: [{ name: '评委常见问题预判', time: 18 }, { name: '回答问题的STAR法则', time: 18 }, { name: '如何优雅地处理刁钻问题', time: 18 }, { name: '时间控制与重点突出', time: 18 }, { name: '全真模拟答辩演练', time: 18 }] }
    ],
    schedule: [
      { title: '开营仪式', time: '第1天', type: 'primary', desc: '破冰活动，了解路演核心要素，分组配对' },
      { title: '演讲基础训练', time: '第1-2周', type: '', desc: '学习演讲技巧、PPT制作和视觉呈现方法' },
      { title: '答辩技巧训练', time: '第3周', type: '', desc: '掌握答辩策略和临场应变技巧' },
      { title: '模拟路演', time: '第4周', type: 'warning', desc: '每人进行3分钟路演，导师现场点评指导' },
      { title: '强化训练', time: '第5周', type: 'danger', desc: '针对薄弱环节强化训练，反复打磨路演表现' },
      { title: '结营展演', time: '第6周', type: 'success', desc: '正式路演展演，评选最佳演讲者' }
    ],
    awards: [
      { level: 'first', name: '最佳演讲者', prize: '荣誉证书 + 竞赛路演推荐名额 + 演讲培训奖学金' },
      { level: 'second', name: '最佳PPT奖', prize: '荣誉证书 + 设计工具会员 + PPT模板资源包' },
      { level: 'excellent', name: '结业证书', prize: '完成全部课程和路演展演后颁发结业证书' }
    ]
  },
  {
    id: 4,
    title: 'AI 项目孵化训练营',
    cover: campCoverMap['AI 项目孵化训练营'],
    description: '学习如何将AI技术应用到实际项目中，包括大模型应用、智能体开发、AI产品设计等。本训练营由AI实验室专家和行业导师联合授课，从技术到产品到商业，全方位赋能AI创新创业。',
    hours: 32,
    students: 2341,
    difficulty: '高级',
    tags: ['人工智能', '大模型', '智能体'],
    target: '有技术基础的学生',
    icon: 'Cpu',
    gradient: 'linear-gradient(135deg, #10b981 0%, #14b8a6 100%)',
    teachers: [
      { name: '周博士', title: 'AI实验室负责人 / 大模型专家', color: '#10b981' },
      { name: '吴工程师', title: 'AI产品总监 / 前大厂AI架构师', color: '#14b8a6' }
    ],
    chapters: [
      { name: '第一章 AI 技术全景概览', duration: 120, lessons: [{ name: 'AI发展史与技术图谱', time: 24 }, { name: '大语言模型原理入门', time: 24 }, { name: 'AI Agent（智能体）概念', time: 24 }, { name: '主流AI平台与API对比', time: 24 }, { name: 'AI伦理与合规要点', time: 24 }] },
      { name: '第二章 大模型应用开发实战', duration: 200, lessons: [{ name: 'Prompt Engineering 高级技巧', time: 33 }, { name: 'RAG检索增强生成实践', time: 34 }, { name: 'Function Calling 与工具调用', time: 33 }, { name: '多模态模型应用（图文音）', time: 33 }, { name: 'SSE流式输出实现方案', time: 33 }, { name: '实战：搭建你的AI对话系统', time: 34 }] },
      { name: '第三章 AI 产品设计与落地', duration: 160, lessons: [{ name: 'AI产品思维与方法论', time: 27 }, { name: '用户体验在AI产品中的挑战', time: 27 }, { name: '成本控制与性能优化', time: 27 }, { name: 'AI项目的商业化路径', time: 26 }, { name: '案例拆解：成功的AI创业项目', time: 27 }, { name: '结业项目：AI+创新创业方案设计', time: 26 }] }
    ],
    schedule: [
      { title: '开营仪式', time: '第1天', type: 'primary', desc: '了解AI项目孵化全流程，领取开发环境和API资源' },
      { title: '技术学习阶段', time: '第1-3周', type: '', desc: '系统学习AI技术栈，完成大模型应用开发实战' },
      { title: '产品设计阶段', time: '第4周', type: '', desc: '学习AI产品设计方法论，设计你的AI+创新项目方案' },
      { title: '项目开发', time: '第5-6周', type: 'warning', desc: '在导师指导下完成AI项目原型开发和测试' },
      { title: '项目路演', time: '第7周', type: 'danger', desc: '项目Demo展示和技术答辩，投资人/企业评委参与' },
      { title: '孵化对接', time: '第8周', type: 'success', desc: '优秀项目获得孵化入驻资格和持续技术支持' }
    ],
    awards: [
      { level: 'first', name: '最佳AI创新项目', prize: '荣誉证书 + AI云服务资源包（价值¥10,000）+ 孵化器入驻资格' },
      { level: 'second', name: '技术突破奖', prize: '荣誉证书 + GPU算力资源 + 大厂实习推荐' },
      { level: 'excellent', name: '结业证书', prize: '完成全部课程和项目开发后颁发结业证书' }
    ]
  }
]

const handleCoverError = () => {
  camp.value.cover = null
}

const toggleChapter = (idx) => {
  expandedChapter.value = expandedChapter.value === idx ? -1 : idx
}

const playLesson = (lesson) => {
  ElMessage.info(`正在加载课程：${lesson.name}...`)
}

const startLearning = () => {
  ElMessage.success(`开始学习「${camp.value.title}」，祝你学有所成！`)
}

onMounted(() => {
  const campId = parseInt(route.params.id)
  const found = allCamps.find(c => c.id === campId)
  if (found) {
    camp.value = found
  }
})
</script>

<style scoped>
.camp-detail {
  min-height: 100vh;
  background-color: #f8fafc;
}

.detail-poster {
  position: relative;
  width: 100%;
  background: linear-gradient(135deg, #0c4a6e 0%, #075985 50%, #0ea5e9 100%);
}

.detail-poster.has-image {
  background: #0f172a;
}

.poster-img {
  width: 100%;
  height: auto;
  object-fit: contain;
  display: block;
  aspect-ratio: 16 / 9;
}

.poster-fallback {
  width: 100%;
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px 40px;
}

.poster-fallback-content {
  text-align: center;
  color: #ffffff;
}

.poster-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 40px 40px 30px;
  background: linear-gradient(to top, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.5) 60%, transparent 100%);
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  flex-wrap: wrap;
  gap: 20px;
}

.poster-info {
  flex: 1;
  color: #ffffff;
}

.poster-tags {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.category-tag {
  background-color: rgba(255, 255, 255, 0.9);
  color: #1e293b;
  border: none;
}

.poster-title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 8px;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
  line-height: 1.3;
}

.poster-desc {
  font-size: 14px;
  color: #bae6fd;
  margin-bottom: 12px;
  line-height: 1.6;
  max-width: 600px;
}

.poster-stats {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
}

.stat {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #e0f2fe;
}

.poster-action {
  flex-shrink: 0;
}

.detail-body {
  padding: 24px 40px;
  max-width: 1400px;
  margin: 0 auto;
}

.detail-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.description {
  font-size: 14px;
  line-height: 1.8;
  color: #334155;
  margin-bottom: 20px;
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-item {
  display: flex;
  gap: 12px;
}

.info-label {
  font-weight: 600;
  color: #1e293b;
  min-width: 80px;
  flex-shrink: 0;
}

.info-value {
  color: #475569;
  line-height: 1.6;
}

.chapter-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.chapter-item {
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  overflow: hidden;
  transition: all 0.2s ease;
}

.chapter-item:hover {
  border-color: #bae6fd;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.chapter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 18px;
  cursor: pointer;
  user-select: none;
  transition: background 0.2s;
}

.chapter-header:hover {
  background-color: #f8fafc;
}

.chapter-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.chapter-arrow {
  transition: transform 0.3s ease;
  color: #94a3b8;
  font-size: 14px;
}

.chapter-arrow.expanded {
  transform: rotate(90deg);
  color: #0ea5e9;
}

.chapter-index {
  font-size: 13px;
  font-weight: 700;
  color: #0ea5e9;
  min-width: 24px;
}

.chapter-name {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}

.chapter-duration {
  font-size: 12px;
  color: #94a3b8;
  white-space: nowrap;
}

.chapter-lessons {
  padding: 0 18px 12px 52px;
}

.lesson-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 13px;
  transition: background 0.2s;
}

.lesson-item:hover {
  background-color: #f1f5f9;
}

.lesson-icon {
  color: #0ea5e9;
  font-size: 14px;
  flex-shrink: 0;
}

.lesson-name {
  flex: 1;
  color: #475569;
}

.lesson-time {
  color: #94a3b8;
  font-size: 12px;
}

.award-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.award-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 16px;
  background: #f8fafc;
  border-radius: 12px;
}

.award-badge {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  color: #ffffff;
  min-width: 100px;
  text-align: center;
  flex-shrink: 0;
}

.award-first { background: linear-gradient(135deg, #f59e0b, #fbbf24); }
.award-second { background: linear-gradient(135deg, #0ea5e9, #38bdf8); }
.award-excellent { background: linear-gradient(135deg, #10b981, #34d399); }

.award-prize {
  font-size: 14px;
  font-weight: 500;
  color: #1e293b;
}

.sidebar-card {
  margin-bottom: 20px;
}

.teacher-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.teacher-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: #f8fafc;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
}

.teacher-info {
  display: flex;
  flex-direction: column;
}

.teacher-name {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.teacher-title {
  font-size: 12px;
  color: #64748b;
  margin: 2px 0 0;
}

.sidebar-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.sidebar-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #f1f5f9;
}

.sidebar-item:last-child {
  border-bottom: none;
}

.sidebar-label {
  color: #64748b;
  font-size: 14px;
}

.sidebar-value {
  color: #1e293b;
  font-weight: 500;
  font-size: 14px;
}

.action-card {
  text-align: center;
}

.register-btn {
  width: 100%;
  margin-bottom: 12px;
}

.register-tip {
  font-size: 13px;
  color: #64748b;
}

.timeline-time {
  font-size: 13px;
  color: #0ea5e9;
  font-weight: 500;
}

.timeline-desc {
  font-size: 13px;
  color: #64748b;
  margin-top: 4px;
  line-height: 1.5;
}

.chapter-expand-enter-active,
.chapter-expand-leave-active {
  transition: all 0.3s ease;
  overflow: hidden;
}

.chapter-expand-enter-from,
.chapter-expand-leave-to {
  opacity: 0;
  max-height: 0;
}
</style>
