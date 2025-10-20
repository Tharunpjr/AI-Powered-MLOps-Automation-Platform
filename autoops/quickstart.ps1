# AutoOps Quick Start Script (Windows PowerShell)
# This script sets up and runs AutoOps in 5 minutes

Write-Host "🚀 AutoOps Quick Start" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "📋 Checking prerequisites..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ $pythonVersion found" -ForegroundColor Green
} catch {
    Write-Host "❌ Python 3 is not installed. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host ""
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
pip install -q --upgrade pip
pip install -q -r services/model_service/requirements.txt
Write-Host "✅ Dependencies installed" -ForegroundColor Green

# Create directories
Write-Host ""
Write-Host "📁 Creating directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path models, examples/sample_data, logs | Out-Null
Write-Host "✅ Directories created" -ForegroundColor Green

# Generate sample data
Write-Host ""
Write-Host "📊 Generating sample data..." -ForegroundColor Yellow
python -c @"
import pandas as pd
import numpy as np
np.random.seed(42)
X = np.random.randn(1000, 4)
y = np.sum(X, axis=1) + 0.1 * np.random.randn(1000)
df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(4)])
df['target'] = y
df.to_csv('examples/sample_data/small_dataset.csv', index=False)
print('✅ Sample data generated')
"@

# Train models
Write-Host ""
Write-Host "🤖 Training models..." -ForegroundColor Yellow
Write-Host "  Training scikit-learn model..." -ForegroundColor Gray
python pipelines/training/train.py `
    --data examples/sample_data/small_dataset.csv `
    --out models/ `
    --model-type random_forest `
    2>&1 | Out-Null
Write-Host "  ✅ scikit-learn model trained" -ForegroundColor Green

Write-Host "  Training PyTorch model..." -ForegroundColor Gray
python pipelines/training/train_pytorch.py `
    --synthetic `
    --out models/ `
    --epochs 50 `
    --hidden-sizes 32 16 `
    2>&1 | Out-Null
Write-Host "  ✅ PyTorch model trained" -ForegroundColor Green

# Test models
Write-Host ""
Write-Host "🧪 Testing models..." -ForegroundColor Yellow
Set-Location services/model_service
python -c @"
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
"@
Set-Location ../..

# Success message
Write-Host ""
Write-Host "✅ AutoOps setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "🎉 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Start the service:" -ForegroundColor White
Write-Host "      cd services/model_service" -ForegroundColor Gray
Write-Host "      python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload" -ForegroundColor Gray
Write-Host ""
Write-Host "   2. Test the API:" -ForegroundColor White
Write-Host "      curl http://localhost:8000/health" -ForegroundColor Gray
Write-Host "      curl -X POST http://localhost:8000/api/v1/predict \" -ForegroundColor Gray
Write-Host "        -H 'Content-Type: application/json' \" -ForegroundColor Gray
Write-Host "        -d '{\"features\": [1.0, 2.0, 3.0, 4.0]}'" -ForegroundColor Gray
Write-Host ""
Write-Host "   3. Deploy for free:" -ForegroundColor White
Write-Host "      See DEPLOYMENT_GUIDE.md for instructions" -ForegroundColor Gray
Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "   - README.md: Overview" -ForegroundColor White
Write-Host "   - COMPLETE_SETUP_GUIDE.md: Full guide" -ForegroundColor White
Write-Host "   - DEPLOYMENT_GUIDE.md: Deployment options" -ForegroundColor White
Write-Host "   - PROJECT_SUMMARY.md: What we built" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Happy MLOps!" -ForegroundColor Cyan
