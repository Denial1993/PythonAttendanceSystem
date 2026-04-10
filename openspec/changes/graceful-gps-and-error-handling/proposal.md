## Why

此變更旨在優化智能打卡系統的穩定性、使用者體驗，並提升登入機制的安全性。當前，若使用者裝置無法獲取 GPS 定位（拒絕、超時或設備不支援），打卡流程會被直接中斷；此外，目前的錯誤提示較為死板，無法有效傳達後端的具體錯誤原因。在安全性方面，登入失敗時若明確指出帳號不存在或密碼錯誤，存在被猜測帳號的資安風險，故需統一錯誤訊息。

## What Changes

- 修改前端 (`main.js`) 裡的 GPS 定位邏輯，設定 Timeout 為 5 秒，若定位失敗則進行彈性降級，以「無座標模式」繼續完成打卡並發送提示。
- 修改後端 (`attendance.py`)，當收到經緯度均為 `null` 的打卡請求時，於資料庫狀態欄位 (`status`) 自動加上 `(無定位)` 之附註（例如「上班 (無定位)」）。
- 優化前端 (`main.js`) 全域錯誤處理（包含註冊、登入、打卡），若伺服器回傳明確錯誤（抓取 `data.detail`），則顯示該具體訊息；若是網路異常（Network Error），則統一提示「無法連接伺服器，請檢查網路」。
- **BREAKING** 優化後端 (`auth.py`) 的登入驗證 API，將登入失敗（帳號錯誤或密碼錯誤）的提示統整為模糊訊息「帳號或密碼錯誤」，防止使用者猜測。

## Capabilities

### New Capabilities
- `error-handling`: 建立前後端統一且安全的錯誤處理機制，前端可捕獲伺服器詳細錯誤，後端避免暴露帳號是否存在。
- `graceful-gps`: 允許在無法獲取 GPS 的情況下彈性容錯，提供無坐標打卡模式。

### Modified Capabilities
- `attendance-recording`: 修改打卡功能，增加無定位打卡狀況下的狀態標記功能 (Appending "(無定位)" to status)。

## Impact

- **前端 (`app/static/main.js`)**: 變更 `performAction`、登入、註冊以及其他相關請求的錯誤捕捉邏輯 (`try...catch`)。
- **後端 API (`app/routers/attendance.py`)**: 調整新增打卡紀錄的邏輯，過濾 `null` 經緯度並修改儲存之 `status`。
- **後端 API (`app/routers/auth.py`)**: 登入端點之錯誤回報 `detail` 參數邏輯變更為統一文字。
