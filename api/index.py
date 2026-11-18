"""Vercel serverless function entrypoint."""

from pathlib import Path
import sys

# Ensure api directory is on sys.path for local module resolution
API_DIR = Path(__file__).resolve().parent
if str(API_DIR) not in sys.path:
    sys.path.insert(0, str(API_DIR))

from fastapi import FastAPI  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from core.config import get_settings  # noqa: E402
from core.constants import APP_NAME, APP_VERSION  # noqa: E402
from core.errors import AppException, app_exception_handler, generic_exception_handler  # noqa: E402
from core.security import rate_limit_middleware, security_headers_middleware  # noqa: E402
from routes import aqi, geo, health, plan  # noqa: E402


def create_app() -> FastAPI:
    """Build Vercel serverless FastAPI app."""
    settings = get_settings()
    app = FastAPI(title=APP_NAME, version=APP_VERSION, docs_url=None, redoc_url=None)

    app.middleware("http")(security_headers_middleware)
    app.middleware("http")(rate_limit_middleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allowed_origins,
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    app.add_exception_handler(AppException, app_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, generic_exception_handler)

    # Direct health check endpoint
    @app.get("/api/health", tags=["Health"])
    @app.get("/health", tags=["Health"])
    def direct_health_check() -> dict[str, str]:
        return {"status": "healthy", "version": APP_VERSION, "app": APP_NAME}

    # Routes with and without /api prefix
    app.include_router(geo.router, prefix="/api/geo", tags=["Geocoding"])
    app.include_router(aqi.router, prefix="/api/aqi", tags=["AirQuality"])
    app.include_router(plan.router, prefix="/api/plan", tags=["Planner"])

    app.include_router(geo.router, prefix="/geo", tags=["Geocoding"])
    app.include_router(aqi.router, prefix="/aqi", tags=["AirQuality"])
    app.include_router(plan.router, prefix="/plan", tags=["Planner"])

    return app


app = create_app()
