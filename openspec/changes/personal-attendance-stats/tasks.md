## 1. 後端 Schema 層

- [x] 1.1 在 `app/schemas.py` 新增 `AttendanceDailyDetail` Schema
- [x] 1.2 在 `app/schemas.py` 新增 `AttendanceMonthlySummary` Schema

## 2. 後端 API 層

- [x] 2.1 在 `app/routers/attendance.py` 頂部新增常數 `WORK_START_HOUR = 9`、`WORK_START_MINUTE = 0`
- [x] 2.2 在 `app/routers/attendance.py` 新增 `GET /api/attendance/summary` 端點
- [x] 2.3 在 summary 端點中驗證權限 logic
- [x] 2.4 實作 summary 從 records 計算統計資訊的 logic

## 3. 前端 CSS 與 HTML

- [x] 3.1 在 `index.html` 的 `<style>` 區塊新增出勤統計所需的 CSS 樣式
- [x] 3.2 在 Dashboard View 新增「本月出勤統計」介面區塊

## 4. 前端 JavaScript 邏輯

- [x] 4.1 新增 `loadMonthlySummary(year, month)` 函式：呼叫 `GET /api/attendance/summary`，將統計數字填入四格卡片
- [x] 4.2 新增 `renderDailyDetails(details)` 函式：將每日明細渲染成列表，遲到的行加上警示色、缺卡的行加上不同標示
- [x] 4.3 在月份選擇器 `change` 事件監聽中呼叫 `loadMonthlySummary()`，讓使用者切換月份時自動更新
- [x] 4.4 在 `showDashboard()` 函式中加入自動載入當月統計的呼叫

## 5. 驗證與測試

- [ ] 5.1 手動測試：以 Role 3 員工登入，確認「本月出勤統計」區塊正確顯示（有打卡資料時）
- [ ] 5.2 手動測試：切換到沒有打卡資料的月份，確認顯示「本月尚無出勤記錄」而非錯誤
- [ ] 5.3 手動測試：確認遲到計算正確（對比資料庫中的打卡時間）
