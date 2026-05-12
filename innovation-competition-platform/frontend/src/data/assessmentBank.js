export const assessmentCategories = [
  { key: 'all', name: '全部分类', icon: 'Menu' },
  {
    key: 'entrepreneurship',
    name: '创业测评',
    children: ['entrepreneurial-spirit', 'entrepreneurial-personality', 'entrepreneurial-interest', 'entrepreneurial-ability']
  },
  {
    key: 'employment',
    name: '就业测评',
    children: ['career-temperament', 'career-values', 'career-interest', 'career-personality']
  },
  {
    key: 'ability',
    name: '能力测评',
    children: ['teamwork-ability', 'self-learning-ability', 'communication-ability', 'emotion-control-ability']
  }
]

export const assessmentList = [
  { id: 'entrepreneurial-spirit', title: '创业精神测评', category: 'entrepreneurship', categoryName: '创业测评', description: '评估创业主动性、机会识别意识、坚韧程度与风险承担倾向，帮助你了解自己的创业精神画像。', duration: 10, questionCount: 10, real: true, heat: 92, coverType: 'gradient', gradient: ['#14b8a6', '#2563eb'], tags: ['创业测评', '真实可测'] },
  { id: 'entrepreneurial-personality', title: '创业性格测评', category: 'entrepreneurship', categoryName: '创业测评', description: '评估学生在风险承受、决策风格、沟通开放性、自我驱动和情绪稳定性方面的创业性格特征。', duration: 10, questionCount: 10, real: true, heat: 88, coverType: 'gradient', gradient: ['#8b5cf6', '#06b6d4'], tags: ['创业测评', '真实可测'] },
  { id: 'entrepreneurial-interest', title: '创业兴趣测评', category: 'entrepreneurship', categoryName: '创业测评', description: '评估学生对创新问题、产品设计、市场验证、用户研究和项目实践的兴趣倾向。', duration: 10, questionCount: 10, real: true, heat: 85, coverType: 'gradient', gradient: ['#f59e0b', '#ef4444'], tags: ['创业测评', '真实可测'] },
  { id: 'entrepreneurial-ability', title: '创业能力测评', category: 'entrepreneurship', categoryName: '创业测评', description: '评估学生的问题分析、资源整合、执行推进、学习迭代和表达展示能力。', duration: 10, questionCount: 10, real: true, heat: 90, coverType: 'gradient', gradient: ['#10b981', '#14b8a6'], tags: ['创业测评', '真实可测'] },
  { id: 'career-temperament', title: '职业气质测评', category: 'employment', categoryName: '就业测评', description: '了解你的职业气质倾向，发现最适合你的职业角色和行业方向。', duration: 10, questionCount: 10, real: false, heat: 76, coverType: 'gradient', gradient: ['#6366f1', '#a78bfa'], tags: ['就业测评', '即将开放'] },
  { id: 'career-values', title: '职业价值观测评', category: 'employment', categoryName: '就业测评', description: '探索你的职业价值观排序，帮你找到与自身价值观匹配的理想工作模式。', duration: 10, questionCount: 10, real: false, heat: 72, coverType: 'gradient', gradient: ['#3b82f6', '#60a5fa'], tags: ['就业测评', '即将开放'] },
  { id: 'career-interest', title: '职业兴趣测评', category: 'employment', categoryName: '就业测评', description: '基于霍兰德兴趣模型，评估你的职业兴趣类型和发展方向。', duration: 10, questionCount: 10, real: false, heat: 80, coverType: 'gradient', gradient: ['#ec4899', '#f472b6'], tags: ['就业测评', '即将开放'] },
  { id: 'career-personality', title: '职业性格测评', category: 'employment', categoryName: '就业测评', description: '评估你的职业人格特质，了解你在工作环境中的行为风格和优势。', duration: 10, questionCount: 10, real: false, heat: 78, coverType: 'gradient', gradient: ['#8b5cf6', '#ec4899'], tags: ['就业测评', '即将开放'] },
  { id: 'teamwork-ability', title: '团队合作能力测评', category: 'ability', categoryName: '能力测评', description: '评估学生在团队沟通、角色协作、冲突处理、责任承担和共同目标推进方面的能力。', duration: 10, questionCount: 10, real: true, heat: 86, coverType: 'gradient', gradient: ['#0ea5e9', '#06b6d4'], tags: ['能力测评', '真实可测'] },
  { id: 'self-learning-ability', title: '自主学习能力测评', category: 'ability', categoryName: '能力测评', description: '评估你的自主学习意识、规划能力、学习策略运用和知识转化能力。', duration: 10, questionCount: 10, real: false, heat: 74, coverType: 'gradient', gradient: ['#f59e0b', '#eab308'], tags: ['能力测评', '即将开放'] },
  { id: 'communication-ability', title: '沟通交际能力测评', category: 'ability', categoryName: '能力测评', description: '评估你的口头/书面表达能力、倾听技巧和社会交往中的适应性。', duration: 10, questionCount: 10, real: false, heat: 82, coverType: 'gradient', gradient: ['#ef4444', '#f87171'], tags: ['能力测评', '即将开放'] },
  { id: 'emotion-control-ability', title: '情绪控制能力测评', category: 'ability', categoryName: '能力测评', description: '评估你在压力场景中的情绪觉察、调节策略和心理弹性水平。', duration: 10, questionCount: 10, real: false, heat: 70, coverType: 'gradient', gradient: ['#06b6d4', '#14b8a6'], tags: ['能力测评', '即将开放'] }
]

export function getAssessmentById(id) {
  return assessmentList.find(item => item.id === id) || null
}

export function getAssessmentsByCategory(category) {
  if (!category || category === 'all') return assessmentList
  return assessmentList.filter(item => item.category === category)
}

export function getAssessmentsBySearch(keyword) {
  if (!keyword || !keyword.trim()) return assessmentList
  const kw = keyword.trim().toLowerCase()
  return assessmentList.filter(item =>
    item.title.toLowerCase().includes(kw) ||
    item.description.toLowerCase().includes(kw) ||
    (item.tags && item.tags.some(tag => tag.toLowerCase().includes(kw))) ||
    item.categoryName.toLowerCase().includes(kw)
  )
}

export { getQuestionnaireById, validateQuestionnaire } from './assessmentQuestionnaires'
export { calculateScore, saveResult, getResult, clearResult, getLevel } from '@/utils/assessmentScoring'