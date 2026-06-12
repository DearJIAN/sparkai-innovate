<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">项目审核</h2>
    </div>

    <el-card shadow="never">
      <el-empty v-if="!loading && pendingProjects.length === 0" description="暂无待审核项目" />
      
      <el-table v-else v-loading="loading" :data="pendingProjects" stripe style="width:100%">
        <el-table-column prop="name" label="项目名称" min-width="180">
          <template #default="{ row }">
            <span class="project-link" @click="$router.push(`/projects/${row.id}`)">{{ row.name }}</span>
          </template>
        </el-table-column>
        <el-table-column label="负责人" width="120">
          <template #default="{ row }">
            {{ row.leader?.real_name || row.leader?.username || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="category" label="类别" width="120" />
        <el-table-column label="提交时间" width="160">
          <template #default="{ row }">{{ formatDate(row.updated_at) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleAudit(row)">去审核</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 直接复用 guide-projects 的审核逻辑（后续可统一样式） -->
    <el-dialog v-model="auditVisible" title="项目审核" width="520px" destroy-on-close>
      <template v-if="currentProject">
        <el-descriptions :column="1" border class="mb-4">
          <el-descriptions-item label="项目名称">{{ currentProject.name }}</el-descriptions-item>
          <el-descriptions-item label="负责人">{{ currentProject.leader?.real_name || currentProject.leader?.username || '-' }}</el-descriptions-item>
        </el-descriptions>
        <el-form :model="auditForm" label-width="90px">
          <el-form-item label="审核结果">
            <el-radio-group v-model="auditForm.result">
              <el-radio value="passed">通过</el-radio>
              <el-radio value="need_modify">需修改</el-radio>
              <el-radio value="rejected">驳回</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="审核意见">
            <el-input v-model="auditForm.comment" type="textarea" :rows="4" placeholder="请输入审核意见..." maxlength="500" show-word-limit />
          </el-form-item>
        </el-form>
      </template>
      <template #footer>
        <el-button @click="auditVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submitAudit">提交审核</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { getProjects, updateProject } from '@/api/project'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const submitting = ref(false)
const projects = ref([])
const auditVisible = ref(false)
const currentProject = ref(null)
const auditForm = reactive({ result: 'passed', comment: '' })

const pendingProjects = computed(() => {
  return projects.value.filter(p => p.status === 'submitted')
})

const fetchProjects = async () => {
  loading.value = true
  try {
    const res = await getProjects({ status: 'submitted' })
    if (res.code === 200) {
      projects.value = res.data.projects
    }
  } catch (error) {
    ElMessage.error('获取待审核项目失败')
  } finally {
    loading.value = false
  }
}

const handleAudit = (project) => {
  currentProject.value = project
  auditForm.result = 'passed'
  auditForm.comment = ''
  auditVisible.value = true
}

const submitAudit = async () => {
  if (!currentProject.value) return
  submitting.value = true
  try {
    const res = await updateProject(currentProject.value.id, {
      status: auditForm.result,
      remark: auditForm.comment
    })
    if (res.code === 200) {
      ElMessage.success('审核成功')
      auditVisible.value = false
      fetchProjects()
    }
  } catch (error) {
    ElMessage.error('提交审核失败')
  } finally {
    submitting.value = false
  }
}

const formatDate = (d) => d ? new Date(d).toLocaleString() : '-'

onMounted(fetchProjects)
</script>

<style scoped>
.page-container { padding: 20px; }
.page-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 24px;
}
.project-link {
  cursor: pointer;
  color: var(--primary-600);
  font-weight: 500;
}
.project-link:hover { color: var(--primary-400); text-decoration: underline; }
.mb-4 { margin-bottom: 16px; }
</style>
