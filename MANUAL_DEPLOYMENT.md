# FusionAI - Manual Vercel Deployment Guide

## ⚠️ Terminal Login Required

The Vercel CLI requires browser-based authentication. Follow these steps:

---

## 🔐 Step 1: Authenticate with Vercel

### Option A: Using Terminal (Recommended)

1. **Run this command** in your terminal:
```bash
npx vercel login
```

2. **You'll see a message like:**
```
Visit https://vercel.com/oauth/device?user_code=RGGQ-MHLS
Press [ENTER] to open the browser
Waiting for authentication...
```

3. **Copy the URL** and open it in your browser
4. **Approve the authentication** in the browser
5. **Return to terminal** - it will automatically continue

### Option B: Manual Login

1. Go to https://vercel.com/login
2. Sign in with your account
3. Create a new token in Settings → Tokens
4. Use the token in terminal when prompted

---

## 🚀 Step 2: Deploy to Production

Once authenticated, run:

```bash
npx vercel --prod --yes
```

**Expected Output:**
```
Vercel CLI 48.10.2
✓ Linked to your-account/fusionai-job-search
✓ Inspect: https://vercel.com/your-account/fusionai-job-search/...
✓ Production: https://fusionai-job-search.vercel.app
```

---

## ⚙️ Step 3: Configure Environment Variables

After deployment, you need to set environment variables:

### Via Vercel Dashboard (Easiest)

1. Go to https://vercel.com/dashboard
2. Click on your project: `fusionai-job-search`
3. Go to **Settings** → **Environment Variables**
4. Add these variables:

| Name | Value |
|------|-------|
| `REACT_APP_API_BASE` | `https://fusionai-job-search.vercel.app/api` |
| `ZENROWS_API_KEY` | Your ZenRows API key |
| `PYTHONUNBUFFERED` | `1` |

5. Click **Save**

### Via CLI (Alternative)

```bash
npx vercel env add REACT_APP_API_BASE
# Enter: https://fusionai-job-search.vercel.app/api

npx vercel env add ZENROWS_API_KEY
# Enter: your_zenrows_api_key

npx vercel env add PYTHONUNBUFFERED
# Enter: 1
```

---

## 🔄 Step 4: Redeploy with Environment Variables

After adding environment variables, redeploy:

```bash
npx vercel --prod --yes
```

This will rebuild with the new environment variables.

---

## ✅ Step 5: Verify Deployment

### Test Your Deployment

```bash
# Replace with your actual project URL
curl https://fusionai-job-search.vercel.app/health

# Expected response:
# {"status":"healthy","scheduler":"running"}
```

### Visit Your Application

Open in browser:
```
https://fusionai-job-search.vercel.app
```

### Test API Endpoints

```bash
# Job search
curl "https://fusionai-job-search.vercel.app/api/jobs/search?limit=5"

# Database stats
curl https://fusionai-job-search.vercel.app/api/v2/resume/stats
```

---

## 🆘 Troubleshooting

### Issue: "Token is not valid"
**Solution:**
```bash
npx vercel logout
npx vercel login
# Follow browser authentication
```

### Issue: "Project not found"
**Solution:**
```bash
# First time? Create new project
npx vercel --prod --yes

# It will ask for project name
# Enter: fusionai-job-search
```

### Issue: Build fails
**Solution:**
1. Check Vercel dashboard build logs
2. Verify environment variables are set
3. Ensure requirements.txt has all dependencies
4. Check frontend/build directory exists

### Issue: API endpoints return 404
**Solution:**
1. Verify REACT_APP_API_BASE is set correctly
2. Check backend/api/index.py exists
3. Review Vercel logs for backend errors
4. Ensure routes are properly configured

---

## 📊 Deployment Checklist

- [ ] Run `npx vercel login`
- [ ] Authenticate in browser
- [ ] Run `npx vercel --prod --yes`
- [ ] Note your deployment URL
- [ ] Go to Vercel dashboard
- [ ] Add environment variables
- [ ] Redeploy with `npx vercel --prod --yes`
- [ ] Test health endpoint
- [ ] Visit frontend URL
- [ ] Test API endpoints
- [ ] Check browser console for errors

---

## 📝 Important Notes

### Project URL Format
Your project will be deployed to:
```
https://fusionai-job-search.vercel.app
```

Or if you chose a different name:
```
https://your-project-name.vercel.app
```

### Environment Variables
- **REACT_APP_API_BASE**: Must match your deployment URL
- **ZENROWS_API_KEY**: Get from your ZenRows account
- **PYTHONUNBUFFERED**: Set to 1 for proper logging

### Database
- SQLite database is ephemeral on Vercel
- Data persists during deployment but resets on redeploy
- For persistent storage, migrate to MongoDB or PostgreSQL

---

## 🎯 Success Indicators

✅ **Deployment Successful When:**
- Vercel shows "Ready" status
- Frontend loads without errors
- Health check returns `{"status":"healthy"}`
- Job search returns job data
- No 500 errors in logs

---

## 📞 Support

- **Vercel Docs**: https://vercel.com/docs
- **Vercel CLI Docs**: https://vercel.com/docs/cli
- **FastAPI Docs**: https://fastapi.tiangolo.com

---

## 🚀 Quick Commands Summary

```bash
# Login
npx vercel login

# Deploy
npx vercel --prod --yes

# View logs
npx vercel logs --prod

# Check status
npx vercel status

# Rollback
npx vercel rollback

# List deployments
npx vercel list
```

---

## ✨ Next Steps

1. **Now**: Run `npx vercel login`
2. **Then**: Authenticate in browser
3. **After**: Run `npx vercel --prod --yes`
4. **Finally**: Configure environment variables in dashboard

---

**Your project is ready to deploy!** 🎉
