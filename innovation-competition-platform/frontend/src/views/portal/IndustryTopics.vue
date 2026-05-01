<template>
  <div class="industry-topics">
    <!-- Banner -->
    <div class="topics-banner">
      <div class="banner-content">
        <h1 class="banner-title">产业命题</h1>
        <p class="banner-subtitle">对接企业真实需求，解决实际业务问题</p>
      </div>
    </div>

    <!-- 命题列表 -->
    <div class="topics-section">
      <div class="topics-grid">
        <div
          v-for="topic in topics"
          :key="topic.id"
          class="topic-card"
        >
          <div class="topic-header">
            <div class="topic-company">
              <el-avatar :size="48" :style="{ background: topic.gradient }">
                <el-icon size="24"><OfficeBuilding /></el-icon>
              </el-avatar>
              <div class="company-info">
                <h4 class="company-name">{{ topic.company }}</h4>
                <el-tag size="small" :type="topic.difficultyType">{{ topic.difficulty }}</el-tag>
              </div>
            </div>
          </div>
          <div class="topic-body">
            <h3 class="topic-title">{{ topic.title }}</h3>
            <div class="topic-section">
              <h5 class="section-title">命题背景</h5>
              <p class="section-content">{{ topic.background }}</p>
            </div>
            <div class="topic-section">
              <h5 class="section-title">需求说明</h5>
              <p class="section-content">{{ topic.requirement }}</p>
            </div>
            <div class="topic-section">
              <h5 class="section-title">交付物要求</h5>
              <ul class="deliverable-list">
                <li v-for="(item, index) in topic.deliverables" :key="index">
                  {{ item }}
                </li>
              </ul>
            </div>
          </div>
          <div class="topic-footer">
            <div class="topic-meta">
              <span class="meta-item">
                <el-icon><Timer /></el-icon>
                {{ topic.duration }}
              </span>
              <span class="meta-item">
                <el-icon><Coin /></el-icon>
                {{ topic.bonus }}
              </span>
            </div>
            <el-button type="primary" size="small" @click="handleAccept(topic)">
              承接命题
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { OfficeBuilding, Timer, Coin } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()

const handleAccept = async (topic) => {
  try {
    await ElMessageBox.confirm(
      `确定要承接「${topic.title}」命题吗？\n\n承接后，系统将为您创建关联项目，您可以在「我的项目」中查看和管理。`,
      '确认承接命题',
      {
        confirmButtonText: '确认承接',
        cancelButtonText: '取消',
        type: 'info'
      }
    )

    // 模拟承接成功（后续可接入后端 API）
    ElMessage.success(`成功承接「${topic.title}」命题，正在为您创建项目...`)

    // 延迟跳转到创建项目页面，并预填充产业命题信息
    setTimeout(() => {
      router.push({
        path: '/create-project',
        query: {
          topic_id: topic.id,
          topic_title: topic.title,
          topic_company: topic.company
        }
      })
    }, 1000)
  } catch {
    // 用户取消
  }
}

const topics = ref([
  {
    id: 1,
    company: '智慧教育科技',
    title: '智慧校园服务创新命题',
    difficulty: '中等',
    difficultyType: 'warning',
    background: '随着教育信息化2.0的推进，高校对智慧校园建设的需求日益增长。如何整合校园各类服务资源，为师生提供一站式便捷服务，是当前面临的重要挑战。',
    requirement: '设计并开发一个智慧校园服务平台，整合课程表、成绩查询、图书借阅、食堂点餐、宿舍报修等核心功能，提升校园生活便利性。',
    deliverables: [
      '完整的产品需求文档（PRD）',
      '可交互的产品原型',
      '核心功能的前端实现代码',
      '项目演示视频（5分钟以内）'
    ],
    duration: '3个月',
    bonus: '优秀团队可获得实习机会',
    gradient: 'linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%)'
  },
  {
    id: 2,
    company: '绿色未来科技',
    title: '低碳生活数据平台命题',
    difficulty: '困难',
    difficultyType: 'danger',
    background: '碳达峰、碳中和目标下，个人碳足迹管理成为社会关注热点。如何通过技术手段帮助用户记录、分析和减少个人碳排放，具有重要的社会价值。',
    requirement: '开发一个个人碳足迹管理平台，能够记录用户日常出行、消费、能源使用等行为数据，计算碳排放量，并提供减排建议和碳积分奖励机制。',
    deliverables: [
      '完整的技术方案文档',
      '移动端应用原型或Demo',
      '碳排放计算模型说明',
      '商业模式分析报告'
    ],
    duration: '4个月',
    bonus: '奖金 10000 元',
    gradient: 'linear-gradient(135deg, #10b981 0%, #14b8a6 100%)'
  },
  {
    id: 3,
    company: '信用科技实验室',
    title: '校园二手交易信用体系命题',
    difficulty: '中等',
    difficultyType: 'warning',
    background: '校园二手交易市场活跃，但交易双方信任问题制约了市场发展。建立一套可靠的信用评价体系，对促进校园二手交易具有重要意义。',
    requirement: '设计一套校园二手交易信用评价体系，包括用户信用评级、交易评价、信用积分、失信惩戒等机制，并开发相应的系统原型。',
    deliverables: [
      '信用评价体系设计方案',
      '系统功能原型',
      '数据库设计文档',
      '测试用例及报告'
    ],
    duration: '2个月',
    bonus: '奖金 5000 元',
    gradient: 'linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%)'
  },
  {
    id: 4,
    company: '数字企业咨询',
    title: '企业数字化运营工具命题',
    difficulty: '简单',
    difficultyType: 'success',
    background: '中小企业数字化转型需求迫切，但缺乏适合自身规模和业务特点的数字化工具。开发轻量级、易上手的数字化运营工具具有广阔市场前景。',
    requirement: '为中小零售企业开发一套轻量级数字化运营工具，包含库存管理、销售统计、客户管理、营销活动等核心功能模块。',
    deliverables: [
      '产品需求文档',
      'Web应用Demo',
      '用户操作手册',
      '竞品分析报告'
    ],
    duration: '2个月',
    bonus: '实习机会 + 奖金 3000 元',
    gradient: 'linear-gradient(135deg, #f59e0b 0%, #ef4444 100%)'
  }
])
</script>

<style scoped>
.industry-topics {
  min-height: 100vh;
  background: linear-gradient(180deg, #f0f9ff 0%, #ffffff 100%);
}

.topics-banner {
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

.topics-section {
  padding: 40px;
  max-width: 1400px;
  margin: 0 auto;
}

.topics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 24px;
}

.topic-card {
  background: #ffffff;
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.topic-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 20px 40px -12px rgba(0, 0, 0, 0.15);
}

.topic-header {
  padding: 20px;
  border-bottom: 1px solid #f1f5f9;
}

.topic-company {
  display: flex;
  align-items: center;
  gap: 12px;
}

.company-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.company-name {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
}

.topic-body {
  padding: 20px;
}

.topic-title {
  font-size: 17px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 16px;
}

.topic-section {
  margin-bottom: 16px;
}

.section-title {
  font-size: 13px;
  font-weight: 600;
  color: #475569;
  margin-bottom: 6px;
}

.section-content {
  font-size: 13px;
  color: #64748b;
  line-height: 1.6;
}

.deliverable-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.deliverable-list li {
  font-size: 13px;
  color: #64748b;
  padding: 4px 0;
  padding-left: 16px;
  position: relative;
}

.deliverable-list li::before {
  content: '•';
  position: absolute;
  left: 4px;
  color: #0ea5e9;
}

.topic-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-top: 1px solid #f1f5f9;
  background: #f8fafc;
  min-height: 56px;
}

.topic-meta {
  display: flex;
  gap: 16px;
  align-items: center;
  flex: 1;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #64748b;
  white-space: nowrap;
}
</style>
