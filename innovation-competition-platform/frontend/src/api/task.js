import request from './request'

export const getTasks = (projectId, params) => request.get(`/projects/${projectId}/tasks`, { params })
export const createTask = (projectId, data) => request.post(`/projects/${projectId}/tasks`, data)
export const updateTask = (taskId, data) => request.put(`/tasks/${taskId}`, data)
export const deleteTask = (taskId) => request.delete(`/tasks/${taskId}`)
