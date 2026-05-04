import request from './request'

export const getUsers = () => request.get('/users/')
export const getUser = (id) => request.get(`/users/${id}`)
export const createUser = (data) => request.post('/users/', data)
export const updateUser = (id, data) => request.put(`/users/${id}`, data)
export const toggleUserStatus = (id) => request.post(`/users/${id}/toggle-status`)
export const deleteUser = (id) => request.delete(`/users/${id}`)
