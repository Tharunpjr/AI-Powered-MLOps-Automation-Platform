# 🚀 AutoOps Quick Start Guide

Get your full-stack AI platform running in 5 minutes!

---

## ✅ What's Ready

Your AutoOps platform includes:
- ✅ **Backend**: FastAPI with ML, PyTorch, and Google Gemini LLM
- ✅ **Frontend**: Next.js with beautiful UI and real-time AI features
- ✅ **API Integration**: Complete REST client connecting frontend to backend
- ✅ **Deployment Configs**: Ready for Netlify (frontend) and Render (backend)

---

## 🏃 Quick Start (Local Development)

### Step 1: Start the Backend (Terminal 1)

```powershell
cd autoops/services/model_service

# Set your Gemini API key
$env:GEMINI_API_KEY="AIzaSyBFlzrCZDE4vbDF6K5uE3-BkaxzM3N5_nM"

# Install dependencies (if not already done)
pip install -r requirements.txt

# Start the server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Backend will be running at: **http://localhost:8000**

Test it: Open http://localhost:8000 in your browser

### Step 2: Install Frontend Dependencies (Terminal 2)

```powershell
cd autoops/frontend

# Install dependencies (first time only)
npm install
```

### Step 3: Start the Frontend

```powershell
# Still in autoops/frontend
npm run dev
```

Frontend will be running at: **http://localhost:3000**

### Step 4: Try It Out! 🎉

Open http://localhost:3000 and:
1. Click "Dashboard" in the navigation
2. Try the **ML Predictions** tab
3. Chat with **AI** using Google Gemini
4. Analyze text **sentiment**
5. View **model information**

---

## 🎯 Features to Test

### 1. ML Predictions
- Enter 4 numbers (e.g., 5.1, 3.5, 1.4, 0.2)
- Click "Predict"
- See real-time prediction from your trained model

### 2. AI Chat
- Type any question
- Get intelligent responses from Google Gemini
- Conversation history is maintained

### 3. Text Analysis
- Enter any text
- Choose analysis type (sentiment, summary, etc.)
- Get AI-powered insights

### 4. Model Info
- View loaded models
- Check model versions
- See system status

---

## 🔧 Troubleshooting

### Backend Issues

**Port already in use?**
```powershell
# Use a different port
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

**Missing dependencies?**
```powershell
pip install fastapi uvicorn google-generativeai scikit-learn torch numpy pandas
```

**Gemini API not working?**
- Check your API key is set correctly
- Get a free key at: https://makersuite.google.com/app/apikey

### Frontend Issues

**Dependencies not installing?**
```powershell
# Try with npm
npm install

# Or use pnpm
npm install -g pnpm
pnpm install
```

**Port 3000 already in use?**
```powershell
# Next.js will automatically suggest port 3001
# Or specify a port:
npm run dev -- -p 3001
```

**Can't connect to backend?**
- Make sure backend is running on port 8000
- Check `.env.local` has correct API URL
- Look for CORS errors in browser console

---

## 📦 Project Structure

```
autoops/
├── services/model_service/     # Backend (FastAPI)
│   ├── app/
│   │   ├── main.py            # Main FastAPI app
│   │   ├── api/               # API endpoints
│   │   └── model/             # ML models & LLM integration
│   └── requirements.txt
│
├── frontend/                   # Frontend (Next.js)
│   ├── app/                   # Pages
│   ├── components/            # React components
│   ├── lib/                   # API client
│   └── package.json
│
├── models/                     # Trained models
├── QUICKSTART.md              # This file
└── FULLSTACK_DEPLOYMENT.md    # Production deployment guide
```

---

## 🚀 Next Steps

### Local Development
1. ✅ Backend running
2. ✅ Frontend running
3. ✅ Test all features
4. 🔄 Make changes and see live updates

### Production Deployment
When ready to deploy:
1. Read `FULLSTACK_DEPLOYMENT.md`
2. Deploy backend to Render.com (free)
3. Deploy frontend to Netlify (free)
4. Share your live URL!

### Enhancements
- Add user authentication
- Save chat history to database
- Upload custom models
- Add more AI features
- Customize the UI

---

## 💡 Tips

- **Backend auto-reloads** when you change Python files
- **Frontend auto-reloads** when you change React components
- Check **browser console** for frontend errors
- Check **terminal** for backend errors
- Use **http://localhost:8000/docs** for API documentation

---

## 🆘 Need Help?

1. Check the terminal output for errors
2. Look at browser console (F12)
3. Visit http://localhost:8000/docs for API docs
4. Read FULLSTACK_DEPLOYMENT.md for deployment help

---

## 🎉 You're All Set!

Your AutoOps AI platform is ready to use. Start building amazing AI-powered features! 🚀

**Backend**: http://localhost:8000  
**Frontend**: http://localhost:3000  
**API Docs**: http://localhost:8000/docs  
