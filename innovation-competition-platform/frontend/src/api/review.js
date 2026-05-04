import request from './request'

export const getPendingProjects = () => request.get('/reviews/projects')
export const getProjectForReview = (projectId) => request.get(`/reviews/projects/${projectId}`)
export const submitReview = (projectId, data) => request.post(`/reviews/projects/${projectId}`, data)
export const getProjectReviews = (projectId) => request.get(`/projects/${projectId}/reviews`)
export const getMyReviews = () => request.get('/reviews/my')
export const getAllReviews = () => request.get('/reviews/all')
