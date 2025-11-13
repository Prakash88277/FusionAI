# 🚀 How to Use the AI Job Matching System

## ⚠️ IMPORTANT: First Time Setup

**The database is empty when you first start!** You need to populate it with jobs before uploading resumes.

---

## 📝 Step-by-Step Instructions

### Step 1: Start the Backend ✅ (Already Running)
```bash
cd backend
python -m uvicorn app.main:app --reload
```

**Status:** Backend is running on http://localhost:8000

---

### Step 2: Start the Frontend
```bash
cd frontend
npm start
```

**Opens:** http://localhost:3000

---

### Step 3: **POPULATE THE DATABASE** (REQUIRED FIRST TIME)

**Option A: Use the Scraper Control Page (Easiest)**

1. Go to http://localhost:3000/scraper
2. Click "🚀 Start Scraping Jobs Now"
3. Wait 30-60 seconds
4. Refresh stats to see jobs added

**Option B: Use API Call**
```bash
curl -X POST "http://localhost:8000/api/scraper/scrape-now"
```

**What happens:**
- Scrapes jobs from Internshala and Naukri
- Stores them in `backend/jobs.db`
- Takes 30-60 seconds
- Adds 50-100 jobs to database

---

### Step 4: Upload Your Resume

1. Go to http://localhost:3000 (Home page)
2. Click "Choose File"
3. Select your resume (PDF or DOCX)
4. Wait for processing (5-10 seconds)
5. Automatically redirects to Dashboard

---

### Step 5: View Matched Jobs

Dashboard shows:
- ✅ Jobs matched from database
- ✅ Match scores (0-100%)
- ✅ Matching skills highlighted
- ✅ Missing skills shown
- ✅ Real apply links

---

## 🔄 Daily Updates

**Automatic Scraping:**
- Runs every day at 2:00 AM
- Adds new jobs automatically
- No manual intervention needed

**Manual Scraping:**
- Use Scraper Control page anytime
- Or trigger via API
- Refreshes job database

---

## 📊 Check Database Status

**Via Scraper Page:**
- Go to http://localhost:3000/scraper
- See total jobs, active jobs, resumes
- See jobs by source

**Via API:**
```bash
curl http://localhost:8000/api/v2/resume/stats
```

---

## 🐛 Troubleshooting

### "No jobs found" on Dashboard

**Cause:** Database is empty

**Solution:**
1. Go to http://localhost:3000/scraper
2. Click "Start Scraping Jobs Now"
3. Wait 60 seconds
4. Go back to Dashboard
5. Click refresh button (🔄)

### Resume upload fails

**Check:**
1. Backend is running (http://localhost:8000)
2. File is PDF or DOCX
3. Check browser console (F12) for errors

### No matches after upload

**Possible reasons:**
1. Database has no jobs → Scrape first
2. Resume skills don't match any jobs
3. Match score threshold too high (default 30%)

---

## 💡 Tips

**For Best Results:**

1. **Scrape jobs first** before uploading resume
2. **Wait for scraping to complete** (30-60 seconds)
3. **Check database stats** to confirm jobs are added
4. **Upload resume** with clear skills listed
5. **View dashboard** to see matches

**Resume Tips:**
- List technical skills clearly (Python, Java, React, etc.)
- Include years of experience
- Use standard format (PDF/DOCX)
- Include education and certifications

---

## 🎯 Quick Test

**Test the entire system:**

```bash
# 1. Check backend health
curl http://localhost:8000/health

# 2. Trigger scraping
curl -X POST "http://localhost:8000/api/scraper/scrape-now"

# 3. Wait 60 seconds

# 4. Check stats
curl http://localhost:8000/api/v2/resume/stats

# 5. Upload resume via frontend
# Go to http://localhost:3000

# 6. View matches on dashboard
# Go to http://localhost:3000/dashboard
```

---

## 📍 Important URLs

- **Home:** http://localhost:3000
- **Dashboard:** http://localhost:3000/dashboard
- **Scraper Control:** http://localhost:3000/scraper
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## ✅ Success Indicators

**System is working when:**

✅ Backend shows "Application startup complete"
✅ Database stats show jobs > 0
✅ Resume upload succeeds without errors
✅ Dashboard shows matched jobs
✅ Match scores are displayed (30-100%)
✅ Apply buttons link to real job postings

---

## 🎉 You're All Set!

**Workflow:**
1. Scrape jobs (once or daily)
2. Upload resume
3. View matches
4. Apply to jobs
5. Repeat!

**The system will:**
- ✅ Scrape jobs daily at 2:00 AM
- ✅ Store everything in local database
- ✅ Match resumes intelligently
- ✅ Show best opportunities

**Good luck with your job search! 🚀**
