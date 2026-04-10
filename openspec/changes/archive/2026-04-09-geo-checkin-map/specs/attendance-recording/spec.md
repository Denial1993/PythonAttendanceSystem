## ADDED Requirements

### Requirement: Save coordinates with Attendance 
The system SHALL extend the attendance recording process to save the user's geographic coordinates alongside the check-in and check-out times.

#### Scenario: Recording an attendance action
- **WHEN** the backend receives an attendance action request containing `lat` and `lng` parameters
- **THEN** the system updates the corresponding `Attendance` record with the provided location coordinates (e.g., `check_in_lat`, `check_out_lat`).
