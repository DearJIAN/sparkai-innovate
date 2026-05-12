import request from './request'

export const uploadMaterial = (formData) =>
  request.post('/material-evaluation/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })

export const startAnalysis = (taskId) =>
  request.post(`/material-evaluation/tasks/${taskId}/analyze`)

export const completeAnalysis = (taskId) =>
  request.post(`/material-evaluation/tasks/${taskId}/complete`)

export const getTaskStatus = (taskId) =>
  request.get(`/material-evaluation/tasks/${taskId}`)

export const getReport = (taskId) =>
  request.get(`/material-evaluation/reports/${taskId}`)

export const downloadReportPdf = (taskId) =>
  request.get(`/material-evaluation/reports/${taskId}/pdf`, {
    responseType: 'blob'
  })

export const getDownloadUrl = (taskId) =>
  `/api/material-evaluation/reports/${taskId}/pdf`

export const getMyTasks = (params = {}) =>
  request.get('/material-evaluation/tasks', { params })