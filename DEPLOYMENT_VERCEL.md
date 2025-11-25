# FusionAI - Vercel Deployment Guide

## Prerequisites

1. **Vercel Account**: Create account at https://vercel.com
2. **GitHub Repository**: Push code to GitHub
3. **Node.js & npm**: Installed locally
4. **Vercel CLI**: Install with `npm install -g vercel`

## Local Testing Before Deployment

### 1. Test Backend
```bash
cd backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Test Frontend
```bash
cd frontend
npm start
```

### 3. Test Production Build
```bash
cd frontend
npm run build
npm install -g serve
serve -s build
```

## Deployment Steps

### Step 1: Prepare Repository
```bash
# Ensure all changes are committed
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

### Step 2: Deploy with Vercel CLI
```bash
# Login to Vercel
vercel login

# Deploy from project root
vercel --prod
```

### Step 3: Configure Environment Variables

In Vercel Dashboard:
1. Go to Project Settings → Environment Variables
2. Add the following:
   - `REACT_APP_API_BASE`: `https://your-project.vercel.app/api`
   - `ZENROWS_API_KEY`: Your ZenRows API key

### Step 4: Verify Deployment

1. Check Vercel Dashboard for build status
2. Visit deployed URL
3. Test API endpoints:
   - `https://your-project.vercel.app/health`
   - `https://your-project.vercel.app/api/jobs/search?limit=5`

## Common Issues & Solutions

### Issue 1: Python Dependencies Not Installing
**Solution**: 
- Ensure `requirements.txt` is in backend directory
- Check Python version compatibility (3.12)
- Verify all packages have Windows wheels available

### Issue 2: Frontend Build Fails
**Solution**:
- Clear node_modules: `rm -r node_modules && npm install`
- Check for ESLint errors: `npm run build -- --verbose`
- Ensure all imports are correct

### Issue 3: API Routes Not Working
**Solution**:
- Verify `backend/api/index.py` exists
- Check CORS configuration in `app/main.py`
- Ensure routes are properly included in `app.main`

### Issue 4: Database Issues
**Solution**:
- SQLite database is stored in `/tmp` on Vercel (ephemeral)
- For persistent storage, migrate to MongoDB or PostgreSQL
- Current setup uses in-memory cache for jobs

## Production Checklist

- [ ] All environment variables configured
- [ ] Frontend build succeeds without warnings
- [ ] Backend API endpoints tested locally
- [ ] Database migrations completed
- [ ] CORS properly configured
- [ ] API keys secured (not in code)
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] Performance optimized
- [ ] Security headers added

## Rollback

If deployment fails:
```bash
# View deployment history
vercel list

# Rollback to previous version
vercel rollback
```

## Monitoring

1. **Vercel Dashboard**: Check build logs and analytics
2. **Error Tracking**: Monitor API errors
3. **Performance**: Check response times
4. **Usage**: Track API calls and bandwidth

## Support

For issues:
1. Check Vercel documentation: https://vercel.com/docs
2. Review build logs in Vercel Dashboard
3. Test locally before redeploying
