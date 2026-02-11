# Bypassing Authentication in Local Environment

## Overview

In local development, the application bypasses JWT authentication to simplify testing and development. This eliminates the need to generate and manage JWT tokens for every API request.

## How It Works

The authentication bypass is implemented in the `required_roles` decorator located in `src/core/jwt.py`.

### Environment-Based Logic

The decorator checks the application environment and applies different authentication strategies:

```python
if settings.environment.lower() in {"production", "prod"}:
    # Full JWT authentication (production)
    handle_missing_request_object(request=request)
    authorization = get_authorization_from_request(request=request)
    token = verify_scheme_and_return_token(authorization=authorization)
    token_data = decode_access_token(token=token)
    user_email = token_data.email
    user_role = token_data.role
    handle_missing_email_in_request(user_email=user_email)

    # Role authorization check
    if user_role not in UserRole.get_values(roles=allowed_roles):
        raise AuthenticationException(...)

    request.state.email = user_email
    request.state.role = user_role
else:
    # Bypass authentication (local/dev)
    if request:
        request.state.email = "dev@sample.com"
        request.state.role = "admin"
```

### Production Environment
- Validates JWT token from `Authorization` header
- Verifies Bearer scheme
- Decodes token and extracts user email and role
- Checks if user's role is authorized for the endpoint
- Stores authenticated user details in `request.state`

### Local/Dev Environment
- **Skips all JWT validation**
- Sets mock user credentials:
  - Email: `dev@sample.com`
  - Role: `admin`
- Stores mock credentials in `request.state`

## Benefits

1. **Faster Development**: No need to generate tokens for testing
2. **Simplified Testing**: All endpoints accessible without authentication setup
3. **Admin Access**: Mock user has admin role, allowing full API access
4. **No Security Risk**: Only works in non-production environments

## Usage

Simply ensure your environment is NOT set to "production" or "prod":

```bash
# In .env file
ENVIRONMENT=development  # or "local", "dev", etc.
```

All protected endpoints will automatically use the mock credentials without requiring an `Authorization` header.

## Important Notes

- This bypass **only works in non-production environments**
- In production, full JWT authentication is always enforced
- The mock user has `admin` role, granting access to all endpoints
- The environment check is case-insensitive
