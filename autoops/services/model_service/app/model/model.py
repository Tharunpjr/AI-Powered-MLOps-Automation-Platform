"""
AutoOps Model Service - Model Management
Model loading, saving, and management utilities.
"""

import os
import pickle
import json
from datetime import datetime
from typing import Any, Dict, Optional, Union
from pathlib import Path

import numpy as np
from sklearn.base import BaseEstimator
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score


class ModelManager:
    """Manages model loading, saving, and metadata operations."""
    
    def __init__(self, model_path: str = "models/model.pkl"):
        """
        Initialize the model manager.
        
        Args:
            model_path: Path to the model file
        """
        self.model_path = Path(model_path)
        self.metadata_path = self.model_path.parent / "model_metadata.json"
        self.model: Optional[BaseEstimator] = None
        self.metadata: Dict[str, Any] = {}
    
    def load_model(self) -> bool:
        """
        Load model from storage.
        
        Returns:
            True if model loaded successfully, False otherwise
        """
        try:
            if not self.model_path.exists():
                print(f"Model file not found at {self.model_path}")
                return False
            
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            # Load metadata if available
            self._load_metadata()
            
            print(f"Model loaded successfully from {self.model_path}")
            return True
            
        except Exception as e:
            print(f"Failed to load model: {e}")
            return False
    
    def save_model(self, model: BaseEstimator, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Save model to storage.
        
        Args:
            model: The model to save
            metadata: Optional metadata to save with the model
            
        Returns:
            True if model saved successfully, False otherwise
        """
        try:
            # Ensure directory exists
            self.model_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save model
            with open(self.model_path, 'wb') as f:
                pickle.dump(model, f)
            
            # Save metadata
            if metadata is None:
                metadata = {}
            
            metadata.update({
                "saved_at": datetime.now().isoformat(),
                "model_type": type(model).__name__,
                "model_path": str(self.model_path)
            })
            
            self._save_metadata(metadata)
            
            print(f"Model saved successfully to {self.model_path}")
            return True
            
        except Exception as e:
            print(f"Failed to save model: {e}")
            return False
    
    def get_model(self) -> Optional[BaseEstimator]:
        """
        Get the loaded model.
        
        Returns:
            The loaded model or None if not loaded
        """
        return self.model
    
    def is_model_loaded(self) -> bool:
        """
        Check if model is loaded.
        
        Returns:
            True if model is loaded, False otherwise
        """
        return self.model is not None
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get model information and metadata.
        
        Returns:
            Dictionary containing model information
        """
        info = {
            "model_loaded": self.is_model_loaded(),
            "model_path": str(self.model_path),
            "metadata": self.metadata.copy()
        }
        
        if self.model is not None:
            info.update({
                "model_type": type(self.model).__name__,
                "model_version": self.metadata.get("version", "unknown"),
                "last_updated": self.metadata.get("saved_at", "unknown")
            })
        
        return info
    
    def create_dummy_model(self, X: np.ndarray, y: np.ndarray) -> BaseEstimator:
        """
        Create a dummy model for testing purposes.
        
        Args:
            X: Training features
            y: Training targets
            
        Returns:
            Trained dummy model
        """
        model = DummyRegressor(strategy='mean')
        model.fit(X, y)
        return model
    
    def create_random_forest_model(self, X: np.ndarray, y: np.ndarray, **kwargs) -> BaseEstimator:
        """
        Create a random forest model.
        
        Args:
            X: Training features
            y: Training targets
            **kwargs: Additional parameters for RandomForestRegressor
            
        Returns:
            Trained random forest model
        """
        default_params = {
            'n_estimators': 100,
            'random_state': 42,
            'max_depth': 10
        }
        default_params.update(kwargs)
        
        model = RandomForestRegressor(**default_params)
        model.fit(X, y)
        return model
    
    def evaluate_model(self, X: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        """
        Evaluate model performance.
        
        Args:
            X: Test features
            y: Test targets
            
        Returns:
            Dictionary containing evaluation metrics
        """
        if self.model is None:
            raise ValueError("No model loaded")
        
        y_pred = self.model.predict(X)
        
        metrics = {
            "mse": float(mean_squared_error(y, y_pred)),
            "rmse": float(np.sqrt(mean_squared_error(y, y_pred))),
            "r2": float(r2_score(y, y_pred))
        }
        
        return metrics
    
    def _load_metadata(self) -> None:
        """Load model metadata from file."""
        try:
            if self.metadata_path.exists():
                with open(self.metadata_path, 'r') as f:
                    self.metadata = json.load(f)
        except Exception as e:
            print(f"Failed to load metadata: {e}")
            self.metadata = {}
    
    def _save_metadata(self, metadata: Dict[str, Any]) -> None:
        """Save model metadata to file."""
        try:
            with open(self.metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            self.metadata = metadata
        except Exception as e:
            print(f"Failed to save metadata: {e}")
