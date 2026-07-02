<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">用户管理</h2>
      <el-button type="primary" @click="showAddDialog">
        <el-icon><Plus /></el-icon> 添加用户
      </el-button>
    </div>

    <el-card shadow="never">
      <div class="toolbar">
        <el-input v-model="searchQuery" placeholder="搜索姓名/用户名/邮箱..." clearable style="width:260px" prefix-icon="Search" />
        <el-select v-model="filterRole" placeholder="角色筛选" clearable style="width:140px">
          <el-option label="学生" value="student" />
          <el-option label="教师" value="teacher" />
          <el-option label="评委" value="judge" />
          <el-option label="管理员" value="admin" />
        </el-select>
        <el-select v-model="filterStatus" placeholder="状态筛选" clearable style="width:120px">
          <el-option label="正常" value="active" />
          <el-option label="禁用" value="disabled" />
        </el-select>
      </div>

      <el-table :data="filteredUsers" stripe style="width:100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="60" align="center" />
        <el-table-column prop="real_name" label="姓名" width="100">
          <template #default="{ row }">{{ row.real_name || row.username }}</template>
        </el-table-column>
        <el-table-column prop="username" label="用户名" width="110" />
        <el-table-column prop="email" label="邮箱" min-width="180" show-overflow-tooltip />
        <el-table-column prop="role" label="角色" width="100">
          <template #default="{ row }">
            <el-tag :type="roleType(row.role)" size="small">{{ roleText(row.role) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="状态" width="80" align="center">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'" size="small" effect="plain">
              {{ row.is_active ? '正常' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="注册时间" width="140">
          <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="280" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="editUser(row)">编辑</el-button>
            <el-button type="warning" link size="small" @click="handleToggleStatus(row)">
              {{ row.is_active ? '禁用' : '启用' }}
            </el-button>
            <el-button type="info" link size="small" @click="handleResetPassword(row)">重置密码</el-button>
            <el-button type="danger" link size="small" @click="handleDeleteUser(row)" class="delete-btn">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrap">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="filteredUsers.length"
          layout="total, sizes, prev, pager, next"
          :page-sizes="[10, 20, 50]"
        />
      </div>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="editingUser ? '编辑用户' : '添加用户'" width="500px" destroy-on-close>
      <el-form :model="userForm" label-width="90px">
        <el-form-item label="用户名" v-if="!editingUser">
          <el-input v-model="userForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item :label="editingUser ? '新密码' : '密码'">
          <el-input v-model="userForm.password" type="password" :placeholder="editingUser ? '留空则不修改' : '请输入密码'" show-password />
        </el-form-item>
        <el-form-item label="真实姓名">
          <el-input v-model="userForm.real_name" placeholder="请输入真实姓名" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="userForm.email" type="email" placeholder="请输入邮箱地址" />
        </el-form-item>
        <el-form-item label="角色">
          <el-radio-group v-model="userForm.role">
            <el-radio value="student">学生</el-radio>
            <el-radio value="teacher">教师</el-radio>
            <el-radio value="judge">评委</el-radio>
            <el-radio value="admin">管理员</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="学院">
          <el-input v-model="userForm.college" placeholder="请输入学院" />
        </el-form-item>
        <el-form-item label="专业">
          <el-input v-model="userForm.major" placeholder="请输入专业" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveUser" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getUsers, createUser, updateUser, toggleUserStatus, deleteUser } from '@/api/user'

const loading = ref(false)
const saving = ref(false)
const searchQuery = ref('')
const filterRole = ref('')
const filterStatus = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const dialogVisible = ref(false)
const editingUser = ref(null)

const userForm = reactive({
  username: '',
  password: '',
  real_name: '',
  email: '',
  role: 'student',
  college: '',
  major: ''
})

const users = ref([])

const filteredUsers = computed(() => {
  let list = users.value
  if (filterRole.value) list = list.filter(u => u.role === filterRole.value)
  if (filterStatus.value) {
    const isActive = filterStatus.value === 'active'
    list = list.filter(u => u.is_active === isActive)
  }
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(u =>
      (u.real_name || '').toLowerCase().includes(q) ||
      (u.username || '').toLowerCase().includes(q) ||
      (u.email || '').toLowerCase().includes(q)
    )
  }
  return list
})

const roleMap = { student: { text: '学生', type: '' }, teacher: { text: '教师', type: 'success' }, judge: { text: '评委', type: 'warning' }, admin: { text: '管理员', type: 'danger' } }
const roleText = (r) => roleMap[r]?.text || r
const roleType = (r) => roleMap[r]?.type || 'info'

function formatDate(d) { return d ? new Date(d).toLocaleDateString('zh-CN') : '-' }

async function fetchUsers() {
  loading.value = true
  try {
    const res = await getUsers()
    if (res.code === 200) {
      users.value = res.data?.users || []
    }
  } catch (e) {
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

function showAddDialog() {
  editingUser.value = null
  Object.assign(userForm, { username: '', password: '', real_name: '', email: '', role: 'student', college: '', major: '' })
  dialogVisible.value = true
}

function editUser(user) {
  editingUser.value = user
  Object.assign(userForm, {
    username: user.username || '',
    password: '',
    real_name: user.real_name || '',
    email: user.email || '',
    role: user.role || 'student',
    college: user.college || '',
    major: user.major || ''
  })
  dialogVisible.value = true
}

async function saveUser() {
  if (!editingUser.value && (!userForm.username || !userForm.password)) {
    ElMessage.warning('请填写用户名和密码')
    return
  }
  saving.value = true
  try {
    if (editingUser.value) {
      const data = { ...userForm }
      if (!data.password) delete data.password
      delete data.username
      const res = await updateUser(editingUser.value.id, data)
      if (res.code === 200) {
        ElMessage.success('用户信息已更新')
        dialogVisible.value = false
        fetchUsers()
      } else {
        ElMessage.error(res.message || '更新失败')
      }
    } else {
      const res = await createUser(userForm)
      if (res.code === 200 || res.code === 201) {
        ElMessage.success('用户已添加')
        dialogVisible.value = false
        fetchUsers()
      } else {
        ElMessage.error(res.message || '添加失败')
      }
    }
  } catch (e) {
    ElMessage.error('操作失败')
  } finally {
    saving.value = false
  }
}

async function handleToggleStatus(user) {
  const action = user.is_active ? '禁用' : '启用'
  await ElMessageBox.confirm(`确定要${action}用户「${user.real_name || user.username}」吗？`, '确认操作')
  try {
    const res = await toggleUserStatus(user.id)
    if (res.code === 200) {
      ElMessage.success(`已${action}用户「${user.real_name || user.username}」`)
      fetchUsers()
    } else {
      ElMessage.error(res.message || '操作失败')
    }
  } catch (e) {
    ElMessage.error('操作失败')
  }
}

async function handleResetPassword(user) {
  try {
    await ElMessageBox.confirm(
      `确定要把用户「${user.real_name || user.username}」的密码重置为 123456 吗？`,
      '重置密码',
      { type: 'warning' }
    )
    const res = await updateUser(user.id, { password: '123456' })
    if (res.code === 200) {
      ElMessage.success(`已成功重置用户「${user.real_name || user.username}」的密码为 123456`)
    } else {
      ElMessage.error(res.message || '重置密码失败')
    }
  } catch (e) {
    if (e !== 'cancel') {
      ElMessage.error('操作失败')
    }
  }
}

async function handleDeleteUser(user) {
  await ElMessageBox.confirm(`确定要删除用户「${user.real_name || user.username}」吗？此操作不可恢复！`, '危险操作', { type: 'warning' })
  try {
    const res = await deleteUser(user.id)
    if (res.code === 200) {
      ElMessage.success('用户已删除')
      fetchUsers()
    } else {
      ElMessage.error(res.message || '删除失败')
    }
  } catch (e) {
    ElMessage.error('删除失败')
  }
}

onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.page-container { padding-bottom: 20px; }

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.toolbar {
  display: flex;
  gap: 10px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.pagination-wrap {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}

.delete-btn { color: var(--danger-500) !important; }
.delete-btn:hover { color: #f56c6c !important; }
</style>
