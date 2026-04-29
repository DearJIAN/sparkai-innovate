import request from './request'

export const getFiles = (projectId, params) => request.get(`/projects/${projectId}/files`, { params })
export const uploadFile = (projectId, formData) => request.post(`/projects/${projectId}/files`, formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
})
export const downloadFile = (fileId) => request.get(`/files/${fileId}/download`, { responseType: 'blob' })
export const deleteFile = (fileId) => request.delete(`/files/${fileId}`)
