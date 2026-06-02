from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.auth import router as auth_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Format HTTPExceptions into the standard API Error response format."""
    # If the detail is already formatted as a dict containing success and error, return it directly
    if isinstance(exc.detail, dict) and "error" in exc.detail:
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail,
            headers=exc.headers,
        )
    
    # Otherwise, wrap standard FastAPI HTTPExceptions
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "HTTP_ERROR",
                "message": str(exc.detail),
            }
        },
        headers=exc.headers,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Format RequestValidationErrors (Pydantic validation errors) into standard format."""
    errors = exc.errors()
    # Build a friendly message detailing what fields failed validation
    details = {}
    for err in errors:
        loc = " -> ".join([str(x) for x in err["loc"]])
        details[loc] = err["msg"]
        
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed.",
                "details": details,
            }
        },
    )


# Health check routes
@app.get("/health", tags=["Health"])
async def health_check():
    """Retrieve system health status."""
    return {"status": "ok", "health": "excellent"}


@app.get("/ready", tags=["Health"])
async def ready_check():
    """Retrieve system readiness status."""
    return {"status": "ready"}


@app.get("/live", tags=["Health"])
async def live_check():
    """Retrieve system liveness status."""
    return {"status": "alive"}


# Register auth API router under versioned prefix
app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
