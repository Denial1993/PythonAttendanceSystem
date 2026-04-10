## Context

目前的打卡系統在處理使用者打卡時，僅記錄打卡當下的系統時間，並沒有驗證或記錄使用者的真實地理位置。為了防範遠端假打卡，並讓管理員掌握員工出勤時的確切位置，我們將導入基於 OpenStreetMap 與 Leaflet.js 的地圖檢視系統。此功能要求打卡時利用瀏覽器的 Geolocation API 獲取座標，並將座標儲存至後端資料庫，最後在後台介面提供管理員視覺化的地圖檢視。
此外，系統還需要有一個「公司基準位置」的動態設定功能，供最高權限管理員自行定義基準點的經緯度。

## Goals / Non-Goals

**Goals:**
- 在前台打卡時，自動獲取並強制送出使用者的 GPS 經緯度座標。
- 修改 `Attendance` 資料表結構，增加儲存座標的欄位。
- 建立 `SystemSettings` (或類似機制) 以儲存與更新「公司基準位置」的經緯度。
- 最高權限角色 (Role 1) 登入後，能在出勤明細中看到地圖 URL/按鈕。
- 點擊地圖連結後，透過 Leaflet.js + OpenStreetMap 顯示打卡的具體位置與公司基準點的相對位置。

**Non-Goals:**
- 不強制綁定特定的原生 App (純基於 Web Geolocation API)。
- 不包含背景持續追蹤功能（僅在按下打卡按鈕的當下獲取座標）。
- 不限制或阻擋距離公司過遠的打卡（目前僅為記錄與顯示，未來如果需要 geo-fencing 再擴充）。

## Decisions

1. **地理資訊獲取方式**：
   使用 HTML5 `navigator.geolocation.getCurrentPosition`。
   *Rationale*: 原生支援，無需載入額外 SDK。若使用者拒絕地理權限，則前端應提示無法打卡。

2. **資料庫 Schema 擴充 (PostgreSQL)**：
   在 `Attendance` 表格中新增欄位：
   - 因為同一筆記錄 (同一個 ID) 包含一天內的多次打卡 (上班、吃午餐、下班)，為了精確，我們新增：`check_in_lat` (Float), `check_in_lng` (Float), `check_out_lat` (Float), `check_out_lng` (Float)。
   *Rationale*: 這樣可以確保上下班的位置都能被獨立記錄。若覺得太多，也可以考慮使用 JSON 格式儲存 `location_data`，但關聯式資料庫中直接增加欄位較好查詢。
   
   建立 `SystemSettings` 表單：
   - 增加一個簡單的 Key-Value 表，例如：設定鍵為 `company_base_lat`與 `company_base_lng`。
   *Rationale*: 保留彈性，未來還可儲存其他全域設定（如：允許的打卡誤差半徑等）。

3. **前端地圖庫選型**：
   使用 Leaflet.js 配合 OpenStreetMap 圖資。
   *Rationale*: 開源、免費、沒有 API Key 的額度限制，且輕量易用。不需要複雜的 npm 構建，可直接使用 CDN 載入。

4. **UI 互動設計**：
   在「今日大家的出勤狀況」或其他人員清單中加入連結。為了 UX 考量，可以設計為「開啟地圖 Modal (彈出視窗)」，在地圖中繪製兩個 Marker：一個是員工打卡點，一個是公司基準點。

## Risks / Trade-offs

- **[位置精確度不佳]** → Web Geolocation API 在桌機或無 GPS 晶片的設備上，可能是透過 IP 定位，精確度極低。
  *Mitigation*: 在介面上提示使用者「建議使用手機進行打卡以取得精確位置」。
- **[使用者拒絕授權定位]** →
  *Mitigation*: 打卡操作必須依賴成功獲取定位。若前端獲取失敗，直接阻擋打卡請求，並跳出提示請使用者開啟定位。
- **[Leaflet 地圖在 Modal 內渲染異常]** → Leaflet 在初始容器隱藏(display:none)的情境下，渲染時常會遇到尺寸計算錯誤（灰畫面）。
  *Mitigation*: 在 Modal 開啟後呼叫 `map.invalidateSize()`，確保地圖正確刷新。
