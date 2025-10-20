#!/usr/bin/env python3
"""
AutoOps PyTorch Training Pipeline
Training script for PyTorch deep learning models.
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
from sklearn.preprocessing import StandardScaler

# Add the services directory to the path for imports
sys.path.append(str(Path(__file__).parent.parent.parent / "services" / "model_service"))

from app.model.pytorch_model import PyTorchModelManager


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
    
    # Generate targets with non-linear relationship
    y = (np.sum(X ** 2, axis=1) + 
         0.5 * np.sin(X[:, 0]) * np.cos(X[:, 1]) + 
         0.1 * np.random.randn(n_samples))
    
    print(f"Created synthetic data with shape: {X.shape}")
    return X, y


def preprocess_data(
    X_train: np.ndarray, 
    X_test: np.ndarray
) -> Tuple[np.ndarray, np.ndarray, StandardScaler]:
    """
    Preprocess data with standardization.
    
    Args:
        X_train: Training features
        X_test: Test features
        
    Returns:
        Tuple of (scaled X_train, scaled X_test, scaler)
    """
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, scaler


def save_model_and_metrics(
    model_manager: PyTorchModelManager,
    metrics: Dict[str, float],
    training_results: Dict[str, Any],
    output_dir: str
) -> str:
    """
    Save model and metrics to files.
    
    Args:
        model_manager: PyTorch model manager with trained model
        metrics: Evaluation metrics
        training_results: Training history and config
        output_dir: Output directory
        
    Returns:
        Path to saved model
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Create timestamp for model versioning
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save model
    model_path = output_path / f"pytorch_model-{timestamp}.pt"
    
    # Prepare metadata
    metadata = {
        "version": f"v1.0.{timestamp}",
        "model_type": "PyTorch",
        "training_timestamp": datetime.now().isoformat(),
        "metrics": metrics,
        "training_config": training_results.get('model_config', {}),
        "final_train_loss": training_results.get('final_train_loss'),
        "final_val_loss": training_results.get('final_val_loss')
    }
    
    success = model_manager.save_model(
        model_manager.model,
        training_results['model_config'],
        metadata
    )
    
    if not success:
        raise RuntimeError("Failed to save model")
    
    # Save metrics separately
    metrics_path = output_path / f"pytorch_metrics-{timestamp}.json"
    with open(metrics_path, 'w') as f:
        json.dump({
            'metrics': metrics,
            'training_history': training_results.get('history', {})
        }, f, indent=2)
    
    # Save latest model as pytorch_model.pt for serving
    latest_model_path = output_path / "pytorch_model.pt"
    model_manager.model_path = latest_model_path
    model_manager.save_model(
        model_manager.model,
        training_results['model_config'],
        metadata
    )
    
    print(f"Model saved to: {model_path}")
    print(f"Latest model saved to: {latest_model_path}")
    print(f"Metrics saved to: {metrics_path}")
    
    return str(model_path)


def main():
    """Main PyTorch training pipeline."""
    parser = argparse.ArgumentParser(description="AutoOps PyTorch Training Pipeline")
    parser.add_argument("--data", type=str, help="Path to training data CSV file")
    parser.add_argument("--out", type=str, default="./models", help="Output directory for model and metrics")
    parser.add_argument("--hidden-sizes", type=int, nargs='+', default=[64, 32], 
                       help="Hidden layer sizes (e.g., --hidden-sizes 128 64 32)")
    parser.add_argument("--epochs", type=int, default=100, help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size")
    parser.add_argument("--learning-rate", type=float, default=0.001, help="Learning rate")
    parser.add_argument("--test-size", type=float, default=0.2, help="Test set size (0.0-1.0)")
    parser.add_argument("--val-size", type=float, default=0.1, help="Validation set size (0.0-1.0)")
    parser.add_argument("--random-state", type=int, default=42, help="Random state for reproducibility")
    parser.add_argument("--synthetic", action="store_true", help="Use synthetic data instead of CSV")
    parser.add_argument("--n-samples", type=int, default=1000, help="Number of synthetic samples")
    parser.add_argument("--n-features", type=int, default=4, help="Number of synthetic features")
    
    args = parser.parse_args()
    
    print("🚀 Starting AutoOps PyTorch Training Pipeline")
    print(f"Hidden sizes: {args.hidden_sizes}")
    print(f"Epochs: {args.epochs}")
    print(f"Batch size: {args.batch_size}")
    print(f"Learning rate: {args.learning_rate}")
    print(f"Output directory: {args.out}")
    
    try:
        # Load data
        if args.synthetic or not args.data:
            print("Using synthetic data")
            X, y = create_synthetic_data(args.n_samples, args.n_features)
        else:
            print(f"Loading data from: {args.data}")
            X, y = load_data(args.data)
        
        # Split data into train, validation, and test
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y, test_size=args.test_size, random_state=args.random_state
        )
        
        val_size_adjusted = args.val_size / (1 - args.test_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp, test_size=val_size_adjusted, random_state=args.random_state
        )
        
        print(f"Training set size: {X_train.shape[0]}")
        print(f"Validation set size: {X_val.shape[0]}")
        print(f"Test set size: {X_test.shape[0]}")
        
        # Preprocess data
        print("Preprocessing data...")
        X_train_scaled, X_val_scaled, scaler = preprocess_data(X_train, X_val)
        X_test_scaled = scaler.transform(X_test)
        
        # Initialize model manager
        model_manager = PyTorchModelManager()
        
        # Train model
        print("Training PyTorch model...")
        training_results = model_manager.train_model(
            X_train_scaled,
            y_train,
            X_val_scaled,
            y_val,
            hidden_sizes=args.hidden_sizes,
            epochs=args.epochs,
            batch_size=args.batch_size,
            learning_rate=args.learning_rate
        )
        
        # Evaluate model
        print("Evaluating model...")
        metrics = model_manager.evaluate_model(X_test_scaled, y_test)
        
        # Print metrics
        print("\n📊 Model Performance Metrics:")
        for metric, value in metrics.items():
            print(f"  {metric.upper()}: {value:.4f}")
        
        print(f"\n📈 Training Results:")
        print(f"  Final Train Loss: {training_results['final_train_loss']:.4f}")
        if training_results['final_val_loss']:
            print(f"  Final Val Loss: {training_results['final_val_loss']:.4f}")
        
        # Save model and metrics
        model_path = save_model_and_metrics(
            model_manager,
            metrics,
            training_results,
            args.out
        )
        
        print(f"\n✅ PyTorch training completed successfully!")
        print(f"Model saved to: {model_path}")
        print(f"Test Metrics: {json.dumps(metrics, indent=2)}")
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
