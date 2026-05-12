<template>
  <div class="coming-page">
    <div class="coming-card">
      <div class="coming-icon">
        <el-icon size="48"><Clock /></el-icon>
      </div>
      <h1 class="coming-title">该测评正在建设中</h1>
      <p class="coming-subtitle">我们正在完善题库、评分模型和结果分析能力，敬请期待。</p>

      <div v-if="assessment" class="coming-info">
        <div class="info-row">
          <span class="info-label">测评名称</span>
          <span class="info-value">{{ assessment.title }}</span>
        </div>
        <div class="info-row">
          <span class="info-label">所属分类</span>
          <span class="info-value">{{ assessment.categoryName }}</span>
        </div>
        <div class="info-row">
          <span class="info-label">预计开放方向</span>
          <span class="info-value">{{ getDirection(assessment.id) }}</span>
        </div>
      </div>

      <div class="coming-status">
        <span class="status-tag">即将开放</span>
      </div>

      <div class="coming-actions">
        <el-button type="primary" size="large" @click="router.push('/assessment')">
          返回在线测评中心
        </el-button>
        <el-button size="large" @click="router.push('/assessment')">
          查看已开放测评
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Clock } from '@element-plus/icons-vue'
import { getAssessmentById } from '@/data/assessmentBank'

const route = useRoute()
const router = useRouter()
const assessment = ref(null)

const directions = {
  'career-temperament': '职业气质类型、行业匹配度和角色发展方向分析',
  'career-values': '职业价值观排序、工作意义感和理想工作模式探索',
  'career-interest': '霍兰德兴趣模型、职业兴趣类型和适配岗位推荐',
  'career-personality': 'MBTI 型职业性格、团队角色定位和职业发展建议',
  'self-learning-ability': '自主学习策略评估、知识转化能力和终身学习画像',
  'communication-ability': '口头/书面表达、倾听技巧和跨场景沟通能力',
  'emotion-control-ability': '情绪觉察、压力管理和心理弹性调节策略'
}

function getDirection(id) {
  return directions[id] || '能力画像分析和个性化发展建议'
}

onMounted(() => {
  const found = getAssessmentById(route.params.id)
  if (found) {
    assessment.value = found
  }
})
</script>

<style scoped>
.coming-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #eff6ff 0%, #f8fafc 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.coming-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 48px 40px;
  max-width: 520px;
  width: 100%;
  text-align: center;
  box-shadow: 0 8px 32px rgba(15, 23, 42, 0.08);
  border: 1px solid #e2e8f0;
  animation: fadeUp 0.5s ease;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(24px); }
  to { opacity: 1; transform: translateY(0); }
}

.coming-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
  background: linear-gradient(135deg, #eff6ff, #dbeafe);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #2563eb;
}

.coming-title {
  font-size: 22px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 10px;
}

.coming-subtitle {
  font-size: 14px;
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 28px;
}

.coming-info {
  background: #f8fafc;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  text-align: left;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
}

.info-row:not(:last-child) {
  border-bottom: 1px solid #f1f5f9;
}

.info-label {
  font-size: 13px;
  color: #94a3b8;
}

.info-value {
  font-size: 14px;
  color: #334155;
  font-weight: 500;
  text-align: right;
  max-width: 60%;
}

.coming-status {
  margin-bottom: 28px;
}

.status-tag {
  display: inline-block;
  font-size: 13px;
  font-weight: 600;
  padding: 6px 18px;
  background: #fff7ed;
  color: #ea580c;
  border-radius: 20px;
  border: 1px solid #fed7aa;
}

.coming-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

@media (max-width: 768px) {
  .coming-card {
    padding: 32px 24px;
  }

  .coming-title {
    font-size: 18px;
  }

  .coming-actions {
    flex-direction: column;
  }
}
</style>