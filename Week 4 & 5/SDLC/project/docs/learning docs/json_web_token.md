# JSON Web Token (JWT) - Complete Guide

## What is JWT?

**JSON Web Token (JWT)** is a secure way to transmit information between parties as a JSON object. It's commonly used for **authentication** and **authorization** in web applications.

Think of JWT as a **digital passport** - once you log in, you receive a token (passport) that proves who you are for every subsequent request.

---

## JWT Structure

A JWT consists of **three parts** separated by dots (`.`):

```
xxxxx.yyyyy.zzzzz
```

### 1. Header (xxxxx)
Contains token type and signing algorithm.

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

### 2. Payload (yyyyy)
Contains claims (user data).

```json
{
  "sub": "user@example.com",
  "role": "admin",
  "exp": 1734567890
}
```

### 3. Signature (zzzzz)
Ensures the token hasn't been tampered with.

```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret_key
)
```

### Example JWT Token
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyQGV4YW1wbGUuY29tIiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNzM0NTY3ODkwfQ.signature_here
```

---

## How JWT Works

### 1. User Login Flow
```
1. User sends credentials (email + password)
   ↓
2. Server validates credentials
   ↓
3. Server creates JWT with user info
   ↓
4. Server sends JWT to client
   ↓
5. Client stores JWT (localStorage, cookie, etc.)
```

### 2. Protected Resource Access
```
1. Client sends request with JWT in Authorization header
   ↓
2. Server extracts and validates JWT
   ↓
3. Server checks user permissions
   ↓
4. Server returns requested data (if authorized)
```

---

## JWT in This Project

### Configuration (`core/config.py:48-50`)

```python
# JWT Settings
JWT_SECRET_KEY: str = Field(validation_alias="JWT_SECRET_KEY")
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
```

**What it means**:
- `JWT_SECRET_KEY` - Secret used to sign tokens (from `.env` file)
- `ALGORITHM` - HS256 (HMAC with SHA-256) for signing
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expires after 30 minutes

---

## Creating JWT Tokens

### Function: `create_access_token()` (`core/jwt.py:16-30`)

```python
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Creates a JWT token with user data"""
    to_encode = data.copy()

    # Add expiration time
    to_encode["exp"] = get_expiration_time(expires_delta=expires_delta)

    # Encode with secret key and algorithm
    encode_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)
    return encode_jwt
```

**What it does**:
1. Takes user data (email, role)
2. Adds expiration time (default 30 minutes)
3. Signs the token with secret key
4. Returns the JWT string

### Expiration Time (`core/jwt.py:33-47`)

```python
def get_expiration_time(expires_delta: timedelta | None) -> datetime:
    """Gets expiration time for JWT token"""
    if expires_delta:
        return datetime.now() + expires_delta
    else:
        return datetime.now() + timedelta(minutes=30)
```

**Default expiry**: 30 minutes from creation time

---

## Login Endpoint (Real Example)

### User Login Route (`api/routes/user.py:58-75`)

```python
@user.post("/user/login")
async def login_user(
    user_login: UserLogin,
    user_service: AbstractUserService = Depends(get_user_service)
):
    """Authenticates a user and returns a Bearer access token"""
    # Validate credentials and generate token
    access_token = await user_service.login_user(user=user_login)

    return {"access_token": access_token, "token_type": "Bearer"}
```

**Request**:
```json
POST /user/login
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer"
}
```

---

## Decoding and Validating JWT

### Function: `decode_access_token()` (`core/jwt.py:50-93`)

```python
def decode_access_token(token: str) -> TokenData:
    """Decodes incoming JWT token"""
    try:
        # Decode token using secret key
        payload: dict = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        # Extract user data
        email: str = payload.get("sub", "")
        role: str = payload.get("role", "")

        # Validate required fields
        if email is None:
            raise AuthenticationException(message="Invalid token: missing email")

        if role is None:
            raise AuthenticationException(message="Invalid token: missing role")

        return TokenData(email=email, role=role)

    except JWTError:
        raise AuthenticationException(message="Invalid or expired token")
```

**What it does**:
1. Decodes the JWT using the secret key
2. Extracts user email and role from payload
3. Validates that required fields exist
4. Returns `TokenData` object
5. Raises exception if token is invalid/expired

**TokenData Schema** (`schema/token.py:15-21`):
```python
class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None
```

---

## Protected Endpoints (Authorization)

### Role-Based Access Control (RBAC)

The `@required_roles()` decorator restricts access based on user roles.

### Decorator: `required_roles()` (`core/jwt.py:96-159`)

```python
@required_roles(UserRole.MANAGER, UserRole.ADMIN)
async def some_protected_endpoint(request: Request):
    # Only MANAGER and ADMIN can access this
    pass
```

**How it works**:
1. Extracts JWT from `Authorization` header
2. Validates the token format (`Bearer <token>`)
3. Decodes the token to get user info
4. Checks if user's role is in allowed roles
5. Attaches user info to request object
6. Allows/denies access

### Real Example: Get All Users (`api/routes/user.py:78-100`)

```python
@user.get("/user/all", response_model=WrapperUserResponse)
@required_roles(UserRole.MANAGER, UserRole.ADMIN, UserRole.STAFF)
async def get_all_users(
    request: Request,
    user_service: AbstractUserService = Depends(get_user_service)
):
    """Retrieves a list of all users - requires authentication"""
    # User email is attached to request by decorator
    current_user_email = request.state.email

    all_users = await user_service.get_users(user_email=current_user_email)
    return {"status": "success", "message": {"users": all_users}}
```

**Request**:
```http
GET /user/all
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**What happens**:
1. `@required_roles` decorator runs first
2. Extracts and validates JWT
3. Checks if user role is MANAGER, ADMIN, or STAFF
4. If authorized, attaches email to `request.state.email`
5. Endpoint function executes with authenticated user

---

## Authorization Flow (Step-by-Step)

### Function: `verify_scheme_and_return_token()` (`core/jwt.py:249-284`)

```python
def verify_scheme_and_return_token(authorization: str) -> str:
    """Verifies Bearer scheme and extracts token"""
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise AuthenticationException(message="Only Bearer scheme is supported")
    except ValueError:
        raise AuthenticationException(
            message="Authorization header must be in format 'Bearer <token>'"
        )
    return token
```

**Expected format**: `Bearer <jwt_token>`

### Complete Authorization Process

1. **Extract Authorization Header** (`jwt.py:198-222`)
```python
authorization = request.headers.get("Authorization")
if not authorization:
    raise AuthenticationException(message="Authorization header missing")
```

2. **Verify Bearer Scheme** (`jwt.py:249-284`)
```python
scheme, token = authorization.split()
if scheme.lower() != "bearer":
    raise AuthenticationException()
```

3. **Decode Token** (`jwt.py:50-93`)
```python
token_data = decode_access_token(token=token)
user_email = token_data.email
user_role = token_data.role
```

4. **Check Role Authorization** (`jwt.py:137-146`)
```python
if user_role not in UserRole.get_values(roles=allowed_roles):
    raise AuthenticationException(message="Unauthorized")
```

5. **Attach User Info to Request** (`jwt.py:148-149`)
```python
request.state.email = user_email
request.state.role = user_role
```

---

## User Roles (RBAC)

### UserRole Enum (`schema/user.py:33-58`)

```python
class UserRole(Enum):
    ADMIN: str = "admin"     # Full access (GET/POST/PUT/PATCH/DELETE)
    MANAGER: str = "manager" # Most access (GET/POST/PUT/PATCH)
    STAFF: str = "staff"     # Read-only (GET)
```

### Permission Matrix

| Endpoint | STAFF | MANAGER | ADMIN |
|----------|-------|---------|-------|
| GET /user/all | ✅ | ✅ | ✅ |
| POST /user/register | ❌ | ✅ | ✅ |
| DELETE /user/{id} | ❌ | ❌ | ✅ |

---

## Development Mode Bypass

### Environment-Based Authentication (`jwt.py:123-153`)

```python
if settings.environment.lower() in {"production", "prod"}:
    # Full JWT validation in production
    authorization = get_authorization_from_request(request=request)
    token = verify_scheme_and_return_token(authorization=authorization)
    token_data = decode_access_token(token=token)
else:
    # Bypass authentication in development
    if request:
        request.state.email = "dev@sample.com"
        request.state.role = "admin"
```

**What it does**:
- **Production**: Full JWT validation required
- **Development**: Bypasses authentication for easier testing
- Controlled by `ENVIRONMENT` variable in `.env`

---

## Complete Flow Example

### 1. User Registration
```http
POST /user/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "role": "manager"
}
```

### 2. User Login
```http
POST /user/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huQGV4YW1wbGUuY29tIiwicm9sZSI6Im1hbmFnZXIiLCJleHAiOjE3MzQ1Njc4OTB9.signature",
  "token_type": "Bearer"
}
```

### 3. Access Protected Resource
```http
GET /user/all
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response** (if authorized):
```json
{
  "status": "success",
  "message": {
    "users": [...]
  }
}
```

---

## Security Features

### 1. Token Expiration
- Tokens expire after 30 minutes (configurable)
- Forces users to re-authenticate periodically
- Reduces risk if token is stolen

### 2. Secret Key
- JWT signed with `JWT_SECRET_KEY` from `.env`
- Keep secret key secure and private
- Never commit secret key to version control

### 3. HTTPS Only (Production)
- Always use HTTPS in production
- Prevents token interception
- JWT sent in plain text (base64 encoded, not encrypted)

### 4. Role Validation
- Every protected endpoint checks user role
- Prevents privilege escalation
- Least privilege principle

### 5. Token Validation
- Signature verification prevents tampering
- Expiration check prevents replay attacks
- Required fields validation (email, role)

---

## Common JWT Errors

### 1. Missing Authorization Header
```json
{
  "detail": {
    "message": "Authorization header missing",
    "field_errors": [{"field": "authorization", "message": "Authorization header is required"}]
  }
}
```

**Solution**: Include `Authorization: Bearer <token>` header

### 2. Invalid Token Format
```json
{
  "detail": {
    "message": "Invalid authorization header format",
    "field_errors": [{"field": "authorization", "message": "Authorization header must be in format 'Bearer <token>'"}]
  }
}
```

**Solution**: Use format `Bearer <token>` (with space)

### 3. Expired Token
```json
{
  "detail": {
    "message": "Could not validate credentials",
    "field_errors": [{"field": "token", "message": "Invalid or expired token"}]
  }
}
```

**Solution**: Login again to get new token

### 4. Unauthorized Role
```json
{
  "detail": {
    "message": "Unauthorized to perform action, you are a staff",
    "field_errors": [{"field": "role", "message": "Role staff is not authorized for this action"}]
  }
}
```

**Solution**: Contact admin to change your role

---

## Testing JWT in Postman

### Step 1: Login to Get Token
```
POST http://localhost:8000/user/login

Body (JSON):
{
  "email": "user@example.com",
  "password": "password123"
}
```

### Step 2: Copy Access Token from Response

### Step 3: Access Protected Endpoint
```
GET http://localhost:8000/user/all

Headers:
Authorization: Bearer <paste_token_here>
```

---

## Best Practices

### ✅ DO
- Store JWT in httpOnly cookies (most secure)
- Use HTTPS in production
- Set reasonable expiration times (15-30 minutes)
- Validate token on every protected request
- Keep secret key secure and rotate periodically
- Use environment variables for sensitive data

### ❌ DON'T
- Store sensitive data in JWT payload (it's base64, not encrypted)
- Share JWT tokens between users
- Use short or predictable secret keys
- Store tokens in localStorage (XSS vulnerable)
- Forget to validate expiration times
- Commit secret keys to version control

---

## Key Takeaways

1. **JWT = Stateless Authentication** - Server doesn't need to store session data
2. **Three Parts** - Header, Payload, Signature
3. **Bearer Token** - Sent in `Authorization` header as `Bearer <token>`
4. **Expiration** - Tokens expire after configured time (30 minutes default)
5. **RBAC** - Role-Based Access Control using `@required_roles` decorator
6. **Development Bypass** - Authentication skipped in non-production environments

---

## Quick Reference

| Task | Function | File Location |
|------|----------|---------------|
| Create JWT | `create_access_token()` | `core/jwt.py:16` |
| Decode JWT | `decode_access_token()` | `core/jwt.py:50` |
| Protect endpoint | `@required_roles()` | `core/jwt.py:96` |
| Verify Bearer scheme | `verify_scheme_and_return_token()` | `core/jwt.py:249` |
| Get auth header | `get_authorization_from_request()` | `core/jwt.py:198` |
| JWT settings | `Settings` class | `core/config.py:48-50` |
| Token schema | `Token`, `TokenData` | `schema/token.py:6,15` |
| Login endpoint | `/user/login` | `api/routes/user.py:58` |

---

## Summary

JWT provides secure, stateless authentication for your API. Users login once to receive a token, then include that token in subsequent requests. The `@required_roles` decorator validates tokens and enforces role-based access control, ensuring only authorized users can access protected resources.
