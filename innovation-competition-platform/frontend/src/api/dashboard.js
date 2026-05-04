import request from './request'

export const getDashboardStats = () => request.get('/dashboard/stats')
export const getRecentData = () => request.get('/dashboard/recent')
export const getPublicStats = () => request.get('/dashboard/public-stats')
