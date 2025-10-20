"""
AutoOps Model Service - Health Check Endpoints
Health and readiness check endpoints for the model service.
"""

import os
import time
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from app.model.predict import ModelPredictor

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    timestamp: str
    service: str
    version: str
    uptime: float


class ReadinessResponse(BaseModel):
    """Readiness check response model."""
    status: str
    model_loaded: bool
    model_version: str
    dependencies: Dict[str, bool]


class LivenessResponse(BaseModel):
    """Liveness check response model."""
    status: str
    timestamp: str
    uptime: float


# Service start time for uptime calculation
service_start_time = time.time()


def get_model_predictor() -> ModelPredictor:
    """Dependency to get the model predictor instance."""
    try:
        return ModelPredictor()
    except Exception:
        return None


@router.get("/", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Basic health check endpoint.
    
    Returns:
        Health status and service information
    """
    uptime = time.time() - service_start_time
    
    return HealthResponse(
        status="healthy",
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        service="AutoOps Model Service",
        version="1.0.0",
        uptime=round(uptime, 2)
    )


@router.get("/ready", response_model=ReadinessResponse)
async def readiness_check(
    predictor: ModelPredictor = Depends(get_model_predictor)
) -> ReadinessResponse:
    """
    Readiness check endpoint to verify service is ready to serve requests.
    
    Args:
        predictor: Model predictor instance
        
    Returns:
        Readiness status and dependency information
    """
    dependencies = {
        "model_loaded": False,
        "model_accessible": False,
        "storage_accessible": True  # Assume storage is accessible
    }
    
    model_loaded = False
    model_version = "unknown"
    
    try:
        if predictor is not None:
            model_loaded = predictor.is_model_loaded()
            if model_loaded:
                model_version = predictor.get_model_version()
                dependencies["model_loaded"] = True
                dependencies["model_accessible"] = True
    except Exception as e:
        print(f"Model readiness check failed: {e}")
    
    # Check if all critical dependencies are ready
    all_ready = all(dependencies.values())
    status = "ready" if all_ready else "not_ready"
    
    if not all_ready:
        raise HTTPException(
            status_code=503,
            detail="Service not ready - dependencies not available"
        )
    
    return ReadinessResponse(
        status=status,
        model_loaded=model_loaded,
        model_version=model_version,
        dependencies=dependencies
    )


@router.get("/live", response_model=LivenessResponse)
async def liveness_check() -> LivenessResponse:
    """
    Liveness check endpoint to verify service is alive.
    
    Returns:
        Liveness status and uptime information
    """
    uptime = time.time() - service_start_time
    
    return LivenessResponse(
        status="alive",
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        uptime=round(uptime, 2)
    )


@router.get("/status")
async def detailed_status(
    predictor: ModelPredictor = Depends(get_model_predictor)
) -> Dict[str, Any]:
    """
    Detailed status endpoint with comprehensive service information.
    
    Args:
        predictor: Model predictor instance
        
    Returns:
        Detailed service status and metrics
    """
    uptime = time.time() - service_start_time
    
    status = {
        "service": "AutoOps Model Service",
        "version": "1.0.0",
        "status": "healthy",
        "uptime_seconds": round(uptime, 2),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "environment": {
            "python_version": os.sys.version,
            "model_path": os.getenv("MODEL_PATH", "/app/models/model.pkl"),
            "log_level": os.getenv("LOG_LEVEL", "INFO")
        }
    }
    
    # Add model information if available
    if predictor is not None:
        try:
            model_info = predictor.get_model_info()
            status["model"] = model_info
        except Exception as e:
            status["model"] = {"error": str(e)}
    
    return status
