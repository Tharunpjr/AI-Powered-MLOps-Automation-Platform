# AutoOps Makefile
# Common commands for AutoOps MLOps automation toolkit

.PHONY: help setup install lint format test build run deploy clean

# Default target
help:
	@echo "AutoOps MLOps Automation Toolkit"
	@echo "================================="
	@echo ""
	@echo "Available commands:"
	@echo "  setup     - Set up development environment"
	@echo "  install   - Install dependencies"
	@echo "  lint      - Run linting checks"
	@echo "  format    - Format code"
	@echo "  test      - Run tests"
	@echo "  build     - Build Docker image"
	@echo "  run       - Run model service locally"
	@echo "  train     - Train a model"
	@echo "  deploy    - Deploy to Kubernetes"
	@echo "  clean     - Clean up temporary files"
	@echo ""

# Setup development environment
setup:
	@echo "🚀 Setting up AutoOps development environment..."
	@python -m venv venv
	@echo "✅ Virtual environment created"
	@echo "📦 Installing dependencies..."
	@pip install --upgrade pip
	@pip install -r services/model_service/requirements.txt
	@echo "✅ Dependencies installed"
	@echo "📁 Creating directories..."
	@mkdir -p models data logs examples/sample_data
	@echo "✅ Directories created"
	@echo "🎯 Setup complete! Run 'make run' to start the service."

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	@pip install --upgrade pip
	@pip install -r services/model_service/requirements.txt
	@echo "✅ Dependencies installed"

# Lint code
lint:
	@echo "🔍 Running linting checks..."
	@ruff check .
	@black --check .
	@isort --check-only .
	@echo "✅ Linting checks completed"

# Format code
format:
	@echo "🎨 Formatting code..."
	@black .
	@isort .
	@echo "✅ Code formatted"

# Run tests
test:
	@echo "🧪 Running tests..."
	@python -m pytest tests/ services/model_service/tests/ -v --cov=services/model_service --cov-report=html --cov-report=term
	@echo "✅ Tests completed"

# Run tests with coverage
test-coverage:
	@echo "🧪 Running tests with coverage..."
	@python -m pytest tests/ services/model_service/tests/ -v --cov=services/model_service --cov-report=html --cov-report=term --cov-fail-under=80
	@echo "✅ Tests with coverage completed"

# Run unit tests only
test-unit:
	@echo "🧪 Running unit tests..."
	@python -m pytest services/model_service/tests/ -v
	@echo "✅ Unit tests completed"

# Run integration tests only
test-integration:
	@echo "🧪 Running integration tests..."
	@python -m pytest tests/integration/ -v
	@echo "✅ Integration tests completed"

# Build Docker image
build:
	@echo "🐳 Building Docker image..."
	@cd services/model_service && docker build -t autoops/model-service:latest .
	@echo "✅ Docker image built: autoops/model-service:latest"

# Build and push Docker image
build-push:
	@echo "🐳 Building and pushing Docker image..."
	@bash scripts/build_and_push.sh --push
	@echo "✅ Docker image built and pushed"

# Run model service locally
run:
	@echo "🚀 Starting AutoOps model service..."
	@cd services/model_service && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
	@echo "✅ Model service started at http://localhost:8000"

# Run with specific configuration
run-dev:
	@echo "🚀 Starting AutoOps model service in development mode..."
	@cd services/model_service && MODEL_PATH=../../models/model.pkl python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug
	@echo "✅ Model service started in development mode"

# Train a model
train:
	@echo "🤖 Training model..."
	@python pipelines/training/train.py --data examples/sample_data/small_dataset.csv --out models/ --model-type random_forest
	@echo "✅ Model training completed"

# Train with synthetic data
train-synthetic:
	@echo "🤖 Training model with synthetic data..."
	@python pipelines/training/train.py --synthetic --out models/ --model-type random_forest
	@echo "✅ Model training with synthetic data completed"

# Evaluate model
evaluate:
	@echo "📊 Evaluating model..."
	@python pipelines/training/evaluate.py --model models/model.pkl --data examples/sample_data/small_dataset.csv --out evaluation_results.json
	@echo "✅ Model evaluation completed"

# Deploy to Kubernetes
deploy:
	@echo "🚀 Deploying to Kubernetes..."
	@bash scripts/deploy_k8s.sh
	@echo "✅ Deployment completed"

# Deploy with dry run
deploy-dry-run:
	@echo "🔍 Deploying to Kubernetes (dry run)..."
	@bash scripts/deploy_k8s.sh --dry-run
	@echo "✅ Dry run deployment completed"

# Deploy to specific namespace
deploy-namespace:
	@echo "🚀 Deploying to Kubernetes namespace: $(NAMESPACE)..."
	@bash scripts/deploy_k8s.sh --namespace $(NAMESPACE)
	@echo "✅ Deployment to namespace $(NAMESPACE) completed"

# Start local development environment
dev:
	@echo "🚀 Starting local development environment..."
	@bash scripts/run_local.sh
	@echo "✅ Local development environment started"

# Start with setup
dev-setup:
	@echo "🚀 Starting local development environment with setup..."
	@bash scripts/run_local.sh setup
	@echo "✅ Local development environment with setup completed"

# Check service status
status:
	@echo "🏥 Checking service status..."
	@python cli/autoops_cli.py status
	@echo "✅ Status check completed"

# Start service via CLI
start:
	@echo "🚀 Starting service via CLI..."
	@python cli/autoops_cli.py start
	@echo "✅ Service started via CLI"

# Run full pipeline
pipeline:
	@echo "🔄 Running full pipeline..."
	@python pipelines/dags/sample_pipeline.py
	@echo "✅ Full pipeline completed"

# Generate sample data
data:
	@echo "📊 Generating sample data..."
	@python -c "import pandas as pd; import numpy as np; np.random.seed(42); X = np.random.randn(1000, 4); y = np.sum(X, axis=1) + 0.1 * np.random.randn(1000); df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(4)]); df['target'] = y; df.to_csv('examples/sample_data/small_dataset.csv', index=False); print('Sample data generated')"
	@echo "✅ Sample data generated"

# Clean up temporary files
clean:
	@echo "🧹 Cleaning up temporary files..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type f -name "*.log" -delete
	@rm -rf .pytest_cache/
	@rm -rf .coverage
	@rm -rf htmlcov/
	@rm -rf dist/
	@rm -rf build/
	@rm -rf *.egg-info/
	@echo "✅ Cleanup completed"

# Clean models and data
clean-models:
	@echo "🧹 Cleaning up models and data..."
	@rm -rf models/*.pkl
	@rm -rf models/*.json
	@rm -rf data/*
	@echo "✅ Models and data cleaned"

# Clean Docker images
clean-docker:
	@echo "🧹 Cleaning up Docker images..."
	@docker rmi autoops/model-service:latest 2>/dev/null || true
	@docker system prune -f
	@echo "✅ Docker cleanup completed"

# Show logs
logs:
	@echo "📋 Showing service logs..."
	@tail -f logs/autoops.log 2>/dev/null || echo "No log file found"

# Show Docker logs
logs-docker:
	@echo "📋 Showing Docker logs..."
	@docker logs -f autoops-model-service 2>/dev/null || echo "No Docker container found"

# Show Kubernetes logs
logs-k8s:
	@echo "📋 Showing Kubernetes logs..."
	@kubectl logs -f deployment/model-service -n autoops 2>/dev/null || echo "No Kubernetes deployment found"

# Health check
health:
	@echo "🏥 Checking service health..."
	@curl -f http://localhost:8000/health || echo "Service not running"
	@echo "✅ Health check completed"

# Metrics check
metrics:
	@echo "📊 Checking metrics..."
	@curl -f http://localhost:8000/metrics || echo "Metrics not available"
	@echo "✅ Metrics check completed"

# API documentation
docs:
	@echo "📖 Opening API documentation..."
	@echo "API documentation available at: http://localhost:8000/docs"
	@echo "ReDoc documentation available at: http://localhost:8000/redoc"

# Security scan
security:
	@echo "🔒 Running security scan..."
	@pip install safety
	@safety check
	@echo "✅ Security scan completed"

# Dependency check
deps:
	@echo "📦 Checking dependencies..."
	@pip check
	@echo "✅ Dependency check completed"

# Update dependencies
update-deps:
	@echo "📦 Updating dependencies..."
	@pip install --upgrade -r services/model_service/requirements.txt
	@echo "✅ Dependencies updated"

# Create requirements from current environment
freeze:
	@echo "📦 Freezing current environment..."
	@pip freeze > requirements-frozen.txt
	@echo "✅ Requirements frozen to requirements-frozen.txt"

# Run all checks
check: lint test security deps
	@echo "✅ All checks completed"

# Full development workflow
dev-full: setup data train test build run
	@echo "✅ Full development workflow completed"

# Production deployment
prod-deploy: test build deploy
	@echo "✅ Production deployment completed"

# Development deployment
dev-deploy: build deploy-dry-run
	@echo "✅ Development deployment completed"
