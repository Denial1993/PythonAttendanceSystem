import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const employeeName = ref(localStorage.getItem('employee_name') || '')
  const username = ref(localStorage.getItem('username') || '')
  const role = ref(localStorage.getItem('role') || '')

  const isLoggedIn = computed(() => !!employeeName.value)
  const isAdmin = computed(() => role.value === '1')
  const isManager = computed(() => role.value === '1' || role.value === '2')

  function login(data, user) {
    employeeName.value = data.employee_name
    username.value = user
    role.value = String(data.role)
    localStorage.setItem('employee_name', data.employee_name)
    localStorage.setItem('username', user)
    localStorage.setItem('role', String(data.role))
  }

  function logout() {
    employeeName.value = ''
    username.value = ''
    role.value = ''
    localStorage.clear()
  }

  return { employeeName, username, role, isLoggedIn, isAdmin, isManager, login, logout }
})
