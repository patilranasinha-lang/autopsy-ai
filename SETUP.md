# Autopsy AI - Setup Guide

Welcome to the Autopsy AI development setup! This guide will get you up and running in minutes.

## Prerequisites

You will need the following installed:
- **Docker** (24.x or later) - [Docker Desktop](https://www.docker.com/get-started)
- **Git** (2.x or later) - [Download Git](https://git-scm.com/downloads)
- **Node.js** (optional, for local development without Docker)

## Quick Start (One-Command Setup)

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd AutopsyAI
   ```

2. **Copy and configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env if you need to change passwords or ports
   ```

3. **Start all services**
   ```bash
   docker compose up --build
   ```

4. **That's it!** Your app is now running:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - Health check: http://localhost:5000/health
   - PostgreSQL: localhost:5432

## Stopping Services

```bash
# Stop containers but keep data
docker compose stop

# Stop and remove containers, but keep volumes
docker compose down

# Stop and remove everything (including data)
docker compose down -v
```

## Development

### Hot Reloading
- Both backend and frontend support hot reloading via Docker volumes!
- Edit files locally, and changes will automatically reflect inside containers!

### Accessing Container Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f db
```

### Running Backend Tests
```bash
# First, exec into the backend container
docker compose exec backend pytest -v
```

## Production Deployment

For production deployment, use `docker-compose.prod.yml`:

1. Copy env vars (ensure production values are used):
   ```bash
   cp .env.example .env
   # Set secure passwords and secrets!
   ```

2. Start production services:
   ```bash
   docker compose -f docker-compose.prod.yml up -d
   ```

## Architecture Overview

### Services
| Service     | Description                          | Port |
|-------------|--------------------------------------|------|
| Frontend    | React + Vite (Dev), Nginx (Prod)    | 3000 |
| Backend API | Flask + Gunicorn                     | 5000 |
| PostgreSQL  | Database                             | 5432 |

### File Structure
```
AutopsyAI/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── models.py
│   │   └── logger.py
│   ├── Dockerfile (multi-stage dev/prod)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── public/
│   ├── Dockerfile (multi-stage dev/prod)
│   └── nginx.conf
├── docker-compose.yml (development)
├── docker-compose.prod.yml (production)
└── .env.example
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   - Check if port 3000/5000/5432 is occupied:
     ```bash
     # On Linux/macOS
     lsof -i :3000
     # On Windows
     netstat -ano | findstr :3000
     ```
   - Change ports in `.env` file!

2. **Database connection errors**
   - Ensure the `db` container is healthy:
     ```bash
     docker compose ps
     ```
   - Check logs: `docker compose logs db`

3. **Changes not reflecting**
   - Restart containers:
     ```bash
     docker compose restart
     ```
   - Rebuild images if dependencies changed:
     ```bash
     docker compose up --build
     ```

4. **Permission denied errors (Docker volumes)**
   - On Linux/macOS: Ensure your user has permissions for Docker!

### Future Scalability

This architecture is designed for future expansion! You can easily add:

- **ML Services** (add as new containers with their own Dockerfile and mount model files)
- **Redis Cache** (add to docker-compose.yml for caching API responses or JWT tokens)
- **Celery Workers** (for background processing)
- **Chrome Extension API** (add as a new service)

Just follow the existing pattern in `docker-compose.yml`!