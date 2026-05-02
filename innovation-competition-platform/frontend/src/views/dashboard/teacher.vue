<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon" style="background: var(--primary-50); color: var(--primary-600);">
            <el-icon size="24"><Folder /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.guideProjects }}</div>
            <div class="stat-label">指导项目</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon" style="background: var(--warning-50); color: var(--warning-600);">
            <el-icon size="24"><Clock /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.pendingReview }}</div>
            <div class="stat-label">待审核</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon" style="background: var(--success-50); color: var(--success-600);">
            <el-icon size="24"><User /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.students }}</div>
            <div class="stat-label">学生人数</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt-5">
      <el-col :span="16">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>我的指导项目</span>
              <el-button type="primary" size="small" @click="$router.push('/guide-projects')">
                查看全部
              </el-button>
            </div>
          </template>
          <div v-if="recentProjects.length === 0" class="empty-hint">暂无指导项目</div>
          <div v-else class="project-list">
            <div
              v-for="p in recentProjects"
              :key="p.id"
              class="project-item"
              @click="$router.push(`/projects/${p.id}`)"
            >
              <div class="project-left">
                <span class="project-name">{{ p.name }}</span>
                <el-tag :type="statusType(p.status)" size="small">{{ statusText(p.status) }}</el-tag>
              </div>
              <div class="project-right">
                <span class="project-leader">{{ p.leader || '未知' }}</span>
                <span class="project-time">{{ p.updated_at || '刚刚更新' }}</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card>
          <template #header><span>待审核提醒</span></template>
          <div v-if="pendingItems.length === 0" class="empty-hint">暂无待审核项</div>
          <div v-else class="pending-list">
            <div v-for="item in pendingItems" :key="item.id" class="pending-item">
              <el-icon color="var(--warning-500)"><WarningFilled /></el-icon>
              <span>{{ item.name }} - {{ item.action }}</span>
            </div>
          </div>
        </el-card>

        <el-card class="mt-4">
          <template #header><span>快捷操作</span></template>
          <div class="quick-actions">
            <el-button type="primary" plain @click="$router.push('/guide-projects')">查看所有项目</el-button>
            <el-button type="success" plain @click="$router.push('/training-camps')">推荐训练营</el-button>
            <el-button type="warning" plain @click="openTeacherAgent">AI 助手</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Folder, Clock, User, WarningFilled } from '@element-plus/icons-vue'

const openTeacherAgent = () => {
  window.dispatchEvent(new CustomEvent('open-huahuo-agent', {
    detail: { capability: 'review_assist', source: 'teacher_dashboard' }
  }))
}

const stats = ref({
  guideProjects: 12,
  pendingReview: 3,
  students: 48
})

const recentProjects = ref([
  { id: 1, name: '智慧校园服务平台', status: 'submitted', leader: '张三', updated_at: '2小时前' },
  { id: 2, name: 'AI 辅助学习系统', status: 'teacher_review', leader: '李四', updated_at: '5小时前' },
  { id: 3, name: '绿色物流配送平台', status: 'passed', leader: '王五', updated_at: '1天前' },
  { id: 4, name: '乡村振兴电商助农', status: 'submitted', leader: '赵六', updated_at: '2天前' }
])

const pendingItems = ref([
  { id: 1, name: '智慧校园服务平台', action: '提交了新版本材料' },
  { id: 2, name: 'AI 辅助学习系统', action: '请求审核通过' },
  { id: 3, name: '绿色物流配送平台', action: '新增团队成员' }
])

const statusMap = {
  draft: { text: '草稿', type: 'info' },
  submitted: { text: '已提交', type: 'primary' },
  teacher_review: { text: '审核中', type: 'warning' },
  judging: { text: '评审中', type: 'warning' },
  passed: { text: '已通过', type: 'success' },
  need_modify: { text: '需修改', type: 'danger' },
  rejected: { text: '已驳回', type: 'danger' }
}

const statusText = (s) => statusMap[s]?.text || s
const statusType = (s) => statusMap[s]?.type || 'info'
</script>

<style scoped>
.stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1;
}

.stat-label {
  font-size: 14px;
  color: var(--text-secondary);
  margin-top: 4px;
}

.mt-5 { margin-top: 20px; }
.mt-4 { margin-top: 16px; }

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.project-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.project-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 14px;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s;
}

.project-item:hover {
  background: var(--primary-50);
}

.project-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.project-name {
  font-weight: 600;
  font-size: 14px;
  color: var(--text-primary);
}

.project-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 2px;
}

.project-leader {
  font-size: 13px;
  color: var(--text-secondary);
}

.project-time {
  font-size: 12px;
  color: var(--text-tertiary);
}

.empty-hint {
  text-align: center;
  color: var(--text-tertiary);
  padding: 24px 0;
  font-size: 13px;
}

.pending-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.pending-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  background: var(--warning-50);
  border-radius: var(--radius-md);
  font-size: 13px;
  color: var(--text-primary);
}

.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
