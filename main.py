"""FastAPI application factory, middleware, and router registration."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles

from core.config import get_settings
from core.constants import APP_NAME, APP_VERSION
from core.errors import (
    AppException,
    app_exception_handler,
    generic_exception_handler,
)
from core.logging import logger
from core.security import rate_limit_middleware, security_headers_middleware
from routes import aqi, geo, health, plan


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application startup and shutdown events."""
    _ = app
    logger.info("Starting %s v%s", APP_NAME, APP_VERSION)
    yield
    logger.info("Shutting down %s", APP_NAME)


def _configure_middleware(app: FastAPI, origins: list[str]) -> None:
    """Register security and optimization middlewares."""
    app.middleware("http")(security_headers_middleware)
    app.middleware("http")(rate_limit_middleware)
    app.add_middleware(GZipMiddleware, minimum_size=500)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )


def _register_routes(app: FastAPI) -> None:
    """Register API routers with and without /api prefix."""
    app.include_router(health.router, prefix="/api", tags=["Health"])
    app.include_router(geo.router, prefix="/api/geo", tags=["Geocoding"])
    app.include_router(aqi.router, prefix="/api/aqi", tags=["AirQuality"])
    app.include_router(plan.router, prefix="/api/plan", tags=["Planner"])

    app.include_router(health.router, tags=["Health"])
    app.include_router(geo.router, prefix="/geo", tags=["Geocoding"])
    app.include_router(aqi.router, prefix="/aqi", tags=["AirQuality"])
    app.include_router(plan.router, prefix="/plan", tags=["Planner"])


def create_app() -> FastAPI:
    """Build and configure the FastAPI application."""
    settings = get_settings()
    app = FastAPI(title=APP_NAME, version=APP_VERSION, lifespan=lifespan)

    _configure_middleware(app, settings.cors_allowed_origins)
    app.add_exception_handler(AppException, app_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, generic_exception_handler)
    _register_routes(app)

    static_dir = Path(__file__).resolve().parent / "public"
    if static_dir.exists():
        app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")

    return app


app = create_app()
