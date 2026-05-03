<template>
  <div class="agent-panel" :class="{ 'agent-panel--compact': compact }">
    <div v-if="!selectedCapability" class="capability-cards">
      <div class="capability-cards__title">🤖 项目智能体</div>
      <div class="capability-cards__desc">选择一个 AI 能力，让我来帮你</div>
      <div class="capability-cards__grid">
        <div
          v-for="cap in capabilities"
          :key="cap.key"
          class="capability-card"
          @click="selectCapability(cap)"
        >
          <div class="capability-card__icon">{{ cap.icon }}</div>
          <div class="capability-card__name">{{ cap.name }}</div>
          <div v-if="compact" class="capability-card__desc">{{ cap.brief }}</div>
        </div>
      </div>

      <div class="smart-navigate-section">
        <div class="smart-navigate-title">🧭 智能引航</div>
        <div class="smart-navigate-desc">告诉我你想做什么，我帮你快速到达</div>
        <div class="smart-navigate-input">
          <el-input
            v-model="navigateInput"
            placeholder="例如：我想报名互联网+比赛"
            size="small"
            @keyup.enter="doNavigate"
          >
            <template #append>
              <el-button :loading="navigateLoading" @click="doNavigate">出发</el-button>
            </template>
          </el-input>
        </div>
        <div v-if="navigateResult" class="navigate-result">
          <div class="navigate-reply">{{ navigateResult.reply }}</div>
          <el-button
            v-if="navigateResult.action === 'navigate' && navigateResult.route"
            type="primary"
            size="small"
            @click="goToRoute(navigateResult.route)"
          >
            前往 {{ navigateResult.label }} →
          </el-button>
        </div>
      </div>
    </div>

    <div v-else class="capability-form">
      <div class="capability-form__header">
        <el-button type="primary" link size="small" @click="goBack">← 返回</el-button>
        <span class="capability-form__title">{{ selectedCapability.icon }} {{ selectedCapability.name }}</span>
      </div>

      <div class="capability-form__body">
        <el-form label-position="top" size="small">
          <el-form-item
            v-if="needsProject"
            label="请输入项目名称"
            :required="needsProjectRequired"
          >
            <el-input
              v-model="form.projectName"
              placeholder="例如：智能垃圾分类助手"
              style="width: 100%"
            />
          </el-form-item>

          <el-form-item
            v-if="needsProject && projects.length > 0"
            label="或从已有项目中选择"
          >
            <el-select
              v-model="form.projectId"
              placeholder="选择已有项目"
              clearable
              teleported="false"
              style="width: 100%"
              @change="onProjectSelect"
            >
              <el-option
                v-for="p in projects"
                :key="p.id"
                :label="p.name"
                :value="p.id"
              />
            </el-select>
          </el-form-item>

          <el-form-item
            v-if="selectedCapability.key === 'material_qa' || selectedCapability.key === 'bp_check'"
            label="选择报名（可选）"
          >
            <el-select
              v-model="form.registrationId"
              placeholder="可选，优先从报名材料检索"
              clearable
              teleported="false"
              style="width: 100%"
            >
              <el-option
                v-for="r in registrations"
                :key="r.id"
                :label="r.competition_name || `报名 #${r.id}`"
                :value="r.id"
              />
            </el-select>
          </el-form-item>

          <el-form-item v-if="selectedCapability.key === 'material_qa'" label="您的问题" required>
            <el-input
              v-model="form.question"
              type="textarea"
              :rows="2"
              placeholder="例如：这个项目的创新点是什么？商业模式有什么问题？"
            />
          </el-form-item>

          <el-form-item v-if="selectedCapability.key === 'roadshow'" label="路演时长">
            <el-radio-group v-model="form.duration">
              <el-radio :value="3">3 分钟</el-radio>
              <el-radio :value="5">5 分钟</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item v-if="selectedCapability.key === 'roadshow'" label="路演风格">
            <el-radio-group v-model="form.style">
              <el-radio value="formal">正式专业</el-radio>
              <el-radio value="passionate">激情澎湃</el-radio>
              <el-radio value="concise">简洁精炼</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item v-if="selectedCapability.key === 'project_idea'" label="竞赛名称（可选）">
            <el-input v-model="form.competitionName" placeholder="例如：互联网+、挑战杯" />
          </el-form-item>

          <el-form-item v-if="selectedCapability.key === 'project_idea'" label="竞赛类别（可选）">
            <el-input v-model="form.competitionCategory" placeholder="例如：科技创新、创业实践" />
          </el-form-item>

          <el-form-item v-if="selectedCapability.key === 'project_idea'" label="赛道（可选）">
            <el-input v-model="form.track" placeholder="例如：人工智能、生物医药" />
          </el-form-item>

          <el-form-item v-if="selectedCapability.key === 'project_idea'" label="你的技能特长（可选）">
            <el-input v-model="form.skills" type="textarea" :rows="2" placeholder="例如：Python、机器学习、产品设计" />
          </el-form-item>

          <el-form-item v-if="selectedCapability.key === 'project_idea'" label="兴趣方向（可选）">
            <el-input v-model="form.interests" type="textarea" :rows="2" placeholder="例如：智慧医疗、绿色能源、教育科技" />
          </el-form-item>

          <el-form-item v-if="selectedCapability.key === 'mock_defense'" label="提问风格">
            <el-radio-group v-model="form.questionType">
              <el-radio value="general">综合提问</el-radio>
              <el-radio value="technical">技术深度</el-radio>
              <el-radio value="business">商业提问</el-radio>
              <el-radio value="tough">压力提问</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item v-if="selectedCapability.key === 'smart_feedback'" label="反馈类型">
            <el-radio-group v-model="form.feedbackType">
              <el-radio value="modify">建议修改</el-radio>
              <el-radio value="approve">建议通过</el-radio>
              <el-radio value="reject">建议驳回</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item
            v-if="needsProject && !indexExists && needsIndex"
            label=""
          >
            <el-button
              type="warning"
              size="small"
              :loading="indexing"
              @click="doIndex"
              style="width: 100%"
            >
              {{ indexing ? '正在索引材料...' : '建立材料索引' }}
            </el-button>
          </el-form-item>
        </el-form>

        <el-button
          type="primary"
          size="small"
          :loading="loading"
          :disabled="!canExecute"
          @click="execute"
          style="width: 100%; margin-top: 8px"
        >
          {{ loading ? 'AI 分析中...' : '执行分析' }}
        </el-button>
      </div>

      <div v-if="result" class="capability-result">
        <div v-if="result.is_fallback" class="capability-result__fallback">
          ⚠️ AI 服务不可用，已使用模板分析
        </div>

        <div v-if="result.disclaimer" class="capability-result__disclaimer">
          {{ result.disclaimer }}
        </div>

        <div
          v-if="resultHtml"
          class="capability-result__content markdown-body"
          v-html="resultHtml"
        />

        <div v-if="result.sources && result.sources.length" class="capability-result__sources">
          <div class="capability-result__sources-title">参考来源：</div>
          <el-tag
            v-for="src in result.sources"
            :key="src.file_name"
            size="small"
            type="info"
            style="margin: 2px 4px"
          >
            {{ src.file_name }}
          </el-tag>
        </div>

        <div class="capability-result__actions">
          <el-button size="small" @click="copyResult">
            <el-icon><DocumentCopy /></el-icon> 复制
          </el-button>
          <el-button size="small" @click="speakResult">
            <el-icon><Microphone /></el-icon> 朗读
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { DocumentCopy, Microphone } from '@element-plus/icons-vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import {
  indexMaterials,
  materialQa,
  bpCheck,
  generateRoadshow,
  reviewAssist,
  competitionRecommend,
  smartNavigate,
  projectIdea,
  mockDefense,
  batchReview,
  smartFeedback,
  reviewDraft,
  scoreCheck,
  getCapabilities,
} from '@/api/agent'
import { getProjects } from '@/api/project'

const router = useRouter()

const props = defineProps({
  userRole: { type: String, default: 'student' },
  initialContext: { type: Object, default: () => ({}) },
  compact: { type: Boolean, default: false },
})

const emit = defineEmits(['result', 'speak', 'navigate'])

const ALL_CAPABILITIES = [
  { key: 'smart_navigate', name: '智能引航', icon: '🧭', brief: '模糊指令跳转', roles: ['student', 'teacher', 'judge', 'admin'], noProject: true },
  { key: 'material_qa', name: 'AI 材料问答', icon: '📄', brief: '基于材料问答', roles: ['student', 'teacher', 'judge', 'admin'] },
  { key: 'bp_check', name: '商业计划书体检', icon: '🏥', brief: '检查完整性', roles: ['student', 'teacher', 'judge', 'admin'] },
  { key: 'roadshow', name: '路演稿生成', icon: '🎤', brief: '生成路演稿', roles: ['student', 'teacher', 'admin'] },
  { key: 'review_assist', name: 'AI 评审辅助', icon: '📋', brief: '评审参考', roles: ['teacher', 'judge', 'admin'] },
  { key: 'competition_recommend', name: '智能竞赛推荐', icon: '🎯', brief: '推荐竞赛', roles: ['student', 'admin'] },
  { key: 'project_idea', name: '项目创意生成', icon: '💡', brief: '生成项目创意', roles: ['student', 'admin'], noProject: true },
  { key: 'mock_defense', name: '模拟路演答辩', icon: '🎓', brief: 'AI模拟评委', roles: ['student', 'teacher', 'admin'] },
  { key: 'batch_review', name: '批量审核助手', icon: '📑', brief: '批量审核分析', roles: ['teacher', 'admin'], noProject: true },
  { key: 'smart_feedback', name: '智能反馈生成', icon: '✏️', brief: '生成反馈意见', roles: ['teacher', 'admin'] },
  { key: 'review_draft', name: '评审意见草稿', icon: '📝', brief: '生成评审草稿', roles: ['judge', 'admin'] },
  { key: 'score_check', name: '评分一致性检查', icon: '✅', brief: '检查评分一致性', roles: ['judge', 'admin'], noProject: true },
]

const capabilities = computed(() =>
  ALL_CAPABILITIES.filter(c => c.roles.includes(props.userRole))
)

const selectedCapability = ref(null)
const projects = ref([])
const projectsLoading = ref(false)
const registrations = ref([])
const loading = ref(false)
const indexing = ref(false)
const indexExists = ref(false)
const result = ref(null)

const navigateInput = ref('')
const navigateLoading = ref(false)
const navigateResult = ref(null)

const form = ref({
  projectId: null,
  projectName: '',
  registrationId: null,
  question: '',
  duration: 3,
  style: 'formal',
  competitionName: '',
  competitionCategory: '',
  track: '',
  skills: '',
  interests: '',
  questionType: 'general',
  feedbackType: 'modify',
})

const needsProject = computed(() => {
  if (!selectedCapability.value) return false
  return !selectedCapability.value.noProject
})

const needsProjectRequired = computed(() => {
  if (!selectedCapability.value) return false
  const key = selectedCapability.value.key
  return !['mock_defense'].includes(key)
})

const needsIndex = computed(() => {
  if (!selectedCapability.value) return false
  const key = selectedCapability.value.key
  return ['material_qa', 'bp_check', 'review_assist', 'smart_feedback', 'review_draft'].includes(key)
})

const resultHtml = computed(() => {
  if (!result.value) return ''
  const text = result.value.answer || result.value.report || result.value.script || result.value.analysis || result.value.recommendation || result.value.ideas || result.value.defense || result.value.feedback || result.value.draft || ''
  if (!text) return ''
  return DOMPurify.sanitize(marked.parse(text))
})

const canExecute = computed(() => {
  if (loading.value) return false
  if (needsProjectRequired.value && !form.value.projectId && !form.value.projectName.trim()) return false
  if (selectedCapability.value?.key === 'material_qa' && !form.value.question.trim()) return false
  return true
})

function selectCapability(cap) {
  if (cap.key === 'smart_navigate') {
    selectedCapability.value = null
    return
  }
  selectedCapability.value = cap
  result.value = null
}

function goBack() {
  selectedCapability.value = null
  result.value = null
}

function goToRoute(route) {
  if (route) {
    emit('navigate', route)
    router.push(route).catch(() => {})
  }
}

async function doNavigate() {
  if (!navigateInput.value.trim()) {
    ElMessage.warning('请输入你想做的事情')
    return
  }
  navigateLoading.value = true
  navigateResult.value = null
  try {
    const res = await smartNavigate({ message: navigateInput.value })
    const d = res.data || res
    navigateResult.value = d
    if (d.action === 'navigate' && d.route) {
      emit('navigate', d.route)
    }
  } catch (e) {
    ElMessage.error('智能引航失败：' + (e.response?.data?.message || e.message))
  } finally {
    navigateLoading.value = false
  }
}

async function fetchProjects() {
  try {
    const res = await getProjects({ page: 1, per_page: 100 })
    projects.value = res.data?.projects || res.projects || []
  } catch (e) {
    console.error('获取项目列表失败:', e)
  }
}

async function searchProjects(query) {
  if (!query) {
    await fetchProjects()
    return
  }
  projectsLoading.value = true
  try {
    const res = await getProjects({ page: 1, per_page: 50, search: query })
    projects.value = res.data?.projects || res.projects || []
  } catch (e) {
    console.error('搜索项目失败:', e)
  } finally {
    projectsLoading.value = false
  }
}

async function onProjectChange(projectId) {
    indexExists.value = false
    form.value.registrationId = null
    registrations.value = []
  }

  function onProjectSelect(projectId) {
    if (projectId) {
      const p = projects.value.find(item => item.id === projectId)
      if (p) {
        form.value.projectName = p.name
      }
    }
    onProjectChange(projectId)
  }

async function doIndex() {
  if (!form.value.projectId) {
    ElMessage.warning('请先选择项目')
    return
  }
  indexing.value = true
  try {
    const data = { source_type: 'project', project_id: form.value.projectId, force_reindex: true }
    const res = await indexMaterials(data)
    indexExists.value = true
    const d = res.data || res
    ElMessage.success(`索引完成：${d.indexed_files || 0} 个文件已索引，${d.skipped_files || 0} 个跳过`)
  } catch (e) {
    ElMessage.error('索引失败：' + (e.response?.data?.message || e.message))
  } finally {
    indexing.value = false
  }
}

async function execute() {
  if (!canExecute.value) return
  loading.value = true
  result.value = null

  try {
    let res
    const capKey = selectedCapability.value.key
    const baseData = { project_id: form.value.projectId }

    switch (capKey) {
      case 'material_qa':
        res = await materialQa({
          ...baseData,
          question: form.value.question,
          registration_id: form.value.registrationId || undefined,
        })
        break
      case 'bp_check':
        res = await bpCheck({
          ...baseData,
          registration_id: form.value.registrationId || undefined,
        })
        break
      case 'roadshow':
        res = await generateRoadshow({
          ...baseData,
          duration: form.value.duration,
          style: form.value.style,
        })
        break
      case 'review_assist':
        res = await reviewAssist(baseData)
        break
      case 'competition_recommend':
        res = await competitionRecommend(baseData)
        break
      case 'project_idea':
        res = await projectIdea({
          competition_name: form.value.competitionName,
          competition_category: form.value.competitionCategory,
          track: form.value.track,
          skills: form.value.skills,
          interests: form.value.interests,
        })
        break
      case 'mock_defense':
        res = await mockDefense({
          ...baseData,
          question_type: form.value.questionType,
        })
        break
      case 'batch_review':
        res = await batchReview({})
        break
      case 'smart_feedback':
        res = await smartFeedback({
          ...baseData,
          feedback_type: form.value.feedbackType,
        })
        break
      case 'review_draft':
        res = await reviewDraft(baseData)
        break
      case 'score_check':
        res = await scoreCheck({
          review_data: form.value.reviewData || {},
        })
        break
    }

    const d = res.data || res
    result.value = d
    emit('result', getResultText(d))
  } catch (e) {
    const msg = e.response?.data?.message || e.message || '执行失败'
    ElMessage.error(msg)
  } finally {
    loading.value = false
  }
}

function getResultText(d) {
  return d.answer || d.report || d.script || d.analysis || d.recommendation || d.ideas || d.defense || d.feedback || d.draft || ''
}

function copyResult() {
  const text = getResultText(result.value)
  if (!text) return
  navigator.clipboard.writeText(text).then(() => {
    ElMessage.success('已复制到剪贴板')
  }).catch(() => {
    ElMessage.error('复制失败')
  })
}

function speakResult() {
  const text = getResultText(result.value)
  if (!text) return
  emit('speak', text)
}

watch(() => props.initialContext, (ctx) => {
  if (!ctx) return
  if (ctx.capability) {
    const cap = ALL_CAPABILITIES.find(c => c.key === ctx.capability)
    if (cap && cap.roles.includes(props.userRole)) {
      selectedCapability.value = cap
    }
  }
  if (ctx.projectId) {
    form.value.projectId = ctx.projectId
  }
  if (ctx.registrationId) {
    form.value.registrationId = ctx.registrationId
  }
}, { immediate: true, deep: true })

onMounted(() => {
  fetchProjects()
})
</script>

<style scoped>
.agent-panel {
  padding: 8px;
  height: 100%;
  display: flex;
  flex-direction: column;
  color: #e2e8f0;
}

.agent-panel--compact {
  padding: 4px;
  font-size: 13px;
}

.agent-panel :deep(.el-form-item__label) {
  color: #94a3b8 !important;
  font-size: 12px;
}

.agent-panel :deep(.el-select .el-input__inner),
.agent-panel :deep(.el-input .el-input__inner),
.agent-panel :deep(.el-textarea .el-textarea__inner) {
  color: #e2e8f0 !important;
  background-color: transparent !important;
  border-color: rgba(6, 182, 212, 0.3) !important;
}

.agent-panel :deep(.el-select .el-input__inner::placeholder),
.agent-panel :deep(.el-input .el-input__inner::placeholder),
.agent-panel :deep(.el-textarea .el-textarea__inner::placeholder) {
  color: #64748b !important;
}

.agent-panel :deep(.el-radio__label) {
  color: #e2e8f0 !important;
}

.agent-panel :deep(.el-select-dropdown__item) {
  color: #e2e8f0 !important;
}

.agent-panel :deep(.el-select-dropdown) {
  background-color: rgba(15, 23, 42, 0.95) !important;
  border: 1px solid rgba(6, 182, 212, 0.3) !important;
}

.agent-panel :deep(.el-select-dropdown__item.hover),
.agent-panel :deep(.el-select-dropdown__item:hover) {
  background-color: rgba(6, 182, 212, 0.15) !important;
}

.agent-panel :deep(.el-select-dropdown__item.selected) {
  color: #06b6d4 !important;
  font-weight: 600;
}

.agent-panel :deep(.el-popper.is-light) {
  background-color: rgba(15, 23, 42, 0.95) !important;
  border: 1px solid rgba(6, 182, 212, 0.3) !important;
}

.agent-panel :deep(.el-popper.is-light .el-popper__arrow::before) {
  background-color: rgba(15, 23, 42, 0.95) !important;
  border-color: rgba(6, 182, 212, 0.3) !important;
}

.smart-navigate-section :deep(.el-input-group__append) {
  background-color: rgba(6, 182, 212, 0.2) !important;
  border-color: rgba(6, 182, 212, 0.3) !important;
  color: #06b6d4 !important;
  box-shadow: none !important;
}

.smart-navigate-section :deep(.el-input-group__append:hover) {
  background-color: rgba(6, 182, 212, 0.3) !important;
}

.capability-cards__title {
  font-size: 14px;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 4px;
  text-align: center;
}

.capability-cards__desc {
  font-size: 12px;
  color: #94a3b8;
  text-align: center;
  margin-bottom: 8px;
}

.capability-cards__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 6px;
}

.agent-panel--compact .capability-cards__grid {
  grid-template-columns: repeat(2, 1fr);
  gap: 4px;
}

.capability-card {
  padding: 10px 6px;
  border: 1px solid rgba(6, 182, 212, 0.2);
  border-radius: 8px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  background: rgba(15, 23, 42, 0.6);
}

.capability-card:hover {
  border-color: #06b6d4;
  background: rgba(6, 182, 212, 0.15);
  transform: translateY(-1px);
}

.capability-card__icon {
  font-size: 22px;
  margin-bottom: 4px;
}

.capability-card__name {
  font-size: 11px;
  color: #e2e8f0;
  font-weight: 500;
}

.capability-card__desc {
  font-size: 11px;
  color: #94a3b8;
  margin-top: 2px;
}

.smart-navigate-section {
  margin-top: 12px;
  padding: 10px;
  background: linear-gradient(135deg, rgba(6, 182, 212, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
  border-radius: 10px;
  border: 1px solid rgba(6, 182, 212, 0.2);
}

.smart-navigate-title {
  font-size: 14px;
  font-weight: 600;
  color: #06b6d4;
  margin-bottom: 2px;
}

.smart-navigate-desc {
  font-size: 11px;
  color: #94a3b8;
  margin-bottom: 8px;
}

.smart-navigate-input {
  width: 100%;
}

.navigate-result {
  margin-top: 8px;
  padding: 8px;
  background: rgba(15, 23, 42, 0.6);
  border-radius: 6px;
  border: 1px solid rgba(6, 182, 212, 0.2);
}

.navigate-reply {
  font-size: 13px;
  color: #e2e8f0;
  margin-bottom: 6px;
}

.capability-form__header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  padding-bottom: 6px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.capability-form__title {
  font-size: 14px;
  font-weight: 600;
  color: #e2e8f0;
}

.capability-form__body {
  flex: 0 0 auto;
}

.capability-result {
  margin-top: 10px;
  flex: 1;
  overflow-y: auto;
  max-height: 300px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 8px;
}

.agent-panel--compact .capability-result {
  max-height: 200px;
}

.capability-result__fallback {
  background: rgba(230, 162, 60, 0.15);
  color: #f59e0b;
  padding: 6px 10px;
  border-radius: 4px;
  font-size: 12px;
  margin-bottom: 8px;
}

.capability-result__disclaimer {
  background: rgba(239, 68, 68, 0.15);
  color: #f87171;
  padding: 6px 10px;
  border-radius: 4px;
  font-size: 12px;
  margin-bottom: 8px;
  font-weight: 500;
}

.capability-result__content {
  font-size: 13px;
  line-height: 1.6;
  color: #e2e8f0;
  word-break: break-word;
}

.capability-result__content :deep(h1),
.capability-result__content :deep(h2),
.capability-result__content :deep(h3),
.capability-result__content :deep(h4),
.capability-result__content :deep(h5),
.capability-result__content :deep(h6) {
  margin: 6px 0 2px;
  font-size: 14px;
  font-weight: 600;
  color: #e2e8f0;
}

.capability-result__content :deep(ul),
.capability-result__content :deep(ol) {
  padding-left: 16px;
  margin: 4px 0;
}

.capability-result__content :deep(li) {
  color: #e2e8f0;
}

.capability-result__content :deep(p) {
  margin: 4px 0;
  color: #e2e8f0;
}

.capability-result__content :deep(strong) {
  color: #22d3ee;
}

.capability-result__content :deep(table) {
  color: #e2e8f0;
}

.capability-result__content :deep(th) {
  color: #06b6d4;
  background: rgba(6, 182, 212, 0.15);
}

.capability-result__content :deep(td) {
  color: #e2e8f0;
}

.capability-result__content :deep(code) {
  color: #22d3ee;
  background: rgba(6, 182, 212, 0.1);
}

.capability-result__sources {
  margin-top: 8px;
  padding-top: 6px;
  border-top: 1px dashed rgba(255, 255, 255, 0.15);
}

.capability-result__sources-title {
  font-size: 12px;
  color: #94a3b8;
  margin-bottom: 4px;
}

.capability-result__actions {
  margin-top: 8px;
  display: flex;
  gap: 6px;
}
</style>
