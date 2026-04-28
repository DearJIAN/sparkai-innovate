import axios from 'axios'
import { ElMessage } from 'element-plus'

const request = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    const res = response.data

    // 业务错误处理（非 200 状态码）
    if (res.code !== 200) {
      // 登录相关接口的错误在页面处理
      const isAuthEndpoint = response.config?.url?.includes('/auth/')
      if (!isAuthEndpoint) {
        ElMessage.error(res.message || '请求失败')
      }

      // 401 未授权，清除 token 并跳转登录
      if (res.code === 401) {
        localStorage.removeItem('token')
        window.location.href = '/login'
      }
    }

    return res
  },
  (error) => {
    const { response } = error

    if (response) {
      const message = response.data?.message || `请求失败 (${response.status})`
      const isAuthEndpoint = response.config?.url?.includes('/auth/')

      if (!isAuthEndpoint) {
        ElMessage.error(message)
      }

      if (response.status === 401) {
        localStorage.removeItem('token')
        window.location.href = '/login'
      }
    } else {
      ElMessage.error('网络错误，请检查网络连接')
    }

    return Promise.reject(error)
  }
)

export default request
