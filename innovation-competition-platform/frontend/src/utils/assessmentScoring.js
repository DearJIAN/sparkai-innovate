export function getLevel(rawScore) {
  if (rawScore >= 35) return { key: 'excellent', label: '优秀', desc: '表现突出，具备较强的创业或团队实践潜力。' }
  if (rawScore >= 28) return { key: 'good', label: '良好', desc: '具备较好的相关能力，适合参与真实项目或竞赛实践。' }
  if (rawScore >= 19) return { key: 'medium', label: '发展中', desc: '已具备一定基础，但稳定性和行动深度仍需要继续提升。' }
  return { key: 'improve', label: '待提升', desc: '当前相关特质还处在起步阶段，建议从小任务和低风险实践开始积累经验。' }
}

export const maxScore = 40
export const questionCount = 10

export function calculateScore(questionnaire, answers) {
  const questions = questionnaire.questions
  let totalScore = 0
  const dimensionMap = {}

  questions.forEach((q) => {
    const selected = answers[q.id]
    const score = selected ? Number(selected) : 0
    totalScore += score

    if (!dimensionMap[q.dimension]) {
      dimensionMap[q.dimension] = { name: q.dimension, score: 0, maxScore: 0, count: 0 }
    }
    dimensionMap[q.dimension].score += score
    dimensionMap[q.dimension].maxScore += 4
    dimensionMap[q.dimension].count += 1
  })

  const scoreRate = Math.round((totalScore / maxScore) * 100)
  const level = getLevel(totalScore)

  const dimensions = Object.values(dimensionMap).map(d => ({
    name: d.name,
    score: d.score,
    maxScore: d.maxScore,
    percent: Math.round((d.score / d.maxScore) * 100)
  }))

  const strong = dimensions.filter(d => d.score >= d.maxScore * 0.75)
  const weak = dimensions.filter(d => d.score < d.maxScore * 0.5)

  const suggestions = []
  if (strong.length > 0) {
    suggestions.push(`你在「${strong.map(d => d.name).join('、')}」方面表现突出，建议在项目实践中充分发挥优势，带动团队成长。`)
  }
  if (weak.length > 0) {
    suggestions.push(`「${weak.map(d => d.name).join('、')}」方面还有提升空间，建议制定专项提升计划，通过真实项目、课程学习和导师指导逐步加强。`)
  }
  if (weak.length === 0 && strong.length === 0) {
    suggestions.push('各维度表现较为均衡，建议选择一到两个优势方向重点发展，同时保持其他维度的持续提升。')
  }
  suggestions.push('建议每 3-6 个月重新测评一次，跟踪能力成长轨迹。')

  const answeredCount = questions.filter(q => answers[q.id] && Number(answers[q.id]) > 0).length
  const answeredAll = answeredCount === questions.length

  return {
    assessmentId: questionnaire.id,
    title: questionnaire.title,
    categoryName: questionnaire.category,
    totalScore,
    maxScore,
    scoreRate,
    completedRate: answeredAll ? 100 : Math.round((answeredCount / questions.length) * 100),
    questionCount: questions.length,
    answeredCount,
    level: level.key,
    levelText: level.label,
    levelDesc: level.desc,
    summary: generateSummary(level.key, dimensions, questionnaire.resultDimensions),
    suggestions,
    strengths: dimensions.filter(d => d.score >= d.maxScore * 0.75),
    risks: dimensions.filter(d => d.score < d.maxScore * 0.5),
    dimensions,
    answeredAll,
    completedAt: new Date().toISOString()
  }
}

function generateSummary(levelKey, dimensions, resultDimensions) {
  const best = dimensions.reduce((a, b) => a.percent > b.percent ? a : b, dimensions[0])
  const worst = dimensions.reduce((a, b) => a.percent < b.percent ? a : b, dimensions[0])

  const summaries = {
    excellent: '整体测评结果非常优秀，你在多个评估维度上都展现出了较高的素养和潜力。',
    good: '整体表现良好，大部分维度都达到了不错的水平，已经具备参与真实项目的基础。',
    medium: '整体处于发展中水平，基础能力已初步建立，但在多个维度上仍有较大的提升空间。',
    improve: '目前在该领域的能力画像还有较大的提升空间，建议从基础开始系统构建能力体系。'
  }

  let text = summaries[levelKey] || ''
  if (best && worst && best.name !== worst.name) {
    text += ` 你的「${best.name}」维度表现最好（${best.percent}%），「${worst.name}」是相对薄弱环节（${worst.percent}%），建议重点关注。`
  } else if (dimensions.length > 1) {
    text += ` 建议在各维度上均衡发展，制定系统化的提升计划。`
  }
  return text
}

export function saveResult(assessmentId, result) {
  try {
    const key = `assessment_result_${assessmentId}`
    sessionStorage.setItem(key, JSON.stringify(result))
    return true
  } catch {
    return false
  }
}

export function getResult(assessmentId) {
  try {
    const key = `assessment_result_${assessmentId}`
    const raw = sessionStorage.getItem(key)
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

export function clearResult(assessmentId) {
  try {
    const key = `assessment_result_${assessmentId}`
    sessionStorage.removeItem(key)
  } catch {
    // silent
  }
}

export function persistTempAnswers(assessmentId, answers) {
  try {
    sessionStorage.setItem(`assessment_temp_${assessmentId}`, JSON.stringify(answers))
  } catch {
    // silent
  }
}

export function getTempAnswers(assessmentId) {
  try {
    const raw = sessionStorage.getItem(`assessment_temp_${assessmentId}`)
    return raw ? JSON.parse(raw) : {}
  } catch {
    return {}
  }
}

export function clearTempAnswers(assessmentId) {
  try {
    sessionStorage.removeItem(`assessment_temp_${assessmentId}`)
  } catch {
    // silent
  }
}