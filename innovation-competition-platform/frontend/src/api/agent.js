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
