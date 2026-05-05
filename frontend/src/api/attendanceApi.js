import http from './http'

export const attendanceApi = {
  checkIn: (employeeName, action, lat = null, lng = null) => {
    let url = `/attendance/?employee_name=${encodeURIComponent(employeeName)}&action=${encodeURIComponent(action)}`
    if (lat !== null && lng !== null) url += `&lat=${lat}&lng=${lng}`
    return http.post(url)
  },

  getPersonalStatus: (employeeName) =>
    http.get(`/attendance/${encodeURIComponent(employeeName)}`),

  search: (startDate, endDate, username) => {
    const params = { start_date: startDate, end_date: endDate, username }
    return http.get('/attendance/search', { params })
  },

  getSummary: (year, month, employeeName, username) =>
    http.get('/attendance/summary', { params: { year, month, employee_name: employeeName, username } })
}
