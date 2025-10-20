"""
AutoOps Model Service - Model Tests
Unit tests for the model management and prediction functionality.
"""

import pytest
import numpy as np
import tempfile
import os
from unittest.mock import patch, MagicMock
from pathlib import Path

# Import model classes
import sys
sys.path.append(str(Path(__file__).parent.parent))

from app.model.model import ModelManager
from app.model.predict import ModelPredictor


class TestModelManager:
    """Test ModelManager class."""
    
    def test_model_manager_init(self):
        """Test ModelManager initialization."""
        model_manager = ModelManager("/tmp/test_model.pkl")
        assert model_manager.model_path == Path("/tmp/test_model.pkl")
        assert model_manager.model is None
        assert model_manager.metadata == {}
    
    def test_create_dummy_model(self):
        """Test creating a dummy model."""
        model_manager = ModelManager()
        
        # Create test data
        X = np.random.randn(100, 4)
        y = np.random.randn(100)
        
        # Create dummy model
        model = model_manager.create_dummy_model(X, y)
        assert model is not None
        
        # Test prediction
        predictions = model.predict(X[:5])
        assert len(predictions) == 5
        assert all(isinstance(p, (int, float)) for p in predictions)
    
    def test_create_random_forest_model(self):
        """Test creating a random forest model."""
        model_manager = ModelManager()
        
        # Create test data
        X = np.random.randn(100, 4)
        y = np.sum(X, axis=1) + 0.1 * np.random.randn(100)
        
        # Create random forest model
        model = model_manager.create_random_forest_model(X, y)
        assert model is not None
        
        # Test prediction
        predictions = model.predict(X[:5])
        assert len(predictions) == 5
        assert all(isinstance(p, (int, float)) for p in predictions)
    
    def test_save_and_load_model(self):
        """Test saving and loading a model."""
        with tempfile.TemporaryDirectory() as temp_dir:
            model_path = os.path.join(temp_dir, "test_model.pkl")
            model_manager = ModelManager(model_path)
            
            # Create test data and model
            X = np.random.randn(100, 4)
            y = np.random.randn(100)
            model = model_manager.create_dummy_model(X, y)
            
            # Save model
            metadata = {"version": "v1.0.0", "test": True}
            success = model_manager.save_model(model, metadata)
            assert success
            
            # Load model
            new_model_manager = ModelManager(model_path)
            success = new_model_manager.load_model()
            assert success
            
            # Verify model is loaded
            assert new_model_manager.is_model_loaded()
            assert new_model_manager.get_model() is not None
            
            # Verify metadata
            info = new_model_manager.get_model_info()
            assert info["model_loaded"] is True
            assert info["metadata"]["version"] == "v1.0.0"
            assert info["metadata"]["test"] is True
    
    def test_model_info(self):
        """Test getting model information."""
        model_manager = ModelManager()
        
        # Test with no model loaded
        info = model_manager.get_model_info()
        assert info["model_loaded"] is False
        assert info["model_path"] is not None
        
        # Test with model loaded
        X = np.random.randn(100, 4)
        y = np.random.randn(100)
        model = model_manager.create_dummy_model(X, y)
        
        metadata = {"version": "v1.0.0"}
        model_manager.save_model(model, metadata)
        
        info = model_manager.get_model_info()
        assert info["model_loaded"] is True
        assert info["model_type"] == "DummyRegressor"
        assert info["model_version"] == "v1.0.0"
    
    def test_evaluate_model(self):
        """Test model evaluation."""
        model_manager = ModelManager()
        
        # Create test data
        X = np.random.randn(100, 4)
        y = np.sum(X, axis=1) + 0.1 * np.random.randn(100)
        
        # Create and train model
        model = model_manager.create_random_forest_model(X, y)
        
        # Evaluate model
        metrics = model_manager.evaluate_model(X, y)
        
        assert "mse" in metrics
        assert "rmse" in metrics
        assert "r2" in metrics
        assert all(isinstance(v, float) for v in metrics.values())


class TestModelPredictor:
    """Test ModelPredictor class."""
    
    def test_model_predictor_init(self):
        """Test ModelPredictor initialization."""
        with patch('app.model.predict.ModelManager') as mock_manager:
            mock_manager.return_value.load_model.return_value = True
            mock_manager.return_value.is_model_loaded.return_value = True
            
            predictor = ModelPredictor("/tmp/test_model.pkl")
            assert predictor.model_loaded is True
    
    def test_predict_success(self):
        """Test successful prediction."""
        with patch('app.model.predict.ModelManager') as mock_manager:
            mock_model = MagicMock()
            mock_model.predict.return_value = np.array([42.0])
            mock_manager.return_value.load_model.return_value = True
            mock_manager.return_value.is_model_loaded.return_value = True
            mock_manager.return_value.get_model.return_value = mock_model
            mock_manager.return_value.get_model_version.return_value = "v1.0.0"
            
            predictor = ModelPredictor()
            result = predictor.predict([1.0, 2.0, 3.0, 4.0])
            
            assert result == 42.0
            mock_model.predict.assert_called_once()
    
    def test_predict_model_not_loaded(self):
        """Test prediction when model is not loaded."""
        with patch('app.model.predict.ModelManager') as mock_manager:
            mock_manager.return_value.load_model.return_value = False
            mock_manager.return_value.is_model_loaded.return_value = False
            
            predictor = ModelPredictor()
            
            with pytest.raises(ValueError, match="Model not loaded"):
                predictor.predict([1.0, 2.0, 3.0, 4.0])
    
    def test_predict_invalid_features(self):
        """Test prediction with invalid features."""
        with patch('app.model.predict.ModelManager') as mock_manager:
            mock_manager.return_value.load_model.return_value = True
            mock_manager.return_value.is_model_loaded.return_value = True
            
            predictor = ModelPredictor()
            
            with pytest.raises(ValueError, match="Features list cannot be empty"):
                predictor.predict([])
    
    def test_batch_predict(self):
        """Test batch prediction."""
        with patch('app.model.predict.ModelManager') as mock_manager:
            mock_model = MagicMock()
            mock_model.predict.return_value = np.array([42.0, 43.0, 44.0])
            mock_manager.return_value.load_model.return_value = True
            mock_manager.return_value.is_model_loaded.return_value = True
            mock_manager.return_value.get_model.return_value = mock_model
            mock_manager.return_value.get_model_version.return_value = "v1.0.0"
            
            predictor = ModelPredictor()
            features_list = [
                [1.0, 2.0, 3.0, 4.0],
                [2.0, 3.0, 4.0, 5.0],
                [3.0, 4.0, 5.0, 6.0]
            ]
            
            result = predictor.batch_predict(features_list)
            
            assert result == [42.0, 43.0, 44.0]
            mock_model.predict.assert_called_once()
    
    def test_get_model_version(self):
        """Test getting model version."""
        with patch('app.model.predict.ModelManager') as mock_manager:
            mock_manager.return_value.load_model.return_value = True
            mock_manager.return_value.is_model_loaded.return_value = True
            mock_manager.return_value.get_model_info.return_value = {
                "model_version": "v1.0.0"
            }
            
            predictor = ModelPredictor()
            version = predictor.get_model_version()
            
            assert version == "v1.0.0"
    
    def test_get_model_info(self):
        """Test getting model information."""
        with patch('app.model.predict.ModelManager') as mock_manager:
            mock_info = {
                "model_loaded": True,
                "model_type": "RandomForestRegressor",
                "model_version": "v1.0.0"
            }
            mock_manager.return_value.load_model.return_value = True
            mock_manager.return_value.is_model_loaded.return_value = True
            mock_manager.return_value.get_model_info.return_value = mock_info
            
            predictor = ModelPredictor()
            info = predictor.get_model_info()
            
            assert info == mock_info
    
    def test_reload_model(self):
        """Test model reload."""
        with patch('app.model.predict.ModelManager') as mock_manager:
            mock_manager.return_value.load_model.return_value = True
            mock_manager.return_value.is_model_loaded.return_value = True
            
            predictor = ModelPredictor()
            result = predictor.reload_model()
            
            assert result is True
    
    def test_validate_features(self):
        """Test feature validation."""
        with patch('app.model.predict.ModelManager') as mock_manager:
            mock_manager.return_value.load_model.return_value = True
            mock_manager.return_value.is_model_loaded.return_value = True
            
            predictor = ModelPredictor()
            
            # Valid features
            assert predictor.validate_features([1.0, 2.0, 3.0, 4.0]) is True
            
            # Invalid features
            assert predictor.validate_features([]) is False
            assert predictor.validate_features(["invalid"]) is False
            assert predictor.validate_features([1.0] * 1001) is False  # Too many features
    
    def test_get_model_capabilities(self):
        """Test getting model capabilities."""
        with patch('app.model.predict.ModelManager') as mock_manager:
            mock_model = MagicMock()
            mock_model.predict_proba = MagicMock()  # Has predict_proba method
            mock_model.feature_importances_ = np.array([0.1, 0.2, 0.3, 0.4])
            
            mock_manager.return_value.load_model.return_value = True
            mock_manager.return_value.is_model_loaded.return_value = True
            mock_manager.return_value.get_model.return_value = mock_model
            
            predictor = ModelPredictor()
            capabilities = predictor.get_model_capabilities()
            
            assert capabilities["model_loaded"] is True
            assert capabilities["supports_probability"] is True
            assert capabilities["supports_feature_importance"] is True
            assert capabilities["supports_batch_prediction"] is True


class TestModelIntegration:
    """Test model integration scenarios."""
    
    def test_full_model_workflow(self):
        """Test complete model workflow."""
        with tempfile.TemporaryDirectory() as temp_dir:
            model_path = os.path.join(temp_dir, "test_model.pkl")
            
            # Create and train model
            model_manager = ModelManager(model_path)
            X = np.random.randn(100, 4)
            y = np.sum(X, axis=1) + 0.1 * np.random.randn(100)
            model = model_manager.create_random_forest_model(X, y)
            
            # Save model
            metadata = {"version": "v1.0.0"}
            model_manager.save_model(model, metadata)
            
            # Load model with predictor
            predictor = ModelPredictor(model_path)
            assert predictor.is_model_loaded()
            
            # Make predictions
            test_features = [1.0, 2.0, 3.0, 4.0]
            prediction = predictor.predict(test_features)
            assert isinstance(prediction, float)
            
            # Test batch prediction
            batch_features = [
                [1.0, 2.0, 3.0, 4.0],
                [2.0, 3.0, 4.0, 5.0]
            ]
            batch_predictions = predictor.batch_predict(batch_features)
            assert len(batch_predictions) == 2
            assert all(isinstance(p, float) for p in batch_predictions)
