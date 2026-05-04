<template>
  <div class="spark-logo" :class="{ 'small': size === 'small', 'large': size === 'large' }">
    <div class="logo-icon">
      <el-icon :size="iconSize" class="trophy-icon">
        <Trophy />
      </el-icon>
      <div class="spark-pulse"></div>
    </div>
    <div class="logo-text-container">
      <span class="text-chinese">火花智创</span>
      <span class="text-english">SparkAI</span>
      <div class="spark-particles">
        <span v-for="n in 8" :key="n" class="particle" :style="particleStyle(n)"></span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Trophy } from '@element-plus/icons-vue'

const props = defineProps({
  size: {
    type: String,
    default: 'normal',
    validator: (value) => ['small', 'normal', 'large'].includes(value)
  }
})

const iconSize = computed(() => {
  const sizes = { small: 22, normal: 30, large: 52 }
  return sizes[props.size] || 30
})

const particleStyle = (n) => {
  const left = ((n - 1) / 8) * 100
  const delay = n * 0.2
  const duration = 1.5 + Math.random() * 1
  return {
    left: `${left}%`,
    animationDelay: `${delay}s`,
    animationDuration: `${duration}s`
  }
}
</script>

<style scoped>
.spark-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  user-select: none;
  cursor: pointer;
}

/* ===== Logo 图标区域 ===== */
.logo-icon {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: v-bind('iconSize + 8 + "px"');
  height: v-bind('iconSize + 8 + "px"');
  flex-shrink: 0;
}

.trophy-icon {
  color: #f59e0b;
  z-index: 2;
  animation: trophyFloat 3s ease-in-out infinite;
}

@keyframes trophyFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-3px); }
}

/* 脉冲光晕 */
.spark-pulse {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(245, 158, 11, 0.4) 0%, rgba(239, 68, 68, 0.2) 40%, transparent 70%);
  animation: pulseGlow 2s ease-in-out infinite;
  z-index: 1;
}

@keyframes pulseGlow {
  0%, 100% {
    opacity: 0.5;
    transform: translate(-50%, -50%) scale(0.8);
  }
  50% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1.3);
  }
}

/* ===== 文字区域 - 彩色渐变 ===== */
.logo-text-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  line-height: 1.2;
  position: relative;
}

.text-chinese {
  font-size: 17px;
  font-weight: 800;
  letter-spacing: 2px;
  background: linear-gradient(135deg, #ef4444 0%, #f97316 25%, #f59e0b 50%, #ec4899 75%, #8b5cf6 100%);
  background-size: 200% 200%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: gradientShift 3s ease infinite, textGlow 2s ease-in-out infinite alternate;
  white-space: nowrap;
}

.text-english {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  background: linear-gradient(90deg, #f59e0b, #ef4444, #ec4899);
  background-size: 200% 100%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: gradientFlow 2s linear infinite;
  white-space: nowrap;
}

@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

@keyframes gradientFlow {
  0% { background-position: 0% 50%; }
  100% { background-position: 200% 50%; }
}

@keyframes textGlow {
  from {
    filter: drop-shadow(0 0 2px rgba(245, 158, 11, 0.3));
  }
  to {
    filter: drop-shadow(0 0 8px rgba(245, 158, 11, 0.6)) drop-shadow(0 0 16px rgba(239, 68, 68, 0.3));
  }
}

/* ===== 粒子效果 - 在文字下方 ===== */
.spark-particles {
  position: absolute;
  bottom: -6px;
  left: 0;
  width: 100%;
  height: 3px;
  overflow: visible;
}

.particle {
  position: absolute;
  width: 3px;
  height: 3px;
  border-radius: 50%;
  bottom: 0;
  animation: particleFloat 2s ease-in-out infinite;
  opacity: 0;
}

.particle:nth-child(1) { background: #ef4444; }
.particle:nth-child(2) { background: #f97316; }
.particle:nth-child(3) { background: #f59e0b; }
.particle:nth-child(4) { background: #eab308; }
.particle:nth-child(5) { background: #ec4899; }
.particle:nth-child(6) { background: #8b5cf6; }
.particle:nth-child(7) { background: #3b82f6; }
.particle:nth-child(8) { background: #06b6d4; }

@keyframes particleFloat {
  0% {
    opacity: 0;
    transform: translateY(0) scale(0.5);
  }
  20% {
    opacity: 1;
    transform: translateY(-4px) scale(1);
  }
  60% {
    opacity: 0.8;
    transform: translateY(-8px) scale(0.8);
  }
  100% {
    opacity: 0;
    transform: translateY(-12px) scale(0);
  }
}

/* ===== 悬停效果 ===== */
.spark-logo:hover .spark-pulse {
  animation: pulseGlowFast 0.8s ease-in-out infinite;
  background: radial-gradient(circle, rgba(245, 158, 11, 0.6) 0%, rgba(239, 68, 68, 0.4) 40%, transparent 70%);
}

.spark-logo:hover .particle {
  animation-duration: 1s;
}

.spark-logo:hover .text-chinese {
  animation: gradientShift 1s ease infinite, textGlowBright 0.5s ease-in-out infinite alternate;
}

@keyframes pulseGlowFast {
  0%, 100% {
    opacity: 0.8;
    transform: translate(-50%, -50%) scale(1);
  }
  50% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1.5);
  }
}

@keyframes textGlowBright {
  from {
    filter: drop-shadow(0 0 4px rgba(245, 158, 11, 0.5));
  }
  to {
    filter: drop-shadow(0 0 12px rgba(245, 158, 11, 0.8)) drop-shadow(0 0 24px rgba(239, 68, 68, 0.5));
  }
}

/* ===== 尺寸变体 ===== */
.spark-logo.small {
  gap: 6px;
}

.spark-logo.small .text-chinese {
  font-size: 13px;
  letter-spacing: 1px;
}

.spark-logo.small .text-english {
  font-size: 9px;
  letter-spacing: 1px;
}

.spark-logo.small .spark-particles {
  bottom: -4px;
  height: 2px;
}

.spark-logo.small .particle {
  width: 2px;
  height: 2px;
}

.spark-logo.large {
  gap: 14px;
}

.spark-logo.large .text-chinese {
  font-size: 32px;
  letter-spacing: 4px;
}

.spark-logo.large .text-english {
  font-size: 18px;
  letter-spacing: 2px;
}

.spark-logo.large .logo-icon {
  width: 64px;
  height: 64px;
}

.spark-logo.large .spark-particles {
  bottom: -8px;
  height: 4px;
}

.spark-logo.large .particle {
  width: 4px;
  height: 4px;
}

/* ===== 减少动画支持 ===== */
@media (prefers-reduced-motion: reduce) {
  .trophy-icon,
  .spark-pulse,
  .particle,
  .text-chinese,
  .text-english {
    animation: none;
  }
  .text-chinese,
  .text-english {
    background-position: 0% 50%;
  }
}
</style>
