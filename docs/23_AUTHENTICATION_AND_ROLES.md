# 23. Authentication and Roles

## 1. Security Architecture
The system employs stateless JSON Web Token (JWT) authentication using the HMAC-SHA256 (`HS256`) signing algorithm, paired with PBKDF2/Bcrypt password hashing (work factor 12).

## 2. User Roles & Permission Matrix

| Feature / Resource | Unauthenticated | Operator (`ROLE_OPERATOR`) | Admin (`ROLE_ADMIN`) |
| :--- | :---: | :---: | :---: |
| View Login Screen | Yes | Yes | Yes |
| View Live Dashboard & Telemetry | No | Read-Only | Read / Write |
| View CCTV Video Feeds | No | Read-Only | Read / Write |
| Trigger What-If Simulation | No | Yes | Yes |
| Calculate Alternative Detours | No | Yes | Yes |
| Acknowledge Alerts | No | Yes | Yes |
| Override Road Status Manually | No | Yes | Yes |
| Edit Camera Feeds & ROIs | No | No | Yes |
| Add / Delete Road Network Nodes | No | No | Yes |
| Adjust System Queue Thresholds | No | No | Yes |
| Manage User Accounts | No | No | Yes |

## 3. JWT Token Payload Example
```json
{
  "sub": "tanish_operator",
  "role": "ROLE_OPERATOR",
  "full_name": "Tanish Dhende",
  "exp": 1790707200,
  "iat": 1790678400
}
```
