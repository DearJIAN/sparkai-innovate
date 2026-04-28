<template>
  <div class="dashboard">
    <h2 class="page-title">数据看板</h2>
    
    <el-row :gutter="20" class="stat-cards">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-icon" style="background: #e6f7ff; color: #1890ff;">
            <el-icon size="24"><FolderOpened /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">0</div>
            <div class="stat-label">项目总数</div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-icon" style="background: #f6ffed; color: #52c41a;">
            <el-icon size="24"><User /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">0</div>
            <div class="stat-label">用户总数</div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-icon" style="background: #fff7e6; color: #fa8c16;">
            <el-icon size="24"><Star /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">0</div>
            <div class="stat-label">待评审</div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-icon" style="background: #f9f0ff; color: #722ed1;">
            <el-icon size="24"><Check /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">0</div>
            <div class="stat-label">已完成评审</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" class="charts-row">
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
            <span>项目类别分布</span>
          </template>
          <div ref="categoryChart" class="chart-container"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'

const trendChart = ref()
const categoryChart = ref()

onMounted(() => {
  const trend = echarts.init(trendChart.value)
  trend.setOption({
    xAxis: { type: 'category', data: ['1月', '2月', '3月', '4月', '5月', '6月'] },
    yAxis: { type: 'value' },
    series: [{ data: [0, 0, 0, 0, 0, 0], type: 'line', smooth: true }]
  })
  
  const category = echarts.init(categoryChart.value)
  category.setOption({
    series: [{
      type: 'pie',
      data: [
        { value: 0, name: '科技创新' },
        { value: 0, name: '社会服务' },
        { value: 0, name: '文化创意' },
        { value: 0, name: '其他' }
      ]
    }]
  })
})
</script>

<style scoped>
.dashboard {
  padding-bottom: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #1a1a2e;
  margin-bottom: 24px;
}

.stat-cards {
  margin-bottom: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #1a1a2e;
}

.stat-label {
  font-size: 14px;
  color: #999;
  margin-top: 4px;
}

.charts-row {
  margin-top: 20px;
}

.chart-container {
  height: 300px;
}
</style>
