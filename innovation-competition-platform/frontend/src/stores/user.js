import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as loginApi, getCurrentUser } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  // State
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(null)
  const isLoading = ref(false)

  // Getters
  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => userInfo.value?.role === 'admin')
  const isStudent = computed(() => userInfo.value?.role === 'student')
  const isTeacher = computed(() => userInfo.value?.role === 'teacher')
  const isJudge = computed(() => userInfo.value?.role === 'judge')
  const currentRole = computed(() => userInfo.value?.role || '')

  // Actions
  const setToken = (newToken) => {
    token.value = newToken
    if (newToken) {
      localStorage.setItem('token', newToken)
    } else {
      localStorage.removeItem('token')
    }
  }

  const setUserInfo = (info) => {
    userInfo.value = info
  }

  const login = async (credentials) => {
    isLoading.value = true
    try {
      const res = await loginApi(credentials)
      if (res.code === 200 && res.data?.token) {
        setToken(res.data.token)
        setUserInfo(res.data.user)
        return { success: true, data: res.data }
      }
      return { success: false, message: res.message || '登录失败' }
    } catch (error) {
      const message = error.response?.data?.message || '登录失败，请检查网络连接'
      return { success: false, message }
    } finally {
      isLoading.value = false
    }
  }

  const fetchUserInfo = async () => {
    if (!token.value) return false
    try {
      const res = await getCurrentUser()
      if (res.code === 200 && res.data?.user) {
        setUserInfo(res.data.user)
        return true
      }
      return false
    } catch (error) {
      logout()
      return false
    }
  }

  const logout = () => {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
  }

  const init = async () => {
    if (token.value && !userInfo.value) {
      return await fetchUserInfo()
    }
    return !!userInfo.value
  }

  return {
    token,
    userInfo,
    isLoading,
    isLoggedIn,
    isAdmin,
    isStudent,
    isTeacher,
    isJudge,
    currentRole,
    login,
    logout,
    fetchUserInfo,
    setToken,
    setUserInfo,
    init
  }
})
