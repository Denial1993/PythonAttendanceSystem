## ADDED Requirements

### Requirement: axios instance 建立與基礎配置
系統 SHALL 建立單一 axios instance，設定 `baseURL: '/api'`，所有 API 模組統一使用此 instance，禁止直接使用 `fetch` 或裸 `axios`。

#### Scenario: 基礎 URL 自動前綴
- **WHEN** 任意 Vue 元件呼叫 `http.get('/attendance/...')`
- **THEN** 實際請求發送至 `/api/attendance/...`

#### Scenario: 禁用裸 fetch
- **WHEN** 程式碼中存在 `fetch(` 的使用
- **THEN** 應視為技術債，須替換為 axios instance 呼叫

---

### Requirement: Request Interceptor - 自動附加 username
系統 SHALL 於每次 HTTP 請求前，從 localStorage 讀取 `username` 並附加至請求，無需在每個呼叫點手動帶入。

#### Scenario: 自動附加 username
- **WHEN** 已登入使用者發送任何 API 請求
- **THEN** 請求中包含當前使用者的 `username`

#### Scenario: 未登入時不附加
- **WHEN** localStorage 中無 `username`
- **THEN** 請求正常發送，不帶 username（僅限 login/register API）

---

### Requirement: Response Interceptor - 成功解包
系統 SHALL 於 Response Interceptor 中回傳 `response.data`，使呼叫方直接拿到 API 回傳的 JSON 物件。

#### Scenario: 呼叫方直接取得 data
- **WHEN** 元件執行 `const data = await http.get('/users/me?username=...')`
- **THEN** `data` 直接為後端 JSON 物件，不需額外 `.data` 解包

---

### Requirement: Response Interceptor - 錯誤處理
系統 SHALL 於 Response Interceptor 統一處理 HTTP 錯誤：401 自動觸發登出；其他錯誤將後端 `detail` 欄位 reject，讓呼叫方 `catch` 可直接取得錯誤訊息。

#### Scenario: 401 自動登出
- **WHEN** API 回傳 401 Unauthorized
- **THEN** Pinia auth store 執行 `logout()`，清除 localStorage 並導向登入頁

#### Scenario: 一般錯誤訊息提取
- **WHEN** API 回傳 4xx/5xx 且 body 包含 `{ detail: "錯誤訊息" }`
- **THEN** `catch(err)` 中 `err` 為可讀字串，元件直接傳入通知顯示

#### Scenario: 網路錯誤處理
- **WHEN** 發生網路連線失敗
- **THEN** `catch(err)` 包含可讀錯誤訊息

---

### Requirement: API 模組化組織
系統 SHALL 將 API 呼叫按功能分組封裝於 `src/api/` 下的獨立模組，元件透過引入模組函式呼叫 API。

#### Scenario: attendance API 模組
- **WHEN** HomeView 需要打卡
- **THEN** 呼叫 `attendanceApi.checkIn(action, lat, lng)` 而非直接操作 http instance

#### Scenario: 模組清晰分離
- **WHEN** 後端 API 路徑變更
- **THEN** 只需修改對應的 API 模組檔案

---

### Requirement: 統一 Content-Type
系統 SHALL 確保所有 POST/PUT 請求的 `Content-Type` 預設為 `application/json`。

#### Scenario: POST 請求自動 JSON 序列化
- **WHEN** 執行 `http.post('/auth/login', { username, password })`
- **THEN** 請求 body 為 JSON 字串，`Content-Type: application/json` 已自動設定
