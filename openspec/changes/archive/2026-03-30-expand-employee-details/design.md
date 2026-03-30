## Context

目前的打卡系統具備基本的上下班打卡以及身份驗證功能。隨著希望將系統轉型為輕量級人資管理系統 (ERP) 的需求浮現，我們需要替員工資料模型添加更多的人事相關欄位，例如電話、地址和薪資，以便主管 (Manager/HR) 能夠使用此系統進行薪酬計算與人員管理。

## Goals / Non-Goals

**Goals:**
- 在不影響現有打卡與登入機制的前提下，平滑擴充 `User` 資料表。
- 實作前後端介接，讓 Role 1 (Admin) 和 Role 2 (Manager) 能查看及編輯所有員工的詳細資料。
- 讓 Role 3 (Normal Employee) 能夠在登入後看到自己的詳細基本資料。

**Non-Goals:**
- 尚未實作完整的薪水與特休自動結算系統 (目前僅實作靜態薪資欄位的新增與顯示)。
- 尚未實作個人資料的員工自行修改功能 (考量到 HR 稽核，目前僅允許 Role 1/2 修改敏感資料如薪資)。

## Decisions

**1. 擴充既有的 User Model 而非建立關聯表 (Profile Table)**
- 理由：目前系統規模尚小，將 `phone`, `address`, `salary` 欄位直接加入 `User` table 能減少 JOIN 查詢的複雜度，提升資料讀寫效率。
- 替代方案：建立 `EmployeeProfile` 表與 `User` 一對一關聯。若未來資料欄位非常龐大 (例如破百個欄位)，可再考慮拆表，但目前尚不需要。

**2. 前端介面權限控制**
- 將於 `index.html` 內新增一個 Dashboard 區塊，該區塊的渲染將透過去判斷 `localStorage.getItem('role')` 來決定是否呈現給使用者，以及後端 API 也加上針對 Role 的驗證防護，確保不被越權存取。

## Risks / Trade-offs

- **資料庫擴充導致的遷移問題 (Data Migration Risk)**
  - 現有的 SQLite 或 PostgreSQL 資料夾庫如果直接新增欄位且設為 `nullable=False` 可能會報錯。
  - **Mitigation**: 新增的欄位 `phone`, `address`, `salary` 將預設為 `nullable=True` (允許為空)。未來再逐步確保資料補齊。
- **機敏個資的隱私風險**
  - 使用者的電話與薪資屬於高機密資料，若 API 權限管控不當會引起嚴重問題。
  - **Mitigation**: 後端 `/api/users` 等查詢全體員工資料的 endpoint 必須再三檢查 `current_user.role` 是否為 1 或是 2，否則拋出 403 Forbidden 錯誤。
