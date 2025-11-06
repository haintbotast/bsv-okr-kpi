"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime, timezone
import logging
from pathlib import Path

from app.config import settings
from app.api.v1 import auth, kpis, templates, files, comments, notifications, analytics, admin, upload, preferences
from app.api.v1 import settings as settings_api

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="KPI Management System API",
    docs_url="/docs" if settings.ENABLE_DOCS else None,
    redoc_url="/redoc" if settings.ENABLE_DOCS else None,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return JSONResponse({
        "status": "healthy",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })


# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(kpis.router, prefix="/api/v1/kpis", tags=["KPIs"])
app.include_router(templates.router, prefix="/api/v1/templates", tags=["Templates"])
app.include_router(files.router, prefix="/api/v1", tags=["Files"])
app.include_router(comments.router, prefix="/api/v1", tags=["Comments"])
app.include_router(notifications.router, prefix="/api/v1", tags=["Notifications"])
app.include_router(analytics.router, prefix="/api/v1", tags=["Analytics"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
app.include_router(settings_api.router, prefix="/api/v1/settings", tags=["Settings"])
app.include_router(upload.router, prefix="/api/v1/upload", tags=["Upload"])
app.include_router(preferences.router, prefix="/api/v1/preferences", tags=["Preferences"])

# Mount static files for uploads
UPLOAD_DIR = Path("/data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Database: {settings.DATABASE_URL}")

    # Start background scheduler
    from app.core.scheduler import start_scheduler
    start_scheduler()


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    # Shutdown scheduler
    from app.core.scheduler import shutdown_scheduler
    shutdown_scheduler()

    logger.info("Shutting down application")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
