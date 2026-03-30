## Context

目前系統僅能記錄每日打卡時間與計算遲到/漏打卡，尚未涵蓋完整的假勤管理。在日常營運中，員工會有請假需求（事假、病假、特休等）。為了減少紙本簽核流程，提升 HR 管理效率，我們需要在此薪資及出勤系統中納入電子的「請假申請單系統」。

## Goals / Non-Goals

**Goals:**
- 建立 `leave_requests` 資料表紀錄請假資訊（申請人、假別、起訖時間、事由、審核狀態）。
- 提供 Role 3 (員工) 送出請假單的 API 與前端介面。
- 提供 Role 3 查看個人歷史請假紀錄與審核狀態的介面。
- 提供 Role 2 / Role 1 (主管/管理員) 瀏覽所有待審核假單的 API 與介面。
- 實作請假單的「同意」或「拒絕」功能。

**Non-Goals:**
- 自動計算特休餘額、病假額度（初期先由 HR 人工管控，或待後續擴充設定頁面）。
- 結合薪資引擎自動扣薪（本階段僅記錄並顯示是否扣薪假別，實際薪資計算模組將在後續另行開發）。
- 複雜的多簽核關卡流程（目前僅分為申請 -> 同意/拒絕 的單階層基本流程）。

## Decisions

1. **資料模型設計 (`LeaveRequest`)**
   - 欄位包含：`id`, `user_id`, `leave_type` (Enum: 事假, 病假, 特休...), `start_time`, `end_time`, `reason`, `status` (Enum: pending, approved, rejected), `created_at`, `updated_at`。
   - 使用 SQLModel / SQLAlchemy 在 PostgreSQL 中建立此關聯表。
2. **RESTful API 規劃 (`routers/leave.py`)**
   - `POST /api/leave`：員工送出假單。
   - `GET /api/leave`：員工查詢個人假單（Role 3），主管/管理員查詢全公司假單（Role 1/2 支持特定條件篩選如 status=pending）。
   - `PUT /api/leave/{id}/status`：主管/管理員更新假單狀態（approve / reject）。
3. **前端 UI 整合**
   - 在 `index.html` 的 Dashboard 頁籤中新增兩塊區域：
     1. 給 Role 3 的「請假申請 / 我的假單」區塊。
     2. 給 Role 1/2 的「待審核假單」區塊。
   - 透過隱藏或顯示 DIV (`display: none` / `block`) 來區分角色的可見範圍，透過現行的 JS authentication state 控制。

## Risks / Trade-offs

- **Risk:** 如果未來出勤統計 (`GET /api/attendance/summary`) 時沒有綜合考量已核准的請假，會造成員工明明請假卻顯示為「缺卡」或「遲到」。
  - **Mitigation:** 此變更只涵蓋請假單自身生命週期，但未來必須更新 `attendance` 模組查詢邏輯，讓日期範圍若命中 approved leave_request 則不以遲到或缺卡計。
- **Trade-off:** 目前使用原有的 `app/templates/index.html` 開發 SPA，檔案會越來越大。
  - **Decision:** 現階段為快速實現功能，繼續維護單一檔案是可接受的，但後續可以考慮導入前端框架 (如 Vue/React) 重構。
