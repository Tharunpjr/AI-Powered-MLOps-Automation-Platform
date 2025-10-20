#!/bin/bash
# AutoOps Local Development Script
# Script to run the AutoOps model service locally

set -e

echo "🚀 Starting AutoOps Local Development Environment"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3.11 is available
check_python() {
    print_status "Checking Python version..."
    if command -v python3.11 &> /dev/null; then
        PYTHON_CMD="python3.11"
    elif command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
        if [[ "$PYTHON_VERSION" == "3.11" ]]; then
            PYTHON_CMD="python3"
        else
            print_error "Python 3.11 is required. Found Python $PYTHON_VERSION"
            exit 1
        fi
    else
        print_error "Python 3.11 is required but not found"
        exit 1
    fi
    print_success "Python version check passed"
}

# Create virtual environment
setup_venv() {
    print_status "Setting up virtual environment..."
    
    if [ ! -d "venv" ]; then
        $PYTHON_CMD -m venv venv
        print_success "Virtual environment created"
    else
        print_status "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    print_success "Virtual environment activated"
}

# Install dependencies
install_dependencies() {
    print_status "Installing dependencies..."
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install requirements
    if [ -f "services/model_service/requirements.txt" ]; then
        pip install -r services/model_service/requirements.txt
        print_success "Model service dependencies installed"
    else
        print_warning "Model service requirements.txt not found"
    fi
    
    # Install additional development dependencies
    pip install jupyter notebook ipykernel
    print_success "Development dependencies installed"
}

# Create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    
    mkdir -p models
    mkdir -p data
    mkdir -p logs
    mkdir -p examples/sample_data
    
    print_success "Directories created"
}

# Generate sample data
generate_sample_data() {
    print_status "Generating sample data..."
    
    if [ ! -f "examples/sample_data/small_dataset.csv" ]; then
        $PYTHON_CMD -c "
import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Generate synthetic data
n_samples = 1000
n_features = 4

# Generate features
X = np.random.randn(n_samples, n_features)

# Generate targets with some relationship to features
y = np.sum(X, axis=1) + 0.1 * np.random.randn(n_samples)

# Create DataFrame
feature_names = [f'feature_{i}' for i in range(n_features)]
df = pd.DataFrame(X, columns=feature_names)
df['target'] = y

# Save to CSV
df.to_csv('examples/sample_data/small_dataset.csv', index=False)
print(f'Generated sample data with {n_samples} samples and {n_features} features')
"
        print_success "Sample data generated"
    else
        print_status "Sample data already exists"
    fi
}

# Train a sample model
train_sample_model() {
    print_status "Training sample model..."
    
    if [ ! -f "models/model.pkl" ]; then
        $PYTHON_CMD pipelines/training/train.py \
            --data examples/sample_data/small_dataset.csv \
            --out models/ \
            --model-type random_forest \
            --synthetic
        print_success "Sample model trained"
    else
        print_status "Sample model already exists"
    fi
}

# Start the model service
start_service() {
    print_status "Starting model service..."
    
    cd services/model_service
    
    # Set environment variables
    export MODEL_PATH="../../models/model.pkl"
    export LOG_LEVEL="INFO"
    export PYTHONPATH="../../"
    
    print_status "Model service starting on http://localhost:8000"
    print_status "API documentation available at http://localhost:8000/docs"
    print_status "Health check available at http://localhost:8000/health"
    print_status "Metrics available at http://localhost:8000/metrics"
    print_status ""
    print_status "Press Ctrl+C to stop the service"
    
    # Start the service
    $PYTHON_CMD -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
}

# Main execution
main() {
    print_status "AutoOps Local Development Setup"
    print_status "================================="
    
    # Check Python
    check_python
    
    # Setup virtual environment
    setup_venv
    
    # Install dependencies
    install_dependencies
    
    # Create directories
    create_directories
    
    # Generate sample data
    generate_sample_data
    
    # Train sample model
    train_sample_model
    
    print_success "Setup completed successfully!"
    print_status ""
    print_status "Next steps:"
    print_status "1. The model service will start automatically"
    print_status "2. Visit http://localhost:8000/docs for API documentation"
    print_status "3. Test the service with: curl http://localhost:8000/health"
    print_status ""
    
    # Start the service
    start_service
}

# Handle script arguments
case "${1:-}" in
    "setup")
        print_status "Running setup only..."
        check_python
        setup_venv
        install_dependencies
        create_directories
        generate_sample_data
        train_sample_model
        print_success "Setup completed!"
        ;;
    "train")
        print_status "Training model only..."
        source venv/bin/activate 2>/dev/null || true
        train_sample_model
        ;;
    "service")
        print_status "Starting service only..."
        source venv/bin/activate 2>/dev/null || true
        start_service
        ;;
    "help"|"-h"|"--help")
        echo "AutoOps Local Development Script"
        echo ""
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  setup   - Run full setup (default)"
        echo "  train   - Train model only"
        echo "  service - Start service only"
        echo "  help    - Show this help message"
        echo ""
        ;;
    *)
        main
        ;;
esac
