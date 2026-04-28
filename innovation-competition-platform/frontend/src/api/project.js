import request from './request'

export const getProjects = (params) => request.get('/projects', { params })
export const getProject = (id) => request.get(`/projects/${id}`)
export const createProject = (data) => request.post('/projects', data)
export const updateProject = (id, data) => request.put(`/projects/${id}`, data)
export const deleteProject = (id) => request.delete(`/projects/${id}`)
export const submitProject = (id) => request.post(`/projects/${id}/submit`)
