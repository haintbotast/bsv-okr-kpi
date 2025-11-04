# =============================================================================
# KPI Management System - Backend Dockerfile
# =============================================================================
# Multi-stage build for optimized production image
# =============================================================================

# =============================================================================
# STAGE 1: Builder
# =============================================================================
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /build

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# =============================================================================
# STAGE 2: Runtime
# =============================================================================
FROM python:3.11-slim

# Create app user (security best practice - don't run as root)
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder to appuser's home
COPY --from=builder /root/.local /home/appuser/.local

# Make sure scripts in .local are usable
ENV PATH=/home/appuser/.local/bin:$PATH

# Copy application code
COPY ./app /app/app
COPY ./alembic /app/alembic
COPY ./scripts /app/scripts
COPY ./alembic.ini /app/alembic.ini

# Create data directories
RUN mkdir -p /data/database /data/uploads /data/backups /data/logs

# Set permissions
RUN chown -R appuser:appuser /app /data /home/appuser/.local

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# Default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# =============================================================================
# BUILD INSTRUCTIONS
# =============================================================================
# Build:
#   docker build -t kpi-backend:latest .
#
# Run (development):
#   docker run -d -p 8000:8000 \
#     -v $(pwd)/data:/data \
#     -e SECRET_KEY=your-secret-key \
#     kpi-backend:latest
#
# Run (with reload for development):
#   docker run -d -p 8000:8000 \
#     -v $(pwd):/app \
#     -v $(pwd)/data:/data \
#     -e SECRET_KEY=your-secret-key \
#     kpi-backend:latest \
#     uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
# =============================================================================
