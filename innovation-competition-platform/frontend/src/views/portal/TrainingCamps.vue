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
          <div class="camp-header" :style="{ background: camp.gradient }">
            <div class="camp-icon">
              <el-icon size="40"><component :is="camp.icon" /></el-icon>
            </div>
            <h3 class="camp-title">{{ camp.title }}</h3>
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
              <el-button type="primary" size="small">
                开始学习
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
import { Clock, User, Star, Opportunity, EditPen, Mic, Cpu } from '@element-plus/icons-vue'

const camps = ref([
  {
    id: 1,
    title: '创新创业基础训练营',
    description: '从零开始学习创新创业基础知识，掌握创业思维和方法论，了解创业全流程。',
    hours: 24,
    students: 1256,
    difficulty: '入门',
    tags: ['创业基础', '商业模式', '市场调研'],
    target: '零基础学生',
    icon: 'Opportunity',
    gradient: 'linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%)'
  },
  {
    id: 2,
    title: '商业计划书写作训练营',
    description: '系统学习商业计划书的撰写方法，包括市场分析、财务预测、团队介绍等核心模块。',
    hours: 18,
    students: 987,
    difficulty: '中级',
    tags: ['商业计划书', '财务分析', '市场预测'],
    target: '有创业想法的学生',
    icon: 'EditPen',
    gradient: 'linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%)'
  },
  {
    id: 3,
    title: '路演表达训练营',
    description: '提升路演演讲能力，学习PPT制作技巧，掌握答辩应对策略，让你的项目脱颖而出。',
    hours: 12,
    students: 1567,
    difficulty: '中级',
    tags: ['演讲技巧', 'PPT制作', '答辩技巧'],
    target: '准备参赛的学生',
    icon: 'Mic',
    gradient: 'linear-gradient(135deg, #f59e0b 0%, #ef4444 100%)'
  },
  {
    id: 4,
    title: 'AI 项目孵化训练营',
    description: '学习如何将AI技术应用到实际项目中，包括大模型应用、智能体开发、AI产品设计等。',
    hours: 32,
    students: 2341,
    difficulty: '高级',
    tags: ['人工智能', '大模型', '智能体'],
    target: '有技术基础的学生',
    icon: 'Cpu',
    gradient: 'linear-gradient(135deg, #10b981 0%, #14b8a6 100%)'
  }
])
</script>

<style scoped>
.training-camps {
  min-height: 100vh;
  background: linear-gradient(180deg, #f0f9ff 0%, #ffffff 100%);
}

.camps-banner {
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
</style>
