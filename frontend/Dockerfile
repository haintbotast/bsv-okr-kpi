# =============================================================================
# KPI Management System - Frontend Dockerfile
# =============================================================================
# Multi-stage build for optimized production image
# =============================================================================

# =============================================================================
# STAGE 1: Builder
# =============================================================================
FROM node:20-alpine as builder

# Set working directory
WORKDIR /build

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
# Use npm install if package-lock.json doesn't exist, otherwise use npm ci
RUN if [ -f package-lock.json ]; then \
        npm ci --legacy-peer-deps; \
    else \
        npm install --legacy-peer-deps; \
    fi

# Copy source code
COPY . .

# Build application
RUN npm run build

# =============================================================================
# STAGE 2: Production with Nginx
# =============================================================================
FROM nginx:1.25-alpine

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built files from builder
COPY --from=builder /build/dist /usr/share/nginx/html

# Create non-root user
RUN addgroup -g 101 -S nginx && \
    adduser -S -D -H -u 101 -h /var/cache/nginx -s /sbin/nologin -G nginx -g nginx nginx

# Set permissions
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    chown -R nginx:nginx /etc/nginx/conf.d && \
    touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid

# Switch to non-root user
USER nginx

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]

# =============================================================================
# BUILD INSTRUCTIONS
# =============================================================================
# Build:
#   docker build -t kpi-frontend:latest .
#
# Run:
#   docker run -d -p 80:80 kpi-frontend:latest
#
# Development (with hot reload):
#   Use docker-compose.yml instead
# =============================================================================
