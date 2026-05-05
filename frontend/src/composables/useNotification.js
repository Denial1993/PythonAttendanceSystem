import { ref } from 'vue'

const message = ref('')
const isError = ref(false)
const visible = ref(false)
let timer = null

export function useNotification() {
  function showNotification(msg, error = false) {
    message.value = msg
    isError.value = error
    visible.value = true
    clearTimeout(timer)
    timer = setTimeout(() => { visible.value = false }, 3000)
  }

  return { message, isError, visible, showNotification }
}
