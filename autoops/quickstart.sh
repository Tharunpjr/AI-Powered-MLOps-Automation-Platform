#!/bin/bash
# AutoOps Quick Start Script
# This script sets up and runs AutoOps in 5 minutes

set -e

echo "🚀 AutoOps Quick Start"
echo "======================"
echo ""

# Check Python version
echo "📋 Checking prerequisites..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python $PYTHON_VERSION found"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r services/model_service/requirements.txt
echo "✅ Dependencies installed"

# Create directories
echo ""
echo "📁 Creating directories..."
mkdir -p models examples/sample_data logs
echo "✅ Directories created"

# Generate sample data
echo ""
echo "📊 Generating sample data..."
python3 -c "
import pandas as pd
import numpy as np
np.random.seed(42)
X = np.random.randn(1000, 4)
y = np.sum(X, axis=1) + 0.1 * np.random.randn(1000)
df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(4)])
df['target'] = y
df.to_csv('examples/sample_data/small_dataset.csv', index=False)
print('✅ Sample data generated')
"

# Train models
echo ""
echo "🤖 Training models..."
echo "  Training scikit-learn model..."
python3 pipelines/training/train.py \
    --data examples/sample_data/small_dataset.csv \
    --out models/ \
    --model-type random_forest \
    > /dev/null 2>&1
echo "  ✅ scikit-learn model trained"

echo "  Training PyTorch model..."
python3 pipelines/training/train_pytorch.py \
    --synthetic \
    --out models/ \
    --epochs 50 \
    --hidden-sizes 32 16 \
    > /dev/null 2>&1
echo "  ✅ PyTorch model trained"

# Test models
echo ""
echo "🧪 Testing models..."
cd services/model_service
python3 -c "
from app.model.unified_predictor import UnifiedPredictor
p = UnifiedPredictor()
if p.is_model_loaded():
    print('✅ Model loaded successfully')
    print(f'   Model type: {p.model_type}')
    print(f'   Model version: {p.get_model_version()}')
    pred = p.predict([1.0, 2.0, 3.0, 4.0])
    print(f'   Test prediction: {pred:.4f}')
else:
    print('❌ Model failed to load')
    exit(1)
"
cd ../..

# Success message
echo ""
echo "✅ AutoOps setup complete!"
echo ""
echo "🎉 Next steps:"
echo "   1. Start the service:"
echo "      cd services/model_service"
echo "      python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
echo ""
echo "   2. Test the API:"
echo "      curl http://localhost:8000/health"
echo "      curl -X POST http://localhost:8000/api/v1/predict \\"
echo "        -H 'Content-Type: application/json' \\"
echo "        -d '{\"features\": [1.0, 2.0, 3.0, 4.0]}'"
echo ""
echo "   3. Deploy for free:"
echo "      See DEPLOYMENT_GUIDE.md for instructions"
echo ""
echo "📚 Documentation:"
echo "   - README.md: Overview"
echo "   - COMPLETE_SETUP_GUIDE.md: Full guide"
echo "   - DEPLOYMENT_GUIDE.md: Deployment options"
echo "   - PROJECT_SUMMARY.md: What we built"
echo ""
echo "🚀 Happy MLOps!"
