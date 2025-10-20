# 🔌 Backend Integration Guide

Your new frontend is ready! Here's how to connect it to the AutoOps backend.

---

## ✅ Setup Complete

- ✅ Frontend files extracted
- ✅ Files moved to correct location
- ✅ Environment configured (`.env.local`)
- ⏳ Dependencies installing...

---

## 🔗 Backend API Connection

### Environment Variable (Already Set!)

```env
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

This is already configured in your `.env.local` file.

---

## 📡 Available API Endpoints

### Base URL
```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
```

### Endpoints

**Health & Info**
```typescript
// Service info
GET ${API_URL}/

// Health check
GET ${API_URL}/health

// API documentation
GET ${API_URL}/docs
```

**ML Predictions**
```typescript
// Make prediction
POST ${API_URL}/api/v1/predict
Body: { features: [5.1, 3.5, 1.4, 0.2] }

// Get model info
GET ${API_URL}/api/v1/model/info

// Reload model
POST ${API_URL}/api/v1/model/reload
```

**AI/LLM Features**
```typescript
// Chat with AI
POST ${API_URL}/api/v1/llm/chat
Body: { 
  message: "Hello!",
  conversation_history: []
}

// Generate text
POST ${API_URL}/api/v1/llm/generate
Body: {
  prompt: "Write a story about...",
  max_tokens: 100,
  temperature: 0.7
}

// Analyze text (sentiment, summary, etc.)
POST ${API_URL}/api/v1/llm/analyze
Body: {
  text: "This is amazing!",
  task: "sentiment"  // Returns: "positive", "negative", or "neutral"
}

// Question answering
POST ${API_URL}/api/v1/llm/qa
Body: {
  question: "What is AI?",
  context: "optional context..."
}

// List available models
GET ${API_URL}/api/v1/llm/models

// LLM status
GET ${API_URL}/api/v1/llm/status
```

**Monitoring**
```typescript
// Prometheus metrics
GET ${API_URL}/metrics
```

---

## 💻 Example API Client

Create `src/lib/api.ts`:

```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const api = {
  // Chat with AI
  async chat(message: string, history: any[] = []) {
    const res = await fetch(`${API_URL}/api/v1/llm/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        message, 
        conversation_history: history 
      })
    })
    return res.json()
  },

  // ML Prediction
  async predict(features: number[]) {
    const res = await fetch(`${API_URL}/api/v1/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ features })
    })
    return res.json()
  },

  // Text Analysis
  async analyzeSentiment(text: string) {
    const res = await fetch(`${API_URL}/api/v1/llm/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, task: 'sentiment' })
    })
    return res.json()
  },

  // Generate Text
  async generateText(prompt: string, maxTokens = 100) {
    const res = await fetch(`${API_URL}/api/v1/llm/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        prompt, 
        max_tokens: maxTokens,
        temperature: 0.7
      })
    })
    return res.json()
  },

  // Model Info
  async getModelInfo() {
    const res = await fetch(`${API_URL}/api/v1/model/info`)
    return res.json()
  },

  // Health Check
  async healthCheck() {
    const res = await fetch(`${API_URL}/health`)
    return res.json()
  }
}
```

---

## 🎯 Usage Examples

### In a React Component

```typescript
'use client'

import { useState } from 'react'
import { api } from '@/lib/api'

export function ChatComponent() {
  const [message, setMessage] = useState('')
  const [response, setResponse] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChat = async () => {
    setLoading(true)
    try {
      const result = await api.chat(message)
      setResponse(result.result)
    } catch (error) {
      console.error('Chat error:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <input 
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Ask me anything..."
      />
      <button onClick={handleChat} disabled={loading}>
        {loading ? 'Thinking...' : 'Send'}
      </button>
      {response && <p>{response}</p>}
    </div>
  )
}
```

### Sentiment Analysis

```typescript
'use client'

import { useState } from 'react'
import { api } from '@/lib/api'

export function SentimentAnalyzer() {
  const [text, setText] = useState('')
  const [sentiment, setSentiment] = useState('')

  const analyze = async () => {
    const result = await api.analyzeSentiment(text)
    setSentiment(result.result) // "positive", "negative", or "neutral"
  }

  return (
    <div>
      <textarea 
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Enter text to analyze..."
      />
      <button onClick={analyze}>Analyze Sentiment</button>
      {sentiment && (
        <div className={`sentiment-${sentiment}`}>
          Sentiment: {sentiment}
        </div>
      )}
    </div>
  )
}
```

### ML Prediction

```typescript
'use client'

import { useState } from 'react'
import { api } from '@/lib/api'

export function MLPredictor() {
  const [features, setFeatures] = useState([5.1, 3.5, 1.4, 0.2])
  const [prediction, setPrediction] = useState<number | null>(null)

  const predict = async () => {
    const result = await api.predict(features)
    setPrediction(result.prediction)
  }

  return (
    <div>
      <input 
        type="text"
        value={features.join(', ')}
        onChange={(e) => setFeatures(e.target.value.split(',').map(Number))}
        placeholder="Enter features (comma-separated)"
      />
      <button onClick={predict}>Predict</button>
      {prediction !== null && (
        <div>Prediction: {prediction}</div>
      )}
    </div>
  )
}
```

---

## 🚀 Start Your Frontend

Once npm install completes:

```powershell
npm run dev
```

Your frontend will start on **http://localhost:3000**

---

## 🔍 Testing the Connection

1. **Start Backend** (if not running):
   ```powershell
   cd services/model_service
   $env:GEMINI_API_KEY="AIzaSyBFlzrCZDE4vbDF6K5uE3-BkaxzM3N5_nM"
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Test Backend**:
   - Visit: http://localhost:8000
   - API Docs: http://localhost:8000/docs

3. **Start Frontend**:
   ```powershell
   cd frontend
   npm run dev
   ```

4. **Test Connection**:
   - Open browser console (F12)
   - Try: `fetch('http://localhost:8000/health').then(r => r.json()).then(console.log)`

---

## 🎨 Your Frontend Structure

```
src/
├── app/
│   ├── dashboard/      # Dashboard pages
│   ├── docs/          # Documentation
│   ├── playground/    # Playground/testing
│   └── page.tsx       # Home page
├── components/
│   ├── ui/           # UI components
│   ├── LandingPage.tsx
│   └── Navigation.tsx
├── hooks/            # Custom hooks
└── lib/
    └── utils.ts      # Utilities
```

Add your API client to `src/lib/api.ts`!

---

## 🆘 Troubleshooting

**CORS Error?**
- Backend already has CORS enabled for localhost:3000
- Check if backend is running on port 8000

**Connection Refused?**
- Make sure backend is running: http://localhost:8000
- Check `.env.local` has correct URL

**API Not Found?**
- Visit http://localhost:8000/docs to see all endpoints
- Check endpoint paths match exactly

---

**Your backend is ready and waiting! Start building! 🚀**
