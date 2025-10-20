"""
AutoOps Model Service - API Endpoints
Main API endpoints for model predictions and operations.
"""

import time
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field, validator

from app.model.unified_predictor import UnifiedPredictor
from app.utils.telemetry import record_prediction

router = APIRouter()

# Global model predictor instance
model_predictor = None


class PredictionRequest(BaseModel):
    """Request model for prediction endpoint."""
    features: List[float] = Field(
        ..., 
        description="Feature vector for prediction",
        example=[1.0, 2.0, 3.0, 4.0]
    )
    
    @validator('features')
    def validate_features(cls, v):
        if not v:
            raise ValueError('Features list cannot be empty')
        if len(v) < 1:
            raise ValueError('Features list must contain at least one value')
        return v


class PredictionResponse(BaseModel):
    """Response model for prediction endpoint."""
    prediction: float = Field(..., description="Model prediction value")
    model_version: str = Field(..., description="Version of the model used")
    prediction_time: float = Field(..., description="Time taken for prediction in seconds")
    features_count: int = Field(..., description="Number of features provided")


class ModelInfo(BaseModel):
    """Model information response."""
    model_version: str
    model_type: str
    features_expected: int
    is_loaded: bool
    last_updated: str


def get_model_predictor() -> UnifiedPredictor:
    """Dependency to get the model predictor instance."""
    global model_predictor
    if model_predictor is None:
        # Try different model paths
        import os
        possible_paths = [
            "../../models/model.pkl",
            "../../../models/model.pkl", 
            "models/model.pkl"
        ]
        
        model_path = None
        for path in possible_paths:
            if os.path.exists(path):
                model_path = path
                print(f"Found model at: {path}")
                break
        
        if model_path:
            model_predictor = UnifiedPredictor(model_path=model_path, model_type="sklearn")
        else:
            print(f"No model found. Current dir: {os.getcwd()}")
            # Create a dummy predictor for now
            model_predictor = UnifiedPredictor()
            
    return model_predictor


@router.post("/predict", response_model=PredictionResponse)
async def predict(
    request: PredictionRequest,
    predictor: UnifiedPredictor = Depends(get_model_predictor)
) -> PredictionResponse:
    """
    Make a prediction using the trained model.
    
    Args:
        request: Prediction request with features
        predictor: Model predictor instance
        
    Returns:
        Prediction response with result and metadata
    """
    start_time = time.time()
    
    try:
        # Make prediction
        prediction = predictor.predict(request.features)
        prediction_time = time.time() - start_time
        
        # Record metrics
        model_version = predictor.get_model_version()
        record_prediction(model_version, prediction_time)
        
        return PredictionResponse(
            prediction=prediction,
            model_version=model_version,
            prediction_time=prediction_time,
            features_count=len(request.features)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


@router.get("/model/info", response_model=ModelInfo)
async def get_model_info(
    predictor: UnifiedPredictor = Depends(get_model_predictor)
) -> ModelInfo:
    """
    Get information about the loaded model.
    
    Args:
        predictor: Model predictor instance
        
    Returns:
        Model information including version and status
    """
    try:
        info = predictor.get_model_info()
        return ModelInfo(**info)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get model info: {str(e)}"
        )


@router.post("/model/reload")
async def reload_model(
    predictor: UnifiedPredictor = Depends(get_model_predictor)
) -> Dict[str, Any]:
    """
    Reload the model from storage.
    
    Args:
        predictor: Model predictor instance
        
    Returns:
        Reload status and model information
    """
    try:
        success = predictor.reload_model()
        if success:
            info = predictor.get_model_info()
            return {
                "status": "success",
                "message": "Model reloaded successfully",
                "model_info": info
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to reload model"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Model reload failed: {str(e)}"
        )


@router.get("/batch/predict")
async def batch_predict(
    features_list: List[List[float]],
    predictor: UnifiedPredictor = Depends(get_model_predictor)
) -> Dict[str, Any]:
    """
    Make batch predictions for multiple feature vectors.
    
    Args:
        features_list: List of feature vectors
        predictor: Model predictor instance
        
    Returns:
        Batch prediction results
    """
    try:
        start_time = time.time()
        predictions = []
        
        for features in features_list:
            prediction = predictor.predict(features)
            predictions.append(prediction)
        
        batch_time = time.time() - start_time
        
        return {
            "predictions": predictions,
            "count": len(predictions),
            "batch_time": batch_time,
            "model_version": predictor.get_model_version()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Batch prediction failed: {str(e)}"
        )
