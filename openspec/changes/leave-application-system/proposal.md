## Why

為了讓此系統更具備 HR ERP 的完整功能，除了目前能查看出勤數據與計算遲到扣薪之外，還需要讓員工 (Role 3) 可以透過系統直接申請請假，省去紙本作業。同時主管 (Role 2) 及系統管理員 (Role 1) 可以在線上審核（同意或拒絕）假單，進而將請假紀錄與出勤統計結合在未來的薪資計算中。

## What Changes

- 新增請假單的資料表 (`LeaveRequest`) 與對應的 SQLAlchemy Model / Pydantic Schema。
- 新增請假單的 CRUD API。
- 員工 (Role 3) 可以在前端介面填寫請假表單（選擇假別、起訖時間、事由等）並送出。
- 員工 (Role 3) 可以查看自己過去與目前的請假進度。
- 主管 (Role 2) / 管理員 (Role 1) 可以在前端介面看到所有待審核的假單，並進行「同意」或「拒絕」的操作。

## Capabilities

### New Capabilities
- `leave-application`: 涵蓋假單的建立、查詢、以及主管審核流程。

### Modified Capabilities
- `personal-attendance-stats`: 未來可能需要將「請假」計入出勤統計，不過本次先僅以建立請假系統為核心。

## Impact

- **Database**: 需新增 `leave_requests` 資料表，紀錄員工的假單資訊與狀態（待審核、已同意、已拒絕）。
- **Backend APIs**: 需擴充 `/api/leave` 相關的 RESTful 路由。
- **Frontend**: Dashboard 需要切分或新增「請假申請」區塊以及「待審核假單」區塊（依據 Role 身分顯示）。
