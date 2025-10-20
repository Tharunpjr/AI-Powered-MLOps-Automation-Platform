"""
AutoOps Model Service - API Tests
Unit tests for the FastAPI model service endpoints.
"""

import pytest
import json
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Import the FastAPI app
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from app.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def mock_model_predictor():
    """Mock model predictor for testing."""
    with patch('app.api.endpoints.get_model_predictor') as mock:
        mock_predictor = MagicMock()
        mock_predictor.predict.return_value = 42.0
        mock_predictor.get_model_version.return_value = "v1.0.0"
        mock_predictor.is_model_loaded.return_value = True
        mock_predictor.get_model_info.return_value = {
            "model_loaded": True,
            "model_type": "RandomForestRegressor",
            "model_version": "v1.0.0"
        }
        mock.return_value = mock_predictor
        yield mock_predictor


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["service"] == "AutoOps Model Service"
        assert data["version"] == "1.0.0"
        assert data["status"] == "healthy"
    
    def test_health_endpoint(self, client):
        """Test health endpoint."""
        response = client.get("/health/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "service" in data
        assert "version" in data
        assert "uptime" in data
    
    def test_readiness_endpoint(self, client, mock_model_predictor):
        """Test readiness endpoint."""
        response = client.get("/health/ready")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "ready"
        assert data["model_loaded"] is True
        assert data["model_version"] == "v1.0.0"
    
    def test_liveness_endpoint(self, client):
        """Test liveness endpoint."""
        response = client.get("/health/live")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "alive"
        assert "timestamp" in data
        assert "uptime" in data
    
    def test_detailed_status_endpoint(self, client, mock_model_predictor):
        """Test detailed status endpoint."""
        response = client.get("/health/status")
        assert response.status_code == 200
        
        data = response.json()
        assert data["service"] == "AutoOps Model Service"
        assert data["version"] == "1.0.0"
        assert data["status"] == "healthy"
        assert "environment" in data


class TestPredictionEndpoints:
    """Test prediction endpoints."""
    
    def test_predict_endpoint_success(self, client, mock_model_predictor):
        """Test successful prediction."""
        request_data = {
            "features": [1.0, 2.0, 3.0, 4.0]
        }
        
        response = client.post("/api/v1/predict", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "prediction" in data
        assert "model_version" in data
        assert "prediction_time" in data
        assert "features_count" in data
        
        assert data["prediction"] == 42.0
        assert data["model_version"] == "v1.0.0"
        assert data["features_count"] == 4
        assert data["prediction_time"] > 0
    
    def test_predict_endpoint_invalid_features(self, client, mock_model_predictor):
        """Test prediction with invalid features."""
        request_data = {
            "features": []
        }
        
        response = client.post("/api/v1/predict", json=request_data)
        assert response.status_code == 422  # Validation error
    
    def test_predict_endpoint_missing_features(self, client, mock_model_predictor):
        """Test prediction with missing features."""
        request_data = {}
        
        response = client.post("/api/v1/predict", json=request_data)
        assert response.status_code == 422  # Validation error
    
    def test_predict_endpoint_model_error(self, client):
        """Test prediction when model fails."""
        with patch('app.api.endpoints.get_model_predictor') as mock:
            mock_predictor = MagicMock()
            mock_predictor.predict.side_effect = Exception("Model error")
            mock.return_value = mock_predictor
            
            request_data = {
                "features": [1.0, 2.0, 3.0, 4.0]
            }
            
            response = client.post("/api/v1/predict", json=request_data)
            assert response.status_code == 500
            
            data = response.json()
            assert "detail" in data
            assert "Model error" in data["detail"]
    
    def test_model_info_endpoint(self, client, mock_model_predictor):
        """Test model info endpoint."""
        response = client.get("/api/v1/model/info")
        assert response.status_code == 200
        
        data = response.json()
        assert data["model_loaded"] is True
        assert data["model_type"] == "RandomForestRegressor"
        assert data["model_version"] == "v1.0.0"
    
    def test_model_reload_endpoint(self, client, mock_model_predictor):
        """Test model reload endpoint."""
        mock_model_predictor.reload_model.return_value = True
        
        response = client.post("/api/v1/model/reload")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "success"
        assert "message" in data
        assert "model_info" in data
    
    def test_batch_predict_endpoint(self, client, mock_model_predictor):
        """Test batch prediction endpoint."""
        mock_model_predictor.batch_predict.return_value = [42.0, 43.0, 44.0]
        
        request_data = [
            [1.0, 2.0, 3.0, 4.0],
            [2.0, 3.0, 4.0, 5.0],
            [3.0, 4.0, 5.0, 6.0]
        ]
        
        response = client.get("/api/v1/batch/predict", params={"features_list": request_data})
        assert response.status_code == 200
        
        data = response.json()
        assert "predictions" in data
        assert "count" in data
        assert "batch_time" in data
        assert "model_version" in data
        
        assert data["predictions"] == [42.0, 43.0, 44.0]
        assert data["count"] == 3


class TestMetricsEndpoint:
    """Test metrics endpoint."""
    
    def test_metrics_endpoint(self, client):
        """Test metrics endpoint."""
        response = client.get("/metrics")
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/plain; version=0.0.4; charset=utf-8"
        
        # Check that metrics content is returned
        content = response.text
        assert "http_requests_total" in content
        assert "http_request_duration_seconds" in content


class TestErrorHandling:
    """Test error handling."""
    
    def test_invalid_json(self, client):
        """Test invalid JSON request."""
        response = client.post(
            "/api/v1/predict",
            data="invalid json",
            headers={"content-type": "application/json"}
        )
        assert response.status_code == 422
    
    def test_unsupported_method(self, client):
        """Test unsupported HTTP method."""
        response = client.put("/api/v1/predict")
        assert response.status_code == 405  # Method not allowed
    
    def test_nonexistent_endpoint(self, client):
        """Test nonexistent endpoint."""
        response = client.get("/api/v1/nonexistent")
        assert response.status_code == 404


class TestCORS:
    """Test CORS headers."""
    
    def test_cors_headers(self, client):
        """Test CORS headers are present."""
        response = client.options("/api/v1/predict")
        assert response.status_code == 200
        
        # Check CORS headers
        headers = response.headers
        assert "access-control-allow-origin" in headers
        assert "access-control-allow-methods" in headers
        assert "access-control-allow-headers" in headers
