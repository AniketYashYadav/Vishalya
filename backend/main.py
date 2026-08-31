from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from backend.core import config
from backend.core.database import init_db
from backend.routers import sync_patients


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database connection pool & tables on startup
    init_db()
    yield


app = FastAPI(
    title=config.PROJECT_NAME,
    description="Vishalya Eco-Syndromic Disease Surveillance System REST API",
    version=config.API_VERSION,
    lifespan=lifespan
)

# CORS configuration for frontend clients (Flutter Mobile App, React Dashboard)
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(sync_patients.router)


@app.get("/", status_code=status.HTTP_200_OK, tags=["System Health"])
def root():
    """
    Root status endpoint.
    """
    return {
        "message": "Vishalya Backend is running",
        "status": "ok"
    }


@app.get("/health", status_code=status.HTTP_200_OK, tags=["System Health"])
def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy"
    }
