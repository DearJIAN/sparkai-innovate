<template>
  <div class="accept-topic-page">
    <div class="page-header">
      <h2 class="page-title">承接产业命题</h2>
      <p class="page-subtitle">填写承接信息，开始你的企业真实项目</p>
    </div>

    <el-card class="form-card" shadow="never" v-loading="loading">
      <!-- 命题信息展示 -->
      <div v-if="topic" class="topic-info-bar">
        <div class="topic-company">
          <el-icon><OfficeBuilding /></el-icon>
          <span>{{ topic.company }}</span>
        </div>
        <h3 class="topic-title">{{ topic.title }}</h3>
        <div class="topic-meta">
          <el-tag size="small" :type="topic.categoryType">{{ topic.category }}</el-tag>
          <span class="meta-item">
            <el-icon><Timer /></el-icon>
            {{ topic.duration }}
          </span>
          <span class="meta-item">
            <el-icon><Coin /></el-icon>
            {{ topic.bonus }}
          </span>
        </div>
      </div>

      <el-divider content-position="left">承接信息</el-divider>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-position="top"
        class="accept-form"
      >
        <el-row :gutter="24">
          <el-col :span="12">
            <el-form-item label="项目负责人" prop="leader_name">
              <el-input v-model="form.leader_name" placeholder="请输入负责人姓名" size="large" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="form.phone" placeholder="请输入联系电话" size="large" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="24">
          <el-col :span="12">
            <el-form-item label="团队人数" prop="team_size">
              <el-input-number v-model="form.team_size" :min="1" :max="20" size="large" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="预计完成时间" prop="expected_finish">
              <el-date-picker
                v-model="form.expected_finish"
                type="date"
                placeholder="选择预计完成时间"
                size="large"
                style="width: 100%"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="项目方案概述" prop="proposal">
          <el-input
            v-model="form.proposal"
            type="textarea"
            :rows="4"
            placeholder="请简要描述你的项目方案思路，包括技术路线、实施计划等"
          />
        </el-form-item>

        <el-form-item label="团队优势" prop="advantage">
          <el-input
            v-model="form.advantage"
            type="textarea"
            :rows="3"
            placeholder="请描述团队的核心优势，如技术能力、相关经验、资源等"
          />
        </el-form-item>

        <el-form-item label="备注（可选）">
          <el-input
            v-model="form.remark"
            type="textarea"
            :rows="2"
            placeholder="其他需要说明的信息"
          />
        </el-form-item>

        <div class="quick-fill-bar">
          <el-icon><MagicStick /></el-icon>
          <span>调试辅助：一键快速生成承接信息</span>
          <el-button type="primary" size="small" @click="quickFill">
            快速填充
          </el-button>
        </div>

        <el-form-item class="form-actions">
          <el-button size="large" @click="$router.back()">取消</el-button>
          <el-button type="primary" size="large" :loading="submitting" @click="handleSubmit">
            确认承接
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { OfficeBuilding, Timer, Coin, MagicStick } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const formRef = ref()
const loading = ref(false)
const submitting = ref(false)

const topic = ref(null)

const form = reactive({
  leader_name: '',
  phone: '',
  team_size: 3,
  expected_finish: '',
  proposal: '',
  advantage: '',
  remark: ''
})

const rules = {
  leader_name: [
    { required: true, message: '请输入负责人姓名', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入联系电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号码', trigger: 'blur' }
  ],
  team_size: [
    { required: true, message: '请输入团队人数', trigger: 'change' }
  ],
  expected_finish: [
    { required: true, message: '请选择预计完成时间', trigger: 'change' }
  ],
  proposal: [
    { required: true, message: '请输入项目方案概述', trigger: 'blur' },
    { min: 20, message: '方案概述至少 20 个字符', trigger: 'blur' }
  ],
  advantage: [
    { required: true, message: '请输入团队优势', trigger: 'blur' },
    { min: 10, message: '团队优势至少 10 个字符', trigger: 'blur' }
  ]
}

// 加载命题信息
onMounted(() => {
  const topicId = parseInt(route.params.id)
  const topicTitle = route.query.topic_title
  const topicCompany = route.query.topic_company

  if (!topicId) {
    ElMessage.error('命题信息不存在')
    router.push('/industry-topics')
    return
  }

  // 模拟加载命题数据（后续可接入后端 API）
  topic.value = {
    id: topicId,
    title: topicTitle || '企业真实命题',
    company: topicCompany || '合作企业',
    category: '技术开发',
    categoryType: 'primary',
    duration: '3-6 个月',
    bonus: '5000-20000 元'
  }
})

const quickFill = () => {
  form.leader_name = '张三'
  form.phone = '13800138000'
  form.team_size = 5
  form.proposal = '本项目将采用敏捷开发模式，分三个阶段实施：第一阶段进行需求调研和技术选型；第二阶段完成核心功能开发；第三阶段进行测试优化和交付。技术栈计划使用 Vue3 + Spring Boot，数据库采用 MySQL + Redis。'
  form.advantage = '团队成员涵盖前端、后端、UI设计和产品经理，具备多个项目实战经验。曾获省级创新创业大赛奖项，熟悉企业级应用开发流程。'
  form.remark = '团队可全职投入，每周保证至少 40 小时开发时间。'

  const now = new Date()
  const finish = new Date(now.getTime() + 120 * 24 * 60 * 60 * 1000)
  form.expected_finish = finish.toISOString().split('T')[0]

  ElMessage.success('已快速生成承接信息')
}

const handleSubmit = async () => {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    // 模拟提交（后续接入后端 API）
    await new Promise(r => setTimeout(r, 1500))

    ElMessage.success('命题承接成功！已为你创建关联项目')

    // 跳转到创建项目页面，预填充产业命题信息
    router.push({
      path: '/create-project',
      query: {
        topic_id: topic.value.id,
        topic_title: topic.value.title,
        proposal: form.proposal,
        advantage: form.advantage,
        source: 'industry_topic'
      }
    })
  } catch (error) {
    ElMessage.error('提交失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.accept-topic-page {
  padding: 20px 40px 40px;
  max-width: 900px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 24px;
}

.page-title {
  font-size: 22px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 4px;
}

.page-subtitle {
  font-size: 14px;
  color: #64748b;
}

.topic-info-bar {
  background: linear-gradient(135deg, #0c4a6e 0%, #075985 50%, #0ea5e9 100%);
  border-radius: 12px;
  padding: 20px 24px;
  color: #ffffff;
  margin-bottom: 24px;
}

.topic-company {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #bae6fd;
  margin-bottom: 8px;
}

.topic-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 12px;
}

.topic-meta {
  display: flex;
  align-items: center;
  gap: 16px;
}

.topic-meta .meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #bae6fd;
}

.accept-form :deep(.el-form-item__label) {
  font-weight: 500;
  color: #1e293b;
  padding-bottom: 8px;
}

.form-actions {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #e2e8f0;
}

.form-actions .el-button {
  min-width: 120px;
}

.form-actions .el-button + .el-button {
  margin-left: 16px;
}

.quick-fill-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border: 1px dashed #0ea5e9;
  border-radius: 10px;
  margin-bottom: 20px;
  color: #0369a1;
  font-size: 13px;
}

.quick-fill-bar .el-icon {
  color: #0ea5e9;
}

.quick-fill-bar span {
  flex: 1;
}
</style>
