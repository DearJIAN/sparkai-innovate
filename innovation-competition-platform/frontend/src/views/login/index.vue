<template>
  <div class="login-page">
    <div class="login-container">
      <!-- 左侧品牌区 -->
      <div class="brand-section">
        <div class="brand-bento">
          <div class="bento-card main-card">
            <div class="main-head">
              <span class="spark-seed"></span>
              <p class="brand-system-title">火种计划 SPARK</p>
            </div>
            <h2 class="main-title">创新创业基础</h2>
            <SparkLogo size="large" />
            <p class="brand-subtitle">Innovate with AI, Spark Your Future</p>
            <div class="feature-grid">
              <span class="feature-chip">竞赛报名</span>
              <span class="feature-chip">项目申报</span>
              <span class="feature-chip">团队协作</span>
              <span class="feature-chip">导师辅导</span>
              <span class="feature-chip">商业计划书</span>
              <span class="feature-chip">专家评审</span>
              <span class="feature-chip">路演答辩</span>
              <span class="feature-chip">项目孵化</span>
            </div>
          </div>

          <div class="bento-card timeline-card" aria-hidden="true">
            <p class="card-title">项目孵化时间轴</p>
            <div class="timeline-track">
              <span class="timeline-node n1"></span>
              <span class="timeline-node n2"></span>
              <span class="timeline-node n3"></span>
              <span class="timeline-node n4"></span>
              <span class="rocket-rise">↑</span>
            </div>
            <div class="timeline-labels">
              <span>创意</span><span>验证</span><span>路演</span><span>孵化</span>
            </div>
          </div>

          <div class="bento-card trend-card" aria-hidden="true">
            <p class="card-title">成长趋势</p>
            <svg viewBox="0 0 300 120" class="trend-svg">
              <polyline points="10,100 70,86 125,72 185,58 240,40 290,24" class="trend-line"/>
              <circle cx="70" cy="86" r="4" class="trend-dot d1"/>
              <circle cx="125" cy="72" r="4" class="trend-dot d2"/>
              <circle cx="185" cy="58" r="4" class="trend-dot d3"/>
              <circle cx="240" cy="40" r="4" class="trend-dot d4"/>
            </svg>
            <div class="trend-value">完成项目 <span>126</span></div>
          </div>

          <div class="bento-card task-card" aria-hidden="true">
            <p class="card-title">任务完成度</p>
            <div class="task-bars">
              <span class="task-bar t1"></span>
              <span class="task-bar t2"></span>
              <span class="task-bar t3"></span>
              <span class="task-bar t4"></span>
              <span class="task-bar t5"></span>
            </div>
            <div class="task-checklist">
              <span class="task-item">需求梳理</span>
              <span class="task-item">BP 初稿</span>
              <span class="task-item">路演演练</span>
            </div>
          </div>

          <div class="bento-card energy-card" aria-hidden="true">
            <p class="card-title">创业能量</p>
            <div class="energy-ring"></div>
            <div class="energy-count">
              <span class="num-scroll">92</span><span>%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧登录表单 -->
      <div class="form-section">
        <div class="form-stack">
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
          <div class="quick-login-hint quick-login-hint-right">
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
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import { User as UserIcon, Lock as LockIcon } from '@element-plus/icons-vue'
import SparkLogo from '@/components/SparkLogo.vue'

const route = useRoute()
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
    const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : '/portal'
    router.push(redirect.startsWith('/login') ? '/portal' : redirect)
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
  background: linear-gradient(135deg, #eff7ff 0%, #eaf5ff 35%, #eef0ff 70%, #f5efff 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  position: relative;
  overflow: hidden;
}

.brand-section::before {
  content: '';
  position: absolute;
  top: -30%;
  right: -10%;
  width: 560px;
  height: 560px;
  background: radial-gradient(circle, rgba(56, 189, 248, 0.24) 0%, transparent 72%);
  border-radius: 50%;
}

.brand-bento {
  position: relative;
  z-index: 2;
  width: min(860px, 100%);
  display: grid;
  grid-template-columns: 1.45fr 1fr;
  grid-template-rows: 240px 240px 230px;
  gap: 18px;
}

.bento-card {
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.68);
  border: 1px solid rgba(255, 255, 255, 0.95);
  box-shadow: 0 18px 36px rgba(37, 99, 235, 0.15);
  backdrop-filter: blur(12px);
  position: relative;
  overflow: hidden;
  padding: 20px 22px;
}

.bento-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(130deg, rgba(255, 255, 255, 0.16), rgba(255, 255, 255, 0));
  pointer-events: none;
}

.main-card {
  grid-column: 1 / 2;
  grid-row: 1 / 4;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  overflow: auto;
}

.main-head {
  display: flex;
  align-items: center;
  gap: 10px;
}

.spark-seed {
  width: 13px;
  height: 13px;
  border-radius: 50%;
  background: radial-gradient(circle, #facc15 0%, #fb7185 52%, #a855f7 100%);
  box-shadow: 0 0 0 0 rgba(250, 204, 21, 0.4);
  animation: seedGlow 2.2s ease-in-out infinite;
}

.brand-system-title {
  font-size: 24px;
  font-weight: 700;
  margin: 0;
  letter-spacing: 0.6px;
  background: linear-gradient(135deg, #f97316 0%, #ef4444 35%, #a855f7 70%, #3b82f6 100%);
  background-size: 300% 300%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: brandTitleGradient 4s ease infinite;
}

.main-title {
  margin: 10px 0 12px;
  font-size: 40px;
  line-height: 1.1;
  color: #1e3a8a;
  font-weight: 800;
}

.brand-subtitle {
  font-size: 15px;
  color: #1d4ed8;
  margin: 8px 0 16px;
  letter-spacing: 0.8px;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  margin-bottom: 12px;
}

.feature-chip {
  font-size: 14px;
  color: #1e3a8a;
  font-weight: 600;
  padding: 10px 12px;
  border-radius: 12px;
  background: rgba(219, 234, 254, 0.7);
  border: 1px solid rgba(147, 197, 253, 0.45);
}

.card-title {
  margin: 0 0 12px;
  font-size: 18px;
  color: #1e3a8a;
  font-weight: 700;
}

.timeline-card { grid-column: 2 / 3; grid-row: 1 / 2; }
.trend-card { grid-column: 2 / 3; grid-row: 2 / 3; }
.task-card { grid-column: 1 / 2; grid-row: 3 / 4; }
.energy-card { grid-column: 2 / 3; grid-row: 3 / 4; }

.timeline-track {
  position: relative;
  height: 84px;
  border-radius: 14px;
  background: linear-gradient(90deg, rgba(219, 234, 254, 0.9), rgba(224, 231, 255, 0.9));
  overflow: hidden;
}

.timeline-track::before {
  content: '';
  position: absolute;
  left: 8%;
  right: 8%;
  top: 50%;
  height: 4px;
  transform: translateY(-50%);
  border-radius: 99px;
  background: linear-gradient(90deg, #60a5fa, #818cf8);
}

.timeline-node {
  position: absolute;
  top: 50%;
  width: 14px;
  height: 14px;
  margin-top: -7px;
  border-radius: 50%;
  background: #fff;
  border: 3px solid #60a5fa;
  box-shadow: 0 0 0 0 rgba(96, 165, 250, 0.28);
  animation: nodeLight 2.8s ease-in-out infinite;
}

.timeline-node.n1 { left: 10%; }
.timeline-node.n2 { left: 34%; animation-delay: .35s; }
.timeline-node.n3 { left: 58%; animation-delay: .7s; }
.timeline-node.n4 { left: 82%; animation-delay: 1.05s; }

.rocket-rise {
  position: absolute;
  right: 14px;
  bottom: 8px;
  color: #2563eb;
  font-size: 22px;
  animation: rocketRise 2.2s ease-in-out infinite;
}

.timeline-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
  font-size: 13px;
  color: #334155;
}

.trend-svg {
  width: 100%;
  height: 120px;
}

.trend-line {
  fill: none;
  stroke: #3b82f6;
  stroke-width: 4;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-dasharray: 360;
  stroke-dashoffset: 360;
  animation: drawLine 3.4s ease-in-out infinite;
}

.trend-dot {
  fill: #22d3ee;
  opacity: 0;
  animation: dotShow 3.4s ease-in-out infinite;
}

.trend-dot.d1 { animation-delay: .45s; }
.trend-dot.d2 { animation-delay: .75s; }
.trend-dot.d3 { animation-delay: 1.05s; }
.trend-dot.d4 { animation-delay: 1.35s; }

.trend-value {
  font-size: 14px;
  color: #334155;
}

.trend-value span {
  margin-left: 6px;
  color: #2563eb;
  font-size: 24px;
  font-weight: 700;
  animation: valuePulse 2.1s ease-in-out infinite;
}

.task-bars {
  height: 112px;
  display: flex;
  align-items: flex-end;
  gap: 10px;
}

.task-bar {
  flex: 1;
  border-radius: 12px 12px 5px 5px;
  background: linear-gradient(180deg, #60a5fa 0%, #22d3ee 100%);
  transform-origin: bottom;
  animation: barGrow 2.8s ease-in-out infinite;
}

.task-bar.t1 { height: 38%; }
.task-bar.t2 { height: 52%; animation-delay: .2s; }
.task-bar.t3 { height: 68%; animation-delay: .4s; }
.task-bar.t4 { height: 84%; animation-delay: .6s; }
.task-bar.t5 { height: 58%; animation-delay: .8s; }

.task-checklist {
  margin-top: 10px;
  display: flex;
  gap: 10px;
}

.task-item {
  flex: 1;
  font-size: 12px;
  color: #1e3a8a;
  padding: 6px 8px;
  border-radius: 10px;
  background: rgba(224, 231, 255, 0.8);
  text-align: center;
  position: relative;
}

.task-item::after {
  content: '✓';
  margin-left: 4px;
  color: #16a34a;
  opacity: 0.3;
  animation: checkBlink 1.9s ease-in-out infinite;
}

.task-item:nth-child(2)::after { animation-delay: .35s; }
.task-item:nth-child(3)::after { animation-delay: .7s; }

.energy-ring {
  width: 128px;
  height: 128px;
  border-radius: 50%;
  margin: 8px auto 4px;
  background:
    radial-gradient(closest-side, rgba(255, 255, 255, 1) 69%, transparent 71% 100%),
    conic-gradient(#3b82f6 0deg, #22d3ee 240deg, rgba(219, 234, 254, 0.9) 240deg 360deg);
  animation: ringRotate 7s linear infinite;
}

.energy-count {
  text-align: center;
  color: #1e3a8a;
  font-size: 30px;
  font-weight: 800;
}

.num-scroll {
  display: inline-block;
  animation: numberRise 2.6s ease-in-out infinite;
}

@keyframes brandTitleGradient {
  0%, 100% { background-position: 0% 50%; }
  25% { background-position: 100% 0%; }
  50% { background-position: 100% 100%; }
  75% { background-position: 0% 100%; }
  75% { background-position: 0% 100%; }
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

.form-stack {
  width: 100%;
  max-width: 420px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.form-card {
  width: 100%;
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
  margin-top: 12px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.72);
  border-radius: var(--radius-lg);
  border: 1px solid rgba(147, 197, 253, 0.4);
  position: relative;
  z-index: 1;
}

.quick-login-hint-right {
  margin-top: 0;
  background: #ffffff;
  border: 1px solid rgba(148, 163, 184, 0.25);
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
}

.hint-title {
  font-size: 12px;
  color: #1e40af;
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
  background: rgba(219, 234, 254, 0.75);
  border-radius: var(--radius-md);
  font-size: 13px;
  color: #1e3a8a;
  cursor: pointer;
  transition: all var(--transition-fast);
  border: 1px solid rgba(147, 197, 253, 0.45);
}

.hint-account:hover {
  background: rgba(191, 219, 254, 0.95);
  color: #1e3a8a;
  border-color: #60a5fa;
}

@keyframes seedGlow {
  0%, 100% { box-shadow: 0 0 0 0 rgba(250, 204, 21, 0.42); }
  50% { box-shadow: 0 0 0 12px rgba(250, 204, 21, 0); }
}

@keyframes nodeLight {
  0%, 100% { box-shadow: 0 0 0 0 rgba(96, 165, 250, 0.3); }
  50% { box-shadow: 0 0 0 8px rgba(96, 165, 250, 0); }
}

@keyframes rocketRise {
  0%, 100% { transform: translateY(0px); opacity: 0.8; }
  50% { transform: translateY(-14px); opacity: 1; }
}

@keyframes drawLine {
  0% { stroke-dashoffset: 360; }
  45%, 100% { stroke-dashoffset: 0; }
}

@keyframes dotShow {
  0%, 22% { opacity: 0; transform: scale(0.7); }
  40%, 100% { opacity: 1; transform: scale(1); }
}

@keyframes valuePulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.08); }
}

@keyframes barGrow {
  0%, 100% { transform: scaleY(0.72); }
  50% { transform: scaleY(1); }
}

@keyframes checkBlink {
  0%, 100% { opacity: 0.2; }
  50% { opacity: 1; }
}

@keyframes ringRotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes numberRise {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-3px); }
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

@media (max-width: 1360px) {
  .brand-bento {
    grid-template-columns: 1fr;
    grid-template-rows: auto;
  }

  .main-card,
  .timeline-card,
  .trend-card,
  .task-card,
  .energy-card {
    grid-column: auto;
    grid-row: auto;
  }
}
</style>
