<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">比赛批次管理</h2>
      <el-button type="primary" :icon="Plus" @click="openCreateDialog">创建比赛</el-button>
    </div>

    <el-card shadow="never" v-loading="loading">
      <el-empty v-if="competitions.length === 0" description="暂无比赛" :image-size="80" />

      <el-table v-else :data="competitions" style="width: 100%">
        <el-table-column prop="name" label="比赛名称" min-width="200">
          <template #default="{ row }">
            <span class="competition-name">{{ row.name }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" min-width="250" show-overflow-tooltip>
          <template #default="{ row }">
            {{ row.description || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="start_time" label="开始时间" width="140">
          <template #default="{ row }">
            {{ formatDate(row.start_time) }}
          </template>
        </el-table-column>
        <el-table-column prop="end_time" label="结束时间" width="140">
          <template #default="{ row }">
            {{ formatDate(row.end_time) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="statusType(row.status)" size="small">{{ statusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="openEditDialog(row)">编辑</el-button>
            <el-button type="danger" link size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 创建/编辑弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑比赛' : '创建比赛'"
      width="560px"
      destroy-on-close
    >
      <el-form :model="form" label-width="80px" :rules="rules" ref="formRef">
        <el-form-item label="比赛名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入比赛名称" maxlength="100" show-word-limit />
        </el-form-item>
        <el-form-item label="比赛描述">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入比赛描述"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
        <el-form-item label="开始时间">
          <el-date-picker
            v-model="form.start_time"
            type="datetime"
            placeholder="选择开始时间"
            format="YYYY-MM-DD HH:mm"
            value-format="YYYY-MM-DDTHH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="结束时间">
          <el-date-picker
            v-model="form.end_time"
            type="datetime"
            placeholder="选择结束时间"
            format="YYYY-MM-DD HH:mm"
            value-format="YYYY-MM-DDTHH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="状态">
          <el-radio-group v-model="form.status">
            <el-radio-button label="draft">草稿</el-radio-button>
            <el-radio-button label="active">进行中</el-radio-button>
            <el-radio-button label="ended">已结束</el-radio-button>
            <el-radio-button label="archived">已归档</el-radio-button>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { getCompetitions, createCompetition, updateCompetition, deleteCompetition } from '@/api/competition'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const submitting = ref(false)
const competitions = ref([])

const dialogVisible = ref(false)
const isEdit = ref(false)
const editingId = ref(null)
const formRef = ref(null)

const form = reactive({
  name: '',
  description: '',
  start_time: null,
  end_time: null,
  status: 'draft'
})

const rules = {
  name: [{ required: true, message: '请输入比赛名称', trigger: 'blur' }]
}

const statusMap = {
  draft: { text: '草稿', type: 'info' },
  active: { text: '进行中', type: 'success' },
  ended: { text: '已结束', type: 'warning' },
  archived: { text: '已归档', type: 'info' }
}

const statusText = (status) => statusMap[status]?.text || status
const statusType = (status) => statusMap[status]?.type || 'info'

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

const fetchCompetitions = async () => {
  loading.value = true
  try {
    const res = await getCompetitions()
    if (res.code === 200) {
      competitions.value = res.data.competitions || []
    }
  } catch (error) {
    ElMessage.error('获取比赛列表失败')
  } finally {
    loading.value = false
  }
}

const openCreateDialog = () => {
  isEdit.value = false
  editingId.value = null
  form.name = ''
  form.description = ''
  form.start_time = null
  form.end_time = null
  form.status = 'draft'
  dialogVisible.value = true
}

const openEditDialog = (row) => {
  isEdit.value = true
  editingId.value = row.id
  form.name = row.name
  form.description = row.description || ''
  form.start_time = row.start_time
  form.end_time = row.end_time
  form.status = row.status
  dialogVisible.value = true
}

const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    const data = {
      name: form.name,
      description: form.description,
      start_time: form.start_time,
      end_time: form.end_time,
      status: form.status
    }

    let res
    if (isEdit.value) {
      res = await updateCompetition(editingId.value, data)
    } else {
      res = await createCompetition(data)
    }

    if (res.code === 200 || res.code === 201) {
      ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
      dialogVisible.value = false
      fetchCompetitions()
    } else {
      ElMessage.error(res.message || '操作失败')
    }
  } catch (error) {
    ElMessage.error('操作失败')
  } finally {
    submitting.value = false
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除比赛 "${row.name}" 吗？`,
      '删除确认',
      { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' }
    )
    const res = await deleteCompetition(row.id)
    if (res.code === 200) {
      ElMessage.success('删除成功')
      fetchCompetitions()
    } else {
      ElMessage.error(res.message || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  fetchCompetitions()
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

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.competition-name {
  font-weight: 500;
  color: var(--text-primary);
}
</style>
