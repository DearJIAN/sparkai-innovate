import request from './request'

// 公共接口（竞赛广场）
export const getPublicCompetitions = (params) => request.get('/public/competitions', { params })
export const getPublicCompetitionDetail = (id) => request.get(`/public/competitions/${id}`)
export const getPublicCompetitionTracks = (id) => request.get(`/public/competitions/${id}/tracks`)
export const getPublicCompetitionCategories = () => request.get('/public/competition-categories')

// 管理员接口
export const getCompetitions = (params) => request.get('/competitions', { params })
export const createCompetition = (data) => request.post('/competitions', data)
export const updateCompetition = (id, data) => request.put(`/competitions/${id}`, data)
export const deleteCompetition = (id) => request.delete(`/competitions/${id}`)
export const createCompetitionTrack = (competitionId, data) => request.post(`/competitions/${competitionId}/tracks`, data)
