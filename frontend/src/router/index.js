import { createRouter, createWebHashHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  { path: '/', component: () => import('@/views/AuthView.vue'), meta: { public: true } },
  { path: '/home',     component: () => import('@/views/HomeView.vue') },
  { path: '/search',   component: () => import('@/views/SearchView.vue') },
  { path: '/leave',    component: () => import('@/views/LeaveView.vue') },
  { path: '/stats',    component: () => import('@/views/StatsView.vue') },
  { path: '/staff',    component: () => import('@/views/StaffView.vue'), meta: { minRole: 2 } },
  { path: '/settings', component: () => import('@/views/SettingsView.vue'), meta: { minRole: 1 } },
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

// Navigation Guard
router.beforeEach((to) => {
  const auth = useAuthStore()

  // 未登入 → 導向登入頁
  if (!to.meta.public && !auth.isLoggedIn) {
    return { path: '/' }
  }

  // 已登入訪問登入頁 → 導向首頁
  if (to.meta.public && auth.isLoggedIn) {
    return { path: '/home' }
  }

  // 角色權限控制
  if (to.meta.minRole) {
    const userRole = parseInt(auth.role) || 3
    if (userRole > to.meta.minRole) {
      return { path: '/home' }
    }
  }
})

export default router
