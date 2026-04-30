import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

const request = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  },
  maxRedirects: 0,
  validateStatus: (status) => status >= 200 && status < 400
})

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

request.interceptors.response.use(
  async (response) => {
    if (response.status >= 300 && response.status < 400) {
      const redirectUrl = response.headers.location
      if (redirectUrl) {
        const originalConfig = response.config
        let newUrl = redirectUrl
        if (redirectUrl.startsWith('http')) {
          try {
            const urlObj = new URL(redirectUrl)
            newUrl = urlObj.pathname + urlObj.search
          } catch {
            newUrl = redirectUrl
          }
        }
        if (newUrl.startsWith(originalConfig.baseURL)) {
          newUrl = newUrl.substring(originalConfig.baseURL.length)
        }
        const newConfig = {
          ...originalConfig,
          url: newUrl
        }
        return request(newConfig)
      }
    }

    const res = response.data

    if (res.code !== 200) {
      const isAuthEndpoint = response.config?.url?.includes('/auth/')
      if (!isAuthEndpoint) {
        ElMessage.error(res.message || '请求失败')
      }

      if (res.code === 401) {
        localStorage.removeItem('token')
        router.push('/login')
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
        router.push('/login')
      }
    } else {
      ElMessage.error('网络错误，请检查网络连接')
    }

    return Promise.reject(error)
  }
)

export default request
