"""Custom domain exceptions and sanitized HTTP error handlers."""

from typing import Any

from fastapi import Request, status
from fastapi.responses import JSONResponse


class AppException(Exception):
    """Base application exception with status code and safe message."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class ExternalAPIError(AppException):
    """Raised when upstream Open-Meteo or Gemini API fails."""

    def __init__(self, service: str, details: str = "Service unavailable") -> None:
        super().__init__(
            message=f"External {service} error: {details}",
            status_code=status.HTTP_502_BAD_GATEWAY,
        )


class LocationNotFoundError(AppException):
    """Raised when geocoding fails to resolve a city query."""

    def __init__(self, query: str) -> None:
        super().__init__(
            message=f"Location not found for query: '{query}'",
            status_code=status.HTTP_404_NOT_FOUND,
        )


async def app_exception_handler(
    request: Request,
    exc: AppException,
) -> JSONResponse:
    """Format known domain exceptions into standard JSON."""
    _ = request
    payload: dict[str, Any] = {
        "success": False,
        "error": {
            "type": exc.__class__.__name__,
            "message": exc.message,
            "status_code": exc.status_code,
        },
    }
    return JSONResponse(status_code=exc.status_code, content=payload)


async def generic_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Mask unexpected errors to prevent stack trace leaks."""
    _ = request
    _ = exc
    payload: dict[str, Any] = {
        "success": False,
        "error": {
            "type": "InternalServerError",
            "message": "An unexpected error occurred. Please try again.",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        },
    }
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=payload,
    )
