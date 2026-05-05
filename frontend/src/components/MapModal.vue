<template>
  <Teleport to="body">
    <div v-if="modelValue" class="map-modal-overlay" @click.self="$emit('update:modelValue', false)">
      <div class="map-modal-content">
        <div class="map-modal-header">
          <strong>{{ title }}</strong>
          <button class="map-modal-close" @click="$emit('update:modelValue', false)">
            <i class="fa-solid fa-xmark"></i>
          </button>
        </div>
        <div ref="mapEl" class="leaflet-map-container"></div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, watch, nextTick, onUnmounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Fix leaflet default icon
import iconUrl from 'leaflet/dist/images/marker-icon.png'
import iconRetinaUrl from 'leaflet/dist/images/marker-icon-2x.png'
import shadowUrl from 'leaflet/dist/images/marker-shadow.png'
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({ iconUrl, iconRetinaUrl, shadowUrl })

const props = defineProps({
  modelValue: Boolean,
  lat: Number,
  lng: Number,
  title: { type: String, default: '打卡位置' }
})
defineEmits(['update:modelValue'])

const mapEl = ref(null)
let mapInstance = null
let marker = null

watch(() => props.modelValue, async (val) => {
  if (val) {
    await nextTick()
    if (!mapInstance && mapEl.value) {
      mapInstance = L.map(mapEl.value).setView([props.lat, props.lng], 16)
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap'
      }).addTo(mapInstance)
    } else if (mapInstance) {
      mapInstance.setView([props.lat, props.lng], 16)
      mapInstance.invalidateSize()
    }
    if (marker) mapInstance.removeLayer(marker)
    marker = L.marker([props.lat, props.lng]).addTo(mapInstance)
      .bindPopup(props.title).openPopup()
  }
})

onUnmounted(() => {
  if (mapInstance) { mapInstance.remove(); mapInstance = null }
})
</script>
