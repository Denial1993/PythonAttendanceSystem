<template>
  <div class="chat-widget">
    <div class="chat-panel" :class="{ open: isOpen }" id="chatPanel">
      <div class="chat-header"><i class="fa-solid fa-robot"></i> 人事助理 (Gemini 3.1)</div>
      <div class="chat-body" ref="chatBody" id="chatBody">
        <div class="chat-msg msg-bot">你好！我是人事助理。請問你想查詢什麼出勤狀況？</div>
        <div v-for="(m, i) in messages" :key="i" class="chat-msg" :class="m.role === 'user' ? 'msg-user' : 'msg-bot'"
             :style="m.error ? { color: '#f87171' } : {}">
          {{ m.text }}
        </div>
      </div>
      <div class="chat-footer">
        <input type="text" v-model="inputText" class="chat-input" id="chatInput"
               placeholder="輸入問題..." autocomplete="off"
               @keyup.enter="send">
        <button class="btn btn-primary" style="width:auto; padding:8px 15px;" @click="send">
          <i class="fa-solid fa-paper-plane"></i>
        </button>
      </div>
    </div>
    <button class="chat-btn" @click="isOpen=!isOpen" id="chatBtn">
      <i class="fa-solid fa-comment-dots" id="chatIcon"></i>
    </button>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { chatApi } from '@/api/chatApi'

const auth = useAuthStore()
const isOpen = ref(false)
const inputText = ref('')
const messages = ref([])
const chatBody = ref(null)

async function scrollDown() {
  await nextTick()
  if (chatBody.value) chatBody.value.scrollTop = chatBody.value.scrollHeight
}

async function send() {
  const text = inputText.value.trim()
  if (!text) return
  messages.value.push({ role: 'user', text })
  inputText.value = ''
  await scrollDown()

  if (!auth.isLoggedIn) {
    messages.value.push({ role: 'bot', text: '請先登入系統才能使用智能助理喔！', error: true })
    await scrollDown()
    return
  }

  try {
    const data = await chatApi.sendMessage(auth.employeeName, text)
    messages.value.push({ role: 'bot', text: data.reply })
  } catch (err) {
    messages.value.push({ role: 'bot', text: `系統提示：${err || '發生未知錯誤'}`, error: true })
  }
  await scrollDown()
}
</script>
