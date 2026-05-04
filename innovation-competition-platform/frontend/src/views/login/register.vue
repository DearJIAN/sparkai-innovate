<template>
  <div class="register-page">
    <div class="register-container">
      <div class="form-card">
        <div class="form-header">
          <el-icon size="40" color="var(--primary-600)"><Trophy /></el-icon>
          <h2 class="form-title">创建账号</h2>
          <p class="form-subtitle">加入火花智创 SparkAI Innovate</p>
        </div>

        <el-form
          ref="formRef"
          :model="form"
          :rules="rules"
          class="register-form"
          label-position="top"
        >
          <el-form-item label="用户名" prop="username">
            <el-input v-model="form.username" placeholder="请输入用户名" size="large" />
          </el-form-item>

          <el-form-item label="密码" prop="password">
            <el-input v-model="form.password" type="password" placeholder="请输入密码" size="large" show-password />
          </el-form-item>

          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input v-model="form.confirmPassword" type="password" placeholder="请再次输入密码" size="large" show-password />
          </el-form-item>

          <el-form-item label="角色" prop="role">
            <el-select v-model="form.role" placeholder="请选择角色" size="large" style="width: 100%">
              <el-option label="学生" value="student" />
              <el-option label="指导老师" value="teacher" />
              <el-option label="评委" value="judge" />
            </el-select>
          </el-form-item>

          <el-form-item label="真实姓名" prop="real_name">
            <el-input v-model="form.real_name" placeholder="请输入真实姓名" size="large" />
          </el-form-item>

          <el-form-item label="邮箱" prop="email">
            <el-input v-model="form.email" placeholder="请输入邮箱" size="large" />
          </el-form-item>

          <el-form-item label="学院" prop="college">
            <el-input v-model="form.college" placeholder="请输入学院" size="large" />
          </el-form-item>

          <el-form-item label="专业" prop="major">
            <el-input v-model="form.major" placeholder="请输入专业" size="large" />
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              class="register-btn"
              :loading="loading"
              @click="handleRegister"
            >
              注册
            </el-button>
          </el-form-item>
        </el-form>

        <div class="form-footer">
          <span class="text-secondary">已有账号？</span>
          <router-link to="/login" class="link-primary">立即登录</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '@/api/auth'
import { ElMessage } from 'element-plus'

const router = useRouter()
const formRef = ref()
const loading = ref(false)

const form = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  role: 'student',
  real_name: '',
  email: '',
  college: '',
  major: ''
})

const validatePass2 = (rule, value, callback) => {
  if (value !== form.password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, message: '用户名至少3个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validatePass2, trigger: 'blur' }
  ],
  role: [{ required: true, message: '请选择角色', trigger: 'change' }],
  real_name: [{ required: true, message: '请输入真实姓名', trigger: 'blur' }],
  email: [{ type: 'email', message: '邮箱格式不正确', trigger: 'blur' }]
}

const handleRegister = async () => {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  loading.value = true
  try {
    const { confirmPassword, ...registerData } = form
    const res = await register(registerData)
    if (res.code === 201) {
      ElMessage.success('注册成功，请登录')
      router.push('/login')
    } else {
      ElMessage.error(res.message || '注册失败')
    }
  } catch (error) {
    const message = error.response?.data?.message || '注册失败'
    ElMessage.error(message)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--gray-900) 0%, var(--primary-900) 100%);
  padding: 40px 20px;
}

.register-container {
  width: 100%;
  max-width: 520px;
}

.form-card {
  background-color: var(--bg-primary);
  border-radius: var(--radius-xl);
  padding: 40px;
  box-shadow: var(--shadow-xl);
}

.form-header {
  text-align: center;
  margin-bottom: 32px;
}

.form-title {
  font-family: var(--font-heading);
  font-size: 24px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 16px 0 8px;
}

.form-subtitle {
  font-size: 14px;
  color: var(--text-secondary);
}

.register-btn {
  width: 100%;
  height: 44px;
  border-radius: var(--radius-md);
  font-size: 15px;
  font-weight: 500;
  background-color: var(--primary-600);
  border-color: var(--primary-600);
  margin-top: 8px;
}

.register-btn:hover {
  background-color: var(--primary-700);
  border-color: var(--primary-700);
}

.form-footer {
  text-align: center;
  margin-top: 20px;
  color: var(--text-secondary);
  font-size: 14px;
}

.link-primary {
  color: var(--primary-600);
  text-decoration: none;
  font-weight: 500;
  margin-left: 4px;
}

.link-primary:hover {
  color: var(--primary-700);
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: var(--text-primary);
}

:deep(.el-input__wrapper) {
  border-radius: var(--radius-md);
}
</style>
