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
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { createProject } from '@/api/project'
import { ElMessage } from 'element-plus'

const router = useRouter()
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

const handleSubmit = async () => {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    const data = { ...form }
    if (data.teacher_id) data.teacher_id = parseInt(data.teacher_id)
    if (data.competition_id) data.competition_id = parseInt(data.competition_id)

    const res = await createProject(data)
    if (res.code === 201) {
      ElMessage.success('项目创建成功')
      router.push('/my-projects')
    } else {
      ElMessage.error(res.message || '创建失败')
    }
  } catch (error) {
    const message = error.response?.data?.message || '创建失败'
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
</style>
