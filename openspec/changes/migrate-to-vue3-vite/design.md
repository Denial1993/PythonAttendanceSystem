## Context

目前打卡系統前端為單檔架構：`attendance_system/app/static/main.js`（1030 行）+ Jinja2 HTML 模板（`base.html` 22KB、`index.html` 13KB）。所有 API 呼叫使用原生 `fetch`，缺乏統一攔截器與錯誤處理。後端為 FastAPI，部署於 Docker 容器，對外透過 Nginx/DuckDNS 提供服務。

## Goals / Non-Goals

**Goals:**
- 建立獨立的 `frontend/` Vite + Vue 3 專案，完整替換現有 HTML 模板前端
- 以 axios 取代所有 `fetch` 呼叫，統一 HTTP 層
- 保持後端 FastAPI API 完全不變（僅新增 CORS middleware）
- 實現相同的所有功能：登入/註冊、打卡、請假系統、統計、員工名冊、系統設定、AI 聊天
- 使用 Vue Router 管理頁面、Pinia 管理登入狀態

**Non-Goals:**
- 不重構後端 API
- 不更改資料庫 Schema
- 不引入 TypeScript（保持 JavaScript 降低遷移成本）
- 不重新設計 UI 視覺風格（保留現有深色主題 CSS）
- 不實作 SSR（維持純 SPA）

## Decisions

### 決策 1：前端目錄位置

**選擇**：在專案根目錄建立 `frontend/` 與 `attendance_system/` 並列，而非放入 `attendance_system/app/static/`。

**理由**：前端為獨立建置單元，應有自己的 `package.json` 與 `node_modules`。建置產出的 `dist/` 內容再複製至後端靜態目錄或由 Docker 多階段建置處理。

**替代方案考量**：放在 `attendance_system/app/frontend/` → 混淆後端與前端邊界，不採用。

---

### 決策 2：Vue 組件劃分策略

**選擇**：依功能模組劃分 View 元件，以 Composable 封裝共用邏輯。

```
frontend/src/
├── views/
│   ├── AuthView.vue        # 登入/註冊
│   ├── HomeView.vue        # 打卡 + 今日狀態 + 大家出勤
│   ├── SearchView.vue      # 歷史紀錄查詢
│   ├── LeaveView.vue       # 請假申請 + 我的假單 + 待審核
│   ├── StatsView.vue       # 月份統計 + 個人資料
│   ├── StaffView.vue       # 員工名冊
│   └── SettingsView.vue    # 系統設定 + 地圖
├── composables/
│   ├── useAuth.js          # 登入/登出/角色
│   ├── useGeolocation.js   # GPS 定位邏輯
│   └── useNotification.js  # 通知 toast
├── components/
│   ├── MapModal.vue        # Leaflet 地圖 Modal
│   ├── ChatWidget.vue      # AI 聊天浮動視窗
│   └── AppNavbar.vue       # 側邊欄導覽
├── stores/
│   └── auth.js             # Pinia：使用者名稱、角色、登入狀態
├── api/
│   └── http.js             # axios instance + 攔截器
└── router/
    └── index.js            # Vue Router 路由定義
```

**理由**：現有 `main.js` 已有清晰的功能分區（auth、打卡、地圖、聊天、個人資料等），對應拆分降低認知負擔。

---

### 決策 3：axios 封裝方式

**選擇**：建立單一 axios instance (`api/http.js`)，設定 `baseURL`，加入 request/response interceptor。

```js
// api/http.js
import axios from 'axios'

const http = axios.create({ baseURL: '/api' })

// Request：自動帶入 username header（或 query param）
http.interceptors.request.use(config => {
  const username = localStorage.getItem('username')
  if (username) config.headers['X-Username'] = username
  return config
})

// Response：401 自動登出，統一解包 data
http.interceptors.response.use(
  res => res.data,
  err => {
    if (err.response?.status === 401) useAuthStore().logout()
    return Promise.reject(err.response?.data || err)
  }
)
export default http
```

**理由**：避免每個 API 呼叫重複帶 username 參數；統一錯誤格式使各 View 只需處理 `catch(err)` 而不需解析 HTTP status。

**替代方案考量**：保留各自的 `fetch` wrapper → 維持原本的問題，不採用。

---

### 決策 4：路由策略

**選擇**：Vue Router Hash 模式（`#/home`），避免需要 Nginx rewrite 規則處理 SPA 路由。

| 路由 | 元件 | 需要登入 |
|------|------|---------|
| `/` | AuthView | 否（自動導向） |
| `#/home` | HomeView | ✅ |
| `#/search` | SearchView | ✅ |
| `#/leave` | LeaveView | ✅ |
| `#/stats` | StatsView | ✅ |
| `#/staff` | StaffView | ✅ (role 1/2) |
| `#/settings` | SettingsView | ✅ (role 1) |

Navigation Guard：未登入時自動導向 AuthView。

---

### 決策 5：部署整合

**選擇**：Docker 多階段建置。Stage 1 用 Node.js 建置前端；Stage 2 複製 `dist/` 至 FastAPI 的 `app/static/dist/`，由 `StaticFiles` 提供服務，並以 catch-all route 回傳 `index.html`。

```dockerfile
# Stage 1 - Build frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Stage 2 - FastAPI
FROM python:3.11-slim
...
COPY --from=frontend-builder /frontend/dist /app/static/dist
```

**開發模式**：`vite dev` 啟動於 `localhost:5173`，`vite.config.js` 設定 proxy 將 `/api` 導向 FastAPI `localhost:8000`。

## Risks / Trade-offs

| 風險 | 緩解措施 |
|------|---------|
| Leaflet.js 在 Vue 環境中的生命週期衝突（地圖 div 尚未掛載） | 在 `onMounted` + `nextTick` 中初始化地圖；`onUnmounted` 時 `map.remove()` |
| 遷移期間前端暫時無法使用 | 先在 `frontend/` 建立新專案並通過本機測試，再替換 Docker 建置 |
| axios response interceptor 解包 `res.data` 可能與現有 API 呼叫慣例不一致 | 各 View 呼叫後直接拿 `data`（不需 `.data` 再解包），需審查所有 API 呼叫點 |
| Vue Router hash mode URL 與現有 bookmark 不相容 | 可接受：目前無外部連結到特定頁面 |

## Migration Plan

1. 建立 `frontend/` Vite 專案骨架（不影響現有後端）
2. 實作 `http.js`（axios）+ Pinia store + Vue Router
3. 依序實作各 View 元件，對應現有 `main.js` 功能
4. 本機以 Vite proxy 測試所有 API 功能
5. 新增 FastAPI CORS middleware + catch-all route
6. 更新 `Dockerfile` 加入多階段建置
7. 更新 `docker-compose.yml`
8. 部署測試，確認所有功能正常後移除舊 `main.js` 與 Jinja2 模板

**Rollback**：舊 `main.js` 與模板保留至最終確認，可隨時切回。

## Open Questions

- Leaflet.js 是否改為 npm 套件引入（`leaflet`），或維持從 CDN 載入？建議改為 npm 以符合 Vite 模組化。
- 開發時是否需要 Hot Reload 支援 FastAPI session？目前使用 localStorage，不影響。
