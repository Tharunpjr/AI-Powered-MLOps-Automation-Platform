# AutoOps Status Check Script
# Verifies your setup is ready to run

Write-Host "🔍 AutoOps Status Check" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# Check Python
Write-Host "Checking Python..." -NoNewline
try {
    $pythonVersion = python --version 2>&1
    Write-Host " ✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host " ❌ Python not found" -ForegroundColor Red
    $allGood = $false
}

# Check Node.js
Write-Host "Checking Node.js..." -NoNewline
try {
    $nodeVersion = node --version 2>&1
    Write-Host " ✅ $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host " ❌ Node.js not found" -ForegroundColor Red
    $allGood = $false
}

# Check npm
Write-Host "Checking npm..." -NoNewline
try {
    $npmVersion = npm --version 2>&1
    Write-Host " ✅ v$npmVersion" -ForegroundColor Green
} catch {
    Write-Host " ❌ npm not found" -ForegroundColor Red
    $allGood = $false
}

Write-Host ""

# Check Backend Files
Write-Host "Checking Backend..." -NoNewline
if (Test-Path "services/model_service/app/main.py") {
    Write-Host " ✅ Backend files found" -ForegroundColor Green
} else {
    Write-Host " ❌ Backend files missing" -ForegroundColor Red
    $allGood = $false
}

# Check Frontend Files
Write-Host "Checking Frontend..." -NoNewline
if (Test-Path "frontend/package.json") {
    Write-Host " ✅ Frontend files found" -ForegroundColor Green
} else {
    Write-Host " ❌ Frontend files missing" -ForegroundColor Red
    $allGood = $false
}

# Check Frontend Dependencies
Write-Host "Checking Frontend Dependencies..." -NoNewline
if (Test-Path "frontend/node_modules") {
    Write-Host " ✅ Installed" -ForegroundColor Green
} else {
    Write-Host " ⚠️  Not installed (run start-frontend.ps1)" -ForegroundColor Yellow
}

# Check Models
Write-Host "Checking ML Models..." -NoNewline
if (Test-Path "models/model.pkl") {
    Write-Host " ✅ Models found" -ForegroundColor Green
} else {
    Write-Host " ⚠️  Models not found (will be created on first run)" -ForegroundColor Yellow
}

# Check API Key
Write-Host "Checking Gemini API Key..." -NoNewline
if ($env:GEMINI_API_KEY) {
    Write-Host " ✅ Set in environment" -ForegroundColor Green
} else {
    Write-Host " ⚠️  Not set (will be set by start-backend.ps1)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================" -ForegroundColor Cyan

if ($allGood) {
    Write-Host "✅ All systems ready!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Run: .\start-backend.ps1  (in one terminal)" -ForegroundColor White
    Write-Host "2. Run: .\start-frontend.ps1 (in another terminal)" -ForegroundColor White
    Write-Host "3. Open: http://localhost:3000" -ForegroundColor White
} else {
    Write-Host "❌ Some requirements missing" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install missing dependencies:" -ForegroundColor Yellow
    Write-Host "- Python: https://www.python.org/downloads/" -ForegroundColor White
    Write-Host "- Node.js: https://nodejs.org/" -ForegroundColor White
}

Write-Host ""
