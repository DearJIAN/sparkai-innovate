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
            label="选择项目"
            :required="needsProjectRequired"
          >
            <el-select
              v-model="form.projectId"
              placeholder="请选择一个项目"
              clearable
              filterable
              :teleported="false"
              style="width: 100%"
              :loading="projectsLoading"
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
              :teleported="false"
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
              <el-radio :label="3">3分钟</el-radio>
              <el-radio :label="5">5分钟</el-radio>
              <el-radio :label="8">8分钟</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item v-if="selectedCapability.key === 'roadshow'" label="风格">
            <el-radio-group v-model="form.style">
              <el-radio label="formal">正式</el-radio>
              <el-radio label="passionate">激情</el-radio>
              <el-radio label="story">故事</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item v-if="selectedCapability.key === 'competition_recommend'" label="竞赛名称（可选）">
            <el-input v-model="form.competitionName" placeholder="输入竞赛名称或方向，留空则推荐所有" />
          </el-form-item>

          <el-form-item v-if="selectedCapability.key === 'competition_recommend'" label="竞赛类别">
            <el-select v-model="form.competitionCategory" placeholder="选择类别" clearable>
              <el-option label="全部" value="" />
              <el-option label="创新创业" value="创新创业" />
              <el-option label="人工智能" value="人工智能" />
              <el-option label="数字经济" value="数字经济" />
              <el-option label="乡村振兴" value="乡村振兴" />
              <el-option label="产业命题" value="产业命题" />
            </el-select>
          </el-form-item>

          <el-form-item v-if="selectedCapability.key === 'competition_recommend'" label="赛道方向">
            <el-input v-model="form.track" placeholder="例如：人工智能、生物医药、新能源" />
          </el-form-item>

          <el-form-item v-if="selectedCapability.key === 'project_idea'" label="技能方向">
            <el-input v-model="form.skills" placeholder="例如：Python、产品设计、市场营销" />
          </el-form-item>

          <el-form-item v-if="selectedCapability.key === 'project_idea'" label="兴趣领域">
            <el-input v-model="form.interests" placeholder="例如：环保、教育、医疗" />
          </el-form-item>

          <el-form-item v-if="selectedCapability.key === 'mock_defense'" label="问题类型">
            <el-radio-group v-model="form.questionType">
              <el-radio label="general">通用</el-radio>
              <el-radio label="technical">技术</el-radio>
              <el-radio label="business">商业</el-radio>
              <el-radio label="challenge">挑战</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item v-if="selectedCapability.key === 'smart_feedback'" label="反馈类型">
            <el-radio-group v-model="form.feedbackType">
              <el-radio label="modify">修改建议</el-radio>
              <el-radio label="encourage">鼓励指导</el-radio>
              <el-radio label="question">提问引导</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item v-if="needsIndex" label="材料索引">
            <div class="index-status">
              <el-button
                :loading="indexing"
                size="small"
                type="warning"
                @click="doIndex"
              >
                {{ indexExists ? '重新建立索引' : '建立材料索引' }}
              </el-button>
              <span v-if="indexExists" class="index-ok">✅ 索引已建立</span>
              <span v-else class="index-tip">请先建立索引，再执行分析</span>
            </div>
          </el-form-item>

          <div class="capability-actions">
            <el-button
              type="primary"
              :loading="loading"
              :disabled="!canExecute"
              @click="execute"
            >
              执行分析
            </el-button>
          </div>
        </el-form>

        <div v-if="result" class="capability-result">
          <div class="capability-result__title">📊 分析结果</div>
          <div class="capability-result__content" v-html="resultHtml" />
          <div class="capability-result__actions">
            <el-button size="small" @click="copyResult">复制</el-button>
            <el-button size="small" @click="speakResult">朗读</el-button>
            <el-button size="small" @click="saveResult">保存</el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import DOMPurify from 'dompurify'
import { marked } from 'marked'
import {
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
  const raw = result.value.answer || result.value.report || result.value.script || result.value.analysis || result.value.recommendation || result.value.ideas || result.value.defense || result.value.feedback || result.value.draft || ''
  const text = typeof raw === 'string' ? raw : JSON.stringify(raw, null, 2)
  if (!text) return ''
  return DOMPurify.sanitize(marked.parse(text))
})

const canExecute = computed(() => {
  if (loading.value) return false
  if (needsProjectRequired.value && !form.value.projectId) return false
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
    ElMessage.error('导航失败：' + (e.response?.data?.message || e.message))
  } finally {
    navigateLoading.value = false
  }
}

async function fetchProjects() {
  projectsLoading.value = true
  try {
    const res = await getProjects({ page: 1, per_page: 100 })
    let list = []
    if (res.data && res.data.projects) {
      list = res.data.projects
    } else if (res.projects) {
      list = res.projects
    } else if (Array.isArray(res.data)) {
      list = res.data
    } else if (Array.isArray(res)) {
      list = res
    }
    console.log('[AgentPanel] fetchProjects got', list.length, 'projects')
    projects.value = list
  } catch (e) {
    console.error('获取项目列表失败:', e)
    projects.value = []
  } finally {
    projectsLoading.value = false
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
    } else {
      form.value.projectName = ''
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
    const msg = e.response?.data?.message || e.message || '未知错误'
    if (msg.includes('暂无上传文件') || msg.includes('暂无上传材料')) {
      ElMessage.warning('该项目暂无上传文件，请先在"材料中心"上传项目文件后再建立索引')
    } else {
      ElMessage.error('索引失败：' + msg)
    }
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
    const key = selectedCapability.value.key

    switch (key) {
      case 'material_qa':
        res = await materialQa({
          project_id: form.value.projectId,
          registration_id: form.value.registrationId,
          question: form.value.question,
        })
        break
      case 'bp_check':
        res = await bpCheck({ project_id: form.value.projectId })
        break
      case 'roadshow':
        res = await generateRoadshow({
          project_id: form.value.projectId,
          duration: form.value.duration,
          style: form.value.style,
        })
        break
      case 'review_assist':
        res = await reviewAssist({ project_id: form.value.projectId })
        break
      case 'competition_recommend':
        res = await competitionRecommend({
          competition_name: form.value.competitionName,
          category: form.value.competitionCategory,
          track: form.value.track,
        })
        break
      case 'project_idea':
        res = await projectIdea({
          skills: form.value.skills,
          interests: form.value.interests,
        })
        break
      case 'mock_defense':
        res = await mockDefense({
          project_id: form.value.projectId,
          question_type: form.value.questionType,
        })
        break
      case 'batch_review':
        res = await batchReview({})
        break
      case 'smart_feedback':
        res = await smartFeedback({
          project_id: form.value.projectId,
          feedback_type: form.value.feedbackType,
        })
        break
      case 'review_draft':
        res = await reviewDraft({ project_id: form.value.projectId })
        break
      case 'score_check':
        res = await scoreCheck({})
        break
      default:
        ElMessage.warning('未知能力')
        return
    }

    result.value = res.data || res
    emit('result', result.value)
  } catch (e) {
    ElMessage.error('执行失败：' + (e.response?.data?.message || e.message))
  } finally {
    loading.value = false
  }
}

function copyResult() {
  const text = result.value?.answer || result.value?.report || result.value?.script || result.value?.analysis || result.value?.recommendation || result.value?.ideas || result.value?.defense || result.value?.feedback || result.value?.draft || ''
  if (!text) return
  navigator.clipboard.writeText(text).then(() => {
    ElMessage.success('已复制到剪贴板')
  }).catch(() => {
    ElMessage.error('复制失败')
  })
}

function speakResult() {
  const text = result.value?.answer || result.value?.report || result.value?.script || result.value?.analysis || result.value?.recommendation || result.value?.ideas || result.value?.defense || result.value?.feedback || result.value?.draft || ''
  if (!text) return
  emit('speak', text)
}

function saveResult() {
  ElMessage.info('保存功能开发中')
}

watch(() => props.initialContext, (ctx) => {
  if (!ctx) return
  if (ctx.projectId) {
    form.value.projectId = ctx.projectId
  }
  if (ctx.projectName) {
    form.value.projectName = ctx.projectName
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
  color: #1e293b !important;
  background-color: #ffffff !important;
  border-color: rgba(6, 182, 212, 0.3) !important;
}

.agent-panel :deep(.el-input__wrapper) {
  background-color: #ffffff !important;
  box-shadow: 0 0 0 1px rgba(6, 182, 212, 0.3) inset !important;
}

.agent-panel :deep(.el-textarea__wrapper) {
  background-color: #ffffff !important;
  box-shadow: 0 0 0 1px rgba(6, 182, 212, 0.3) inset !important;
}

.agent-panel :deep(.el-select .el-input__inner::placeholder),
.agent-panel :deep(.el-input .el-input__inner::placeholder),
.agent-panel :deep(.el-textarea .el-textarea__inner::placeholder) {
  color: #94a3b8 !important;
}

.agent-panel :deep(.el-radio__label) {
  color: #e2e8f0 !important;
}

.agent-panel :deep(.el-select-dropdown__item) {
  color: #1e293b !important;
}

.agent-panel :deep(.el-select-dropdown) {
  background-color: #ffffff !important;
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
  background-color: #ffffff !important;
  border: 1px solid rgba(6, 182, 212, 0.3) !important;
}

.agent-panel :deep(.el-popper.is-light .el-popper__arrow::before) {
  background-color: #ffffff !important;
  border-color: rgba(6, 182, 212, 0.3) !important;
}

.agent-panel :deep(.el-select-dropdown__empty) {
  color: #94a3b8 !important;
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
  background: rgba(6, 182, 212, 0.08);
  border: 1px solid rgba(6, 182, 212, 0.15);
  border-radius: 8px;
  padding: 8px 4px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
}

.capability-card:hover {
  background: rgba(6, 182, 212, 0.15);
  border-color: rgba(6, 182, 212, 0.3);
  transform: translateY(-1px);
}

.capability-card__icon {
  font-size: 20px;
  margin-bottom: 2px;
}

.capability-card__name {
  font-size: 12px;
  color: #e2e8f0;
  font-weight: 500;
}

.capability-card__desc {
  font-size: 10px;
  color: #94a3b8;
  margin-top: 2px;
}

.smart-navigate-section {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid rgba(6, 182, 212, 0.1);
}

.smart-navigate-title {
  font-size: 13px;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 2px;
}

.smart-navigate-desc {
  font-size: 11px;
  color: #94a3b8;
  margin-bottom: 6px;
}

.smart-navigate-input {
  margin-bottom: 8px;
}

.navigate-result {
  background: rgba(6, 182, 212, 0.08);
  border: 1px solid rgba(6, 182, 212, 0.2);
  border-radius: 6px;
  padding: 8px;
  margin-top: 6px;
}

.navigate-reply {
  font-size: 12px;
  color: #e2e8f0;
  margin-bottom: 6px;
  line-height: 1.5;
}

.capability-form__header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.capability-form__title {
  font-size: 14px;
  font-weight: 600;
  color: #e2e8f0;
}

.capability-form__body {
  flex: 1;
  overflow-y: auto;
}

.capability-actions {
  margin-top: 8px;
  display: flex;
  justify-content: center;
}

.capability-result {
  margin-top: 12px;
  padding: 10px;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(6, 182, 212, 0.2);
  border-radius: 8px;
}

.capability-result__title {
  font-size: 13px;
  font-weight: 600;
  color: #06b6d4;
  margin-bottom: 6px;
}

.capability-result__content {
  font-size: 12px;
  line-height: 1.6;
  color: #e2e8f0;
}

.capability-result__content :deep(h1),
.capability-result__content :deep(h2),
.capability-result__content :deep(h3) {
  color: #06b6d4;
  margin: 8px 0 4px;
}

.capability-result__content :deep(p) {
  margin: 4px 0;
}

.capability-result__content :deep(ul),
.capability-result__content :deep(ol) {
  padding-left: 16px;
  margin: 4px 0;
}

.capability-result__content :deep(li) {
  margin: 2px 0;
}

.capability-result__content :deep(code) {
  background: rgba(6, 182, 212, 0.1);
  padding: 1px 4px;
  border-radius: 3px;
  font-size: 11px;
}

.capability-result__content :deep(pre) {
  background: rgba(6, 182, 212, 0.05);
  padding: 6px;
  border-radius: 4px;
  overflow-x: auto;
}

.index-status {
  display: flex;
  align-items: center;
  gap: 8px;
}

.index-ok {
  color: #10b981;
  font-size: 12px;
}

.index-tip {
  color: #f59e0b;
  font-size: 12px;
}

.capability-result__actions {
  margin-top: 8px;
  display: flex;
  gap: 6px;
}
</style>