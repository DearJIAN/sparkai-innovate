const normalizedBase = (import.meta.env.BASE_URL || '/').replace(/\/+$/, '') || ''

export const APP_BASE = normalizedBase

export function withAppBase(path = '') {
  const normalizedPath = path.startsWith('/') ? path : `/${path}`
  return `${APP_BASE}${normalizedPath}` || normalizedPath
}

export function withApiBase(path = '') {
  return withAppBase(`/api${path.startsWith('/') ? path : `/${path}`}`)
}
