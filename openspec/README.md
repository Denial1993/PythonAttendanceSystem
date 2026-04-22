# 智能打卡 & 假勤管理系統 (Attendance System)

這是一個基於 **Python FastAPI** 與 **Vue 3** 概念開發的現代化打卡系統，具備智慧化管理、GPS 定位驗證、以及 AI 助理功能。

## 🚀 技術架構 (Tech Stack)

### 後端 (Backend)
* **語言**: Python 3.11+
* **框架**: [FastAPI](https://fastapi.tiangolo.com/) (高效能、自動化 Swagger 文件)
* **ORM**: SQLAlchemy (搭配 PostgreSQL 驅動)
* **資料庫**: [Supabase](https://supabase.com/) (PostgreSQL) - 提供穩定的雲端資料存取

### 前端 (Frontend)
* **基礎**: 原生 JavaScript (Vanilla JS) 搭配現代化架構設計
* **發展中**: 逐步轉向 Vue 3 組件化開發模式
* **地圖**: Leaflet.js (處理 GPS 打卡座標顯示)

### 雲端與自動化 (DevOps)
* **部署**: [Render](https://render.com/) (Docker 容器化部署)
* **監控**: [UptimeRobot](https://uptimerobot.com/) (透過 `/api/health` 確保服務不休眠)
* **自動化**: GitHub Actions (CI/CD 流程整合)

---

## 🛠️ 核心功能

- [x] **身分驗證**: 支援管理員 (Role 1/2) 與 一般員工 (Role 3) 權限控管。
- [x] **智能打卡**: 整合瀏覽器 Geolocation API，紀錄打卡經緯度。
- [x] **請假系統**: 完整的「申請、審核、扣額」流程，自動計算有效餘額。
- [x] **AI 助理**: 整合 Google Gemini，協助查詢打卡規範與系統操作。
- [x] **防休眠機制**: 透過 UptimeRobot 每 5 分鐘進行 Health Check，保持伺服器與資料庫活躍。

---

## 🏗️ 如何在本機執行

1. **複製專案**:
   ```bash
   git clone [https://github.com/Denial1993/PythonAttendanceSystem.git](https://github.com/Denial1993/PythonAttendanceSystem.git)
   cd PythonAttendanceSystem
   
2. **設定環境變數**:
   建立 .env 檔案並填入你的 DATABASE_URL (Supabase) 與 GEMINI_API_KEY。

3. **使用 Docker 啟動**:
   ```bash
   docker-compose up --build
   ```

4. **訪問頁面**:
   * 前端首頁: http://localhost:8000
   * API 文件 (Swagger): http://localhost:8000/docs

## 📘 檔案結構
- `app/main.py`:  FastAPI 應用入口。
- `app/models/`: SQLAlchemy 資料模型。
- `app/routers/`: 各項功能 API 路由。
- `app/schemas/`: Pydantic 資料驗證模型。
- `docker-compose.yml`: 部署設定。
