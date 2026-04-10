## ADDED Requirements

### Requirement: Get Geo-location on Check-in
The system SHALL request the user's geographic location (latitude and longitude) via the browser's Geolocation API when any attendance action (clock-in, clock-out, lunch break) is triggered.

#### Scenario: User grants location permission
- **WHEN** user clicks an attendance action button and permits location tracking
- **THEN** the system successfully captures the current latitude and longitude and includes them in the API request

#### Scenario: User denies location permission
- **WHEN** user clicks an attendance action button but denies location tracking
- **THEN** the system blocks the attendance action and displays an error message informing the user that location permission is required.
