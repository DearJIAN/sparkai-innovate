<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <el-button link :icon="ArrowLeft" @click="$router.back()">返回项目</el-button>
        <h2 class="page-title">团队成员管理</h2>
      </div>
      <el-button v-if="canManage" type="primary" :icon="Plus" @click="showAddDialog = true">
        添加成员
      </el-button>
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

    <!-- 成员列表 -->
    <el-card shadow="never" v-loading="loading">
      <el-empty v-if="members.length === 0" description="暂无团队成员" />

      <div v-else class="member-list">
        <el-row :gutter="16">
          <el-col
            v-for="member in members"
            :key="member.id"
            :xs="24"
            :sm="12"
            :md="8"
            :lg="6"
          >
            <div class="member-card">
              <div class="member-avatar">
                <el-avatar :size="48" :icon="UserFilled" />
              </div>
              <div class="member-content">
                <div class="member-header">
                  <span class="member-name">{{ member.member_name }}</span>
                  <el-tag v-if="member.role_in_project" size="small" type="info">
                    {{ member.role_in_project }}
                  </el-tag>
                </div>
                <p class="member-responsibility">
                  {{ member.responsibility || '暂无分工描述' }}
                </p>
                <div v-if="canManage" class="member-actions">
                  <el-button type="primary" link size="small" @click="handleEdit(member)">
                    编辑
                  </el-button>
                  <el-button type="danger" link size="small" @click="handleDelete(member)">
                    删除
                  </el-button>
                </div>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
    </el-card>

    <!-- 添加成员弹窗 -->
    <el-dialog
      v-model="showAddDialog"
      title="添加团队成员"
      width="500px"
      destroy-on-close
    >
      <el-form
        ref="addFormRef"
        :model="addForm"
        :rules="memberRules"
        label-position="top"
      >
        <el-form-item label="成员姓名" prop="member_name">
          <el-input v-model="addForm.member_name" placeholder="请输入成员姓名" />
        </el-form-item>
        <el-form-item label="关联用户 ID（可选）" prop="user_id">
          <el-input v-model="addForm.user_id" placeholder="请输入平台用户 ID" />
        </el-form-item>
        <el-form-item label="项目角色" prop="role_in_project">
          <el-select v-model="addForm.role_in_project" placeholder="请选择角色" style="width: 100%">
            <el-option label="技术负责人" value="技术负责人" />
            <el-option label="产品经理" value="产品经理" />
            <el-option label="设计师" value="设计师" />
            <el-option label="开发工程师" value="开发工程师" />
            <el-option label="市场运营" value="市场运营" />
            <el-option label="财务" value="财务" />
            <el-option label="成员" value="成员" />
          </el-select>
        </el-form-item>
        <el-form-item label="分工描述" prop="responsibility">
          <el-input
            v-model="addForm.responsibility"
            type="textarea"
            :rows="3"
            placeholder="请描述该成员的具体分工"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleAdd">确定</el-button>
      </template>
    </el-dialog>

    <!-- 编辑成员弹窗 -->
    <el-dialog
      v-model="showEditDialog"
      title="编辑成员信息"
      width="500px"
      destroy-on-close
    >
      <el-form
        ref="editFormRef"
        :model="editForm"
        :rules="memberRules"
        label-position="top"
      >
        <el-form-item label="成员姓名" prop="member_name">
          <el-input v-model="editForm.member_name" placeholder="请输入成员姓名" />
        </el-form-item>
        <el-form-item label="关联用户 ID（可选）" prop="user_id">
          <el-input v-model="editForm.user_id" placeholder="请输入平台用户 ID" />
        </el-form-item>
        <el-form-item label="项目角色" prop="role_in_project">
          <el-select v-model="editForm.role_in_project" placeholder="请选择角色" style="width: 100%">
            <el-option label="技术负责人" value="技术负责人" />
            <el-option label="产品经理" value="产品经理" />
            <el-option label="设计师" value="设计师" />
            <el-option label="开发工程师" value="开发工程师" />
            <el-option label="市场运营" value="市场运营" />
            <el-option label="财务" value="财务" />
            <el-option label="成员" value="成员" />
          </el-select>
        </el-form-item>
        <el-form-item label="分工描述" prop="responsibility">
          <el-input
            v-model="editForm.responsibility"
            type="textarea"
            :rows="3"
            placeholder="请描述该成员的具体分工"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleUpdate">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ArrowLeft, Plus, UserFilled } from '@element-plus/icons-vue'
import { getMembers, addMember, updateMember, deleteMember } from '@/api/member'
import { getProject } from '@/api/project'
import { ElMessage, ElMessageBox } from 'element-plus'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const projectId = computed(() => route.params.id)
const loading = ref(false)
const submitting = ref(false)
const members = ref([])
const projectName = ref('')
const projectStatus = ref('')
const projectLeaderId = ref(null)

const showAddDialog = ref(false)
const showEditDialog = ref(false)
const addFormRef = ref()
const editFormRef = ref()

const addForm = reactive({
  member_name: '',
  user_id: '',
  role_in_project: '',
  responsibility: ''
})

const editForm = reactive({
  id: null,
  member_name: '',
  user_id: '',
  role_in_project: '',
  responsibility: ''
})

const memberRules = {
  member_name: [
    { required: true, message: '请输入成员姓名', trigger: 'blur' }
  ]
}

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

const canManage = computed(() => {
  if (!userStore.userInfo) return false
  if (userStore.isAdmin) return true
  return projectLeaderId.value === userStore.userInfo.id
})

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

const fetchMembers = async () => {
  loading.value = true
  try {
    const res = await getMembers(projectId.value)
    if (res.code === 200) {
      members.value = res.data.members || []
    }
  } catch (error) {
    ElMessage.error('获取成员列表失败')
  } finally {
    loading.value = false
  }
}

const handleAdd = async () => {
  const valid = await addFormRef.value?.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    const data = { ...addForm }
    if (data.user_id) data.user_id = parseInt(data.user_id)

    const res = await addMember(projectId.value, data)
    if (res.code === 201) {
      ElMessage.success('成员添加成功')
      showAddDialog.value = false
      addFormRef.value?.resetFields()
      fetchMembers()
    } else {
      ElMessage.error(res.message || '添加失败')
    }
  } catch (error) {
    ElMessage.error(error.response?.data?.message || '添加失败')
  } finally {
    submitting.value = false
  }
}

const handleEdit = (member) => {
  Object.assign(editForm, {
    id: member.id,
    member_name: member.member_name,
    user_id: member.user_id || '',
    role_in_project: member.role_in_project || '',
    responsibility: member.responsibility || ''
  })
  showEditDialog.value = true
}

const handleUpdate = async () => {
  const valid = await editFormRef.value?.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    const data = {
      member_name: editForm.member_name,
      user_id: editForm.user_id ? parseInt(editForm.user_id) : null,
      role_in_project: editForm.role_in_project,
      responsibility: editForm.responsibility
    }

    const res = await updateMember(editForm.id, data)
    if (res.code === 200) {
      ElMessage.success('成员更新成功')
      showEditDialog.value = false
      fetchMembers()
    } else {
      ElMessage.error(res.message || '更新失败')
    }
  } catch (error) {
    ElMessage.error(error.response?.data?.message || '更新失败')
  } finally {
    submitting.value = false
  }
}

const handleDelete = async (member) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除成员 "${member.member_name}" 吗？`,
      '删除确认',
      { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' }
    )
    const res = await deleteMember(member.id)
    if (res.code === 200) {
      ElMessage.success('成员删除成功')
      fetchMembers()
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
  fetchMembers()
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

.member-list {
  margin-top: 8px;
}

.member-card {
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 20px;
  margin-bottom: 16px;
  display: flex;
  gap: 16px;
  transition: all var(--transition-fast);
}

.member-card:hover {
  border-color: var(--primary-300);
  box-shadow: var(--shadow-md);
}

.member-avatar {
  flex-shrink: 0;
}

.member-content {
  flex: 1;
  min-width: 0;
}

.member-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.member-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.member-responsibility {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
  margin: 0 0 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.member-actions {
  display: flex;
  gap: 8px;
}
</style>
