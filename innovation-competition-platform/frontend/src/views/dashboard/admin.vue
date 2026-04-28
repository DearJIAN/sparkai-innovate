<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon" style="background: var(--primary-50); color: var(--primary-600);">
            <el-icon size="24"><FolderOpened /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">0</div>
            <div class="stat-label">项目总数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon" style="background: var(--success-50); color: var(--success-600);">
            <el-icon size="24"><User /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">0</div>
            <div class="stat-label">用户总数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon" style="background: var(--warning-50); color: var(--warning-600);">
            <el-icon size="24"><Star /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">0</div>
            <div class="stat-label">待评审</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon" style="background: var(--info-50); color: var(--info-600);">
            <el-icon size="24"><Trophy /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">0</div>
            <div class="stat-label">比赛批次</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt-5">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>项目趋势</span>
          </template>
          <div ref="trendChart" class="chart-container"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>用户分布</span>
          </template>
          <div ref="userChart" class="chart-container"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'

const trendChart = ref()
const userChart = ref()

onMounted(() => {
  const trend = echarts.init(trendChart.value)
  trend.setOption({
    xAxis: { type: 'category', data: ['1月', '2月', '3月', '4月', '5月', '6月'] },
    yAxis: { type: 'value' },
    series: [{ data: [0, 0, 0, 0, 0, 0], type: 'line', smooth: true, areaStyle: {} }]
  })

  const user = echarts.init(userChart.value)
  user.setOption({
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      data: [
        { value: 0, name: '学生' },
        { value: 0, name: '教师' },
        { value: 0, name: '评委' },
        { value: 0, name: '管理员' }
      ]
    }]
  })
})
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

.mt-5 {
  margin-top: 20px;
}

.chart-container {
  height: 300px;
}
</style>
