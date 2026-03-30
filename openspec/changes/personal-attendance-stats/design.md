## Context

現有的 attendance router 已有 `/search` 端點可依日期區間查詢打卡紀錄，回傳的是原始記錄列表。本次要在後端新增「統計計算」邏輯，對原始記錄進行二次處理後回傳摘要數字，並在前端用視覺化卡片呈現給員工。

現有的 Attendance model 欄位如下：
- `date`：日期
- `check_in_time`：上班打卡時間
- `check_out_time`：下班打卡時間
- `lunch_out_time` / `lunch_in_time`：午休進出
- `status`：目前狀態字串

## Goals / Non-Goals

**Goals:**
- 新增後端 API 計算並回傳員工特定月份的出勤統計摘要。
- 前端新增互動式統計卡片，讓員工可以選擇月份查閱自己的出勤數字。
- 呈現每日出勤明細列表，讓員工能看出哪天遲到或缺卡。

**Non-Goals:**
- 不允許員工自行修改任何打卡記錄（仍為唯讀）。
- 遲到標準尚不開放由 HR 動態設定（本次先固定為 09:00）。
- 尚未加入「補打卡申請」功能。

## Decisions

**1. 統計計算在後端還是前端？**
- **決定：後端計算**。好處是邏輯集中、可複用（例如未來薪資結算時可直接呼叫），前端只負責渲染。
- 替代方案：前端 JavaScript 計算。缺點是邏輯分散、不易維護，且未來很難給薪資模組重用。

**2. 遲到判定標準**
- **決定：固定為上班時間 > 09:00**。計算方式為 `check_in_time > time(9, 0)` 則視為遲到，遲到分鐘 = `(check_in_time - 09:00)` 的分鐘數。
- 若當日完全沒有 `check_in_time` 記錄，則不計入遲到，而是計入「缺卡日」。

**3. 「缺卡日」定義**
- 有 Attendance 記錄但 `check_in_time` 為 null 的日子。
- `check_out_time` 為 null 也視為「未完整打卡」，在明細中標示，但不計入缺卡日次數（下班忘打卡另外標示）。

**4. API 設計：Query Parameters**
- `GET /api/attendance/summary?username=xxx&year=2026&month=3`
- 使用 query parameters，和現有其他 attendance 端點的風格保持一致。

## Risks / Trade-offs

- **遲到定義異動風險**：若未來公司決定上班時間改為 08:30，需要改動後端 hard-coded 的標準。
  - **Mitigation**：將 `WORK_START_HOUR` 抽出為模組等級的常數，未來便於修改。
- **月份無資料**：若查詢的月份完全沒有任何打卡記錄，API 仍應正常回傳空統計（全為 0），前端應優雅顯示「本月尚無出勤記錄」。
