<template>
  <Teleport to="body">
    <div class="notification" :class="{ show: visible }"
         :style="{ borderLeft: isError ? '4px solid #f87171' : '4px solid #4ade80' }">
      {{ message }}
    </div>
  </Teleport>
</template>

<script setup>
import { useNotification } from '@/composables/useNotification'
const { message, isError, visible } = useNotification()
</script>
