## 1. 資料庫與資料模型 (Backend)

- [x] 1.1 在 `app/models.py` 新增 `LeaveRequest` 資料表，包含 `id`, `user_id` (ForeignKey), `leave_type`, `start_time`, `end_time`, `reason`, `status`, `created_at`, `updated_at`
- [x] 1.2 在 `app/schemas.py` 建立對應的 Pydantic 模型 (如 `LeaveRequestCreate`, `LeaveRequestOut`, `LeaveRequestUpdateStatus`)
- [x] 1.3 執行 Alembic（若有導入）或直接重啟 Docker (`docker-compose restart`) 讓 SQLModel 自動建立表格 (取決於系統當前設定檔策略)

## 2. API 路由建立 (Backend)

- [x] 2.1 建立新的 router `app/routers/leave.py`，並在 `app/main.py` 註冊該路由
- [x] 2.2 實作 `POST /api/leave`：接收請假表單，建立新的 `LeaveRequest` 紀錄，狀態預設設為 `pending`
- [x] 2.3 實作 `GET /api/leave`：讀取使用者的假單。Role 3 僅回傳個人的紀錄；Role 1/2 可帶入 query 參數回傳指定或所有紀錄
- [x] 2.4 實作 `PUT /api/leave/{id}/status`：接收 `status` (`approved` 或 `rejected`) 更新請假單狀態，必須驗證操作者身分為 Role 1/2

## 3. 前端 UI - 員工請假介面 (Role 3)

- [x] 3.1 在 `index.html` 的 Dashboard 建立「請假申請」區塊 (`<div id="leaveApplyBlock">`)
- [x] 3.2 建立請假表單：包含「假別下拉選單」、「開始時間(datetime)」、「結束時間(datetime)」、「事由」及送出按鈕
- [x] 3.3 建立「我的假單」歷史列表區塊 (`<div id="myLeaveListBlock">`)
- [x] 3.4 實作 JS：發送 POST request 送出假單，成功後自動重新讀取列表
- [x] 3.5 實作 JS：發送 GET request 取回假單並渲染列表，搭配狀態徽章 ( pending(灰)/approved(綠)/rejected(紅) )

## 4. 前端 UI - 主管審核介面 (Role 1/2)

- [x] 4.1 在 `index.html` 的 Dashboard 建立「待審核假單」區塊 (`<div id="leaveApprovalBlock">`)
- [x] 4.2 實作 JS：根據 Role，若是 1 或 2，才顯示上述審核區塊
- [x] 4.3 實作 JS：發送 GET request 取回所有 (或指定條件) 假單，渲染於審核列表中，並在此列表中加上「同意」、「拒絕」兩顆按鈕
- [x] 4.4 實作按鈕點擊事件：呼叫 `PUT /api/leave/{id}/status`，根據主管點擊結果送出對應狀態，完成後重新整理審核列表

## 5. 測試與驗證

- [x] 5.1 登入 Role 3 帳號，測試提交事假與病假，確認「我的假單」中有顯示且為 "pending"。
- [x] 5.2 登入 Role 2 帳號，確認「待審核假單」有浮現剛剛送交的紀錄。
- [x] 5.3 點擊「同意」或「拒絕」，觀察前端 UI 與資料庫是否更新狀態。
- [x] 5.4 再次登入 Role 3 帳號，確認剛剛被主管審核通過的假單狀態轉為 "approved"。
