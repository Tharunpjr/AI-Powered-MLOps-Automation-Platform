# 🚀 AutoOps Deployment Guide - Render + Netlify

## 📋 **Overview**
Deploy your AutoOps platform with:
- **Backend**: Render (Free tier with PostgreSQL)
- **Frontend**: Netlify (Free tier with CDN)

---

## 🔧 **Backend Deployment (Render)**

### Step 1: Prepare Repository
1. Push your code to GitHub/GitLab
2. Ensure these files are in your root directory:
   - `production_backend.py`
   - `requirements.txt`
   - `render.yaml`
   - `models/` folder with your ML model

### Step 2: Deploy on Render
1. **Go to**: https://render.com
2. **Sign up/Login** with GitHub
3. **Click**: "New" → "Web Service"
4. **Connect**: Your GitHub repository
5. **Configure**:
   - **Name**: `autoops-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python production_backend.py`
   - **Plan**: Free

### Step 3: Environment Variables
Add these in Render dashboard:
```
GEMINI_API_KEY = AIzaSyBFlzrCZDE4vbDF6K5uE3-BkaxzM3N5_nM
DATABASE_URL = sqlite:///./autoops.db
PORT = 10000
```

### Step 4: Deploy
- Click **"Create Web Service"**
- Wait 5-10 minutes for deployment
- Your backend will be at: `https://autoops-backend.onrender.com`

---

## 🌐 **Frontend Deployment (Netlify)**

### Step 1: Prepare Frontend
1. Navigate to `frontend/` directory
2. Ensure these files exist:
   - `netlify.toml`
   - `next.config.js`
   - `package.json`

### Step 2: Deploy on Netlify
1. **Go to**: https://netlify.com
2. **Sign up/Login** with GitHub
3. **Click**: "Add new site" → "Import an existing project"
4. **Connect**: Your GitHub repository
5. **Configure**:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `out`

### Step 3: Environment Variables
Add in Netlify dashboard:
```
NEXT_PUBLIC_API_URL = https://autoops-backend.onrender.com
```

### Step 4: Deploy
- Click **"Deploy site"**
- Wait 2-5 minutes for deployment
- Your frontend will be at: `https://your-site-name.netlify.app`

---

## 🎯 **Quick Deploy Commands**

### For Backend (Render):
```bash
# 1. Ensure requirements.txt is up to date
pip freeze > requirements.txt

# 2. Commit and push to GitHub
git add .
git commit -m "Deploy to Render"
git push origin main
```

### For Frontend (Netlify):
```bash
# 1. Build locally to test
cd frontend
npm run build

# 2. Commit and push to GitHub
git add .
git commit -m "Deploy to Netlify"
git push origin main
```

---

## 🔗 **Expected URLs**

After deployment, your platform will be accessible at:

- **Frontend Dashboard**: `https://your-site-name.netlify.app/dashboard`
- **Backend API**: `https://autoops-backend.onrender.com`
- **API Documentation**: `https://autoops-backend.onrender.com/docs`

---

## ✅ **Deployment Checklist**

### Backend (Render):
- [ ] Repository connected to Render
- [ ] Environment variables set
- [ ] Build completes successfully
- [ ] Health check passes at `/health`
- [ ] API docs accessible at `/docs`

### Frontend (Netlify):
- [ ] Repository connected to Netlify
- [ ] Build completes successfully
- [ ] Environment variables set
- [ ] Site loads without errors
- [ ] API calls work to Render backend

---

## 🐛 **Troubleshooting**

### Common Issues:

1. **Backend Build Fails**:
   - Check `requirements.txt` has all dependencies
   - Ensure Python version compatibility
   - Check Render build logs

2. **Frontend Build Fails**:
   - Run `npm run build` locally first
   - Check for TypeScript errors
   - Ensure all dependencies in `package.json`

3. **API Connection Issues**:
   - Verify `NEXT_PUBLIC_API_URL` points to Render URL
   - Check CORS settings in backend
   - Ensure Render service is running

4. **Database Issues**:
   - SQLite works for development
   - For production, consider PostgreSQL on Render
   - Check database file permissions

---

## 🚀 **Production Optimizations**

### For Better Performance:
1. **Use PostgreSQL** instead of SQLite on Render
2. **Enable caching** for API responses
3. **Add monitoring** with Render metrics
4. **Set up custom domain** on Netlify
5. **Enable HTTPS** (automatic on both platforms)

---

## 💰 **Cost Breakdown**

### Free Tier Limits:
- **Render**: 750 hours/month, sleeps after 15min inactivity
- **Netlify**: 100GB bandwidth, 300 build minutes/month

### Upgrade Options:
- **Render Pro**: $7/month (always on, better performance)
- **Netlify Pro**: $19/month (more bandwidth, advanced features)

---

## 🎉 **Success!**

Once deployed, your AutoOps platform will be:
- ✅ **Publicly accessible** worldwide
- ✅ **Automatically scaled** by cloud providers
- ✅ **HTTPS secured** by default
- ✅ **Continuously deployed** from GitHub
- ✅ **Production ready** with monitoring

**Share your deployed platform with anyone using the Netlify URL!**