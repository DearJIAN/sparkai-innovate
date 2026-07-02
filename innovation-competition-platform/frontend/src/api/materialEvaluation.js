import request from './request'
import { withApiBase } from '@/utils/appBase'

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
  request.get(`/material-evaluation/reports/${taskId}/download`, {
    timeout: 300000
  })

export const getDownloadUrl = (taskId) =>
  withApiBase(`/material-evaluation/reports/${taskId}/download`)

export const getMyTasks = (params = {}) =>
  request.get('/material-evaluation/tasks', { params })
