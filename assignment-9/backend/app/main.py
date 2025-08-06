from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.list_routes import router as list_router
from app.api.routes.task_routes import router as task_router
from app.api.routes.auth_routes import router as auth_router
from app.core.config import settings

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="API for a Todo List application",
    version="0.1.0",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers with prefix
app.include_router(auth_router, prefix=settings.API_PREFIX)
app.include_router(list_router, prefix=settings.API_PREFIX)
app.include_router(task_router, prefix=settings.API_PREFIX)

# Root endpoint for health check
@app.get("/")
async def root():
    return {
        "message": "Todo List API is running", 
        "docs": "/docs",
        "status": "healthy"
    }
