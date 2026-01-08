from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time
import logging

from app.api.movies import router as movies_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("assessment-3")

app = FastAPI(title="Simple Movie Manager")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    """Middleware that logs request execution time."""
    start = time.monotonic()
    response = await call_next(request)
    elapsed = time.monotonic() - start
    # add timing header (seconds)
    response.headers["X-Process-Time"] = f"{elapsed:.6f}"
    # log method, path, status and elapsed
    logger.info(f"{request.method} {request.url.path} -> {response.status_code} in {elapsed:.6f}s")
    return response


# Include API routers
app.include_router(movies_router)