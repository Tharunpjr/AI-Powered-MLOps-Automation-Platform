# AutoOps Complete Setup & Deployment Guide

## 🎯 Complete End-to-End Guide: From Zero to Production

This guide will take you from a fresh installation to a fully deployed, production-ready MLOps platform with AI capabilities - **completely free**.

---

## 📋 Table of Contents

1. [Local Setup](#1-local-setup)
2. [Train Your First Model](#2-train-your-first-model)
3. [Test Locally](#3-test-locally)
4. [Deploy to Production (Free)](#4-deploy-to-production-free)
5. [Monitor & Maintain](#5-monitor--maintain)
6. [Advanced Features](#6-advanced-features)

---

## 1. Local Setup

### Step 1.1: Install Prerequisites

**Windows:**
```powershell
# Install Python 3.11
winget install Python.Python.3.11

# Install Git
winget install Git.Git

# Verify installations
python --version  # Should show 3.11.x
git --version
```

**Mac/Linux:**
```bash
# Install Python 3.11
brew install python@3.11  # Mac
# or
sudo apt install python3.11  # Ubuntu/Debian

# Install Git
brew install git  # Mac
# or
sudo apt install git  # Ubuntu/Debian
```

### Step 1.2: Clone Repository

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/autoops.git
cd autoops

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### Step 1.3: Install Dependencies

```bash
# Install core dependencies
pip install --upgrade pip
pip install -r services/model_service/requirements.txt

# This installs:
# - FastAPI & Uvicorn (API server)
# - PyTorch (deep learning)
# - scikit-learn (traditional ML)
# - Prometheus client (metrics)
# - And more...
```

---

## 2. Train Your First Model

### Option A: Quick Start with Synthetic Data

#### Train scikit-learn Model (Traditional ML)
```bash
# Generate sample data
python -c "import pandas as pd; import numpy as np; np.random.seed(42); X = np.random.randn(1000, 4); y = np.sum(X, axis=1) + 0.1 * np.random.randn(1000); df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(4)]); df['target'] = y; df.to_csv('examples/sample_data/small_dataset.csv', index=False)"

# Train model
python pipelines/training/train.py \
  --data examples/sample_data/small_dataset.csv \
  --out models/ \
  --model-type random_forest

# Expected output:
# ✅ Training completed successfully!
# Model saved to: models/model-YYYYMMDD_HHMMSS.pkl
# Metrics: {"mse": 0.30, "rmse": 0.55, "r2": 0.92}
```

#### Train PyTorch Neural Network (Deep Learning) 🔥
```bash
# Train with synthetic data
python pipelines/training/train_pytorch.py \
  --synthetic \
  --out models/ \
  --epochs 100 \
  --hidden-sizes 64 32 \
  --batch-size 32 \
  --learning-rate 0.001

# Expected output:
# ✅ PyTorch training completed successfully!
# Model saved to: models/pytorch_model-YYYYMMDD_HHMMSS.pt
# Test Metrics: {"mse": 0.65, "rmse": 0.81, "r2": 0.92}
```

### Option B: Train with Your Own Data

#### Prepare Your Data
Your CSV should have:
- Features in columns (e.g., `feature_0`, `feature_1`, ...)
- Target in the last column (e.g., `target`)

Example:
```csv
feature_0,feature_1,feature_2,feature_3,target
1.5,2.3,0.8,1.2,5.8
0.9,1.7,2.1,0.5,5.2
...
```

#### Train with Your Data
```bash
# scikit-learn
python pipelines/training/train.py \
  --data your_data.csv \
  --out models/ \
  --model-type random_forest

# PyTorch
python pipelines/training/train_pytorch.py \
  --data your_data.csv \
  --out models/ \
  --epochs 200 \
  --hidden-sizes 128 64 32
```

---

## 3. Test Locally

### Step 3.1: Start the Service

```bash
cd services/model_service

# Start the API server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# You should see:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# INFO:     Application startup complete.
# 🚀 AutoOps Model Service started successfully!
```

### Step 3.2: Test Endpoints

Open a new terminal and run:

```bash
# 1. Health Check
curl http://localhost:8000/health

# Expected response:
# {
#   "status": "healthy",
#   "timestamp": "2025-10-19 12:00:00 UTC",
#   "service": "AutoOps Model Service",
#   "version": "1.0.0",
#   "uptime": 10.5
# }

# 2. Model Info
curl http://localhost:8000/api/v1/model/info

# Expected response:
# {
#   "model_loaded": true,
#   "model_type": "sklearn",  # or "pytorch"
#   "model_version": "v1.0.20251019_120000",
#   "framework": "scikit-learn",  # or "PyTorch"
#   "features_expected": 4
# }

# 3. Make a Prediction
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0, 2.0, 3.0, 4.0]}'

# Expected response:
# {
#   "prediction": 10.5,
#   "model_version": "v1.0.20251019_120000",
#   "prediction_time": 0.002,
#   "features_count": 4
# }

# 4. Check Metrics (Prometheus format)
curl http://localhost:8000/metrics

# Expected response:
# # HELP http_requests_total Total HTTP requests
# # TYPE http_requests_total counter
# http_requests_total{method="POST",endpoint="/api/v1/predict",status_code="200"} 1.0
# ...
```

### Step 3.3: Test with Python

```python
import requests

# Make prediction
response = requests.post(
    "http://localhost:8000/api/v1/predict",
    json={"features": [1.0, 2.0, 3.0, 4.0]}
)

print(response.json())
# {'prediction': 10.5, 'model_version': 'v1.0...', ...}
```

---

## 4. Deploy to Production (Free)

### Option 1: Render.com (Recommended - Easiest) ⭐

#### Step 4.1.1: Prepare for Deployment

```bash
# 1. Create Procfile (for Render)
echo "web: cd services/model_service && uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# 2. Create render.yaml
cat > render.yaml << 'EOF'
services:
  - type: web
    name: autoops-model-service
    env: python
    region: oregon
    plan: free
    buildCommand: pip install -r services/model_service/requirements.txt
    startCommand: cd services/model_service && uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: MODEL_PATH
        value: ../../models/model.pkl
EOF

# 3. Commit changes
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

#### Step 4.1.2: Deploy to Render

1. Go to [render.com](https://render.com) and sign up (free)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Render will auto-detect `render.yaml`
5. Click **"Create Web Service"**
6. Wait 5-10 minutes for deployment
7. Your service will be live at: `https://autoops-model-service.onrender.com`

#### Step 4.1.3: Upload Model to Hugging Face (Free Storage)

```bash
# Install Hugging Face CLI
pip install huggingface_hub

# Login (get token from https://huggingface.co/settings/tokens)
huggingface-cli login

# Upload models
python scripts/upload_model_to_hf.py --repo-id YOUR_USERNAME/autoops-models

# Update your service to download models on startup
# Add to services/model_service/app/main.py startup:
```

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Download models from HF on startup
    from huggingface_hub import hf_hub_download
    import os
    
    if not os.path.exists("../../models/model.pkl"):
        print("Downloading models from Hugging Face...")
        hf_hub_download(
            repo_id="YOUR_USERNAME/autoops-models",
            filename="model.pkl",
            local_dir="../../models"
        )
    
    setup_telemetry()
    print("🚀 AutoOps Model Service started successfully!")
    yield
    print("🛑 AutoOps Model Service shutting down...")
```

### Option 2: Fly.io (Docker-based)

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh  # Mac/Linux
# or
iwr https://fly.io/install.ps1 -useb | iex  # Windows

# Login
fly auth login

# Launch app
cd services/model_service
fly launch --name autoops-model-service

# Deploy
fly deploy

# Your service is live at: https://autoops-model-service.fly.dev
```

### Option 3: Railway.app

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
cd services/model_service
railway init

# Deploy
railway up

# Get URL
railway domain
```

### Option 4: Hugging Face Spaces (ML-Focused)

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Choose **Docker** SDK
4. Clone your space:
```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/autoops-service
cd autoops-service

# Copy files
cp -r ../autoops/services/model_service/* .
cp ../autoops/models/* ./models/

# Create Dockerfile for HF (port 7860)
cat > Dockerfile << 'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ ./app/
COPY models/ ./models/
EXPOSE 7860
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
EOF

# Push
git add .
git commit -m "Deploy AutoOps"
git push
```

---

## 5. Monitor & Maintain

### Setup Free Monitoring

#### UptimeRobot (Uptime Monitoring)
1. Go to [uptimerobot.com](https://uptimerobot.com)
2. Add monitor: `https://your-app.onrender.com/health`
3. Get alerts via email/SMS

#### Grafana Cloud (Metrics & Dashboards)
1. Sign up at [grafana.com](https://grafana.com/products/cloud)
2. Create Prometheus data source
3. Point to: `https://your-app.onrender.com/metrics`
4. Import dashboard template

#### Better Stack (Logs)
1. Sign up at [betterstack.com](https://betterstack.com)
2. Create log source
3. Configure structured logging

### Keep Service Alive (Render Free Tier)

Render free tier sleeps after 15 minutes of inactivity. Keep it alive:

```bash
# Use cron-job.org to ping every 10 minutes
# Add job: curl https://your-app.onrender.com/health
```

Or use GitHub Actions:

```yaml
# .github/workflows/keep-alive.yml
name: Keep Service Alive
on:
  schedule:
    - cron: '*/10 * * * *'  # Every 10 minutes
jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - name: Ping service
        run: curl https://your-app.onrender.com/health
```

---

## 6. Advanced Features

### A. Add Custom Domain (Free)

**Render.com:**
1. Go to your service settings
2. Add custom domain
3. Update DNS records (CNAME)
4. Automatic HTTPS included!

### B. Set Up CI/CD

Your GitHub Actions workflow is already configured! Just push to trigger:

```bash
git add .
git commit -m "Update model"
git push origin main

# Automatically:
# 1. Runs tests
# 2. Builds Docker image
# 3. Deploys to production
```

### C. Add Authentication

```python
# services/model_service/app/api/auth.py
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

API_KEY = "your-secret-key"  # Use environment variable
api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key

# Use in endpoints:
@router.post("/predict")
async def predict(
    request: PredictionRequest,
    api_key: str = Depends(verify_api_key)
):
    ...
```

### D. Add Rate Limiting

```bash
pip install slowapi

# In app/main.py:
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/v1/predict")
@limiter.limit("100/minute")
async def predict(...):
    ...
```

### E. Add Model Versioning

```python
# Support multiple model versions
@router.post("/api/v1/predict")
async def predict(
    request: PredictionRequest,
    model_version: str = "latest"
):
    if model_version == "latest":
        predictor = get_model_predictor()
    else:
        predictor = load_model_version(model_version)
    ...
```

---

## 🎉 Congratulations!

You now have a **production-ready, AI-powered MLOps platform** deployed for **FREE**!

### What You've Built:

✅ **ML Training Pipeline**: Both scikit-learn and PyTorch  
✅ **REST API**: FastAPI with health checks and metrics  
✅ **Production Deployment**: Live on the internet  
✅ **Monitoring**: Uptime and performance tracking  
✅ **CI/CD**: Automated testing and deployment  
✅ **Model Storage**: Free cloud storage for models  
✅ **Observability**: Prometheus metrics and structured logs  

### Next Steps:

1. **Train on real data**: Replace synthetic data with your dataset
2. **Add more models**: Deploy multiple models simultaneously
3. **Scale up**: Upgrade to paid tiers when needed
4. **Add features**: Authentication, rate limiting, caching
5. **Share**: Make your API public or share with team

### Cost Breakdown:

- **Hosting**: $0/month (Render free tier)
- **Model Storage**: $0/month (Hugging Face)
- **Monitoring**: $0/month (UptimeRobot + Grafana Cloud free tier)
- **CI/CD**: $0/month (GitHub Actions)
- **Domain** (optional): $12/year (Namecheap)

**Total: $0/month** 🎉

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [PyTorch Tutorials](https://pytorch.org/tutorials)
- [Render Documentation](https://render.com/docs)
- [Hugging Face Hub](https://huggingface.co/docs/hub)
- [Prometheus Best Practices](https://prometheus.io/docs/practices)

## 🆘 Troubleshooting

**Service won't start:**
- Check logs: `fly logs` or Render dashboard
- Verify Python version: 3.11+
- Check model path in environment variables

**Model not loading:**
- Ensure model files are uploaded to HF
- Check download script runs on startup
- Verify file paths are correct

**Slow predictions:**
- Use PyTorch with GPU (upgrade to paid tier)
- Implement caching for common requests
- Optimize model size

**Out of memory:**
- Reduce batch size
- Use smaller model architecture
- Upgrade to larger instance

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/autoops/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/autoops/discussions)
- **Email**: your-email@example.com

---

**Built with ❤️ using AutoOps**
