<template>
  <div class="dashboard-page">
    <component :is="dashboardComponent" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useUserStore } from '@/stores/user'
import StudentDashboard from './student.vue'
import TeacherDashboard from './teacher.vue'
import JudgeDashboard from './judge.vue'
import AdminDashboard from './admin.vue'

const userStore = useUserStore()

const dashboardComponent = computed(() => {
  const role = userStore.userInfo?.role
  const components = {
    student: StudentDashboard,
    teacher: TeacherDashboard,
    judge: JudgeDashboard,
    admin: AdminDashboard
  }
  return components[role] || StudentDashboard
})
</script>

<style scoped>
.dashboard-page {
  height: 100%;
}
</style>
