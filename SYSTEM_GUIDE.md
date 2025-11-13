# AI-Powered Job Matching System - Complete Guide

## 🎯 System Overview

This is a comprehensive job matching system that:
1. **Scrapes jobs daily** from multiple sources (Internshala, Naukri, etc.)
2. **Stores jobs** in a local SQLite database
3. **Parses resumes** to extract skills, experience, and keywords
4. **Matches resumes** with jobs using intelligent algorithms
5. **Displays matched jobs** on a beautiful React frontend

---

## 🏗️ Architecture

```
Frontend (React) → Backend API (FastAPI) → Database (SQLite)
                                        ↓
                                    Scrapers (Daily Schedule)
```

### Components:

**Backend:**
- `app/database/` - SQLite database models and connection
- `app/scrapers/` - Web scrapers for job sites
- `app/services/` - Resume parser and job matcher
- `app/api/routes/` - API endpoints

**Frontend:**
- `src/components/` - React components
- `src/pages/` - Page components
- `src/services/` - API service layer

---

## 🚀 Setup Instructions

### 1. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 3. Start the Backend

```bash
cd backend
python -m uvicorn app.main:app --reload
```

The backend will:
- ✅ Initialize SQLite database (`backend/jobs.db`)
- ✅ Start the daily scraping scheduler
- ✅ Run on `http://localhost:8000`

### 4. Start the Frontend

```bash
cd frontend
npm start
```

Frontend runs on `http://localhost:3000`

---

## 📊 How It Works

### Daily Job Scraping

The system automatically scrapes jobs **every day at 2:00 AM**:

```python
# Configured in: backend/app/scrapers/scheduler.py
schedule.every().day.at("02:00").do(scrape_jobs_task)
```

**Scraped Sources:**
- ✅ Internshala
- ✅ Naukri.com
- 🔄 More sources can be added easily

**What's Scraped:**
- Job title
- Company name
- Location
- Skills required
- Experience level
- Salary (if available)
- Apply link

### Resume Processing

When a user uploads a resume:

1. **Extract Text** from PDF/DOCX
2. **Parse Information:**
   - Name, email, phone
   - Technical skills (Python, Java, React, etc.)
   - Years of experience
   - Education
   - Certifications

3. **Match with Jobs:**
   - Compare resume skills with job requirements
   - Calculate match score (0-100%)
   - Consider experience level
   - Rank by relevance

4. **Display Results:**
   - Show top matching jobs
   - Highlight matching skills
   - Show missing skills
   - Provide apply links

---

## 🔧 API Endpoints

### Enhanced Resume API (V2)

**Upload and Match:**
```
POST /api/v2/resume/upload-and-match
- Uploads resume
- Parses skills and experience
- Matches with database jobs
- Returns top matches
```

**Get Matches:**
```
GET /api/v2/resume/matches/{resume_id}
- Retrieves matches for existing resume
```

**Database Stats:**
```
GET /api/v2/resume/stats
- Total jobs in database
- Jobs by source
- Total resumes processed
```

### Scraper Control

**Manual Scraping:**
```
POST /api/scraper/scrape-now
- Triggers immediate job scraping
- Runs in background
```

**Scraper Status:**
```
GET /api/scraper/scraper-status
- Shows available scrapers
- Current status
```

---

## 💾 Database Schema

### Jobs Table
```sql
- id: Primary key
- job_id: Unique identifier
- title: Job title
- company: Company name
- location: Job location
- skills: JSON array of required skills
- experience_min/max: Experience range
- source: Scraping source
- apply_link: Application URL
- scraped_at: Timestamp
```

### Resumes Table
```sql
- id: Primary key
- resume_id: Unique identifier
- filename: Original filename
- skills: JSON array of extracted skills
- experience_years: Years of experience
- education: JSON array
- uploaded_at: Timestamp
```

### Job Matches Table
```sql
- id: Primary key
- resume_id: Foreign key
- job_id: Foreign key
- match_score: Overall match (0-100)
- skill_match_score: Skills match
- experience_match_score: Experience match
- matching_skills: JSON array
- missing_skills: JSON array
```

---

## 🎨 Frontend Features

### Home Page
- Beautiful hero section
- Resume upload component
- How it works section

### Dashboard
- Grid of matched jobs
- Search functionality
- Match score badges
- Apply buttons with real links

### Job Cards
- Company and location
- Required skills
- Match percentage
- Experience level
- Salary (if available)

---

## 🔍 Matching Algorithm

The system uses a weighted scoring algorithm:

```python
Overall Match = (Skill Match × 70%) + (Experience Match × 30%)
```

**Skill Matching:**
- Compares resume skills with job requirements
- Calculates percentage of matching skills
- Lists missing skills

**Experience Matching:**
- Checks if candidate meets experience requirements
- Penalizes under-qualification more than over-qualification
- Considers experience ranges

---

## 🛠️ Manual Scraping

You can trigger scraping manually via:

1. **API Call:**
```bash
curl -X POST "http://localhost:8000/api/scraper/scrape-now?keywords=python&keywords=java&location=India&limit_per_source=100"
```

2. **Python Script:**
```python
from app.scrapers.scraper_manager import scraper_manager
from app.database.database import SessionLocal

db = SessionLocal()
result = scraper_manager.scrape_and_save(
    db=db,
    keywords=['python', 'java', 'developer'],
    location='India',
    limit_per_source=100
)
print(result)
```

---

## 📈 Testing the System

### 1. Check Backend Health
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "scheduler": "running"
}
```

### 2. Check Database Stats
```bash
curl http://localhost:8000/api/v2/resume/stats
```

### 3. Trigger Manual Scraping
```bash
curl -X POST "http://localhost:8000/api/scraper/scrape-now"
```

### 4. Upload Resume
- Go to http://localhost:3000
- Click "Choose File"
- Select your resume (PDF/DOCX)
- Wait for processing
- View matched jobs on dashboard

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill the process if needed
taskkill /PID <process_id> /F

# Restart backend
python -m uvicorn app.main:app --reload
```

### Database not initializing
```bash
# Delete old database
rm backend/jobs.db

# Restart backend (will recreate database)
python -m uvicorn app.main:app --reload
```

### No jobs in database
```bash
# Trigger manual scraping
curl -X POST "http://localhost:8000/api/scraper/scrape-now"

# Check logs for errors
# Look in terminal where backend is running
```

### Frontend can't connect to backend
- Ensure backend is running on port 8000
- Check CORS settings in `backend/app/main.py`
- Verify API_BASE in `frontend/src/services/api.js`

---

## 🎯 Adding New Scrapers

To add a new job site scraper:

1. Create new scraper file:
```python
# backend/app/scrapers/linkedin_scraper.py
from app.scrapers.base_scraper import BaseScraper

class LinkedInScraper(BaseScraper):
    def __init__(self):
        super().__init__("linkedin")
        self.base_url = "https://www.linkedin.com"
    
    def scrape(self, keywords, location, limit):
        # Implement scraping logic
        pass
```

2. Register in scraper manager:
```python
# backend/app/scrapers/scraper_manager.py
from app.scrapers.linkedin_scraper import LinkedInScraper

self.scrapers = {
    'internshala': IntershalaScraper(),
    'naukri': NaukriScraper(),
    'linkedin': LinkedInScraper(),  # Add here
}
```

---

## 📝 Key Files Reference

**Backend:**
- `app/main.py` - Main application entry point
- `app/database/models.py` - Database models
- `app/scrapers/scraper_manager.py` - Scraper coordinator
- `app/scrapers/scheduler.py` - Daily scheduling
- `app/services/enhanced_resume_parser.py` - Resume parsing
- `app/services/job_matcher.py` - Matching algorithm
- `app/api/routes/enhanced_resume.py` - Resume API endpoints

**Frontend:**
- `src/components/ResumeUpload.js` - Upload component
- `src/pages/Dashboard.js` - Job display
- `src/services/api.js` - API service layer

---

## 🎉 Success Indicators

System is working correctly when:

✅ Backend starts without errors
✅ Database file created (`backend/jobs.db`)
✅ Scheduler shows "running" in health check
✅ Manual scraping returns jobs
✅ Resume upload succeeds
✅ Dashboard shows matched jobs
✅ Match scores are reasonable (30-100%)
✅ Apply links work

---

## 📞 Support

If you encounter issues:

1. Check backend logs in terminal
2. Check browser console (F12) for frontend errors
3. Verify all dependencies are installed
4. Ensure database file exists and has data
5. Try manual scraping to populate database

---

## 🚀 Next Steps

**Enhancements to consider:**
- Add more job site scrapers
- Implement user authentication
- Add job bookmarking
- Email notifications for new matches
- Advanced filtering options
- Resume version history
- Application tracking

---

**System Status:** ✅ Fully Functional
**Last Updated:** 2025-01-29
**Version:** 2.0.0
