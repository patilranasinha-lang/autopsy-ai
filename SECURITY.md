# AutopsyAI Security Overview

## Core Security Principles

### 1. Layered Architecture
The user management system follows a strict layered architecture to ensure separation of concerns:
- **Routes Layer**: Handles HTTP requests/responses and input validation
- **Service Layer**: Contains business logic and security checks
- **Repository Layer**: Manages database interactions (no raw SQL exposed)
- **Model Layer**: Defines data structures and relationships

### 2. Input Validation
All user inputs are validated before processing:
- **Email Format**: RFC-compliant email validation using regular expressions
- **Password Strength**: Minimum 8 characters (enforced in validator)
- **Username/Email Uniqueness**: Checked before user creation to prevent duplicates
- **Sanitized Outputs**: User data returned via API never includes sensitive information like passwords

### 3. Password Security
Passwords are never stored in plaintext:
- **Hashing**: Uses Werkzeug's `generate_password_hash` which defaults to PBKDF2 with SHA-256
- **Salt Generation**: Automatic cryptographically secure salt generation per password
- **Constant-time Comparison**: Password verification uses `check_password_hash` which is resistant to timing attacks

### 4. Authentication & Authorization
- **JWT Tokens**: Uses Flask-JWT-Extended for stateless authentication
- **Protected Routes**: `/api/auth/profile` requires valid JWT token
- **Generic Error Messages**: Prevents account enumeration by returning "Invalid credentials" for both non-existent users and wrong passwords
- **No Sensitive Data in Logs**: Logs never include passwords or partial credentials

### 5. Database Security
- **Parameterized Queries**: Uses SQLAlchemy ORM which prevents SQL injection
- **Relationship Integrity**: Foreign keys with cascading deletes to maintain data consistency
- **Indexing**: Indexes on username, email, and user_id for efficient lookups without exposing more data

## Threat Mitigation Strategies

| Threat | Mitigation |
|--------|------------|
| SQL Injection | Uses SQLAlchemy ORM with parameterized queries |
| Password Brute Force | Generic error messages, future: rate limiting |
| Account Enumeration | Generic "Invalid credentials" response for all login failures |
| Timing Attacks | Constant-time password comparison |
| XSS Attacks | Output sanitization (to_dict() method removes sensitive data) |
| Sensitive Data Exposure | No plaintext passwords, no sensitive data in logs |

## Environment Variables
Ensure these are set in production (never commit to version control):
- `SECRET_KEY`: Flask secret key for session management
- `JWT_SECRET_KEY`: Secret key for signing JWT tokens (minimum 32 bytes recommended)
- `DATABASE_URL`: PostgreSQL connection string with credentials
