## 1. 資料庫層 (Database Layer)

- [x] 1.1 修改 `app/models.py`：在 `User` Model 中新增 `phone` (String, nullable)、`address` (String, nullable)、`salary` (Integer, nullable) 三個欄位
- [x] 1.2 確認資料庫遷移策略：由於系統使用 `Base.metadata.create_all()`，重新啟動時會以 `ALTER TABLE` 追加欄位，或透過刪除並重建資料表完成遷移（開發環境）

## 2. Schema 層 (Pydantic Schemas)

- [x] 2.1 修改 `app/schemas.py`：在 `UserResponse` 中新增 `phone`, `address`, `salary` 的 Optional 欄位，讓 API 能回傳這些資料
- [x] 2.2 在 `app/schemas.py` 新增 `UserProfileUpdate` Schema，包含 `phone`, `address`, `salary` 等可更新欄位，供 HR 更新員工資料時使用

## 3. API 路由層 (Routers)

- [x] 3.1 新增 `app/routers/users.py`：建立 `GET /api/users` 端點，僅允許 Role 1 / Role 2 呼叫，回傳全體員工詳細資料列表（含電話、地址、薪資）
- [x] 3.2 在 `app/routers/users.py`：建立 `GET /api/users/me` 端點，供任何已登入員工查詢自身的詳細資料
- [x] 3.3 在 `app/routers/users.py`：建立 `PUT /api/users/{user_id}` 端點，僅允許 Role 1 / Role 2 呼叫，可更新指定員工的詳細欄位（使用 `UserProfileUpdate` Schema）
- [x] 3.4 在 `app/main.py` 中 `include_router` 載入新的 `users` router，掛載前綴 `/api/users`

## 4. 前端介面 (Frontend UI)

- [x] 4.1 在 `index.html` 的 Dashboard View 中，新增「員工名冊」區塊（僅 Role 1 / Role 2 可見），以卡片或表格形式展示所有員工的電話、地址、薪資
- [x] 4.2 在「員工名冊」區塊加入「編輯」按鈕，點擊後彈出 Modal 讓 HR 修改電話、地址、薪資，並呼叫 `PUT /api/users/{user_id}`
- [x] 4.3 在 `index.html` 的 Dashboard View 中，新增「我的個人資料」區塊（所有角色皆可見），呼叫 `GET /api/users/me` 顯示自身的電話與地址資訊（Role 3 不顯示薪資）
- [x] 4.4 在 `showDashboard()` 函式中，依角色控制「員工名冊」和「個人資料」區塊的顯示邏輯

## 5. 驗證與測試

- [x] 5.1 手動測試：以 Role 2 帳號登入，確認可以看到員工名冊並成功編輯薪資
- [x] 5.2 手動測試：以 Role 3 帳號登入，確認看不到員工名冊，但可以看到自己的個人資料
- [x] 5.3 手動測試：直接呼叫 `GET /api/users`（以 Role 3 的 username），確認系統回傳 403 Forbidden

