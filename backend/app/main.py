import time
from fastapi import FastAPI, HTTPException, Request, status, Response
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

from app.api.v1.auth import router as auth_router
from app.api.v1.jobs import router as jobs_router
from app.api.v1.workflows import router as workflows_router
from app.api.v1.resumes import router as resumes_router
from app.api.v1.ai import router as ai_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Prometheus metrics setup
HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total number of HTTP requests processed",
    ["method", "endpoint", "status_code"]
)
HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"]
)

@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    path = request.url.path
    if path in ["/metrics", "/health", "/ready", "/live"]:
        return await call_next(request)
        
    start_time = time.time()
    try:
        response = await call_next(request)
        duration = time.time() - start_time
        status_code = str(response.status_code)
        HTTP_REQUESTS_TOTAL.labels(method=request.method, endpoint=path, status_code=status_code).inc()
        HTTP_REQUEST_DURATION_SECONDS.labels(method=request.method, endpoint=path).observe(duration)
        return response
    except Exception as e:
        duration = time.time() - start_time
        HTTP_REQUESTS_TOTAL.labels(method=request.method, endpoint=path, status_code="500").inc()
        HTTP_REQUEST_DURATION_SECONDS.labels(method=request.method, endpoint=path).observe(duration)
        raise e

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


@app.get("/metrics", tags=["Health"])
def metrics():
    """Expose Prometheus metrics."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# Create database tables automatically on startup
@app.on_event("startup")
async def on_startup():
    from app.db.session import engine, Base
    import app.models
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Register auth API router under versioned prefix
app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
app.include_router(jobs_router, prefix=f"{settings.API_V1_STR}/jobs", tags=["Jobs"])
app.include_router(workflows_router, prefix=f"{settings.API_V1_STR}/workflows", tags=["Workflows"])
app.include_router(resumes_router, prefix=f"{settings.API_V1_STR}/resumes", tags=["Resumes"])
app.include_router(ai_router, prefix=f"{settings.API_V1_STR}/ai", tags=["AI"])
