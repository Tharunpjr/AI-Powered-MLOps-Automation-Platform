"""
AutoOps Test Configuration
Shared test fixtures and configuration for the AutoOps test suite.
"""

import pytest
import tempfile
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    import pandas as pd
    import numpy as np
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Generate synthetic data
    n_samples = 100
    n_features = 4
    
    X = np.random.randn(n_samples, n_features)
    y = np.sum(X, axis=1) + 0.1 * np.random.randn(n_samples)
    
    # Create DataFrame
    feature_names = [f"feature_{i}" for i in range(n_features)]
    df = pd.DataFrame(X, columns=feature_names)
    df['target'] = y
    
    return df


@pytest.fixture
def sample_model():
    """Create a sample trained model for testing."""
    from sklearn.dummy import DummyRegressor
    import numpy as np
    
    # Create dummy model
    model = DummyRegressor(strategy='mean')
    
    # Generate sample data
    X = np.random.randn(100, 4)
    y = np.random.randn(100)
    
    # Train model
    model.fit(X, y)
    
    return model


@pytest.fixture
def mock_model_predictor():
    """Mock model predictor for testing."""
    with patch('app.model.predict.ModelManager') as mock:
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


@pytest.fixture
def mock_requests():
    """Mock requests for testing HTTP calls."""
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "healthy",
            "service": "AutoOps Model Service",
            "version": "1.0.0"
        }
        mock_get.return_value = mock_response
        yield mock_get


@pytest.fixture
def test_config():
    """Test configuration."""
    return {
        "app": {
            "name": "AutoOps Test",
            "version": "1.0.0",
            "environment": "test"
        },
        "model_service": {
            "host": "localhost",
            "port": 8000,
            "log_level": "DEBUG"
        },
        "training": {
            "data": {
                "path": "test_data.csv",
                "test_size": 0.2
            },
            "model": {
                "type": "dummy",
                "params": {}
            }
        }
    }


@pytest.fixture
def sample_csv_file(temp_dir, sample_data):
    """Create a sample CSV file for testing."""
    csv_path = os.path.join(temp_dir, "sample_data.csv")
    sample_data.to_csv(csv_path, index=False)
    return csv_path


@pytest.fixture
def sample_model_file(temp_dir, sample_model):
    """Create a sample model file for testing."""
    import pickle
    
    model_path = os.path.join(temp_dir, "model.pkl")
    with open(model_path, 'wb') as f:
        pickle.dump(sample_model, f)
    return model_path


@pytest.fixture
def mock_docker():
    """Mock Docker operations for testing."""
    with patch('subprocess.run') as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Docker build successful"
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        yield mock_run


@pytest.fixture
def mock_kubectl():
    """Mock kubectl operations for testing."""
    with patch('subprocess.run') as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "kubectl command successful"
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        yield mock_run


@pytest.fixture
def mock_environment():
    """Mock environment variables for testing."""
    env_vars = {
        "MODEL_PATH": "/tmp/test_model.pkl",
        "LOG_LEVEL": "DEBUG",
        "PYTHONPATH": "/tmp"
    }
    
    with patch.dict(os.environ, env_vars):
        yield env_vars


@pytest.fixture(scope="session")
def test_session():
    """Test session fixture for setup/teardown."""
    print("Setting up test session...")
    yield
    print("Tearing down test session...")


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment for each test."""
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Set test environment variables
    os.environ["TESTING"] = "true"
    os.environ["LOG_LEVEL"] = "DEBUG"
    
    yield
    
    # Cleanup after test
    if "TESTING" in os.environ:
        del os.environ["TESTING"]


# Pytest configuration
def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection."""
    for item in items:
        # Add unit marker to tests in specific directories
        if "test_model" in str(item.fspath) or "test_api" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        
        # Add integration marker to tests in integration directory
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        
        # Add slow marker to tests that take longer
        if "full_pipeline" in str(item.fspath):
            item.add_marker(pytest.mark.slow)
