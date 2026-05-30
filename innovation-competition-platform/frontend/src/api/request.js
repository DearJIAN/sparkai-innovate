import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'
import { withApiBase } from '@/utils/appBase'

const request = axios.create({
  baseURL: withApiBase(''),
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
    const skipGlobalError = !!response.config?.skipGlobalError
    if (response.config.responseType === 'blob' || response.config.responseType === 'arraybuffer') {
      const ct = response.headers?.['content-type'] || ''
      const isErrorStatus = response.status >= 400
      const isNonBinaryContent = ct && !ct.includes('pdf') && !ct.includes('octet-stream') && !ct.includes('image')

      if (isErrorStatus || (isNonBinaryContent && response.data?.size < 1000)) {
        const text = await new Promise(resolve => {
          const reader = new FileReader()
          reader.onload = () => resolve(reader.result)
          reader.readAsText(response.data)
        })
        try {
          const json = JSON.parse(text)
          if (json.message) {
            ElMessage.error(json.message)
          }
        } catch {
        }
        return Promise.reject(new Error('下载内容格式异常'))
      }
      return response.data
    }

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
      if (!isAuthEndpoint && !skipGlobalError) {
        ElMessage.error(res.message || '请求失败')
      }

      if (res.code === 401) {
        const currentPath = router.currentRoute.value.fullPath
        localStorage.removeItem('token')
        router.push({
          path: '/login',
          query: currentPath && currentPath !== '/login' ? { redirect: currentPath } : {}
        })
      }
    }

    return res
  },
  (error) => {
    const { response } = error
    const skipGlobalError = !!response?.config?.skipGlobalError

    if (response) {
      const message = response.data?.message || `请求失败 (${response.status})`
      const isAuthEndpoint = response.config?.url?.includes('/auth/')

      if (!isAuthEndpoint && !skipGlobalError) {
        ElMessage.error(message)
      }

      if (response.status === 401) {
        const currentPath = router.currentRoute.value.fullPath
        localStorage.removeItem('token')
        router.push({
          path: '/login',
          query: currentPath && currentPath !== '/login' ? { redirect: currentPath } : {}
        })
      }
    } else if (!error?.config?.skipGlobalError) {
      ElMessage.error('网络错误，请检查网络连接')
    }

    return Promise.reject(error)
  }
)

export default request
