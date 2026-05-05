import http from './http'

export const authApi = {
  login: (username, password) =>
    http.post('/auth/login', { username, password }),

  register: (username, password, employee_name) =>
    http.post('/auth/register', { username, password, employee_name })
}
