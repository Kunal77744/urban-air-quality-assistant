"""Security middleware, response headers, and rate limiter."""

import time
from collections import defaultdict
from collections.abc import Awaitable, Callable

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse

from core.config import get_settings

_request_timestamps: dict[str, list[float]] = defaultdict(list)


async def security_headers_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """Inject strict security and privacy response headers."""
    response: Response = await call_next(request)
    headers = response.headers
    headers["X-Content-Type-Options"] = "nosniff"
    headers["X-Frame-Options"] = "DENY"
    headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
    headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'; style-src 'self'; "
        "img-src 'self' data:; connect-src 'self'; frame-ancestors 'none';"
    )
    return response


async def rate_limit_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """Enforce per-client IP rate limits to prevent brute-force and DoS."""
    client_ip = request.client.host if request.client else "127.0.0.1"
    now = time.monotonic()
    limit = get_settings().rate_limit_per_minute

    timestamps = _request_timestamps[client_ip]
    _request_timestamps[client_ip] = [ts for ts in timestamps if now - ts < 60.0]

    if len(_request_timestamps[client_ip]) >= limit:
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"error": "Rate limit exceeded. Try again in a minute."},
        )

    _request_timestamps[client_ip].append(now)
    return await call_next(request)
