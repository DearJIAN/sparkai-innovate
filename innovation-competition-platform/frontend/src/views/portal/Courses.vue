<template>
  <div class="courses-page">
    <!-- Banner -->
    <div class="courses-banner">
      <div class="banner-content">
        <h1 class="banner-title">在线课程</h1>
        <p class="banner-subtitle">系统学习创新创业知识，提升综合能力</p>
      </div>
    </div>

    <!-- 课程列表 -->
    <div class="courses-section">
      <div class="courses-grid">
        <div
          v-for="course in courses"
          :key="course.id"
          class="course-card"
        >
          <div class="course-cover" :style="{ background: course.gradient }">
            <div class="cover-content">
              <el-icon size="48"><component :is="course.icon" /></el-icon>
              <span class="cover-title">{{ course.title }}</span>
            </div>
          </div>
          <div class="course-body">
            <h3 class="course-title">{{ course.title }}</h3>
            <p class="course-teacher">讲师：{{ course.teacher }}</p>
            <div class="course-meta">
              <span class="meta-item">
                <el-icon><User /></el-icon>
                {{ course.students }} 人学习
              </span>
              <span class="meta-item">
                <el-icon><Clock /></el-icon>
                {{ course.duration }}
              </span>
            </div>
            <div class="course-tags">
              <el-tag
                v-for="tag in course.tags"
                :key="tag"
                size="small"
                class="course-tag"
              >
                {{ tag }}
              </el-tag>
            </div>
            <div class="course-footer">
              <el-button type="primary" size="small">
                查看课程
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { User, Clock, Opportunity, TrendCharts, PieChart, ChatDotRound, Collection } from '@element-plus/icons-vue'

const courses = ref([
  {
    id: 1,
    title: '创业基础',
    teacher: '张教授',
    students: 2341,
    duration: '12小时',
    tags: ['创业入门', '商业思维'],
    icon: 'Opportunity',
    gradient: 'linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%)'
  },
  {
    id: 2,
    title: '市场调研方法',
    teacher: '李副教授',
    students: 1876,
    duration: '8小时',
    tags: ['市场分析', '用户研究'],
    icon: 'TrendCharts',
    gradient: 'linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%)'
  },
  {
    id: 3,
    title: '商业模式设计',
    teacher: '王教授',
    students: 1567,
    duration: '10小时',
    tags: ['商业模式', '价值主张'],
    icon: 'PieChart',
    gradient: 'linear-gradient(135deg, #10b981 0%, #14b8a6 100%)'
  },
  {
    id: 4,
    title: '项目路演技巧',
    teacher: '赵讲师',
    students: 2134,
    duration: '6小时',
    tags: ['演讲', '路演', '表达'],
    icon: 'ChatDotRound',
    gradient: 'linear-gradient(135deg, #f59e0b 0%, #ef4444 100%)'
  },
  {
    id: 5,
    title: '创业法律与知识产权',
    teacher: '陈律师',
    students: 1234,
    duration: '8小时',
    tags: ['法律', '知识产权', '合规'],
    icon: 'Collection',
    gradient: 'linear-gradient(135deg, #6366f1 0%, #818cf8 100%)'
  }
])
</script>

<style scoped>
.courses-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #f0f9ff 0%, #ffffff 100%);
}

.courses-banner {
  background: linear-gradient(135deg, #0c4a6e 0%, #075985 50%, #0ea5e9 100%);
  padding: 50px 40px;
  border-radius: 0 0 40px 40px;
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

.course-card {
  background: #ffffff;
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.course-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 20px 40px -12px rgba(0, 0, 0, 0.15);
}

.course-cover {
  height: 160px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cover-content {
  text-align: center;
  color: #ffffff;
}

.cover-content .el-icon {
  margin-bottom: 8px;
}

.cover-title {
  display: block;
  font-size: 16px;
  font-weight: 600;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.course-body {
  padding: 20px;
}

.course-title {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 8px;
}

.course-teacher {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 12px;
}

.course-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #64748b;
}

.course-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 16px;
}

.course-tag {
  background-color: #f1f5f9;
  color: #475569;
  border: none;
}

.course-footer {
  padding-top: 12px;
  border-top: 1px solid #e2e8f0;
}
</style>
