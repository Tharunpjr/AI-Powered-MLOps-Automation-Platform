# 🏗️ AutoOps Architecture

## Full-Stack AI Platform Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│                     http://localhost:3000                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP/REST
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                      FRONTEND (Next.js)                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Landing   │  │  Dashboard  │  │   About     │             │
│  │    Page     │  │    Page     │  │    Page     │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                   │
│  ┌──────────────────────────────────────────────────┐           │
│  │           Dashboard Components                    │           │
│  ├──────────────────────────────────────────────────┤           │
│  │  • ML Predictions  • AI Chat                     │           │
│  │  • Text Analysis   • Model Info                  │           │
│  └──────────────────────────────────────────────────┘           │
│                                                                   │
│  ┌──────────────────────────────────────────────────┐           │
│  │              API Client (lib/api.ts)             │           │
│  │  • REST client  • Error handling                 │           │
│  │  • TypeScript types  • Toast notifications       │           │
│  └──────────────────────────────────────────────────┘           │
│                                                                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ REST API Calls
                             │ (JSON over HTTP)
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                     BACKEND (FastAPI)                            │
│                   http://localhost:8000                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────┐           │
│  │              API Endpoints                        │           │
│  ├──────────────────────────────────────────────────┤           │
│  │  /health          - Health check                 │           │
│  │  /metrics         - Prometheus metrics           │           │
│  │  /api/v1/predict  - ML predictions               │           │
│  │  /api/v1/llm/chat - AI chat                      │           │
│  │  /api/v1/llm/generate - Text generation          │           │
│  │  /api/v1/llm/analyze  - Text analysis            │           │
│  │  /docs            - Interactive API docs         │           │
│  └──────────────────────────────────────────────────┘           │
│                                                                   │
│  ┌──────────────────────────────────────────────────┐           │
│  │              Middleware                           │           │
│  ├──────────────────────────────────────────────────┤           │
│  │  • CORS (allow frontend)                         │           │
│  │  • Metrics collection                            │           │
│  │  • Request logging                               │           │
│  └──────────────────────────────────────────────────┘           │
│                                                                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│  Traditional  │  │    PyTorch    │  │      LLM      │
│      ML       │  │ Deep Learning │  │   (Gemini)    │
├───────────────┤  ├───────────────┤  ├───────────────┤
│               │  │               │  │               │
│ • scikit-     │  │ • Neural      │  │ • Google      │
│   learn       │  │   Networks    │  │   Gemini API  │
│ • Random      │  │ • Custom      │  │ • Chat        │
│   Forest      │  │   Models      │  │ • Generation  │
│ • XGBoost     │  │ • GPU/CPU     │  │ • Analysis    │
│               │  │   Support     │  │ • Q&A         │
│               │  │               │  │               │
└───────┬───────┘  └───────┬───────┘  └───────┬───────┘
        │                  │                  │
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  Model Storage  │
                  ├─────────────────┤
                  │ • models/*.pkl  │
                  │ • models/*.pt   │
                  │ • Metadata      │
                  └─────────────────┘
```

---

## 🔄 Request Flow

### 1. ML Prediction Flow
```
User Input (Frontend)
    │
    ├─ Enter features: [5.1, 3.5, 1.4, 0.2]
    │
    ▼
API Client (lib/api.ts)
    │
    ├─ POST /api/v1/predict
    ├─ Body: { features: [5.1, 3.5, 1.4, 0.2] }
    │
    ▼
FastAPI Backend
    │
    ├─ Load model from models/model.pkl
    ├─ Run prediction
    ├─ Return result
    │
    ▼
Frontend Display
    │
    └─ Show: "Prediction: 0 (Setosa)"
```

### 2. AI Chat Flow
```
User Message (Frontend)
    │
    ├─ "What is machine learning?"
    │
    ▼
API Client (lib/api.ts)
    │
    ├─ POST /api/v1/llm/chat
    ├─ Body: { message: "What is...", conversation_history: [] }
    │
    ▼
FastAPI Backend
    │
    ├─ Call Google Gemini API
    ├─ Process response
    │
    ▼
Gemini API
    │
    ├─ Generate intelligent response
    │
    ▼
Frontend Display
    │
    └─ Show AI response in chat interface
```

### 3. Text Analysis Flow
```
User Text (Frontend)
    │
    ├─ "This product is amazing!"
    │
    ▼
API Client (lib/api.ts)
    │
    ├─ POST /api/v1/llm/analyze
    ├─ Body: { text: "This product...", task: "sentiment" }
    │
    ▼
FastAPI Backend
    │
    ├─ Call Gemini for analysis
    │
    ▼
Frontend Display
    │
    └─ Show: "Sentiment: Positive (95% confidence)"
```

---

## 📦 Component Details

### Frontend Stack
- **Framework**: Next.js 15 (React 19)
- **Styling**: Tailwind CSS 4
- **UI Components**: Radix UI + shadcn/ui
- **Icons**: Lucide React
- **Animations**: Tailwind Animate
- **State**: React Hooks (useState, useEffect)
- **HTTP Client**: Fetch API
- **Notifications**: Sonner (toast)

### Backend Stack
- **Framework**: FastAPI
- **ML Libraries**: 
  - scikit-learn (traditional ML)
  - PyTorch (deep learning)
  - google-generativeai (LLM)
- **Metrics**: Prometheus
- **Validation**: Pydantic
- **ASGI Server**: Uvicorn
- **Serialization**: Pickle, PyTorch

### Data Flow
1. **User Input** → Frontend form/chat
2. **API Call** → REST client sends JSON
3. **Backend Processing** → FastAPI routes to model
4. **Model Inference** → ML/DL/LLM generates result
5. **Response** → JSON back to frontend
6. **Display** → React components render result

---

## 🔐 Security & Configuration

### Environment Variables

**Frontend (.env.local)**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Backend (environment)**
```env
GEMINI_API_KEY=your_api_key_here
MODEL_PATH=../../models/model.pkl
LOG_LEVEL=INFO
```

### CORS Configuration
Backend allows requests from:
- `http://localhost:3000` (dev)
- `https://*.netlify.app` (production)
- `https://*.vercel.app` (production)

---

## 📊 Monitoring & Observability

### Metrics Collected
- Request count by endpoint
- Request duration histograms
- Error rates
- Model inference time
- API response times

### Health Checks
- `/health` - Basic health status
- `/metrics` - Prometheus metrics
- Model loading status
- LLM API connectivity

---

## 🚀 Deployment Architecture

### Development
```
Local Machine
├── Terminal 1: Backend (port 8000)
└── Terminal 2: Frontend (port 3000)
```

### Production
```
Internet
    │
    ├─── Frontend (Netlify)
    │    └── https://autoops.netlify.app
    │
    └─── Backend (Render.com)
         └── https://autoops-api.onrender.com
```

---

## 🔄 Development Workflow

1. **Start Backend**: `.\start-backend.ps1`
2. **Start Frontend**: `.\start-frontend.ps1`
3. **Make Changes**: Edit files
4. **Auto Reload**: Both servers reload automatically
5. **Test**: Use browser and API docs
6. **Deploy**: Push to GitHub → Auto-deploy

---

## 📈 Scalability Considerations

### Current Setup (Free Tier)
- ✅ Perfect for demos and prototypes
- ✅ Handles 100s of requests/day
- ✅ Single instance deployment

### Scaling Up
- Add Redis for caching
- Use PostgreSQL for persistence
- Load balancer for multiple instances
- CDN for static assets
- Separate model serving instances

---

## 🎯 Key Design Decisions

1. **Monorepo Structure**: Frontend and backend in one repo for easy development
2. **REST API**: Simple, well-understood protocol
3. **TypeScript**: Type safety in frontend
4. **Pydantic**: Type validation in backend
5. **Modular Models**: Easy to add new model types
6. **Environment Config**: Flexible deployment options
7. **Free Hosting**: Zero cost to get started

---

## 🔮 Future Enhancements

- [ ] User authentication (JWT)
- [ ] Database integration (PostgreSQL)
- [ ] Chat history persistence
- [ ] Model versioning
- [ ] A/B testing framework
- [ ] Batch predictions
- [ ] WebSocket for real-time updates
- [ ] Model upload interface
- [ ] Custom model training UI
- [ ] Analytics dashboard

---

This architecture provides a solid foundation for building production-ready AI applications while keeping development simple and deployment free! 🚀
