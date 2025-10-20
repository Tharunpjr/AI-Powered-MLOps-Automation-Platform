# AutoOps Deployment Script
Write-Host "🚀 AutoOps Deployment Preparation" -ForegroundColor Green
Write-Host "=" * 50

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "📁 Initializing Git repository..." -ForegroundColor Yellow
    git init
    git add .
    git commit -m "Initial commit - AutoOps Platform"
} else {
    Write-Host "📁 Git repository already exists" -ForegroundColor Green
}

# Update requirements.txt
Write-Host "📦 Updating requirements.txt..." -ForegroundColor Yellow
pip freeze > requirements.txt

# Check required files
$requiredFiles = @(
    "production_backend.py",
    "requirements.txt", 
    "render.yaml",
    "frontend/netlify.toml",
    "frontend/next.config.js",
    "frontend/package.json"
)

Write-Host "`n✅ Checking deployment files..." -ForegroundColor Yellow
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✅ $file" -ForegroundColor Green
    } else {
        Write-Host "❌ $file (missing)" -ForegroundColor Red
    }
}

# Build frontend locally to test
Write-Host "`n🏗️ Testing frontend build..." -ForegroundColor Yellow
Set-Location frontend
try {
    npm run build
    Write-Host "✅ Frontend build successful" -ForegroundColor Green
} catch {
    Write-Host "❌ Frontend build failed" -ForegroundColor Red
}
Set-Location ..

# Commit changes
Write-Host "`n📤 Preparing for deployment..." -ForegroundColor Yellow
git add .
git status

Write-Host "`n🎯 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Push to GitHub: git push origin main" -ForegroundColor White
Write-Host "2. Deploy backend on Render: https://render.com" -ForegroundColor White
Write-Host "3. Deploy frontend on Netlify: https://netlify.com" -ForegroundColor White
Write-Host "4. Follow DEPLOYMENT_INSTRUCTIONS.md for detailed steps" -ForegroundColor White

Write-Host "`n🚀 Ready for deployment!" -ForegroundColor Green