import request from './request'

export const getMembers = (projectId) => request.get(`/projects/${projectId}/members`)
export const addMember = (projectId, data) => request.post(`/projects/${projectId}/members`, data)
export const updateMember = (memberId, data) => request.put(`/members/${memberId}`, data)
export const deleteMember = (memberId) => request.delete(`/members/${memberId}`)
