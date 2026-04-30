const META_LINE_PREFIXES = [
  "用户问的是", "首先我需要", "首先需要", "我需要", "还要", "得用",
  "检查一下", "是的，", "是的，这样", "这应该", "可以了", "按照要求", "符合要求", "回复里"
]

const META_LINE_KEYWORDS = [
  "自我思考", "思考过程", "分析步骤", "提示词复述", "内部说明", "用户问的是", "我需要给出"
]

const ANSWER_MARKERS = [
  "最终答案：", "答案：", "可以这样说：", "比如可以这样说：", "直接回答：", "简洁地说：", "可以回答："
]

export function detectEmotionByText(text) {
  const lower = (text || '').toLowerCase()
  if (/开心|高兴|太好了|哈哈|棒|厉害|优秀|成功|恭喜/.test(lower)) return 'happy'
  if (/害羞|脸红|不好意思|羞/.test(lower)) return 'shy'
  if (/生气|愤怒|烦|讨厌|气死/.test(lower)) return 'angry'
  if (/难过|伤心|失望|遗憾|抱歉/.test(lower)) return 'sad'
  if (/晕|头晕|困惑|迷茫|不懂/.test(lower)) return 'dizzy'
  if (/惊讶|天哪|哇|震惊|意外/.test(lower)) return 'surprise'
  return null
}

export function getExpressionByEmotion(emotion) {
  const map = {
    happy: '02 脸红爱心',
    shy: '02 脸红爱心',
    angry: '03 生气',
    sad: '08 流泪',
    dizzy: '04 晕',
    surprise: '07 星星眼'
  }
  return map[emotion] || '06 0.0'
}

export function updateExpressionByText(text) {
  const emotion = detectEmotionByText(text)
  if (emotion) {
    const expression = getExpressionByEmotion(emotion)
    window.__syncExpressionState && window.__syncExpressionState(expression)
  }
}

export function notifyLive2dHook(name, payload) {
  try {
    const hooks = window.__voiceLive2dHooks
    const fn = hooks && typeof hooks[name] === 'function' ? hooks[name] : null
    if (fn) fn(payload)
  } catch (_e) {}
}

export function useLive2d() {
  return {
    detectEmotionByText,
    getExpressionByEmotion,
    updateExpressionByText,
    notifyLive2dHook
  }
}
