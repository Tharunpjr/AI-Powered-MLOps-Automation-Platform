# 🎨 Frontend Setup Guide

## ✅ Frontend Directory Cleaned

The old frontend template has been removed. You can now add your own frontend!

---

## 📁 What's Left

Configuration files that you might need:

```
frontend/
├── .env.local              # Environment variables (API URL)
├── .env.local.example      # Example env file
├── .gitignore             # Git ignore rules
├── components.json        # shadcn/ui config (if using)
├── netlify.toml           # Netlify deployment config
├── next.config.mjs        # Next.js configuration
├── package.json           # Dependencies (update as needed)
├── postcss.config.mjs     # PostCSS config
└── tsconfig.json          # TypeScript config
```

---

## 🚀 Adding Your Frontend

### Option 1: Extract Your Files

1. **Extract your frontend files** into the `frontend/` directory
2. **Install dependencies**:
   ```powershell
   cd frontend
   npm install
   ```
3. **Update `.env.local`** with the backend URL:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```
4. **Start your frontend**:
   ```powershell
   npm run dev
   ```

### Option 2: Start Fresh

1. **Delete the frontend directory** entirely:
   ```powershell
   Remove-Item -Recurse -Force frontend
   ```
2. **Create your own frontend**:
   ```powershell
   # React
   npx create-react-app frontend
   
   # Next.js
   npx create-next-app@latest frontend
   
   # Vue
   npm create vue@latest frontend
   
   # Or any other framework
   ```
3. **Configure to connect to backend** at `http://localhost:8000`

---

## 🔌 Backend API

Your backend is still running and ready to use!

### API Endpoints

**Base URL**: `http://localhost:8000`

**Health & Info**
- `GET /` - Service information
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation

**ML Predictions**
- `POST /api/v1/predict` - Make predictions
- `GET /api/v1/model/info` - Model information

**AI/LLM**
- `POST /api/v1/llm/chat` - Chat with AI
- `POST /api/v1/llm/generate` - Generate text
- `POST /api/v1/llm/analyze` - Analyze text
- `POST /api/v1/llm/qa` - Question answering

**Monitoring**
- `GET /metrics` - Prometheus metrics

### API Documentation

Visit: **http://localhost:8000/docs**

Interactive Swagger UI with:
- All endpoints documented
- Try it out feature
- Request/response examples
- Schema definitions

---

## 📝 Example API Calls

### JavaScript/TypeScript

```typescript
// Chat with AI
const response = await fetch('http://localhost:8000/api/v1/llm/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'Hello!',
    conversation_history: []
  })
});
const data = await response.json();
console.log(data.result);

// ML Prediction
const prediction = await fetch('http://localhost:8000/api/v1/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    features: [5.1, 3.5, 1.4, 0.2]
  })
});
const result = await prediction.json();
console.log(result.prediction);

// Text Analysis
const analysis = await fetch('http://localhost:8000/api/v1/llm/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: 'This is amazing!',
    task: 'sentiment'
  })
});
const sentiment = await analysis.json();
console.log(sentiment.result); // "positive", "negative", or "neutral"
```

### Python

```python
import requests

# Chat
response = requests.post('http://localhost:8000/api/v1/llm/chat', json={
    'message': 'Hello!',
    'conversation_history': []
})
print(response.json()['result'])

# Prediction
response = requests.post('http://localhost:8000/api/v1/predict', json={
    'features': [5.1, 3.5, 1.4, 0.2]
})
print(response.json()['prediction'])
```

### cURL

```bash
# Chat
curl -X POST http://localhost:8000/api/v1/llm/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "conversation_history": []}'

# Prediction
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

---

## 🎯 What You Can Build

With the backend API, you can create:

1. **AI Chatbot Interface** - Chat with Google Gemini
2. **ML Prediction Dashboard** - Visualize model predictions
3. **Text Analysis Tool** - Sentiment analysis, summarization
4. **Question Answering System** - Q&A with context
5. **Admin Panel** - Model management and monitoring
6. **Mobile App** - React Native, Flutter, etc.
7. **Desktop App** - Electron, Tauri, etc.

---

## 🔧 Configuration Files

### .env.local (Important!)

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Add your own environment variables here
```

### package.json

Update dependencies as needed for your frontend framework.

### CORS

The backend already has CORS enabled for:
- `http://localhost:3000`
- `http://localhost:3001`
- `https://*.netlify.app`
- `https://*.vercel.app`

If you use a different port, update `services/model_service/app/main.py`:

```python
allow_origins=[
    "http://localhost:3000",
    "http://localhost:YOUR_PORT",  # Add your port
    # ...
]
```

---

## 🚀 Quick Start

1. **Add your frontend files** to `frontend/` directory
2. **Install dependencies**: `npm install`
3. **Configure API URL** in `.env.local`
4. **Start development**: `npm run dev`
5. **Test API connection** at http://localhost:8000/docs

---

## 📚 Resources

- **Backend API Docs**: http://localhost:8000/docs
- **Backend Source**: `services/model_service/app/`
- **API Endpoints**: `services/model_service/app/api/`
- **Models**: `services/model_service/app/model/`

---

## 🆘 Need Help?

- Check backend logs in the terminal
- Visit API docs: http://localhost:8000/docs
- Test endpoints with Swagger UI
- Check CORS settings if connection fails

---

**Your backend is ready! Build whatever frontend you want!** 🎨
