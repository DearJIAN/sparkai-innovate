<template>
  <div class="test-button-demo">
    <h3 class="demo-title">TestButton 组件演示</h3>
    <p class="demo-desc">基于 ui-ux-pro-max 设计系统 (Exaggerated Minimalism + Indigo Palette)</p>

    <div class="demo-group">
      <h4 class="group-label">Primary Variants</h4>
      <div class="demo-row">
        <TestButton variant="primary" @click="handleClick">立即报名</TestButton>
        <TestButton variant="primary" size="large" @click="handleClick">提交项目</TestButton>
        <TestButton variant="primary" size="small" @click="handleClick">确认</TestButton>
        <TestButton variant="primary" :loading="true">加载中...</TestButton>
        <TestButton variant="primary" disabled>已截止</TestButton>
      </div>
    </div>

    <div class="demo-group">
      <h4 class="group-label">Secondary & Outline</h4>
      <div class="demo-row">
        <TestButton variant="secondary" @click="handleClick">查看详情</TestButton>
        <TestButton variant="outline" @click="handleClick">了解更多</TestButton>
        <TestButton variant="ghost" @click="handleClick">取消操作</TestButton>
      </div>
    </div>

    <div class="demo-group">
      <h4 class="group-label">Accent / CTA</h4>
      <div class="demo-row">
        <TestButton variant="accent" @click="handleClick">
          <template #icon><el-icon><Star /></el-icon></template>
          收藏竞赛
        </TestButton>
        <TestButton variant="accent" gradient @click="handleClick">
          <template #icon><el-icon><Trophy /></el-icon></template>
          立即参赛
        </TestButton>
      </div>
    </div>

    <div class="demo-group">
      <h4 class="group-label">Icon Only</h4>
      <div class="demo-row">
        <TestButton variant="ghost" icon-only circle @click="handleClick">
          <template #icon><el-icon size="18"><Plus /></el-icon></template>
        </TestButton>
        <TestButton variant="primary" icon-only circle @click="handleClick">
          <template #icon><el-icon size="18"><Search /></el-icon></template>
        </TestButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import TestButton from './TestButton.vue'
import { Star, Trophy, Plus, Search } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const handleClick = () => {
  ElMessage.success('按钮点击触发成功')
}
</script>

<style scoped>
.test-button-demo {
  padding: 40px;
  max-width: 800px;
  margin: 0 auto;
}

.demo-title {
  font-family: 'Baloo 2', cursive;
  font-size: clamp(1.8rem, 4vw, 2.8rem);
  font-weight: 700;
  color: #312E81;
  letter-spacing: -0.03em;
  margin-bottom: 4px;
}

.demo-desc {
  font-size: 14px;
  color: #6366F1;
  margin-bottom: 36px;
  letter-spacing: 0.02em;
}

.demo-group {
  margin-bottom: 32px;
  padding: 24px;
  background: linear-gradient(135deg, #EEF2FF 0%, #F5F3FF 100%);
  border-radius: 16px;
  border: 1px solid rgba(99, 102, 241, 0.12);
}

.group-label {
  font-family: 'Baloo 2', cursive;
  font-size: 15px;
  font-weight: 600;
  color: #4F46E5;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 16px;
}

.demo-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
}
</style>
