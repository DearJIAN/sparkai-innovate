<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">创建项目</h2>
    </div>

    <el-card class="form-card" shadow="never">
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-position="top"
        class="project-form"
      >
        <el-row :gutter="24">
          <el-col :span="12">
            <el-form-item label="项目名称" prop="name">
              <el-input v-model="form.name" placeholder="请输入项目名称" size="large" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="项目类别" prop="category">
              <el-select v-model="form.category" placeholder="请选择类别" size="large" style="width: 100%">
                <el-option label="科技创新" value="科技创新" />
                <el-option label="社会服务" value="社会服务" />
                <el-option label="文化创意" value="文化创意" />
                <el-option label="电子商务" value="电子商务" />
                <el-option label="现代农业" value="现代农业" />
                <el-option label="其他" value="其他" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="24">
          <el-col :span="12">
            <el-form-item label="所属赛道" prop="track">
              <el-select v-model="form.track" placeholder="请选择赛道" size="large" style="width: 100%">
                <el-option label="人工智能" value="人工智能" />
                <el-option label="大数据" value="大数据" />
                <el-option label="物联网" value="物联网" />
                <el-option label="新能源" value="新能源" />
                <el-option label="生物医药" value="生物医药" />
                <el-option label="智能制造" value="智能制造" />
                <el-option label="数字经济" value="数字经济" />
                <el-option label="其他" value="其他" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="当前阶段" prop="stage">
              <el-select v-model="form.stage" placeholder="请选择阶段" size="large" style="width: 100%">
                <el-option label="创意阶段" value="idea" />
                <el-option label="验证阶段" value="proof" />
                <el-option label="资源整合" value="resource" />
                <el-option label="产品开发" value="development" />
                <el-option label="市场推广" value="market" />
                <el-option label="路演展示" value="roadshow" />
                <el-option label="孵化运营" value="incubation" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="项目简介" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="4"
            placeholder="请简要描述您的项目，包括项目背景、目标、创新点等"
          />
        </el-form-item>

        <el-row :gutter="24">
          <el-col :span="12">
            <el-form-item label="指导老师 ID" prop="teacher_id">
              <el-input v-model="form.teacher_id" placeholder="请输入指导老师用户 ID" size="large" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="比赛批次 ID" prop="competition_id">
              <el-input v-model="form.competition_id" placeholder="请输入比赛批次 ID（可选）" size="large" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="24">
          <el-col :span="12">
            <el-form-item label="开始时间" prop="start_date">
              <el-date-picker
                v-model="form.start_date"
                type="date"
                placeholder="选择开始时间"
                size="large"
                style="width: 100%"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="预计结束时间" prop="end_date">
              <el-date-picker
                v-model="form.end_date"
                type="date"
                placeholder="选择预计结束时间"
                size="large"
                style="width: 100%"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <div class="quick-fill-bar">
        <el-icon><MagicStick /></el-icon>
        <span>调试辅助：一键快速生成项目信息</span>
        <el-button type="primary" size="small" @click="quickFillProject">
          快速填充
        </el-button>
      </div>

      <el-form-item class="form-actions">
        <el-button size="large" @click="$router.back()">取消</el-button>
        <el-button type="primary" size="large" :loading="submitting" @click="handleSubmit">
          创建项目
        </el-button>
      </el-form-item>
    </el-form>
  </el-card>
</div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { createProject } from '@/api/project'
import { ElMessage } from 'element-plus'
import { MagicStick } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const formRef = ref()
const submitting = ref(false)

const form = reactive({
  name: '',
  description: '',
  category: '',
  track: '',
  stage: 'idea',
  teacher_id: '',
  competition_id: '',
  start_date: '',
  end_date: ''
})

const rules = {
  name: [
    { required: true, message: '请输入项目名称', trigger: 'blur' },
    { min: 2, max: 100, message: '项目名称长度在 2-100 个字符', trigger: 'blur' }
  ],
  category: [{ required: true, message: '请选择项目类别', trigger: 'change' }],
  track: [{ required: true, message: '请选择所属赛道', trigger: 'change' }],
  stage: [{ required: true, message: '请选择当前阶段', trigger: 'change' }],
  description: [
    { required: true, message: '请输入项目简介', trigger: 'blur' },
    { min: 10, message: '项目简介至少 10 个字符', trigger: 'blur' }
  ]
}

onMounted(() => {
  if (route.query.source === 'industry_topic') {
    if (route.query.topic_title) {
      form.name = `基于【${route.query.topic_title}】的创新项目`
    }
    
    let desc = ''
    if (route.query.proposal) desc += `【方案概述】\n${route.query.proposal}\n\n`
    if (route.query.advantage) desc += `【团队优势】\n${route.query.advantage}`
    if (desc) {
      form.description = desc
    }
    
    form.category = '科技创新'
    form.track = '其他'
  }
})

const quickFillProject = () => {
  const projectNames = [
    '智慧校园一站式服务平台',
    'AI 驱动的个性化学习助手',
    '校园二手交易信用平台',
    '基于区块链的学历认证系统',
    '大学生创业资源共享平台'
  ]
  const categories = ['科技创新', '社会服务', '文化创意', '电子商务', '现代农业']
  const tracks = ['人工智能', '大数据', '物联网', '新能源', '生物医药', '智能制造', '数字经济']
  const stages = ['idea', 'proof', 'resource', 'development', 'market']

  form.name = projectNames[Math.floor(Math.random() * projectNames.length)]
  form.category = categories[Math.floor(Math.random() * categories.length)]
  form.track = tracks[Math.floor(Math.random() * tracks.length)]
  form.stage = stages[Math.floor(Math.random() * stages.length)]
  form.description = `本项目旨在通过${form.track}技术，打造一个面向大学生的${form.category}平台。项目将整合校园内外资源，为用户提供便捷的服务体验，同时探索可持续的商业模式。团队由跨学科成员组成，具备扎实的技术功底和丰富的实践经验。`
  form.teacher_id = ''
  form.competition_id = ''

  const now = new Date()
  form.start_date = now.toISOString().split('T')[0]
  const end = new Date(now.getTime() + 90 * 24 * 60 * 60 * 1000)
  form.end_date = end.toISOString().split('T')[0]

  ElMessage.success('已快速生成项目信息')
}

const handleSubmit = async () => {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    // 数据预处理
    const data = { ...form }

    // 处理 teacher_id：空字符串转为 null，非空转为整数
    if (data.teacher_id && String(data.teacher_id).trim()) {
      const tid = parseInt(data.teacher_id)
      if (isNaN(tid) || tid <= 0) {
        ElMessage.warning('指导老师 ID 必须是有效的正整数')
        submitting.value = false
        return
      }
      data.teacher_id = tid
    } else {
      data.teacher_id = null
    }

    // 处理 competition_id：空字符串转为 null，非空转为整数
    if (data.competition_id && String(data.competition_id).trim()) {
      const cid = parseInt(data.competition_id)
      if (isNaN(cid) || cid <= 0) {
        ElMessage.warning('比赛批次 ID 必须是有效的正整数')
        submitting.value = false
        return
      }
      data.competition_id = cid
    } else {
      data.competition_id = null
    }

    // 处理日期：确保是字符串格式
    if (data.start_date && typeof data.start_date === 'object') {
      data.start_date = data.start_date.toISOString().split('T')[0]
    }
    if (data.end_date && typeof data.end_date === 'object') {
      data.end_date = data.end_date.toISOString().split('T')[0]
    }

    const res = await createProject(data)
    if (res.code === 201 || res.code === 200) {
      ElMessage.success('项目创建成功')
      router.push('/my-projects')
    } else {
      ElMessage.error(res.message || '创建失败')
    }
  } catch (error) {
    console.error('[CreateProject] Error:', error)
    let message = '创建失败'
    if (error.response) {
      const status = error.response.status
      const serverMsg = error.response.data?.message || error.response.data?.error
      if (status === 500) {
        message = serverMsg || '服务器内部错误，请检查输入数据格式是否正确'
      } else if (status === 400) {
        message = serverMsg || '请求参数错误，请检查必填项'
      } else if (status === 401) {
        message = '登录已过期，请重新登录'
      } else if (status === 403) {
        message = '权限不足，无法创建项目'
      } else {
        message = serverMsg || `请求失败 (${status})`
      }
    } else if (error.request) {
      message = '网络连接失败，请检查网络后重试'
    } else {
      message = error.message || '创建失败'
    }
    ElMessage.error(message)
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.page-container {
  padding-bottom: 20px;
}

.page-header {
  margin-bottom: 24px;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
}

.form-card {
  max-width: 900px;
}

.project-form :deep(.el-form-item__label) {
  font-weight: 500;
  color: var(--text-primary);
  padding-bottom: 8px;
}

.form-actions {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid var(--border-light);
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
