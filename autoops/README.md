# AutoOps - AI-Powered MLOps Automation Toolkit

AutoOps is a complete **full-stack AI platform** with a beautiful Next.js frontend and powerful FastAPI backend. Build, deploy, and interact with ML models and LLMs through an intuitive web interface.

## 🆕 Complete Full-Stack Platform

### Frontend (Next.js + React)
- ✅ **Beautiful UI**: Modern, responsive design with smooth animations
- ✅ **AI Chat Interface**: Real-time chat with Google Gemini
- ✅ **ML Predictions**: Interactive model predictions with live results
- ✅ **Text Analysis**: Sentiment analysis and text processing
- ✅ **Model Dashboard**: View model info and system status
- ✅ **Mobile Responsive**: Works perfectly on all devices

### Backend (FastAPI + Python)
- ✅ **Large Language Models**: Google Gemini API integration
- ✅ **PyTorch Deep Learning**: Neural network training and inference
- ✅ **Traditional ML**: scikit-learn models (RandomForest, XGBoost)
- ✅ **REST API**: Complete API with auto-generated docs
- ✅ **Production-Ready**: Health checks, metrics, CORS enabled
- ✅ **Free Deployment**: Ready for Render.com and Netlify

## 🚀 Quick Start (5 Minutes)

```powershell
# 1. Check your setup
.\check-status.ps1

# 2. Start backend (Terminal 1)
.\start-backend.ps1

# 3. Start frontend (Terminal 2)
.\start-frontend.ps1

# 4. Open http://localhost:3000 🎉
```

## 📖 Documentation

**📚 [INDEX.md](INDEX.md)** - Complete documentation index

| Guide | Purpose |
|-------|---------|
| **[GET_STARTED.md](GET_STARTED.md)** | 👈 **Start here!** Complete beginner's guide |
| [WHY_AUTOOPS.md](WHY_AUTOOPS.md) | Why choose AutoOps? |
| [QUICKSTART.md](QUICKSTART.md) | Detailed setup instructions |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design and data flow |
| [FEATURES.md](FEATURES.md) | Complete feature list |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Common issues and solutions |
| [FULLSTACK_DEPLOYMENT.md](FULLSTACK_DEPLOYMENT.md) | Production deployment guide |

## ✨ What You Get

### 🎨 Frontend Features
- **Landing Page**: Animated hero, feature cards, responsive navigation
- **Dashboard**: Tabbed interface with ML predictions, AI chat, text analysis
- **Real-time Updates**: Live predictions and AI responses
- **Beautiful UI**: Tailwind CSS with smooth animations
- **Toast Notifications**: User-friendly error and success messages
- **Mobile Optimized**: Perfect experience on all screen sizes

### ⚡ Backend Features
- **Multiple Model Types**: Traditional ML, PyTorch, and LLMs in one API
- **Google Gemini Integration**: Powerful AI chat and text generation
- **Auto-generated Docs**: Interactive API docs at `/docs`
- **Prometheus Metrics**: Built-in monitoring and observability
- **Health Checks**: Kubernetes-ready health endpoints
- **CORS Enabled**: Ready for frontend integration

### 🛠️ Developer Experience
- **One-Click Start**: Simple PowerShell scripts to run everything
- **Hot Reload**: Both frontend and backend auto-reload on changes
- **Type Safety**: Full TypeScript support in frontend
- **API Client**: Pre-built REST client with error handling
- **Status Checker**: Verify your setup before starting

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Development](#development)
- [Deployment](#deployment)
- [Monitoring](#monitoring)
- [Contributing](#contributing)
- [License](#license)

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │    │  Training       │    │  Model Service  │
│                 │    │  Pipeline       │    │                 │
│ • CSV Files     │───▶│                 │───▶│ • FastAPI       │
│ • Databases     │    │ • Data Prep     │    │ • Health Checks │
│ • APIs          │    │ • Model Train   │    │ • Metrics       │
│                 │    │ • Evaluation    │    │ • Predictions   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Monitoring    │    │  Deployment     │    │  Infrastructure │
│                 │    │                 │    │                 │
│ • Prometheus    │    │ • Kubernetes    │    │ • Terraform     │
│ • Grafana       │    │ • Helm Charts   │    │ • Cloud Resources│
│ • Logging       │    │ • CI/CD         │    │ • Networking    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start (5 Minutes)

### Prerequisites

- Python 3.11+
- Git
- (Optional) Docker for containerized deployment

### 1. Clone and Setup

```bash
git clone https://github.com/YOUR_USERNAME/autoops.git
cd autoops

# Install dependencies
pip install -r services/model_service/requirements.txt
```

### 2. Train Models

#### Option A: Train scikit-learn Model
```bash
# Generate sample data
python -c "import pandas as pd; import numpy as np; np.random.seed(42); X = np.random.randn(1000, 4); y = np.sum(X, axis=1) + 0.1 * np.random.randn(1000); df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(4)]); df['target'] = y; df.to_csv('examples/sample_data/small_dataset.csv', index=False)"

# Train model
python pipelines/training/train.py --data examples/sample_data/small_dataset.csv --out models/
```

#### Option B: Train PyTorch Neural Network (NEW! 🔥)
```bash
# Train with synthetic data
python pipelines/training/train_pytorch.py --synthetic --out models/ --epochs 100 --hidden-sizes 64 32

# Or train with your data
python pipelines/training/train_pytorch.py --data your_data.csv --out models/ --epochs 200
```

### 3. Start the Service

```bash
cd services/model_service
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Test the Service

```bash
# Health check
curl http://localhost:8000/health

# Traditional ML prediction (works with both scikit-learn and PyTorch models!)
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0, 2.0, 3.0, 4.0]}'

# NEW: Chat with AI (requires GEMINI_API_KEY)
curl -X POST http://localhost:8000/api/v1/llm/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello! Tell me about machine learning."}'

# NEW: Generate text
curl -X POST http://localhost:8000/api/v1/llm/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write a poem about AI", "max_tokens": 100}'

# NEW: Analyze sentiment
curl -X POST http://localhost:8000/api/v1/llm/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this product!", "task": "sentiment"}'

# Get model info
curl http://localhost:8000/api/v1/model/info

# Check Prometheus metrics
curl http://localhost:8000/metrics
```

### 5. Deploy for FREE! 🎉

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for step-by-step instructions to deploy to:
- **Render.com** (Recommended - 5 minutes)
- **Fly.io** (Docker-based)
- **Railway.app** (Developer-friendly)
- **Google Cloud Run** (Scalable)
- **Hugging Face Spaces** (ML-focused)

**All options are FREE!** No credit card required.

## 📦 Installation

### Local Development

```bash
# Clone repository
git clone <repository-url>
cd autoops

# Setup environment
make setup

# Install dependencies
make install

# Generate sample data
make data

# Train model
make train

# Start service
make run
```

### Docker

```bash
# Build image
make build

# Run container
docker run -p 8000:8000 autoops/model-service:latest
```

### Kubernetes

```bash
# Deploy to Kubernetes
make deploy

# Deploy to specific namespace
make deploy-namespace NAMESPACE=my-namespace

# Dry run deployment
make deploy-dry-run
```

## 🛠️ Usage

### CLI Commands

```bash
# Start service
python cli/autoops_cli.py start

# Check status
python cli/autoops_cli.py status

# Train model
python cli/autoops_cli.py train --data data.csv --output models/

# Deploy
python cli/autoops_cli.py deploy --env production

# Run tests
python cli/autoops_cli.py test
```

### API Endpoints

- `GET /` - Service information
- `GET /health` - Health check
- `GET /health/ready` - Readiness check
- `GET /health/live` - Liveness check
- `GET /metrics` - Prometheus metrics
- `POST /api/v1/predict` - Make predictions
- `GET /api/v1/model/info` - Model information
- `POST /api/v1/model/reload` - Reload model

### Training Pipeline

```bash
# Train with custom data
python pipelines/training/train.py \
  --data your_data.csv \
  --out models/ \
  --model-type random_forest

# Evaluate model
python pipelines/training/evaluate.py \
  --model models/model.pkl \
  --data test_data.csv \
  --out evaluation_results.json
```

## 🔧 Development

### Project Structure

```
autoops/
├── .github/workflows/          # CI/CD pipelines
├── infra/                      # Infrastructure as Code
│   ├── terraform/             # Terraform configurations
│   └── k8s/                   # Kubernetes manifests
├── services/model_service/     # Model serving service
│   ├── app/                   # FastAPI application
│   ├── tests/                 # Unit tests
│   └── Dockerfile             # Container definition
├── pipelines/                 # ML pipelines
│   ├── training/              # Training scripts
│   └── dags/                  # Orchestration DAGs
├── scripts/                   # Utility scripts
├── cli/                       # Command-line interface
├── configs/                   # Configuration files
├── tests/                     # Integration tests
└── examples/                  # Examples and demos
```

### Development Commands

```bash
# Setup development environment
make setup

# Run linting
make lint

# Format code
make format

# Run tests
make test

# Run specific test types
make test-unit
make test-integration

# Build Docker image
make build

# Start development server
make run-dev
```

### Testing

```bash
# Run all tests
make test

# Run with coverage
make test-coverage

# Run unit tests only
make test-unit

# Run integration tests only
make test-integration
```

## 🚀 Deployment

### Local Deployment

```bash
# Build and run locally
make build
make run
```

### Kubernetes Deployment

```bash
# Deploy to Kubernetes
make deploy

# Deploy with specific namespace
make deploy-namespace NAMESPACE=autoops-prod

# Check deployment status
kubectl get pods -n autoops
kubectl get services -n autoops
```

### CI/CD Pipeline

The project includes GitHub Actions workflows for:

- **CI Pipeline**: Linting, testing, building, and pushing images
- **CD Pipeline**: Automated deployment to Kubernetes
- **Security Scanning**: Dependency and vulnerability checks

### Infrastructure Provisioning

```bash
# Initialize Terraform
cd infra/terraform
terraform init

# Plan infrastructure
terraform plan

# Apply infrastructure
terraform apply
```

## 📊 Monitoring

### Metrics

- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and dashboards
- **Custom Metrics**: Model performance and business metrics

### Health Checks

- **Liveness**: Service is running
- **Readiness**: Service is ready to serve requests
- **Health**: Overall service health

### Logging

- **Structured Logs**: JSON-formatted logs
- **Log Levels**: Configurable logging levels
- **Log Aggregation**: Centralized log collection

## 🔧 Configuration

### Environment Variables

```bash
# Copy example configuration
cp .env.example .env

# Edit configuration
nano .env
```

### Configuration Files

- `configs/default_config.yaml` - Main configuration
- `configs/logging_config.json` - Logging configuration
- `infra/terraform/variables.tf` - Infrastructure variables

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

### Development Setup

```bash
# Clone your fork
git clone <your-fork-url>
cd autoops

# Setup development environment
make setup

# Run tests
make test

# Run linting
make lint
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [Project Wiki](link-to-wiki)
- **Issues**: [GitHub Issues](link-to-issues)
- **Discussions**: [GitHub Discussions](link-to-discussions)
- **Email**: support@autoops.dev

## 🙏 Acknowledgments

- FastAPI for the web framework
- scikit-learn for machine learning
- Kubernetes for orchestration
- Prometheus for monitoring
- The open-source community

---

**AutoOps** - Making MLOps automation simple and reliable. 🚀
