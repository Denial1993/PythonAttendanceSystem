## 1. 資料庫建置與更新 (Database)

- [x] 1.1 在 `models.py` 的 `Attendance` 類別新增 `check_in_lat`, `check_in_lng`, `check_out_lat`, `check_out_lng` 四個 Float 欄位。
- [x] 1.2 在 `models.py` 中建立新的 `SystemSettings` 類別，用來儲存環境設定（包含 `company_base_lat` 和 `company_base_lng`）。
- [x] 1.3 套用資料庫變更（使用 Alembic 或直接重建/更新表格）。

## 2. 後端 API 功能開發 (Backend)

- [x] 2.1 修改 `routers/attendance.py` 的 `check_in_or_update` 路由，接受前端傳入的 `lat` 與 `lng` 參數，並依據動作寫入對應的資料庫欄位。
- [x] 2.2 在後端新增一個 `/settings` 相關路由模組（或直接寫在 users/auth 裡），實作「取得」與「更新」公司基準座標的 API (限 Role 1)。
- [x] 2.3 修改 `routers/attendance.py` 或前端邏輯，讓拉取「出勤狀態」列表 API 的返回結果中，包含經緯度資訊。

## 3. 前端打卡地理位置追蹤 (Frontend - Tracking)

- [x] 3.1 於 `static/main.js` (或原腳本) 的 `performAction` 方法內，整合 `navigator.geolocation.getCurrentPosition`。
- [x] 3.2 在呼叫後端 API 時，將取得的 `lat` 與 `lng` 夾帶為參數。
- [x] 3.3 若定位失敗或使用者拒絕權限，顯示對應的錯誤提示或決定是否允許無線上打卡（阻擋並提示錯誤）。

## 4. 前端管理員地圖檢視器 (Frontend - Map Viewer)

- [x] 4.1 於 `base.html` 引入 Leaflet.js 的 CDN (CSS & JS)，並在適當位置建立地圖 Modal (預設隱藏)。
- [x] 4.2 於 `main.js` 或對應的腳本中，新增地圖渲染邏輯，當 Admin 點擊出勤列表上的座標按鈕時，展開 Modal 並顯示該地點。
- [x] 4.3 在後台出勤清單渲染邏輯中，針對有經緯度資料的記錄，新增「顯示地圖」的按鈕，點擊後觸發 Modal。

## 5. 前端基準點設定介面 (Frontend - Settings UI)

- [x] 5.1 在畫面上新增一個專屬區塊或 Modal 供管理員 (Role 1) 設定/更新公司基準經緯度。
- [x] 5.2 實作對應的 JS 邏輯送出新座標至 `/settings` API。
