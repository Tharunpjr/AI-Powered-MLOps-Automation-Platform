# 🎯 Get Started with AutoOps

**Your complete AI platform is ready!** This guide will get you up and running in minutes.

---

## 📚 Documentation Overview

We've created comprehensive guides for you:

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **GET_STARTED.md** (this file) | Quick overview and first steps | Start here! |
| **QUICKSTART.md** | Detailed setup instructions | Setting up for first time |
| **ARCHITECTURE.md** | System design and data flow | Understanding how it works |
| **TROUBLESHOOTING.md** | Common issues and solutions | When something goes wrong |
| **FULLSTACK_DEPLOYMENT.md** | Production deployment | Deploying to the internet |
| **README.md** | Project overview | General information |

---

## 🚀 Three Steps to Success

### Step 1: Verify Your Setup (30 seconds)

```powershell
cd autoops
.\check-status.ps1
```

This checks:
- ✅ Python installed
- ✅ Node.js installed
- ✅ Project files present
- ✅ Dependencies status

**If anything is missing**, the script will tell you what to install.

---

### Step 2: Start the Backend (1 minute)

Open a terminal and run:

```powershell
cd autoops
.\start-backend.ps1
```

You should see:
```
🚀 Starting AutoOps Backend...
✅ Gemini API Key configured
📍 Starting server on http://localhost:8000
```

**Test it**: Open http://localhost:8000 in your browser  
You should see API information and available endpoints.

**Troubleshooting**: If it fails, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

### Step 3: Start the Frontend (2 minutes)

Open a **new terminal** and run:

```powershell
cd autoops
.\start-frontend.ps1
```

First time? It will install dependencies (takes 1-2 minutes).

You should see:
```
🎨 Starting AutoOps Frontend...
📦 Installing dependencies...
✅ Dependencies ready
📍 Starting dev server on http://localhost:3000
```

**Open it**: Go to http://localhost:3000 in your browser

---

## 🎉 You're Running!

You should now see the AutoOps landing page with:
- Animated hero section
- Feature cards
- Navigation menu

### Try These Features:

1. **Click "Dashboard"** in the navigation
2. **ML Predictions Tab**:
   - Enter 4 numbers: `5.1, 3.5, 1.4, 0.2`
   - Click "Predict"
   - See the prediction result!

3. **AI Chat Tab**:
   - Type: "What is machine learning?"
   - Press Enter or click Send
   - Watch the AI respond!

4. **Text Analysis Tab**:
   - Enter: "This product is amazing!"
   - Select "Sentiment Analysis"
   - Click "Analyze"
   - See the sentiment result!

5. **Model Info Tab**:
   - View loaded models
   - Check system status
   - See model details

---

## 🎓 What You Just Built

### Frontend (http://localhost:3000)
- Modern Next.js application
- Beautiful UI with Tailwind CSS
- Real-time AI interactions
- Mobile responsive

### Backend (http://localhost:8000)
- FastAPI REST API
- Machine Learning models
- Google Gemini AI integration
- Auto-generated docs at `/docs`

### The Connection
- Frontend calls backend via REST API
- Real-time predictions and AI responses
- Error handling and loading states
- Toast notifications for feedback

---

## 📖 Next Steps

### Learn More

1. **Explore the API**:
   - Visit http://localhost:8000/docs
   - Try the interactive API documentation
   - Test endpoints directly

2. **Understand the Architecture**:
   - Read [ARCHITECTURE.md](ARCHITECTURE.md)
   - See how data flows
   - Learn about components

3. **Customize It**:
   - Edit frontend components in `frontend/components/`
   - Modify backend endpoints in `services/model_service/app/api/`
   - Add new features!

### Deploy to Production

When you're ready to share with the world:

1. Read [FULLSTACK_DEPLOYMENT.md](FULLSTACK_DEPLOYMENT.md)
2. Deploy backend to Render.com (free)
3. Deploy frontend to Netlify (free)
4. Share your live URL!

**Total cost**: $0/month for basic usage

---

## 🛠️ Development Workflow

### Making Changes

**Frontend Changes**:
1. Edit files in `frontend/` folder
2. Save the file
3. Browser auto-refreshes
4. See your changes instantly!

**Backend Changes**:
1. Edit files in `services/model_service/app/`
2. Save the file
3. Server auto-reloads
4. Test in browser or API docs

### Testing

**Manual Testing**:
- Use the web interface
- Check browser console (F12) for errors
- Watch terminal output for logs

**API Testing**:
- Use http://localhost:8000/docs
- Try different inputs
- Check responses

---

## 🎯 Common Tasks

### Add a New Frontend Component

```powershell
cd frontend/components
# Create your component file
# Import and use it in pages
```

### Add a New API Endpoint

```powershell
cd services/model_service/app/api
# Edit endpoints.py or create new file
# Add route with @router.post() or @router.get()
```

### Change the Gemini API Key

Edit `start-backend.ps1`:
```powershell
$env:GEMINI_API_KEY = "your_new_key_here"
```

### Use a Different Port

**Backend**:
```powershell
python -m uvicorn app.main:app --port 8001 --reload
```

**Frontend** (update `.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8001
```

---

## 🐛 Something Not Working?

### Quick Fixes

1. **Restart everything**:
   - Press Ctrl+C in both terminals
   - Run start scripts again

2. **Check the logs**:
   - Look at terminal output
   - Check browser console (F12)

3. **Verify setup**:
   ```powershell
   .\check-status.ps1
   ```

4. **Read troubleshooting guide**:
   - See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
   - Find your specific error
   - Follow the solution

### Still Stuck?

1. Check all terminals for error messages
2. Verify both services are running
3. Test backend directly: http://localhost:8000
4. Test frontend directly: http://localhost:3000
5. Check browser Network tab (F12)

---

## 💡 Pro Tips

1. **Keep both terminals visible** - You'll see errors immediately
2. **Use browser DevTools** - F12 is your best friend
3. **Check API docs** - http://localhost:8000/docs shows everything
4. **Save often** - Auto-reload makes development fast
5. **Test incrementally** - Make small changes and test

---

## 🎨 Customization Ideas

### Easy Wins
- Change colors in `frontend/styles/`
- Update text in components
- Add new dashboard tabs
- Modify landing page content

### Medium Difficulty
- Add new ML models
- Create new API endpoints
- Add charts and visualizations
- Implement user preferences

### Advanced
- Add authentication
- Integrate database
- Add file upload
- Create admin panel
- Build mobile app

---

## 📊 Project Stats

```
Frontend:
- Next.js 15 + React 19
- TypeScript for type safety
- Tailwind CSS for styling
- 20+ UI components

Backend:
- FastAPI + Python
- 3 model types (ML, DL, LLM)
- 10+ API endpoints
- Prometheus metrics

Total Lines of Code: ~5,000
Setup Time: 5 minutes
Cost: $0
```

---

## 🌟 What Makes This Special

1. **Complete Full-Stack**: Frontend + Backend + AI
2. **Production-Ready**: Health checks, metrics, error handling
3. **Free to Deploy**: Netlify + Render = $0/month
4. **Easy to Extend**: Add features without breaking things
5. **Well Documented**: Guides for everything
6. **Modern Stack**: Latest versions of everything
7. **Type Safe**: TypeScript + Pydantic
8. **Beautiful UI**: Professional design out of the box

---

## 🚀 You're Ready!

You now have:
- ✅ A running full-stack AI platform
- ✅ Beautiful web interface
- ✅ Powerful backend API
- ✅ Google Gemini AI integration
- ✅ Complete documentation
- ✅ Deployment guides

**What will you build?** 🎯

---

## 📞 Quick Reference

| What | Where | URL |
|------|-------|-----|
| Frontend | Browser | http://localhost:3000 |
| Backend | Browser | http://localhost:8000 |
| API Docs | Browser | http://localhost:8000/docs |
| Health Check | Browser | http://localhost:8000/health |
| Metrics | Browser | http://localhost:8000/metrics |

**Scripts**:
- `.\check-status.ps1` - Verify setup
- `.\start-backend.ps1` - Start backend
- `.\start-frontend.ps1` - Start frontend

**Docs**:
- `QUICKSTART.md` - Detailed setup
- `ARCHITECTURE.md` - How it works
- `TROUBLESHOOTING.md` - Fix issues
- `FULLSTACK_DEPLOYMENT.md` - Deploy it

---

Happy coding! 🎉
