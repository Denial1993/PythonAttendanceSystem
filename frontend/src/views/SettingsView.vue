<template>
  <div class="container">
    <div class="board-container" style="margin-top:0;">
      <div class="board-title"><i class="fa-solid fa-map-location-dot"></i> 公司基準座標設定</div>
      <div style="font-size:0.9rem; line-height:2; margin-top:15px;">
        <div class="input-group">
          <label style="color:#d0d0d0; font-size:0.8rem; display:block; margin-bottom:5px;">緯度 (Latitude)：</label>
          <input type="number" step="any" v-model="lat" id="settingLat" placeholder="例如: 25.0330"
            style="width:100%; padding:8px; border-radius:8px; border:1px solid rgba(255,255,255,0.2); background:rgba(0,0,0,0.3); color:white;">
        </div>
        <div class="input-group">
          <label style="color:#d0d0d0; font-size:0.8rem; display:block; margin-bottom:5px;">經度 (Longitude)：</label>
          <input type="number" step="any" v-model="lng" id="settingLng" placeholder="例如: 121.5654"
            style="width:100%; padding:8px; border-radius:8px; border:1px solid rgba(255,255,255,0.2); background:rgba(0,0,0,0.3); color:white;">
        </div>
        <button class="btn btn-primary" @click="saveSettings">儲存座標設定</button>

        <!-- 地圖預覽 -->
        <div ref="mapEl" id="settingsMap"
             style="height:300px; margin-top:20px; border-radius:12px; border:1px solid rgba(255,255,255,0.1); overflow:hidden;"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import iconUrl from 'leaflet/dist/images/marker-icon.png'
import iconRetinaUrl from 'leaflet/dist/images/marker-icon-2x.png'
import shadowUrl from 'leaflet/dist/images/marker-shadow.png'
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({ iconUrl, iconRetinaUrl, shadowUrl })

import { useAuthStore } from '@/stores/auth'
import { settingsApi } from '@/api/settingsApi'
import { useNotification } from '@/composables/useNotification'

const auth = useAuthStore()
const { showNotification } = useNotification()

const lat = ref('')
const lng = ref('')
const mapEl = ref(null)
let mapInstance = null
let marker = null

function updateMap(la, lo) {
  if (!la || !lo || isNaN(la) || isNaN(lo)) return
  if (!mapInstance && mapEl.value) {
    mapInstance = L.map(mapEl.value).setView([la, lo], 16)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom:19, attribution:'© OpenStreetMap' }).addTo(mapInstance)
  } else if (mapInstance) {
    mapInstance.setView([la, lo], 16)
    mapInstance.invalidateSize()
  }
  if (marker) mapInstance.removeLayer(marker)
  marker = L.marker([la, lo]).addTo(mapInstance).bindPopup('公司基準位置').openPopup()
}

async function loadSettings() {
  try {
    const data = await settingsApi.getSettings(auth.username)
    if (data.base_lat) { lat.value = data.base_lat; lng.value = data.base_lng }
    await nextTick()
    updateMap(parseFloat(lat.value), parseFloat(lng.value))
  } catch {}
}

async function saveSettings() {
  try {
    await settingsApi.saveSettings({ base_lat: parseFloat(lat.value), base_lng: parseFloat(lng.value) }, auth.username)
    showNotification('座標設定已儲存！')
    updateMap(parseFloat(lat.value), parseFloat(lng.value))
  } catch (err) { showNotification(err || '儲存失敗', true) }
}

onMounted(loadSettings)
onUnmounted(() => { if (mapInstance) { mapInstance.remove(); mapInstance = null } })
</script>
