# 34. Security

## 1. Academic System Threat Model & Safeguards
While designed as an academic prototype, Crowd Flow incorporates defense-in-depth security best practices appropriate for municipal operational software:

1. **Authentication & Authorization:**
   - Passwords hashed using `passlib` with PBKDF2/Bcrypt and high iteration cost.
   - JWT tokens signed with strong random secret key stored in environment variables (`.env`).
   - Role-Based Access Control (`ROLE_OPERATOR` vs `ROLE_ADMIN`) verified on sensitive routes.
2. **Input Sanitization & Injection Prevention:**
   - All API inputs validated via strictly typed Pydantic v2 schemas.
   - All database queries parameterized via SQLAlchemy ORM, eliminating SQL injection.
3. **Network Isolation:**
   - CORS middleware restricted to designated frontend origin (`http://localhost:5173`).
4. **Credential Safety:**
   - Zero hardcoded passwords, tokens, or secret keys in source code; `.env.example` provided for safe environment setup.


## Security Architecture

`mermaid
flowchart TD
    USER["Operator"] --> LOGIN["Login Form"]
    LOGIN --> BCRYPT["bcrypt Password Hash Verification"]
    BCRYPT --> JWT["JWT Token Generation - HS256"]
    JWT --> HEADER["Authorization: Bearer Token"]
    HEADER --> MW["FastAPI Security Middleware"]
    MW --> ROLE{"Role Check"}
    ROLE -- Admin --> ADMIN["Full Access"]
    ROLE -- Operator --> OPS["Read + Control Access"]
    ROLE -- Viewer --> VIEW["Read-Only Access"]
`

