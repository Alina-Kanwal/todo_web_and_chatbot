"""
Hackathon Todo API - FastAPI Application
Main entry point for the backend server.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.core.config import get_settings

settings = get_settings()


def create_application() -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Returns:
        FastAPI: Configured application instance
    """
    application = FastAPI(
        title=settings.app_name,
        description="Multi-user todo application with JWT authentication",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    
    # Configure CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Health check endpoint
    @application.get("/api/health", tags=["Health"])
    async def health_check():
        """
        Health check endpoint for deployment verification.
        
        Returns:
            dict: Service status
        """
        return {
            "status": "healthy",
            "service": settings.app_name,
            "version": "0.1.0",
        }
    
    # Root endpoint
    @application.get("/", tags=["Root"])
    async def root():
        """Root endpoint with API information."""
        return {
            "name": settings.app_name,
            "version": "0.1.0",
            "docs": "/docs",
            "health": "/api/health",
        }
    
    # Include routers
    from src.api.routes.auth import router as auth_router
    from src.api.routes.tasks import router as tasks_router
    from src.api.routes.chat import router as chat_router
    application.include_router(auth_router)
    application.include_router(tasks_router)
    application.include_router(chat_router)

    return application


# Create application instance
app = create_application()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
