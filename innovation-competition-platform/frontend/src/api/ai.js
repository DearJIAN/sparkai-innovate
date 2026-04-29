import request from './request'

export const generateProjectSummary = (data) => request.post('/ai/project-summary', data)
export const generateBusinessAdvice = (data) => request.post('/ai/business-plan-advice', data)
export const generateRiskAnalysis = (data) => request.post('/ai/risk-analysis', data)
export const getAiRecords = () => request.get('/ai/records')
