import http from './http'

export const chatApi = {
  sendMessage: (employeeName, query) =>
    http.post('/chat', { employee_name: employeeName, query })
}
