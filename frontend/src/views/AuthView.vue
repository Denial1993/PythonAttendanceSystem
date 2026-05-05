<template>
  <div class="container">
    <h1><i class="fa-solid fa-clock"></i> 智能打卡系統</h1>
    <p class="subtitle">請先登入系統以進行操作</p>

    <div class="auth-tabs">
      <div class="auth-tab" :class="{ active: tab === 0 }" @click="tab = 0">登入</div>
      <div class="auth-tab" :class="{ active: tab === 1 }" @click="tab = 1">註冊</div>
    </div>

    <!-- 登入表單 -->
    <div v-show="tab === 0">
      <div class="input-group">
        <label><i class="fa-solid fa-user"></i> 帳號</label>
        <input v-model="loginUsername" type="text" placeholder="請輸入帳號" id="loginUsername">
      </div>
      <div class="input-group">
        <label><i class="fa-solid fa-lock"></i> 密碼</label>
        <input v-model="loginPassword" type="password" placeholder="請輸入密碼" id="loginPassword"
               @keyup.enter="performLogin">
      </div>
      <button class="btn btn-primary" id="btnLogin" @click="performLogin" :disabled="loading">
        <i class="fa-solid fa-spinner fa-spin" v-if="loading"></i>
        <span v-else>登入進系統</span>
      </button>
    </div>

    <!-- 註冊表單 -->
    <div v-show="tab === 1">
      <div class="input-group">
        <label>帳號</label>
        <input v-model="regUsername" type="text" id="regUsername">
      </div>
      <div class="input-group">
        <label>密碼</label>
        <input v-model="regPassword" type="password" id="regPassword">
      </div>
      <div class="input-group">
        <label>真實姓名</label>
        <input v-model="regName" type="text" id="regEmployeeName">
      </div>
      <button class="btn btn-primary" id="btnRegister" @click="performRegister" :disabled="loading">
        <i class="fa-solid fa-spinner fa-spin" v-if="loading"></i>
        <span v-else>註冊帳號</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '@/api/authApi'
import { useAuthStore } from '@/stores/auth'
import { useNotification } from '@/composables/useNotification'

const router = useRouter()
const auth = useAuthStore()
const { showNotification } = useNotification()

const tab = ref(0)
const loading = ref(false)
const loginUsername = ref('')
const loginPassword = ref('')
const regUsername = ref('')
const regPassword = ref('')
const regName = ref('')

async function performLogin() {
  if (!loginUsername.value || !loginPassword.value) return
  loading.value = true
  try {
    const data = await authApi.login(loginUsername.value, loginPassword.value)
    auth.login(data, loginUsername.value)
    router.push('/home')
  } catch (err) {
    showNotification(err || '登入失敗', true)
  } finally {
    loading.value = false
  }
}

async function performRegister() {
  if (!regUsername.value || !regPassword.value || !regName.value) {
    showNotification('請填寫所有欄位！', true); return
  }
  loading.value = true
  try {
    await authApi.register(regUsername.value, regPassword.value, regName.value)
    showNotification('註冊成功！請登入。')
    tab.value = 0
    regUsername.value = ''; regPassword.value = ''; regName.value = ''
  } catch (err) {
    showNotification(err || '註冊失敗', true)
  } finally {
    loading.value = false
  }
}
</script>
