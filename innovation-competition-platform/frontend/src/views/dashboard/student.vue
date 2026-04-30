<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon" style="background: var(--primary-50); color: var(--primary-600);">
            <el-icon size="24"><FolderOpened /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">0</div>
            <div class="stat-label">我的项目</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon" style="background: var(--warning-50); color: var(--warning-600);">
            <el-icon size="24"><Timer /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">0</div>
            <div class="stat-label">待办任务</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon" style="background: var(--success-50); color: var(--success-600);">
            <el-icon size="24"><Star /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">-</div>
            <div class="stat-label">评审得分</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt-5">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>最近项目</span>
          </template>
          <el-empty description="暂无项目，快去创建吧" />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>待办任务</span>
          </template>
          <el-empty description="暂无待办任务" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { FolderOpened, Timer, Star } from '@element-plus/icons-vue'
</script>

<style scoped>
.dashboard {
  padding-bottom: 20px;
}

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
</style>
