## 1. 後端修改

- [x] 1.1 修改 `app/routers/auth.py` 中 `login` API 的錯誤處理邏輯，將帳號不存在或密碼錯誤的情境，統一拋出 `HTTPException(status_code=401, detail="帳號或密碼錯誤")`。
- [x] 1.2 修改 `app/routers/attendance.py` 的打卡新增邏輯，若 `request.lat` 和 `request.lng` 皆為 null，將 `request.action` 字串修改為附帶 "(無定位)" 後再存入資料庫。

## 2. 前端修改

- [x] 2.1 在 `app/static/main.js` 實作包含 5 秒 Timeout 的 GPS 定位取得 Promise (`Promise.race`)。
- [x] 2.2 修改 `app/static/main.js` 的 `performAction`，替換原先中斷程序的定位失敗邏輯為「給予警告並向下相容，將 lat 與 lng 帶 null 進行無座標打卡 (`sendCheckInRequest`)」。
- [x] 2.3 調整 `app/static/main.js` 所有的 fetch try...catch 區塊 (包含登入、註冊、打卡)，使其在 `!res.ok` 時不僅顯示連線錯誤，而是嘗試解析 `data.detail` 後透過 Notification 將詳細錯誤呈現給使用者。
- [x] 2.4 在 `app/static/main.js` 的 try...catch 的 catch 捕捉端點中，遇到 TypeError 或無伺服器回應狀況，統一顯示「無法連接伺服器，請檢查網路」。
