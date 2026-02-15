# Docker Environment Configuration Guide

## Overview

This document explains how the inventory manager application handles environment variables and secrets in both local development and Docker containerized environments.

## Architecture Overview

The application uses a multi-layered configuration approach:

1. **Local Development**: Environment variables from `.env` file
2. **Docker Environment**: Combination of `.env` file, Docker secrets, and environment variables
3. **Configuration Management**: Pydantic Settings with multiple validation aliases

## Configuration Flow

```
Local Development:
├── .env file (project/.env)
│   ├── JWT_SECRET_KEY
│   ├── LOG_LEVEL
│   ├── ENVIRONMENT
│   ├── POSTGRESQL_PWD (for local DB)
│   └── DB_HOST (localhost)
└── Settings class reads from .env

Docker Environment:
├── docker-compose.yaml
│   ├── env_file: ./project/.env (non-sensitive vars)
│   ├── environment: DB_HOST=db (override for container)
│   ├── secrets: db_password (PostgreSQL password)
│   └── depends_on: db (wait for PostgreSQL)
├── Docker secrets mounted at /run/secrets/
│   └── db_password (from secrets/db_password.txt)
└── Settings class reads from multiple sources
```

## File Structure

### 1. `.env` File (project/.env)

Contains environment-specific configuration:

```bash
JWT_SECRET_KEY=the-secret-key-for-json-web-token
LOG_LEVEL=WARNING
ENVIRONMENT=prod
POSTGRESQL_PWD=123456          # Used for local development
DB_HOST=localhost              # Used for local development
```

**Purpose:**
- Stores non-sensitive configuration for both local and Docker environments
- Contains sensitive data for local development (POSTGRESQL_PWD)
- In production, sensitive values should be overridden by Docker secrets

### 2. Docker Compose (docker-compose.yaml)

Orchestrates the multi-container application:

```yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: inventory_manager
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password  # Read from secret
    secrets:
      - db_password
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d inventory_manager"]
      interval: 5s
      timeout: 5s
      retries: 5

  project:
    build: ./project
    ports:
      - "5003:5003"
    secrets:
      - db_password                # Mount secret file
    env_file:
      - ./project/.env             # Load .env variables
    depends_on:
      db:
        condition: service_healthy # Wait for DB to be ready
    environment:
      DB_HOST: db                  # Override for Docker network
      POSTGRESQL_PWD: ${POSTGRESQL_PWD:-}  # Optional override

secrets:
  db_password:
    file: ./secrets/db_password.txt  # Source file for secret
```

**Key Features:**
- `env_file`: Loads all variables from `.env`
- `environment`: Overrides specific variables for Docker context
- `secrets`: Mounts sensitive files into `/run/secrets/`
- `depends_on` with `condition`: Ensures DB is ready before starting app

### 3. Configuration Class (project/src/core/config.py)

Handles configuration with Pydantic Settings:

```python
class Settings(BaseSettings, metaclass=Singleton):
    # Database configuration
    postgresql_pwd: str = Field(
        validation_alias=AliasChoices("POSTGRESQL_PWD", "db_password")
    )
    db_host: str = Field(
        default="localhost",
        validation_alias=AliasChoices("DB_HOST", "db_host")
    )

    # Environment
    environment: str = Field(validation_alias="ENVIRONMENT")

    # JWT
    JWT_SECRET_KEY: str = Field(validation_alias="JWT_SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://postgres:{self.postgresql_pwd}@{self.db_host}:5432/inventory_manager"

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,              # Load from .env
        env_file_encoding="utf-8",
        secrets_dir="/run/secrets",     # Read Docker secrets
        env_prefix="",
        extra="ignore",
    )
```

**Key Features:**
- `validation_alias=AliasChoices()`: Allows multiple variable names for the same field
- `secrets_dir="/run/secrets"`: Tells Pydantic to look for secret files
- `env_file=ENV_FILE`: Specifies the .env file location
- Singleton pattern ensures one configuration instance

### 4. Dockerfile (project/Dockerfile)

Builds the application container:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
COPY package ./package

RUN pip3 install --no-cache-dir -r requirements.txt

COPY /src ./src/

EXPOSE 5003

CMD [ "python", "-m", "src.api.main" ]
```

**Note:** The Dockerfile doesn't copy `.env` file because:
- Docker Compose passes environment variables at runtime
- Secrets are mounted by Docker at runtime
- This prevents baking sensitive data into the image

## How It Works

### Local Development Flow

1. Application starts
2. `Settings` class initializes (src/core/config.py:59)
3. Pydantic reads `project/.env` file (specified in config.py:51)
4. Variables are loaded:
   - `JWT_SECRET_KEY` → JWT configuration
   - `POSTGRESQL_PWD` → Database password
   - `DB_HOST=localhost` → Connects to local PostgreSQL
   - `ENVIRONMENT=prod` → Application mode
5. `DATABASE_URL` property generates connection string
6. Application connects to local database

### Docker Environment Flow

1. `docker-compose up` starts services
2. **Database Service (db)**:
   - Reads password from `/run/secrets/db_password`
   - Initializes PostgreSQL with credentials
   - Healthcheck ensures DB is ready
3. **Application Service (project)**:
   - Waits for DB healthcheck to pass
   - Loads variables from `project/.env`
   - Docker mounts `/run/secrets/db_password` (from secrets/db_password.txt)
   - Environment overrides: `DB_HOST=db` (uses Docker service name)
4. `Settings` class initializes:
   - Reads `.env` file for base configuration
   - Checks `/run/secrets/` directory for secret files
   - Uses environment variable overrides
5. Variable resolution (priority order):
   - Environment variables (highest priority)
   - Docker secrets from `/run/secrets/`
   - `.env` file (lowest priority)
6. `postgresql_pwd` field resolution:
   - Looks for `POSTGRESQL_PWD` environment variable first
   - Falls back to `db_password` file in `/run/secrets/`
   - Uses value from `/run/secrets/db_password` in Docker
7. `db_host` field resolution:
   - Uses `DB_HOST=db` from environment override
   - Connects to `db` service via Docker network
8. Application connects to containerized database

## Variable Resolution Priority

Pydantic Settings resolves values in this order (highest to lowest):

1. **Environment variables** (explicitly set in docker-compose environment section)
2. **Docker secrets** (files in `/run/secrets/`)
3. **env_file** (variables from `.env` file)
4. **Default values** (specified in Field(default=...))

### Example: Database Password Resolution

**Local Development:**
```
POSTGRESQL_PWD (from .env) → "123456"
```

**Docker Environment:**
```
1. Check POSTGRESQL_PWD env var → Not set or empty
2. Check /run/secrets/db_password → "123456" (found!)
3. Use this value for postgresql_pwd field
```

### Example: Database Host Resolution

**Local Development:**
```
DB_HOST (from .env) → "localhost"
```

**Docker Environment:**
```
1. Check DB_HOST env var → "db" (found in environment section!)
2. Use this value, override .env
3. db_host = "db"
```

## Security Best Practices

### Local Development
- `.env` file contains all configuration including passwords
- File should be in `.gitignore`
- Acceptable for local development only

### Docker/Production
- **Sensitive data**: Use Docker secrets (mounted files)
- **Non-sensitive config**: Use `.env` file or environment variables
- **Never commit** `secrets/` directory or `.env` with real credentials
- Secrets are mounted at runtime, not baked into images

### Advantages of This Approach

1. **Flexibility**: Same code works locally and in Docker
2. **Security**: Secrets separated from configuration
3. **Override Capability**: Docker can override `.env` values
4. **No Code Changes**: Environment-specific values handled externally
5. **Validation**: Pydantic ensures all required values are present

## Troubleshooting

### Issue: Application can't find environment variables

**Solution:**
1. Check `.env` file exists at `project/.env`
2. Verify `env_file` path in docker-compose.yaml
3. Ensure variables are not commented out
4. Check for typos in variable names

### Issue: Database connection fails in Docker

**Solution:**
1. Verify `DB_HOST=db` in environment section
2. Check database service name matches
3. Ensure `depends_on` with healthcheck is configured
4. Verify secrets file exists: `secrets/db_password.txt`

### Issue: Password not loaded from secret

**Solution:**
1. Check secret is mounted: `docker-compose exec project ls /run/secrets/`
2. Verify `secrets_dir="/run/secrets"` in config
3. Ensure `validation_alias` includes "db_password"
4. Check secret file has no extra whitespace/newlines

### Issue: Works locally but fails in Docker

**Solution:**
1. Check if using `localhost` instead of service name
2. Verify environment overrides in docker-compose.yaml
3. Ensure all required secrets are defined
4. Check file paths are absolute or relative to correct location

## Testing the Configuration

### Local Development
```bash
cd project
python -m src.api.main
# Should connect to localhost:5432
```

### Docker Environment
```bash
# From SDLC directory
docker-compose up --build

# Verify secrets mounted
docker-compose exec project cat /run/secrets/db_password

# Check environment variables
docker-compose exec project env | grep -E "DB_HOST|ENVIRONMENT|JWT"
```

## Summary

This configuration system provides:
- **Seamless transition** between local and containerized environments
- **Security** through Docker secrets for sensitive data
- **Flexibility** with multiple validation aliases and priority resolution
- **Maintainability** with centralized configuration management
- **Type safety** through Pydantic validation

The key insight is that Pydantic Settings automatically handles multiple sources (env files, environment variables, secrets) with a clear priority order, making the same code work in different environments without modification.
