"""
AutoOps Training Utilities
Utility functions for data processing and model training.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import mean_squared_error, r2_score

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProcessor:
    """Handles data preprocessing and transformation."""
    
    def __init__(self, scaler_type: str = "standard"):
        """
        Initialize data processor.
        
        Args:
            scaler_type: Type of scaler to use ("standard" or "minmax")
        """
        self.scaler_type = scaler_type
        self.scaler = None
        self.feature_names = None
        self.target_name = None
    
    def fit_transform(self, X: np.ndarray, y: np.ndarray = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Fit scaler and transform data.
        
        Args:
            X: Features
            y: Targets (optional)
            
        Returns:
            Tuple of (transformed_features, transformed_targets)
        """
        if self.scaler_type == "standard":
            self.scaler = StandardScaler()
        elif self.scaler_type == "minmax":
            self.scaler = MinMaxScaler()
        else:
            raise ValueError(f"Unknown scaler type: {self.scaler_type}")
        
        X_transformed = self.scaler.fit_transform(X)
        
        if y is not None:
            # For targets, we typically don't scale, but we can if needed
            return X_transformed, y
        
        return X_transformed, None
    
    def transform(self, X: np.ndarray) -> np.ndarray:
        """
        Transform data using fitted scaler.
        
        Args:
            X: Features to transform
            
        Returns:
            Transformed features
        """
        if self.scaler is None:
            raise ValueError("Scaler not fitted. Call fit_transform first.")
        
        return self.scaler.transform(X)
    
    def inverse_transform(self, X: np.ndarray) -> np.ndarray:
        """
        Inverse transform data.
        
        Args:
            X: Transformed features
            
        Returns:
            Original scale features
        """
        if self.scaler is None:
            raise ValueError("Scaler not fitted. Call fit_transform first.")
        
        return self.scaler.inverse_transform(X)


class ModelValidator:
    """Handles model validation and cross-validation."""
    
    def __init__(self, cv_folds: int = 5, random_state: int = 42):
        """
        Initialize model validator.
        
        Args:
            cv_folds: Number of cross-validation folds
            random_state: Random state for reproducibility
        """
        self.cv_folds = cv_folds
        self.random_state = random_state
        self.cv_scores = None
    
    def cross_validate(self, model: Any, X: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
        """
        Perform cross-validation on model.
        
        Args:
            model: Model to validate
            X: Features
            y: Targets
            
        Returns:
            Dictionary containing cross-validation results
        """
        cv = KFold(n_splits=self.cv_folds, shuffle=True, random_state=self.random_state)
        
        # Perform cross-validation
        cv_scores = cross_val_score(model, X, y, cv=cv, scoring='r2')
        
        self.cv_scores = cv_scores
        
        results = {
            "cv_scores": cv_scores.tolist(),
            "cv_mean": float(cv_scores.mean()),
            "cv_std": float(cv_scores.std()),
            "cv_min": float(cv_scores.min()),
            "cv_max": float(cv_scores.max()),
            "cv_folds": self.cv_folds
        }
        
        return results
    
    def validate_model_stability(self, model: Any, X: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
        """
        Validate model stability across different data splits.
        
        Args:
            model: Model to validate
            X: Features
            y: Targets
            
        Returns:
            Dictionary containing stability metrics
        """
        from sklearn.model_selection import train_test_split
        
        stability_scores = []
        
        # Test stability across multiple random splits
        for i in range(10):
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=i
            )
            
            # Train and evaluate
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            score = r2_score(y_test, y_pred)
            stability_scores.append(score)
        
        stability_scores = np.array(stability_scores)
        
        return {
            "stability_scores": stability_scores.tolist(),
            "stability_mean": float(stability_scores.mean()),
            "stability_std": float(stability_scores.std()),
            "stability_min": float(stability_scores.min()),
            "stability_max": float(stability_scores.max())
        }


class ExperimentTracker:
    """Tracks training experiments and results."""
    
    def __init__(self, experiment_dir: str = "./experiments"):
        """
        Initialize experiment tracker.
        
        Args:
            experiment_dir: Directory to store experiment results
        """
        self.experiment_dir = Path(experiment_dir)
        self.experiment_dir.mkdir(parents=True, exist_ok=True)
    
    def create_experiment(self, experiment_name: str = None) -> str:
        """
        Create a new experiment.
        
        Args:
            experiment_name: Name for the experiment
            
        Returns:
            Experiment ID
        """
        if experiment_name is None:
            experiment_name = f"experiment_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        experiment_id = experiment_name
        experiment_path = self.experiment_dir / experiment_id
        experiment_path.mkdir(parents=True, exist_ok=True)
        
        # Create experiment metadata
        metadata = {
            "experiment_id": experiment_id,
            "created_at": datetime.now().isoformat(),
            "status": "created"
        }
        
        with open(experiment_path / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Created experiment: {experiment_id}")
        return experiment_id
    
    def log_experiment_results(
        self, 
        experiment_id: str, 
        results: Dict[str, Any]
    ) -> str:
        """
        Log experiment results.
        
        Args:
            experiment_id: ID of the experiment
            results: Results to log
            
        Returns:
            Path to results file
        """
        experiment_path = self.experiment_dir / experiment_id
        results_file = experiment_path / "results.json"
        
        # Add timestamp to results
        results["logged_at"] = datetime.now().isoformat()
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Logged results for experiment: {experiment_id}")
        return str(results_file)
    
    def get_experiment_history(self) -> List[Dict[str, Any]]:
        """
        Get history of all experiments.
        
        Returns:
            List of experiment metadata
        """
        experiments = []
        
        for experiment_dir in self.experiment_dir.iterdir():
            if experiment_dir.is_dir():
                metadata_file = experiment_dir / "metadata.json"
                if metadata_file.exists():
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                        experiments.append(metadata)
        
        return sorted(experiments, key=lambda x: x["created_at"], reverse=True)


def load_data_with_validation(
    data_path: str, 
    target_column: str = None
) -> Tuple[np.ndarray, np.ndarray, List[str]]:
    """
    Load and validate data with proper error handling.
    
    Args:
        data_path: Path to data file
        target_column: Name of target column (if None, uses last column)
        
    Returns:
        Tuple of (features, targets, feature_names)
    """
    try:
        df = pd.read_csv(data_path)
        logger.info(f"Loaded data with shape: {df.shape}")
        
        # Validate data
        if df.empty:
            raise ValueError("Data file is empty")
        
        if df.isnull().any().any():
            logger.warning("Data contains missing values")
        
        # Determine target column
        if target_column is None:
            target_column = df.columns[-1]
        
        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not found in data")
        
        # Split features and target
        feature_columns = [col for col in df.columns if col != target_column]
        X = df[feature_columns].values
        y = df[target_column].values
        
        logger.info(f"Features shape: {X.shape}, Target shape: {y.shape}")
        
        return X, y, feature_columns
        
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise


def save_training_artifacts(
    model: Any,
    metrics: Dict[str, Any],
    experiment_id: str,
    output_dir: str
) -> Dict[str, str]:
    """
    Save all training artifacts.
    
    Args:
        model: Trained model
        metrics: Training metrics
        experiment_id: Experiment ID
        output_dir: Output directory
        
    Returns:
        Dictionary of saved file paths
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    artifacts = {}
    
    # Save model
    model_file = output_path / f"model_{experiment_id}.pkl"
    import pickle
    with open(model_file, 'wb') as f:
        pickle.dump(model, f)
    artifacts["model"] = str(model_file)
    
    # Save metrics
    metrics_file = output_path / f"metrics_{experiment_id}.json"
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f, indent=2)
    artifacts["metrics"] = str(metrics_file)
    
    # Save experiment info
    experiment_file = output_path / f"experiment_{experiment_id}.json"
    experiment_info = {
        "experiment_id": experiment_id,
        "timestamp": datetime.now().isoformat(),
        "metrics": metrics
    }
    with open(experiment_file, 'w') as f:
        json.dump(experiment_info, f, indent=2)
    artifacts["experiment"] = str(experiment_file)
    
    logger.info(f"Saved training artifacts for experiment: {experiment_id}")
    return artifacts
