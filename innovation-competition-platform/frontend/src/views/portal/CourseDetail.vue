<template>
  <div class="course-detail">
    <div class="detail-poster" :class="{ 'has-image': course.cover }">
      <img
        v-if="course.cover"
        :src="course.cover"
        :alt="course.title"
        class="poster-img"
        @error="handleCoverError"
      />
      <div v-else class="poster-fallback" :style="{ background: course.gradient }">
        <div class="poster-fallback-content">
          <el-icon size="60" style="color:#fff;margin-bottom:16px;"><component :is="course.icon" /></el-icon>
          <h1 class="poster-title">{{ course.title }}</h1>
        </div>
      </div>
      <div class="poster-overlay">
        <div class="poster-info">
          <div class="poster-tags" v-if="course.cover">
            <el-tag size="large" class="category-tag">在线课程</el-tag>
            <el-tag type="warning" size="large">{{ course.rating }} 分</el-tag>
          </div>
          <h1 class="poster-title" v-if="course.cover">{{ course.title }}</h1>
          <p class="poster-desc">{{ course.description }}</p>
          <div class="poster-stats">
            <span class="stat"><el-icon><User /></el-icon>{{ course.students }} 人学习</span>
            <span class="stat"><el-icon><Clock /></el-icon>{{ course.duration }}</span>
            <span class="stat"><el-icon><Star /></el-icon>{{ course.rating }} 分</span>
          </div>
        </div>
        <div class="poster-action">
          <el-button type="primary" size="large" @click="startCourse">
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
                <span>课程简介</span>
              </div>
            </template>
            <p class="description">{{ course.description }}</p>
            <div class="info-list">
              <div class="info-item">
                <span class="info-label">授课讲师</span>
                <span class="info-value">{{ course.teacher }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">课程时长</span>
                <span class="info-value">{{ course.duration }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">课程评分</span>
                <span class="info-value">{{ course.rating }} / 5.0</span>
              </div>
            </div>
          </el-card>

          <el-card class="detail-card" shadow="never">
            <template #header>
              <div class="card-header">
                <el-icon><Notebook /></el-icon>
                <span>课程目录</span>
              </div>
            </template>
            <div class="chapter-list">
              <div v-for="(chapter, idx) in course.chapters" :key="idx" class="chapter-item">
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
                        {{ lIdx === 0 ? '免费试看' : '会员' }}
                      </el-tag>
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
                <span>学习计划</span>
              </div>
            </template>
            <el-timeline>
              <el-timeline-item
                v-for="(item, index) in course.schedule"
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
                <span>学习成果</span>
              </div>
            </template>
            <div class="award-list">
              <div v-for="award in course.awards" :key="award.level" class="award-item">
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
              <span>课程信息</span>
            </template>
            <div class="sidebar-info">
              <div class="sidebar-item">
                <span class="sidebar-label">课程类型</span>
                <span class="sidebar-value">在线课程</span>
              </div>
              <div class="sidebar-item">
                <span class="sidebar-label">授课讲师</span>
                <span class="sidebar-value">{{ course.teacher }}</span>
              </div>
              <div class="sidebar-item">
                <span class="sidebar-label">课程时长</span>
                <span class="sidebar-value">{{ course.duration }}</span>
              </div>
              <div class="sidebar-item">
                <span class="sidebar-label">学习人数</span>
                <span class="sidebar-value">{{ course.students }} 人</span>
              </div>
              <div class="sidebar-item">
                <span class="sidebar-label">课程评分</span>
                <span class="sidebar-value">{{ course.rating }} 分</span>
              </div>
              <div class="sidebar-item">
                <span class="sidebar-label">章节总数</span>
                <span class="sidebar-value">{{ course.chapters.length }} 章</span>
              </div>
            </div>
          </el-card>

          <el-card class="sidebar-card" shadow="never">
            <template #header>
              <span>课程标签</span>
            </template>
            <div class="tag-list">
              <el-tag
                v-for="tag in course.tags"
                :key="tag"
                class="course-tag"
              >
                {{ tag }}
              </el-tag>
            </div>
          </el-card>

          <el-card class="sidebar-card action-card" shadow="never">
            <el-button type="primary" size="large" class="register-btn" @click="startCourse">
              <el-icon><VideoPlay /></el-icon> 开始学习
            </el-button>
            <p class="register-tip">{{ course.teacher }} · {{ course.duration }} · {{ course.rating }}分</p>
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
import { User, Clock, Star, ArrowRight, VideoPlay, InfoFilled, Calendar, Trophy, Notebook } from '@element-plus/icons-vue'

import coverChuangye from '@/assets/images/courses/创业基础.png'
import coverShichang from '@/assets/images/courses/市场调研方法.png'
import coverShangye from '@/assets/images/courses/商业模式设计.png'
import coverLuyan from '@/assets/images/courses/项目路演技巧.png'
import coverFalv from '@/assets/images/courses/创业法律与知识产权.png'

const courseCoverMap = {
  '创业基础': coverChuangye,
  '市场调研方法': coverShichang,
  '商业模式设计': coverShangye,
  '项目路演技巧': coverLuyan,
  '创业法律与知识产权': coverFalv
}

const route = useRoute()
const expandedChapter = ref(0)

const course = ref({
  id: 0,
  title: '',
  cover: null,
  teacher: '',
  students: 0,
  duration: '',
  rating: 0,
  tags: [],
  icon: 'Opportunity',
  gradient: 'linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%)',
  description: '',
  chapters: [],
  schedule: [],
  awards: []
})

const allCourses = [
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
      { name: '第一章 创新与创业概论', lessons: [{ name: '创业的定义与内涵', time: 25 }, { name: '创新的类型与价值', time: 25 }, { name: '创业精神与企业家素质', time: 25 }, { name: '国内外创业环境分析', time: 25 }] },
      { name: '第二章 创业机会识别', lessons: [{ name: '机会来源与发现方法', time: 30 }, { name: '市场痛点分析技巧', time: 30 }, { name: '机会评估与筛选框架', time: 30 }] },
      { name: '第三章 商业模式入门', lessons: [{ name: '商业模式画布详解', time: 35 }, { name: '经典商业模式案例分析', time: 35 }] }
    ],
    schedule: [
      { title: '开始学习', time: '随时', type: 'primary', desc: '在线课程，可随时开始学习，自主安排进度' },
      { title: '第一章学习', time: '第1周', type: '', desc: '学习创新与创业概论，完成课后思考题' },
      { title: '第二章学习', time: '第2周', type: '', desc: '学习创业机会识别方法，完成案例分析作业' },
      { title: '第三章学习', time: '第3周', type: '', desc: '学习商业模式入门，完成商业模式画布练习' },
      { title: '期末考核', time: '第4周', type: 'warning', desc: '完成在线考试和创业计划书提交' },
      { title: '获得证书', time: '考核通过后', type: 'success', desc: '通过考核后获得课程结业证书' }
    ],
    awards: [
      { level: 'first', name: '优秀学员', prize: '课程结业证书（优秀） + 推荐参加创业实践项目' },
      { level: 'excellent', name: '结业证书', prize: '完成全部课程学习和考核后颁发课程结业证书' }
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
      { name: '第一章 调研方法论', lessons: [{ name: '市场调研概述与流程', time: 20 }, { name: '定性研究与定量研究', time: 25 }, { name: '调研方案设计要点', time: 20 }] },
      { name: '第二章 数据收集技术', lessons: [{ name: '问卷设计与优化', time: 30 }, { name: '深度访谈技巧', time: 30 }, { name: '观察法与实验法', time: 25 }] },
      { name: '第三章 数据分析与报告', lessons: [{ name: '数据清洗与整理', time: 25 }, { name: '统计分析方法入门', time: 30 }, { name: '调研报告撰写规范', time: 20 }] }
    ],
    schedule: [
      { title: '开始学习', time: '随时', type: 'primary', desc: '在线课程，可随时开始学习' },
      { title: '方法论学习', time: '第1周', type: '', desc: '学习调研方法论基础，理解定性与定量研究区别' },
      { title: '数据收集实战', time: '第2周', type: '', desc: '学习问卷设计和访谈技巧，完成调研方案设计' },
      { title: '数据分析', time: '第3周', type: '', desc: '学习数据分析和报告撰写方法' },
      { title: '期末考核', time: '第4周', type: 'warning', desc: '提交完整市场调研报告作为考核' },
      { title: '获得证书', time: '考核通过后', type: 'success', desc: '通过考核后获得课程结业证书' }
    ],
    awards: [
      { level: 'first', name: '优秀学员', prize: '课程结业证书（优秀） + 推荐参加市场调研实习' },
      { level: 'excellent', name: '结业证书', prize: '完成全部课程学习和考核后颁发课程结业证书' }
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
      { name: '第一章 商业模式核心要素', lessons: [{ name: '价值主张：你为谁解决什么问题？', time: 28 }, { name: '客户细分与渠道策略', time: 28 }, { name: '客户关系管理', time: 24 }] },
      { name: '第二章 收入与成本', lessons: [{ name: '收入来源设计', time: 30 }, { name: '成本结构分析', time: 28 }, { name: '盈利模式创新', time: 32 }] },
      { name: '第三章 商业模式创新实战', lessons: [{ name: '平台型商业模式', time: 30 }, { name: '订阅制与SaaS模式', time: 28 }, { name: '生态系统战略', time: 30 }] }
    ],
    schedule: [
      { title: '开始学习', time: '随时', type: 'primary', desc: '在线课程，可随时开始学习' },
      { title: '核心要素学习', time: '第1-2周', type: '', desc: '学习商业模式核心要素和价值主张设计' },
      { title: '收入成本分析', time: '第3周', type: '', desc: '学习收入来源设计和成本结构分析方法' },
      { title: '创新实战', time: '第4周', type: '', desc: '学习商业模式创新方法，完成商业模式设计方案' },
      { title: '期末考核', time: '第5周', type: 'warning', desc: '提交商业模式设计方案作为考核' },
      { title: '获得证书', time: '考核通过后', type: 'success', desc: '通过考核后获得课程结业证书' }
    ],
    awards: [
      { level: 'first', name: '优秀学员', prize: '课程结业证书（优秀） + 商业模式咨询实践机会' },
      { level: 'excellent', name: '结业证书', prize: '完成全部课程学习和考核后颁发课程结业证书' }
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
      { name: '第一章 路演演讲基础', lessons: [{ name: '路演的核心原则', time: 22 }, { name: '开场白的黄金法则', time: 22 }, { name: '故事化表达的运用', time: 22 }] },
      { name: '第二章 PPT制作与呈现', lessons: [{ name: '路演PPT的设计美学', time: 28 }, { name: '数据可视化的艺术', time: 26 }, { name: '动画与节奏控制', time: 24 }] },
      { name: '第三章 答辩与临场应变', lessons: [{ name: '评委提问预判与准备', time: 24 }, { name: '回答问题的逻辑框架', time: 24 }, { name: '压力下的从容应对', time: 24 }] }
    ],
    schedule: [
      { title: '开始学习', time: '随时', type: 'primary', desc: '在线课程，可随时开始学习' },
      { title: '演讲基础', time: '第1周', type: '', desc: '学习路演演讲基础技巧和故事化表达方法' },
      { title: 'PPT制作', time: '第2周', type: '', desc: '学习路演PPT设计美学和数据可视化技巧' },
      { title: '答辩训练', time: '第3周', type: '', desc: '学习答辩策略和临场应变技巧' },
      { title: '期末考核', time: '第4周', type: 'warning', desc: '提交路演视频作为考核' },
      { title: '获得证书', time: '考核通过后', type: 'success', desc: '通过考核后获得课程结业证书' }
    ],
    awards: [
      { level: 'first', name: '优秀学员', prize: '课程结业证书（优秀） + 竞赛路演指导机会' },
      { level: 'excellent', name: '结业证书', prize: '完成全部课程学习和考核后颁发课程结业证书' }
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
      { name: '第一章 公司设立法律基础', lessons: [{ name: '企业形式选择（个体/有限/股份）', time: 25 }, { name: '公司注册流程与材料', time: 25 }, { name: '股东权利与义务', time: 25 }] },
      { name: '第二章 股权与治理', lessons: [{ name: '股权分配的常见陷阱', time: 28 }, { name: '期权池设计与管理', time: 27 }, { name: '公司治理结构搭建', time: 25 }] },
      { name: '第三章 知识产权保护', lessons: [{ name: '专利申请策略与流程', time: 28 }, { name: '商标注册与品牌保护', time: 26 }, { name: '著作权与商业秘密', time: 26 }] }
    ],
    schedule: [
      { title: '开始学习', time: '随时', type: 'primary', desc: '在线课程，可随时开始学习' },
      { title: '公司设立', time: '第1-2周', type: '', desc: '学习公司设立的法律基础和注册流程' },
      { title: '股权治理', time: '第3周', type: '', desc: '学习股权分配和公司治理结构设计' },
      { title: '知识产权', time: '第4周', type: '', desc: '学习专利、商标、著作权等知识产权保护方法' },
      { title: '期末考核', time: '第5周', type: 'warning', desc: '完成在线考试和案例分析报告' },
      { title: '获得证书', time: '考核通过后', type: 'success', desc: '通过考核后获得课程结业证书' }
    ],
    awards: [
      { level: 'first', name: '优秀学员', prize: '课程结业证书（优秀） + 免费法律咨询1次' },
      { level: 'excellent', name: '结业证书', prize: '完成全部课程学习和考核后颁发课程结业证书' }
    ]
  }
]

const handleCoverError = () => {
  course.value.cover = null
}

const toggleChapter = (idx) => {
  expandedChapter.value = expandedChapter.value === idx ? -1 : idx
}

const startCourse = () => {
  ElMessage.success(`开始学习「${course.value.title}」，祝你学有所成！`)
}

onMounted(() => {
  const courseId = parseInt(route.params.id)
  const found = allCourses.find(c => c.id === courseId)
  if (found) {
    course.value = found
  }
})
</script>

<style scoped>
.course-detail {
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
.award-excellent { background: linear-gradient(135deg, #10b981, #34d399); }

.award-prize {
  font-size: 14px;
  font-weight: 500;
  color: #1e293b;
}

.sidebar-card {
  margin-bottom: 20px;
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

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.course-tag {
  background-color: #f1f5f9;
  color: #475569;
  border: none;
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
