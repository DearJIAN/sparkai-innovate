<template>
  <div class="assessment-page">
    <div class="assessment-banner">
      <div class="banner-bg"></div>
      <div class="banner-content">
        <h1 class="banner-title">在线测评中心</h1>
        <p class="banner-subtitle">探索创业潜能、团队协作与职业发展画像</p>
      </div>
    </div>

    <div class="assessment-layout">
      <aside class="sidebar">
        <div class="sidebar-title">测评分类</div>
        <div
          v-for="cat in categories"
          :key="cat.key"
          class="sidebar-item"
          :class="{ active: activeCategory === cat.key }"
          @click="selectCategory(cat.key)"
        >
          <span class="sidebar-label">{{ cat.name }}</span>
          <span class="sidebar-count">{{ getCategoryCount(cat.key) }}</span>
        </div>
      </aside>

      <div class="main-area">
        <div class="main-header">
          <h2 class="main-title">{{ currentCategoryName }}</h2>
          <div class="main-search">
            <el-input
              v-model="searchKeyword"
              placeholder="搜索测评名称、描述或标签..."
              clearable
              size="large"
              class="search-input"
              @input="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </div>
        </div>

        <div v-if="filteredList.length === 0" class="empty-state">
          <el-icon size="64"><Search /></el-icon>
          <p>没有找到匹配的测评</p>
          <span>试试其他关键词或切换分类</span>
        </div>

        <TransitionGroup name="card-list" tag="div" class="assessment-grid">
          <div
            v-for="item in filteredList"
            :key="item.id"
            class="assessment-card"
            :class="[`theme-${item.id}`]"
            @click="handleStart(item)"
          >
            <div class="card-cover" :style="coverStyle(item)">
              <div class="card-cover-bg-deco" :style="getBgDeco(item)"></div>
              <component :is="getSvgComponent(item)" :accent-color="getAccentColor(item)" />
              <div class="cover-tag" :style="{ background: getTheme(item).accentColor + '22', color: getTheme(item).accentColor, borderColor: getTheme(item).accentColor + '44' }">{{ getThemeLabel(item) }}</div>
              <div class="cover-sub" :style="{ color: getTheme(item).accentColor }">{{ getThemeSubtitle(item) }}</div>
            </div>
            <div class="card-body">
              <h3 class="card-title">{{ item.title }}</h3>
              <p class="card-desc">{{ item.description }}</p>
              <div class="card-meta">
                <span class="meta-item">
                  <el-icon size="14"><Clock /></el-icon>
                  {{ item.duration }}分钟
                </span>
                <span class="meta-item">
                  <el-icon size="14"><Document /></el-icon>
                  {{ item.questionCount }}题
                </span>
                <span class="meta-item">
                  <el-icon size="14"><View /></el-icon>
                  {{ item.heat }}
                </span>
              </div>
              <div class="card-footer">
                <el-button
                  :type="item.real ? 'primary' : 'default'"
                  size="small"
                  round
                  class="card-btn"
                  :class="{ 'btn-real': item.real }"
                  @click.stop="handleStart(item)"
                >
                  {{ item.real ? '开始测评' : '查看详情' }}
                  <el-icon><ArrowRight /></el-icon>
                </el-button>
              </div>
            </div>
          </div>
        </TransitionGroup>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, h } from 'vue'
import { useRouter } from 'vue-router'
import { Search, Clock, Document, View, ArrowRight } from '@element-plus/icons-vue'
import {
  assessmentCategories,
  assessmentList,
  getAssessmentsByCategory,
  getAssessmentsBySearch
} from '@/data/assessmentBank'
import { assessmentVisualThemes } from '@/data/assessmentVisualThemes'

const router = useRouter()
const activeCategory = ref('all')
const searchKeyword = ref('')

const categories = assessmentCategories

const filteredList = computed(() => {
  const byCategory = getAssessmentsByCategory(activeCategory.value)
  const bySearch = getAssessmentsBySearch(searchKeyword.value)
  const ids = new Set(bySearch.map(item => item.id))
  return byCategory.filter(item => ids.has(item.id))
})

const currentCategoryName = computed(() => {
  const cat = categories.find(c => c.key === activeCategory.value)
  return cat ? (cat.key === 'all' ? '全部测评' : cat.name) : '全部测评'
})

function getTheme(item) {
  return assessmentVisualThemes[item.id] || assessmentVisualThemes['entrepreneurial-spirit']
}

function coverStyle(item) {
  const theme = getTheme(item)
  return { background: `linear-gradient(135deg, ${theme.gradient[0]}, ${theme.gradient[1]})` }
}

function getBgDeco(item) {
  const theme = getTheme(item)
  return { background: theme.bgDecorations }
}

function getAccentColor(item) {
  return getTheme(item).accentColor
}

function getThemeLabel(item) {
  return getTheme(item).label
}

function getThemeSubtitle(item) {
  return getTheme(item).subtitle
}

function getSvgComponent(item) {
  const theme = getTheme(item)
  const svgType = theme.svgDecorations
  const ac = theme.accentColor
  return { render: () => renderSvg(svgType, ac) }
}

function renderSvg(svgType, ac) {
  const gradId = `grad_${svgType}`
  switch (svgType) {
    case 'spark-energy':
      return h('svg', { viewBox: '0 0 200 120', class: 'card-svg-deco' }, [
        h('defs', null, [
          h('linearGradient', { id: gradId, x1: '0%', y1: '0%', x2: '100%', y2: '100%' }, [
            h('stop', { offset: '0%', 'stop-color': ac, 'stop-opacity': '0.3' }),
            h('stop', { offset: '100%', 'stop-color': ac, 'stop-opacity': '0.05' })
          ])
        ]),
        h('circle', { cx: '100', cy: '60', r: '40', fill: 'none', stroke: `url(#${gradId})`, 'stroke-width': '1', class: 'svg-pulse' }),
        h('circle', { cx: '100', cy: '60', r: '25', fill: 'none', stroke: ac, 'stroke-width': '0.8', 'stroke-dasharray': '4 6', class: 'svg-rotate-slow' }),
        h('polygon', { points: '100,28 107,45 125,47 111,60 115,78 100,68 85,78 89,60 75,47 93,45', fill: ac, opacity: '0.4', class: 'svg-float' }),
        ...[0, 60, 120, 180, 240, 300].map(angle =>
          h('line', {
            key: `el${angle}`,
            x1: 100 + 35 * Math.cos(angle * Math.PI / 180),
            y1: 60 + 35 * Math.sin(angle * Math.PI / 180),
            x2: 100 + 42 * Math.cos(angle * Math.PI / 180),
            y2: 60 + 42 * Math.sin(angle * Math.PI / 180),
            stroke: ac, 'stroke-width': '1.2', opacity: '0.25', class: 'svg-pulse-delay'
          })
        )
      ])
    case 'radar-dots':
      return h('svg', { viewBox: '0 0 200 120', class: 'card-svg-deco' }, [
        h('defs', null, [
          h('linearGradient', { id: gradId, x1: '0%', y1: '0%', x2: '100%', y2: '100%' }, [
            h('stop', { offset: '0%', 'stop-color': ac, 'stop-opacity': '0.25' }),
            h('stop', { offset: '100%', 'stop-color': ac, 'stop-opacity': '0.05' })
          ])
        ]),
        ...[3, 2, 1].map(r => {
          const radius = r * 15
          const pts = []
          for (let i = 0; i < 6; i++) {
            const a = i * 60 * Math.PI / 180 - Math.PI / 2
            pts.push(`${100 + radius * Math.cos(a)},${60 + radius * Math.sin(a)}`)
          }
          return h('polygon', { key: `radar${r}`, points: pts.join(' '), fill: 'none', stroke: `url(#${gradId})`, 'stroke-width': '0.8', class: 'svg-rotate-slow' })
        }),
        ...[0, 60, 120, 180, 240, 300].map((angle, i) => {
          const a = angle * Math.PI / 180 - Math.PI / 2
          return h('circle', {
            key: `dot${i}`,
            cx: 100 + 45 * Math.cos(a),
            cy: 60 + 45 * Math.sin(a),
            r: 2 + i % 2,
            fill: ac, opacity: '0.5', class: 'svg-pulse-delay'
          })
        })
      ])
    case 'compass-path':
      return h('svg', { viewBox: '0 0 200 120', class: 'card-svg-deco' }, [
        h('defs', null, [
          h('linearGradient', { id: gradId, x1: '0%', y1: '0%', x2: '100%', y2: '100%' }, [
            h('stop', { offset: '0%', 'stop-color': ac, 'stop-opacity': '0.3' }),
            h('stop', { offset: '100%', 'stop-color': ac, 'stop-opacity': '0.05' })
          ])
        ]),
        h('circle', { cx: '100', cy: '60', r: '38', fill: 'none', stroke: `url(#${gradId})`, 'stroke-width': '1', class: 'svg-rotate-slow' }),
        h('circle', { cx: '100', cy: '60', r: '4', fill: ac, opacity: '0.5' }),
        h('path', { d: 'M100,22 L106,50 L100,60 L94,50 Z', fill: ac, opacity: '0.3', class: 'svg-float' }),
        h('path', { d: 'M100,98 L94,70 L100,60 L106,70 Z', fill: ac, opacity: '0.15' }),
        h('path', { d: 'M62,60 L90,54 L100,60 L90,66 Z', fill: ac, opacity: '0.15' }),
        h('path', { d: 'M138,60 L110,66 L100,60 L110,54 Z', fill: ac, opacity: '0.25', class: 'svg-float' }),
        h('path', { d: 'M78,38 L94,50 L100,60 L86,52 Z', fill: ac, opacity: '0.12' }),
        h('path', { d: 'M122,82 L106,70 L100,60 L114,68 Z', fill: ac, opacity: '0.2', class: 'svg-pulse-delay' })
      ])
    case 'data-bars':
      return h('svg', { viewBox: '0 0 200 120', class: 'card-svg-deco' }, [
        h('defs', null, [
          h('linearGradient', { id: gradId, x1: '0%', y1: '0%', x2: '0%', y2: '100%' }, [
            h('stop', { offset: '0%', 'stop-color': ac, 'stop-opacity': '0.4' }),
            h('stop', { offset: '100%', 'stop-color': ac, 'stop-opacity': '0.1' })
          ])
        ]),
        ...[0, 1, 2, 3, 4].map((i) => {
          const h_val = 15 + i * 8 + (i % 2) * 5
          return h('rect', {
            key: `bar${i}`,
            x: 44 + i * 28,
            y: 80 - h_val,
            width: 16,
            height: h_val,
            rx: 3,
            fill: `url(#${gradId})`,
            class: 'svg-bar'
          })
        }),
        h('line', { x1: '38', y1: '82', x2: '180', y2: '82', stroke: ac, 'stroke-width': '0.5', opacity: '0.2' }),
        h('circle', { cx: '44', cy: '78', r: '2', fill: ac, opacity: '0.4', class: 'svg-float' })
      ])
    case 'network-nodes':
      return h('svg', { viewBox: '0 0 200 120', class: 'card-svg-deco' }, [
        h('defs', null, [
          h('linearGradient', { id: gradId, x1: '0%', y1: '0%', x2: '100%', y2: '100%' }, [
            h('stop', { offset: '0%', 'stop-color': ac, 'stop-opacity': '0.3' }),
            h('stop', { offset: '100%', 'stop-color': ac, 'stop-opacity': '0.05' })
          ])
        ]),
        h('circle', { cx: '60', cy: '40', r: '3', fill: ac, opacity: '0.5', class: 'svg-pulse' }),
        h('circle', { cx: '140', cy: '40', r: '3', fill: ac, opacity: '0.5', class: 'svg-pulse-delay' }),
        h('circle', { cx: '100', cy: '60', r: '4', fill: ac, opacity: '0.6', class: 'svg-pulse' }),
        h('circle', { cx: '60', cy: '80', r: '3', fill: ac, opacity: '0.5', class: 'svg-pulse-delay' }),
        h('circle', { cx: '140', cy: '80', r: '3', fill: ac, opacity: '0.5', class: 'svg-pulse' }),
        h('line', { x1: '60', y1: '40', x2: '100', y2: '60', stroke: `url(#${gradId})`, 'stroke-width': '1', class: 'svg-rotate-slow' }),
        h('line', { x1: '140', y1: '40', x2: '100', y2: '60', stroke: `url(#${gradId})`, 'stroke-width': '1', class: 'svg-rotate-slow' }),
        h('line', { x1: '60', y1: '80', x2: '100', y2: '60', stroke: `url(#${gradId})`, 'stroke-width': '1', class: 'svg-rotate-slow' }),
        h('line', { x1: '140', y1: '80', x2: '100', y2: '60', stroke: `url(#${gradId})`, 'stroke-width': '1', class: 'svg-rotate-slow' }),
        h('line', { x1: '60', y1: '40', x2: '60', y2: '80', stroke: `url(#${gradId})`, 'stroke-width': '0.6', class: 'svg-rotate-slow' }),
        h('line', { x1: '140', y1: '40', x2: '140', y2: '80', stroke: `url(#${gradId})`, 'stroke-width': '0.6', class: 'svg-rotate-slow' })
      ])
    case 'abstract-shape':
      return h('svg', { viewBox: '0 0 200 120', class: 'card-svg-deco' }, [
        h('defs', null, [
          h('linearGradient', { id: gradId, x1: '0%', y1: '0%', x2: '100%', y2: '100%' }, [
            h('stop', { offset: '0%', 'stop-color': ac, 'stop-opacity': '0.25' }),
            h('stop', { offset: '100%', 'stop-color': ac, 'stop-opacity': '0.05' })
          ])
        ]),
        h('polygon', { points: '100,20 150,55 135,100 65,100 50,55', fill: 'none', stroke: `url(#${gradId})`, 'stroke-width': '1.2', class: 'svg-rotate-slow' }),
        h('polygon', { points: '100,35 135,60 125,90 75,90 65,60', fill: 'none', stroke: ac, 'stroke-width': '0.6', opacity: '0.2', class: 'svg-rotate-slow' }),
        h('circle', { cx: '100', cy: '60', r: '2', fill: ac, opacity: '0.4' })
      ])
    case 'concentric-circles':
      return h('svg', { viewBox: '0 0 200 120', class: 'card-svg-deco' }, [
        ...[40, 30, 20, 10].map((r, i) =>
          h('circle', {
            key: `cc${i}`,
            cx: '100', cy: '60', r,
            fill: 'none',
            stroke: ac,
            'stroke-width': 0.6 + (i % 2) * 0.4,
            opacity: 0.35 - i * 0.05,
            'stroke-dasharray': i % 2 === 0 ? '4 6' : 'none',
            class: i % 2 === 0 ? 'svg-rotate-slow' : 'svg-float'
          })
        )
      ])
    case 'path-direction':
      return h('svg', { viewBox: '0 0 200 120', class: 'card-svg-deco' }, [
        h('defs', null, [
          h('linearGradient', { id: gradId, x1: '0%', y1: '0%', x2: '100%', y2: '0%' }, [
            h('stop', { offset: '0%', 'stop-color': ac, 'stop-opacity': '0.1' }),
            h('stop', { offset: '50%', 'stop-color': ac, 'stop-opacity': '0.3' }),
            h('stop', { offset: '100%', 'stop-color': ac, 'stop-opacity': '0.1' })
          ])
        ]),
        h('path', { d: 'M30,60 Q60,30 100,50 T170,40', fill: 'none', stroke: `url(#${gradId})`, 'stroke-width': '2', class: 'svg-rotate-slow' }),
        h('circle', { cx: '30', cy: '60', r: '3', fill: ac, opacity: '0.3' }),
        h('circle', { cx: '100', cy: '50', r: '4', fill: ac, opacity: '0.5', class: 'svg-pulse' }),
        h('circle', { cx: '170', cy: '40', r: '3', fill: ac, opacity: '0.3' }),
        h('polygon', { points: '170,34 178,40 170,46', fill: ac, opacity: '0.4', class: 'svg-float' })
      ])
    case 'geometric-diamond':
      return h('svg', { viewBox: '0 0 200 120', class: 'card-svg-deco' }, [
        h('defs', null, [
          h('linearGradient', { id: gradId, x1: '0%', y1: '0%', x2: '100%', y2: '100%' }, [
            h('stop', { offset: '0%', 'stop-color': ac, 'stop-opacity': '0.25' }),
            h('stop', { offset: '100%', 'stop-color': ac, 'stop-opacity': '0.05' })
          ])
        ]),
        h('polygon', { points: '100,20 145,60 100,100 55,60', fill: 'none', stroke: `url(#${gradId})`, 'stroke-width': '1.2', class: 'svg-rotate-slow' }),
        h('polygon', { points: '100,35 130,60 100,85 70,60', fill: 'none', stroke: ac, 'stroke-width': '0.6', opacity: '0.15', class: 'svg-rotate-slow' })
      ])
    case 'growth-spiral':
      return h('svg', { viewBox: '0 0 200 120', class: 'card-svg-deco' }, [
        h('defs', null, [
          h('linearGradient', { id: gradId, x1: '0%', y1: '100%', x2: '100%', y2: '0%' }, [
            h('stop', { offset: '0%', 'stop-color': ac, 'stop-opacity': '0.1' }),
            h('stop', { offset: '100%', 'stop-color': ac, 'stop-opacity': '0.3' })
          ])
        ]),
        h('path', { d: 'M100,60 Q95,45 100,35 Q110,25 120,40 Q125,60 110,70 Q90,75 80,55 Q75,30 105,20 Q135,15 145,50', fill: 'none', stroke: `url(#${gradId})`, 'stroke-width': '1.5', class: 'svg-rotate-slow' }),
        h('circle', { cx: '100', cy: '60', r: '2', fill: ac, opacity: '0.4' })
      ])
    case 'speech-bubbles':
      return h('svg', { viewBox: '0 0 200 120', class: 'card-svg-deco' }, [
        h('defs', null, [
          h('linearGradient', { id: gradId, x1: '0%', y1: '0%', x2: '100%', y2: '100%' }, [
            h('stop', { offset: '0%', 'stop-color': ac, 'stop-opacity': '0.2' }),
            h('stop', { offset: '100%', 'stop-color': ac, 'stop-opacity': '0.05' })
          ])
        ]),
        h('rect', { x: '45', y: '35', width: '60', height: '32', rx: '8', fill: 'none', stroke: `url(#${gradId})`, 'stroke-width': '1.2', class: 'svg-float' }),
        h('polygon', { points: '55,67 60,82 68,67', fill: 'none', stroke: ac, 'stroke-width': '0.8', opacity: '0.2' }),
        h('rect', { x: '95', y: '50', width: '55', height: '28', rx: '8', fill: 'none', stroke: ac, 'stroke-width': '0.8', opacity: '0.2', class: 'svg-float' }),
        h('polygon', { points: '135,78 140,90 145,78', fill: 'none', stroke: ac, 'stroke-width': '0.6', opacity: '0.15' }),
        h('circle', { cx: '65', cy: '48', r: '1.5', fill: ac, opacity: '0.4' }),
        h('circle', { cx: '80', cy: '48', r: '1.5', fill: ac, opacity: '0.4' }),
        h('circle', { cx: '72', cy: '55', r: '1.5', fill: ac, opacity: '0.4' })
      ])
    case 'wave-balance':
      return h('svg', { viewBox: '0 0 200 120', class: 'card-svg-deco' }, [
        h('defs', null, [
          h('linearGradient', { id: gradId, x1: '0%', y1: '0%', x2: '100%', y2: '0%' }, [
            h('stop', { offset: '0%', 'stop-color': ac, 'stop-opacity': '0.1' }),
            h('stop', { offset: '50%', 'stop-color': ac, 'stop-opacity': '0.25' }),
            h('stop', { offset: '100%', 'stop-color': ac, 'stop-opacity': '0.1' })
          ])
        ]),
        h('path', { d: 'M30,65 Q55,40 80,60 T130,55 T170,65', fill: 'none', stroke: `url(#${gradId})`, 'stroke-width': '1.5', class: 'svg-rotate-slow' }),
        h('path', { d: 'M30,75 Q55,55 80,70 T130,65 T170,75', fill: 'none', stroke: ac, 'stroke-width': '0.8', opacity: '0.15', class: 'svg-rotate-slow' }),
        h('circle', { cx: '80', cy: '60', r: '2', fill: ac, opacity: '0.4', class: 'svg-float' }),
        h('circle', { cx: '130', cy: '55', r: '2', fill: ac, opacity: '0.4', class: 'svg-float' })
      ])
    default:
      return h('svg', { viewBox: '0 0 200 120', class: 'card-svg-deco' }, [
        h('circle', { cx: '100', cy: '60', r: '30', fill: 'none', stroke: ac, 'stroke-width': '0.8', opacity: '0.2' })
      ])
  }
}

function selectCategory(key) {
  activeCategory.value = key
}

function getCategoryCount(key) {
  if (key === 'all') return assessmentList.length
  const cat = categories.find(c => c.key === key)
  if (!cat || !cat.children) return 0
  return assessmentList.filter(item => cat.children.includes(item.id)).length
}

function handleSearch() {
}

function handleStart(item) {
  if (item.real) {
    router.push(`/assessment/${item.id}`)
  } else {
    router.push(`/assessment/${item.id}/coming-soon`)
  }
}
</script>

<style scoped>
.assessment-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #eff6ff 0%, #f8fafc 100%);
}

.assessment-banner {
  position: relative;
  background: linear-gradient(135deg, #1e40af 0%, #2563eb 50%, #06b6d4 100%);
  padding: 48px 40px 40px;
  overflow: hidden;
}

.banner-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background:
    radial-gradient(circle at 20% 50%, rgba(14, 165, 233, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 80% 30%, rgba(139, 92, 246, 0.1) 0%, transparent 50%);
}

.banner-content {
  position: relative;
  z-index: 2;
  max-width: 1200px;
  margin: 0 auto;
}

.banner-title {
  font-size: 32px;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 8px;
}

.banner-subtitle {
  font-size: 16px;
  color: #93c5fd;
}

.assessment-layout {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  gap: 0;
  padding: 24px 40px 40px;
}

.sidebar {
  width: 220px;
  flex-shrink: 0;
  background: #ffffff;
  border-radius: 12px;
  padding: 16px 0;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
  align-self: flex-start;
  position: sticky;
  top: 80px;
}

.sidebar-title {
  font-size: 14px;
  font-weight: 600;
  color: #475569;
  padding: 8px 20px 12px;
  border-bottom: 1px solid #f1f5f9;
  margin-bottom: 4px;
}

.sidebar-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
  color: #475569;
  border-left: 3px solid transparent;
}

.sidebar-item:hover {
  background: #f8fafc;
  color: #2563eb;
}

.sidebar-item.active {
  background: #eff6ff;
  color: #2563eb;
  font-weight: 600;
  border-left-color: #2563eb;
}

.sidebar-count {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 10px;
  background: #f1f5f9;
  color: #64748b;
}

.sidebar-item.active .sidebar-count {
  background: #dbeafe;
  color: #2563eb;
}

.main-area {
  flex: 1;
  margin-left: 24px;
  min-width: 0;
}

.main-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
  gap: 16px;
}

.main-title {
  font-size: 20px;
  font-weight: 600;
  color: #1e293b;
  white-space: nowrap;
}

.main-search {
  width: 320px;
}

.search-input :deep(.el-input__wrapper) {
  border-radius: 24px;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.08);
}

.assessment-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.empty-state {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 64px 0;
  color: #94a3b8;
}

.empty-state p {
  font-size: 16px;
  font-weight: 500;
  color: #64748b;
  margin: 16px 0 4px;
}

.empty-state span {
  font-size: 13px;
  color: #94a3b8;
}

.assessment-card {
  background: #ffffff;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
}

.assessment-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 40px rgba(15, 23, 42, 0.12);
}

.card-cover {
  height: 180px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.card-cover-bg-deco {
  position: absolute;
  inset: 0;
  z-index: 1;
}

.card-svg-deco {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  z-index: 2;
  pointer-events: none;
}

.card-cover-overlay {
  display: none;
}

.cover-tag {
  position: absolute;
  top: 12px;
  left: 12px;
  z-index: 3;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.12em;
  padding: 4px 12px;
  border-radius: 6px;
  border: 1px solid;
  backdrop-filter: blur(4px);
  line-height: 1.4;
}

.cover-sub {
  position: absolute;
  bottom: 10px;
  left: 12px;
  right: 12px;
  z-index: 3;
  font-size: 9px;
  opacity: 0.5;
  letter-spacing: 0.03em;
  line-height: 1.3;
  text-align: left;
}

.card-body {
  padding: 20px;
}

.card-title {
  font-size: 17px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 8px;
}

.card-desc {
  font-size: 13px;
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 14px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 14px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #94a3b8;
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.card-btn {
  flex-shrink: 0;
}

.btn-real {
  background: linear-gradient(135deg, #2563eb, #3b82f6);
  border-color: #2563eb;
  color: #ffffff;
}

.btn-real:hover {
  background: linear-gradient(135deg, #1d4ed8, #2563eb);
  border-color: #1d4ed8;
  color: #ffffff;
}

/* SVG animations */
@keyframes svgFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}

@keyframes svgPulse {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 0.6; }
}

@keyframes svgRotateSlow {
  from { transform: rotate(0deg); transform-origin: center; }
  to { transform: rotate(360deg); transform-origin: center; }
}

@keyframes svgBarGrow {
  from { transform: scaleY(0.3); transform-origin: bottom; }
  to { transform: scaleY(1); transform-origin: bottom; }
}

.card-svg-deco :deep(.svg-float) {
  animation: svgFloat 4s ease-in-out infinite;
}

.card-svg-deco :deep(.svg-pulse) {
  animation: svgPulse 3s ease-in-out infinite;
}

.card-svg-deco :deep(.svg-pulse-delay) {
  animation: svgPulse 3s ease-in-out infinite;
  animation-delay: 1.5s;
}

.card-svg-deco :deep(.svg-rotate-slow) {
  animation: svgRotateSlow 20s linear infinite;
}

.card-svg-deco :deep(.svg-bar) {
  animation: svgBarGrow 1.5s ease-out;
}

/* card list transition */
.card-list-enter-active {
  transition: all 0.4s ease;
}

.card-list-leave-active {
  transition: all 0.3s ease;
}

.card-list-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.card-list-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* responsive */
@media (max-width: 1024px) {
  .assessment-layout {
    flex-direction: column;
    padding: 16px;
  }

  .sidebar {
    width: 100%;
    position: static;
    display: flex;
    overflow-x: auto;
    padding: 8px;
    gap: 0;
    border-radius: 12px;
    margin-bottom: 16px;
  }

  .sidebar-title {
    display: none;
  }

  .sidebar-item {
    border-left: none;
    white-space: nowrap;
    padding: 8px 14px;
    font-size: 13px;
    border-radius: 8px;
    flex-shrink: 0;
  }

  .sidebar-item.active {
    border-left: none;
  }

  .sidebar-count {
    display: none;
  }

  .main-area {
    margin-left: 0;
  }

  .main-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .main-search {
    width: 100%;
  }

  .assessment-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .assessment-banner {
    padding: 32px 20px;
  }

  .banner-title {
    font-size: 24px;
  }

  .banner-subtitle {
    font-size: 14px;
  }

  .assessment-grid {
    grid-template-columns: 1fr;
  }

  .cover-tag {
    font-size: 10px;
    padding: 3px 10px;
  }

  .cover-sub {
    font-size: 8px;
  }
}
</style>