# Clean Frontend Script
# Removes frontend source files but keeps configuration

Write-Host "🧹 Cleaning frontend directory..." -ForegroundColor Cyan
Write-Host ""

$frontendPath = "frontend"

# Stop frontend if running
Write-Host "Stopping frontend process..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -like "*node*"} | Stop-Process -Force -ErrorAction SilentlyContinue

# Remove source directories
Write-Host "Removing source directories..." -ForegroundColor Yellow
Remove-Item -Path "$frontendPath/app" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$frontendPath/components" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$frontendPath/hooks" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$frontendPath/lib" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$frontendPath/public" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$frontendPath/styles" -Recurse -Force -ErrorAction SilentlyContinue

# Remove build artifacts
Write-Host "Removing build artifacts..." -ForegroundColor Yellow
Remove-Item -Path "$frontendPath/.next" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$frontendPath/node_modules" -Recurse -Force -ErrorAction SilentlyContinue

# Remove lock files
Write-Host "Removing lock files..." -ForegroundColor Yellow
Remove-Item -Path "$frontendPath/package-lock.json" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$frontendPath/pnpm-lock.yaml" -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "✅ Frontend cleaned!" -ForegroundColor Green
Write-Host ""
Write-Host "Kept configuration files:" -ForegroundColor Cyan
Write-Host "  - package.json (you may want to update this)" -ForegroundColor White
Write-Host "  - next.config.mjs" -ForegroundColor White
Write-Host "  - tsconfig.json" -ForegroundColor White
Write-Host "  - .env.local" -ForegroundColor White
Write-Host "  - .gitignore" -ForegroundColor White
Write-Host "  - netlify.toml" -ForegroundColor White
Write-Host ""
Write-Host "You can now extract your new frontend files here!" -ForegroundColor Green
Write-Host ""
