## ADDED Requirements

### Requirement: Leave Application Submission
員工 (Role 3) SHALL 能夠送出請假申請單，指定假別 (leave_type)、開始時間 (start_time)、結束時間 (end_time) 與事由 (reason)。

#### Scenario: Successful submission
- **WHEN** Role 3 使用者填寫完成有效假單資訊並送出時
- **THEN** 系統建立一筆新的請假紀錄，狀態預設為 "pending" (待審核)

### Requirement: View Own Leave Requests
員工 (Role 3) SHALL 能夠查看自己建立的所有歷史假單與當前假單狀態。

#### Scenario: View personal requests
- **WHEN** Role 3 使用者瀏覽請假頁面時
- **THEN** 畫面上僅列出該名使用者自己送出的假單紀錄

### Requirement: View All Leave Requests
主管與管理員 (Role 1, Role 2) SHALL 能夠瀏覽全公司所有員工的假單紀錄，特別是可以過濾出 "pending" 狀態的假單。

#### Scenario: View pending requests
- **WHEN** Role 1 或 Role 2 使用者瀏覽請假管理頁面時
- **THEN** 能夠看見包含其他員工在內的所有假單

### Requirement: Approve or Reject Leave Requests
主管與管理員 (Role 1, Role 2) SHALL 能夠將 "pending" 狀態的假單狀態更新為 "approved" (同意) 或 "rejected" (拒絕)。

#### Scenario: Approve request
- **WHEN** Role 1/2 使用者針對某張待審核假單點擊「同意」
- **THEN** 該假單狀態更新為 "approved"

#### Scenario: Reject request
- **WHEN** Role 1/2 使用者針對某張待審核假單點擊「拒絕」
- **THEN** 該假單狀態更新為 "rejected"
