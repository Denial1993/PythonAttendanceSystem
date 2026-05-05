## 1. 專案初始化與基礎建設

- [x] 1.1 在專案根目錄執行 `npm create vite@latest frontend -- --template vue`，初始化 Vite + Vue 3 專案
- [x] 1.2 安裝前端依賴：`npm install vue-router@4 pinia axios leaflet`
- [x] 1.3 建立 `frontend/vite.config.js`，設定開發 proxy 將 `/api` 轉發至 `http://localhost:8000`
- [x] 1.4 建立目錄結構：`src/api/`、`src/stores/`、`src/views/`、`src/components/`、`src/composables/`、`src/router/`
- [x] 1.5 將現有 `base.html` 的 CSS 樣式（深色主題、glassmorphism）移植至 `src/assets/main.css`

## 2. HTTP 層 - axios 封裝

- [x] 2.1 建立 `src/api/http.js`：axios instance，設定 `baseURL: '/api'`，`Content-Type: application/json`
- [x] 2.2 實作 Request Interceptor：自動從 localStorage 讀取 `username` 並附加至需要的 API 請求
- [x] 2.3 實作 Response Interceptor：成功時解包 `response.data`，401 自動登出，錯誤時提取 `detail` 字串 reject
- [x] 2.4 建立 `src/api/authApi.js`：封裝 `login`、`register` 函式
- [x] 2.5 建立 `src/api/attendanceApi.js`：封裝 `checkIn`、`getPersonalStatus`、`search`、`getSummary` 函式
- [x] 2.6 建立 `src/api/leaveApi.js`：封裝 `getBalance`、`getMyLeaves`、`getPending`、`submitLeave`、`approve`、`reject` 函式
- [x] 2.7 建立 `src/api/usersApi.js`：封裝 `getMe`、`updateMe`、`getAllUsers` 函式
- [x] 2.8 建立 `src/api/settingsApi.js`：封裝 `getSettings`、`saveSettings` 函式
- [x] 2.9 建立 `src/api/chatApi.js`：封裝 `sendMessage` 函式

## 3. 全域狀態與路由

- [x] 3.1 建立 `src/stores/auth.js`（Pinia）：state 包含 `employeeName`、`username`、`role`、`isLoggedIn`；actions 包含 `login`、`logout`，從 localStorage 初始化
- [x] 3.2 建立 `src/router/index.js`（Hash 模式）：定義所有路由 `/`、`/home`、`/search`、`/leave`、`/stats`、`/staff`、`/settings`
- [x] 3.3 實作 Navigation Guard：未登入導向 `/`；role=3 訪問 `/staff`、`/settings` 導向 `/home`
- [x] 3.4 在 `src/main.js` 中掛載 Pinia、Vue Router，引入全域 CSS

## 4. 共用 Composables 與元件

- [x] 4.1 建立 `src/composables/useNotification.js`：管理 toast 通知狀態（message、isError、visible），提供 `showNotification` 函式
- [x] 4.2 建立 `src/composables/useGeolocation.js`：封裝 `getPositionWithTimeout`，對應現有邏輯（10s timeout）
- [x] 4.3 建立 `src/components/AppNavbar.vue`：固定側邊欄，根據 Pinia role 動態顯示連結，包含登出按鈕
- [x] 4.4 建立 `src/components/NotificationToast.vue`：全域通知 Toast 元件，支援成功/錯誤顏色
- [x] 4.5 建立 `src/components/MapModal.vue`：Leaflet 地圖 Modal，`onMounted` 後初始化，`onUnmounted` 時 `map.remove()`，接收 `lat`、`lng`、`title` props

## 5. 頁面 View 元件實作

- [x] 5.1 建立 `src/views/AuthView.vue`：登入/註冊 tab 切換，呼叫 `authApi`，成功後更新 Pinia store 並導向 `/home`
- [x] 5.2 建立 `src/views/HomeView.vue`：打卡按鈕（上班/吃午餐/午餐回來/下班）+ 今日狀態卡片 + 大家出勤看板（管理員/主管可見）
- [x] 5.3 建立 `src/views/SearchView.vue`：日期範圍查詢表單 + 結果列表，管理員可輸入目標員工帳號
- [x] 5.4 建立 `src/views/LeaveView.vue`：假勤額度顯示 + 申請表單 + 我的假單清單 + 待審核清單（管理員/主管）
- [x] 5.5 建立 `src/views/StatsView.vue`：個人資料卡（可編輯）+ 月份統計（出勤天數、遲到次數）+ 每日明細列表
- [x] 5.6 建立 `src/views/StaffView.vue`：員工名冊表格（姓名、電話、角色），呼叫 `usersApi.getAllUsers`
- [x] 5.7 建立 `src/views/SettingsView.vue`：座標輸入表單 + 地圖預覽（嵌入 Leaflet），僅 role=1 可見

## 6. AI 聊天元件

- [x] 6.1 建立 `src/components/ChatWidget.vue`：右下角浮動聊天按鈕 + 聊天面板，Enter 鍵或按鈕送出，呼叫 `chatApi.sendMessage`

## 7. App 根元件整合

- [x] 7.1 更新 `src/App.vue`：包含 `AppNavbar`、`RouterView`、`NotificationToast`、`ChatWidget`（已登入時顯示），並整合全域通知邏輯

## 8. 後端整合

- [x] 8.1 在 `attendance_system/app/main.py` 新增 `CORSMiddleware`，允許 `localhost:5173` 開發期跨域
- [x] 8.2 在 `main.py` 新增 `StaticFiles` 掛載：`app.mount("/", StaticFiles(directory="static/dist", html=True))`
- [x] 8.3 確認 FastAPI 的所有 API 路由前綴為 `/api`，與 axios baseURL 對應

## 9. Docker 部署整合

- [x] 9.1 更新 `Dockerfile` 為多階段建置：Stage 1 用 `node:20-alpine` 建置前端 `dist/`；Stage 2 複製 `dist/` 至 FastAPI 靜態目錄
- [x] 9.2 更新 `docker-compose.yml`：確認 build context 涵蓋 `frontend/` 目錄
- [ ] 9.3 本機執行 `docker-compose up --build` 驗證多階段建置正常

## 10. 功能驗證與清理

- [ ] 10.1 本機開發模式：啟動 FastAPI（port 8000）+ Vite dev server（port 5173），逐一測試所有功能
- [ ] 10.2 驗證清單：登入/登出、打卡四種動作（GPS 與無 GPS）、請假申請與審核、月份統計、員工名冊、系統設定地圖
- [ ] 10.3 驗證 role 權限控制：role=3 無法看到員工名冊、系統設定、薪資欄位
- [ ] 10.4 驗證 Leaflet 地圖：打卡位置 Modal 開關正常，設定頁地圖 marker 正確
- [ ] 10.5 確認所有 `fetch` 呼叫已移除，全部改為 axios
- [ ] 10.6 （選做）移除舊 `main.js` 與 Jinja2 模板（`base.html`、`index.html`、`navbar.html`）
