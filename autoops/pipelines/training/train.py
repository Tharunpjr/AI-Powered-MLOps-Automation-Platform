#!/usr/bin/env python3
"""
AutoOps Training Pipeline
Main training script for model development and evaluation.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# Add the services directory to the path for imports
sys.path.append(str(Path(__file__).parent.parent.parent / "services" / "model_service"))

from app.model.model import ModelManager


def load_data(data_path: str) -> Tuple[np.ndarray, np.ndarray]:
    """
    Load training data from CSV file.
    
    Args:
        data_path: Path to the CSV data file
        
    Returns:
        Tuple of (features, targets)
    """
    try:
        df = pd.read_csv(data_path)
        print(f"Loaded data with shape: {df.shape}")
        
        # Assume last column is target, rest are features
        features = df.iloc[:, :-1].values
        targets = df.iloc[:, -1].values
        
        print(f"Features shape: {features.shape}")
        print(f"Targets shape: {targets.shape}")
        
        return features, targets
        
    except Exception as e:
        print(f"Error loading data: {e}")
        raise


def create_synthetic_data(n_samples: int = 1000, n_features: int = 4) -> Tuple[np.ndarray, np.ndarray]:
    """
    Create synthetic training data for demonstration.
    
    Args:
        n_samples: Number of samples to generate
        n_features: Number of features
        
    Returns:
        Tuple of (features, targets)
    """
    np.random.seed(42)
    
    # Generate features
    X = np.random.randn(n_samples, n_features)
    
    # Generate targets with some relationship to features
    y = np.sum(X, axis=1) + 0.1 * np.random.randn(n_samples)
    
    print(f"Created synthetic data with shape: {X.shape}")
    return X, y


def train_model(X: np.ndarray, y: np.ndarray, model_type: str = "random_forest") -> Any:
    """
    Train a model on the provided data.
    
    Args:
        X: Training features
        y: Training targets
        model_type: Type of model to train
        
    Returns:
        Trained model
    """
    model_manager = ModelManager()
    
    if model_type == "random_forest":
        model = model_manager.create_random_forest_model(X, y)
    elif model_type == "dummy":
        model = model_manager.create_dummy_model(X, y)
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
    print(f"Trained {model_type} model")
    return model


def evaluate_model(model: Any, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
    """
    Evaluate model performance on test data.
    
    Args:
        model: Trained model
        X_test: Test features
        y_test: Test targets
        
    Returns:
        Dictionary of evaluation metrics
    """
    y_pred = model.predict(X_test)
    
    metrics = {
        "mse": float(mean_squared_error(y_test, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_test, y_pred))),
        "mae": float(mean_absolute_error(y_test, y_pred)),
        "r2": float(r2_score(y_test, y_pred))
    }
    
    return metrics


def save_model_and_metrics(
    model: Any, 
    metrics: Dict[str, float], 
    output_dir: str,
    model_type: str
) -> str:
    """
    Save model and metrics to files.
    
    Args:
        model: Trained model
        metrics: Evaluation metrics
        output_dir: Output directory
        model_type: Type of model
        
    Returns:
        Path to saved model
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Create timestamp for model versioning
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save model
    model_path = output_path / f"model-{timestamp}.pkl"
    model_manager = ModelManager(str(model_path))
    
    # Prepare metadata
    metadata = {
        "version": f"v1.0.{timestamp}",
        "model_type": model_type,
        "training_timestamp": datetime.now().isoformat(),
        "metrics": metrics
    }
    
    success = model_manager.save_model(model, metadata)
    if not success:
        raise RuntimeError("Failed to save model")
    
    # Save metrics separately
    metrics_path = output_path / f"metrics-{timestamp}.json"
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    # Save latest model as model.pkl for serving
    latest_model_path = output_path / "model.pkl"
    model_manager_latest = ModelManager(str(latest_model_path))
    model_manager_latest.save_model(model, metadata)
    
    print(f"Model saved to: {model_path}")
    print(f"Latest model saved to: {latest_model_path}")
    print(f"Metrics saved to: {metrics_path}")
    
    return str(model_path)


def main():
    """Main training pipeline."""
    parser = argparse.ArgumentParser(description="AutoOps Training Pipeline")
    parser.add_argument("--data", type=str, help="Path to training data CSV file")
    parser.add_argument("--out", type=str, default="./models", help="Output directory for model and metrics")
    parser.add_argument("--model-type", type=str, default="random_forest", 
                       choices=["random_forest", "dummy"], help="Type of model to train")
    parser.add_argument("--test-size", type=float, default=0.2, help="Test set size (0.0-1.0)")
    parser.add_argument("--random-state", type=int, default=42, help="Random state for reproducibility")
    parser.add_argument("--synthetic", action="store_true", help="Use synthetic data instead of CSV")
    parser.add_argument("--n-samples", type=int, default=1000, help="Number of synthetic samples")
    parser.add_argument("--n-features", type=int, default=4, help="Number of synthetic features")
    
    args = parser.parse_args()
    
    print("🚀 Starting AutoOps Training Pipeline")
    print(f"Model type: {args.model_type}")
    print(f"Output directory: {args.out}")
    
    try:
        # Load data
        if args.synthetic or not args.data:
            print("Using synthetic data")
            X, y = create_synthetic_data(args.n_samples, args.n_features)
        else:
            print(f"Loading data from: {args.data}")
            X, y = load_data(args.data)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=args.test_size, random_state=args.random_state
        )
        
        print(f"Training set size: {X_train.shape[0]}")
        print(f"Test set size: {X_test.shape[0]}")
        
        # Train model
        print("Training model...")
        model = train_model(X_train, y_train, args.model_type)
        
        # Evaluate model
        print("Evaluating model...")
        metrics = evaluate_model(model, X_test, y_test)
        
        # Print metrics
        print("\n📊 Model Performance Metrics:")
        for metric, value in metrics.items():
            print(f"  {metric.upper()}: {value:.4f}")
        
        # Save model and metrics
        model_path = save_model_and_metrics(model, metrics, args.out, args.model_type)
        
        print(f"\n✅ Training completed successfully!")
        print(f"Model saved to: {model_path}")
        print(f"Metrics: {json.dumps(metrics, indent=2)}")
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
