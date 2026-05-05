<template>
  <div class="container">
    <!-- 打卡按鈕 -->
    <div class="buttons-grid">
      <button class="btn btn-check-in"  @click="doAction('上班')">
        <i class="fa-solid fa-right-to-bracket"></i> 上班
      </button>
      <button class="btn btn-lunch-out" @click="doAction('吃午餐')">
        <i class="fa-solid fa-utensils"></i> 吃午餐
      </button>
      <button class="btn btn-lunch-in"  @click="doAction('午餐回來')">
        <i class="fa-solid fa-mug-hot"></i> 午餐回來
      </button>
      <button class="btn btn-check-out" @click="doAction('下班')">
        <i class="fa-solid fa-right-from-bracket"></i> 下班
      </button>
    </div>

    <!-- 今日狀態 -->
    <div class="board-container" style="background: rgba(255,255,255,0.05);">
      <p style="margin:0 0 10px 0; font-weight:600;">
        <i class="fa-solid fa-circle-info"></i> 目前狀態：
        <span style="color:#ff7eb3">{{ todayStatus }}</span>
      </p>
      <div style="display:flex; justify-content:space-between; font-size:0.9rem; border-top:1px solid rgba(255,255,255,0.1); padding-top:10px;">
        <span>In: <b>{{ checkIn }}</b></span>
        <span>Out: <b>{{ checkOut }}</b></span>
      </div>
    </div>

    <!-- 大家出勤看板（管理員/主管） -->
    <div v-if="auth.isManager" class="board-container" id="everyoneBoardContainer">
      <div class="board-title" style="display:flex; justify-content:space-between; align-items:center;">
        <span><i class="fa-solid fa-users"></i> 大家的出勤狀況</span>
        <input type="month" v-model="boardMonth" @change="loadBoard"
          style="background:transparent; color:white; border:1px solid rgba(255,255,255,0.2); border-radius:5px; padding:2px; font-size:0.85rem;">
      </div>
      <div class="board-list" id="boardList">
        <div v-if="boardLoading" style="color:#a0a0b0; text-align:center;">
          <i class="fa-solid fa-spinner fa-spin"></i> 載入中...
        </div>
        <template v-else>
          <div v-if="boardItems.length === 0" style="color:#a0a0b0; padding:10px; text-align:center;">
            此月份尚無紀錄
          </div>
          <div v-for="r in boardItems" :key="r.id || r.date + r.employee_name" class="board-item"
               style="flex-direction:column; align-items:flex-start; gap:4px;">
            <div style="display:flex; justify-content:space-between; width:100%;">
              <span style="font-weight:600;">{{ r.employee_name }}</span>
              <span class="status-work" style="font-size:0.8rem; padding:2px 8px; border-radius:8px;">{{ r.status }}</span>
            </div>
            <div style="font-size:0.8rem; color:#a0a0b0; display:flex; justify-content:space-between; width:100%;">
              <span><i class="fa-regular fa-calendar"></i> {{ r.date }}</span>
              <span>
                {{ r.check_in_time?.substring(0,5) || '' }}
                <i v-if="auth.isAdmin && r.check_in_lat && r.check_in_lng"
                   class="fa fa-map-marker-alt" style="cursor:pointer;color:#4ade80;"
                   @click="openMap(r.check_in_lat, r.check_in_lng, r.employee_name + ' 上班打卡地點')"></i>
                <i v-if="auth.isAdmin && r.check_out_lat && r.check_out_lng"
                   class="fa fa-map-marker-alt" style="cursor:pointer;color:#f87171;"
                   @click="openMap(r.check_out_lat, r.check_out_lng, r.employee_name + ' 下班打卡地點')"></i>
              </span>
            </div>
          </div>
        </template>
      </div>
    </div>

    <!-- Map Modal -->
    <MapModal v-model="showMap" :lat="mapLat" :lng="mapLng" :title="mapTitle" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { attendanceApi } from '@/api/attendanceApi'
import { useGeolocation } from '@/composables/useGeolocation'
import { useNotification } from '@/composables/useNotification'
import MapModal from '@/components/MapModal.vue'

const auth = useAuthStore()
const { getPositionWithTimeout } = useGeolocation()
const { showNotification } = useNotification()

// 今日狀態
const todayStatus = ref('今日尚未打卡')
const checkIn = ref('-')
const checkOut = ref('-')

// 看板
const boardMonth = ref(new Date().toISOString().substring(0, 7))
const boardItems = ref([])
const boardLoading = ref(false)

// 地圖
const showMap = ref(false)
const mapLat = ref(0)
const mapLng = ref(0)
const mapTitle = ref('')

function openMap(lat, lng, title) {
  mapLat.value = lat; mapLng.value = lng; mapTitle.value = title
  showMap.value = true
}

async function loadPersonalStatus() {
  try {
    const data = await attendanceApi.getPersonalStatus(auth.employeeName)
    const todayStr = new Date().toLocaleDateString('en-CA')
    if (data.length > 0 && data[0].date === todayStr) {
      const rec = data[0]
      todayStatus.value = rec.status
      checkIn.value = rec.check_in_time ? rec.check_in_time.substring(0, 5) : '-'
      checkOut.value = rec.check_out_time ? rec.check_out_time.substring(0, 5) : '-'
    } else {
      todayStatus.value = '今日尚未打卡'
      checkIn.value = '-'; checkOut.value = '-'
    }
  } catch {}
}

async function loadBoard() {
  if (!auth.isManager) return
  boardLoading.value = true
  try {
    const [year, month] = boardMonth.value.split('-').map(Number)
    const startDate = `${boardMonth.value}-01`
    const lastDay = new Date(year, month, 0).getDate()
    const endDate = `${boardMonth.value}-${String(lastDay).padStart(2, '0')}`
    boardItems.value = await attendanceApi.search(startDate, endDate, auth.username)
  } catch {} finally {
    boardLoading.value = false
  }
}

async function doAction(action) {
  if (!navigator.geolocation) {
    showNotification('無法獲取定位，將以無座標模式打卡', true)
    return sendCheckIn(action, null, null)
  }
  showNotification('正在獲取GPS定位以進行打卡...')
  try {
    const pos = await getPositionWithTimeout(10000)
    await sendCheckIn(action, pos.coords.latitude, pos.coords.longitude)
  } catch {
    showNotification('無法獲取定位，將以無座標模式打卡', true)
    await sendCheckIn(action, null, null)
  }
}

async function sendCheckIn(action, lat, lng) {
  try {
    await attendanceApi.checkIn(auth.employeeName, action, lat, lng)
    showNotification(`成功打卡：${action}`)
    await loadPersonalStatus()
    await loadBoard()
  } catch (err) {
    showNotification(err || '打卡失敗', true)
  }
}

onMounted(() => {
  loadPersonalStatus()
  loadBoard()
})
</script>
