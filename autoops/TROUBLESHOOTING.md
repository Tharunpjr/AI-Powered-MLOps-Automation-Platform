# 🔧 AutoOps Troubleshooting Guide

Common issues and their solutions.

---

## 🚨 Quick Diagnostics

Run this first to check your setup:
```powershell
.\check-status.ps1
```

---

## Backend Issues

### ❌ "Port 8000 is already in use"

**Solution 1**: Kill the existing process
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill it (replace PID with actual process ID)
taskkill /PID <PID> /F
```

**Solution 2**: Use a different port
```powershell
cd services/model_service
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```
Then update frontend `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8001
```

---

### ❌ "ModuleNotFoundError: No module named 'fastapi'"

**Solution**: Install backend dependencies
```powershell
cd services/model_service
pip install -r requirements.txt
```

Or install individually:
```powershell
pip install fastapi uvicorn google-generativeai scikit-learn torch numpy pandas prometheus-client
```

---

### ❌ "Gemini API Error" or "Invalid API Key"

**Solution 1**: Check your API key
```powershell
# Verify it's set
echo $env:GEMINI_API_KEY

# Set it manually
$env:GEMINI_API_KEY = "your_actual_api_key_here"
```

**Solution 2**: Get a new API key
1. Visit: https://makersuite.google.com/app/apikey
2. Create a new API key
3. Update in `start-backend.ps1`

**Solution 3**: Check API quota
- Free tier has limits
- Wait a few minutes and try again
- Check Google Cloud Console for quota

---

### ❌ "Model file not found"

**Solution**: Models are created on first training
```powershell
# Train a simple model
cd autoops
python pipelines/training/train_pytorch.py
```

Or the backend will create a default model on first prediction.

---

### ❌ Backend starts but crashes immediately

**Check logs for specific error**:
```powershell
cd services/model_service
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug
```

Common causes:
- Missing dependencies → Install requirements.txt
- Python version too old → Use Python 3.8+
- Corrupted model file → Delete and retrain

---

## Frontend Issues

### ❌ "Port 3000 is already in use"

**Solution**: Next.js will automatically suggest port 3001
```
? Port 3000 is in use, would you like to use 3001 instead? › (Y/n)
```
Press `Y` and it will use 3001.

Or manually specify:
```powershell
npm run dev -- -p 3001
```

---

### ❌ "npm: command not found" or "node: command not found"

**Solution**: Install Node.js
1. Download from: https://nodejs.org/
2. Install LTS version (recommended)
3. Restart terminal
4. Verify: `node --version` and `npm --version`

---

### ❌ "npm install" fails or takes forever

**Solution 1**: Clear npm cache
```powershell
npm cache clean --force
npm install
```

**Solution 2**: Use different package manager
```powershell
# Install pnpm
npm install -g pnpm

# Use pnpm instead
pnpm install
```

**Solution 3**: Delete node_modules and retry
```powershell
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install
```

---

### ❌ "Cannot find module 'react'" or TypeScript errors

**Solution**: Install dependencies
```powershell
cd frontend
npm install
```

If still failing:
```powershell
# Clean install
Remove-Item -Recurse -Force node_modules
npm install
```

---

### ❌ Frontend loads but shows "Failed to fetch" errors

**Checklist**:
1. ✅ Is backend running? Check http://localhost:8000
2. ✅ Is `.env.local` correct?
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```
3. ✅ Check browser console (F12) for CORS errors
4. ✅ Restart both frontend and backend

**Solution**: Verify backend CORS settings
Backend should allow `http://localhost:3000` (already configured in `main.py`)

---

### ❌ "Hydration error" or React warnings

**Solution**: Clear Next.js cache
```powershell
cd frontend
Remove-Item -Recurse -Force .next
npm run dev
```

---

## Connection Issues

### ❌ Frontend can't connect to backend

**Debug steps**:

1. **Test backend directly**:
```powershell
# In browser or curl
curl http://localhost:8000/health
```

2. **Check frontend API URL**:
```powershell
cd frontend
type .env.local
```
Should show: `NEXT_PUBLIC_API_URL=http://localhost:8000`

3. **Check browser console** (F12):
- Look for CORS errors
- Look for network errors
- Check the actual URL being called

4. **Verify both are running**:
- Backend: http://localhost:8000 should show API info
- Frontend: http://localhost:3000 should show landing page

---

### ❌ "CORS policy" error in browser

**Solution**: Backend CORS is already configured, but verify:

1. Backend is running on port 8000
2. Frontend is running on port 3000
3. Restart both services

If using different ports, update backend `main.py`:
```python
allow_origins=[
    "http://localhost:3000",
    "http://localhost:3001",  # Add your port
    # ...
]
```

---

## Performance Issues

### ❌ Backend is slow to respond

**Causes**:
1. **First request**: Models load on first use (10-30 seconds)
2. **Gemini API**: External API calls take 1-3 seconds
3. **Large models**: PyTorch models can be slow on CPU

**Solutions**:
- Wait for first request to complete
- Use smaller models for testing
- Consider GPU for PyTorch models
- Cache responses for repeated queries

---

### ❌ Frontend is slow to load

**Solutions**:
```powershell
# Production build is faster
cd frontend
npm run build
npm start
```

Or optimize development:
- Close unused browser tabs
- Disable browser extensions
- Clear browser cache

---

## Deployment Issues

### ❌ Netlify build fails

**Common causes**:
1. **Wrong build directory**: Should be `frontend`
2. **Missing env vars**: Add `NEXT_PUBLIC_API_URL` in Netlify dashboard
3. **Build command**: Should be `npm run build`
4. **Publish directory**: Should be `.next`

**Solution**: Check Netlify build settings match:
```
Base directory: frontend
Build command: npm run build
Publish directory: .next
```

---

### ❌ Render deployment fails

**Common causes**:
1. **Missing requirements.txt**: Should be in `services/model_service/`
2. **Wrong start command**: Should be in `render.yaml`
3. **Missing env vars**: Add `GEMINI_API_KEY` in Render dashboard

**Solution**: Verify `render.yaml` is correct and push to GitHub

---

### ❌ Deployed app works but API calls fail

**Solution**: Update frontend environment variable

In Netlify dashboard:
```
NEXT_PUBLIC_API_URL = https://your-backend.onrender.com
```

Redeploy frontend after changing env vars.

---

## Development Issues

### ❌ Changes not reflecting

**Frontend**:
```powershell
# Hard refresh browser
Ctrl + Shift + R

# Or restart dev server
# Stop with Ctrl+C, then:
npm run dev
```

**Backend**:
```powershell
# Should auto-reload, but if not:
# Stop with Ctrl+C, then:
python -m uvicorn app.main:app --reload
```

---

### ❌ Git issues when deploying

**Solution**: Initialize git if needed
```powershell
cd autoops
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/autoops.git
git push -u origin main
```

---

## Still Having Issues?

### 📋 Gather Information

1. **Check versions**:
```powershell
python --version
node --version
npm --version
```

2. **Check logs**:
- Backend: Look at terminal output
- Frontend: Check browser console (F12)
- Network: Check Network tab in browser

3. **Test individually**:
- Backend: http://localhost:8000/docs
- Frontend: http://localhost:3000
- API: http://localhost:8000/health

### 🔍 Debug Mode

**Backend with debug logging**:
```powershell
cd services/model_service
python -m uvicorn app.main:app --reload --log-level debug
```

**Frontend with verbose output**:
```powershell
cd frontend
npm run dev -- --debug
```

### 📝 Create an Issue

If still stuck, create a GitHub issue with:
- Operating system
- Python version
- Node.js version
- Error messages (full text)
- Steps to reproduce
- What you've already tried

---

## 💡 Pro Tips

1. **Always check both terminals** - errors show in the terminal where the service is running
2. **Browser DevTools are your friend** - F12 shows network errors, console logs, etc.
3. **Start fresh** - Sometimes stopping everything and restarting helps
4. **Check the docs** - http://localhost:8000/docs shows all API endpoints
5. **One thing at a time** - Test backend first, then frontend

---

## ✅ Verification Checklist

Before asking for help, verify:

- [ ] Python 3.8+ installed
- [ ] Node.js 18+ installed
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (`npm install`)
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] `.env.local` exists in frontend folder
- [ ] `GEMINI_API_KEY` is set
- [ ] No firewall blocking ports
- [ ] Both terminals show no errors

---

Most issues are solved by:
1. Installing missing dependencies
2. Restarting the services
3. Checking environment variables
4. Verifying ports are correct

Good luck! 🚀
