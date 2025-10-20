# AutoOps Frontend Startup Script
# Run this to start the Next.js frontend

Write-Host "🎨 Starting AutoOps Frontend..." -ForegroundColor Cyan
Write-Host ""

# Navigate to frontend directory
Set-Location frontend

# Check if node_modules exists
if (-not (Test-Path "node_modules")) {
    Write-Host "📦 Installing dependencies (first time only)..." -ForegroundColor Yellow
    npm install
    Write-Host ""
}

Write-Host "✅ Dependencies ready" -ForegroundColor Green
Write-Host "📍 Starting dev server on http://localhost:3000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

# Start the dev server
npm run dev
