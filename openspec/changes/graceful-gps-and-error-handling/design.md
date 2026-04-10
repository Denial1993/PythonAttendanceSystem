## Context

目前智能打卡系統的 GPS 定位機制過於剛性，當裝置無法獲取定位（拒絕授權、設備不支援、定位超時）時，流程會被徹底中斷，導致員工無法完成打卡，這增加了考勤紀錄遺漏的風險。
同時，系統的前端錯誤捕捉邏輯未能詳細傳達後端的錯誤訊息，當 API 返回非 `200` 狀態碼時，僅顯示制式的「連線錯誤」；且登入失敗時後端直接暴露出「帳號不存在」或「密碼錯誤」，這容易讓惡意攻擊者猜測系統內有效帳號。

## Goals / Non-Goals

**Goals:**
- 提供 GPS 定位 5 秒的 Timeout 控制。
- 定位失敗時啟動「降級模式（Graceful Degradation）」，將 `lat` 和 `lng` 設為 `null` 繼續執行打卡並透過 Notification 提示使用者。
- 後端接收打卡紀錄時，若發現座標皆為 `null`，則在 `status` 後方加上特定標記「(無定位)」。
- 若伺服器回傳明確的 `HTTPException(detail=...)`，前端要能讀取 `data.detail` 並呈現在畫面；網路斷線時則顯示「無法連接伺服器，請檢查網路」。
- 將 `auth.py` 的登入失敗邏輯之 `detail` 統一改為「帳號或密碼錯誤」，以防禦使用者列舉攻擊 (User Enumeration)。

**Non-Goals:**
- 不重新設計前端通知 (Notification) UI 元件，僅利用現有的 `showNotification` 函數。
- 不改變系統層級認證或授權邏輯，僅修改提示文字。

## Decisions

- **前端 GPS Timeout 實作**:
  使用 `Promise.race()` 將原有的 `navigator.geolocation.getCurrentPosition` 打包，和一個 5000 毫秒的 `setTimeout` 建立的 Reject Promise 進行處理競爭。超時後的 Error 與定位遭拒的 Error 合併處理，導向 `sendCheckInRequest(action, null, null)` 與發出黃色警告提示。
- **前端錯誤捕捉訊息讀取**:
  在發出 `fetch` 遇到 `res.ok === false` 時，先解析 `await res.json()` 並取得 `data.detail`。如果解析失敗或是有其他 `catch(err)` 攔截到，若是 `TypeError` (Network Error)，顯示網路無法連接。
- **後端狀態文字串接**:
  在 `attendance.py` API，當 `lat` 與 `lng` 皆為 `None` 時，存入 `Attendance` Model 時的 `status` 字串修改為 `f"{request.action} (無定位)"`。
- **登入錯誤模糊化**:
  登入 API 中，將「找不到使用者」以及「密碼驗證失敗」這兩個 `if` 區塊的回傳結果統整為拋出 `HTTPException(status_code=401, detail="帳號或密碼錯誤")`。

## Risks / Trade-offs

- **Risk: 無定位打卡遭濫用**
  - *Mitigation*: 降級允許打卡可能造成員工刻意關閉 GPS，規避出勤追蹤。因為此為人事管理層面考量，系統加上「(無定位)」註記已可提供主管後續稽核和管理之判斷依據。
