<template>
  <nav class="sidebar" :class="{ show: mobileOpen }">
    <div class="sidebar-header">
      <div class="nav-logo">
        <i class="fa-solid fa-clock"></i> 智能打卡
      </div>
    </div>

    <div class="nav-menu" id="navMenu">
      <RouterLink to="/home"   class="nav-link" @click="closeMobile">
        <i class="fa-solid fa-house"></i> 首頁
      </RouterLink>
      <RouterLink to="/search" class="nav-link" @click="closeMobile">
        <i class="fa-solid fa-magnifying-glass"></i> 查詢紀錄
      </RouterLink>
      <RouterLink to="/leave"  class="nav-link" @click="closeMobile">
        <i class="fa-solid fa-calendar-minus"></i> 請假系統
      </RouterLink>
      <RouterLink to="/stats"  class="nav-link" @click="closeMobile">
        <i class="fa-solid fa-chart-pie"></i> 出勤統計
      </RouterLink>
      <RouterLink v-if="auth.isManager" to="/staff" class="nav-link" @click="closeMobile">
        <i class="fa-solid fa-users-gear"></i> 員工名冊
      </RouterLink>
      <RouterLink v-if="auth.isAdmin" to="/settings" class="nav-link" @click="closeMobile">
        <i class="fa-solid fa-gear"></i> 系統設定
      </RouterLink>
    </div>

    <div class="sidebar-footer">
      <div class="nav-user">
        <i class="fa-solid fa-circle-user" style="font-size:1.5rem; color:#a0a0b0;"></i>
        <span class="nav-user-name">{{ auth.employeeName }}</span>
      </div>
      <button class="btn-logout-sm" @click="handleLogout">
        <i class="fa-solid fa-right-from-bracket"></i> 登出
      </button>
    </div>
  </nav>

  <!-- Mobile overlay -->
  <div v-if="mobileOpen" class="sidebar-overlay" @click="closeMobile"></div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

const props = defineProps({ mobileOpen: Boolean })
const emit = defineEmits(['close'])

function closeMobile() { emit('close') }

function handleLogout() {
  auth.logout()
  router.push('/')
}
</script>
