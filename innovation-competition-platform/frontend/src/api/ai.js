import request from './request'

export const generateProjectSummary = (data) => request.post('/ai/project-summary', data)
export const generateBusinessAdvice = (data) => request.post('/ai/business-plan-advice', data)
export const generateRiskAnalysis = (data) => request.post('/ai/risk-analysis', data)
export const getAiRecords = () => request.get('/ai/records')
export const chatWithAi = (data) => request.post('/ai/chat', data)
export const getVoiceConfig = () => request.get('/ai/voice/config')
export const getAiHealth = () => request.get('/ai/health')
export const synthesizeTts = (data) => request.post('/ai/tts/synthesize', data)
export const getExpressions = () => request.get('/ai/expressions')
export const getModelInfo = () => request.get('/ai/model-info')

export function chatStream(message, sessionId, scene = '创新创业平台') {
  return fetch('/api/ai/chat/stream', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token') || ''}`,
    },
    body: JSON.stringify({ message, sessionId, scene }),
  })
}

export function voiceChatStream(message, sessionId, scene = '创新创业平台') {
  return fetch('/api/ai/voice/chat/stream', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token') || ''}`,
    },
    body: JSON.stringify({ message, sessionId, scene }),
  })
}

export function uploadAsrAudio(formData) {
  return fetch('/api/ai/asr', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token') || ''}`,
    },
    body: formData,
  })
}
