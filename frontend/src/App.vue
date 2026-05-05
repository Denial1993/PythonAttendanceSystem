<template>
  <div class="app-layout">
    <!-- Sidebar（已登入才顯示）-->
    <AppNavbar v-if="auth.isLoggedIn" :mobileOpen="mobileOpen" @close="mobileOpen=false" />

    <div class="main-wrapper">
      <!-- Mobile Header -->
      <header v-if="auth.isLoggedIn" class="mobile-header">
        <div class="nav-logo"><i class="fa-solid fa-clock"></i> 智能打卡</div>
        <button class="mobile-menu-btn" @click="mobileOpen=!mobileOpen">
          <i class="fa-solid fa-bars"></i>
        </button>
      </header>

      <main class="main-content">
        <RouterView />
      </main>

      <!-- Footer -->
      <footer v-if="auth.isLoggedIn" class="footer">
        <div class="footer-col">
          <h4><i class="fa-solid fa-clock"></i> 智能打卡系統</h4>
          <div>基於 AI 的人事考勤管理平台</div>
          <div>Powered by FastAPI + Vue 3 + Gemini</div>
        </div>
        <div class="footer-col">
          <h4>功能</h4>
          <div>GPS 定位打卡</div>
          <div>請假管理</div>
          <div>出勤統計</div>
        </div>
        <div class="footer-bottom">
          © 2026 智能打卡系統. All rights reserved.
        </div>
      </footer>
    </div>
  </div>

  <!-- 全域元件 -->
  <NotificationToast />
  <ChatWidget v-if="auth.isLoggedIn" />
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import AppNavbar from '@/components/AppNavbar.vue'
import NotificationToast from '@/components/NotificationToast.vue'
import ChatWidget from '@/components/ChatWidget.vue'

const auth = useAuthStore()
const mobileOpen = ref(false)
</script>
