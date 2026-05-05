import http from './http'

export const usersApi = {
  getMe: (username) =>
    http.get('/users/me', { params: { username } }),

  updateMe: (payload) =>
    http.put('/users/me', payload),

  getAllUsers: (username) =>
    http.get('/users/', { params: { username } })
}
