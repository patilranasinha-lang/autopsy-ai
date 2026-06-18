# ===========================================
# Frontend Dockerfile - Production-Grade
# ===========================================
# Multi-stage build: dev server + optimized production (nginx)
# Non-root user for security
# ===========================================

# ===================
# Base Stage
# ===================
FROM node:22-slim AS base

# Set working directory
WORKDIR /app

# Set non-root user
RUN useradd -ms /bin/sh -u 1001 autopsyai
USER autopsyai

# Copy package files first for layer caching
COPY --chown=autopsyai:autopsyai package*.json ./


# ===================
# Development Stage (Vite Dev Server)
# ===================
FROM base AS development

# Install all dependencies (including dev deps)
RUN npm install

# Copy the entire project
COPY --chown=autopsyai:autopsyai . .

# Expose Vite port
EXPOSE 3000

# Run Vite dev server with hot reload
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]


# ===================
# Build Stage (Production)
# ===================
FROM base AS builder

# Install all dependencies
RUN npm install

# Copy the entire project
COPY --chown=autopsyai:autopsyai . .

# Build the React app for production
RUN npm run build


# ===================
# Production Stage (Nginx as web server)
# ===================
FROM nginx:alpine AS production

# Copy custom nginx config
COPY --from=builder /app/nginx.conf /etc/nginx/nginx.conf

# Copy built static files from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose Nginx port
EXPOSE 80

# Healthcheck
HEALTHCHECK --interval=10s --timeout=3s \
  CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

# Run Nginx
CMD ["nginx", "-g", "daemon off;"]
