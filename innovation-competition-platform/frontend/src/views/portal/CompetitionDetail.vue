<template>
  <div class="competition-detail">
    <!-- 竞赛头图 -->
    <div class="detail-header" :style="{ background: competition.gradient }">
      <div class="header-content">
        <div class="header-tags">
          <el-tag :type="competition.levelType" size="large">{{ competition.level }}</el-tag>
          <el-tag size="large" class="category-tag">{{ competition.category }}</el-tag>
          <el-tag :type="competition.statusType" size="large">{{ competition.statusText }}</el-tag>
        </div>
        <h1 class="header-title">{{ competition.name }}</h1>
        <p class="header-organizer">主办方：{{ competition.organizer }}</p>
        <div class="header-stats">
          <span class="stat">
            <el-icon><Calendar /></el-icon>
            报名截止：{{ competition.endDate }}
          </span>
          <span class="stat">
            <el-icon><View /></el-icon>
            {{ competition.viewCount }} 浏览
          </span>
          <span class="stat">
            <el-icon><User /></el-icon>
            {{ competition.registrationCount }} 人报名
          </span>
        </div>
      </div>
      <div class="header-action">
        <el-button
          v-if="canRegister"
          type="primary"
          size="large"
          @click="goToRegister"
        >
          立即报名
        </el-button>
        <el-button
          v-else-if="!isStudent"
          type="info"
          size="large"
          disabled
        >
          当前角色不可报名
        </el-button>
        <el-button
          v-else-if="hasRegistered"
          type="success"
          size="large"
          @click="goToMyRegistrations"
        >
          查看我的报名
        </el-button>
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="detail-body">
      <el-row :gutter="24">
        <el-col :span="16">
          <!-- 竞赛简介 -->
          <el-card class="detail-card" shadow="never">
            <template #header>
              <div class="card-header">
                <el-icon><Document /></el-icon>
                <span>竞赛简介</span>
              </div>
            </template>
            <p class="description">{{ competition.description }}</p>
            <div class="info-list">
              <div class="info-item">
                <span class="info-label">目标对象</span>
                <span class="info-value">{{ competition.targetAudience }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">参赛要求</span>
                <span class="info-value">{{ competition.requirements }}</span>
              </div>
            </div>
          </el-card>

          <!-- 赛道设置 -->
          <el-card class="detail-card" shadow="never">
            <template #header>
              <div class="card-header">
                <el-icon><Flag /></el-icon>
                <span>赛道设置</span>
              </div>
            </template>
            <div class="track-list">
              <div
                v-for="track in competition.tracks"
                :key="track.id"
                class="track-item"
              >
                <div class="track-header">
                  <h4 class="track-name">{{ track.name }}</h4>
                  <el-tag :type="track.status === 'open' ? 'success' : 'info'" size="small">
                    {{ track.status === 'open' ? '开放中' : '已关闭' }}
                  </el-tag>
                </div>
                <p class="track-desc">{{ track.description }}</p>
                <div class="track-meta">
                  <span>团队人数：{{ track.teamMin }}-{{ track.teamMax }}人</span>
                  <span>材料要求：{{ track.materialRequirements }}</span>
                </div>
              </div>
            </div>
          </el-card>

          <!-- 时间安排 -->
          <el-card class="detail-card" shadow="never">
            <template #header>
              <div class="card-header">
                <el-icon><Timer /></el-icon>
                <span>时间安排</span>
              </div>
            </template>
            <el-timeline>
              <el-timeline-item
                v-for="(item, index) in competition.schedule"
                :key="index"
                :type="item.type"
                :icon="item.icon"
              >
                <h4>{{ item.title }}</h4>
                <p>{{ item.time }}</p>
                <p v-if="item.desc" class="timeline-desc">{{ item.desc }}</p>
              </el-timeline-item>
            </el-timeline>
          </el-card>

          <!-- 奖项设置 -->
          <el-card class="detail-card" shadow="never">
            <template #header>
              <div class="card-header">
                <el-icon><Trophy /></el-icon>
                <span>奖项设置</span>
              </div>
            </template>
            <div class="award-list">
              <div
                v-for="award in competition.awards"
                :key="award.level"
                class="award-item"
              >
                <div class="award-badge" :class="`award-${award.level}`">
                  {{ award.name }}
                </div>
                <div class="award-detail">
                  <p class="award-prize">{{ award.prize }}</p>
                  <p class="award-count">名额：{{ award.count }}个</p>
                </div>
              </div>
            </div>
          </el-card>

          <!-- 材料要求 -->
          <el-card class="detail-card" shadow="never">
            <template #header>
              <div class="card-header">
                <el-icon><FolderOpened /></el-icon>
                <span>材料要求</span>
              </div>
            </template>
            <el-descriptions :column="1" border>
              <el-descriptions-item
                v-for="material in competition.materials"
                :key="material.type"
                :label="material.type"
              >
                {{ material.requirement }}
              </el-descriptions-item>
            </el-descriptions>
          </el-card>
        </el-col>

        <el-col :span="8">
          <!-- 竞赛信息侧边栏 -->
          <el-card class="sidebar-card" shadow="never">
            <template #header>
              <span>竞赛信息</span>
            </template>
            <div class="sidebar-info">
              <div class="sidebar-item">
                <span class="sidebar-label">报名开始</span>
                <span class="sidebar-value">{{ competition.registrationStart }}</span>
              </div>
              <div class="sidebar-item">
                <span class="sidebar-label">报名截止</span>
                <span class="sidebar-value">{{ competition.registrationEnd }}</span>
              </div>
              <div class="sidebar-item">
                <span class="sidebar-label">竞赛开始</span>
                <span class="sidebar-value">{{ competition.competitionStart }}</span>
              </div>
              <div class="sidebar-item">
                <span class="sidebar-label">竞赛结束</span>
                <span class="sidebar-value">{{ competition.competitionEnd }}</span>
              </div>
              <div class="sidebar-item">
                <span class="sidebar-label">竞赛级别</span>
                <span class="sidebar-value">{{ competition.level }}</span>
              </div>
              <div class="sidebar-item">
                <span class="sidebar-label">竞赛分类</span>
                <span class="sidebar-value">{{ competition.category }}</span>
              </div>
            </div>
          </el-card>

          <!-- 报名按钮固定 -->
          <el-card class="sidebar-card action-card" shadow="never">
            <el-button
              v-if="canRegister"
              type="primary"
              size="large"
              class="register-btn"
              @click="goToRegister"
            >
              立即报名
            </el-button>
            <el-button
              v-else-if="!isStudent"
              type="info"
              size="large"
              class="register-btn"
              disabled
            >
              当前角色不可报名
            </el-button>
            <el-button
              v-else-if="hasRegistered"
              type="success"
              size="large"
              class="register-btn"
              @click="goToMyRegistrations"
            >
              查看我的报名
            </el-button>
            <p class="register-tip">报名截止：{{ competition.endDate }}</p>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import {
  Calendar, View, User, Document, Flag, Timer,
  Trophy, FolderOpened
} from '@element-plus/icons-vue'
import { getPublicCompetitionDetail } from '@/api/competition'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const isStudent = computed(() => userStore.isStudent)
const canRegister = computed(() => userStore.isStudent && !hasRegistered.value)
const hasRegistered = ref(false)

const competition = ref({
  id: route.params.id,
  name: '',
  organizer: '',
  category: '',
  level: '',
  levelType: 'success',
  status: 'active',
  statusType: 'success',
  statusText: '报名中',
  endDate: '',
  viewCount: 0,
  registrationCount: 0,
  gradient: 'linear-gradient(135deg, #0c4a6e 0%, #075985 50%, #0ea5e9 100%)',
  description: '',
  targetAudience: '',
  requirements: '',
  registrationStart: '',
  registrationEnd: '',
  competitionStart: '',
  competitionEnd: '',
  tracks: [],
  schedule: [],
  awards: [],
  materials: []
})

const loadDetail = async () => {
  try {
    const res = await getPublicCompetitionDetail(route.params.id)
    if (res.code === 200) {
      const data = res.data
      hasRegistered.value = data.has_registered || false
      
      const levelTypeMap = { '国家级': 'danger', '省级': 'warning' }
      const statusTextMap = { active: '报名中', upcoming: '即将开始', ended: '已结束' }
      const statusTypeMap = { active: 'success', upcoming: 'info', ended: 'info' }

      competition.value = {
        ...competition.value,
        ...data,
        endDate: data.registration_end ? data.registration_end.split('T')[0] : '',
        levelType: levelTypeMap[data.level] || 'success',
        statusText: statusTextMap[data.status] || '报名中',
        statusType: statusTypeMap[data.status] || 'success',
        registrationStart: data.registration_start ? data.registration_start.split('T')[0] : '',
        registrationEnd: data.registration_end ? data.registration_end.split('T')[0] : '',
        competitionStart: data.competition_start ? data.competition_start.split('T')[0] : '',
        competitionEnd: data.competition_end ? data.competition_end.split('T')[0] : '',
        gradient: data.poster_url 
          ? `url(${data.poster_url}) center/cover`
          : 'linear-gradient(135deg, #0c4a6e 0%, #075985 50%, #0ea5e9 100%)'
      }
      
      // If the backend didn't provide schedule, awards, materials, we can keep some dummy ones or parse them
      if (!data.schedule || data.schedule.length === 0) {
        competition.value.schedule = [
          { title: '报名开始', time: competition.value.registrationStart, type: 'primary', icon: 'More' },
          { title: '报名截止', time: competition.value.registrationEnd, type: 'warning', icon: 'More' }
        ]
      }
      if (!data.awards || data.awards.length === 0) {
        competition.value.awards = [
          { level: 'first', name: '一等奖', prize: data.awards || '奖金及证书', count: 3 }
        ]
      }
      if (!data.materials || data.materials.length === 0) {
        competition.value.materials = [
          { type: '项目申报材料', requirement: '按要求提交' }
        ]
      }
    }
  } catch(e) {
    console.error('获取竞赛详情失败', e)
  }
}

onMounted(() => {
  loadDetail()
})

const goToRegister = () => {
  router.push(`/competitions/${route.params.id}/register`)
}

const goToMyRegistrations = () => {
  router.push('/my-registrations')
}
</script>

<style scoped>
.competition-detail {
  min-height: 100vh;
  background-color: #f8fafc;
}

/* 头部 */
.detail-header {
  padding: 50px 40px;
  color: #ffffff;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  flex-wrap: wrap;
  gap: 24px;
}

.header-content {
  flex: 1;
}

.header-tags {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.category-tag {
  background-color: rgba(255, 255, 255, 0.9);
  color: #1e293b;
  border: none;
}

.header-title {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 12px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.header-organizer {
  font-size: 16px;
  color: #bae6fd;
  margin-bottom: 16px;
}

.header-stats {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
}

.stat {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #e0f2fe;
}

.header-action {
  flex-shrink: 0;
}

/* 内容区域 */
.detail-body {
  padding: 24px 40px;
  max-width: 1400px;
  margin: 0 auto;
}

.detail-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.description {
  font-size: 14px;
  line-height: 1.8;
  color: #334155;
  margin-bottom: 20px;
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-item {
  display: flex;
  gap: 12px;
}

.info-label {
  font-weight: 600;
  color: #1e293b;
  min-width: 80px;
  flex-shrink: 0;
}

.info-value {
  color: #475569;
  line-height: 1.6;
}

/* 赛道 */
.track-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.track-item {
  padding: 16px;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.track-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.track-name {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
}

.track-desc {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 8px;
  line-height: 1.5;
}

.track-meta {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: #475569;
}

/* 奖项 */
.award-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.award-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 16px;
  background: #f8fafc;
  border-radius: 12px;
}

.award-badge {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  color: #ffffff;
  min-width: 80px;
  text-align: center;
}

.award-first { background: linear-gradient(135deg, #f59e0b, #fbbf24); }
.award-second { background: linear-gradient(135deg, #94a3b8, #cbd5e1); }
.award-third { background: linear-gradient(135deg, #b45309, #d97706); }
.award-excellent { background: linear-gradient(135deg, #0ea5e9, #38bdf8); }
.award-creative { background: linear-gradient(135deg, #8b5cf6, #a78bfa); }

.award-prize {
  font-size: 14px;
  font-weight: 500;
  color: #1e293b;
}

.award-count {
  font-size: 13px;
  color: #64748b;
}

/* 侧边栏 */
.sidebar-card {
  margin-bottom: 20px;
}

.sidebar-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.sidebar-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #f1f5f9;
}

.sidebar-item:last-child {
  border-bottom: none;
}

.sidebar-label {
  color: #64748b;
  font-size: 14px;
}

.sidebar-value {
  color: #1e293b;
  font-weight: 500;
  font-size: 14px;
}

.action-card {
  text-align: center;
}

.register-btn {
  width: 100%;
  margin-bottom: 12px;
}

.register-tip {
  font-size: 13px;
  color: #64748b;
}

.timeline-desc {
  font-size: 13px;
  color: #64748b;
  margin-top: 4px;
}
</style>
