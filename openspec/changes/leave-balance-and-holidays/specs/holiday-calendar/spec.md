## ADDED Requirements

### Requirement: 建立及維護公司休假日曆
系統必須具備儲存並查詢每一天是否為需上班之工作日的能力，以此判定請假時是否扣除時數或是否記為曠職。

#### Scenario: 查詢特定日期是否為假日
- **WHEN** 系統要求計算或驗證某個日期
- **THEN** 後端查詢 `Holidays` 表，若存在且 `is_holiday=true` 則該日無出勤義務。

#### Scenario: 處理補班日
- **WHEN** 行政機關規定週六為補班日
- **THEN** 該日在 `Holidays` 的設定必須標記為 `is_holiday=false`，代表有出勤義務，請假時數需算入。
