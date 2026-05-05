## Why

目前前端為單一大型 `main.js` 純原生 JavaScript 搭配 Jinja2 HTML 模板，隨著功能增加（打卡、請假、統計、人員管理、設定），程式碼已超過 1000 行且難以維護。同時所有 API 呼叫使用原生 `fetch`，缺乏統一的錯誤處理、請求攔截與請求取消等企業級功能。遷移至 Vue 3 + Vite 可大幅提升可維護性與開發體驗。

## What Changes

- **BREAKING**: 前端從 Jinja2 模板 (`base.html`, `index.html`, `navbar.html`) 改為 Vue 3 SPA 架構，FastAPI 後端改為僅提供 API 服務
- **BREAKING**: 移除所有 `main.js` 中的 `fetch` 呼叫，改為 axios 封裝
- 新增獨立的 Vite 前端專案目錄 (`frontend/`)，與 `attendance_system/` 並列
- 將現有的 UI 功能拆分為 Vue 3 元件：登入、打卡、請假、統計、員工名冊、系統設定
- 新增 axios instance 配置：統一 baseURL、請求/回應攔截、401 自動登出
- 新增 Vue Router 管理頁面路由
- 新增 Pinia 管理全域狀態（使用者資訊、角色）
- FastAPI 新增 CORS middleware 與靜態資源服務（或由 Nginx 提供）
- Docker Compose 新增前端建置流程或開發 proxy 配置

## Capabilities

### New Capabilities

- `vue-frontend-app`: Vue 3 + Vite 前端應用，包含所有現有功能的元件化實作
- `axios-http-client`: 封裝 axios instance，提供統一的 API 呼叫方式、攔截器與錯誤處理

### Modified Capabilities

- `attendance-recording`: 打卡 API 呼叫從 `fetch` 改為 axios，行為規格不變
- `geo-location-tracking`: GPS 定位邏輯移入 Vue Composable，行為規格不變
- `company-location-settings`: 設定頁改為 Vue 元件，行為規格不變

## Impact

- **前端目錄**: 新增 `frontend/` 目錄，包含 `package.json`、`vite.config.js`、`src/` 等 Vite 標準結構
- **後端**: `attendance_system/app/main.py` 需新增 CORS middleware；Jinja2 模板可保留或最終移除
- **依賴**: 前端新增 `vue@3`、`vue-router@4`、`pinia`、`axios`；後端新增 `fastapi[cors]`
- **Docker**: `Dockerfile` 需加入 Node.js 建置步驟，或使用多階段建置
- **部署**: 建置產出的 `dist/` 靜態資源由 FastAPI 的 `StaticFiles` 或 Nginx 提供服務
