<template>
  <div class="container">
    <!-- 個人資料 -->
    <div class="board-container" style="margin-top:0;">
      <div class="board-title" style="display:flex; justify-content:space-between;">
        <span><i class="fa-solid fa-id-card"></i> 我的資料</span>
        <button v-if="!editing" id="editProfileBtn" class="btn btn-primary"
                style="padding:4px 12px; width:auto; font-size:0.85rem;" @click="editing=true">編輯資料</button>
      </div>

      <!-- 檢視模式 -->
      <div v-if="!editing" id="profileViewMode" style="font-size:0.9rem; line-height:2;">
        <div>姓名：<span id="profileName">{{ profile.employee_name || auth.employeeName }}</span></div>
        <div>電話：<span id="profilePhone">{{ profile.phone || '-' }}</span></div>
        <div>地址：<span id="profileAddress">{{ profile.address || '-' }}</span></div>
        <div v-if="auth.isManager" id="profileSalaryRow">薪資：<span id="profileSalary">{{ profile.salary || '-' }}</span></div>
      </div>

      <!-- 編輯模式 -->
      <div v-else id="profileEditMode" style="font-size:0.9rem; line-height:2;">
        <div style="margin-bottom:10px;">姓名：<span id="editProfileName">{{ auth.employeeName }}</span>
          <span style="color:#a0a0b0; font-size:0.8rem;">(不可修改)</span>
        </div>
        <div class="input-group">
          <label>電話：</label>
          <input type="text" v-model="editPhone" id="editProfilePhone" placeholder="0912-345-678">
        </div>
        <div class="input-group">
          <label>地址：</label>
          <input type="text" v-model="editAddress" id="editProfileAddress" placeholder="台北市...">
        </div>
        <div v-if="auth.isManager" id="editSalaryRow" class="input-group">
          <label>薪資（僅管理員可編輯）：</label>
          <input type="number" v-model="editSalary" id="editProfileSalary">
        </div>
        <div style="display:flex; gap:10px;">
          <button class="btn btn-primary" style="padding:8px; flex:1;" @click="saveProfile">儲存</button>
          <button class="btn" style="padding:8px; flex:1;" @click="editing=false">取消</button>
        </div>
      </div>
    </div>

    <!-- 月份統計 -->
    <div class="board-container">
      <div class="board-title" style="display:flex; justify-content:space-between; align-items:center;">
        <span><i class="fa-solid fa-chart-pie"></i> 月份統計</span>
        <input type="month" v-model="month" @change="loadSummary"
          style="background:transparent; color:white; border:1px solid rgba(255,255,255,0.2); border-radius:5px; padding:2px;">
      </div>
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-num" id="statWorkDays">{{ stats.work_days ?? '-' }}</div>
          <div class="stat-label">出勤天數</div>
        </div>
        <div class="stat-card">
          <div class="stat-num" id="statLateCount"
               style="background:linear-gradient(135deg,#fb923c,#f43f5e);-webkit-background-clip:text;">
            {{ stats.late_count ?? '-' }}
          </div>
          <div class="stat-label">遲到次數</div>
        </div>
      </div>
      <ul id="dailyDetailList" style="list-style:none; padding:0; margin:0; font-size:0.85rem;">
        <li v-if="summaryLoading" style="color:#a0a0b0; text-align:center; padding:10px;">
          <i class="fa-solid fa-spinner fa-spin"></i>
        </li>
        <li v-else-if="dailyDetails.length===0" style="color:#a0a0b0; text-align:center; padding:10px;">
          本月尚無打卡紀錄
        </li>
        <li v-for="d in dailyDetails" :key="d.date"
            style="padding:10px 0; border-bottom:1px solid rgba(255,255,255,0.1); display:flex; flex-direction:column; gap:5px;">
          <div style="display:flex; justify-content:space-between;">
            <span><i class="fa-regular fa-calendar"></i> {{ d.date }}</span>
            <span :style="{ color: dayStatusColor(d), fontWeight:'bold' }">{{ dayStatusText(d) }}</span>
          </div>
          <div style="font-size:0.8rem; color:#a0a0b0;">
            In: {{ d.check_in_time?.substring(0,5) || '-' }} | Out: {{ d.check_out_time?.substring(0,5) || '-' }}
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { usersApi } from '@/api/usersApi'
import { attendanceApi } from '@/api/attendanceApi'
import { useNotification } from '@/composables/useNotification'

const auth = useAuthStore()
const { showNotification } = useNotification()

const editing = ref(false)
const profile = ref({})
const editPhone = ref('')
const editAddress = ref('')
const editSalary = ref('')

const month = ref(new Date().toISOString().substring(0,7))
const stats = ref({})
const dailyDetails = ref([])
const summaryLoading = ref(false)

function dayStatusColor(d) {
  if (d.is_missing_checkin || d.is_missing_checkout) return '#f87171'
  if (d.is_late) return '#fb923c'
  return '#4ade80'
}
function dayStatusText(d) {
  if (d.is_missing_checkin) return '未打上班卡'
  if (d.is_late) return `遲到 (${d.late_minutes}分)`
  if (d.is_missing_checkout) return '未打下班卡'
  return '正常'
}

async function loadProfile() {
  try {
    const data = await usersApi.getMe(auth.username)
    profile.value = data
    editPhone.value = data.phone || ''
    editAddress.value = data.address || ''
    editSalary.value = data.salary || ''
  } catch {}
}

async function saveProfile() {
  const payload = { username: auth.username, phone: editPhone.value, address: editAddress.value }
  if (auth.isManager && editSalary.value) payload.salary = parseInt(editSalary.value)
  try {
    const data = await usersApi.updateMe(payload)
    profile.value = { ...profile.value, ...data }
    editing.value = false
    showNotification('個人資料更新成功！')
  } catch (err) { showNotification(err || '更新失敗', true) }
}

async function loadSummary() {
  summaryLoading.value = true
  try {
    const [y, m] = month.value.split('-').map(Number)
    const data = await attendanceApi.getSummary(y, m, auth.employeeName, auth.username)
    stats.value = data
    dailyDetails.value = data.daily_details || []
  } catch (err) {
    stats.value = {}; dailyDetails.value = []
  } finally { summaryLoading.value = false }
}

onMounted(() => { loadProfile(); loadSummary() })
</script>
