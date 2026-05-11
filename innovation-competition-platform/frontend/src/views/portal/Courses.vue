<template>
  <div class="courses-page">
    <!-- Banner -->
    <div class="portal-hero-banner portal-hero-banner--course">
      <div class="banner-decoration">
        <div class="deco-circle c1"></div>
        <div class="deco-circle c2"></div>
      </div>
      <div class="banner-content">
        <div class="banner-badge">
          <el-icon size="16"><Notebook /></el-icon>
          <span>在线课程</span>
        </div>
        <h1 class="banner-title">在线课程</h1>
        <p class="banner-subtitle">系统学习创新创业知识，提升综合能力</p>
      </div>
    </div>

    <!-- 课程列表 -->
    <div class="courses-section">
      <div class="courses-grid">
        <SparkPortalCard
          v-for="course in courses"
          :key="course.id"
          :gradient="course.gradient"
          :cover-image="course.cover || ''"
          :title="course.title"
          :description="'讲师：' + course.teacher"
          :tags="course.tags"
          :max-tags="2"
          :meta-items="[
            { icon: User, text: course.students + ' 人学习' },
            { icon: Clock, text: course.duration }
          ]"
          :primary-action-text="'查看课程'"
          :primary-action-icon="VideoPlay"
          :on-primary-click="() => openCourse(course)"
        />
      </div>
    </div>

    <!-- 课程详情弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      :title="currentCourse?.title || '课程详情'"
      width="720px"
      class="course-dialog"
      destroy-on-close
    >
      <template v-if="currentCourse">
        <!-- 课程头部信息 -->
        <div class="course-detail-header" :style="{ background: currentCourse.gradient }">
          <el-icon size="40" style="color:#fff;"><component :is="currentCourse.icon" /></el-icon>
          <div class="header-info">
            <h2>{{ currentCourse.title }}</h2>
            <p>讲师：{{ currentCourse.teacher }}</p>
          </div>
        </div>

        <!-- 课程简介 -->
        <div class="course-detail-body">
          <div class="detail-section">
            <h4><el-icon><InfoFilled /></el-icon> 课程简介</h4>
            <p>{{ currentCourse.description }}</p>
          </div>

          <el-divider content-position="left">课程目录</el-divider>

          <!-- 章节列表 -->
          <div class="chapter-list">
            <div v-for="(chapter, idx) in currentCourse.chapters" :key="idx" class="chapter-item">
              <div class="chapter-header" @click="toggleChapter(idx)">
                <div class="chapter-left">
                  <el-icon class="chapter-arrow" :class="{ expanded: expandedChapter === idx }"><ArrowRight /></el-icon>
                  <span class="chapter-index">{{ String(idx + 1).padStart(2, '0') }}</span>
                  <span class="chapter-name">{{ chapter.name }}</span>
                </div>
                <span class="chapter-lesson-count">{{ chapter.lessons.length }} 节课</span>
              </div>
              <transition name="chapter-expand">
                <div v-show="expandedChapter === idx" class="chapter-lessons">
                  <div v-for="(lesson, lIdx) in chapter.lessons" :key="lIdx" class="lesson-item">
                    <el-icon class="lesson-icon"><VideoPlay /></el-icon>
                    <span class="lesson-name">{{ lesson.name }}</span>
                    <span class="lesson-time">{{ lesson.time }}分钟</span>
                    <el-tag size="small" :type="lIdx === 0 ? 'success' : 'info'" effect="plain">
                      {{ lIdx === 0 ? '免费' : '会员' }}
                    </el-tag>
                  </div>
                </div>
              </transition>
            </div>
          </div>

          <!-- 学习数据 -->
          <div class="course-stats">
            <div class="stat-item">
              <el-icon><User /></el-icon>
              <span>{{ currentCourse.students }} 人学习</span>
            </div>
            <div class="stat-item">
              <el-icon><Star /></el-icon>
              <span>{{ currentCourse.rating }} 分</span>
            </div>
            <div class="stat-item">
              <el-icon><Clock /></el-icon>
              <span>{{ currentCourse.duration }}</span>
            </div>
          </div>
        </div>
      </template>

      <template #footer>
        <el-button @click="dialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="startCourse">
          <el-icon><VideoPlay /></el-icon> 开始学习
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { User, Clock, Opportunity, TrendCharts, PieChart, ChatDotRound, Collection, ArrowRight, VideoPlay, InfoFilled, Star, Notebook } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import SparkPortalCard from '@/components/portal/SparkPortalCard.vue'

// 导入课程封面图片
import coverChuangye from '@/assets/images/courses/创业基础.png'
import coverShichang from '@/assets/images/courses/市场调研方法.png'
import coverShangye from '@/assets/images/courses/商业模式设计.png'
import coverLuyan from '@/assets/images/courses/项目路演技巧.png'
import coverFalv from '@/assets/images/courses/创业法律与知识产权.png'

// 课程封面映射
const courseCoverMap = {
  '创业基础': coverChuangye,
  '市场调研方法': coverShichang,
  '商业模式设计': coverShangye,
  '项目路演技巧': coverLuyan,
  '创业法律与知识产权': coverFalv
}

const dialogVisible = ref(false)
const currentCourse = ref(null)
const expandedChapter = ref(0)

const courses = ref([
  {
    id: 1,
    title: '创业基础',
    cover: courseCoverMap['创业基础'],
    teacher: '张教授',
    students: 2341,
    duration: '12小时',
    rating: 4.8,
    tags: ['创业入门', '商业思维'],
    icon: 'Opportunity',
    gradient: 'linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%)',
    description: '本课程从零开始带你了解创新创业的基础概念，包括什么是创业、为什么需要创新思维、如何发现商业机会等核心内容。通过案例分析和实战练习，帮助学员建立系统的创业认知框架。',
    chapters: [
      {
        name: '第一章 创新与创业概论',
        lessons: [
          { name: '创业的定义与内涵', time: 25 },
          { name: '创新的类型与价值', time: 25 },
          { name: '创业精神与企业家素质', time: 25 },
          { name: '国内外创业环境分析', time: 25 }
        ]
      },
      {
        name: '第二章 创业机会识别',
        lessons: [
          { name: '机会来源与发现方法', time: 30 },
          { name: '市场痛点分析技巧', time: 30 },
          { name: '机会评估与筛选框架', time: 30 }
        ]
      },
      {
        name: '第三章 商业模式入门',
        lessons: [
          { name: '商业模式画布详解', time: 35 },
          { name: '经典商业模式案例分析', time: 35 }
        ]
      }
    ]
  },
  {
    id: 2,
    title: '市场调研方法',
    cover: courseCoverMap['市场调研方法'],
    teacher: '李副教授',
    students: 1876,
    duration: '8小时',
    rating: 4.7,
    tags: ['市场分析', '用户研究'],
    icon: 'TrendCharts',
    gradient: 'linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%)',
    description: '系统学习市场调研的方法论和实操技能，包括问卷设计、用户访谈、数据分析等核心方法。帮助创业者科学地了解市场需求，为产品决策提供数据支撑。',
    chapters: [
      {
        name: '第一章 调研方法论',
        lessons: [
          { name: '市场调研概述与流程', time: 20 },
          { name: '定性研究与定量研究', time: 25 },
          { name: '调研方案设计要点', time: 20 }
        ]
      },
      {
        name: '第二章 数据收集技术',
        lessons: [
          { name: '问卷设计与优化', time: 30 },
          { name: '深度访谈技巧', time: 30 },
          { name: '观察法与实验法', time: 25 }
        ]
      },
      {
        name: '第三章 数据分析与报告',
        lessons: [
          { name: '数据清洗与整理', time: 25 },
          { name: '统计分析方法入门', time: 30 },
          { name: '调研报告撰写规范', time: 20 }
        ]
      }
    ]
  },
  {
    id: 3,
    title: '商业模式设计',
    cover: courseCoverMap['商业模式设计'],
    teacher: '王教授',
    students: 1567,
    duration: '10小时',
    rating: 4.9,
    tags: ['商业模式', '价值主张'],
    icon: 'PieChart',
    gradient: 'linear-gradient(135deg, #10b981 0%, #14b8a6 100%)',
    description: '深入学习商业模式设计的核心框架和方法，掌握价值主张设计、收入模式构建、成本结构优化等关键技能。通过大量真实案例拆解，让你学会设计可持续的商业模式。',
    chapters: [
      {
        name: '第一章 商业模式核心要素',
        lessons: [
          { name: '价值主张：你为谁解决什么问题？', time: 28 },
          { name: '客户细分与渠道策略', time: 28 },
          { name: '客户关系管理', time: 24 }
        ]
      },
      {
        name: '第二章 收入与成本',
        lessons: [
          { name: '收入来源设计', time: 30 },
          { name: '成本结构分析', time: 28 },
          { name: '盈利模式创新', time: 32 }
        ]
      },
      {
        name: '第三章 商业模式创新实战',
        lessons: [
          { name: '平台型商业模式', time: 30 },
          { name: '订阅制与SaaS模式', time: 28 },
          { name: '生态系统战略', time: 30 }
        ]
      }
    ]
  },
  {
    id: 4,
    title: '项目路演技巧',
    cover: courseCoverMap['项目路演技巧'],
    teacher: '赵讲师',
    students: 2134,
    duration: '6小时',
    rating: 4.6,
    tags: ['演讲', '路演', '表达'],
    icon: 'ChatDotRound',
    gradient: 'linear-gradient(135deg, #f59e0b 0%, #ef4444 100%)',
    description: '专注于提升路演表达能力的实战课程，涵盖PPT制作、演讲技巧、答辩应对等核心内容。帮助你用最短的时间打动评委和投资人。',
    chapters: [
      {
        name: '第一章 路演演讲基础',
        lessons: [
          { name: '路演的核心原则', time: 22 },
          { name: '开场白的黄金法则', time: 22 },
          { name: '故事化表达的运用', time: 22 }
        ]
      },
      {
        name: '第二章 PPT制作与呈现',
        lessons: [
          { name: '路演PPT的设计美学', time: 28 },
          { name: '数据可视化的艺术', time: 26 },
          { name: '动画与节奏控制', time: 24 }
        ]
      },
      {
        name: '第三章 答辩与临场应变',
        lessons: [
          { name: '评委提问预判与准备', time: 24 },
          { name: '回答问题的逻辑框架', time: 24 },
          { name: '压力下的从容应对', time: 24 }
        ]
      }
    ]
  },
  {
    id: 5,
    title: '创业法律与知识产权',
    cover: courseCoverMap['创业法律与知识产权'],
    teacher: '陈律师',
    students: 1234,
    duration: '8小时',
    rating: 4.5,
    tags: ['法律', '知识产权', '合规'],
    icon: 'Collection',
    gradient: 'linear-gradient(135deg, #6366f1 0%, #818cf8 100%)',
    description: '创业者必备的法律基础知识课程，涵盖公司注册、股权架构、合同管理、知识产权保护等内容。帮你规避法律风险，让创业之路走得更稳。',
    chapters: [
      {
        name: '第一章 公司设立法律基础',
        lessons: [
          { name: '企业形式选择（个体/有限/股份）', time: 25 },
          { name: '公司注册流程与材料', time: 25 },
          { name: '股东权利与义务', time: 25 }
        ]
      },
      {
        name: '第二章 股权与治理',
        lessons: [
          { name: '股权分配的常见陷阱', time: 28 },
          { name: '期权池设计与管理', time: 27 },
          { name: '公司治理结构搭建', time: 25 }
        ]
      },
      {
        name: '第三章 知识产权保护',
        lessons: [
          { name: '专利申请策略与流程', time: 28 },
          { name: '商标注册与品牌保护', time: 26 },
          { name: '著作权与商业秘密', time: 26 }
        ]
      }
    ]
  }
])

function openCourse(course) {
  currentCourse.value = course
  expandedChapter.value = 0
  dialogVisible.value = true
}

function toggleChapter(idx) {
  expandedChapter.value = expandedChapter.value === idx ? -1 : idx
}

const router = useRouter()

function startCourse() {
  router.push(`/courses/${currentCourse.value.id}`)
}
</script>

<style scoped>
.courses-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #f0f9ff 0%, #ffffff 100%);
}

.portal-hero-banner {
  position: relative;
  overflow: hidden;
  min-height: 260px;
  padding: 56px 48px;
  border-radius: 0 0 36px 36px;
  color: #fff;
}

.portal-hero-banner::before,
.portal-hero-banner::after {
  content: '';
  position: absolute;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.08);
  pointer-events: none;
}

.portal-hero-banner::before {
  width: 280px;
  height: 280px;
  right: -60px;
  top: -40px;
  animation: bannerFloat 8s ease-in-out infinite;
}

.portal-hero-banner::after {
  width: 180px;
  height: 180px;
  left: -40px;
  bottom: -40px;
  animation: bannerFloat 10s ease-in-out infinite reverse;
}

@keyframes bannerFloat {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-12px) scale(1.05); }
}

.portal-hero-banner--course {
  background: linear-gradient(135deg, #047857 0%, #06b6d4 100%);
}

.banner-decoration { position: absolute; right: 48px; top: 0; width: 35%; height: 100%; z-index: 1; }

.deco-circle { position: absolute; border-radius: 50%; opacity: 0.12; }
.c1 { width: 220px; height: 220px; background: #34d399; right: -20px; top: -20px; animation: decoFloat 8s ease-in-out infinite; }
.c2 { width: 150px; height: 150px; background: #6ee7b7; right: 140px; bottom: -20px; animation: decoFloat 10s ease-in-out infinite reverse; }

@keyframes decoFloat {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-12px) scale(1.05); }
}

.banner-content {
  position: relative;
  z-index: 2;
  max-width: 720px;
}

.banner-badge {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 8px 18px; border-radius: 999px;
  background: rgba(255, 255, 255, 0.14);
  color: rgba(255, 255, 255, 0.92);
  margin-bottom: 24px;
  font-size: 13px;
  font-weight: 500;
}

.banner-title {
  font-size: 40px;
  font-weight: 800;
  color: #ffffff;
  margin: 0 0 18px;
  line-height: 1.2;
}

.banner-subtitle {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.82);
  max-width: 720px;
  line-height: 1.8;
}

.courses-section {
  padding: 40px;
  max-width: 1400px;
  margin: 0 auto;
}

.courses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

/* Dialog styles */
.course-detail-header {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 24px 28px;
  border-radius: 12px;
  margin-bottom: 20px;
  color: #fff;
}

.header-info h2 {
  font-size: 22px;
  font-weight: 700;
  margin: 0 0 6px;
}

.header-info p {
  font-size: 14px;
  opacity: 0.85;
  margin: 0;
}

.detail-section {
  margin-bottom: 16px;
}

.detail-section h4 {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 10px;
}

.detail-section p {
  font-size: 14px;
  line-height: 1.7;
  color: #475569;
  margin: 0;
}

.chapter-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
}

.chapter-item {
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  overflow: hidden;
  transition: all 0.2s ease;
}

.chapter-item:hover {
  border-color: var(--primary-300);
}

.chapter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 13px 18px;
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

.chapter-lesson-count {
  font-size: 12px;
  color: #94a3b8;
}

.chapter-lessons {
  padding: 0 18px 12px 52px;
}

.lesson-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 10px;
  border-radius: 6px;
  font-size: 13px;
  transition: background 0.2s;
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

.course-stats {
  display: flex;
  gap: 32px;
  padding: 16px 20px;
  background: #f8fafc;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #475569;
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
