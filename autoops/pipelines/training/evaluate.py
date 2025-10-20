#!/usr/bin/env python3
"""
AutoOps Model Evaluation
Model evaluation and validation utilities.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple

import numpy as np
import pandas as pd
from sklearn.metrics import (
    mean_squared_error, r2_score, mean_absolute_error,
    explained_variance_score, max_error
)

# Add the services directory to the path for imports
sys.path.append(str(Path(__file__).parent.parent.parent / "services" / "model_service"))

from app.model.model import ModelManager


def load_model(model_path: str) -> Any:
    """
    Load a trained model from file.
    
    Args:
        model_path: Path to the model file
        
    Returns:
        Loaded model
    """
    model_manager = ModelManager(model_path)
    if not model_manager.load_model():
        raise ValueError(f"Failed to load model from {model_path}")
    
    return model_manager.get_model()


def load_test_data(data_path: str) -> Tuple[np.ndarray, np.ndarray]:
    """
    Load test data from CSV file.
    
    Args:
        data_path: Path to the test data CSV file
        
    Returns:
        Tuple of (features, targets)
    """
    try:
        df = pd.read_csv(data_path)
        print(f"Loaded test data with shape: {df.shape}")
        
        # Assume last column is target, rest are features
        features = df.iloc[:, :-1].values
        targets = df.iloc[:, -1].values
        
        return features, targets
        
    except Exception as e:
        print(f"Error loading test data: {e}")
        raise


def comprehensive_evaluation(
    model: Any, 
    X_test: np.ndarray, 
    y_test: np.ndarray
) -> Dict[str, float]:
    """
    Perform comprehensive model evaluation.
    
    Args:
        model: Trained model
        X_test: Test features
        y_test: Test targets
        
    Returns:
        Dictionary of comprehensive evaluation metrics
    """
    y_pred = model.predict(X_test)
    
    # Basic regression metrics
    metrics = {
        "mse": float(mean_squared_error(y_test, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_test, y_pred))),
        "mae": float(mean_absolute_error(y_test, y_pred)),
        "r2": float(r2_score(y_test, y_pred)),
        "explained_variance": float(explained_variance_score(y_test, y_pred)),
        "max_error": float(max_error(y_test, y_pred))
    }
    
    # Additional metrics
    residuals = y_test - y_pred
    metrics.update({
        "mean_residual": float(np.mean(residuals)),
        "std_residual": float(np.std(residuals)),
        "residual_range": float(np.max(residuals) - np.min(residuals))
    })
    
    # Percentage metrics
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
    metrics["mape"] = float(mape)
    
    return metrics


def evaluate_model_performance(
    model: Any, 
    X_test: np.ndarray, 
    y_test: np.ndarray,
    threshold_rmse: float = None
) -> Dict[str, Any]:
    """
    Evaluate model performance with pass/fail criteria.
    
    Args:
        model: Trained model
        X_test: Test features
        y_test: Test targets
        threshold_rmse: RMSE threshold for pass/fail
        
    Returns:
        Dictionary containing performance evaluation
    """
    metrics = comprehensive_evaluation(model, X_test, y_test)
    
    # Determine if model passes quality gates
    passes_quality_gates = True
    quality_issues = []
    
    if threshold_rmse and metrics["rmse"] > threshold_rmse:
        passes_quality_gates = False
        quality_issues.append(f"RMSE {metrics['rmse']:.4f} exceeds threshold {threshold_rmse}")
    
    if metrics["r2"] < 0.5:  # R² threshold
        passes_quality_gates = False
        quality_issues.append(f"R² {metrics['r2']:.4f} below threshold 0.5")
    
    if metrics["mape"] > 20:  # MAPE threshold
        passes_quality_gates = False
        quality_issues.append(f"MAPE {metrics['mape']:.2f}% exceeds threshold 20%")
    
    return {
        "metrics": metrics,
        "passes_quality_gates": passes_quality_gates,
        "quality_issues": quality_issues,
        "recommendation": "PASS" if passes_quality_gates else "FAIL"
    }


def save_evaluation_results(
    results: Dict[str, Any], 
    output_path: str
) -> str:
    """
    Save evaluation results to file.
    
    Args:
        results: Evaluation results
        output_path: Output file path
        
    Returns:
        Path to saved results file
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Evaluation results saved to: {output_file}")
    return str(output_file)


def main():
    """Main evaluation pipeline."""
    parser = argparse.ArgumentParser(description="AutoOps Model Evaluation")
    parser.add_argument("--model", type=str, required=True, help="Path to trained model file")
    parser.add_argument("--data", type=str, required=True, help="Path to test data CSV file")
    parser.add_argument("--out", type=str, default="./evaluation_results.json", 
                       help="Output file for evaluation results")
    parser.add_argument("--threshold-rmse", type=float, help="RMSE threshold for quality gates")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    print("🔍 Starting AutoOps Model Evaluation")
    print(f"Model: {args.model}")
    print(f"Test data: {args.data}")
    
    try:
        # Load model
        print("Loading model...")
        model = load_model(args.model)
        
        # Load test data
        print("Loading test data...")
        X_test, y_test = load_test_data(args.data)
        
        # Evaluate model
        print("Evaluating model...")
        results = evaluate_model_performance(
            model, X_test, y_test, args.threshold_rmse
        )
        
        # Print results
        print("\n📊 Evaluation Results:")
        print(f"  R² Score: {results['metrics']['r2']:.4f}")
        print(f"  RMSE: {results['metrics']['rmse']:.4f}")
        print(f"  MAE: {results['metrics']['mae']:.4f}")
        print(f"  MAPE: {results['metrics']['mape']:.2f}%")
        print(f"  Quality Gates: {'PASS' if results['passes_quality_gates'] else 'FAIL'}")
        
        if results['quality_issues']:
            print("\n⚠️  Quality Issues:")
            for issue in results['quality_issues']:
                print(f"  - {issue}")
        
        # Save results
        output_file = save_evaluation_results(results, args.out)
        
        print(f"\n✅ Evaluation completed successfully!")
        print(f"Results saved to: {output_file}")
        
        # Exit with appropriate code
        sys.exit(0 if results['passes_quality_gates'] else 1)
        
    except Exception as e:
        print(f"❌ Evaluation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
