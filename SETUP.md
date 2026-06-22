# Autopsy AI Setup Guide

## Prerequisites

- Docker and Docker Compose
- Python 3.10+
- Node.js 18+

## Quick Start (Docker)

The easiest way to get started is using Docker Compose:

```bash
# 1. Clone the repository
git clone https://github.com/your-org/autopsy-ai.git
cd autopsy-ai

# 2. Copy environment file
cp .env.example .env

# 3. Start all services (database, backend, frontend)
docker-compose up --build

# 4. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:5000
# Health check: http://localhost:5000/health
```

## Local Development (Without Docker)

### Backend Setup

1. Create a virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   .\venv\Scripts\activate  # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up PostgreSQL:
   - Install PostgreSQL locally or use Docker:
     ```bash
     docker run -d \
       --name postgres-autopsy \
       -e POSTGRES_USER=postgres \
       -e POSTGRES_PASSWORD=postgres \
       -e POSTGRES_DB=autopsy_ai \
       -p 5432:5432 \
       postgres:16-alpine
     ```

4. Copy environment file:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. Run database migrations:
   ```bash
   flask db upgrade
   ```

6. Start the backend server:
   ```bash
   flask run --debug
   ```

### Frontend Setup

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start the frontend dev server:
   ```bash
   npm run dev
   ```

## Database Migrations

### Create a New Migration
When you change the models, create a migration:
```bash
cd backend
flask db migrate -m "Description of change"
```

### Apply Migrations
```bash
flask db upgrade
```

### Rollback Migrations
```bash
flask db downgrade
```

## API Endpoints

### Users
- `POST /api/users` - Create a new user
- `GET /api/users` - List users (paginated)
- `GET /api/users/<id>` - Get a single user

### Uploads
- `POST /api/uploads` - Create a new upload
- `GET /api/uploads` - List uploads (paginated)
- `GET /api/uploads?user_id=<id>` - Filter uploads by user
- `GET /api/uploads/<id>` - Get a single upload

### Reports
- `POST /api/reports` - Create a new report
- `GET /api/reports` - List reports (paginated)
- `GET /api/reports?user_id=<id>` - Filter reports by user
- `GET /api/reports/<id>` - Get a single report

## Running Tests

### Backend Tests
```bash
cd backend
pytest -v
```

### Coverage Report
```bash
pytest --cov=app --cov-report=term-missing
```

## Architecture Overview

### Backend Structure
```
backend/
├── app/
│   ├── __init__.py       # Application factory
│   ├── models.py         # SQLAlchemy models (User, Upload, Report)
│   ├── repositories/     # Data access layer
│   ├── services/         # Business logic layer
│   ├── routes/           # API endpoints
│   └── logger.py         # Logging configuration
├── migrations/           # Alembic database migrations
├── tests/                # Test suite
└── requirements.txt      # Dependencies
```

### Key Architectural Decisions
1. **Repository Pattern:** Separates data access logic from business logic
2. **Service Layer:** Contains all business logic, uses repositories for data access
3. **Flask-Migrate:** Manages database schema changes
4. **Pagination:** All list endpoints support pagination to handle large datasets
5. **Database Indexes:** Added on frequently filtered columns (username, email, user_id)
6. **Cascading Deletes:** Deleting a user automatically deletes their uploads and reports
