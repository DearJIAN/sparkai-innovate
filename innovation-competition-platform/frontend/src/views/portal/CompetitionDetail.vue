<template>
  <div class="competition-detail">
    <div class="detail-poster" :class="{ 'has-image': competition.localImage || competition.poster_url }">
      <img
        v-if="competition.localImage"
        :src="competition.localImage"
        :alt="competition.name"
        class="poster-img"
        @error="handlePosterError"
      />
      <img
        v-else-if="competition.poster_url"
        :src="competition.poster_url"
        :alt="competition.name"
        class="poster-img"
        @error="handlePosterError"
      />
      <div v-else class="poster-fallback" :style="{ background: competition.gradient }">
        <div class="poster-fallback-content">
          <div class="poster-tags">
            <el-tag :type="competition.levelType" size="large">{{ competition.level }}</el-tag>
            <el-tag size="large" class="category-tag">{{ competition.category }}</el-tag>
            <el-tag :type="competition.statusType" size="large">{{ competition.statusText }}</el-tag>
          </div>
          <h1 class="poster-title">{{ competition.name }}</h1>
          <p class="poster-organizer">主办方：{{ competition.organizer }}</p>
        </div>
      </div>
      <div class="poster-overlay">
        <div class="poster-info">
          <div class="poster-tags">
            <el-tag :type="competition.levelType" size="large">{{ competition.level }}</el-tag>
            <el-tag size="large" class="category-tag">{{ competition.category }}</el-tag>
            <el-tag :type="competition.statusType" size="large">{{ competition.statusText }}</el-tag>
          </div>
          <h1 class="poster-title">{{ competition.name }}</h1>
          <p class="poster-organizer">主办方：{{ competition.organizer }}</p>
          <div class="poster-stats">
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
        <div class="poster-action">
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
    </div>

    <div class="detail-body">
      <el-row :gutter="24">
        <el-col :span="16">
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
              >
                <h4>{{ item.title }}</h4>
                <p class="timeline-time">{{ item.time }}</p>
                <p v-if="item.desc" class="timeline-desc">{{ item.desc }}</p>
              </el-timeline-item>
            </el-timeline>
          </el-card>

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
                <span class="sidebar-label">初赛评审</span>
                <span class="sidebar-value">{{ competition.competitionStart }}</span>
              </div>
              <div class="sidebar-item">
                <span class="sidebar-label">决赛时间</span>
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
              <div class="sidebar-item">
                <span class="sidebar-label">主办方</span>
                <span class="sidebar-value">{{ competition.organizer }}</span>
              </div>
            </div>
          </el-card>

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

import imgAI from '@/assets/images/competitions/2026 AI 应用创新设计大赛.png'
import imgRural from '@/assets/images/competitions/2026 乡村振兴公益创业实践赛.png'
import imgEnterprise from '@/assets/images/competitions/2026 企业真实命题创新挑战赛.png'
import imgInnovation from '@/assets/images/competitions/2026 大学生创新创业计划训练赛.png'
import imgCareer from '@/assets/images/competitions/2026 大学生职业规划与就业能力大赛.png'
import imgDigital from '@/assets/images/competitions/2026 数字经济与商业模式创新挑战赛.png'
import imgSmartMfg from '@/assets/images/competitions/2026 智能制造与物联网应用赛.png'
import imgEcommerce from '@/assets/images/competitions/2026 校园电子商务运营挑战赛.png'
import imgSoftware from '@/assets/images/competitions/2026 软件工程创新项目挑战赛.png'
import imgRedDream from '@/assets/images/competitions/2026 青年红色筑梦公益项目赛.png'

const competitionImages = {
  'AI 应用创新设计大赛': imgAI,
  '乡村振兴公益创业实践赛': imgRural,
  '企业真实命题创新挑战赛': imgEnterprise,
  '大学生创新创业计划训练赛': imgInnovation,
  '大学生职业规划与就业能力大赛': imgCareer,
  '数字经济与商业模式创新挑战赛': imgDigital,
  '智能制造与物联网应用赛': imgSmartMfg,
  '校园电子商务运营挑战赛': imgEcommerce,
  '软件工程创新项目挑战赛': imgSoftware,
  '青年红色筑梦公益项目赛': imgRedDream
}

const getLocalImage = (name) => {
  const key = name.replace(/^2026\s*/, '')
  return competitionImages[key] || null
}

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const isStudent = computed(() => userStore.isStudent)
const canRegister = computed(() => userStore.isStudent && !hasRegistered.value)
const hasRegistered = ref(false)
const posterError = ref(false)

const competition = ref({
  id: route.params.id,
  name: '2026 AI 应用创新设计大赛',
  organizer: '全国大学生创新创业教育指导委员会',
  category: '人工智能',
  level: '国家级',
  levelType: 'danger',
  status: 'active',
  statusType: 'success',
  statusText: '报名中',
  endDate: '2026-04-15',
  viewCount: 3567,
  registrationCount: 1289,
  localImage: null,
  poster_url: '',
  gradient: 'linear-gradient(135deg, #0c4a6e 0%, #075985 50%, #0ea5e9 100%)',
  description: '本竞赛旨在激发大学生在人工智能领域的创新潜能，鼓励学生将AI技术应用于实际场景中解决真实问题。参赛团队需围绕指定赛道提交具有创新性和实用性的AI应用方案。',
  targetAudience: '全国高校在校本科生、研究生（含硕士、博士）均可组队参赛',
  requirements: '每队3-5人，可跨校组队；需有1名指导老师；每位学生只能参加一个队伍',
  registrationStart: '2026-03-01',
  registrationEnd: '2026-04-15',
  competitionStart: '2026-05-01',
  competitionEnd: '2026-06-15',
  tracks: [
    { id: 1, name: 'AI+教育创新赛道', description: '利用AI技术解决教育教学中的实际问题', teamMin: 3, teamMax: 5, materialRequirements: '系统演示视频+技术文档', status: 'open' },
    { id: 2, name: 'AI+医疗健康赛道', description: '将AI应用于医疗诊断、健康管理等领域', teamMin: 3, teamMax: 5, materialRequirements: '数据集说明+模型报告+演示视频', status: 'open' },
    { id: 3, name: 'AI+智慧城市赛道', description: '面向城市治理、交通优化等场景的AI解决方案', teamMin: 3, teamMax: 5, materialRequirements: '系统原型+部署方案+效果评估报告', status: 'open' }
  ],
  schedule: [],
  awards: [],
  materials: []
})

const handlePosterError = () => {
  posterError.value = true
}

const getScheduleForCompetition = (name, rs, re, cs, ce) => {
  const base = [
    { title: '报名启动', time: rs || '2026-03-01', type: 'primary', desc: '开放在线报名通道，参赛团队可通过平台提交报名信息，填写团队成员及项目概述' },
    { title: '报名截止', time: re || '2026-04-15', type: 'warning', desc: '逾期将无法补报，请确保在截止日期前完成报名及材料提交' },
    { title: '初赛评审', time: cs || '2026-05-01', type: '', desc: '专家评委对提交的项目材料进行线上初评，筛选晋级复赛的项目团队' },
    { title: '复赛评审', time: ce ? new Date(new Date(ce).getTime() - 14*86400000).toISOString().split('T')[0] : '2026-05-20', type: '', desc: '晋级团队进行线上答辩，评委根据项目创新性、可行性、团队表现等维度综合评分' },
    { title: '决赛路演', time: ce || '2026-06-15', type: 'danger', desc: '入围决赛团队进行现场路演答辩，角逐最终奖项，评委现场打分并提问' },
    { title: '结果公布与颁奖', time: ce ? new Date(new Date(ce).getTime() + 7*86400000).toISOString().split('T')[0] : '2026-06-22', type: 'success', desc: '公示获奖名单，举行颁奖典礼，颁发证书及奖金，优秀项目推荐参加更高级别赛事' }
  ]

  if (name.includes('AI') || name.includes('人工智能')) {
    base[2].desc = '专家评委对AI应用项目进行技术评审，重点考察模型创新性、应用场景和落地价值'
    base[4].desc = '决赛团队现场演示AI系统运行效果，回答评委关于算法、数据和产品设计的提问'
  } else if (name.includes('乡村振兴') || name.includes('公益')) {
    base[2].desc = '评审重点考察项目的公益价值、社会影响力和乡村落地可行性'
    base[4].desc = '入围团队展示公益项目成果，重点阐述乡村帮扶成效和可持续发展方案'
  } else if (name.includes('电子商务') || name.includes('数字经济')) {
    base[2].desc = '评审重点考察商业模式的创新性、数据分析能力和运营策略'
    base[4].desc = '决赛团队展示电商运营成果或商业模式方案，评委从盈利能力和市场前景维度评分'
  } else if (name.includes('软件') || name.includes('智能制造') || name.includes('物联网')) {
    base[2].desc = '技术评审重点考察系统架构设计、代码质量、创新技术应用和工程实践能力'
    base[4].desc = '决赛团队进行系统现场演示和技术答辩，展示项目的技术深度和创新亮点'
  }
  return base
}

const getAwardsForCompetition = (name, level) => {
  const isNational = level?.includes('国家')
  const isProvincial = level?.includes('省')

  const base = [
    { level: 'first', name: '特等奖', prize: isNational ? '奖金 ¥20,000 + 国家级荣誉证书 + 推荐参加国际赛事' : isProvincial ? '奖金 ¥10,000 + 省级荣誉证书 + 推荐参加国赛' : '奖金 ¥5,000 + 校级荣誉证书 + 推荐参加省赛', count: 1 },
    { level: 'second', name: '一等奖', prize: isNational ? '奖金 ¥10,000 + 国家级荣誉证书 + 创业孵化入驻资格' : isProvincial ? '奖金 ¥5,000 + 省级荣誉证书 + 导师一对一指导' : '奖金 ¥2,000 + 校级荣誉证书 + 创业培训资格', count: isNational ? 2 : 3 },
    { level: 'third', name: '二等奖', prize: isNational ? '奖金 ¥5,000 + 国家级荣誉证书 + 项目展示机会' : isProvincial ? '奖金 ¥2,000 + 省级荣誉证书 + 创业资源对接' : '奖金 ¥1,000 + 校级荣誉证书', count: isNational ? 4 : 6 },
    { level: 'excellent', name: '三等奖', prize: isNational ? '奖金 ¥2,000 + 国家级荣誉证书' : isProvincial ? '奖金 ¥800 + 省级荣誉证书' : '奖金 ¥500 + 校级荣誉证书', count: isNational ? 8 : 12 },
    { level: 'creative', name: '最佳创意奖', prize: '荣誉证书 + 精美奖品 + 优先推荐参加创新项目孵化', count: 2 },
    { level: 'teamwork', name: '最佳团队奖', prize: '荣誉证书 + 团队建设基金 ¥1,000 + 团队培训机会', count: 1 }
  ]

  if (name.includes('AI') || name.includes('人工智能')) {
    base[4] = { level: 'creative', name: '最佳创意奖', prize: '荣誉证书 + AI云服务资源包（价值¥5,000）+ 优先推荐参加AI创新项目孵化', count: 2 }
    base[5] = { level: 'teamwork', name: '最佳技术奖', prize: '荣誉证书 + 技术书籍礼包 + 大厂实习推荐机会', count: 1 }
  } else if (name.includes('乡村振兴') || name.includes('公益') || name.includes('红色')) {
    base[4] = { level: 'creative', name: '最佳公益影响力奖', prize: '荣誉证书 + 公益基金支持¥3,000 + 媒体宣传报道', count: 2 }
    base[5] = { level: 'teamwork', name: '最佳乡村实践奖', prize: '荣誉证书 + 乡村落地支持资源 + 地方政府对接机会', count: 1 }
  } else if (name.includes('电子商务') || name.includes('数字经济')) {
    base[4] = { level: 'creative', name: '最佳商业模式奖', prize: '荣誉证书 + 电商平台资源扶持 + 投资人对接机会', count: 2 }
    base[5] = { level: 'teamwork', name: '最佳运营奖', prize: '荣誉证书 + 电商培训课程 + 运营工具礼包', count: 1 }
  } else if (name.includes('职业规划')) {
    base[0].prize = '奖金 ¥3,000 + 荣誉证书 + 名企实习推荐名额'
    base[1].prize = '奖金 ¥1,500 + 荣誉证书 + 职业发展指导'
    base[2].prize = '奖金 ¥800 + 荣誉证书 + 求职辅导课程'
    base[3].prize = '奖金 ¥300 + 荣誉证书'
    base[4] = { level: 'creative', name: '最佳职业规划奖', prize: '荣誉证书 + 名企内推资格 + 职业测评工具', count: 2 }
    base[5] = { level: 'teamwork', name: '最具潜力奖', prize: '荣誉证书 + 职业技能培训课程 + 简历优化服务', count: 2 }
  }
  return base
}

const getMaterialsForCompetition = (name) => {
  const base = [
    { type: '项目申报书', requirement: 'PDF格式，不超过20页，包含项目背景、创新点、实施方案、预期成果等' },
    { type: '团队信息表', requirement: '包含所有成员姓名、学号、专业、联系方式及分工说明' },
    { type: '身份证明', requirement: '所有成员学生证扫描件或在校证明' }
  ]

  if (name.includes('AI') || name.includes('人工智能') || name.includes('软件') || name.includes('智能制造') || name.includes('物联网')) {
    base.push({ type: '技术文档', requirement: '系统架构设计文档、核心算法说明、API接口文档（如有）' })
    base.push({ type: '演示视频', requirement: '3-5分钟项目演示视频，展示核心功能和技术亮点' })
    base.push({ type: '源代码仓库', requirement: '提供GitHub/Gitee仓库链接，需包含README和部署说明' })
  } else if (name.includes('电子商务') || name.includes('数字经济')) {
    base.push({ type: '商业计划书', requirement: '详细的市场分析、盈利模式、运营策略和财务预测' })
    base.push({ type: '运营数据', requirement: '如有实际运营，提供关键运营数据截图和分析报告' })
  } else if (name.includes('乡村振兴') || name.includes('公益') || name.includes('红色')) {
    base.push({ type: '社会影响报告', requirement: '项目对目标群体产生的实际影响，包含数据支撑和受益人反馈' })
    base.push({ type: '落地证明', requirement: '合作单位证明函或项目落地照片、视频等佐证材料' })
  } else if (name.includes('职业规划')) {
    base.push({ type: '职业规划书', requirement: '个人职业发展路径规划，包含自我分析、目标设定和行动计划' })
    base.push({ type: '实践证明', requirement: '实习、志愿服务、社团活动等相关证明材料' })
  } else {
    base.push({ type: '路演PPT', requirement: '不超过15页，重点展示项目创新点和商业价值' })
  }
  return base
}

const loadDetail = async () => {
  let compName = competition.value.name
  let compLevel = competition.value.level
  let rs = competition.value.registrationStart
  let re = competition.value.registrationEnd
  let cs = competition.value.competitionStart
  let ce = competition.value.competitionEnd

  try {
    const res = await getPublicCompetitionDetail(route.params.id)
    if (res.code === 200) {
      const data = res.data
      hasRegistered.value = data.has_registered || false

      const levelTypeMap = { '国家级': 'danger', '省级': 'warning' }
      const statusTextMap = { active: '报名中', upcoming: '即将开始', ended: '已结束' }
      const statusTypeMap = { active: 'success', upcoming: 'info', ended: 'info' }

      const localImage = getLocalImage(data.name)

      if (data.name) compName = data.name
      if (data.level) compLevel = data.level
      if (data.registration_start) rs = data.registration_start.split('T')[0]
      if (data.registration_end) re = data.registration_end.split('T')[0]
      if (data.competition_start) cs = data.competition_start.split('T')[0]
      if (data.competition_end) ce = data.competition_end.split('T')[0]

      competition.value = {
        ...competition.value,
        ...data,
        localImage: posterError.value ? null : localImage,
        endDate: data.registration_end ? data.registration_end.split('T')[0] : competition.value.endDate,
        levelType: levelTypeMap[data.level] || competition.value.levelType || 'success',
        statusText: statusTextMap[data.status] || competition.value.statusText || '报名中',
        statusType: statusTypeMap[data.status] || competition.value.statusType || 'success',
        registrationStart: rs,
        registrationEnd: re,
        competitionStart: cs,
        competitionEnd: ce,
        gradient: 'linear-gradient(135deg, #0c4a6e 0%, #075985 50%, #0ea5e9 100%)'
      }

      // 始终使用生成的完整数据，不依赖API返回的空数组
    }
  } catch(e) {
    console.error('获取竞赛详情失败，使用默认数据', e)
  }

  // 强制重新生成完整的时间安排、奖项设置和材料要求
  competition.value.schedule = getScheduleForCompetition(compName, rs, re, cs, ce)
  competition.value.awards = getAwardsForCompetition(compName, compLevel)
  competition.value.materials = getMaterialsForCompetition(compName)
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

.detail-poster {
  position: relative;
  width: 100%;
  background: linear-gradient(135deg, #0c4a6e 0%, #075985 50%, #0ea5e9 100%);
  border: none;
  padding: 0;
}

.detail-poster.has-image {
  background: #0f172a;
}

.poster-img {
  width: 100%;
  height: auto;
  object-fit: contain;
  display: block;
  aspect-ratio: 16 / 9;
}

.poster-fallback {
  width: 100%;
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px 40px;
}

.poster-fallback-content {
  text-align: center;
  color: #ffffff;
}

.poster-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 40px 40px 30px;
  background: linear-gradient(to top, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.5) 60%, transparent 100%);
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  flex-wrap: wrap;
  gap: 20px;
}

.poster-info {
  flex: 1;
  color: #ffffff;
}

.poster-tags {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.category-tag {
  background-color: rgba(255, 255, 255, 0.9);
  color: #1e293b;
  border: none;
}

.poster-title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 8px;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
  line-height: 1.3;
}

.poster-organizer {
  font-size: 15px;
  color: #bae6fd;
  margin-bottom: 12px;
}

.poster-stats {
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

.poster-action {
  flex-shrink: 0;
}

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
  min-width: 100px;
  text-align: center;
  flex-shrink: 0;
}

.award-first { background: linear-gradient(135deg, #f59e0b, #fbbf24); }
.award-second { background: linear-gradient(135deg, #94a3b8, #cbd5e1); }
.award-third { background: linear-gradient(135deg, #b45309, #d97706); }
.award-excellent { background: linear-gradient(135deg, #0ea5e9, #38bdf8); }
.award-creative { background: linear-gradient(135deg, #8b5cf6, #a78bfa); }
.award-teamwork { background: linear-gradient(135deg, #10b981, #34d399); }

.award-prize {
  font-size: 14px;
  font-weight: 500;
  color: #1e293b;
}

.award-count {
  font-size: 13px;
  color: #64748b;
}

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

.timeline-time {
  font-size: 13px;
  color: #0ea5e9;
  font-weight: 500;
}

.timeline-desc {
  font-size: 13px;
  color: #64748b;
  margin-top: 4px;
  line-height: 1.5;
}
</style>
