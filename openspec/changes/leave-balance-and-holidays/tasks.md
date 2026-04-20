## 1. 資料庫變更 (Database Schema)

- [x] 1.1 在 `app/models.py` 中新增 `Holidays` 模型 (date, name, is_holiday)
- [x] 1.2 在 `app/models.py` 中將 `User` 模型新增 `hire_date` (Date) 欄位
- [x] 1.3 在 `app/models.py` 中新增 `LeaveBalances` 模型 (user_id, leave_type, total_hours, used_hours, valid_from, valid_until)
- [x] 1.4 在 `app/schemas.py` 更新對應的 Pydantic 模型 (包含取得與修改的 Request/Response Schema)

## 2. 建立假勤計算核心邏輯

- [x] 2.1 實作函式 `calculate_request_hours`：給定起訖時間，計算區間內的實際工作時數（需跳過週末、跳過 `Holidays` 中 `is_holiday=True` 的日子，並計入 `is_holiday=False` 的補班日）。
- [x] 2.2 實作檢查特定假別剩餘可用時數 `(total_hours - used_hours)` 是否足夠的輔助邏輯。

## 3. 修改 API (Router)

- [x] 3.1 修改 `POST` 請假申請 API：送出假單前，呼叫時數計算與餘額檢查邏輯。若額度不足回傳 `400 Bad Request`。
- [x] 3.2 修改 `PUT` 審核通過 API：當主管按鈕審核通過後，自動將該假單的請假時數累加到該員工對應的 `LeaveBalances` 的 `used_hours` 欄位中。
- [x] 3.3 新增一隻 API 給後台人員使用（或啟動腳本），能以批次方式寫入該年度的政府日曆資料到 `Holidays` 表。

## 4. 前端介面連動 (Frontend)

- [x] 4.1 在員工的請假申請頁面，透過 API 獲取並顯示當前可用額度 (可用時數)。
- [x] 4.2 當無法請假 (收到 400 回應) 時，前端正確攔截並跳出錯誤提示對話框。
