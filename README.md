# AI Resume Job Matcher

An intelligent system that fuses different AI APIs into one intelligent job matching platform. Upload your resume and get matched with the perfect jobs using AI-powered analysis.

## Features

- **Resume Parsing**: Extract skills, experience, and education from PDF/DOCX resumes
- **Job Matching**: AI-powered job matching using TF-IDF and cosine similarity
- **Multiple Job Sources**: Scrape jobs from LinkedIn, Google Careers, Microsoft, Internshala, and more
- **Professional UI**: Modern, responsive dashboard with beautiful job cards
- **Advanced Filtering**: Filter by location, experience level, job type, and match score
- **Real-time Matching**: Instant job recommendations based on your resume

## Technology Stack

### Backend
- Python 3.12
- FastAPI
- scikit-learn (TF-IDF)
- spaCy (NLP)
- MongoDB (optional)
- Pydantic

### Frontend
- React.js
- Framer Motion
- Axios
- TailwindCSS (via inline styles)

## Installation

### Backend Setup

`ash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
`

### Frontend Setup

`ash
cd frontend
npm install
npm start
`

## Usage

1. Start the backend server (port 8000)
2. Start the frontend development server (port 3000)
3. Upload your resume in PDF or DOCX format
4. View matched jobs on the dashboard
5. Use filters to refine results
6. Apply directly through external links

## API Endpoints

- POST /api/resume/upload - Upload and parse resume
- POST /api/resume/upload-and-recommend - Upload resume and get recommendations
- GET /api/jobs/match/{resume_id} - Get matched jobs
- GET /api/jobs/search - Search for jobs
- GET /api/jobs/scrape - Scrape jobs from sources

## Project Structure

`
Major Project/
 backend/
    app/
       api/
          routes/
              auth.py
              jobs.py
              resume.py
       models/
          job.py
          resume.py
          user.py
       services/
          simple_resume_parser.py
          simple_job_aggregator.py
          simple_job_matcher.py
          simple_job_recommendation_service.py
          mock_job_service.py
          simple_scrapers.py
          auth.py
       main.py
    requirements.txt
 frontend/
     src/
        components/
           Navbar.js
           ResumeUpload.js
           JobCard.js
        pages/
           Home.js
           Dashboard.js
           Login.js
           Register.js
           JobDetails.js
        services/
           api.js
        App.js
     package.json
`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Author

Prakash Choudhary

## Acknowledgments

- FastAPI community
- React.js community
- All the AI/ML libraries that made this possible
