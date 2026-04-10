## Why

目前打卡系統缺乏地理位置驗證機制，無法確認員工打卡時的真實位置。為了防範遠端假打卡，並讓管理員能精確掌握同仁打卡的地理資訊，我們計劃導入地圖系統（OpenStreetMap + Leaflet.js）。這不僅能提升差勤管理的嚴謹度，日後也能作為外勤人員軌跡追蹤的基礎。

## What Changes

- 在前端打卡時透過瀏覽器 Geolocation API 獲取員工當下座標 (lat, lng)。
- 更新 `Attendance` 資料表，新增 `check_in_lat` / `check_in_lng` (甚至其他打卡動作的座標) 等欄位儲存地理資訊。
- 在後台「今日大家的出勤狀況」或其他人員清單中，供最高權限管理員看到「地圖連結 (URL)」。
- 開發一個地圖檢視畫面 (或 Modal)，管理員點擊連結後，可用 UI 在地圖上查看該員工當時的打卡地點。
- 新增最高權限專屬的環境變數或資料庫設定介面，供管理員隨時變更公司的「基準經緯度」，作為日後位置驗證的判定中心。

## Capabilities

### New Capabilities
- `geo-location-tracking`: 員工打卡時獲取與儲存經緯度的能力。
- `admin-map-viewer`: 管理員使用地圖 UI (Leaflet.js) 查看員工打卡位置的能力。
- `company-location-settings`: 供最高權限管理員設定並隨時更新公司基準位置介面的能力。

### Modified Capabilities
- `attendance-recording`: 擴充原有的打卡功能，將端點與資料模型增加經緯度參數。

## Impact

- **Database**: `Attendance` table 需新增欄位，儲存各種打卡動作的經緯度。可能需建立一個新的 `SystemSettings` table 儲存公司設定座標。
- **Frontend / Templates**: 
  - `footer.html`/`index.html` 將需要載入 Leaflet.js 與 OpenStreetMap 的 CDN 資源。
  - 需要取得地理權限的 JS 邏輯處理與失敗處理 (例如未給予位置權限不給打卡)。
  - 管理員專用 UI 的調整 (地圖連結的顯示、Modal 顯示)。
- **Backend API**: 
  - `/attendance` route 需修改參數接受座標。
  - 需新增供管理員設定公司基準地點的 API endpoints。
