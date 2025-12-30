from fastapi import Request, Response
from fastapi.responses import JSONResponse
from typing import Callable, Coroutine, Any
from restmon.state import shutdown_event

async def shutdown_middleware(request: Request, call_next: Callable[[Request], Coroutine[Any, Any, Response]]) -> Response:
    # live всегда отвечает
    if request.url.path == "/health/live":
        return await call_next(request)

    if shutdown_event.is_set():
        return JSONResponse(
            status_code=503,
            content={"status": "shutting_down"},
        )

    return await call_next(request)