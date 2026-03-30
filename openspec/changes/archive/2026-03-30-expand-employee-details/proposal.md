## Why

為了將現有的打卡系統升級為輕量級人資系統 (ERP)，首要任務是擴充員工的詳細資料。目前的 `User` 資料表僅包含帳號、密碼和角色，缺乏能用來聯絡與計算薪資的核心基本資料。藉由擴增電話、地址及薪資欄位，能讓 HR (Role 2) 擁有充足的資訊進行未來薪酬結算以及日常的人事管理。

## What Changes

- 在系統的 `User` 資料模型 (Database Schema) 中新增 `phone` (電話)、`address` (地址)、與 `salary` (薪資) 等欄位。
- 建立給予 HR (Role 2) 檢視與管理所有員工詳細資料的後端 API。
- 建立給予一般員工 (Role 3) 檢視個人詳細聯絡資訊的後端 API。
- 在前端 Dashboard 新增「員工資料管理區塊」(僅限 Role 1, 2 可見)，以及「個人資料區塊」(依據角色顯示對應功能)。

## Capabilities

### New Capabilities
- `employee-profile`: 涵蓋員工詳細個人聯絡資訊、敘薪資料的建立與檢視能力。

### Modified Capabilities

## Impact

- `app/models.py` 的 `User` model 將被擴充並需要執行資料庫遷移 (Database Migration)。
- `app/schemas.py` 將新增或修改 User 的 Pydantic schema 來處理新的資料欄位。
- `app/routers/auth.py` (或其他新的 router 例如 `users.py`) 將新增 API 端點。
- `app/templates/index.html` 將會有相對應的前端介面更新。
