<template>
  <div class="page-container">
    <h2 class="page-title">AI 项目助手</h2>
    <p class="page-subtitle">基于 AI 技术，为创新创业项目提供智能化辅助分析</p>

    <el-row :gutter="24">
      <!-- 左侧输入区 -->
      <el-col :span="10">
        <el-card shadow="never">
          <template #header>
            <span>项目信息</span>
          </template>

          <el-form :model="form" label-position="top">
            <el-form-item label="项目名称">
              <el-input v-model="form.project_name" placeholder="请输入项目名称" />
            </el-form-item>

            <el-form-item label="项目简介">
              <el-input
                v-model="form.description"
                type="textarea"
                :rows="4"
                placeholder="简要描述你的项目想法、目标用户、核心功能"
              />
            </el-form-item>

            <el-form-item label="项目类别">
              <el-input v-model="form.category" placeholder="例如：互联网+、人工智能、社会公益" />
            </el-form-item>

            <el-form-item label="所属赛道">
              <el-input v-model="form.track" placeholder="例如：高教主赛道、青年红色筑梦之旅" />
            </el-form-item>

            <el-form-item label="选择 AI 功能">
              <el-radio-group v-model="form.ai_type">
                <el-radio-button label="summary">生成项目简介</el-radio-button>
                <el-radio-button label="business_advice">商业计划书建议</el-radio-button>
                <el-radio-button label="risk_analysis">风险分析</el-radio-button>
              </el-radio-group>
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                :loading="loading"
                :icon="MagicStick"
                @click="handleGenerate"
                style="width: 100%"
              >
                {{ loading ? 'AI 生成中...' : '开始生成' }}
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <!-- 历史记录 -->
        <el-card class="mt-4" shadow="never">
          <template #header>
            <span>历史记录</span>
          </template>
          <el-empty v-if="records.length === 0" description="暂无记录" :image-size="60" />
          <div v-else class="record-list">
            <div
              v-for="record in records.slice(0, 5)"
              :key="record.id"
              class="record-item"
              @click="showRecord(record)"
            >
              <el-icon size="16" color="var(--primary-500)"><MagicStick /></el-icon>
              <span class="record-type">{{ typeText(record.type) }}</span>
              <span class="record-time">{{ formatDate(record.created_at) }}</span>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 右侧输出区 -->
      <el-col :span="14">
        <el-card shadow="never" class="output-card">
          <template #header>
            <div class="output-header">
              <span>AI 输出结果</span>
              <div v-if="result" class="output-actions">
                <el-button type="primary" link size="small" :icon="CopyDocument" @click="copyResult">
                  复制
                </el-button>
              </div>
            </div>
          </template>

          <div v-if="!result" class="output-placeholder">
            <el-icon size="48" color="var(--text-tertiary)"><MagicStick /></el-icon>
            <p>在左侧输入项目信息，选择 AI 功能，点击开始生成</p>
          </div>

          <div v-else class="output-content">
            <div class="result-type-tag">
              <el-tag :type="resultTypeTag.type" size="small">{{ resultTypeTag.text }}</el-tag>
            </div>
            <pre class="result-text">{{ result }}</pre>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { MagicStick, CopyDocument } from '@element-plus/icons-vue'
import {
  generateProjectSummary,
  generateBusinessAdvice,
  generateRiskAnalysis,
  getAiRecords
} from '@/api/ai'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const result = ref('')
const currentType = ref('')
const records = ref([])

const form = reactive({
  project_name: '',
  description: '',
  category: '',
  track: '',
  ai_type: 'summary'
})

const typeMap = {
  summary: { text: '项目简介', type: 'primary' },
  business_advice: { text: '商业计划书建议', type: 'success' },
  risk_analysis: { text: '风险分析', type: 'warning' }
}

const typeText = (type) => typeMap[type]?.text || type
const resultTypeTag = computed(() => typeMap[currentType.value] || { text: '', type: '' })

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

const handleGenerate = async () => {
  if (!form.project_name.trim()) {
    ElMessage.warning('请输入项目名称')
    return
  }

  loading.value = true
  currentType.value = form.ai_type

  try {
    const data = {
      project_name: form.project_name,
      description: form.description,
      category: form.category,
      track: form.track
    }

    let res
    switch (form.ai_type) {
      case 'summary':
        res = await generateProjectSummary(data)
        break
      case 'business_advice':
        res = await generateBusinessAdvice(data)
        break
      case 'risk_analysis':
        res = await generateRiskAnalysis(data)
        break
      default:
        res = await generateProjectSummary(data)
    }

    if (res.code === 200) {
      result.value = res.data.result
      ElMessage.success('生成成功')
      fetchRecords()
    } else {
      ElMessage.error(res.message || '生成失败')
    }
  } catch (error) {
    ElMessage.error('生成失败')
  } finally {
    loading.value = false
  }
}

const copyResult = () => {
  navigator.clipboard.writeText(result.value).then(() => {
    ElMessage.success('已复制到剪贴板')
  }).catch(() => {
    ElMessage.error('复制失败')
  })
}

const showRecord = (record) => {
  result.value = record.result
  currentType.value = record.type
}

const fetchRecords = async () => {
  try {
    const res = await getAiRecords()
    if (res.code === 200) {
      records.value = res.data.records || []
    }
  } catch (error) {
    console.error('获取记录失败', error)
  }
}

onMounted(() => {
  fetchRecords()
})
</script>

<style scoped>
.page-container {
  padding-bottom: 20px;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.page-subtitle {
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 24px;
}

.mt-4 {
  margin-top: 16px;
}

.output-card {
  min-height: 500px;
}

.output-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.output-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  color: var(--text-tertiary);
}

.output-placeholder p {
  margin-top: 16px;
  font-size: 14px;
}

.output-content {
  padding: 8px;
}

.result-type-tag {
  margin-bottom: 12px;
}

.result-text {
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 13px;
  line-height: 1.8;
  color: var(--text-primary);
  white-space: pre-wrap;
  word-wrap: break-word;
  background: var(--bg-secondary);
  padding: 16px;
  border-radius: var(--radius-lg);
  margin: 0;
  max-height: 600px;
  overflow-y: auto;
}

.record-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.record-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.record-item:hover {
  background: var(--primary-50);
}

.record-type {
  flex: 1;
  font-size: 13px;
  color: var(--text-primary);
}

.record-time {
  font-size: 12px;
  color: var(--text-tertiary);
}
</style>
