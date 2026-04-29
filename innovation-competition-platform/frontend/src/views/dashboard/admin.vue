<template>
  <div class="page-container">
    <h2 class="page-title">管理员数据看板</h2>

    <div v-loading="loading">
      <!-- 核心统计卡片 -->
      <el-row :gutter="16" class="stats-row">
        <el-col :span="4">
          <div class="stat-card" style="--stat-color: var(--primary-500)">
            <el-icon size="24"><User /></el-icon>
            <div class="stat-value">{{ stats.users?.total || 0 }}</div>
            <div class="stat-label">注册用户</div>
          </div>
        </el-col>
        <el-col :span="4">
          <div class="stat-card" style="--stat-color: var(--success-500)">
            <el-icon size="24"><Folder /></el-icon>
            <div class="stat-value">{{ stats.projects?.total || 0 }}</div>
            <div class="stat-label">项目总数</div>
          </div>
        </el-col>
        <el-col :span="4">
          <div class="stat-card" style="--stat-color: var(--warning-500)">
            <el-icon size="24"><Document /></el-icon>
            <div class="stat-value">{{ stats.projects?.submitted || 0 }}</div>
            <div class="stat-label">待评审</div>
          </div>
        </el-col>
        <el-col :span="4">
          <div class="stat-card" style="--stat-color: var(--info-500)">
            <el-icon size="24"><Star /></el-icon>
            <div class="stat-value">{{ stats.reviews || 0 }}</div>
            <div class="stat-label">评审次数</div>
          </div>
        </el-col>
        <el-col :span="4">
          <div class="stat-card" style="--stat-color: var(--primary-600)">
            <el-icon size="24"><Files /></el-icon>
            <div class="stat-value">{{ stats.files || 0 }}</div>
            <div class="stat-label">上传文件</div>
          </div>
        </el-col>
        <el-col :span="4">
          <div class="stat-card" style="--stat-color: var(--danger-500)">
            <el-icon size="24"><MagicStick /></el-icon>
            <div class="stat-value">{{ stats.ai_records || 0 }}</div>
            <div class="stat-label">AI 调用</div>
          </div>
        </el-col>
      </el-row>

      <!-- 图表区域 -->
      <el-row :gutter="16" class="charts-row">
        <el-col :span="12">
          <el-card shadow="never">
            <template #header><span>项目状态分布</span></template>
            <div ref="statusChartRef" class="chart-container"></div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card shadow="never">
            <template #header><span>用户角色分布</span></template>
            <div ref="roleChartRef" class="chart-container"></div>
          </el-card>
        </el-col>
      </el-row>

      <el-row :gutter="16" class="charts-row">
        <el-col :span="12">
          <el-card shadow="never">
            <template #header><span>项目阶段分布</span></template>
            <div ref="stageChartRef" class="chart-container"></div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card shadow="never">
            <template #header><span>项目赛道分布</span></template>
            <div ref="trackChartRef" class="chart-container"></div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 最近活动 -->
      <el-row :gutter="16" class="recent-row">
        <el-col :span="8">
          <el-card shadow="never">
            <template #header><span>最近创建的项目</span></template>
            <el-empty v-if="!recent.projects?.length" description="暂无数据" :image-size="60" />
            <div v-else class="recent-list">
              <div v-for="item in recent.projects" :key="item.id" class="recent-item">
                <el-icon size="16" color="var(--primary-500)"><Folder /></el-icon>
                <span class="recent-name">{{ item.name }}</span>
                <span class="recent-time">{{ formatDate(item.created_at) }}</span>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card shadow="never">
            <template #header><span>最近上传的文件</span></template>
            <el-empty v-if="!recent.files?.length" description="暂无数据" :image-size="60" />
            <div v-else class="recent-list">
              <div v-for="item in recent.files" :key="item.id" class="recent-item">
                <el-icon size="16" color="var(--success-500)"><Document /></el-icon>
                <span class="recent-name">{{ item.original_name }}</span>
                <span class="recent-time">{{ formatDate(item.created_at) }}</span>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card shadow="never">
            <template #header><span>最近评审</span></template>
            <el-empty v-if="!recent.reviews?.length" description="暂无数据" :image-size="60" />
            <div v-else class="recent-list">
              <div v-for="item in recent.reviews" :key="item.id" class="recent-item">
                <el-icon size="16" color="var(--warning-500)"><Star /></el-icon>
                <span class="recent-name">{{ item.project_name }} {{ item.total_score }}分</span>
                <span class="recent-time">{{ formatDate(item.created_at) }}</span>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { User, Folder, Document, Star, Files, MagicStick } from '@element-plus/icons-vue'
import { getDashboardStats, getRecentData } from '@/api/dashboard'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const stats = ref({})
const recent = ref({})

const statusChartRef = ref(null)
const roleChartRef = ref(null)
const stageChartRef = ref(null)
const trackChartRef = ref(null)

let echarts = null

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

const initCharts = async () => {
  if (!echarts) {
    echarts = await import('echarts')
  }

  await nextTick()

  // 项目状态分布饼图
  if (statusChartRef.value) {
    const statusChart = echarts.init(statusChartRef.value)
    const projectStats = stats.value.projects || {}
    statusChart.setOption({
      tooltip: { trigger: 'item' },
      legend: { bottom: 0 },
      series: [{
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: { borderRadius: 8, borderColor: '#fff', borderWidth: 2 },
        label: { show: false },
        emphasis: { label: { show: true, fontSize: 14, fontWeight: 'bold' } },
        data: [
          { value: projectStats.draft || 0, name: '草稿', itemStyle: { color: '#909399' } },
          { value: projectStats.submitted || 0, name: '待评审', itemStyle: { color: '#E6A23C' } },
          { value: projectStats.passed || 0, name: '已通过', itemStyle: { color: '#67C23A' } },
          { value: projectStats.rejected || 0, name: '已驳回', itemStyle: { color: '#F56C6C' } },
          { value: projectStats.need_modify || 0, name: '需修改', itemStyle: { color: '#409EFF' } }
        ]
      }]
    })
  }

  // 用户角色分布饼图
  if (roleChartRef.value) {
    const roleChart = echarts.init(roleChartRef.value)
    const roleStats = stats.value.users?.by_role || {}
    roleChart.setOption({
      tooltip: { trigger: 'item' },
      legend: { bottom: 0 },
      series: [{
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: { borderRadius: 8, borderColor: '#fff', borderWidth: 2 },
        label: { show: false },
        emphasis: { label: { show: true, fontSize: 14, fontWeight: 'bold' } },
        data: [
          { value: roleStats.student || 0, name: '学生', itemStyle: { color: '#409EFF' } },
          { value: roleStats.teacher || 0, name: '教师', itemStyle: { color: '#67C23A' } },
          { value: roleStats.judge || 0, name: '评委', itemStyle: { color: '#E6A23C' } },
          { value: roleStats.admin || 0, name: '管理员', itemStyle: { color: '#F56C6C' } }
        ]
      }]
    })
  }

  // 项目阶段分布柱状图
  if (stageChartRef.value) {
    const stageChart = echarts.init(stageChartRef.value)
    const stageData = stats.value.projects?.by_stage || {}
    const stageNames = {
      idea: '创意阶段', proof: '验证阶段', resource: '资源整合',
      development: '产品开发', market: '市场推广', roadshow: '路演展示', incubation: '孵化运营'
    }
    stageChart.setOption({
      tooltip: { trigger: 'axis' },
      xAxis: {
        type: 'category',
        data: Object.keys(stageData).map(k => stageNames[k] || k),
        axisLabel: { rotate: 30 }
      },
      yAxis: { type: 'value' },
      series: [{
        data: Object.values(stageData),
        type: 'bar',
        itemStyle: { color: '#409EFF', borderRadius: [4, 4, 0, 0] }
      }]
    })
  }

  // 项目赛道分布柱状图
  if (trackChartRef.value) {
    const trackChart = echarts.init(trackChartRef.value)
    const trackData = stats.value.projects?.by_track || {}
    trackChart.setOption({
      tooltip: { trigger: 'axis' },
      xAxis: {
        type: 'category',
        data: Object.keys(trackData),
        axisLabel: { rotate: 30 }
      },
      yAxis: { type: 'value' },
      series: [{
        data: Object.values(trackData),
        type: 'bar',
        itemStyle: { color: '#67C23A', borderRadius: [4, 4, 0, 0] }
      }]
    })
  }
}

const fetchData = async () => {
  loading.value = true
  try {
    const [statsRes, recentRes] = await Promise.all([
      getDashboardStats(),
      getRecentData()
    ])

    if (statsRes.code === 200) {
      stats.value = statsRes.data || {}
    }
    if (recentRes.code === 200) {
      recent.value = recentRes.data || {}
    }

    await initCharts()
  } catch (error) {
    ElMessage.error('获取数据失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.page-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 24px;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  --stat-color: var(--text-primary);
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 20px;
  text-align: center;
  transition: all var(--transition-fast);
}

.stat-card:hover {
  border-color: var(--stat-color);
  box-shadow: var(--shadow-sm);
}

.stat-card .el-icon {
  color: var(--stat-color);
  margin-bottom: 8px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--stat-color);
  line-height: 1;
  margin-bottom: 6px;
}

.stat-label {
  font-size: 13px;
  color: var(--text-secondary);
}

.charts-row {
  margin-bottom: 16px;
}

.chart-container {
  width: 100%;
  height: 280px;
}

.recent-row {
  margin-bottom: 20px;
}

.recent-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.recent-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
}

.recent-name {
  flex: 1;
  font-size: 13px;
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.recent-time {
  font-size: 12px;
  color: var(--text-tertiary);
  flex-shrink: 0;
}
</style>
