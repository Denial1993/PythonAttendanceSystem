## ADDED Requirements

### Requirement: Map Viewing Interface for Admins
The system SHALL provide an interface for Role 1 (Admin) and Role 2 (Manager) users to view the geographic location of an attendance record on a map.

#### Scenario: Admin views a check-in location
- **WHEN** an Admin clicks the "View Map" link or button next to an employee's check-in record
- **THEN** a Leaflet.js map is displayed centered on the recorded coordinates of that check-in.

#### Scenario: Displaying base location
- **WHEN** the map view opens for a check-in record
- **THEN** the map also displays a marker representing the company's base location, allowing visual distance comparison.
