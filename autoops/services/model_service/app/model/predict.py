"""
AutoOps Model Service - Prediction Interface
Model prediction interface and utilities.
"""

import os
import time
from typing import List, Dict, Any, Optional
import numpy as np

from app.model.model import ModelManager


class ModelPredictor:
    """Handles model predictions and inference operations."""
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the model predictor.
        
        Args:
            model_path: Path to the model file (optional)
        """
        if model_path is None:
            # Try different possible paths
            possible_paths = [
                os.getenv("MODEL_PATH", "../../models/model.pkl"),
                "../../models/model.pkl",
                "../../../models/model.pkl",
                "models/model.pkl",
                "/app/models/model.pkl"
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    model_path = path
                    break
            else:
                model_path = possible_paths[0]  # Use default if none found
        
        self.model_manager = ModelManager(model_path)
        self.model_loaded = False
        self._load_model()
    
    def _load_model(self) -> bool:
        """
        Load the model from storage.
        
        Returns:
            True if model loaded successfully, False otherwise
        """
        self.model_loaded = self.model_manager.load_model()
        return self.model_loaded
    
    def predict(self, features: List[float]) -> float:
        """
        Make a prediction using the loaded model.
        
        Args:
            features: List of feature values for prediction
            
        Returns:
            Prediction value
            
        Raises:
            ValueError: If model is not loaded or features are invalid
        """
        if not self.model_loaded:
            raise ValueError("Model not loaded")
        
        if not features:
            raise ValueError("Features list cannot be empty")
        
        try:
            # Convert to numpy array and reshape for prediction
            features_array = np.array(features).reshape(1, -1)
            
            # Make prediction
            model = self.model_manager.get_model()
            if model is None:
                raise ValueError("Model is None")
            
            prediction = model.predict(features_array)[0]
            return float(prediction)
            
        except Exception as e:
            raise ValueError(f"Prediction failed: {str(e)}")
    
    def batch_predict(self, features_list: List[List[float]]) -> List[float]:
        """
        Make batch predictions for multiple feature vectors.
        
        Args:
            features_list: List of feature vectors
            
        Returns:
            List of predictions
            
        Raises:
            ValueError: If model is not loaded or features are invalid
        """
        if not self.model_loaded:
            raise ValueError("Model not loaded")
        
        if not features_list:
            raise ValueError("Features list cannot be empty")
        
        try:
            # Convert to numpy array
            features_array = np.array(features_list)
            
            # Make predictions
            model = self.model_manager.get_model()
            if model is None:
                raise ValueError("Model is None")
            
            predictions = model.predict(features_array)
            return [float(p) for p in predictions]
            
        except Exception as e:
            raise ValueError(f"Batch prediction failed: {str(e)}")
    
    def is_model_loaded(self) -> bool:
        """
        Check if model is loaded.
        
        Returns:
            True if model is loaded, False otherwise
        """
        return self.model_loaded and self.model_manager.is_model_loaded()
    
    def get_model_version(self) -> str:
        """
        Get the model version.
        
        Returns:
            Model version string
        """
        info = self.model_manager.get_model_info()
        return info.get("model_version", "unknown")
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get comprehensive model information.
        
        Returns:
            Dictionary containing model information
        """
        return self.model_manager.get_model_info()
    
    def reload_model(self) -> bool:
        """
        Reload the model from storage.
        
        Returns:
            True if model reloaded successfully, False otherwise
        """
        self.model_loaded = self._load_model()
        return self.model_loaded
    
    def get_prediction_stats(self) -> Dict[str, Any]:
        """
        Get prediction statistics and metrics.
        
        Returns:
            Dictionary containing prediction statistics
        """
        info = self.get_model_info()
        
        stats = {
            "model_loaded": self.is_model_loaded(),
            "model_type": info.get("model_type", "unknown"),
            "model_version": info.get("model_version", "unknown"),
            "last_updated": info.get("last_updated", "unknown"),
            "model_path": info.get("model_path", "unknown")
        }
        
        return stats
    
    def validate_features(self, features: List[float]) -> bool:
        """
        Validate feature vector for prediction.
        
        Args:
            features: List of feature values
            
        Returns:
            True if features are valid, False otherwise
        """
        if not features:
            return False
        
        try:
            # Check if all values are numeric
            for value in features:
                float(value)
            
            # Check for reasonable number of features
            if len(features) < 1 or len(features) > 1000:
                return False
            
            return True
            
        except (ValueError, TypeError):
            return False
    
    def get_model_capabilities(self) -> Dict[str, Any]:
        """
        Get model capabilities and requirements.
        
        Returns:
            Dictionary containing model capabilities
        """
        if not self.is_model_loaded():
            return {
                "model_loaded": False,
                "capabilities": {}
            }
        
        model = self.model_manager.get_model()
        if model is None:
            return {
                "model_loaded": False,
                "capabilities": {}
            }
        
        capabilities = {
            "model_loaded": True,
            "model_type": type(model).__name__,
            "supports_batch_prediction": True,
            "supports_probability": hasattr(model, 'predict_proba'),
            "supports_feature_importance": hasattr(model, 'feature_importances_'),
            "max_features": 1000,  # Reasonable default
            "min_features": 1
        }
        
        return capabilities
