import request from './request'

// 学生相关接口
export const createRegistration = (data) => request.post('/registrations', data)
export const getRegistration = (id) => request.get(`/registrations/${id}`)
export const updateRegistration = (id, data) => request.put(`/registrations/${id}`, data)
export const submitRegistration = (id) => request.post(`/registrations/${id}/submit`)
export const getMyRegistrations = () => request.get('/my-registrations')

// 队员相关
export const addRegistrationMember = (registrationId, data) => request.post(`/registrations/${registrationId}/members`, data)
export const updateRegistrationMember = (memberId, data) => request.put(`/registration-members/${memberId}`, data)
export const deleteRegistrationMember = (memberId) => request.delete(`/registration-members/${memberId}`)

// 材料相关
export const uploadRegistrationMaterial = (registrationId, data) => request.post(`/registrations/${registrationId}/materials`, data)
export const deleteRegistrationMaterial = (materialId) => request.delete(`/registration-materials/${materialId}`)

// 管理员相关接口
export const getAdminRegistrations = (params) => request.get('/admin/registrations', { params })
export const getAdminRegistrationDetail = (id) => request.get(`/admin/registrations/${id}`)
export const approveRegistration = (id) => request.post(`/admin/registrations/${id}/approve`)
export const rejectRegistration = (id, data) => request.post(`/admin/registrations/${id}/reject`, data)
export const getRegistrationStatistics = () => request.get('/admin/registrations/statistics')
