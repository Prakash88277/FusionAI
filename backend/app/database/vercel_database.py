"""
Vercel-compatible database service using in-memory data
Since Vercel doesn't support persistent SQLite, we'll use the 30 Google jobs as static data
"""

from typing import List, Dict, Any, Optional
from app.models.job import Job, JobType, ExperienceLevel
from datetime import datetime
import json

# Static data - the 30 Google jobs we kept
GOOGLE_JOBS_DATA = [
    {
        "id": "1",
        "title": "Software Engineer, Backend",
        "company": "Google",
        "location": "Bengaluru, Karnataka, India",
        "description": "Build and maintain scalable backend systems for Google's core products, focusing on performance and reliability.",
        "skills": ["Python", "Java", "Go", "Distributed Systems", "Microservices"],
        "apply_link": "https://careers.google.com/jobs/results/",
        "salary_text": "₹15-25 LPA",
        "source": "google",
        "job_type": "full_time",
        "experience_level": "mid"
    },
    {
        "id": "2",
        "title": "Software Engineer, Frontend",
        "company": "Google",
        "location": "Bengaluru, Karnataka, India",
        "description": "Develop user-facing features for Google's web applications using modern JavaScript frameworks and technologies.",
        "skills": ["JavaScript", "React", "TypeScript", "HTML", "CSS"],
        "apply_link": "https://careers.google.com/jobs/results/",
        "salary_text": "₹15-25 LPA",
        "source": "google",
        "job_type": "full_time",
        "experience_level": "mid"
    },
    {
        "id": "3",
        "title": "Software Engineer Intern",
        "company": "Google",
        "location": "Hyderabad, Telangana, India",
        "description": "Summer internship program for students to work on real Google products and gain hands-on experience.",
        "skills": ["Python", "Java", "JavaScript", "Data Structures", "Algorithms"],
        "apply_link": "https://careers.google.com/jobs/results/",
        "salary_text": "₹50k-80k/month",
        "source": "google",
        "job_type": "internship",
        "experience_level": "entry"
    },
    {
        "id": "4",
        "title": "Senior Software Engineer, Mobile (Android)",
        "company": "Google",
        "location": "Bengaluru, Karnataka, India",
        "description": "Lead Android development for Google's mobile applications, focusing on performance and user experience.",
        "skills": ["Android", "Kotlin", "Java", "Mobile Development", "UI/UX"],
        "apply_link": "https://careers.google.com/jobs/results/",
        "salary_text": "₹25-40 LPA",
        "source": "google",
        "job_type": "full_time",
        "experience_level": "senior"
    },
    {
        "id": "5",
        "title": "Software Engineer III, Machine Learning",
        "company": "Google",
        "location": "Bengaluru, Karnataka, India",
        "description": "Develop and deploy machine learning models for Google's products, working with large-scale data.",
        "skills": ["Python", "TensorFlow", "Machine Learning", "Data Science", "AI"],
        "apply_link": "https://careers.google.com/jobs/results/",
        "salary_text": "₹30-45 LPA",
        "source": "google",
        "job_type": "full_time",
        "experience_level": "senior"
    },
    {
        "id": "6",
        "title": "Staff Software Engineer, AI/ML",
        "company": "Google",
        "location": "Bengaluru, Karnataka, India",
        "description": "Senior technical leadership role for AI/ML systems, mentoring teams and driving product strategy.",
        "skills": ["Python", "Machine Learning", "AI", "Leadership", "System Design"],
        "apply_link": "https://careers.google.com/jobs/results/",
        "salary_text": "₹55-80 LPA",
        "source": "google",
        "job_type": "full_time",
        "experience_level": "senior"
    },
    {
        "id": "7",
        "title": "Software Engineer II, Google Ads",
        "company": "Google",
        "location": "Hyderabad, Telangana, India",
        "description": "Work on Google Ads platform, building features that help advertisers reach their customers effectively.",
        "skills": ["Java", "Python", "Distributed Systems", "Advertising Technology", "Scalability"],
        "apply_link": "https://careers.google.com/jobs/results/",
        "salary_text": "₹20-30 LPA",
        "source": "google",
        "job_type": "full_time",
        "experience_level": "mid"
    },
    {
        "id": "8",
        "title": "Technical Program Manager",
        "company": "Google",
        "location": "Bengaluru, Karnataka, India",
        "description": "Lead cross-functional teams to deliver complex technical projects, coordinating between engineering and product teams.",
        "skills": ["Project Management", "Technical Leadership", "Communication", "Strategy", "Agile"],
        "apply_link": "https://careers.google.com/jobs/results/",
        "salary_text": "₹25-40 LPA",
        "source": "google",
        "job_type": "full_time",
        "experience_level": "senior"
    },
    {
        "id": "9",
        "title": "Senior Embedded Software Engineer",
        "company": "Google",
        "location": "Bengaluru, Karnataka, India",
        "description": "Develop embedded software for Google's hardware products, working on low-level system programming.",
        "skills": ["C", "C++", "Embedded Systems", "Hardware", "Linux"],
        "apply_link": "https://careers.google.com/jobs/results/",
        "salary_text": "₹25-40 LPA",
        "source": "google",
        "job_type": "full_time",
        "experience_level": "senior"
    },
    {
        "id": "10",
        "title": "Software Development Engineer (PhD)",
        "company": "Google",
        "location": "Bengaluru, Karnataka, India",
        "description": "Research-focused role for PhD graduates to work on cutting-edge technology and publish research.",
        "skills": ["Research", "Python", "Machine Learning", "Algorithms", "Publications"],
        "apply_link": "https://careers.google.com/jobs/results/",
        "salary_text": "₹30-50 LPA",
        "source": "google",
        "job_type": "full_time",
        "experience_level": "senior"
    },
    {
        "id": "11",
        "title": "Software Engineer II, Platforms",
        "company": "Google",
        "location": "Hyderabad, Telangana, India",
        "description": "Build and maintain platform services that power Google's applications and infrastructure.",
        "skills": ["Java", "Python", "Kubernetes", "Cloud Computing", "DevOps"],
        "apply_link": "https://careers.google.com/jobs/results/",
        "salary_text": "₹20-30 LPA",
        "source": "google",
        "job_type": "full_time",
        "experience_level": "mid"
    },
    {
        "id": "12",
        "title": "Senior Software Engineer, Search",
        "company": "Google",
        "location": "Bengaluru, Karnataka, India",
        "description": "Work on Google Search infrastructure, improving search quality and performance for billions of users.",
        "skills": ["Java", "C++", "Distributed Systems", "Information Retrieval", "Algorithms"],
        "apply_link": "https://careers.google.com/jobs/results/",
        "salary_text": "₹30-45 LPA",
        "source": "google",
        "job_type": "full_time",
        "experience_level": "senior"
    },
    {
        "id": "13",
        "title": "Software Engineer III, ML Platform",
        "company": "Google",
        "location": "Bengaluru, Karnataka, India",
        "description": "Build machine learning platforms and tools used by thousands of engineers across Google.",
        "skills": ["Python", "TensorFlow", "Kubernetes", "ML Infrastructure", "Scalability"],
        "apply_link": "https://careers.google.com/jobs/results/",
        "salary_text": "₹25-40 LPA",
        "source": "google",
        "job_type": "full_time",
        "experience_level": "senior"
    },
    {
        "id": "14",
        "title": "Solution Specialist, Video and Media",
        "company": "Google",
        "location": "Mumbai, Maharashtra, India",
        "description": "Help media companies leverage Google's video and advertising technologies to grow their business.",
        "skills": ["Sales", "Technical Consulting", "Video Technology", "Client Management", "Presentations"],
        "apply_link": "https://careers.google.com/jobs/results/",
        "salary_text": "₹20-35 LPA",
        "source": "google",
        "job_type": "full_time",
        "experience_level": "mid"
    },
    {
        "id": "15",
        "title": "Software Engineer III, Search Quality",
        "company": "Google",
        "location": "Bengaluru, Karnataka, India",
        "description": "Improve search result quality through machine learning and algorithmic improvements.",
        "skills": ["Python", "Machine Learning", "Information Retrieval", "Data Analysis", "Statistics"],
        "apply_link": "https://careers.google.com/jobs/results/",
        "salary_text": "₹25-40 LPA",
        "source": "google",
        "job_type": "full_time",
        "experience_level": "senior"
    },
    {
        "id": "16",
        "title": "Site Reliability Engineer (SRE) III",
        "company": "Google",
        "location": "Bengaluru, Karnataka, India",
        "description": "Ensure the reliability and performance of Google's services through automation and monitoring.",
        "skills": ["Python", "Go", "Kubernetes", "Monitoring", "Automation"],
        "apply_link": "https://careers.google.com/jobs/results/",
        "salary_text": "₹25-40 LPA",
        "source": "google",
        "job_type": "full_time",
        "experience_level": "senior"
    },
    {
        "id": "17",
        "title": "Software Engineer, Payments",
        "company": "Google",
        "location": "Bengaluru, Karnataka, India",
        "description": "Build secure and scalable payment systems for Google's products and services.",
        "skills": ["Java", "Python", "Security", "Payments", "Distributed Systems"],
        "apply_link": "https://careers.google.com/jobs/results/",
        "salary_text": "₹20-30 LPA",
        "source": "google",
        "job_type": "full_time",
        "experience_level": "mid"
    },
    {
        "id": "18",
        "title": "Software Engineer III, Infrastructure",
        "company": "Google",
        "location": "Hyderabad, Telangana, India",
        "description": "Build and maintain the infrastructure that powers Google's global services and applications.",
        "skills": ["C++", "Python", "Distributed Systems", "Infrastructure", "Performance"],
        "apply_link": "https://careers.google.com/jobs/results/",
        "salary_text": "₹25-40 LPA",
        "source": "google",
        "job_type": "full_time",
        "experience_level": "senior"
    },
    {
        "id": "19",
        "title": "Software Engineer III, Distributed Systems",
        "company": "Google",
        "location": "Bengaluru, Karnataka, India",
        "description": "Design and implement large-scale distributed systems that handle billions of requests daily.",
        "skills": ["Java", "C++", "Distributed Systems", "Scalability", "Performance"],
        "apply_link": "https://careers.google.com/jobs/results/",
        "salary_text": "₹25-40 LPA",
        "source": "google",
        "job_type": "full_time",
        "experience_level": "senior"
    },
    {
        "id": "20",
        "title": "Software Engineer III, Data Systems",
        "company": "Google",
        "location": "Bengaluru, Karnataka, India",
        "description": "Build data processing systems that handle petabytes of data for Google's analytics and insights.",
        "skills": ["Java", "Python", "Big Data", "Data Processing", "Analytics"],
        "apply_link": "https://careers.google.com/jobs/results/",
        "salary_text": "₹25-40 LPA",
        "source": "google",
        "job_type": "full_time",
        "experience_level": "senior"
    },
    {
        "id": "21",
        "title": "Technical Program Manager, AI/ML",
        "company": "Google",
        "location": "Bengaluru, Karnataka, India",
        "description": "Lead AI/ML product launches and coordinate between research, engineering, and product teams.",
        "skills": ["Project Management", "AI/ML", "Technical Leadership", "Strategy", "Communication"],
        "apply_link": "https://careers.google.com/jobs/results/",
        "salary_text": "₹30-45 LPA",
        "source": "google",
        "job_type": "full_time",
        "experience_level": "senior"
    },
    {
        "id": "22",
        "title": "Senior Software Engineer, Frontend (Ads)",
        "company": "Google",
        "location": "Hyderabad, Telangana, India",
        "description": "Lead frontend development for Google Ads, creating intuitive interfaces for advertisers.",
        "skills": ["JavaScript", "React", "TypeScript", "UI/UX", "Performance"],
        "apply_link": "https://careers.google.com/jobs/results/",
        "salary_text": "₹25-40 LPA",
        "source": "google",
        "job_type": "full_time",
        "experience_level": "senior"
    },
    {
        "id": "23",
        "title": "Software Engineer II, Core Systems",
        "company": "Google",
        "location": "Bengaluru, Karnataka, India",
        "description": "Work on core systems that power Google's infrastructure and serve billions of users.",
        "skills": ["C++", "Java", "System Programming", "Performance", "Scalability"],
        "apply_link": "https://careers.google.com/jobs/results/",
        "salary_text": "₹20-30 LPA",
        "source": "google",
        "job_type": "full_time",
        "experience_level": "mid"
    },
    {
        "id": "24",
        "title": "Software Engineer II, Developer Tools",
        "company": "Google",
        "location": "Bengaluru, Karnataka, India",
        "description": "Build tools and platforms that help Google engineers be more productive and efficient.",
        "skills": ["Python", "Java", "Developer Tools", "Automation", "Productivity"],
        "apply_link": "https://careers.google.com/jobs/results/",
        "salary_text": "₹20-30 LPA",
        "source": "google",
        "job_type": "full_time",
        "experience_level": "mid"
    },
    {
        "id": "25",
        "title": "Software Engineer III, Robotics",
        "company": "Google",
        "location": "Bengaluru, Karnataka, India",
        "description": "Work on robotics and automation projects, combining software and hardware engineering.",
        "skills": ["Python", "C++", "Robotics", "Computer Vision", "Machine Learning"],
        "apply_link": "https://careers.google.com/jobs/results/",
        "salary_text": "₹25-40 LPA",
        "source": "google",
        "job_type": "full_time",
        "experience_level": "senior"
    },
    {
        "id": "26",
        "title": "Software Engineer III, Video Processing",
        "company": "Google",
        "location": "Hyderabad, Telangana, India",
        "description": "Develop video encoding and streaming technologies for YouTube and other Google services.",
        "skills": ["C++", "Video Processing", "Multimedia", "Performance", "Algorithms"],
        "apply_link": "https://careers.google.com/jobs/results/",
        "salary_text": "₹25-40 LPA",
        "source": "google",
        "job_type": "full_time",
        "experience_level": "senior"
    },
    {
        "id": "27",
        "title": "Security Engineer, Cloud Infrastructure",
        "company": "Google",
        "location": "Bengaluru, Karnataka, India",
        "description": "Implement security controls for Google Cloud's infrastructure, focusing on IAM and encryption.",
        "skills": ["Security", "Cloud Computing", "Python", "Cryptography", "Infrastructure"],
        "apply_link": "https://careers.google.com/jobs/results/",
        "salary_text": "₹25-40 LPA",
        "source": "google",
        "job_type": "full_time",
        "experience_level": "senior"
    },
    {
        "id": "28",
        "title": "Staff Software Engineer, Machine Learning",
        "company": "Google",
        "location": "Bengaluru, Karnataka, India",
        "description": "Senior technical leadership for ML systems, driving architecture decisions and mentoring teams.",
        "skills": ["Python", "Machine Learning", "System Design", "Leadership", "Architecture"],
        "apply_link": "https://careers.google.com/jobs/results/",
        "salary_text": "₹55-80 LPA",
        "source": "google",
        "job_type": "full_time",
        "experience_level": "senior"
    },
    {
        "id": "29",
        "title": "Software Engineer, Early Career (AdTech)",
        "company": "Google",
        "location": "Hyderabad, Telangana, India",
        "description": "Entry-level role working on advertising technology, with mentorship and learning opportunities.",
        "skills": ["Java", "Python", "Advertising Technology", "Learning", "Problem Solving"],
        "apply_link": "https://careers.google.com/jobs/results/",
        "salary_text": "₹15-20 LPA",
        "source": "google",
        "job_type": "full_time",
        "experience_level": "entry"
    },
    {
        "id": "30",
        "title": "Software Engineer III, Search Ranking",
        "company": "Google",
        "location": "Bengaluru, Karnataka, India",
        "description": "Work on search ranking algorithms that determine what billions of users see in search results.",
        "skills": ["Python", "Machine Learning", "Information Retrieval", "Algorithms", "Data Analysis"],
        "apply_link": "https://careers.google.com/jobs/results/",
        "salary_text": "₹30-45 LPA",
        "source": "google",
        "job_type": "full_time",
        "experience_level": "senior"
    }
]

class VercelDatabaseService:
    """Vercel-compatible database service using static data"""
    
    def __init__(self):
        self.jobs_data = GOOGLE_JOBS_DATA
    
    def get_jobs(self, 
                 keywords: Optional[str] = None,
                 location: Optional[str] = None,
                 company: Optional[str] = None,
                 country: Optional[str] = None,
                 job_type: Optional[str] = None,
                 experience_level: Optional[str] = None,
                 salary_min: Optional[int] = None,
                 salary_max: Optional[int] = None,
                 limit: int = 30) -> List[Job]:
        """Get jobs with filtering"""
        
        filtered_jobs = self.jobs_data.copy()
        
        # Apply keyword filtering
        if keywords:
            keyword_list = [k.strip().lower() for k in keywords.split(',') if k.strip()]
            if keyword_list:
                filtered_jobs = [
                    job for job in filtered_jobs
                    if any(
                        keyword in job['title'].lower() or
                        keyword in job['description'].lower() or
                        any(keyword in skill.lower() for skill in job['skills'])
                        for keyword in keyword_list
                    )
                ]
        
        # Apply other filters
        if location:
            filtered_jobs = [job for job in filtered_jobs if location.lower() in job['location'].lower()]
        
        if company:
            filtered_jobs = [job for job in filtered_jobs if company.lower() in job['company'].lower()]
        
        if job_type:
            filtered_jobs = [job for job in filtered_jobs if job['job_type'] == job_type.lower()]
        
        if experience_level:
            filtered_jobs = [job for job in filtered_jobs if job['experience_level'] == experience_level.lower()]
        
        # Convert to Job models
        jobs = []
        for job_data in filtered_jobs[:limit]:
            try:
                job = Job(
                    id=job_data['id'],
                    title=job_data['title'],
                    company=job_data['company'],
                    location=job_data['location'],
                    description=job_data['description'],
                    skills=job_data['skills'],
                    skills_required=job_data['skills'],
                    apply_link=job_data['apply_link'],
                    source=job_data['source'],
                    posted_date=datetime.now(),
                    scraped_date=datetime.now(),
                    job_type=JobType.FULL_TIME if job_data['job_type'] == 'full_time' else JobType.INTERNSHIP,
                    experience_level=ExperienceLevel.SENIOR if job_data['experience_level'] == 'senior' else ExperienceLevel.MID,
                    salary_text=job_data['salary_text'],
                    salary_currency="INR",
                    is_active=True
                )
                jobs.append(job)
            except Exception as e:
                print(f"Error creating job: {e}")
                continue
        
        return jobs
    
    def get_job_count(self) -> int:
        """Get total number of jobs"""
        return len(self.jobs_data)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        return {
            "total_jobs": len(self.jobs_data),
            "active_jobs": len(self.jobs_data),
            "jobs_by_source": {"google": len(self.jobs_data)}
        }

# Global instance
vercel_database_service = VercelDatabaseService()
