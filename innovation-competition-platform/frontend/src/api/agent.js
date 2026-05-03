import request from './request'

const agentTimeout = { timeout: 120000 }

export const indexMaterials = (data) => request.post('/agent/index-materials', data, agentTimeout)
export const materialQa = (data) => request.post('/agent/material-qa', data, agentTimeout)
export const bpCheck = (data) => request.post('/agent/bp-check', data, agentTimeout)
export const generateRoadshow = (data) => request.post('/agent/roadshow', data, agentTimeout)
export const reviewAssist = (data) => request.post('/agent/review-assist', data, agentTimeout)
export const competitionRecommend = (data) => request.post('/agent/competition-recommend', data, agentTimeout)
export const getAgentTasks = (params) => request.get('/agent/tasks', { params })
export const getAgentTask = (id) => request.get(`/agent/tasks/${id}`)
export const smartNavigate = (data) => request.post('/agent/navigate', data, agentTimeout)
export const projectIdea = (data) => request.post('/agent/project-idea', data, agentTimeout)
export const mockDefense = (data) => request.post('/agent/mock-defense', data, agentTimeout)
export const batchReview = (data) => request.post('/agent/batch-review', data, agentTimeout)
export const smartFeedback = (data) => request.post('/agent/smart-feedback', data, agentTimeout)
export const reviewDraft = (data) => request.post('/agent/review-draft', data, agentTimeout)
export const scoreCheck = (data) => request.post('/agent/score-check', data, agentTimeout)
export const getCapabilities = () => request.get('/agent/capabilities')
