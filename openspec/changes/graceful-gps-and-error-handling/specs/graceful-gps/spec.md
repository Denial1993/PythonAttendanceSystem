## ADDED Requirements

### Requirement: Graceful GPS Degradation
The frontend client SHALL attempt to retrieve GPS coordinates within a 5-second timeout window. If it fails, the client MUST fallback to sending a null-coordinate check-in request instead of aborting the operation.

#### Scenario: GPS retrieval fails or times out
- **WHEN** the user denies GPS permissions or the location request exceeds 5 seconds
- **THEN** the client proceeds to send the check-in request with null coordinates and notifies the user "無法獲取定位，將以無座標模式打卡"
