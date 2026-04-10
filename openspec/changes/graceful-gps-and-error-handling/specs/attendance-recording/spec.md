## MODIFIED Requirements

### Requirement: Save coordinates with Attendance 
The system SHALL extend the attendance recording process to save the user's geographic coordinates alongside the check-in and check-out times. If coordinates are absent, the system SHALL explicitly mark the status text to indicate the absence of location data.

#### Scenario: Recording an attendance action
- **WHEN** the backend receives an attendance action request containing `lat` and `lng` parameters
- **THEN** the system updates the corresponding `Attendance` record with the provided location coordinates (e.g., `check_in_lat`, `check_out_lat`).

#### Scenario: Recording a coordinate-less attendance action
- **WHEN** the backend receives an attendance action request where `lat` and `lng` are null
- **THEN** the system appends " (無定位)" to the status field (e.g., "上班 (無定位)") before inserting into the database.
