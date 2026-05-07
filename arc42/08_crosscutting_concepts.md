# 08. 橫切關注點

## 8.1 安全性 (Security)
- **密碼儲存**：使用 `passlib` 與 `bcrypt` 進行單向雜湊。
- **API 權限**：透過 `router.beforeEach` 在前端阻擋非法路徑，並在後端透過 `User.role` 進行權限檢查。

## 8.2 時區與國際化 (Localization)
- **台灣時區**：後端統一使用 `datetime.now(TW_TZ)` 以避免伺服器時區與台灣時間不一致的問題。
- **中文顯示**：系統介面與 AI 回覆均以繁體中文 (zh-TW) 為主。

## 8.3 資料驗證 (Validation)
- **Pydantic**：後端 API 輸入與輸出皆透過 Pydantic Schemas 進行類型檢查與資料清理。

## 8.4 種子資料 (Seeding)
- **自動化種子**：系統啟動時若資料庫為空，會自動執行 `seeds.py` 建立初始管理者帳號與基礎假別設定。
