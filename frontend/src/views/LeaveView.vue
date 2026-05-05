<template>
  <div class="container">
    <!-- 假勤額度 -->
    <div class="board-container" style="margin-top:0;">
      <div class="board-title"><i class="fa-solid fa-wallet"></i> 我的假勤可用額度</div>
      <div id="leaveBalancesBlock" style="font-size:0.9rem; padding:10px; color:#d0d0d0;">
        <div v-if="balanceLoading"><i class="fa-solid fa-spinner fa-spin"></i> 載入中...</div>
        <div v-else-if="balances.length === 0" style="color:#a0a0b0;">無假勤資料</div>
        <div v-else v-for="b in balances" :key="b.leave_type" style="margin-bottom:6px;">
          <b>{{ b.leave_type }}</b>：剩餘 {{ b.remaining }} 小時（已用 {{ b.used }} / {{ b.total }}）
        </div>
      </div>
    </div>

    <!-- 申請假單 -->
    <div class="board-container">
      <div class="board-title"><i class="fa-solid fa-pen-to-square"></i> 填寫假單</div>
      <div class="input-group">
        <select v-model="leaveType" id="leaveType">
          <option value="事假">事假</option>
          <option value="病假">病假</option>
          <option value="特休">特休</option>
        </select>
      </div>
      <div style="display:flex; gap:10px;">
        <input type="datetime-local" v-model="leaveStart" class="input-group" id="leaveStart" style="flex:1;">
        <input type="datetime-local" v-model="leaveEnd"   class="input-group" id="leaveEnd"   style="flex:1;">
      </div>
      <input type="text" v-model="leaveReason" placeholder="事由(選填)" class="input-group">
      <button id="btnSubmitLeave" class="btn btn-primary" @click="submitLeave">送出申請</button>
    </div>

    <!-- 我的假單 -->
    <div class="board-container">
      <div class="board-title"><i class="fa-solid fa-list"></i> 我的假單紀錄</div>
      <div id="myLeaveList">
        <div v-if="myLeavesLoading" style="color:#a0a0b0;"><i class="fa-solid fa-spinner fa-spin"></i></div>
        <div v-else-if="myLeaves.length === 0" style="color:#a0a0b0; padding:10px;">目前沒有任何假單紀錄。</div>
        <div v-for="leave in myLeaves" :key="leave.id"
             class="board-item" style="border-left:4px solid; margin-bottom:10px; flex-direction:column; align-items:flex-start;"
             :style="{ borderColor: statusColor(leave.status) }">
          <div style="display:flex; justify-content:space-between; width:100%;">
            <b>{{ leave.leave_type }}</b>
            <span :style="{ color: statusColor(leave.status), fontWeight:'bold' }">{{ statusText(leave.status) }}</span>
          </div>
          <div style="font-size:0.85rem; color:#d0d0d0; margin:5px 0;">
            {{ leave.start_time?.replace('T',' ') }} ~ {{ leave.end_time?.replace('T',' ') }}
          </div>
          <div style="font-size:0.85rem; color:#a0a0b0;">理由：{{ leave.reason || '無' }}</div>
        </div>
      </div>
    </div>

    <!-- 待審核（管理員/主管） -->
    <div v-if="auth.isManager" class="board-container" id="leaveApprovalBlock">
      <div class="board-title"><i class="fa-solid fa-clipboard-check"></i> 待審核清單</div>
      <div id="approvalLeaveListBlock">
        <div v-if="pendingLoading" style="color:#a0a0b0;"><i class="fa-solid fa-spinner fa-spin"></i></div>
        <div v-else-if="pendingLeaves.length === 0" style="color:#a0a0b0;">目前沒有待處理的假單。</div>
        <div v-for="leave in pendingLeaves" :key="leave.id" class="board-item"
             style="flex-direction:column; align-items:flex-start; gap:8px; margin-bottom:10px;">
          <div style="display:flex; justify-content:space-between; width:100%;">
            <b>{{ leave.employee_name }}</b>
            <span style="color:#fb923c; font-size:0.85rem;">{{ leave.leave_type }}</span>
          </div>
          <div style="font-size:0.85rem; color:#d0d0d0;">
            {{ leave.start_time?.replace('T',' ') }} ~ {{ leave.end_time?.replace('T',' ') }}
          </div>
          <div style="font-size:0.85rem; color:#a0a0b0;">理由：{{ leave.reason || '無' }}</div>
          <div style="display:flex; gap:10px;">
            <button class="btn btn-primary" style="padding:6px 16px; width:auto; font-size:0.85rem;"
                    @click="handleApprove(leave.id)">核准</button>
            <button class="btn" style="padding:6px 16px; width:auto; font-size:0.85rem; color:#f87171; border-color:rgba(248,113,113,0.3);"
                    @click="handleReject(leave.id)">駁回</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { leaveApi } from '@/api/leaveApi'
import { useNotification } from '@/composables/useNotification'

const auth = useAuthStore()
const { showNotification } = useNotification()

const balances = ref([])
const balanceLoading = ref(false)
const myLeaves = ref([])
const myLeavesLoading = ref(false)
const pendingLeaves = ref([])
const pendingLoading = ref(false)

const leaveType = ref('事假')
const leaveStart = ref('')
const leaveEnd = ref('')
const leaveReason = ref('')

function statusColor(s) {
  if (s === 'approved') return '#4ade80'
  if (s === 'rejected') return '#f87171'
  return '#fb923c'
}
function statusText(s) {
  if (s === 'approved') return '已核准'
  if (s === 'rejected') return '已駁回'
  return '待審核'
}

async function loadBalances() {
  balanceLoading.value = true
  try { balances.value = await leaveApi.getBalance(auth.username) } catch {} finally { balanceLoading.value = false }
}

async function loadMyLeaves() {
  myLeavesLoading.value = true
  try { myLeaves.value = await leaveApi.getMyLeaves(auth.username) } catch {} finally { myLeavesLoading.value = false }
}

async function loadPending() {
  if (!auth.isManager) return
  pendingLoading.value = true
  try { pendingLeaves.value = await leaveApi.getPending(auth.username) } catch {} finally { pendingLoading.value = false }
}

async function submitLeave() {
  if (!leaveStart.value || !leaveEnd.value) {
    showNotification('請填寫請假時間', true); return
  }
  try {
    await leaveApi.submitLeave({
      username: auth.username,
      leave_type: leaveType.value,
      start_time: leaveStart.value,
      end_time: leaveEnd.value,
      reason: leaveReason.value
    })
    showNotification('假單已送出！')
    leaveStart.value = ''; leaveEnd.value = ''; leaveReason.value = ''
    loadMyLeaves()
  } catch (err) { showNotification(err || '送出失敗', true) }
}

async function handleApprove(id) {
  try {
    await leaveApi.approve(id, auth.username)
    showNotification('已核准！')
    loadPending()
  } catch (err) { showNotification(err || '操作失敗', true) }
}

async function handleReject(id) {
  try {
    await leaveApi.reject(id, auth.username)
    showNotification('已駁回')
    loadPending()
  } catch (err) { showNotification(err || '操作失敗', true) }
}

onMounted(() => {
  loadBalances(); loadMyLeaves(); loadPending()
})
</script>
