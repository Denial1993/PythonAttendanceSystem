# 06. 執行期視圖

## 6.1 打卡流程
描述員工點擊「上班打卡」時的系統運作：
1. **Frontend**：取得瀏覽器地理位置 (Latitude/Longitude)。
2. **Frontend**：呼叫 `POST /api/attendance` 並帶入員工名與座標。
3. **Backend**：驗證今日是否已有紀錄。
4. **Backend**：寫入 `attendances` 資料表，並更新狀態為「上班中」。
5. **Backend**：回傳打卡成功紀錄。
6. **Frontend**：更新 UI 狀態。

## 6.2 假單審核流程 (扣除額度)
1. **Admin**：在假單清單點擊「批准」。
2. **Backend**：呼叫 `update_leave_status`。
3. **Backend**：調用 `utils.calculate_request_hours` 計算時數（跳過假日與午休）。
4. **Backend**：調用 `utils.deduct_leave_balance` 扣除員工假別額度。
5. **Backend**：更新假單狀態為 `approved`。

## 6.3 AI 助理對話流程
1. **User**：在對話框輸入「我上週遲到了幾次？」。
2. **Backend**：接收請求，從資料庫查詢該 User 近 30 筆出勤資料。
3. **Backend**：將資料轉換為文字 Prompt。
4. **Backend**：呼叫 Gemini API。
5. **Backend**：回傳 Gemini 的回答。
