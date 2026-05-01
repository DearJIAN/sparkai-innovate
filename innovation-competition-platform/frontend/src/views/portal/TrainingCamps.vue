<template>
  <div class="training-camps">
    <!-- Banner -->
    <div class="camps-banner">
      <div class="banner-content">
        <h1 class="banner-title">创新创业训练营</h1>
        <p class="banner-subtitle">系统化学习，专业化训练，助力项目快速成长</p>
      </div>
    </div>

    <!-- 训练营列表 -->
    <div class="camps-section">
      <div class="camps-grid">
        <div
          v-for="camp in camps"
          :key="camp.id"
          class="camp-card"
        >
          <div class="camp-header" :style="camp.cover ? {} : { background: camp.gradient }">
            <img
              v-if="camp.cover"
              :src="camp.cover"
              :alt="camp.title"
              class="camp-cover-img"
              :style="{ aspectRatio: '16/9', objectFit: 'cover', width: '100%', display: 'block' }"
              @error="handleCoverError($event, camp)"
            />
            <template v-else>
              <div class="camp-icon">
                <el-icon size="40"><component :is="camp.icon" /></el-icon>
              </div>
              <h3 class="camp-title">{{ camp.title }}</h3>
            </template>
          </div>
          <div class="camp-body">
            <p class="camp-desc">{{ camp.description }}</p>
            <div class="camp-meta">
              <div class="meta-item">
                <el-icon><Clock /></el-icon>
                <span>{{ camp.hours }} 课时</span>
              </div>
              <div class="meta-item">
                <el-icon><User /></el-icon>
                <span>{{ camp.students }} 人学习</span>
              </div>
              <div class="meta-item">
                <el-icon><Star /></el-icon>
                <span>难度：{{ camp.difficulty }}</span>
              </div>
            </div>
            <div class="camp-tags">
              <el-tag
                v-for="tag in camp.tags"
                :key="tag"
                size="small"
                class="camp-tag"
              >
                {{ tag }}
              </el-tag>
            </div>
            <div class="camp-footer">
              <div class="camp-progress">
                <span class="progress-label">适合对象</span>
                <span class="progress-value">{{ camp.target }}</span>
              </div>
              <el-button type="primary" size="small" @click="openCamp(camp)">
                开始学习
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 学习内容弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      :title="currentCamp?.title || '训练营详情'"
      width="720px"
      class="camp-dialog"
      destroy-on-close
    >
      <template v-if="currentCamp">
        <!-- 训练营简介 -->
        <div class="dialog-intro">
          <p class="intro-text">{{ currentCamp.description }}</p>
          <div class="intro-stats">
            <span><el-icon><Clock /></el-icon> {{ currentCamp.hours }} 课时</span>
            <span><el-icon><User /></el-icon> {{ currentCamp.students }} 人已学</span>
            <span><el-icon><Star /></el-icon> {{ currentCamp.difficulty }}</span>
          </div>
        </div>

        <!-- 课程章节列表 -->
        <el-divider content-position="left">课程大纲</el-divider>
        <div class="chapter-list">
          <div v-for="(chapter, idx) in currentCamp.chapters" :key="idx" class="chapter-item">
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

        <!-- 讲师介绍 -->
        <el-divider content-position="left">讲师团队</el-divider>
        <div class="teacher-list">
          <div v-for="(teacher, tIdx) in currentCamp.teachers" :key="tIdx" class="teacher-card">
            <el-avatar :size="48" :style="{ background: teacher.color }">{{ teacher.name[0] }}</el-avatar>
            <div class="teacher-info">
              <h4 class="teacher-name">{{ teacher.name }}</h4>
              <p class="teacher-title">{{ teacher.title }}</p>
            </div>
          </div>
        </div>
      </template>

      <template #footer>
        <el-button @click="dialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="startLearning">
          <el-icon><VideoPlay /></el-icon> 立即开始学习
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Clock, User, Star, Opportunity, EditPen, Mic, Cpu, ArrowRight, VideoPlay } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

// 导入训练营封面图片
import coverChuangxin from '@/assets/images/training-camps/创新创业基础训练营.png'
import coverShangye from '@/assets/images/training-camps/商业计划书写作训练营.png'
import coverLuyan from '@/assets/images/training-camps/路演表达训练营.png'
import coverAI from '@/assets/images/training-camps/AI项目孵化训练营.png'

// 训练营封面映射
const campCoverMap = {
  '创新创业基础训练营': coverChuangxin,
  '商业计划书写作训练营': coverShangye,
  '路演表达训练营': coverLuyan,
  'AI 项目孵化训练营': coverAI
}

// 图片加载失败时回退到渐变色
function handleCoverError(event, camp) {
  camp.cover = null
}

const dialogVisible = ref(false)
const currentCamp = ref(null)
const expandedChapter = ref(0)

const camps = ref([
  {
    id: 1,
    title: '创新创业基础训练营',
    cover: campCoverMap['创新创业基础训练营'],
    description: '从零开始学习创新创业基础知识，掌握创业思维和方法论，了解创业全流程。',
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
      {
        name: '第一章 创新思维与创业意识',
        duration: 120,
        lessons: [
          { name: '什么是创新创业？', time: 20 },
          { name: '创新思维的培养方法', time: 25 },
          { name: '识别商业机会的技巧', time: 25 },
          { name: '创业者必备素质', time: 25 },
          { name: '本章小结与思考题', time: 25 }
        ]
      },
      {
        name: '第二章 商业模式设计',
        duration: 150,
        lessons: [
          { name: '商业模式画布详解', time: 30 },
          { name: '价值主张设计', time: 30 },
          { name: '客户细分与渠道策略', time: 30 },
          { name: '收入来源与成本结构', time: 30 },
          { name: '实战：设计你的商业模式', time: 30 }
        ]
      },
      {
        name: '第三章 市场调研与用户分析',
        duration: 130,
        lessons: [
          { name: '市场调研方法论', time: 25 },
          { name: '用户画像构建技巧', time: 25 },
          { name: '竞品分析方法', time: 30 },
          { name: '数据收集与分析工具', time: 25 },
          { name: '案例：成功产品的市场洞察', time: 25 }
        ]
      },
      {
        name: '第四章 创业团队组建与管理',
        duration: 140,
        lessons: [
          { name: '理想团队成员画像', time: 25 },
          { name: '股权分配与激励机制', time: 30 },
          { name: '高效协作的方法与工具', time: 28 },
          { name: '冲突管理与沟通技巧', time: 27 },
          { name: '从0到1组建你的创始团队', time: 30 }
        ]
      }
    ]
  },
  {
    id: 2,
    title: '商业计划书写作训练营',
    cover: campCoverMap['商业计划书写作训练营'],
    description: '系统学习商业计划书的撰写方法，包括市场分析、财务预测、团队介绍等核心模块。',
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
      {
        name: '第一章 商业计划书概述',
        duration: 90,
        lessons: [
          { name: '为什么需要商业计划书？', time: 18 },
          { name: '优秀BP的核心要素', time: 18 },
          { name: '投资人关注什么？', time: 18 },
          { name: '常见错误与避坑指南', time: 18 },
          { name: '模板解析与结构设计', time: 18 }
        ]
      },
      {
        name: '第二章 核心模块撰写技巧',
        duration: 180,
        lessons: [
          { name: '执行摘要：一页纸打动投资人', time: 30 },
          { name: '市场分析与行业研究', time: 35 },
          { name: '产品/服务描述与竞争优势', time: 30 },
          { name: '财务模型与盈利预测', time: 35 },
          { name: '团队介绍与融资需求', time: 30 },
          { name: '实战：完成你的BP初稿', time: 20 }
        ]
      },
      {
        name: '第三章 BP优化与路演准备',
        duration: 110,
        lessons: [
          { name: '视觉设计与排版美学', time: 22 },
          { name: '数据可视化呈现技巧', time: 22 },
          { name: '从文字到PPT的转化', time: 22 },
          { name: '模拟答辩与反馈改进', time: 22 },
          { name: '最终打磨与提交指南', time: 22 }
        ]
      }
    ]
  },
  {
    id: 3,
    title: '路演表达训练营',
    cover: campCoverMap['路演表达训练营'],
    description: '提升路演演讲能力，学习PPT制作技巧，掌握答辩应对策略，让你的项目脱颖而出。',
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
      {
        name: '第一章 路演演讲基础',
        duration: 80,
        lessons: [
          { name: '路演演讲的特点与要求', time: 16 },
          { name: '开场白的黄金法则', time: 16 },
          { name: '故事化表达的魔力', time: 16 },
          { name: '肢体语言与舞台表现', time: 16 },
          { name: '声音控制与节奏把握', time: 16 }
        ]
      },
      {
        name: '第二章 PPT制作与视觉呈现',
        duration: 100,
        lessons: [
          { name: '路演PPT的设计原则', time: 20 },
          { name: '每页PPT的信息架构', time: 20 },
          { name: '图表与数据的艺术表达', time: 20 },
          { name: '动画效果的正确使用', time: 20 },
          { name: '实战：打造你的路演PPT', time: 20 }
        ]
      },
      {
        name: '第三章 答辩技巧与临场应变',
        duration: 90,
        lessons: [
          { name: '评委常见问题预判', time: 18 },
          { name: '回答问题的STAR法则', time: 18 },
          { name: '如何优雅地处理刁钻问题', time: 18 },
          { name: '时间控制与重点突出', time: 18 },
          { name: '全真模拟答辩演练', time: 18 }
        ]
      }
    ]
  },
  {
    id: 4,
    title: 'AI 项目孵化训练营',
    cover: campCoverMap['AI 项目孵化训练营'],
    description: '学习如何将AI技术应用到实际项目中，包括大模型应用、智能体开发、AI产品设计等。',
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
      {
        name: '第一章 AI 技术全景概览',
        duration: 120,
        lessons: [
          { name: 'AI发展史与技术图谱', time: 24 },
          { name: '大语言模型原理入门', time: 24 },
          { name: 'AI Agent（智能体）概念', time: 24 },
          { name: '主流AI平台与API对比', time: 24 },
          { name: 'AI伦理与合规要点', time: 24 }
        ]
      },
      {
        name: '第二章 大模型应用开发实战',
        duration: 200,
        lessons: [
          { name: 'Prompt Engineering 高级技巧', time: 33 },
          { name: 'RAG检索增强生成实践', time: 34 },
          { name: 'Function Calling 与工具调用', time: 33 },
          { name: '多模态模型应用（图文音）', time: 33 },
          { name: 'SSE流式输出实现方案', time: 33 },
          { name: '实战：搭建你的AI对话系统', time: 34 }
        ]
      },
      {
        name: '第三章 AI 产品设计与落地',
        duration: 160,
        lessons: [
          { name: 'AI产品思维与方法论', time: 27 },
          { name: '用户体验在AI产品中的挑战', time: 27 },
          { name: '成本控制与性能优化', time: 27 },
          { name: 'AI项目的商业化路径', time: 26 },
          { name: '案例拆解：成功的AI创业项目', time: 27 },
          { name: '结业项目：AI+创新创业方案设计', time: 26 }
        ]
      }
    ]
  }
])

function openCamp(camp) {
  currentCamp.value = camp
  expandedChapter.value = 0
  dialogVisible.value = true
}

function toggleChapter(idx) {
  expandedChapter.value = expandedChapter.value === idx ? -1 : idx
}

function playLesson(lesson) {
  ElMessage.info(`正在加载课程：${lesson.name}...`)
}

const router = useRouter()

function startLearning() {
  router.push(`/training-camps/${currentCamp.value.id}`)
}
</script>

<style scoped>
.training-camps {
  min-height: 100vh;
  background: linear-gradient(180deg, #f0f9ff 0%, #ffffff 100%);
}

.camps-banner {
  background: linear-gradient(135deg, #312e81 0%, #4338ca 40%, #7c3aed 100%);
  padding: 50px 40px;
  border-radius: 0 0 40px 40px;
  position: relative;
  overflow: hidden;
}

.camps-banner::before {
  content: '';
  position: absolute;
  top: -40%;
  right: -15%;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(167,139,250,0.2) 0%, transparent 70%);
  border-radius: 50%;
  animation: campGlow 7s ease-in-out infinite;
}

.camps-banner::after {
  content: '';
  position: absolute;
  bottom: -40%;
  left: -15%;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(196,181,253,0.12) 0%, transparent 70%);
  border-radius: 50%;
  animation: campGlow 9s ease-in-out infinite reverse;
}

@keyframes campGlow {
  0%, 100% { transform: scale(1) translate(0, 0); opacity: 0.5; }
  33% { transform: scale(1.1) translate(20px, -10px); opacity: 0.8; }
  66% { transform: scale(1.05) translate(-10px, 15px); opacity: 1; }
}

.banner-content {
  max-width: 1400px;
  margin: 0 auto;
}

.banner-title {
  font-size: 32px;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 12px;
}

.banner-subtitle {
  font-size: 16px;
  color: #bae6fd;
}

.camps-section {
  padding: 40px;
  max-width: 1400px;
  margin: 0 auto;
}

.camps-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}

.camp-card {
  background: #ffffff;
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.camp-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 20px 40px -12px rgba(0, 0, 0, 0.15);
}

.camp-header {
  padding: 32px;
  text-align: center;
  color: #ffffff;
  position: relative;
  overflow: hidden;
}

.camp-cover-img {
  width: 100%;
  display: block;
  object-fit: cover;
  aspect-ratio: 16/9;
}

.camp-icon {
  margin-bottom: 12px;
}

.camp-title {
  font-size: 18px;
  font-weight: 600;
  color: #ffffff;
}

.camp-body {
  padding: 24px;
}

.camp-desc {
  font-size: 14px;
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 16px;
}

.camp-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 16px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #475569;
}

.camp-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.camp-tag {
  background-color: #f1f5f9;
  color: #475569;
  border: none;
}

.camp-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
}

.camp-progress {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.progress-label {
  font-size: 12px;
  color: #94a3b8;
}

.progress-value {
  font-size: 13px;
  color: #475569;
  font-weight: 500;
}

/* Dialog styles */
.dialog-intro {
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 16px;
}

.intro-text {
  font-size: 15px;
  line-height: 1.7;
  color: #334155;
  margin-bottom: 12px;
}

.intro-stats {
  display: flex;
  gap: 24px;
  font-size: 13px;
  color: #475569;
}

.intro-stats span {
  display: flex;
  align-items: center;
  gap: 4px;
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
  border-color: var(--primary-300);
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
  color: var(--primary-500);
}

.chapter-index {
  font-size: 13px;
  font-weight: 700;
  color: var(--primary-500);
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
  cursor: default;
}

.lesson-item:hover {
  background-color: #f1f5f9;
}

.lesson-icon {
  color: var(--primary-400);
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

.teacher-list {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
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

/* Transition */
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
