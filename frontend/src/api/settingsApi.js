import http from './http'

export const settingsApi = {
  getSettings: (username) =>
    http.get('/settings', { params: { username } }),

  saveSettings: (payload, username) =>
    http.put('/settings', payload, { params: { username } })
}
