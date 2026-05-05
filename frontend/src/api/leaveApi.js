import http from './http'

export const leaveApi = {
  getBalance: (username) =>
    http.get('/leave/balance', { params: { username } }),

  getMyLeaves: (username) =>
    http.get('/leave', { params: { username } }),

  getPending: (username) =>
    http.get('/leave/pending', { params: { username } }),

  submitLeave: (payload) =>
    http.post('/leave', payload),

  approve: (leaveId, username) =>
    http.put(`/leave/${leaveId}/approve`, null, { params: { username } }),

  reject: (leaveId, username) =>
    http.put(`/leave/${leaveId}/reject`, null, { params: { username } })
}
