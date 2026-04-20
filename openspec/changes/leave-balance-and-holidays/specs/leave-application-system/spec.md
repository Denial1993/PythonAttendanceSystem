## ADDED Requirements

### Requirement: 請假時數連動國定假日與補班日運算
修改原本可能只用天數相減或單純計算區間時數的機制，請假時數計算過程必須扣除非工作日。

#### Scenario: 跨越國定假日請假
- **WHEN** 員工申請的請假區間中包含 `is_holiday=true` 的日期或單純週休週末
- **THEN** 系統計算 `total_request_hours` 時會自動跳過這些日子。

### Requirement: 檢查個人假勤額度防呆
在建立新的 `LeaveRequest` 時，強制檢查 `LeaveBalances` 是否足夠。

#### Scenario: 申請超出可用額度
- **WHEN** 員工提出 24 小時的特休申請，但該假別目前的餘額 (total_hours - used_hours) 只有 16 小時
- **THEN** 系統拒絕假單成立，拋出 400 Bad Request 錯誤，並提示額度不足。
