import request from './request'

export const getCompetitions = (params) => request.get('/competitions', { params })
export const createCompetition = (data) => request.post('/competitions', data)
export const updateCompetition = (id, data) => request.put(`/competitions/${id}`, data)
export const deleteCompetition = (id) => request.delete(`/competitions/${id}`)
