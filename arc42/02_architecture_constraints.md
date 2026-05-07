# 02. 架構限制

## 2.1 技術限制
- **後端框架**：必須使用 Python FastAPI 框架。
- **前端框架**：使用 Vue 3 (Vite) + Pinia 狀態管理。
- **資料庫**：使用 PostgreSQL (正式環境託管於 Supabase)。
- **ORM**：使用 SQLAlchemy 2.0+。

## 2.2 部署限制
- **正式機平台**：部署於 Render (Web Service)。
- **容器化**：開發環境需支援 Docker Compose 一鍵啟動。
- **靜態資源**：前端建置產物需由 FastAPI 伺服器掛載提供。

## 2.3 組織與資安限制
- **時區限制**：系統必須鎖定為 台灣時區 (UTC+8)。
- **認證機制**：需具備密碼加密儲存 (bcrypt) 與基礎角色權限控制 (Admin, Manager, Normal)。
