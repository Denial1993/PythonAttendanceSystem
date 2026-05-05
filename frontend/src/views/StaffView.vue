<template>
  <div class="container">
    <div class="board-container" style="margin-top:0;">
      <div class="board-title"><i class="fa-solid fa-users-gear"></i> 員工名冊管理</div>
      <div style="overflow-x:auto;">
        <table class="employee-table">
          <thead>
            <tr>
              <th>姓名</th>
              <th>電話</th>
              <th>角色</th>
            </tr>
          </thead>
          <tbody id="staffTableBody">
            <tr v-if="loading">
              <td colspan="3" style="text-align:center; padding:15px; color:#a0a0b0;">
                <i class="fa-solid fa-spinner fa-spin"></i> 載入資料中...
              </td>
            </tr>
            <tr v-else-if="users.length===0">
              <td colspan="3" style="text-align:center; padding:15px; color:#a0a0b0;">目前沒有員工資料</td>
            </tr>
            <tr v-for="u in users" :key="u.username">
              <td style="font-weight:bold;">{{ u.employee_name }}</td>
              <td>{{ u.phone || '未填寫' }}</td>
              <td>
                <span :style="{ color: roleColor(u.role), border: `1px solid ${roleColor(u.role)}`, padding:'2px 8px', borderRadius:'12px', fontSize:'0.8rem' }">
                  {{ roleName(u.role) }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { usersApi } from '@/api/usersApi'
import { useNotification } from '@/composables/useNotification'

const auth = useAuthStore()
const { showNotification } = useNotification()
const users = ref([])
const loading = ref(false)

function roleColor(r) {
  if (String(r)==='1') return '#fb923c'
  if (String(r)==='2') return '#4ade80'
  return '#d0d0d0'
}
function roleName(r) {
  if (String(r)==='1') return '系統管理員'
  if (String(r)==='2') return '人事主管'
  return '一般員工'
}

onMounted(async () => {
  loading.value = true
  try { users.value = await usersApi.getAllUsers(auth.username) }
  catch (err) { showNotification(err || '載入失敗', true) }
  finally { loading.value = false }
})
</script>
