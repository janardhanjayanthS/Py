# Docker Compose Guide

## What is Docker Compose?

**Docker Compose** is a tool for defining and running multi-container Docker applications. Instead of manually starting each container, you define all services in a single YAML file and start everything with one command.

**Official Documentation**: [https://docs.docker.com/compose/](https://docs.docker.com/compose/)

---

## Why Use Docker Compose?

1. **Single Configuration File**: Define all services in one place
2. **Easy Setup**: Start entire application with one command
3. **Consistent Environment**: Same setup across all machines
4. **Service Dependencies**: Automatically start services in correct order
5. **Networking**: Services can communicate using service names
6. **Volume Management**: Persist data across container restarts

---

## Project Architecture

This project uses Docker Compose to run two services:

```
┌─────────────────────────────────────┐
│         Docker Compose              │
│                                     │
│  ┌──────────────┐  ┌─────────────┐ │
│  │   Database   │  │   Project   │ │
│  │  (postgres)  │◄─┤  (FastAPI)  │ │
│  │   Port 5432  │  │  Port 5003  │ │
│  └──────────────┘  └─────────────┘ │
│         │                  │        │
│    ┌────▼──────────────────▼────┐  │
│    │   Shared Network           │  │
│    └────────────────────────────┘  │
└─────────────────────────────────────┘
```

---

## Docker Compose File Structure

The `docker-compose.yaml` file has four main sections:

```yaml
services:        # Define containers to run
  db:           # Database service
  project:      # Application service

secrets:        # Sensitive data management
  db_password:  # Database password

volumes:        # Persistent data storage
  pgdata:       # PostgreSQL data
```

---

## Detailed Configuration Breakdown

### 1. Services Section

Services are the containers that make up your application.

#### Database Service (`db`)

```yaml
services:
  db:
    image: postgres:16
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: inventory_manager
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d inventory_manager"]
      interval: 5s
      timeout: 5s
      retries: 5
```

**Line-by-Line Explanation:**

##### `image: postgres:16`
- **What it does**: Uses official PostgreSQL version 16 image from Docker Hub
- **Why**: PostgreSQL is the database for storing application data
- **Alternative**: Could use `postgres:15` or `postgres:latest`

##### `ports: - "5432:5432"`
- **What it does**: Maps port 5432 on host to port 5432 in container
- **Format**: `"HOST_PORT:CONTAINER_PORT"`
- **Why**: Allows accessing database from host machine (e.g., for debugging)
- **Example**: Connect with `psql -h localhost -p 5432 -U postgres`

##### `environment:`
Environment variables configure the PostgreSQL container:

- **`POSTGRES_DB: inventory_manager`**
  - Creates database named "inventory_manager" on startup
  - Application connects to this database

- **`POSTGRES_USER: postgres`**
  - Sets database username to "postgres"
  - Default PostgreSQL superuser

- **`POSTGRES_PASSWORD_FILE: /run/secrets/db_password`**
  - Reads password from secrets file (secure method)
  - Instead of hardcoding password in YAML

##### `secrets: - db_password`
- **What it does**: Mounts secret file into container at `/run/secrets/db_password`
- **Why**: Keeps sensitive data out of version control
- **Security**: Password never appears in docker-compose.yaml

##### `volumes: - pgdata:/var/lib/postgresql/data`
- **What it does**: Persists database data to named volume `pgdata`
- **Why**: Data survives container restarts and deletions
- **Path**: `/var/lib/postgresql/data` is where PostgreSQL stores data
- **Without this**: All data would be lost when container stops

##### `healthcheck:`
Health checks verify the database is ready before starting dependent services:

```yaml
test: ["CMD-SHELL", "pg_isready -U postgres -d inventory_manager"]
interval: 5s
timeout: 5s
retries: 5
```

- **`test`**: Command to check if database is ready
  - `pg_isready`: PostgreSQL utility to check connection
  - `-U postgres`: Check as postgres user
  - `-d inventory_manager`: Check specific database

- **`interval: 5s`**: Run health check every 5 seconds
- **`timeout: 5s`**: Wait max 5 seconds for response
- **`retries: 5`**: Try 5 times before marking unhealthy

**Why needed?**: Database takes time to start. Application should wait until database is ready.

---

#### Project Service (`project`)

```yaml
project:
  build: ./project
  ports:
    - "5003:5003"
  secrets:
    - db_password
  env_file:
    - ./project/.env
  depends_on:
    db:
      condition: service_healthy
  environment:
    DB_HOST: db
```

**Line-by-Line Explanation:**

##### `build: ./project`
- **What it does**: Builds Docker image from Dockerfile in `./project` directory
- **Why**: Custom application code needs to be containerized
- **Process**: 
  1. Reads `./project/Dockerfile`
  2. Builds image with application code
  3. Creates container from image

##### `ports: - "5003:5003"`
- **What it does**: Maps port 5003 on host to port 5003 in container
- **Why**: Access FastAPI application at `http://localhost:5003`
- **Example**: API endpoints available at `http://localhost:5003/docs`

##### `secrets: - db_password`
- **What it does**: Mounts database password secret into container
- **Why**: Application needs password to connect to database
- **Access**: Application reads from `/run/secrets/db_password`

##### `env_file: - ./project/.env`
- **What it does**: Loads environment variables from `.env` file
- **Why**: Configuration like JWT secret, environment name, etc.
- **Example `.env` contents**:
  ```
  ENVIRONMENT=production
  JWT_SECRET_KEY=your_secret_key_here
  ```

##### `depends_on:`
Defines service dependencies:

```yaml
depends_on:
  db:
    condition: service_healthy
```

- **`db`**: This service depends on `db` service
- **`condition: service_healthy`**: Wait until database passes health check
- **Why**: Application can't start without database being ready
- **Result**: Docker Compose starts `db` first, waits for health check, then starts `project`

##### `environment: DB_HOST: db`
- **What it does**: Sets environment variable `DB_HOST=db`
- **Why**: Application needs to know database hostname
- **Magic**: Docker Compose creates internal DNS
  - Service name `db` resolves to database container IP
  - Application connects to `db:5432` instead of `localhost:5432`

---

### 2. Secrets Section

```yaml
secrets:
  db_password:
    file: ./secrets/db_password.txt
```

**What it does**: Defines secrets for secure credential management

##### `db_password:`
- **Name**: Secret identifier used in services
- **`file: ./secrets/db_password.txt`**: Path to file containing password

**How it works**:
1. Create file: `./secrets/db_password.txt` with password inside
2. Docker Compose reads file content
3. Mounts content to `/run/secrets/db_password` in containers
4. Application reads password from mounted file

**Security Benefits**:
- ✅ Password not in docker-compose.yaml
- ✅ Password not in environment variables (visible in `docker inspect`)
- ✅ Can add `secrets/` to `.gitignore`
- ✅ Different passwords for dev/staging/production

**Example Setup**:
```bash
# Create secrets directory
mkdir secrets

# Create password file
echo "my_secure_password123" > secrets/db_password.txt

# Protect file permissions
chmod 600 secrets/db_password.txt
```

---

### 3. Volumes Section

```yaml
volumes:
  pgdata:
```

**What it does**: Defines named volumes for persistent data storage

##### `pgdata:`
- **Name**: Volume identifier
- **Purpose**: Store PostgreSQL database files
- **Location**: Managed by Docker (usually `/var/lib/docker/volumes/`)
- **Lifecycle**: Persists even after containers are deleted

**Why Named Volumes?**
- ✅ Data survives container restarts
- ✅ Data survives container deletions
- ✅ Easy to backup and restore
- ✅ Can be shared between containers
- ✅ Docker manages storage location

**Volume Commands**:
```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect sdlc_pgdata

# Remove volume (deletes all data!)
docker volume rm sdlc_pgdata

# Backup volume
docker run --rm -v sdlc_pgdata:/data -v $(pwd):/backup ubuntu tar czf /backup/backup.tar.gz /data
```

---

## How Docker Compose Works

### Starting the Application

```bash
docker-compose up
```

**What happens**:
1. ✅ Reads `docker-compose.yaml`
2. ✅ Creates network for services to communicate
3. ✅ Creates named volume `pgdata`
4. ✅ Pulls `postgres:16` image (if not cached)
5. ✅ Builds `project` image from Dockerfile
6. ✅ Starts `db` service
7. ✅ Runs health checks on `db` every 5 seconds
8. ⏳ Waits for `db` to be healthy
9. ✅ Starts `project` service (after `db` is healthy)
10. ✅ Application is ready!

### Service Communication

Services communicate using service names as hostnames:

```python
# In application code
DATABASE_URL = "postgresql://postgres:password@db:5432/inventory_manager"
#                                              ^^
#                                    Service name, not 'localhost'
```

**How it works**:
- Docker Compose creates internal network
- Each service gets DNS entry with its service name
- `db` resolves to database container's IP address
- Services can communicate without exposing ports to host

---

## Common Docker Compose Commands

### Start Services

```bash
# Start in foreground (see logs)
docker-compose up

# Start in background (detached mode)
docker-compose up -d

# Rebuild images before starting
docker-compose up --build

# Start specific service
docker-compose up db
```

### Stop Services

```bash
# Stop services (keeps containers)
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes (deletes data!)
docker-compose down -v

# Stop and remove containers + images
docker-compose down --rmi all
```

### View Logs

```bash
# View all logs
docker-compose logs

# Follow logs (like tail -f)
docker-compose logs -f

# View logs for specific service
docker-compose logs db
docker-compose logs project

# View last 100 lines
docker-compose logs --tail=100
```

### Service Management

```bash
# List running services
docker-compose ps

# Restart services
docker-compose restart

# Restart specific service
docker-compose restart project

# Execute command in running container
docker-compose exec project bash
docker-compose exec db psql -U postgres -d inventory_manager
```

### Build and Images

```bash
# Build images
docker-compose build

# Build without cache
docker-compose build --no-cache

# Pull latest images
docker-compose pull
```

**Documentation**: [https://docs.docker.com/compose/reference/](https://docs.docker.com/compose/reference/)

---

## Project-Specific Usage

### First Time Setup

```bash
# 1. Create secrets directory and password file
mkdir secrets
echo "your_secure_password" > secrets/db_password.txt

# 2. Create .env file in project directory
cd project
cat > .env << EOF
ENVIRONMENT=production
JWT_SECRET_KEY=your_jwt_secret_key_here
EOF

# 3. Start services
cd ..
docker-compose up -d

# 4. Check if services are running
docker-compose ps

# 5. View logs
docker-compose logs -f
```

### Accessing the Application

Once services are running:

- **FastAPI Application**: [http://localhost:5003](http://localhost:5003)
- **API Documentation**: [http://localhost:5003/docs](http://localhost:5003/docs)
- **Database**: `psql -h localhost -p 5432 -U postgres -d inventory_manager`

### Development Workflow

```bash
# Make code changes in ./project

# Rebuild and restart
docker-compose up --build -d

# View logs to check for errors
docker-compose logs -f project

# Access database for debugging
docker-compose exec db psql -U postgres -d inventory_manager
```

### Troubleshooting

```bash
# Check service status
docker-compose ps

# View detailed logs
docker-compose logs project
docker-compose logs db

# Restart services
docker-compose restart

# Clean restart (removes containers)
docker-compose down
docker-compose up -d

# Nuclear option (removes everything including data!)
docker-compose down -v
docker-compose up --build -d
```

---

## Environment Variables

The application uses environment variables from multiple sources:

### 1. docker-compose.yaml
```yaml
environment:
  DB_HOST: db
```

### 2. .env file
```
ENVIRONMENT=production
JWT_SECRET_KEY=your_secret_key
```

### 3. Secrets
```
/run/secrets/db_password
```

**Priority** (highest to lowest):
1. Environment variables in `docker-compose.yaml`
2. Variables from `env_file`
3. Secrets mounted as files

---

## Networking

Docker Compose automatically creates a network for services:

```
Network Name: sdlc_default (project_name + _default)

Services on network:
├── db (postgres:16)
│   └── Accessible at: db:5432
└── project (FastAPI app)
    └── Accessible at: project:5003
```

**Key Points**:
- Services communicate using service names
- No need to expose ports for inter-service communication
- Only exposed ports are accessible from host machine

---

## Data Persistence

### What Persists

✅ **Database Data** - Stored in `pgdata` volume  
✅ **Secrets** - Stored in `./secrets/` directory  
✅ **Environment Config** - Stored in `./project/.env`

### What Doesn't Persist

❌ **Container Logs** - Lost when container is removed  
❌ **Temporary Files** - Lost when container restarts  
❌ **In-Memory Data** - Lost when container stops

### Backup Strategy

```bash
# Backup database
docker-compose exec db pg_dump -U postgres inventory_manager > backup.sql

# Backup volume
docker run --rm -v sdlc_pgdata:/data -v $(pwd):/backup ubuntu tar czf /backup/pgdata_backup.tar.gz /data

# Restore database
docker-compose exec -T db psql -U postgres inventory_manager < backup.sql
```

---

## Security Best Practices

### 1. Use Secrets for Sensitive Data
✅ Store passwords in secrets files  
❌ Don't hardcode passwords in docker-compose.yaml

### 2. Protect Secret Files
```bash
chmod 600 secrets/db_password.txt
echo "secrets/" >> .gitignore
```

### 3. Use Environment-Specific Configs
- Development: `docker-compose.dev.yaml`
- Production: `docker-compose.prod.yaml`

### 4. Don't Expose Unnecessary Ports
Only expose ports needed for external access:
- ✅ `5003:5003` - API needs external access
- ⚠️ `5432:5432` - Database port (only for debugging)

### 5. Use Specific Image Versions
✅ `postgres:16` - Specific version  
❌ `postgres:latest` - Unpredictable updates

---

## Common Issues and Solutions

### Issue 1: Port Already in Use

**Error**: `Bind for 0.0.0.0:5432 failed: port is already allocated`

**Solution**:
```bash
# Check what's using the port
netstat -ano | findstr :5432

# Stop conflicting service or change port in docker-compose.yaml
ports:
  - "5433:5432"  # Use different host port
```

### Issue 2: Database Not Ready

**Error**: Application crashes with "connection refused"

**Solution**: Health check ensures database is ready. If still failing:
```bash
# Check database logs
docker-compose logs db

# Manually check database
docker-compose exec db pg_isready -U postgres
```

### Issue 3: Volume Permission Issues

**Error**: Permission denied when accessing volume

**Solution**:
```bash
# Remove volume and recreate
docker-compose down -v
docker-compose up -d
```

### Issue 4: Changes Not Reflected

**Error**: Code changes don't appear in running container

**Solution**:
```bash
# Rebuild image
docker-compose up --build -d
```

---

## Summary

Docker Compose simplifies running multi-container applications:

✅ **Two Services**: PostgreSQL database + FastAPI application  
✅ **Automatic Networking**: Services communicate using service names  
✅ **Health Checks**: Application waits for database to be ready  
✅ **Secrets Management**: Secure password storage  
✅ **Data Persistence**: Database data survives restarts  
✅ **Easy Commands**: Start everything with `docker-compose up`

**Key Takeaway**: Docker Compose makes it easy to run complex applications consistently across different environments. One command starts everything, and services are automatically configured to work together.

---

## Additional Resources

- **Docker Compose Docs**: [https://docs.docker.com/compose/](https://docs.docker.com/compose/)
- **Compose File Reference**: [https://docs.docker.com/compose/compose-file/](https://docs.docker.com/compose/compose-file/)
- **Docker Networking**: [https://docs.docker.com/network/](https://docs.docker.com/network/)
- **Docker Volumes**: [https://docs.docker.com/storage/volumes/](https://docs.docker.com/storage/volumes/)
- **Docker Secrets**: [https://docs.docker.com/engine/swarm/secrets/](https://docs.docker.com/engine/swarm/secrets/)
- **PostgreSQL Docker**: [https://hub.docker.com/_/postgres](https://hub.docker.com/_/postgres)
