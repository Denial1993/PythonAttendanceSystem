## ADDED Requirements

### Requirement: 系統必須儲存員工的詳細個人資料
`User` 資料表必須能夠儲存員工的電話 (phone)、地址 (address) 以及薪資 (salary) 等額外核薪與聯絡關聯資料。

#### Scenario: 建立新員工帳號時
- **WHEN** 系統建立新的 User 記錄時
- **THEN** 新的 `phone`, `address`, `salary` 欄位允許設為空白 (nullable)，以便相容於舊有的員工註冊流程

### Requirement: 系統管理者與人資主管得檢視所有員工詳細資料
系統必須提供 API 讓擁有 Role 1 (Admin) 或 Role 2 (Manager) 權限的使用者，能夠一覽所有員工包含機敏資料在內的詳細列表。

#### Scenario: 權限符合時的資料讀取
- **WHEN** 登入使用者為 Role 1 或是 Role 2，並請求全體員工名冊
- **THEN** 系統必須回傳所有使用者的資料陣列，包含電話、地址、以及薪資

#### Scenario: 越權存取阻擋
- **WHEN** 登入使用者為 Role 3 (一般員工)，試圖請求全體員工詳細名冊
- **THEN** 系統必須拒絕該請求並回傳 403 Forbidden 錯誤碼

### Requirement: 員工得檢視自己的詳細個人資料
系統必須提供 API 讓一般員工 (Role 3) 能夠查詢屬於自己的完整個人資料，以確認聯絡資訊是否正確。

#### Scenario: 員工查詢個人資料
- **WHEN** 員工請求查詢自己的個人 Profile
- **THEN** 系統必須回傳該名員工的完整資料 (包含 phone, address, salary)，但不包含其他員工的資料
