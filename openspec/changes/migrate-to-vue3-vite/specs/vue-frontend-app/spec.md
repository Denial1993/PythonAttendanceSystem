## ADDED Requirements

### Requirement: Vite 專案初始化
系統 SHALL 在專案根目錄建立 `frontend/` 作為獨立的 Vite + Vue 3 前端專案，包含 `package.json`、`vite.config.js`、`src/` 等標準結構。

#### Scenario: 開發模式啟動
- **WHEN** 開發者執行 `npm run dev` 於 `frontend/` 目錄
- **THEN** Vite 開發伺服器啟動於 `localhost:5173`，且 `/api` 請求透過 proxy 轉發至 `localhost:8000`

#### Scenario: 生產建置
- **WHEN** 執行 `npm run build`
- **THEN** 建置產出至 `frontend/dist/`，包含 `index.html` 與壓縮後的 JS/CSS 資源

---

### Requirement: Vue Router 路由管理
系統 SHALL 使用 Vue Router 4 以 Hash 模式管理所有頁面路由，並於未登入時自動導向登入頁。

#### Scenario: 未登入訪問受保護路由
- **WHEN** 使用者直接訪問 `#/home` 且 localStorage 中無 `employee_name`
- **THEN** Vue Router navigation guard 自動導向 `#/` 登入頁

#### Scenario: 登入後路由跳轉
- **WHEN** 登入成功
- **THEN** 自動導向 `#/home`

#### Scenario: 角色限制路由
- **WHEN** 一般員工（role=3）嘗試訪問 `#/staff` 或 `#/settings`
- **THEN** 自動導向 `#/home`

---

### Requirement: Pinia 全域狀態管理
系統 SHALL 使用 Pinia 管理登入狀態，包含 `employeeName`、`username`、`role`、`isLoggedIn`。

#### Scenario: 登入後狀態持久化
- **WHEN** 登入成功後重新整理頁面
- **THEN** Pinia store 從 localStorage 恢復使用者資訊，維持登入狀態

#### Scenario: 登出清除狀態
- **WHEN** 使用者點擊登出
- **THEN** Pinia store 清除所有狀態，localStorage 清除，導向登入頁

---

### Requirement: AuthView 登入與註冊元件
系統 SHALL 提供登入與註冊表單，功能完全對應現有 `performLogin` 與 `performRegister`。

#### Scenario: 登入成功
- **WHEN** 使用者輸入正確帳號密碼並送出
- **THEN** 呼叫 `POST /api/auth/login`，儲存 `employee_name`、`username`、`role` 至 Pinia store 與 localStorage，並導向 `#/home`

#### Scenario: 登入失敗
- **WHEN** 帳號或密碼錯誤
- **THEN** 顯示通知 toast 提示錯誤訊息

#### Scenario: 註冊成功
- **WHEN** 填寫完整資料後送出
- **THEN** 呼叫 `POST /api/auth/register`，成功後切換至登入 tab

---

### Requirement: HomeView 打卡與出勤看板元件
系統 SHALL 提供打卡按鈕（上班/吃午餐/午餐回來/下班）與個人今日狀態顯示，管理員/主管可見大家出勤看板。

#### Scenario: GPS 打卡成功
- **WHEN** 使用者點擊打卡按鈕且 GPS 定位成功
- **THEN** 呼叫 `POST /api/attendance/` 帶入座標，顯示成功通知並刷新狀態

#### Scenario: GPS 失敗降級打卡
- **WHEN** GPS 定位逾時或被拒絕
- **THEN** 顯示警告通知，仍以無座標方式呼叫打卡 API

#### Scenario: 出勤看板按月份篩選
- **WHEN** 管理員/主管更改月份選擇器
- **THEN** 呼叫 `GET /api/attendance/search` 並刷新出勤清單

---

### Requirement: LeaveView 請假系統元件
系統 SHALL 提供假單申請表單、個人假單清單、管理員待審核清單。

#### Scenario: 送出請假申請
- **WHEN** 填寫假別、時間與事由後點擊送出
- **THEN** 呼叫 `POST /api/leave`，成功後刷新「我的假單」清單

#### Scenario: 管理員核准/駁回
- **WHEN** 管理員/主管點擊核准或駁回按鈕
- **THEN** 呼叫對應的 `PUT /api/leave/{id}` API，刷新待審核清單

#### Scenario: 假勤額度顯示
- **WHEN** 進入請假頁面
- **THEN** 呼叫 `GET /api/leave/balance` 並顯示各假別剩餘額度

---

### Requirement: StatsView 統計與個人資料元件
系統 SHALL 顯示月份統計（出勤天數、遲到次數、每日明細）與個人資料（可編輯）。

#### Scenario: 月份統計載入
- **WHEN** 使用者切換至統計頁或更改月份
- **THEN** 呼叫 `GET /api/attendance/summary` 並更新統計卡片與每日明細列表

#### Scenario: 個人資料編輯儲存
- **WHEN** 使用者修改電話/地址後點擊儲存
- **THEN** 呼叫 `PUT /api/users/me`，成功後顯示通知並切回檢視模式

---

### Requirement: AppNavbar 側邊欄導覽元件
系統 SHALL 提供固定側邊欄，根據使用者角色動態顯示或隱藏導覽項目。

#### Scenario: 一般員工導覽項目
- **WHEN** role=3 的使用者登入
- **THEN** 側邊欄不顯示「員工名冊」與「系統設定」連結

#### Scenario: 管理員導覽項目
- **WHEN** role=1 的使用者登入
- **THEN** 側邊欄顯示所有導覽連結包含「系統設定」

---

### Requirement: ChatWidget AI 聊天浮動元件
系統 SHALL 提供右下角浮動的 AI 聊天視窗，功能對應現有 `sendChatMessage`。

#### Scenario: 傳送訊息
- **WHEN** 使用者輸入文字並按 Enter 或送出按鈕
- **THEN** 呼叫 `POST /api/chat`，回傳的 reply 顯示於聊天視窗中

---

### Requirement: MapModal 地圖 Modal 元件
系統 SHALL 提供可重用的 Leaflet 地圖 Modal，於 `onMounted` 後初始化地圖，`onUnmounted` 時銷毀。

#### Scenario: 地圖正確初始化
- **WHEN** Modal 開啟並傳入有效的 lat/lng
- **THEN** Leaflet 地圖於 `nextTick` 後初始化，顯示對應位置的 marker

#### Scenario: 地圖 Modal 關閉銷毀
- **WHEN** 使用者關閉 Modal
- **THEN** Leaflet map instance 呼叫 `.remove()` 釋放資源，避免重複初始化錯誤

---

### Requirement: SettingsView 系統設定元件
系統 SHALL 提供公司基準座標設定表單與地圖預覽，僅 role=1 可存取。

#### Scenario: 載入現有設定
- **WHEN** 管理員進入設定頁
- **THEN** 呼叫 `GET /api/settings` 並填入緯度/經度輸入框，同時更新地圖 marker

#### Scenario: 儲存設定
- **WHEN** 管理員輸入座標後點擊儲存
- **THEN** 呼叫 `PUT /api/settings`，成功後顯示通知並更新地圖

---

### Requirement: StaffView 員工名冊元件
系統 SHALL 提供員工名冊表格，僅 role=1/2 可存取。

#### Scenario: 載入員工清單
- **WHEN** 管理員/主管進入員工名冊頁
- **THEN** 呼叫 `GET /api/users/` 並渲染員工表格（姓名、電話、角色）

---

### Requirement: SearchView 歷史紀錄查詢元件
系統 SHALL 提供日期範圍查詢，管理員/主管可指定查詢目標員工。

#### Scenario: 查詢歷史紀錄
- **WHEN** 使用者設定日期範圍後點擊查詢
- **THEN** 呼叫 `GET /api/attendance/search` 並顯示結果列表

#### Scenario: 管理員指定員工查詢
- **WHEN** role=1/2 的使用者填入目標員工帳號
- **THEN** API 查詢包含 `username` 參數，回傳該員工資料

---

### Requirement: 通知 Toast 系統
系統 SHALL 提供全域通知 toast，對應現有 `showNotification` 功能。

#### Scenario: 成功通知顯示
- **WHEN** 操作成功
- **THEN** 右上角顯示綠色通知 toast，3 秒後自動消失

#### Scenario: 錯誤通知顯示
- **WHEN** 操作失敗
- **THEN** 右上角顯示紅色通知 toast，3 秒後自動消失

---

### Requirement: FastAPI 靜態資源整合
後端 SHALL 新增 CORS middleware 支援開發期跨域請求，並提供 catch-all route 回傳 `frontend/dist/index.html`。

#### Scenario: 開發期 CORS
- **WHEN** Vite dev server（localhost:5173）發送 API 請求至 FastAPI（localhost:8000）
- **THEN** FastAPI 回傳正確的 CORS headers，請求不被瀏覽器封鎖

#### Scenario: 生產期 SPA 路由
- **WHEN** 使用者直接訪問 `https://domain.com/` 或重新整理 SPA 頁面
- **THEN** FastAPI catch-all route 回傳 `dist/index.html`，由 Vue Router 處理路由
