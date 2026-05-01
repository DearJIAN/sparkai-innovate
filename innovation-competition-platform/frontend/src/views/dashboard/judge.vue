<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon" style="background: var(--warning-50); color: var(--warning-600);">
            <el-icon size="24"><StarFilled /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.pending }}</div>
            <div class="stat-label">待评审</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon" style="background: var(--success-50); color: var(--success-600);">
            <el-icon size="24"><DocumentChecked /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.completed }}</div>
            <div class="stat-label">已评审</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon" style="background: var(--info-50); color: var(--info-600);">
            <el-icon size="24"><Odometer /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.progress }}%</div>
            <div class="stat-label">评审进度</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt-5">
      <el-col :span="16">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>待评审项目</span>
              <el-button type="primary" size="small" @click="$router.push('/pending-reviews')">查看全部</el-button>
            </div>
          </template>
          <div v-if="pendingProjects.length === 0" class="empty-hint">暂无待评审项目</div>
          <div v-else class="project-list">
            <div
              v-for="p in pendingProjects"
              :key="p.id"
              class="project-item"
              @click="$router.push(`/reviews/${p.id}`)"
            >
              <div class="project-main">
                <span class="project-name">{{ p.name }}</span>
                <div class="project-meta">
                  <el-tag :type="statusType(p.status)" size="small">{{ statusText(p.status) }}</el-tag>
                  <span>{{ p.category || '-' }}</span>
                  <span>{{ p.track || '-' }}</span>
                </div>
                <p class="project-desc">{{ p.description || '暂无描述' }}</p>
              </div>
              <div class="project-action">
                <el-button type="primary" size="small" @click.stop="$router.push(`/reviews/${p.id}`)">
                  开始评审
                </el-button>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card>
          <template #header><span>评分分布</span></template>
          <div class="score-dist">
            <div v-for="item in scoreDistribution" :key="item.label" class="dist-item">
              <span class="dist-label">{{ item.label }}</span>
              <div class="dist-bar-bg">
                <div class="dist-bar-fill" :style="{ width: item.percent + '%', background: item.color }"></div>
              </div>
              <span class="dist-count">{{ item.count }}</span>
            </div>
          </div>
        </el-card>

        <el-card class="mt-4">
          <template #header><span>快捷操作</span></template>
          <div class="quick-actions">
            <el-button type="primary" plain @click="$router.push('/pending-reviews')">待评审列表</el-button>
            <el-button type="success" plain @click="$router.push('/ai-assistant')">AI 辅助分析</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { StarFilled, DocumentChecked, Odometer } from '@element-plus/icons-vue'

const stats = ref({
  pending: 8,
  completed: 15,
  progress: 65
})

const pendingProjects = ref([
  { id: 1, name: '智慧校园服务平台', description: '基于物联网技术的校园综合服务平台，整合教务、生活、社交等多场景...', status: 'judging', category: '信息技术', track: '主赛道' },
  { id: 2, name: 'AI 辅助学习系统', description: '利用大语言模型技术为学生提供个性化学习方案和智能答疑功能...', status: 'judging', category: '人工智能', track: '人工智能赛道' },
  { id: 3, name: '绿色物流配送平台', description: '面向城市末端物流的绿色配送解决方案，优化路径规划降低碳排放...', status: 'judging', category: '绿色科技', track: '主赛道' },
  { id: 4, name: '乡村振兴电商助农', description: '连接农村生产者和城市消费者的电商平台，帮助农产品上行...', status: 'submitted', category: '乡村振兴', track: '红旅专项' }
])

const scoreDistribution = ref([
  { label: '90-100分', count: 3, percent: 20, color: '#67C23A' },
  { label: '80-89分', count: 5, percent: 33, color: '#409EFF' },
  { label: '70-79分', count: 4, percent: 27, color: '#E6A23C' },
  { label: '60-69分', count: 2, percent: 13, color: '#F56C6C' },
  { label: '<60分', count: 1, percent: 7, color: '#909399' }
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
  gap: 12px;
}

.project-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid transparent;
}

.project-item:hover {
  background: var(--primary-50);
  border-color: var(--primary-200);
}

.project-main {
  flex: 1;
  min-width: 0;
}

.project-name {
  font-weight: 600;
  font-size: 15px;
  color: var(--text-primary);
  display: block;
  margin-bottom: 6px;
}

.project-meta {
  display: flex;
  gap: 10px;
  align-items: center;
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 6px;
}

.project-desc {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.project-action {
  flex-shrink: 0;
  margin-left: 16px;
}

.empty-hint {
  text-align: center;
  color: var(--text-tertiary);
  padding: 32px 0;
  font-size: 13px;
}

.score-dist {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.dist-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
}

.dist-label {
  width: 70px;
  flex-shrink: 0;
  color: var(--text-secondary);
}

.dist-bar-bg {
  flex: 1;
  height: 8px;
  background: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
}

.dist-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
}

.dist-count {
  width: 30px;
  text-align: right;
  color: var(--text-secondary);
  font-weight: 600;
}

.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
