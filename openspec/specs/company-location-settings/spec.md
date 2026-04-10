## ADDED Requirements

### Requirement: Configurable Company Base Location
The system SHALL allow Role 1 (Admin) users to configure and update the company's designated base geolocation (latitude and longitude) via a secure interface.

#### Scenario: Admin updates the base location
- **WHEN** a Role 1 user submits new latitude and longitude values in the settings interface
- **THEN** the system updates the global system settings in the database to reflect the new coordinates.

#### Scenario: Unauthorized access attempt
- **WHEN** a non-Admin user (Role 2 or Role 3) attempts to access or submit changes to the base location settings
- **THEN** the system denies access with a 403 Forbidden error.
