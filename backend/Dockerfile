# ===========================================
# Backend Dockerfile - Production-Grade
# ===========================================
# Multi-stage build for optimized images
# Non-root user for security
# ===========================================

# ===================
# Builder Stage (Dependencies and dev/prod shared
# ===================
FROM python:3.12-slim-bookworm AS builder

# Set working directory
WORKDIR /app

# Install system dependencies (for psycopg2 (PostgreSQL client)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# ===================
# Development Stage (Hot Reload)
# ===================
FROM builder AS development

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=development
ENV FLASK_APP=run.py

# Copy the entire project
COPY . .

# Expose the Flask dev server port
EXPOSE 5000

# Use Flask dev server with hot reload
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000", "--reload"]


# ===================
# Production Stage (Gunicorn WSGI server
# ===================
FROM python:3.12-slim-bookworm AS production

# Set non-root user
RUN useradd -ms /bin/sh -u 1001 autopsyai
USER autopsyai

# Create workdir and set ownership
RUN mkdir -p /app && chown -R autopsyai:autopsyai /app
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production
ENV PATH="/opt/venv/bin:$PATH"

# Copy venv from builder
COPY --from=builder --chown=autopsyai:autopsyai /opt/venv /opt/venv

# Copy only necessary production files
COPY --chown=autopsyai:autopsyai app/ app/
COPY --chown=autopsyai:autopsyai config.py config.py
COPY --chown=autopsyai:autopsyai wsgi.py wsgi.py

# Switch to non-root user
USER autopsyai

# Expose port
EXPOSE 5000

# Run Gunicorn
CMD ["gunicorn", \
    "--bind", "0.0.0.0:5000", \
    "--workers", "4", \
    "--threads", "2", \
    "--timeout", "120", \
    "--access-logfile", "-", \
    "--error-logfile", "-", \
    "wsgi:app"]
