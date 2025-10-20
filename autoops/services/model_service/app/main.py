"""
AutoOps Model Service - FastAPI Application
Main entry point for the model serving service.
"""

import os
import time
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

from app.api.endpoints import router as api_router
from app.api.health import router as health_router
from app.utils.telemetry import setup_telemetry, get_metrics

# Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total', 
    'Total HTTP requests', 
    ['method', 'endpoint', 'status_code']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown tasks."""
    # Startup
    setup_telemetry()
    print("🚀 AutoOps Model Service started successfully!")
    yield
    # Shutdown
    print("🛑 AutoOps Model Service shutting down...")


# Create FastAPI application
app = FastAPI(
    title="AutoOps Model Service",
    description="MLOps automation toolkit model serving API",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev
        "http://localhost:3001",  # Alternative port
        "https://*.netlify.app",  # Netlify deployments
        "https://*.vercel.app",   # Vercel deployments
        "*"  # Allow all for development (configure for production)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """Middleware to collect Prometheus metrics."""
    start_time = time.time()
    
    # Process request
    response = await call_next(request)
    
    # Calculate duration
    duration = time.time() - start_time
    
    # Extract metrics
    method = request.method
    endpoint = request.url.path
    status_code = str(response.status_code)
    
    # Record metrics
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, status_code=status_code).inc()
    REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(duration)
    
    return response


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# Include routers
app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(api_router, prefix="/api/v1", tags=["api"])

# Add LLM endpoints
try:
    from app.api.llm_endpoints import router as llm_router
    app.include_router(llm_router, prefix="/api/v1/llm", tags=["llm"])
    print("✅ LLM endpoints loaded")
except ImportError as e:
    print(f"⚠️ LLM endpoints not available: {e}")


@app.get("/")
async def root():
    """Root endpoint with service information."""
    return {
        "service": "AutoOps AI-Powered Model Service",
        "version": "1.0.0",
        "status": "healthy",
        "capabilities": [
            "Traditional ML (scikit-learn)",
            "Deep Learning (PyTorch)", 
            "Large Language Models (LLMs)",
            "Text Generation & Chat",
            "Sentiment Analysis",
            "Question Answering"
        ],
        "endpoints": {
            "health": "/health",
            "metrics": "/metrics",
            "ml_predict": "/api/v1/predict",
            "llm_chat": "/api/v1/llm/chat",
            "llm_generate": "/api/v1/llm/generate",
            "llm_analyze": "/api/v1/llm/analyze",
            "llm_qa": "/api/v1/llm/qa",
            "docs": "/docs"
        },
        "llm_providers": {
            "gemini": "Google Gemini API (recommended)",
            "huggingface": "Hugging Face models (free)"
        },
        "setup": {
            "gemini": "Set GEMINI_API_KEY environment variable",
            "get_gemini_key": "https://makersuite.google.com/app/apikey"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
