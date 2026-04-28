<template>
  <div class="projects">
    <div class="page-header">
      <h2 class="page-title">项目管理</h2>
      <el-button type="primary" :icon="Plus" @click="handleCreate">
        创建项目
      </el-button>
    </div>
    
    <el-card>
      <el-table :data="projectList" v-loading="loading">
        <el-table-column prop="name" label="项目名称" />
        <el-table-column prop="category" label="类别" />
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag :type="statusType(row.status)">{{ statusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" />
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button type="primary" link :icon="View" @click="handleView(row)">查看</el-button>
            <el-button type="primary" link :icon="Edit" @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" link :icon="Delete" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="pageSize"
          :total="total"
          layout="total, prev, pager, next"
          @current-change="fetchProjects"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getProjects, deleteProject } from '@/api/project'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const projectList = ref([])
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)

const statusMap = {
  draft: { text: '草稿', type: 'info' },
  submitted: { text: '已提交', type: 'warning' },
  reviewing: { text: '评审中', type: 'primary' },
  approved: { text: '已通过', type: 'success' },
  rejected: { text: '已驳回', type: 'danger' }
}

const statusText = (status) => statusMap[status]?.text || status
const statusType = (status) => statusMap[status]?.type || 'info'

const fetchProjects = async () => {
  loading.value = true
  try {
    const res = await getProjects({ page: page.value, per_page: pageSize.value })
    projectList.value = res.projects || []
    total.value = res.total || 0
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const handleCreate = () => {
  // TODO: 打开创建弹窗
}

const handleView = (row) => {
  // TODO: 查看详情
}

const handleEdit = (row) => {
  // TODO: 编辑项目
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该项目吗？', '提示', { type: 'warning' })
    await deleteProject(row.id)
    ElMessage.success('删除成功')
    fetchProjects()
  } catch {
    // 取消
  }
}

onMounted(fetchProjects)
</script>

<style scoped>
.projects {
  padding-bottom: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #1a1a2e;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
