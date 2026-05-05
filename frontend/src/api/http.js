import axios from 'axios'

const http = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' }
})

// Request Interceptor：自動附加 username（query param 形式）
http.interceptors.request.use(config => {
  const username = localStorage.getItem('username')
  if (username) {
    config.params = config.params || {}
    // 只對需要驗證的 API 帶入，login/register 不需要
    const noAuthPaths = ['/auth/login', '/auth/register']
    const needsAuth = !noAuthPaths.some(p => config.url?.includes(p))
    if (needsAuth && !config.params.username) {
      config.params.username = username
    }
  }
  return config
})

// Response Interceptor：解包 data，統一錯誤處理
http.interceptors.response.use(
  res => res.data,
  err => {
    if (err.response?.status === 401) {
      localStorage.clear()
      window.location.hash = '/'
    }
    const detail = err.response?.data?.detail
    if (typeof detail === 'string') return Promise.reject(detail)
    if (Array.isArray(detail)) return Promise.reject(`欄位格式錯誤 (${detail[0]?.loc?.[1]}: ${detail[0]?.msg})`)
    if (!err.response) return Promise.reject('無法連接伺服器，請檢查網路')
    return Promise.reject(err.response?.data || err.message || '發生未知錯誤')
  }
)

export default http
