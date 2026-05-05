<template>
  <div class="container">
    <div class="board-container" style="margin-top:0;">
      <div class="board-title"><i class="fa-solid fa-magnifying-glass"></i> 查詢歷史紀錄</div>
      <div style="display:flex; gap:10px; margin-bottom:15px;">
        <input type="date" v-model="startDate" class="input-group" style="margin-bottom:0; padding:8px;">
        <input type="date" v-model="endDate"   class="input-group" style="margin-bottom:0; padding:8px;">
      </div>
      <input v-if="auth.isManager" type="text" v-model="targetEmployee"
             placeholder="目標員工帳號(選填)" class="input-group" style="padding:8px;">
      <button class="btn btn-primary" @click="performSearch">查詢</button>

      <div class="board-list" style="margin-top:15px;" id="searchResultList">
        <div v-if="loading" style="color:#a0a0b0; text-align:center;">
          <i class="fa-solid fa-spinner fa-spin"></i> 查詢中...
        </div>
        <div v-else-if="results.length === 0 && searched" style="color:#a0a0b0; text-align:center; padding:10px;">
          查無資料
        </div>
        <div v-for="r in results" :key="r.id || r.date + r.employee_name" class="board-item"
             style="flex-direction:column; align-items:flex-start; gap:4px;">
          <div style="display:flex; justify-content:space-between; width:100%;">
            <span style="font-weight:600;">{{ r.employee_name }}</span>
            <span class="status-work" style="font-size:0.8rem; padding:2px 8px; border-radius:8px;">{{ r.status }}</span>
          </div>
          <div style="font-size:0.8rem; color:#a0a0b0;">
            <i class="fa-regular fa-calendar"></i> {{ r.date }}
            &nbsp;|&nbsp; In: {{ r.check_in_time?.substring(0,5) || '-' }}
            &nbsp; Out: {{ r.check_out_time?.substring(0,5) || '-' }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { attendanceApi } from '@/api/attendanceApi'
import { useNotification } from '@/composables/useNotification'

const auth = useAuthStore()
const { showNotification } = useNotification()

const todayStr = new Date().toLocaleDateString('en-CA')
const startDate = ref(todayStr)
const endDate = ref(todayStr)
const targetEmployee = ref('')
const results = ref([])
const loading = ref(false)
const searched = ref(false)

async function performSearch() {
  loading.value = true; searched.value = false
  try {
    const user = targetEmployee.value || auth.username
    results.value = await attendanceApi.search(startDate.value, endDate.value, user)
    searched.value = true
  } catch (err) {
    showNotification(err || '查詢失敗', true)
  } finally {
    loading.value = false
  }
}
</script>
