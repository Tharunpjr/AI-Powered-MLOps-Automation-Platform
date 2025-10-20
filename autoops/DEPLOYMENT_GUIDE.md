# AutoOps Free Deployment Guide

Complete guide to deploy AutoOps MLOps platform with **ZERO COST** using free-tier cloud services.

## 🎯 Deployment Options (All Free!)

### Option 1: Render.com (Recommended - Easiest)
**Best for**: Quick deployment, automatic HTTPS, zero config
- ✅ Free tier: 750 hours/month
- ✅ Automatic HTTPS
- ✅ Auto-deploy from GitHub
- ✅ Built-in monitoring

### Option 2: Railway.app
**Best for**: Developer-friendly, great DX
- ✅ $5 free credit/month
- ✅ GitHub integration
- ✅ Easy environment variables

### Option 3: Fly.io
**Best for**: Global edge deployment
- ✅ 3 VMs free (256MB RAM each)
- ✅ Global CDN
- ✅ Docker-native

### Option 4: Google Cloud Run
**Best for**: Scalability, pay-per-use
- ✅ 2 million requests/month free
- ✅ Auto-scaling
- ✅ Serverless

### Option 5: Hugging Face Spaces
**Best for**: ML/AI models, community sharing
- ✅ Completely free
- ✅ GPU support (limited)
- ✅ Built for ML

---

## 🚀 Quick Start: Deploy to Render.com (5 minutes)

### Step 1: Prepare Your Repository

1. **Push to GitHub** (if not already):
```bash
cd autoops
git init
git add .
git commit -m "Initial AutoOps setup"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/autoops.git
git push -u origin main
```

### Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub (free)
3. Authorize Render to access your repositories

### Step 3: Deploy Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your `autoops` repository
3. Configure:
   - **Name**: `autoops-model-service`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: `services/model_service`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`

4. **Environment Variables**:
   ```
   MODEL_PATH=../../models/model.pkl
   PYTHON_VERSION=3.11
   ```

5. Click **"Create Web Service"**

### Step 4: Train and Upload Model

Since Render doesn't persist files, use one of these approaches:

#### Option A: Use Cloud Storage (Recommended)
```bash
# Install AWS CLI or use S3-compatible storage
pip install boto3

# Upload trained model
python scripts/upload_model_to_s3.py
```

#### Option B: Embed Model in Docker Image
```bash
# Train model locally
python pipelines/training/train_pytorch.py --synthetic --out models/

# Build Docker image with model
docker build -t autoops-service -f services/model_service/Dockerfile .

# Push to Docker Hub
docker tag autoops-service YOUR_USERNAME/autoops-service:latest
docker push YOUR_USERNAME/autoops-service:latest
```

Then update Render to use Docker:
- **Runtime**: `Docker`
- **Dockerfile Path**: `services/model_service/Dockerfile`

---

## 🐳 Deploy to Fly.io (Docker-based)

### Step 1: Install Fly CLI
```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex

# Mac/Linux
curl -L https://fly.io/install.sh | sh
```

### Step 2: Login and Initialize
```bash
fly auth login
cd autoops/services/model_service
fly launch
```

### Step 3: Configure fly.toml
```toml
app = "autoops-model-service"

[build]
  dockerfile = "Dockerfile"

[env]
  PORT = "8000"
  MODEL_PATH = "/app/models/model.pkl"

[[services]]
  http_checks = []
  internal_port = 8000
  processes = ["app"]
  protocol = "tcp"

  [[services.ports]]
    force_https = true
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443

  [[services.tcp_checks]]
    grace_period = "10s"
    interval = "15s"
    restart_limit = 0
    timeout = "2s"

[mounts]
  source = "autoops_models"
  destination = "/app/models"
```

### Step 4: Deploy
```bash
# Create volume for models
fly volumes create autoops_models --size 1

# Deploy
fly deploy

# Check status
fly status

# View logs
fly logs
```

---

## ☁️ Deploy to Google Cloud Run

### Step 1: Setup Google Cloud
```bash
# Install gcloud CLI
# Visit: https://cloud.google.com/sdk/docs/install

# Login
gcloud auth login

# Create project
gcloud projects create autoops-project --name="AutoOps"
gcloud config set project autoops-project

# Enable APIs
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### Step 2: Build and Push Container
```bash
cd autoops/services/model_service

# Build for Cloud Run
gcloud builds submit --tag gcr.io/autoops-project/model-service

# Or use Docker
docker build -t gcr.io/autoops-project/model-service .
docker push gcr.io/autoops-project/model-service
```

### Step 3: Deploy to Cloud Run
```bash
gcloud run deploy autoops-model-service \
  --image gcr.io/autoops-project/model-service \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10 \
  --set-env-vars MODEL_PATH=/app/models/model.pkl
```

---

## 🤗 Deploy to Hugging Face Spaces

### Step 1: Create Space
1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Choose:
   - **Space name**: `autoops-model-service`
   - **License**: `MIT`
   - **SDK**: `Docker`
   - **Hardware**: `CPU basic` (free)

### Step 2: Create Dockerfile for HF Spaces
```dockerfile
# Create: services/model_service/Dockerfile.hf
FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ ./app/
COPY models/ ./models/

# Expose port (HF Spaces uses 7860)
EXPOSE 7860

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

### Step 3: Push to HF Space
```bash
# Clone your space
git clone https://huggingface.co/spaces/YOUR_USERNAME/autoops-model-service
cd autoops-model-service

# Copy files
cp -r ../autoops/services/model_service/* .
cp ../autoops/models/* ./models/

# Commit and push
git add .
git commit -m "Deploy AutoOps model service"
git push
```

---

## 🔧 Deploy to Railway.app

### Step 1: Install Railway CLI
```bash
npm install -g @railway/cli
# or
brew install railway
```

### Step 2: Login and Initialize
```bash
railway login
cd autoops/services/model_service
railway init
```

### Step 3: Configure and Deploy
```bash
# Set environment variables
railway variables set MODEL_PATH=../../models/model.pkl
railway variables set PYTHON_VERSION=3.11

# Deploy
railway up

# Get URL
railway domain
```

---

## 📦 Model Storage Solutions (Free)

### Option 1: GitHub Releases
```bash
# Create release with model
gh release create v1.0.0 models/model.pkl models/pytorch_model.pt

# Download in deployment
wget https://github.com/YOUR_USERNAME/autoops/releases/download/v1.0.0/model.pkl
```

### Option 2: Hugging Face Model Hub
```python
# Upload model
from huggingface_hub import HfApi
api = HfApi()
api.upload_file(
    path_or_fileobj="models/pytorch_model.pt",
    path_in_repo="pytorch_model.pt",
    repo_id="YOUR_USERNAME/autoops-models",
    repo_type="model"
)

# Download in deployment
from huggingface_hub import hf_hub_download
model_path = hf_hub_download(
    repo_id="YOUR_USERNAME/autoops-models",
    filename="pytorch_model.pt"
)
```

### Option 3: AWS S3 Free Tier
```python
import boto3

# Upload
s3 = boto3.client('s3')
s3.upload_file('models/model.pkl', 'autoops-models', 'model.pkl')

# Download
s3.download_file('autoops-models', 'model.pkl', '/app/models/model.pkl')
```

---

## 🔐 Environment Variables Setup

Create `.env` file (never commit this!):
```bash
# Model Configuration
MODEL_PATH=/app/models/model.pkl
MODEL_TYPE=auto

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO

# Cloud Storage (if using)
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
S3_BUCKET=autoops-models

# Monitoring
PROMETHEUS_ENABLED=true
GRAFANA_ENABLED=false
```

---

## 🧪 Testing Your Deployment

### Health Check
```bash
curl https://your-app.onrender.com/health
```

### Make Prediction
```bash
curl -X POST https://your-app.onrender.com/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0, 2.0, 3.0, 4.0]}'
```

### Check Metrics
```bash
curl https://your-app.onrender.com/metrics
```

---

## 📊 Monitoring (Free Tools)

### 1. UptimeRobot
- Free monitoring for 50 monitors
- Email/SMS alerts
- [uptimerobot.com](https://uptimerobot.com)

### 2. Grafana Cloud Free Tier
- 10k metrics series
- 50GB logs
- [grafana.com/products/cloud](https://grafana.com/products/cloud)

### 3. Better Stack (formerly Logtail)
- 1GB logs/month free
- [betterstack.com](https://betterstack.com)

---

## 🎯 Recommended Free Stack

**For Production-Ready Free Deployment:**

1. **Hosting**: Render.com (web service)
2. **Model Storage**: Hugging Face Model Hub
3. **Monitoring**: UptimeRobot + Grafana Cloud
4. **Logs**: Better Stack
5. **CI/CD**: GitHub Actions (included)
6. **Database** (if needed): Supabase (free tier)

**Total Cost: $0/month** 🎉

---

## 🚨 Important Notes

1. **Free tier limitations**:
   - Render: Service sleeps after 15 min inactivity
   - Railway: $5 credit/month (~500 hours)
   - Fly.io: 3 VMs with 256MB RAM each

2. **Keep services alive**:
   ```bash
   # Use cron-job.org to ping every 10 minutes
   curl https://your-app.onrender.com/health
   ```

3. **Model size limits**:
   - Keep models < 500MB for free tiers
   - Use model compression if needed

4. **Cold starts**:
   - First request may take 30-60 seconds
   - Subsequent requests are fast

---

## 📚 Next Steps

1. ✅ Deploy to Render.com (easiest)
2. ✅ Set up monitoring with UptimeRobot
3. ✅ Configure GitHub Actions for CI/CD
4. ✅ Add custom domain (optional, free with Render)
5. ✅ Set up Grafana dashboards

**Your AutoOps platform is now production-ready at ZERO COST!** 🚀
