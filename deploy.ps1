# FusionAI Vercel Deployment Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "FusionAI - Vercel Deployment Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check if git is clean
Write-Host "[1/5] Checking git status..." -ForegroundColor Yellow
$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "⚠️  Uncommitted changes detected:" -ForegroundColor Yellow
    Write-Host $gitStatus
    $confirm = Read-Host "Continue with deployment? (y/n)"
    if ($confirm -ne "y") {
        Write-Host "❌ Deployment cancelled" -ForegroundColor Red
        exit 1
    }
}

# Step 2: Build frontend
Write-Host ""
Write-Host "[2/5] Building frontend..." -ForegroundColor Yellow
Set-Location frontend
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Frontend build failed" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Frontend build successful" -ForegroundColor Green
Set-Location ..

# Step 3: Verify backend files
Write-Host ""
Write-Host "[3/5] Verifying backend files..." -ForegroundColor Yellow
if (-not (Test-Path "backend/api/index.py")) {
    Write-Host "❌ backend/api/index.py not found" -ForegroundColor Red
    exit 1
}
if (-not (Test-Path "backend/requirements.txt")) {
    Write-Host "❌ backend/requirements.txt not found" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Backend files verified" -ForegroundColor Green

# Step 4: Deploy to Vercel
Write-Host ""
Write-Host "[4/5] Deploying to Vercel..." -ForegroundColor Yellow
Write-Host "Note: You may be prompted to login or confirm deployment" -ForegroundColor Cyan
npx vercel --prod

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Deployment failed" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Deployment successful" -ForegroundColor Green

# Step 5: Verify deployment
Write-Host ""
Write-Host "[5/5] Verifying deployment..." -ForegroundColor Yellow
Write-Host "Visit your Vercel dashboard to verify the deployment" -ForegroundColor Cyan
Write-Host "URL: https://vercel.com/dashboard" -ForegroundColor Cyan

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ Deployment Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
