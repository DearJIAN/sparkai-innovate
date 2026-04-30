<template>
  <div class="login-page">
    <div class="login-container">
      <!-- 左侧品牌区 -->
      <div class="brand-section">
        <div class="brand-content">
          <div class="brand-logo">
            <el-icon size="48" color="var(--primary-400)"><Trophy /></el-icon>
          </div>
          <h1 class="brand-title">创新创业比赛全流程管理系统</h1>
          <p class="brand-subtitle">Innovation Competition Management Platform</p>
          <div class="brand-features">
            <div class="feature-item">
              <el-icon size="20" color="var(--primary-400)"><CircleCheck /></el-icon>
              <span>竞赛发现与报名</span>
            </div>
            <div class="feature-item">
              <el-icon size="20" color="var(--primary-400)"><CircleCheck /></el-icon>
              <span>项目申报与管理</span>
            </div>
            <div class="feature-item">
              <el-icon size="20" color="var(--primary-400)"><CircleCheck /></el-icon>
              <span>团队协作与任务跟踪</span>
            </div>
            <div class="feature-item">
              <el-icon size="20" color="var(--primary-400)"><CircleCheck /></el-icon>
              <span>专家评审与打分</span>
            </div>
            <div class="feature-item">
              <el-icon size="20" color="var(--primary-400)"><CircleCheck /></el-icon>
              <span>AI 智能辅助</span>
            </div>
          </div>

          <!-- 快速登录提示 -->
          <div class="quick-login-hint">
            <p class="hint-title">演示账号</p>
            <div class="hint-accounts">
              <span class="hint-account" @click="fillAccount('student1', 'student123')">学生</span>
              <span class="hint-account" @click="fillAccount('teacher1', 'teacher123')">老师</span>
              <span class="hint-account" @click="fillAccount('judge1', 'judge123')">评委</span>
              <span class="hint-account" @click="fillAccount('admin', 'admin123')">管理员</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧登录表单 -->
      <div class="form-section">
        <div class="form-card">
          <h2 class="form-title">欢迎回来</h2>
          <p class="form-subtitle">请登录您的账号</p>

          <el-form
            ref="formRef"
            :model="form"
            :rules="rules"
            class="login-form"
            @keyup.enter="handleLogin"
          >
            <el-form-item prop="username">
              <el-input
                v-model="form.username"
                placeholder="用户名"
                size="large"
                :prefix-icon="UserIcon"
                class="custom-input"
              />
            </el-form-item>

            <el-form-item prop="password">
              <el-input
                v-model="form.password"
                type="password"
                placeholder="密码"
                size="large"
                :prefix-icon="LockIcon"
                show-password
                class="custom-input"
              />
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                size="large"
                class="login-btn"
                :loading="userStore.isLoading"
                @click="handleLogin"
              >
                登录
              </el-button>
            </el-form-item>
          </el-form>

          <div class="form-footer">
            <span class="text-secondary">还没有账号？</span>
            <router-link to="/register" class="link-primary">立即注册</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import { User as UserIcon, Lock as LockIcon } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref()

const form = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, message: '用户名至少3个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6个字符', trigger: 'blur' }
  ]
}

const fillAccount = (username, password) => {
  form.username = username
  form.password = password
}

const handleLogin = async () => {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  const result = await userStore.login(form)

  if (result.success) {
    ElMessage.success('登录成功')
    // 登录成功后统一跳转到平台首页
    router.push('/portal')
  } else {
    ElMessage.error(result.message)
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  background-color: var(--bg-secondary);
}

.login-container {
  display: flex;
  width: 100%;
  min-height: 100vh;
}

/* 左侧品牌区 */
.brand-section {
  flex: 1;
  background: linear-gradient(135deg, var(--gray-900) 0%, var(--primary-900) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px;
  position: relative;
  overflow: hidden;
}

.brand-section::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -20%;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(34, 211, 238, 0.1) 0%, transparent 70%);
  border-radius: 50%;
}

.brand-content {
  position: relative;
  z-index: 1;
  max-width: 480px;
}

.brand-logo {
  margin-bottom: 32px;
}

.brand-title {
  font-family: var(--font-heading);
  font-size: 32px;
  font-weight: 700;
  color: var(--text-inverse);
  margin-bottom: 12px;
  line-height: 1.3;
}

.brand-subtitle {
  font-size: 16px;
  color: var(--primary-300);
  margin-bottom: 48px;
  letter-spacing: 1px;
}

.brand-features {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--gray-300);
  font-size: 15px;
}

/* 右侧表单区 */
.form-section {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px;
  background-color: var(--bg-secondary);
}

.form-card {
  width: 100%;
  max-width: 420px;
  background-color: var(--bg-primary);
  border-radius: var(--radius-xl);
  padding: 48px;
  box-shadow: var(--shadow-lg);
}

.form-title {
  font-family: var(--font-heading);
  font-size: 28px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.form-subtitle {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 32px;
}

.login-form {
  margin-bottom: 24px;
}

:deep(.custom-input .el-input__wrapper) {
  border-radius: var(--radius-md);
  box-shadow: 0 0 0 1px var(--border-light) inset;
  padding: 4px 16px;
}

:deep(.custom-input .el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px var(--primary-400) inset;
}

:deep(.custom-input .el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px var(--primary-500) inset;
}

.login-btn {
  width: 100%;
  height: 44px;
  border-radius: var(--radius-md);
  font-size: 15px;
  font-weight: 500;
  background-color: var(--primary-600);
  border-color: var(--primary-600);
  transition: all var(--transition-fast);
}

.login-btn:hover {
  background-color: var(--primary-700);
  border-color: var(--primary-700);
}

.form-footer {
  text-align: center;
  font-size: 14px;
}

.text-secondary {
  color: var(--text-secondary);
}

.link-primary {
  color: var(--primary-600);
  text-decoration: none;
  font-weight: 500;
  margin-left: 4px;
  transition: color var(--transition-fast);
}

.link-primary:hover {
  color: var(--primary-700);
}

/* 快速登录提示 */
.quick-login-hint {
  margin-top: 40px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: var(--radius-lg);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.hint-title {
  font-size: 12px;
  color: var(--gray-400);
  margin-bottom: 10px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.hint-accounts {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.hint-account {
  padding: 6px 12px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-md);
  font-size: 13px;
  color: var(--gray-300);
  cursor: pointer;
  transition: all var(--transition-fast);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.hint-account:hover {
  background: rgba(255, 255, 255, 0.2);
  color: var(--text-inverse);
  border-color: var(--primary-400);
}

/* 响应式 */
@media (max-width: 1024px) {
  .brand-section {
    display: none;
  }

  .form-section {
    padding: 24px;
  }
}
</style>
