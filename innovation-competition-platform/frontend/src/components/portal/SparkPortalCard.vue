<template>
  <div
    class="spark-card"
    :class="{ 'spark-card--clickable': clickable }"
    @click="clickable && onCardClick && onCardClick()"
  >
    <div class="spark-card__cover">
      <img
        v-if="coverImage"
        class="spark-card__cover-image"
        :src="coverImage"
        :alt="title || '卡片封面图'"
        loading="lazy"
      />
      <div v-if="level || status" class="spark-card__badge">
        {{ level || status }}
      </div>
      <div v-if="!coverImage" class="spark-card__cover-placeholder" :style="{ background: gradient }">
        <div class="cover-placeholder-pattern"></div>
      </div>
    </div>
    <div class="spark-card__body">
      <div v-if="tags && tags.length" class="spark-card__tags">
        <span
          v-for="tag in visibleTags"
          :key="tag"
          class="spark-card__tag"
        >{{ tag }}</span>
        <span v-if="tags.length > maxTags" class="spark-card__tag spark-card__tag--more">
          +{{ tags.length - maxTags }}
        </span>
      </div>
      <h3 v-if="title" class="spark-card__title">{{ title }}</h3>
      <p v-if="description" class="spark-card__desc">{{ description }}</p>
      <div v-if="metaItems && metaItems.length" class="spark-card__meta">
        <div v-for="(item, idx) in metaItems" :key="idx" class="spark-card__meta-item">
          <el-icon v-if="item.icon" size="14"><component :is="item.icon" /></el-icon>
          <span>{{ item.text }}</span>
        </div>
      </div>
      <div v-if="primaryActionText || secondaryActionText" class="spark-card__actions">
        <el-button
          v-if="primaryActionText"
          type="primary"
          size="default"
          class="spark-card__btn-primary"
          @click.stop="onPrimaryClick && onPrimaryClick()"
        >
          {{ primaryActionText }}
          <el-icon v-if="primaryActionIcon"><component :is="primaryActionIcon" /></el-icon>
        </el-button>
        <el-button
          v-if="secondaryActionText"
          size="default"
          class="spark-card__btn-secondary"
          @click.stop="onSecondaryClick && onSecondaryClick()"
        >
          <el-icon v-if="secondaryActionIcon"><component :is="secondaryActionIcon" /></el-icon>
          {{ secondaryActionText }}
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  gradient: { type: String, default: 'linear-gradient(135deg, #2563eb 0%, #7c3aed 100%)' },
  coverImage: { type: String, default: '' },
  coverTitle: { type: String, default: '' },
  level: { type: String, default: '' },
  status: { type: String, default: '' },
  title: { type: String, default: '' },
  description: { type: String, default: '' },
  tags: { type: Array, default: () => [] },
  maxTags: { type: Number, default: 3 },
  metaItems: { type: Array, default: () => [] },
  primaryActionText: { type: String, default: '' },
  primaryActionIcon: { type: Object, default: null },
  secondaryActionText: { type: String, default: '' },
  secondaryActionIcon: { type: Object, default: null },
  clickable: { type: Boolean, default: true },
  onCardClick: { type: Function, default: null },
  onPrimaryClick: { type: Function, default: null },
  onSecondaryClick: { type: Function, default: null }
})

const visibleTags = computed(() => props.tags.slice(0, props.maxTags))
</script>

<style scoped>
.spark-card {
  background: #ffffff;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 12px 32px rgba(15, 23, 42, 0.08);
  transition: transform 0.35s cubic-bezier(0.4, 0, 0.2, 1),
              box-shadow 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
}

.spark-card--clickable {
  cursor: pointer;
}

.spark-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 32px -8px rgba(0, 0, 0, 0.12), 0 4px 12px -2px rgba(0, 0, 0, 0.06);
}

.spark-card__cover {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  overflow: hidden;
  border-radius: 20px 20px 0 0;
  padding: 0;
  border: none;
  background: transparent;
}

.spark-card__cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  border-radius: 0;
  transition: transform 0.55s cubic-bezier(0.16, 1, 0.3, 1);
}

.spark-card:hover .spark-card__cover-image {
  transform: scale(1.03);
}

.spark-card__badge {
  position: absolute;
  top: 16px;
  right: 16px;
  padding: 4px 12px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(8px);
  color: #ffffff;
  font-size: 12px;
  font-weight: 600;
  border: 1px solid rgba(255, 255, 255, 0.25);
  z-index: 1;
}

.spark-card__cover-placeholder {
  position: absolute;
  inset: 0;
  background-size: 300% 300%;
  animation: sparkGradientFlow 8s ease infinite;
}

.cover-placeholder-pattern {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image:
    radial-gradient(circle at 30% 40%, rgba(255,255,255,0.1) 0%, transparent 50%),
    radial-gradient(circle at 70% 60%, rgba(255,255,255,0.06) 0%, transparent 50%);
}

.spark-card__body {
  padding: 20px 24px 24px;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.spark-card__tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  margin-bottom: 12px;
}

.spark-card__tag {
  padding: 3px 10px;
  border-radius: 8px;
  background: #f1f5f9;
  color: #475569;
  font-size: 11px;
  font-weight: 500;
}

.spark-card__tag--more {
  background: #e2e8f0;
  color: #64748b;
}

.spark-card__title {
  font-size: 17px;
  font-weight: 600;
  color: #0f172a;
  margin-bottom: 8px;
  line-height: 1.5;
}

.spark-card__desc {
  font-size: 13px;
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 14px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex-shrink: 0;
}

.spark-card__meta {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-top: auto;
  margin-bottom: 18px;
}

.spark-card__meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #64748b;
}

.spark-card__meta-item .el-icon {
  color: #94a3b8;
  flex-shrink: 0;
}

.spark-card__actions {
  display: flex;
  gap: 10px;
  margin-top: auto;
}

.spark-card__btn-primary {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  border: none;
  color: #fff;
  border-radius: 12px;
  font-weight: 500;
  padding: 10px 20px;
  transition: all 0.3s ease;
}

.spark-card__btn-primary:hover {
  background: linear-gradient(135deg, #1d4ed8, #6d28d9);
  box-shadow: 0 6px 18px rgba(37, 99, 235, 0.3);
  transform: translateY(-1px);
}

.spark-card__btn-secondary {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  color: #475569;
  border-radius: 12px;
  font-weight: 500;
  padding: 10px 18px;
  transition: all 0.3s ease;
}

.spark-card__btn-secondary:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
  color: #0f172a;
}

@keyframes sparkGradientFlow {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

@media (prefers-reduced-motion: reduce) {
  .spark-card {
    transition: none;
  }
  .spark-card__cover,
  .spark-card__cover-image {
    animation: none !important;
    transition: none !important;
  }
}
</style>