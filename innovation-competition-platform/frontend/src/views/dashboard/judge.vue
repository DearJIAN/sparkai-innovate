<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon" style="background: var(--primary-50); color: var(--primary-600);">
            <el-icon size="24"><StarFilled /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">0</div>
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
            <div class="stat-value">0</div>
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
            <div class="stat-value">0</div>
            <div class="stat-label">评审进度</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt-5">
      <el-col :span="24">
        <el-card>
          <template #header>
            <span>待评审项目</span>
          </template>
          <el-empty description="暂无待评审项目" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

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
</style>
