## ADDED Requirements

### Requirement: Unified Error Messages
The system SHALL intercept login failures and provide standardized error messages. For login, any failure due to invalid username or password MUST result in a generic "帳號或密碼錯誤" message to prevent account enumeration attacks.

#### Scenario: User provides an incorrect password or non-existent username
- **WHEN** user attempts to log in with an incorrect password or an unregistered username
- **THEN** the API returns a 401 Unauthorized status code with the detail "帳號或密碼錯誤"

### Requirement: Detailed Client-Side Error Reporting
The frontend client SHALL display specific error messages returned by the server when the response status is not successful, provided a specific detail exists.

#### Scenario: API returns a specific error detail
- **WHEN** the backend responds with a non-200 status code and contains `{ "detail": "<specific message>" }`
- **THEN** the client extracts the detail and displays `<specific message>` to the user via a notification

#### Scenario: Complete network failure
- **WHEN** the fetch request fails entirely due to a network error
- **THEN** the client suppresses the raw exception and notifies the user with "無法連接伺服器，請檢查網路"
