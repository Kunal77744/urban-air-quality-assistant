"""Vercel serverless function entrypoint."""

import sys
from pathlib import Path

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
from routes import aqi, geo, plan  # noqa: E402


def _register_middleware(app: FastAPI) -> None:
    """Attach security headers, rate limiting, and CORS."""
    settings = get_settings()
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


def _register_routes(app: FastAPI) -> None:
    """Register API routers with and without /api prefix."""

    @app.get("/api/health", tags=["Health"])
    @app.get("/health", tags=["Health"])
    def direct_health_check() -> dict[str, str]:
        return {"status": "healthy", "version": APP_VERSION, "app": APP_NAME}

    for prefix in ("/api", ""):
        app.include_router(geo.router, prefix=f"{prefix}/geo", tags=["Geocoding"])
        app.include_router(aqi.router, prefix=f"{prefix}/aqi", tags=["AirQuality"])
        app.include_router(plan.router, prefix=f"{prefix}/plan", tags=["Planner"])


def create_app() -> FastAPI:
    """Build Vercel serverless FastAPI app."""
    app = FastAPI(title=APP_NAME, version=APP_VERSION, docs_url=None, redoc_url=None)
    _register_middleware(app)
    _register_routes(app)
    return app


app = create_app()
