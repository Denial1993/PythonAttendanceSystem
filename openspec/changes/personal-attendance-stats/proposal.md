## Why

目前系統對一般員工 (Role 3) 而言，只能看到一筆一筆的原始打卡紀錄，沒有任何「統計摘要」。員工無法輕易知道自己這個月遲到了幾次、幾分鐘，或是哪天忘記打下班卡。加入個人出勤統計頁面，能讓每位員工對自己的出勤狀況一目了然，也能在月底薪資計算前即時自我核對。

## What Changes

- 在後端新增一支「月份出勤統計 API」，接收員工當月打卡記錄並計算出統計數字（遲到次數、遲到總分鐘數、缺卡日數、正常出勤天數）。
- 在前端 Dashboard 新增「本月出勤統計」區塊，以視覺化方式呈現統計結果（含月份切換功能）。
- 統計區塊對所有角色開放，但查詢的資料僅限本人（Role 3 必定只看自己）。
- 遲到的判斷基準設定為「上班打卡時間 > 09:00」（此標準未來可由 HR 設定，但本次先硬編碼）。
- 「缺卡」的定義為有出勤但漏打上班卡或下班卡的日子。

## Capabilities

### New Capabilities
- `attendance-monthly-summary`: 計算並回傳員工指定月份的出勤統計摘要（遲到次數、遲到分鐘、缺卡日、出勤日）

### Modified Capabilities

## Impact

- `app/routers/attendance.py`：新增 `GET /api/attendance/summary` 端點。
- `app/schemas.py`：新增 `AttendanceMonthlySummary` response schema。
- `app/templates/index.html`：新增出勤統計 UI 區塊、月份選擇器與對應的 JS 邏輯。
