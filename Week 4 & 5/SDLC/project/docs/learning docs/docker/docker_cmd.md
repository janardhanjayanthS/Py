# Docker Commands Reference Guide

A comprehensive reference for Docker and Docker Compose commands with concise descriptions and practical examples.

---

## Table of Contents

1. [Quick Reference Table](#quick-reference-table)
2. [Docker Compose Commands](#docker-compose-commands)
3. [Docker Image Commands](#docker-image-commands)
4. [Docker Container Commands](#docker-container-commands)
5. [Docker Volume Commands](#docker-volume-commands)
6. [Docker Network Commands](#docker-network-commands)
7. [Docker System Commands](#docker-system-commands)
8. [Common Command Patterns](#common-command-patterns)
9. [Shell Aliases](#shell-aliases)

---

## Quick Reference Table

| COMMAND                                           | DESCRIPTION                                                              |
| ------------------------------------------------- | ------------------------------------------------------------------------ |
| **DOCKER COMPOSE**                                |
| `docker compose up`                               | Build images (if needed) and start all services in foreground            |
| `docker compose up -d`                            | Build images (if needed) and start all services in background (detached) |
| `docker compose up --build`                       | Force rebuild images and start all services                              |
| `docker compose down`                             | Stop and remove containers, networks (keeps volumes and images)          |
| `docker compose down -v`                          | Stop and remove containers, networks, AND volumes (⚠️ deletes all data)  |
| `docker compose down --rmi all`                   | Stop and remove containers, networks, AND images                         |
| `docker compose build`                            | Build or rebuild services without starting them                          |
| `docker compose build --no-cache`                 | Build images without using cache (clean build)                           |
| `docker compose start`                            | Start existing stopped containers                                        |
| `docker compose stop`                             | Stop running containers without removing them                            |
| `docker compose restart`                          | Restart all services                                                     |
| `docker compose ps`                               | List containers managed by compose                                       |
| `docker compose logs`                             | View output from all services                                            |
| `docker compose logs -f`                          | Follow log output in real-time                                           |
| `docker compose logs -f <service>`                | Follow logs for specific service (e.g., `project`)                       |
| `docker compose exec <service> <cmd>`             | Execute command in running container (e.g., `exec project bash`)         |
| `docker compose run <service> <cmd>`              | Run one-off command in new container                                     |
| `docker compose pull`                             | Pull latest images defined in compose file                               |
| **DOCKER IMAGES**                                 |
| `docker images`                                   | List all images on local system                                          |
| `docker images -a`                                | List all images including intermediate layers                            |
| `docker build -t <name:tag> .`                    | Build image from Dockerfile with tag                                     |
| `docker build --no-cache -t <name:tag> .`         | Build image without using cache                                          |
| `docker pull <image:tag>`                         | Download image from registry                                             |
| `docker push <image:tag>`                         | Upload image to registry                                                 |
| `docker rmi <image>`                              | Remove specific image                                                    |
| `docker rmi $(docker images -q)`                  | Remove all images                                                        |
| `docker image prune`                              | Remove unused images                                                     |
| `docker image prune -a`                           | Remove all images not used by containers                                 |
| `docker tag <source> <target:tag>`                | Create tag for image                                                     |
| `docker inspect <image>`                          | Show detailed information about image                                    |
| `docker history <image>`                          | Show image layer history and sizes                                       |
| **DOCKER CONTAINERS**                             |
| `docker ps`                                       | List running containers                                                  |
| `docker ps -a`                                    | List all containers (running and stopped)                                |
| `docker run <image>`                              | Create and start container from image                                    |
| `docker run -d <image>`                           | Run container in background (detached)                                   |
| `docker run -it <image> <cmd>`                    | Run container interactively with terminal                                |
| `docker run --name <n> <image>`                   | Run container with custom name                                           |
| `docker run -p <host>:<container> <image>`        | Run container with port mapping                                          |
| `docker run -v <host>:<container> <image>`        | Run container with volume mount                                          |
| `docker start <container>`                        | Start stopped container                                                  |
| `docker stop <container>`                         | Stop running container gracefully                                        |
| `docker restart <container>`                      | Restart container                                                        |
| `docker kill <container>`                         | Force stop container immediately                                         |
| `docker rm <container>`                           | Remove stopped container                                                 |
| `docker rm -f <container>`                        | Force remove running container                                           |
| `docker rm $(docker ps -aq)`                      | Remove all stopped containers                                            |
| `docker exec -it <container> <cmd>`               | Execute command in running container (e.g., `bash`)                      |
| `docker logs <container>`                         | View container logs                                                      |
| `docker logs -f <container>`                      | Follow container logs in real-time                                       |
| `docker logs --tail 100 <container>`              | View last 100 log lines                                                  |
| `docker inspect <container>`                      | Show detailed container information                                      |
| `docker stats`                                    | Show live resource usage statistics for all containers                   |
| `docker stats <container>`                        | Show resource usage for specific container                               |
| `docker top <container>`                          | Show running processes in container                                      |
| `docker port <container>`                         | Show port mappings for container                                         |
| `docker container prune`                          | Remove all stopped containers                                            |
| **DOCKER VOLUMES**                                |
| `docker volume ls`                                | List all volumes                                                         |
| `docker volume create <n>`                        | Create named volume                                                      |
| `docker volume inspect <n>`                       | Show detailed volume information                                         |
| `docker volume rm <n>`                            | Remove specific volume                                                   |
| `docker volume prune`                             | Remove all unused volumes (⚠️ deletes data)                              |
| `docker volume prune -f`                          | Force remove unused volumes without confirmation                         |
| **DOCKER NETWORKS**                               |
| `docker network ls`                               | List all networks                                                        |
| `docker network create <n>`                       | Create new network                                                       |
| `docker network inspect <n>`                      | Show detailed network information                                        |
| `docker network connect <network> <container>`    | Connect container to network                                             |
| `docker network disconnect <network> <container>` | Disconnect container from network                                        |
| `docker network rm <n>`                           | Remove specific network                                                  |
| `docker network prune`                            | Remove all unused networks                                               |
| **DOCKER SYSTEM**                                 |
| `docker info`                                     | Display system-wide information                                          |
| `docker version`                                  | Show Docker version information                                          |
| `docker system df`                                | Show Docker disk usage                                                   |
| `docker system prune`                             | Remove unused containers, networks, and images                           |
| `docker system prune -a`                          | Remove all unused containers, networks, images, and build cache          |
| `docker system prune -a --volumes`                | Remove everything including volumes (⚠️ nuclear option)                  |
| **DOCKER REGISTRY**                               |
| `docker login`                                    | Log in to Docker registry                                                |
| `docker logout`                                   | Log out from Docker registry                                             |
| `docker search <term>`                            | Search Docker Hub for images                                             |

---

## Docker Compose Commands

### Lifecycle Management

```bash
# Start services
docker compose up                    # Foreground mode (see logs)
docker compose up -d                 # Detached mode (background)
docker compose up --build            # Force rebuild before starting
docker compose up --force-recreate   # Recreate containers even if config unchanged

# Stop services
docker compose stop                  # Stop containers (can be started again)
docker compose down                  # Stop and remove containers and networks
docker compose down -v               # Stop and remove including volumes
docker compose down --rmi all        # Stop and remove including all images

# Restart services
docker compose restart               # Restart all services
docker compose restart <service>     # Restart specific service
```

### Build Commands

```bash
# Build images
docker compose build                 # Build all services
docker compose build <service>       # Build specific service
docker compose build --no-cache      # Build without cache (clean build)
docker compose build --pull          # Pull base images before building
docker compose build --parallel      # Build images in parallel
```

### Service Management

```bash
# Control individual services
docker compose start <service>       # Start stopped service
docker compose stop <service>        # Stop running service
docker compose pause <service>       # Pause service
docker compose unpause <service>     # Unpause service
docker compose kill <service>        # Force kill service

# Scale services
docker compose up -d --scale <service>=3  # Run 3 instances of service
```

### Logs and Monitoring

```bash
# View logs
docker compose logs                  # All services
docker compose logs <service>        # Specific service
docker compose logs -f               # Follow logs in real-time
docker compose logs -f <service>     # Follow specific service logs
docker compose logs --tail=100       # Last 100 lines
docker compose logs --since 30m      # Logs from last 30 minutes

# Process information
docker compose ps                    # List containers
docker compose ps -a                 # List all containers (including stopped)
docker compose top                   # Display running processes
```

### Execute Commands

```bash
# Run commands in services
docker compose exec <service> <cmd>  # Execute in running container
docker compose exec -it <service> bash    # Interactive bash shell
docker compose exec <service> env    # View environment variables

# Run one-off commands
docker compose run <service> <cmd>   # Run command in new container
docker compose run --rm <service> <cmd>   # Auto-remove after execution
```

### Configuration

```bash
# Validate and view configuration
docker compose config                # Validate and show resolved config
docker compose config --services     # List services
docker compose config --volumes      # List volumes
docker compose ls                    # List running compose projects
```

---

## Docker Image Commands

### Listing Images

```bash
# List images
docker images                        # All images
docker images -a                     # All images including intermediates
docker images <name>                 # Images matching name
docker images --filter "dangling=true"   # Untagged images
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"  # Custom format
```

### Building Images

```bash
# Build from Dockerfile
docker build .                       # Build from current directory
docker build -t <name:tag> .         # Build with tag
docker build -f <file> .             # Build from specific Dockerfile
docker build --no-cache .            # Build without cache
docker build --build-arg KEY=value . # Build with build arguments
docker build --target <stage> .      # Build specific stage (multi-stage)

# Advanced builds
docker buildx build --platform linux/amd64,linux/arm64 .  # Multi-platform
```

### Managing Images

```bash
# Pull/Push images
docker pull <image:tag>              # Download from registry
docker push <image:tag>              # Upload to registry
docker pull --all-tags <image>       # Pull all tags

# Tag images
docker tag <source> <target:tag>     # Create new tag
docker tag myapp:latest myapp:v1.0   # Example

# Remove images
docker rmi <image>                   # Remove image
docker rmi -f <image>                # Force remove
docker rmi $(docker images -q)       # Remove all images

# Inspect images
docker inspect <image>               # Detailed information
docker history <image>               # Layer history
docker image ls --digests            # Show image digests
```

### Cleanup

```bash
# Prune unused images
docker image prune                   # Remove dangling images
docker image prune -a                # Remove all unused images
docker image prune -a --filter "until=24h"  # Remove images older than 24h
```

---

## Docker Container Commands

### Running Containers

```bash
# Basic run
docker run <image>                   # Run container
docker run -d <image>                # Detached mode
docker run --name <n> <image>        # With custom name
docker run --rm <image>              # Auto-remove after exit

# Interactive mode
docker run -it <image> bash          # Interactive with terminal
docker run -it --entrypoint bash <image>  # Override entrypoint

# Port mapping
docker run -p 8080:80 <image>        # Map host:container ports
docker run -P <image>                # Map all exposed ports randomly

# Volume mounting
docker run -v /host/path:/container/path <image>     # Bind mount
docker run -v myvolume:/container/path <image>       # Named volume
docker run -v /container/path <image>                # Anonymous volume

# Environment variables
docker run -e KEY=value <image>      # Single variable
docker run --env-file .env <image>   # From file

# Network
docker run --network <network> <image>   # Specific network
docker run --network host <image>    # Use host network

# Resource limits
docker run -m 512m <image>           # Memory limit
docker run --cpus 2 <image>          # CPU limit
```

### Managing Containers

```bash
# List containers
docker ps                            # Running containers
docker ps -a                         # All containers
docker ps -q                         # Only container IDs
docker ps --filter "status=exited"   # Filter by status

# Start/Stop containers
docker start <container>             # Start stopped container
docker stop <container>              # Stop gracefully (SIGTERM)
docker kill <container>              # Force stop (SIGKILL)
docker restart <container>           # Restart container
docker pause <container>             # Pause processes
docker unpause <container>           # Unpause processes

# Remove containers
docker rm <container>                # Remove stopped container
docker rm -f <container>             # Force remove running container
docker rm $(docker ps -aq)           # Remove all stopped containers
```

### Inspecting Containers

```bash
# View information
docker logs <container>              # View logs
docker logs -f <container>           # Follow logs
docker logs --tail 100 <container>   # Last 100 lines
docker logs --since 30m <container>  # Logs from last 30 minutes

docker inspect <container>           # Detailed info (JSON)
docker top <container>               # Running processes
docker stats <container>             # Resource usage (live)
docker port <container>              # Port mappings
docker diff <container>              # Changes to filesystem
```

### Executing in Containers

```bash
# Execute commands
docker exec <container> <cmd>        # Execute command
docker exec -it <container> bash     # Interactive shell
docker exec -u root <container> <cmd>  # Execute as specific user
docker exec -e VAR=value <container> <cmd>  # With environment variable
```

### Copying Files

```bash
# Copy files
docker cp <container>:/path /host/path   # From container to host
docker cp /host/path <container>:/path   # From host to container
```

### Cleanup

```bash
# Prune containers
docker container prune               # Remove all stopped containers
docker container prune --filter "until=24h"  # Remove stopped containers older than 24h
```

---

## Docker Volume Commands

### Managing Volumes

```bash
# List volumes
docker volume ls                     # List all volumes
docker volume ls --filter dangling=true  # Dangling volumes

# Create volume
docker volume create <name>          # Create named volume
docker volume create --driver local <name>  # With specific driver

# Inspect volume
docker volume inspect <name>         # Detailed information
docker volume inspect <name> --format '{{.Mountpoint}}'  # Get mount point

# Remove volume
docker volume rm <name>              # Remove volume
docker volume rm $(docker volume ls -q)  # Remove all volumes

# Cleanup
docker volume prune                  # Remove unused volumes
docker volume prune -f               # Force without confirmation
```

### Backup and Restore

```bash
# Backup volume to tar file
docker run --rm \
  -v <volume>:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/backup.tar.gz -C /data .

# Restore volume from tar file
docker run --rm \
  -v <volume>:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/backup.tar.gz -C /data

# Copy volume to another volume
docker run --rm \
  -v <source-volume>:/source \
  -v <target-volume>:/target \
  alpine sh -c "cp -av /source/. /target/"
```

---

## Docker Network Commands

### Managing Networks

```bash
# List networks
docker network ls                    # List all networks
docker network ls --filter driver=bridge  # Filter by driver

# Create network
docker network create <name>         # Create bridge network
docker network create --driver bridge <name>  # Explicit driver
docker network create --subnet 172.20.0.0/16 <name>  # With subnet
docker network create --internal <name>  # Internal network (no external access)

# Inspect network
docker network inspect <name>        # Detailed information
docker network inspect <name> --format '{{json .Containers}}'  # Connected containers

# Connect/Disconnect
docker network connect <network> <container>  # Connect container
docker network disconnect <network> <container>  # Disconnect container

# Remove network
docker network rm <name>             # Remove network
docker network rm $(docker network ls -q)  # Remove all networks

# Cleanup
docker network prune                 # Remove unused networks
```

---

## Docker System Commands

### System Information

```bash
# View information
docker version                       # Docker version
docker info                          # System-wide information
docker system df                     # Disk usage
docker system df -v                  # Verbose disk usage

# Events
docker events                        # Real-time events
docker events --filter 'type=container'  # Filter by type
docker events --since '2024-01-01'   # Events since date
```

### System Cleanup

```bash
# Prune system
docker system prune                  # Remove unused data
docker system prune -a               # Remove all unused data
docker system prune -a --volumes     # Include volumes (⚠️ nuclear option)
docker system prune --filter "until=24h"  # Older than 24 hours

# Space reclamation
docker builder prune                 # Remove build cache
docker builder prune -a              # Remove all build cache
```

---

## Common Command Patterns

### Development Workflow

```bash
# Build and run
docker compose up --build -d         # Build, start detached
docker compose logs -f project       # Follow app logs

# Rebuild single service
docker compose build project         # Rebuild
docker compose up -d project         # Restart

# Quick restart
docker compose restart project       # Restart without rebuilding

# View what's running
docker compose ps                    # List services
docker ps                            # List containers
```

### Debugging Workflow

```bash
# Access container shell
docker compose exec project bash     # If running
docker compose run --rm project bash # One-off container

# Check logs
docker compose logs -f project       # Follow logs
docker compose logs --tail 100 project  # Last 100 lines

# Check environment
docker compose exec project env      # Environment variables
docker compose exec project printenv DATABASE_URL  # Specific variable

# Check network
docker network inspect sdlc_default  # Network details
docker inspect sdlc-app-1 | grep IPAddress  # Container IP

# Check resources
docker stats                         # All containers
docker stats sdlc-app-1             # Specific container
```

### Database Operations

```bash
# Connect to PostgreSQL
docker compose exec db psql -U postgres -d inventory_manager

# Run SQL commands
docker compose exec db psql -U postgres -c "SELECT version();"

# Execute SQL file
docker compose exec -T db psql -U postgres -d inventory_manager < schema.sql

# Backup database
docker compose exec db pg_dump -U postgres inventory_manager > backup.sql

# Restore database
docker compose exec -T db psql -U postgres inventory_manager < backup.sql

# Check database size
docker compose exec db psql -U postgres -c \
  "SELECT pg_size_pretty(pg_database_size('inventory_manager'));"

# List databases
docker compose exec db psql -U postgres -c "\l"

# List tables
docker compose exec db psql -U postgres -d inventory_manager -c "\dt"
```

### Cleanup Workflows

```bash
# Stop everything
docker compose down                  # Stop and remove containers

# Nuclear option (⚠️ deletes all data)
docker compose down -v               # Remove volumes too
docker system prune -a --volumes     # Clean entire system

# Selective cleanup
docker container prune               # Remove stopped containers
docker image prune                   # Remove dangling images
docker volume prune                  # Remove unused volumes
docker network prune                 # Remove unused networks

# Free up space
docker system df                     # Check space usage
docker system prune -a               # Reclaim space
```

### Image Management

```bash
# Build and tag
docker build -t myapp:latest .
docker build -t myapp:v1.0 .
docker tag myapp:latest myapp:dev

# Push to registry
docker login
docker tag myapp:latest username/myapp:latest
docker push username/myapp:latest

# Multi-platform build
docker buildx create --use
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:latest --push .

# View image details
docker history myapp:latest          # Layer history
docker inspect myapp:latest          # Detailed info
docker images --filter reference=myapp  # All myapp images
```

### Container Operations

```bash
# Run with options
docker run -d \
  --name myapp \
  -p 8080:8080 \
  -e DATABASE_URL=postgres://... \
  -v $(pwd)/data:/app/data \
  --restart unless-stopped \
  myapp:latest

# Copy files
docker cp config.json myapp:/app/    # To container
docker cp myapp:/app/logs ./         # From container

# Monitor container
docker logs -f myapp                 # Follow logs
docker stats myapp                   # Resource usage
docker top myapp                     # Processes

# Backup container
docker commit myapp myapp:backup     # Create image from container
docker save myapp:backup > backup.tar  # Save image to file
docker load < backup.tar             # Load image from file
```

### Network Troubleshooting

```bash
# Check connectivity
docker compose exec project ping db  # Ping database
docker compose exec project nslookup db  # DNS lookup

# View network config
docker network inspect sdlc_default  # Network details
docker inspect project | grep -A 20 NetworkSettings  # Container network

# Test from host
curl http://localhost:5003/health    # Test exposed port

# Run network tools
docker run --rm --network sdlc_default nicolaka/netshoot curl http://db:5432
```

---

## Shell Aliases

Add these to your `~/.bashrc` or `~/.zshrc` for faster Docker commands:

### Docker Compose Aliases

```bash
alias dc='docker compose'
alias dcu='docker compose up'
alias dcud='docker compose up -d'
alias dcub='docker compose up --build'
alias dcubd='docker compose up --build -d'
alias dcd='docker compose down'
alias dcdv='docker compose down -v'
alias dcb='docker compose build'
alias dcl='docker compose logs'
alias dclf='docker compose logs -f'
alias dcp='docker compose ps'
alias dce='docker compose exec'
alias dcr='docker compose run --rm'
alias dcrestart='docker compose restart'
alias dcstop='docker compose stop'
alias dcstart='docker compose start'
```

### Docker Aliases

```bash
alias d='docker'
alias di='docker images'
alias dps='docker ps'
alias dpsa='docker ps -a'
alias drm='docker rm'
alias drmi='docker rmi'
alias dl='docker logs'
alias dlf='docker logs -f'
alias dex='docker exec -it'
alias dst='docker stats'
alias din='docker inspect'
alias dnet='docker network'
alias dvol='docker volume'
```

### Cleanup Aliases

```bash
alias docker-clean='docker system prune -a --volumes -f'
alias docker-clean-containers='docker container prune -f'
alias docker-clean-images='docker image prune -a -f'
alias docker-clean-volumes='docker volume prune -f'
alias docker-clean-networks='docker network prune -f'
alias docker-nuke='docker stop $(docker ps -aq) && docker system prune -a --volumes -f'
```

### Useful Combos

```bash
# Stop all running containers
alias docker-stop-all='docker stop $(docker ps -q)'

# Remove all stopped containers
alias docker-rm-stopped='docker rm $(docker ps -aq -f status=exited)'

# Remove dangling images
alias docker-rmi-dangling='docker rmi $(docker images -f dangling=true -q)'

# Show container IPs
alias docker-ips='docker inspect -f "{{.Name}} - {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" $(docker ps -q)'

# Follow logs of last created container
alias docker-logs-last='docker logs -f $(docker ps -lq)'

# Quick bash into container
dsh() {
  docker exec -it $1 bash
}

# Quick compose exec
dce() {
  docker compose exec $1 bash
}
```

---

## Additional Tips

### Command Output Formatting

```bash
# JSON output
docker inspect <container> --format '{{json .NetworkSettings.Networks}}'

# Specific field
docker inspect <container> --format '{{.State.Status}}'

# Table format
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Custom format
docker images --format "{{.Repository}}:{{.Tag}} - {{.Size}}"
```

### Useful Filters

```bash
# Filter containers
docker ps --filter "status=running"
docker ps --filter "name=project"
docker ps --filter "label=com.docker.compose.project=sdlc"

# Filter images
docker images --filter "dangling=true"
docker images --filter "reference=python:*"

# Filter volumes
docker volume ls --filter "dangling=true"

# Filter networks
docker network ls --filter "driver=bridge"
```

### Batch Operations

```bash
# Stop all containers
docker stop $(docker ps -q)

# Remove all exited containers
docker rm $(docker ps -aq -f status=exited)

# Remove all images with pattern
docker rmi $(docker images 'myapp:*' -q)

# Remove all volumes not used
docker volume rm $(docker volume ls -qf dangling=true)
```

---

## Quick Reference Card

```
╔════════════════════════════════════════════════════════════════╗
║                    DOCKER QUICK REFERENCE                      ║
╠════════════════════════════════════════════════════════════════╣
║ COMPOSE                                                        ║
║  docker compose up -d --build    Build & start detached        ║
║  docker compose down -v          Stop & remove (including vols)║
║  docker compose logs -f          Follow logs                   ║
║  docker compose exec <svc> bash  Shell into service            ║
╠════════════════════════════════════════════════════════════════╣
║ CONTAINERS                                                     ║
║  docker ps                       List running                  ║
║  docker exec -it <id> bash       Shell into container          ║
║  docker logs -f <id>             Follow logs                   ║
║  docker stop <id>                Stop container                ║
╠════════════════════════════════════════════════════════════════╣
║ IMAGES                                                         ║
║  docker images                   List images                   ║
║  docker build -t <name> .        Build image                   ║
║  docker rmi <id>                 Remove image                  ║
╠════════════════════════════════════════════════════════════════╣
║ CLEANUP                                                        ║
║  docker system prune -a          Clean all unused              ║
║  docker container prune          Remove stopped containers     ║
║  docker image prune -a           Remove unused images          ║
║  docker volume prune             Remove unused volumes         ║
╚════════════════════════════════════════════════════════════════╝
```

---

## Emergency Commands

### When Things Go Wrong

```bash
# Container won't stop
docker kill <container>              # Force kill
docker rm -f <container>             # Force remove

# Out of disk space
docker system df                     # Check usage
docker system prune -a --volumes     # Nuclear cleanup

# Can't connect to Docker daemon
sudo systemctl restart docker        # Restart Docker service
sudo usermod -aG docker $USER        # Add user to docker group (then logout/login)

# Port already in use
lsof -i :5003                        # Find process
sudo kill -9 <PID>                   # Kill process

# Container keeps restarting
docker update --restart=no <container>  # Disable restart
docker logs <container>              # Check logs
```

---

## Resources

- [Official Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Hub](https://hub.docker.com/)
- [Docker Cheat Sheet](https://docs.docker.com/get-started/docker_cheatsheet.pdf)
