"""
AutoOps Unified Model Predictor
Supports both scikit-learn and PyTorch models with a unified interface.
"""

import os
from typing import List, Dict, Any, Optional
import numpy as np

from app.model.model import ModelManager
from app.model.pytorch_model import PyTorchModelManager
from app.model.llm_model import LLMModelManager


class UnifiedPredictor:
    """Unified predictor that handles scikit-learn, PyTorch, and LLM models."""
    
    def __init__(self, model_path: Optional[str] = None, model_type: str = "auto", llm_model: str = "chat"):
        """
        Initialize the unified predictor.
        
        Args:
            model_path: Path to the model file (optional)
            model_type: Type of model ("sklearn", "pytorch", "llm", or "auto")
            llm_model: LLM model type for text tasks ("chat", "sentiment", "qa", etc.)
        """
        self.model_type = model_type
        self.llm_model = llm_model
        self.sklearn_manager = None
        self.pytorch_manager = None
        self.llm_manager = None
        self.active_manager = None
        
        if model_path is None:
            # Try to find models with correct paths
            possible_paths = [
                ("models/model.pkl", "sklearn"),
                ("models/pytorch_model.pt", "pytorch"),
                ("../../models/model.pkl", "sklearn"),
                ("../../models/pytorch_model.pt", "pytorch"),
                ("../../../models/model.pkl", "sklearn"),
                ("../../../models/pytorch_model.pt", "pytorch"),
            ]
            
            for path, mtype in possible_paths:
                if os.path.exists(path):
                    model_path = path
                    if model_type == "auto":
                        self.model_type = mtype
                    print(f"Found model at: {path}")
                    break
            
            if model_path is None:
                print("No model found in any of the expected paths")
                print(f"Current working directory: {os.getcwd()}")
                print("Available files:")
                for root, dirs, files in os.walk("."):
                    for file in files:
                        if file.endswith(('.pkl', '.pt')):
                            print(f"  {os.path.join(root, file)}")
        
        self._load_model(model_path)
    
    def _load_model(self, model_path: Optional[str] = None):
        """Load the appropriate model based on type."""
        if self.model_type == "auto":
            # Try to detect model type from file extension
            if model_path and model_path.endswith('.pt'):
                self.model_type = "pytorch"
            elif model_path and model_path.endswith('.pkl'):
                self.model_type = "sklearn"
            else:
                # Try both
                self._try_load_both(model_path)
                return
        
        if self.model_type == "sklearn":
            self.sklearn_manager = ModelManager(model_path if model_path else "models/model.pkl")
            if self.sklearn_manager.load_model():
                self.active_manager = self.sklearn_manager
                print(f"Loaded scikit-learn model")
        
        elif self.model_type == "pytorch":
            self.pytorch_manager = PyTorchModelManager(model_path if model_path else "models/pytorch_model.pt")
            if self.pytorch_manager.load_model():
                self.active_manager = self.pytorch_manager
                print(f"Loaded PyTorch model")
    
    def _try_load_both(self, model_path: Optional[str] = None):
        """Try to load both model types."""
        # Try sklearn first
        self.sklearn_manager = ModelManager("models/model.pkl")
        if self.sklearn_manager.load_model():
            self.active_manager = self.sklearn_manager
            self.model_type = "sklearn"
            print("Loaded scikit-learn model")
            return
        
        # Try pytorch
        self.pytorch_manager = PyTorchModelManager("models/pytorch_model.pt")
        if self.pytorch_manager.load_model():
            self.active_manager = self.pytorch_manager
            self.model_type = "pytorch"
            print("Loaded PyTorch model")
            return
    
    def predict(self, features: List[float]) -> float:
        """
        Make a prediction using the loaded model.
        
        Args:
            features: List of feature values for prediction
            
        Returns:
            Prediction value
        """
        if self.active_manager is None:
            raise ValueError("No model loaded")
        
        features_array = np.array(features).reshape(1, -1)
        
        if self.model_type == "sklearn":
            model = self.sklearn_manager.get_model()
            prediction = model.predict(features_array)[0]
        
        elif self.model_type == "pytorch":
            prediction = self.pytorch_manager.predict(features_array)[0][0]
        
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
        
        return float(prediction)
    
    def batch_predict(self, features_list: List[List[float]]) -> List[float]:
        """
        Make batch predictions for multiple feature vectors.
        
        Args:
            features_list: List of feature vectors
            
        Returns:
            List of predictions
        """
        if self.active_manager is None:
            raise ValueError("No model loaded")
        
        features_array = np.array(features_list)
        
        if self.model_type == "sklearn":
            model = self.sklearn_manager.get_model()
            predictions = model.predict(features_array)
        
        elif self.model_type == "pytorch":
            predictions = self.pytorch_manager.predict(features_array).flatten()
        
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
        
        return [float(p) for p in predictions]
    
    def is_model_loaded(self) -> bool:
        """Check if a model is loaded."""
        return self.active_manager is not None
    
    def get_model_version(self) -> str:
        """Get the model version."""
        if self.active_manager is None:
            return "unknown"
        
        info = self.active_manager.get_model_info()
        return info.get("model_version", "unknown")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get comprehensive model information."""
        if self.active_manager is None:
            return {
                "model_loaded": False,
                "model_type": "none",
                "features_expected": 0,
                "is_loaded": False,
                "last_updated": "unknown"
            }
        
        info = self.active_manager.get_model_info()
        
        return {
            "model_loaded": True,
            "model_type": self.model_type,
            "model_version": info.get("model_version", "unknown"),
            "features_expected": info.get("model_config", {}).get("input_size", 4),
            "is_loaded": True,
            "last_updated": info.get("last_updated", "unknown"),
            "framework": "PyTorch" if self.model_type == "pytorch" else "scikit-learn",
            "device": info.get("device", "cpu") if self.model_type == "pytorch" else "cpu",
            "parameters": info.get("parameters") if self.model_type == "pytorch" else None
        }
    
    def reload_model(self) -> bool:
        """Reload the model from storage."""
        self._load_model()
        return self.is_model_loaded()
    
    def validate_features(self, features: List[float]) -> bool:
        """Validate feature vector for prediction."""
        if not features:
            return False
        
        try:
            for value in features:
                float(value)
            
            if len(features) < 1 or len(features) > 1000:
                return False
            
            return True
            
        except (ValueError, TypeError):
            return False
