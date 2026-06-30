<template>
  <div class="competition-register">
    <div class="register-container">
      <!-- 步骤条 -->
      <div class="steps-header">
        <el-steps :active="currentStep" finish-status="success" simple>
          <el-step title="选择赛道" />
          <el-step title="队伍信息" />
          <el-step title="队员信息" />
          <el-step title="上传材料" />
          <el-step title="确认报名" />
        </el-steps>
      </div>

      <!-- Step 1: 选择赛道 -->
      <div v-if="currentStep === 0" class="step-content">
        <h2 class="step-title">选择参赛赛道</h2>
        <p class="step-desc">请选择一个赛道报名参赛</p>
        <div class="track-selection">
          <el-radio-group v-model="form.trackId" class="track-group">
            <el-radio-button
              v-for="track in tracks"
              :key="track.id"
              :label="track.id"
              class="track-option"
            >
              <div class="track-card">
                <h4>{{ track.name }}</h4>
                <p>{{ track.description }}</p>
                <div class="track-requirement">
                  <span>团队人数：{{ track.teamMin }}-{{ track.teamMax }}人</span>
                  <span>材料：{{ track.materialRequirements }}</span>
                </div>
              </div>
            </el-radio-button>
          </el-radio-group>
        </div>
      </div>

      <!-- Step 2: 队伍信息 -->
      <div v-if="currentStep === 1" class="step-content">
        <div class="quick-fill-bar">
          <el-button type="primary" plain size="small" @click="quickFillTeamInfo">
            <el-icon><MagicStick /></el-icon>
            快速生成队伍信息
          </el-button>
          <span class="quick-fill-hint">一键填充测试数据，方便调试</span>
        </div>
        <h2 class="step-title">填写队伍信息</h2>
        <p class="step-desc">请填写参赛队伍的基本信息</p>
        <el-form
          ref="teamFormRef"
          :model="form"
          :rules="teamRules"
          label-width="120px"
          class="register-form"
        >
          <el-form-item label="队伍名称" prop="teamName">
            <el-input v-model="form.teamName" placeholder="请输入队伍名称" />
          </el-form-item>
          <el-form-item label="学校" prop="school">
            <el-input v-model="form.school" placeholder="请输入学校名称" />
          </el-form-item>
          <el-form-item label="学院" prop="college">
            <el-input v-model="form.college" placeholder="请输入学院名称" />
          </el-form-item>
          <el-form-item label="专业" prop="major">
            <el-input v-model="form.major" placeholder="请输入专业名称" />
          </el-form-item>
          <el-form-item label="指导老师" prop="teacherName">
            <el-input v-model="form.teacherName" placeholder="请输入指导老师姓名" />
          </el-form-item>
          <el-form-item label="老师电话" prop="teacherPhone">
            <el-input v-model="form.teacherPhone" placeholder="请输入指导老师电话" />
          </el-form-item>
          <el-form-item label="联系电话" prop="contactPhone">
            <el-input v-model="form.contactPhone" placeholder="请输入联系电话" />
          </el-form-item>
          <el-form-item label="联系邮箱" prop="contactEmail">
            <el-input v-model="form.contactEmail" placeholder="请输入联系邮箱" />
          </el-form-item>
          <el-form-item label="关联项目" prop="projectId">
            <el-select v-model="form.projectId" placeholder="选择已有项目（可选）" clearable style="width: 100%">
              <el-option
                v-for="project in myProjects"
                :key="project.id"
                :label="project.name"
                :value="project.id"
              />
            </el-select>
          </el-form-item>
        </el-form>
      </div>

      <!-- Step 3: 队员信息 -->
      <div v-if="currentStep === 2" class="step-content">
        <div class="quick-fill-bar">
          <el-button type="primary" plain size="small" @click="quickFillMembers">
            <el-icon><MagicStick /></el-icon>
            快速生成队员信息
          </el-button>
          <span class="quick-fill-hint">一键填充测试队员数据</span>
        </div>
        <h2 class="step-title">添加队员信息</h2>
        <p class="step-desc">
          你是队长，请添加其他队员（{{ selectedTrack?.teamMin || 3 }}-{{ selectedTrack?.teamMax || 5 }}人）
        </p>
        <div class="members-list">
          <el-card
            v-for="(member, index) in form.members"
            :key="index"
            class="member-card"
            shadow="never"
          >
            <template #header>
              <div class="member-header">
                <span>队员 {{ index + 1 }}</span>
                <el-button
                  v-if="index > 0"
                  type="danger"
                  link
                  size="small"
                  @click="removeMember(index)"
                >
                  删除
                </el-button>
              </div>
            </template>
            <el-form
              :model="member"
              label-width="80px"
              class="member-form"
            >
              <el-form-item label="姓名" required>
                <el-input v-model="member.name" placeholder="姓名" />
              </el-form-item>
              <el-form-item label="学号" required>
                <el-input v-model="member.studentNo" placeholder="学号" />
              </el-form-item>
              <el-form-item label="学院">
                <el-input v-model="member.college" placeholder="学院" />
              </el-form-item>
              <el-form-item label="专业">
                <el-input v-model="member.major" placeholder="专业" />
              </el-form-item>
              <el-form-item label="电话">
                <el-input v-model="member.phone" placeholder="电话" />
              </el-form-item>
              <el-form-item label="邮箱">
                <el-input v-model="member.email" placeholder="邮箱" />
              </el-form-item>
            </el-form>
          </el-card>
          <el-button
            type="primary"
            plain
            class="add-member-btn"
            @click="addMember"
            :disabled="form.members.length >= (selectedTrack?.teamMax || 5)"
          >
            <el-icon><Plus /></el-icon>
            添加队员
          </el-button>
        </div>
      </div>

      <!-- Step 4: 上传材料 -->
      <div v-if="currentStep === 3" class="step-content">
        <h2 class="step-title">上传报名材料</h2>
        <p class="step-desc">请上传所需的报名材料</p>
        <div class="materials-upload">
          <div
            v-for="material in materialTypes"
            :key="material.type"
            class="material-item"
          >
            <div class="material-info">
              <h4>{{ material.type }}</h4>
              <p>{{ material.desc }}</p>
            </div>
            <el-upload
              :action="uploadAction"
              :headers="uploadHeaders"
              :data="{ material_type: material.type }"
              :on-success="(res) => handleUploadSuccess(res, material.type)"
              :on-error="handleUploadError"
              :limit="1"
              class="material-uploader"
            >
              <el-button type="primary" size="small">
                <el-icon><Upload /></el-icon>
                上传文件
              </el-button>
            </el-upload>
          </div>
        </div>
      </div>

      <!-- Step 5: 确认报名 -->
      <div v-if="currentStep === 4" class="step-content">
        <h2 class="step-title">确认报名信息</h2>
        <p class="step-desc">请确认以下报名信息是否准确</p>
        <div class="confirm-content">
          <el-descriptions title="竞赛信息" :column="1" border>
            <el-descriptions-item label="竞赛名称">{{ competition.name }}</el-descriptions-item>
            <el-descriptions-item label="赛道">{{ selectedTrack?.name }}</el-descriptions-item>
          </el-descriptions>

          <el-descriptions title="队伍信息" :column="2" border class="mt-4">
            <el-descriptions-item label="队伍名称">{{ form.teamName }}</el-descriptions-item>
            <el-descriptions-item label="学校">{{ form.school }}</el-descriptions-item>
            <el-descriptions-item label="学院">{{ form.college }}</el-descriptions-item>
            <el-descriptions-item label="专业">{{ form.major }}</el-descriptions-item>
            <el-descriptions-item label="指导老师">{{ form.teacherName }}</el-descriptions-item>
            <el-descriptions-item label="老师电话">{{ form.teacherPhone }}</el-descriptions-item>
            <el-descriptions-item label="联系电话">{{ form.contactPhone }}</el-descriptions-item>
            <el-descriptions-item label="联系邮箱">{{ form.contactEmail }}</el-descriptions-item>
          </el-descriptions>

          <el-descriptions title="队员信息" :column="1" border class="mt-4">
            <el-descriptions-item label="队长">{{ userStore.userInfo?.real_name || userStore.userInfo?.username }}</el-descriptions-item>
            <el-descriptions-item label="队员">
              <div v-for="(member, index) in form.members" :key="index">
                {{ member.name }} ({{ member.studentNo }})
              </div>
            </el-descriptions-item>
          </el-descriptions>

          <div class="confirm-agreement">
            <el-checkbox v-model="agreed">
              我确认以上报名信息真实有效，并同意遵守竞赛规则
            </el-checkbox>
          </div>
        </div>
      </div>

      <!-- 底部操作按钮 -->
      <div class="step-actions">
        <el-button v-if="currentStep > 0" @click="prevStep">上一步</el-button>
        <el-button v-if="currentStep < 4" type="primary" @click="nextStep">
          下一步
        </el-button>
        <el-button
          v-if="currentStep === 4"
          type="primary"
          :disabled="!agreed"
          :loading="submitting"
          @click="submitRegistrationFinal"
        >
          提交报名
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import { Plus, Upload, MagicStick } from '@element-plus/icons-vue'
import { getPublicCompetitionDetail } from '@/api/competition'
import { getProjects } from '@/api/project'
import { createRegistration, addRegistrationMember, submitRegistration, getRegistration, updateRegistration } from '@/api/registration'
import { withApiBase } from '@/utils/appBase'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const currentStep = ref(0)
const submitting = ref(false)
const agreed = ref(false)
const teamFormRef = ref()

const competition = ref({})
const tracks = ref([])
const selectedTrack = computed(() => tracks.value.find(t => t.id === form.value.trackId))

const myProjects = ref([])

const form = ref({
  trackId: null,
  teamName: '',
  school: '',
  college: '',
  major: '',
  teacherName: '',
  teacherPhone: '',
  contactPhone: '',
  contactEmail: '',
  projectId: null,
  members: [
    { name: '', studentNo: '', college: '', major: '', phone: '', email: '' }
  ]
})

const registrationId = ref(null)

const teamRules = {
  teamName: [{ required: true, message: '请输入队伍名称', trigger: 'blur' }],
  school: [{ required: true, message: '请输入学校名称', trigger: 'blur' }],
  college: [{ required: true, message: '请输入学院名称', trigger: 'blur' }],
  major: [{ required: true, message: '请输入专业名称', trigger: 'blur' }],
  teacherName: [{ required: true, message: '请输入指导老师姓名', trigger: 'blur' }],
  teacherPhone: [{ required: true, message: '请输入指导老师电话', trigger: 'blur' }],
  contactPhone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }],
  contactEmail: [
    { required: true, message: '请输入联系邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ]
}

const materialTypes = [
  { type: '项目申报书', desc: 'PDF格式，不超过20页' },
  { type: '商业计划书', desc: 'PDF格式，不超过30页' },
  { type: '路演PPT', desc: 'PPT或PDF格式，不超过15页' },
  { type: '演示视频', desc: 'MP4格式，3-5分钟' },
  { type: '项目图片', desc: 'JPG/PNG格式，至少3张' },
  { type: '其他附件', desc: '相关证明材料' }
]

const uploadHeaders = computed(() => {
  return {
    Authorization: `Bearer ${localStorage.getItem('token')}`
  }
})

const uploadAction = computed(() => {
  if (!registrationId.value) return ''
  return withApiBase(`/registrations/${registrationId.value}/materials`)
})

onMounted(async () => {
  try {
    const compId = route.params.id
    const res = await getPublicCompetitionDetail(compId)
    if (res.code === 200) {
      competition.value = res.data
      tracks.value = res.data.tracks || []
    }
    
    // 加载已有项目
    const projRes = await getProjects({ page: 1, per_page: 100 })
    if (projRes.code === 200 && projRes.data.projects) {
      myProjects.value = projRes.data.projects
    }
    
    // 如果是从我的赛事带了 regId 过来，则预填充表单
    const regId = route.query.regId
    if (regId) {
      const regRes = await getRegistration(regId)
      if (regRes.code === 200) {
        const reg = regRes.data
        form.value.trackId = reg.track_id
        form.value.teamName = reg.team_name
        form.value.school = reg.school
        form.value.college = reg.college
        form.value.major = reg.major
        form.value.teacherName = reg.teacher_name
        form.value.teacherPhone = reg.teacher_phone
        form.value.contactPhone = reg.contact_phone
        form.value.contactEmail = reg.contact_email
        form.value.projectId = reg.project_id
        
        if (reg.members && reg.members.length > 0) {
          form.value.members = reg.members.map(m => ({
            id: m.id,
            name: m.name,
            studentNo: m.student_no,
            college: m.college,
            major: m.major,
            phone: m.phone,
            email: m.email
          }))
        } else {
          form.value.members = [ { name: '', studentNo: '', college: '', major: '', phone: '', email: '' } ]
        }
        registrationId.value = reg.id
      }
    }
  } catch (error) {
    console.error('加载数据失败', error)
  }
})

const nextStep = async () => {
  if (currentStep.value === 0) {
    if (!form.value.trackId) {
      ElMessage.warning('请选择一个赛道')
      return
    }
  }

  if (currentStep.value === 1) {
    const valid = await teamFormRef.value?.validate().catch(() => false)
    if (!valid) return
    
    // 第二步完成时，创建报名草稿
    const payload = {
      competition_id: parseInt(route.params.id),
      track_id: form.value.trackId,
      team_name: form.value.teamName,
      school: form.value.school,
      college: form.value.college,
      major: form.value.major,
      teacher_name: form.value.teacherName,
      teacher_phone: form.value.teacherPhone,
      contact_phone: form.value.contactPhone,
      contact_email: form.value.contactEmail,
      project_id: form.value.projectId || null
    }
    if (!registrationId.value) {
      try {
        const res = await createRegistration(payload)
        if (res.code === 201) {
          registrationId.value = res.data.registration.id
        } else {
          return
        }
      } catch (e) {
        return
      }
    } else {
      try {
        await updateRegistration(registrationId.value, payload)
      } catch (e) {
        return
      }
    }
  }

  if (currentStep.value === 2) {
    const valid = validateMembers()
    if (!valid) return
    
    // 第三步完成时，上传队员
    try {
      for (const member of form.value.members) {
        if (member.name && member.studentNo && !member.id) {
          const payload = {
            name: member.name,
            student_no: member.studentNo,
            college: member.college,
            major: member.major,
            phone: member.phone,
            email: member.email,
            role_in_team: 'member'
          }
          const res = await addRegistrationMember(registrationId.value, payload)
          if (res.code === 201) {
            member.id = res.data.member.id
          }
        }
      }
    } catch (e) {
      console.error('添加队员失败', e)
    }
  }

  currentStep.value++
}

const prevStep = () => {
  currentStep.value--
}

const validateMembers = () => {
  const track = selectedTrack.value
  const memberCount = form.value.members.length + 1 // +1 for leader

  if (memberCount < track.teamMin) {
    ElMessage.warning(`团队人数至少需要 ${track.teamMin} 人`)
    return false
  }

  for (const member of form.value.members) {
    if (!member.name || !member.studentNo) {
      ElMessage.warning('请填写完整的队员信息')
      return false
    }
  }

  return true
}

const addMember = () => {
  form.value.members.push({
    name: '',
    studentNo: '',
    college: '',
    major: '',
    phone: '',
    email: ''
  })
}

const removeMember = (index) => {
  form.value.members.splice(index, 1)
}

const handleUploadSuccess = (response, type) => {
  if (response.code === 201) {
    ElMessage.success(`${type} 上传成功`)
  } else {
    ElMessage.error(response.message || '上传失败')
  }
}

const handleUploadError = () => {
  ElMessage.error('上传失败，请检查网络或文件大小')
}

const submitRegistrationFinal = async () => {
  if (!agreed.value) {
    ElMessage.warning('请确认报名信息并同意规则')
    return
  }

  submitting.value = true
  try {
    const res = await submitRegistration(registrationId.value)
    if (res.code === 200) {
      ElMessage.success('报名提交成功！')
      router.push('/my-registrations')
    }
  } catch (error) {
    console.error(error)
  } finally {
    submitting.value = false
  }
}

function quickFillTeamInfo() {
  form.value.teamName = '创新先锋队'
  form.value.school = 'XX大学'
  form.value.college = '计算机科学与技术学院'
  form.value.major = '软件工程'
  form.value.teacherName = '张教授'
  form.value.teacherPhone = '13800138000'
  form.value.contactPhone = '13900139000'
  form.value.contactEmail = 'team_leader@example.com'
  if (form.value.trackId === null && tracks.value.length > 0) {
    form.value.trackId = tracks.value[0].id
  }
  ElMessage.success('队伍信息已快速填充')
}

function quickFillMembers() {
  const testMembers = [
    { name: '李明', studentNo: '2023010001', college: '计算机学院', major: '人工智能', phone: '13811110001', email: 'liming@example.com' },
    { name: '王芳', studentNo: '2023010002', college: '计算机学院', major: '数据科学', phone: '13811110002', email: 'wangfang@example.com' },
    { name: '张伟', studentNo: '2023010003', college: '计算机学院', major: '软件工程', phone: '13811110003', email: 'zhangwei@example.com' }
  ]
  const maxMembers = (selectedTrack.value?.teamMax || 5) - 1
  form.value.members = testMembers.slice(0, maxMembers).map(m => ({ ...m }))
  ElMessage.success(`已快速生成 ${form.value.members.length} 名队员信息`)
}
</script>

<style scoped>
.competition-register {
  min-height: 100vh;
  background-color: #f8fafc;
  padding: 24px 40px;
}

.register-container {
  max-width: 1000px;
  margin: 0 auto;
  background: #ffffff;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.steps-header {
  margin-bottom: 32px;
}

.step-content {
  margin-bottom: 32px;
}

.step-title {
  font-size: 22px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 8px;
}

.quick-fill-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
  padding: 10px 16px;
  background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
  border-radius: 10px;
  border: 1px solid rgba(14, 165, 233, 0.2);
}

.quick-fill-hint {
  font-size: 12px;
  color: #64748b;
}

.step-desc {
  font-size: 14px;
  color: #64748b;
  margin-bottom: 24px;
}

/* 赛道选择 */
.track-selection {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.track-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.track-option {
  width: 100%;
}

.track-option :deep(.el-radio-button__inner) {
  width: 100%;
  text-align: left;
  padding: 20px;
  height: auto;
  border-radius: 12px !important;
  border: 1px solid #e2e8f0;
}

.track-card h4 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #1e293b;
}

.track-card p {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 8px;
}

.track-requirement {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: #475569;
}

/* 表单 */
.register-form {
  max-width: 600px;
}

/* 队员 */
.members-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.member-card {
  border: 1px solid #e2e8f0;
  border-radius: 12px;
}

.member-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.member-form {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.add-member-btn {
  width: 100%;
  margin-top: 8px;
}

/* 材料上传 */
.materials-upload {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.material-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.material-info h4 {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 4px;
}

.material-info p {
  font-size: 13px;
  color: #64748b;
}

/* 确认 */
.confirm-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.mt-4 {
  margin-top: 16px;
}

.confirm-agreement {
  margin-top: 24px;
  padding: 16px;
  background: #f0f9ff;
  border-radius: 12px;
}

/* 底部按钮 */
.step-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  padding-top: 24px;
  border-top: 1px solid #e2e8f0;
}
</style>
