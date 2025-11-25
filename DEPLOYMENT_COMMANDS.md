# FusionAI - Deployment Commands

## Prerequisites
- Vercel account created at https://vercel.com
- GitHub repository with project code
- Node.js and npm installed locally

## Deployment Steps

### Step 1: Verify Project Status
```bash
# Check if all required files exist
Test-Path "backend/requirements.txt"  # Should be True
Test-Path "backend/api/index.py"      # Should be True
Test-Path "frontend/build"             # Should be True
Test-Path "vercel.json"                # Should be True
```

### Step 2: Login to Vercel
```bash
npx vercel login
```
**Expected Output:**
```
? Log in to Vercel (Y/n) Y
? Which login method would you like to use? (Use arrow keys)
❯ GitHub
  GitLab
  Bitbucket
  Email
```

### Step 3: Deploy to Production
```bash
npx vercel --prod
```

**Expected Output:**
```
Vercel CLI 48.10.2
? Set up and deploy "C:\Users\...\Major Project"? (Y/n) Y
? Which scope do you want to deploy to? Your Scope
? Link to existing project? (y/N) N
? What's your project's name? fusionai-job-search
? In which directory is your code located? ./
? Want to modify these settings? (y/N) N
```

### Step 4: Wait for Deployment
The deployment will:
1. Build frontend (npm run build)
2. Install backend dependencies
3. Deploy both to Vercel
4. Provide deployment URL

**Expected Output:**
```
✓ Linked to your-account/fusionai-job-search (created .vercel)
✓ Inspect: https://vercel.com/your-account/fusionai-job-search/...
✓ Production: https://fusionai-job-search.vercel.app
```

### Step 5: Configure Environment Variables

Go to Vercel Dashboard → Project Settings → Environment Variables

Add these variables:
```
REACT_APP_API_BASE=https://fusionai-job-search.vercel.app/api
ZENROWS_API_KEY=your_zenrows_api_key_here
PYTHONUNBUFFERED=1
```

### Step 6: Redeploy with Environment Variables
```bash
npx vercel --prod
```

## Verification Commands

### Test Deployed Backend
```bash
# Health check
curl https://your-project.vercel.app/health

# Root endpoint
curl https://your-project.vercel.app/

# Job search
curl "https://your-project.vercel.app/api/jobs/search?limit=5"

# Database stats
curl https://your-project.vercel.app/api/v2/resume/stats
```

### Test Deployed Frontend
```bash
# Visit in browser
https://your-project.vercel.app
```

## Troubleshooting Commands

### View Deployment Logs
```bash
npx vercel logs --prod
```

### Check Project Status
```bash
npx vercel status
```

### List All Deployments
```bash
npx vercel list
```

### Rollback to Previous Version
```bash
npx vercel rollback
```

### Remove Project
```bash
npx vercel remove
```

## Common Issues & Solutions

### Issue: Build Fails with Python Error
```bash
# Solution: Check requirements.txt
cat backend/requirements.txt

# Verify Python version compatibility
python --version  # Should be 3.12+
```

### Issue: Frontend Build Fails
```bash
# Solution: Clear cache and rebuild
rm -r frontend/node_modules
npm install
npm run build
```

### Issue: API Routes Not Working
```bash
# Solution: Verify backend/api/index.py
cat backend/api/index.py

# Check if routes are included in app.main
grep "include_router" backend/app/main.py
```

### Issue: Environment Variables Not Set
```bash
# Solution: Check Vercel dashboard
# Project Settings → Environment Variables

# Or set via CLI
npx vercel env add REACT_APP_API_BASE
npx vercel env add ZENROWS_API_KEY
```

## Post-Deployment Checklist

- [ ] Deployment URL accessible
- [ ] Frontend loads without errors
- [ ] Backend health check passes
- [ ] Job search returns results
- [ ] Resume upload works
- [ ] Database stats endpoint responds
- [ ] No console errors in browser
- [ ] API responses are correct
- [ ] Error handling works
- [ ] Performance is acceptable

## Success Indicators

✅ **Deployment Successful When:**
- Frontend loads at https://your-project.vercel.app
- Backend API responds at https://your-project.vercel.app/api
- Health check returns {"status":"healthy"}
- Job search returns job data
- No 500 errors in logs

## Next Steps

1. Share deployment URL with users
2. Monitor Vercel dashboard for errors
3. Set up error tracking (Sentry, etc.)
4. Configure custom domain (optional)
5. Set up CI/CD for automatic deployments

## Support

- Vercel Status: https://www.vercelstatus.com
- Vercel Docs: https://vercel.com/docs
- FastAPI Docs: https://fastapi.tiangolo.com
- React Docs: https://react.dev
