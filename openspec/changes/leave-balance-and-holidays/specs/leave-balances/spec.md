## ADDED Requirements

### Requirement: 建立特休發放與計算邏輯 (週年制)
系統需為每一位設定了 `hire_date` 的員工，在到職日滿半年、一年、兩年等週期時，建立並發配對應天數換算成的「小時」進入 `LeaveBalances` 中。

#### Scenario: 員工到職滿半年獲得特休
- **WHEN** 員工到職日滿半年
- **THEN** 系統在其 `LeaveBalances` 新增 `total_hours=24` (3天*8小時) 的特休額度，並設定 `valid_until` 為滿一年的那一天。

### Requirement: 使用者能查詢個人額度
員工進入請假系統介面時，系統必須顯示當前年度所有假別的可用剩餘時數。

#### Scenario: 進入請假申請頁面
- **WHEN** 員工登入並導航至請假申請子頁面
- **THEN** 前端請求後端 API 取得該員工目前的 `total_hours` 與 `used_hours` 並計算相減，顯示於畫面上。
