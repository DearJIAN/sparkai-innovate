<template>
  <div class="agent-panel" :class="{ 'agent-panel--compact': compact }">
    <div v-if="!selectedCapability" class="capability-cards">
      <div class="capability-cards__title">项目智能体</div>
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
    </div>

    <div v-else class="capability-form">
      <div class="capability-form__header">
        <el-button type="primary" link size="small" @click="goBack">← 返回</el-button>
        <span class="capability-form__title">{{ selectedCapability.icon }} {{ selectedCapability.name }}</span>
      </div>

      <div class="capability-form__body">
        <el-form label-position="top" size="small">
          <el-form-item label="选择项目" required>
            <el-select
              v-model="form.projectId"
              placeholder="请选择项目"
              filterable
              style="width: 100%"
              @change="onProjectChange"
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
              filterable
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

          <el-form-item v-if="!indexExists" label="">
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
} from '@/api/agent'
import { getProjects } from '@/api/project'

const props = defineProps({
  userRole: { type: String, default: 'student' },
  initialContext: { type: Object, default: () => ({}) },
  compact: { type: Boolean, default: false },
})

const emit = defineEmits(['result', 'speak'])

const ALL_CAPABILITIES = [
  { key: 'material_qa', name: 'AI 材料问答', icon: '📄', brief: '基于材料问答', roles: ['student', 'teacher', 'judge', 'admin'] },
  { key: 'bp_check', name: '商业计划书体检', icon: '🏥', brief: '检查完整性', roles: ['student', 'teacher', 'judge', 'admin'] },
  { key: 'roadshow', name: '路演稿生成', icon: '🎤', brief: '生成路演稿', roles: ['student', 'teacher', 'admin'] },
  { key: 'review_assist', name: 'AI 评审辅助', icon: '📋', brief: '评审参考', roles: ['teacher', 'judge', 'admin'] },
  { key: 'competition_recommend', name: '智能竞赛推荐', icon: '🎯', brief: '推荐竞赛', roles: ['student', 'admin'] },
]

const capabilities = computed(() =>
  ALL_CAPABILITIES.filter(c => c.roles.includes(props.userRole))
)

const selectedCapability = ref(null)
const projects = ref([])
const registrations = ref([])
const loading = ref(false)
const indexing = ref(false)
const indexExists = ref(false)
const result = ref(null)

const form = ref({
  projectId: null,
  registrationId: null,
  question: '',
  duration: 3,
  style: 'formal',
})

const resultHtml = computed(() => {
  if (!result.value) return ''
  const text = result.value.answer || result.value.report || result.value.script || result.value.analysis || result.value.recommendation || ''
  if (!text) return ''
  return DOMPurify.sanitize(marked.parse(text))
})

const canExecute = computed(() => {
  if (loading.value) return false
  if (!form.value.projectId) return false
  if (selectedCapability.value?.key === 'material_qa' && !form.value.question.trim()) return false
  return true
})

function selectCapability(cap) {
  selectedCapability.value = cap
  result.value = null
}

function goBack() {
  selectedCapability.value = null
  result.value = null
}

async function fetchProjects() {
  try {
    const res = await getProjects({ page: 1, per_page: 100 })
    projects.value = res.projects || res.data?.projects || []
  } catch (e) {
    console.error('获取项目列表失败:', e)
  }
}

async function onProjectChange(projectId) {
  indexExists.value = false
  form.value.registrationId = null
  registrations.value = []
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
  return d.answer || d.report || d.script || d.analysis || d.recommendation || ''
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
}

.agent-panel--compact {
  padding: 4px;
  font-size: 13px;
}

.capability-cards__title {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 8px;
  text-align: center;
}

.capability-cards__grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 6px;
}

.agent-panel--compact .capability-cards__grid {
  grid-template-columns: repeat(2, 1fr);
  gap: 4px;
}

.capability-card {
  padding: 10px 6px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  background: #fafafa;
}

.capability-card:hover {
  border-color: #409eff;
  background: #ecf5ff;
  transform: translateY(-1px);
}

.capability-card__icon {
  font-size: 22px;
  margin-bottom: 4px;
}

.capability-card__name {
  font-size: 12px;
  color: #303133;
  font-weight: 500;
}

.capability-card__desc {
  font-size: 11px;
  color: #909399;
  margin-top: 2px;
}

.capability-form__header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  padding-bottom: 6px;
  border-bottom: 1px solid #ebeef5;
}

.capability-form__title {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
}

.capability-form__body {
  flex: 0 0 auto;
}

.capability-result {
  margin-top: 10px;
  flex: 1;
  overflow-y: auto;
  max-height: 300px;
  border-top: 1px solid #ebeef5;
  padding-top: 8px;
}

.agent-panel--compact .capability-result {
  max-height: 200px;
}

.capability-result__fallback {
  background: #fdf6ec;
  color: #e6a23c;
  padding: 6px 10px;
  border-radius: 4px;
  font-size: 12px;
  margin-bottom: 8px;
}

.capability-result__disclaimer {
  background: #fef0f0;
  color: #f56c6c;
  padding: 6px 10px;
  border-radius: 4px;
  font-size: 12px;
  margin-bottom: 8px;
  font-weight: 500;
}

.capability-result__content {
  font-size: 13px;
  line-height: 1.6;
  color: #303133;
  word-break: break-word;
}

.capability-result__content :deep(h1),
.capability-result__content :deep(h2),
.capability-result__content :deep(h3) {
  margin: 8px 0 4px;
  font-size: 14px;
}

.capability-result__content :deep(ul),
.capability-result__content :deep(ol) {
  padding-left: 16px;
  margin: 4px 0;
}

.capability-result__content :deep(p) {
  margin: 4px 0;
}

.capability-result__sources {
  margin-top: 8px;
  padding-top: 6px;
  border-top: 1px dashed #dcdfe6;
}

.capability-result__sources-title {
  font-size: 12px;
  color: #909399;
  margin-bottom: 4px;
}

.capability-result__actions {
  margin-top: 8px;
  display: flex;
  gap: 6px;
}
</style>
