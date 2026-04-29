<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <el-button link :icon="ArrowLeft" @click="$router.back()">返回项目</el-button>
        <h2 class="page-title">项目材料管理</h2>
      </div>
    </div>

    <!-- 项目信息 -->
    <el-card class="project-info-card" shadow="never">
      <div class="project-info">
        <span class="project-name">{{ projectName }}</span>
        <el-tag :type="statusType(projectStatus)" size="small">
          {{ statusText(projectStatus) }}
        </el-tag>
      </div>
    </el-card>

    <!-- 上传区域 -->
    <el-card class="upload-card" shadow="never">
      <template #header>
        <span>上传材料</span>
      </template>
      <el-upload
        ref="uploadRef"
        action=""
        :auto-upload="false"
        :on-change="handleFileChange"
        :on-remove="handleFileRemove"
        :file-list="fileList"
        :limit="5"
        drag
        multiple
      >
        <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
        <div class="el-upload__text">
          将文件拖到此处，或 <em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            支持图片、文档、PPT、PDF、视频、压缩包等格式，单个文件不超过 4GB
          </div>
        </template>
      </el-upload>

      <div v-if="fileList.length > 0" class="upload-form">
        <el-form :model="uploadForm" label-width="100px">
          <el-form-item label="材料类型">
            <el-select v-model="uploadForm.material_type" placeholder="请选择材料类型" style="width: 240px">
              <el-option label="项目申报书" value="项目申报书" />
              <el-option label="商业计划书" value="商业计划书" />
              <el-option label="路演PPT" value="路演PPT" />
              <el-option label="项目图片" value="项目图片" />
              <el-option label="演示视频" value="演示视频" />
              <el-option label="调研报告" value="调研报告" />
              <el-option label="其他附件" value="其他附件" />
            </el-select>
          </el-form-item>
        </el-form>
        <el-button type="primary" :loading="uploading" @click="handleUpload">
          开始上传
        </el-button>
      </div>
    </el-card>

    <!-- 文件列表 -->
    <el-card class="file-list-card" shadow="never" v-loading="loading">
      <template #header>
        <div class="file-list-header">
          <span>材料列表</span>
          <el-select v-model="filterType" placeholder="筛选类型" clearable size="small" style="width: 160px" @change="fetchFiles">
            <el-option label="项目申报书" value="项目申报书" />
            <el-option label="商业计划书" value="商业计划书" />
            <el-option label="路演PPT" value="路演PPT" />
            <el-option label="项目图片" value="项目图片" />
            <el-option label="演示视频" value="演示视频" />
            <el-option label="调研报告" value="调研报告" />
            <el-option label="其他附件" value="其他附件" />
          </el-select>
        </div>
      </template>

      <el-empty v-if="files.length === 0" description="暂无材料文件" />

      <div v-else class="file-list">
        <div
          v-for="file in files"
          :key="file.id"
          class="file-item"
        >
          <div class="file-icon">
            <el-icon size="32" :color="fileIconColor(file.file_type)">
              <component :is="fileIcon(file.file_type)" />
            </el-icon>
          </div>
          <div class="file-info">
            <div class="file-name">{{ file.original_name }}</div>
            <div class="file-meta">
              <el-tag size="small" type="info">{{ file.material_type }}</el-tag>
              <span class="file-size">{{ formatFileSize(file.file_size) }}</span>
              <span class="file-uploader">上传者: {{ file.uploader?.real_name || file.uploader?.username || '-' }}</span>
              <span class="file-time">{{ formatDate(file.created_at) }}</span>
            </div>
          </div>
          <div class="file-actions">
            <el-button type="primary" link size="small" @click="handleDownload(file)">
              <el-icon><Download /></el-icon>下载
            </el-button>
            <el-button
              v-if="canDelete(file)"
              type="danger"
              link
              size="small"
              @click="handleDelete(file)"
            >
              <el-icon><Delete /></el-icon>删除
            </el-button>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import {
  ArrowLeft, UploadFilled, Document, Picture, VideoCamera,
  Collection, Download, Delete
} from '@element-plus/icons-vue'
import { getFiles, uploadFile, downloadFile, deleteFile } from '@/api/file'
import { getProject } from '@/api/project'
import { ElMessage, ElMessageBox } from 'element-plus'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const projectId = computed(() => route.params.id)
const loading = ref(false)
const uploading = ref(false)
const files = ref([])
const fileList = ref([])
const projectName = ref('')
const projectStatus = ref('')
const projectLeaderId = ref(null)
const filterType = ref('')

const uploadForm = reactive({
  material_type: '其他附件'
})

const statusMap = {
  draft: { text: '草稿', type: 'info' },
  submitted: { text: '已提交', type: 'primary' },
  teacher_review: { text: '审核中', type: 'warning' },
  judging: { text: '评审中', type: 'warning' },
  passed: { text: '已通过', type: 'success' },
  need_modify: { text: '需修改', type: 'danger' },
  rejected: { text: '已驳回', type: 'danger' }
}

const statusText = (status) => statusMap[status]?.text || status
const statusType = (status) => statusMap[status]?.type || 'info'

const fileIcon = (type) => {
  const iconMap = {
    image: Picture,
    video: VideoCamera,
    document: Document,
    ppt: Collection,
    spreadsheet: Document,
    archive: Collection
  }
  return iconMap[type] || Document
}

const fileIconColor = (type) => {
  const colorMap = {
    image: '#409EFF',
    video: '#E6A23C',
    document: '#67C23A',
    ppt: '#F56C6C',
    spreadsheet: '#67C23A',
    archive: '#909399'
  }
  return colorMap[type] || '#909399'
}

const formatFileSize = (bytes) => {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

const canDelete = (file) => {
  if (!userStore.userInfo) return false
  if (userStore.isAdmin) return true
  if (projectLeaderId.value === userStore.userInfo.id) return true
  return file.uploader_id === userStore.userInfo.id
}

const fetchProject = async () => {
  try {
    const res = await getProject(projectId.value)
    if (res.code === 200) {
      const project = res.data.project
      projectName.value = project.name
      projectStatus.value = project.status
      projectLeaderId.value = project.leader_id
    }
  } catch (error) {
    console.error(error)
  }
}

const fetchFiles = async () => {
  loading.value = true
  try {
    const params = {}
    if (filterType.value) params.material_type = filterType.value
    const res = await getFiles(projectId.value, params)
    if (res.code === 200) {
      files.value = res.data.files || []
    }
  } catch (error) {
    ElMessage.error('获取文件列表失败')
  } finally {
    loading.value = false
  }
}

const handleFileChange = (uploadFile) => {
  fileList.value.push(uploadFile)
}

const handleFileRemove = (uploadFile) => {
  const index = fileList.value.indexOf(uploadFile)
  if (index > -1) {
    fileList.value.splice(index, 1)
  }
}

const handleUpload = async () => {
  if (fileList.value.length === 0) {
    ElMessage.warning('请选择要上传的文件')
    return
  }

  uploading.value = true
  let successCount = 0

  for (const file of fileList.value) {
    try {
      const formData = new FormData()
      formData.append('file', file.raw)
      formData.append('material_type', uploadForm.material_type)

      const res = await uploadFile(projectId.value, formData)
      if (res.code === 201) {
        successCount++
      } else {
        ElMessage.error(`${file.name} 上传失败: ${res.message}`)
      }
    } catch (error) {
      ElMessage.error(`${file.name} 上传失败`)
    }
  }

  uploading.value = false
  fileList.value = []

  if (successCount > 0) {
    ElMessage.success(`成功上传 ${successCount} 个文件`)
    fetchFiles()
  }
}

const handleDownload = async (file) => {
  try {
    const res = await downloadFile(file.id)
    const blob = new Blob([res])
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = file.original_name
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    ElMessage.success('下载成功')
  } catch (error) {
    ElMessage.error('下载失败')
  }
}

const handleDelete = async (file) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除文件 "${file.original_name}" 吗？`,
      '删除确认',
      { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' }
    )
    const res = await deleteFile(file.id)
    if (res.code === 200) {
      ElMessage.success('文件删除成功')
      fetchFiles()
    } else {
      ElMessage.error(res.message || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.message || '删除失败')
    }
  }
}

onMounted(() => {
  fetchProject()
  fetchFiles()
})
</script>

<style scoped>
.page-container {
  padding-bottom: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.project-info-card {
  margin-bottom: 20px;
}

.project-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.project-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.upload-card {
  margin-bottom: 20px;
}

.upload-form {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid var(--border-light);
  display: flex;
  align-items: flex-end;
  gap: 16px;
}

.file-list-card {
  min-height: 300px;
}

.file-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.file-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.file-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  transition: all var(--transition-fast);
}

.file-item:hover {
  border-color: var(--primary-300);
  box-shadow: var(--shadow-sm);
}

.file-icon {
  width: 48px;
  height: 48px;
  border-radius: 10px;
  background: var(--bg-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.file-info {
  flex: 1;
  min-width: 0;
}

.file-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 8px;
  word-break: break-all;
}

.file-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.file-size,
.file-uploader,
.file-time {
  font-size: 12px;
  color: var(--text-secondary);
}

.file-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}
</style>
