# AutoOps Backend Startup Script
# Run this to start the FastAPI backend

Write-Host "🚀 Starting AutoOps Backend..." -ForegroundColor Cyan
Write-Host ""

# Set Gemini API Key
$env:GEMINI_API_KEY = "AIzaSyBFlzrCZDE4vbDF6K5uE3-BkaxzM3N5_nM"

# Navigate to service directory
Set-Location services/model_service

Write-Host "✅ Gemini API Key configured" -ForegroundColor Green
Write-Host "📍 Starting server on http://localhost:8000" -ForegroundColor Yellow
Write-Host "📚 API docs available at http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

# Start the server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
