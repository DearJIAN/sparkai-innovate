<template>
  <div class="upload-page">
    <div class="upload-hero">
      <div class="upload-hero-bg"></div>
      <div class="upload-hero-content">
        <el-button link class="back-btn" @click="goBack">
          <el-icon><ArrowLeft /></el-icon>
          返回评估中心
        </el-button>
        <h1 class="upload-hero-title">{{ isPPT ? '上传PPT材料' : '上传报告材料' }}</h1>
        <p class="upload-hero-desc">
          {{ isPPT ? '请上传路演PPT导出的PDF文件' : '请上传商业计划书或项目报告导出的PDF文件' }}
        </p>
      </div>
    </div>

    <div class="upload-main">
      <input ref="fileInput" type="file" accept=".pdf,application/pdf" @change="handleFileSelect" class="hidden-input" />

      <div class="upload-card" :class="{ 'has-file': uploadedFile }">
        <div v-if="!uploadedFile" class="upload-area" @click="triggerUpload" @dragover.prevent @drop.prevent="handleDrop">
          <div class="upload-icon-wrapper">
            <el-icon size="40"><UploadFilled /></el-icon>
          </div>
          <p class="upload-primary-text">点击上传或拖拽PDF文件到此处</p>
          <p class="upload-secondary-text">仅支持 PDF 格式。请先将 PPT、商业计划书或项目报告导出为 PDF 后上传</p>
          <div class="upload-formats">
            <span class="format-tag allowed">PDF ✓</span>
            <span class="format-tag denied">PPTX ✗</span>
            <span class="format-tag denied">DOCX ✗</span>
            <span class="format-tag denied">图片 ✗</span>
          </div>
        </div>

        <div v-else class="file-info" @click="triggerUpload">
          <div class="file-icon-box">
            <el-icon size="36"><Document /></el-icon>
          </div>
          <div class="file-details">
            <p class="file-name">{{ uploadedFile.name }}</p>
            <p class="file-meta">
              <span>{{ formatFileSize(uploadedFile.size) }}</span>
              <span class="dot">·</span>
              <span>PDF 文件</span>
            </p>
          </div>
          <el-button circle class="remove-btn" @click.stop="removeFile">
            <el-icon size="18"><Close /></el-icon>
          </el-button>
        </div>
      </div>

      <div v-if="uploadError" class="upload-error">
        <el-icon size="16"><WarningFilled /></el-icon>
        <span>{{ uploadError }}</span>
      </div>

      <div class="upload-actions">
        <el-button size="large" class="action-back" @click="goBack">
          <el-icon><ArrowLeft /></el-icon>
          返回
        </el-button>
        <el-button
          type="primary"
          size="large"
          class="action-start"
          :loading="uploading"
          :disabled="!uploadedFile || uploading"
          @click="startEvaluation"
        >
          <el-icon v-if="!uploading"><MagicStick /></el-icon>
          {{ uploading ? '上传中...' : '开始AI评估' }}
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft, UploadFilled, Document, Close, WarningFilled, MagicStick } from '@element-plus/icons-vue'
import { uploadMaterial } from '@/api/materialEvaluation'

const route = useRoute()
const router = useRouter()

const evalType = computed(() => route.params.type)
const isPPT = computed(() => evalType.value === 'ppt')

const fileInput = ref(null)
const uploadedFile = ref(null)
const uploading = ref(false)
const uploadError = ref('')

function triggerUpload() {
  if (fileInput.value) {
    fileInput.value.value = ''
    fileInput.value.click()
  }
}

function validateFile(file) {
  uploadError.value = ''
  if (!file) return false

  const ext = file.name.split('.').pop()?.toLowerCase()
  if (ext !== 'pdf' && file.type !== 'application/pdf') {
    uploadError.value = '当前仅支持 PDF 文件，请将材料导出为 PDF 后重新上传。'
    return false
  }

  if (file.size > 50 * 1024 * 1024) {
    uploadError.value = '文件大小超过限制（最大50MB），请压缩后重新上传。'
    return false
  }

  return true
}

function handleFileSelect(e) {
  const file = e.target.files[0]
  if (validateFile(file)) {
    uploadedFile.value = file
  }
}

function handleDrop(e) {
  const file = e.dataTransfer.files[0]
  if (validateFile(file)) {
    uploadedFile.value = file
  }
}

function removeFile() {
  uploadedFile.value = null
  uploadError.value = ''
  if (fileInput.value) fileInput.value.value = ''
}

function formatFileSize(bytes) {
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

async function startEvaluation() {
  if (!uploadedFile.value) return
  uploadError.value = ''
  uploading.value = true

  try {
    const formData = new FormData()
    formData.append('file', uploadedFile.value)
    formData.append('evaluation_type', evalType.value)

    const res = await uploadMaterial(formData)
    if (res.code === 200 && res.data) {
      ElMessage.success('上传成功，正在进入AI评估')
      router.push(`/ai-material-evaluation/progress/${res.data.id}`)
    }
  } catch (e) {
    uploadError.value = '文件上传失败，请检查网络后重试'
    ElMessage.error('上传失败，请重试')
  } finally {
    uploading.value = false
  }
}

function goBack() {
  router.push('/ai-material-evaluation')
}
</script>

<style scoped>
.upload-page {
  min-height: 100vh;
  background: #f5f8ff;
}

.upload-hero {
  position: relative;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  padding: 36px 24px 28px;
  overflow: hidden;
}

.upload-hero-bg {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 400px 200px at 30% 60%, rgba(99,102,241,0.3), transparent),
    radial-gradient(ellipse 300px 180px at 70% 40%, rgba(124,58,237,0.25), transparent);
}

.upload-hero-content {
  max-width: 700px;
  margin: 0 auto;
  position: relative;
  z-index: 2;
}

.back-btn {
  color: rgba(255,255,255,0.75);
  font-size: 14px;
  margin-bottom: 12px;
  padding: 0;
}

.back-btn:hover {
  color: #fff;
}

.upload-hero-title {
  font-size: 28px;
  font-weight: 700;
  color: #fff;
  margin: 0 0 8px;
}

.upload-hero-desc {
  font-size: 14px;
  color: rgba(255,255,255,0.7);
  margin: 0;
}

.upload-main {
  max-width: 600px;
  margin: 0 auto;
  padding: 48px 24px 80px;
}

.upload-card {
  background: #fff;
  border-radius: 20px;
  border: 1px solid #e8ecf4;
  box-shadow: 0 4px 20px rgba(37,99,235,0.08);
  transition: all 0.3s;
}

.upload-card.has-file {
  border-color: #93c5fd;
  box-shadow: 0 4px 24px rgba(37,99,235,0.12);
}

.upload-area {
  padding: 48px 32px;
  text-align: center;
  cursor: pointer;
}

.upload-area:hover .upload-icon-wrapper {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(37,99,235,0.15);
}

.hidden-input {
  display: none;
}

.upload-icon-wrapper {
  width: 72px;
  height: 72px;
  margin: 0 auto 20px;
  background: linear-gradient(135deg, #eff6ff, #eef2ff);
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6366f1;
  transition: all 0.3s;
}

.upload-primary-text {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 8px;
}

.upload-secondary-text {
  font-size: 13px;
  color: #94a3b8;
  margin: 0 0 16px;
  line-height: 1.6;
}

.upload-formats {
  display: flex;
  justify-content: center;
  gap: 8px;
  flex-wrap: wrap;
}

.format-tag {
  font-size: 12px;
  padding: 3px 10px;
  border-radius: 8px;
  font-weight: 500;
}

.format-tag.allowed {
  background: #ecfdf5;
  color: #10b981;
  border: 1px solid #a7f3d0;
}

.format-tag.denied {
  background: #f8fafc;
  color: #cbd5e1;
  border: 1px solid #e2e8f0;
}

.file-info {
  display: flex;
  align-items: center;
  padding: 28px 32px;
  gap: 20px;
  cursor: pointer;
}

.file-icon-box {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #eff6ff, #eef2ff);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #3b82f6;
  flex-shrink: 0;
}

.file-details {
  flex: 1;
  min-width: 0;
}

.file-name {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-meta {
  font-size: 13px;
  color: #64748b;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 6px;
}

.dot { color: #cbd5e1; }

.remove-btn {
  flex-shrink: 0;
  border-color: #fecaca;
  color: #ef4444;
}

.remove-btn:hover {
  background: #fef2f2;
  border-color: #ef4444;
  color: #dc2626;
}

.upload-error {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  margin-top: 12px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 12px;
  color: #dc2626;
  font-size: 13px;
}

.upload-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
  justify-content: flex-end;
}

.action-back {
  border-radius: 12px;
  border-color: #e2e8f0;
  color: #64748b;
  font-size: 15px;
  height: 46px;
  padding: 0 24px;
}

.action-start {
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  height: 46px;
  padding: 0 28px;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  border: none;
  display: flex;
  align-items: center;
  gap: 8px;
}

.action-start:hover:not(:disabled) {
  background: linear-gradient(135deg, #1d4ed8, #6d28d9);
}

.action-start:disabled {
  background: #e2e8f0;
  color: #94a3b8;
}

@media (max-width: 768px) {
  .upload-hero-title { font-size: 22px; }
  .upload-hero { padding: 32px 16px; }
  .upload-area { padding: 36px 20px; }
  .file-info { padding: 20px 24px; }
}
</style>