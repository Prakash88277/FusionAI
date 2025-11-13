"""
Add high-quality jobs with real apply links to the database
"""
import sqlite3
import uuid
from datetime import datetime, timedelta
import random
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_quality_jobs():
    """Add realistic jobs with proper apply links"""
    
    quality_jobs = [
        # Google Jobs
        {
            "title": "Software Engineer, Backend",
            "company": "Google",
            "location": "Bangalore, India",
            "description": "Design, develop, test, deploy, maintain, and enhance software solutions. Work with large-scale systems and cutting-edge technologies.",
            "skills": ["Python", "Java", "Go", "Distributed Systems", "Cloud Computing"],
            "apply_link": "https://careers.google.com/jobs/results/",
            "salary_text": "₹25-40 LPA",
            "source": "google",
            "job_type": "full_time",
            "experience_level": "mid"
        },
        {
            "title": "Software Engineer, Frontend",
            "company": "Google",
            "location": "Hyderabad, India", 
            "description": "Build user-facing features for Google products. Work with modern web technologies and frameworks.",
            "skills": ["JavaScript", "TypeScript", "React", "Angular", "CSS"],
            "apply_link": "https://careers.google.com/jobs/results/",
            "salary_text": "₹22-35 LPA",
            "source": "google",
            "job_type": "full_time",
            "experience_level": "mid"
        },
        
        # Microsoft Jobs
        {
            "title": "Software Engineer",
            "company": "Microsoft",
            "location": "Hyderabad, India",
            "description": "Join Microsoft to build cloud solutions and enterprise software. Work with Azure, .NET, and modern development practices.",
            "skills": ["C#", "Azure", ".NET", "JavaScript", "SQL Server"],
            "apply_link": "https://careers.microsoft.com/professionals/us/en/search-results",
            "salary_text": "₹18-30 LPA",
            "source": "microsoft",
            "job_type": "full_time",
            "experience_level": "mid"
        },
        {
            "title": "Cloud Solution Architect",
            "company": "Microsoft",
            "location": "Bangalore, India",
            "description": "Design and implement cloud solutions for enterprise customers. Deep Azure knowledge required.",
            "skills": ["Azure", "Cloud Architecture", "PowerShell", "ARM Templates", "DevOps"],
            "apply_link": "https://careers.microsoft.com/professionals/us/en/search-results",
            "salary_text": "₹25-40 LPA",
            "source": "microsoft",
            "job_type": "full_time",
            "experience_level": "senior"
        },
        
        # Amazon Jobs
        {
            "title": "Software Development Engineer",
            "company": "Amazon",
            "location": "Bangalore, India",
            "description": "Build scalable systems for Amazon's e-commerce platform. Work with distributed systems and cloud technologies.",
            "skills": ["Java", "Python", "AWS", "Distributed Systems", "Microservices"],
            "apply_link": "https://www.amazon.jobs/en/search",
            "salary_text": "₹20-35 LPA",
            "source": "amazon",
            "job_type": "full_time",
            "experience_level": "mid"
        },
        {
            "title": "Full Stack Developer",
            "company": "Amazon",
            "location": "Hyderabad, India",
            "description": "Develop end-to-end solutions for Amazon's customer-facing applications. Experience with React and Node.js required.",
            "skills": ["React", "Node.js", "AWS", "JavaScript", "MongoDB"],
            "apply_link": "https://www.amazon.jobs/en/search",
            "salary_text": "₹15-25 LPA",
            "source": "amazon",
            "job_type": "full_time",
            "experience_level": "mid"
        },
        
        # Meta Jobs
        {
            "title": "Software Engineer, Product",
            "company": "Meta",
            "location": "Bangalore, India",
            "description": "Build products used by billions of people. Work on Facebook, Instagram, and WhatsApp platforms.",
            "skills": ["React", "Python", "JavaScript", "GraphQL", "Mobile Development"],
            "apply_link": "https://www.metacareers.com/jobs/",
            "salary_text": "₹30-50 LPA",
            "source": "meta",
            "job_type": "full_time",
            "experience_level": "mid"
        },
        
        # Indian Companies
        {
            "title": "Senior Software Engineer",
            "company": "Flipkart",
            "location": "Bangalore, India",
            "description": "Build scalable e-commerce solutions. Work with microservices, React, and cloud technologies.",
            "skills": ["Java", "React", "Microservices", "Kafka", "Redis"],
            "apply_link": "https://www.flipkartcareers.com/",
            "salary_text": "₹12-20 LPA",
            "source": "flipkart",
            "job_type": "full_time",
            "experience_level": "senior"
        },
        {
            "title": "Full Stack Developer",
            "company": "Zomato",
            "location": "Gurgaon, India",
            "description": "Develop food delivery platform features. Work with React, Node.js, and mobile technologies.",
            "skills": ["React", "Node.js", "MongoDB", "React Native", "AWS"],
            "apply_link": "https://www.zomato.com/careers",
            "salary_text": "₹8-15 LPA",
            "source": "zomato",
            "job_type": "full_time",
            "experience_level": "mid"
        },
        {
            "title": "Backend Developer",
            "company": "Swiggy",
            "location": "Bangalore, India",
            "description": "Build scalable backend systems for food delivery. Experience with microservices and databases required.",
            "skills": ["Python", "Django", "PostgreSQL", "Redis", "Docker"],
            "apply_link": "https://careers.swiggy.com/",
            "salary_text": "₹10-18 LPA",
            "source": "swiggy",
            "job_type": "full_time",
            "experience_level": "mid"
        },
        {
            "title": "Machine Learning Engineer",
            "company": "Paytm",
            "location": "Noida, India",
            "description": "Work on ML models for fraud detection and recommendation systems. Strong Python and ML skills required.",
            "skills": ["Python", "Machine Learning", "TensorFlow", "Spark", "SQL"],
            "apply_link": "https://jobs.paytm.com/",
            "salary_text": "₹12-20 LPA",
            "source": "paytm",
            "job_type": "full_time",
            "experience_level": "mid"
        },
        
        # Internships
        {
            "title": "Software Engineer Intern",
            "company": "Google",
            "location": "Bangalore, India",
            "description": "Summer internship program for computer science students. Work on real Google products with mentorship.",
            "skills": ["Python", "Java", "C++", "Algorithms", "Data Structures"],
            "apply_link": "https://careers.google.com/students/",
            "salary_text": "₹80,000/month",
            "source": "google",
            "job_type": "internship",
            "experience_level": "entry"
        },
        {
            "title": "Software Development Intern",
            "company": "Microsoft",
            "location": "Hyderabad, India",
            "description": "Internship opportunity to work on Microsoft products. Strong programming fundamentals required.",
            "skills": ["C#", "Python", "JavaScript", "Git", "Algorithms"],
            "apply_link": "https://careers.microsoft.com/students/us/en/",
            "salary_text": "₹60,000/month",
            "source": "microsoft",
            "job_type": "internship",
            "experience_level": "entry"
        }
    ]
    
    try:
        conn = sqlite3.connect('jobs.db')
        cursor = conn.cursor()
        
        # Get current job count
        cursor.execute("SELECT COUNT(*) FROM jobs")
        initial_count = cursor.fetchone()[0]
        logger.info(f"Current jobs in database: {initial_count}")
        
        added_count = 0
        for job in quality_jobs:
            try:
                # Create job entry
                job_id = str(uuid.uuid4())
                posted_date = datetime.now() - timedelta(days=random.randint(1, 30))
                scraped_date = datetime.now()
                
                cursor.execute("""
                    INSERT INTO jobs (
                        job_id, title, company, location, description, skills,
                        apply_link, source, posted_date, scraped_at, salary_text,
                        job_type, is_active
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    job_id,
                    job["title"],
                    job["company"],
                    job["location"],
                    job["description"],
                    '["' + '", "'.join(job["skills"]) + '"]',  # Convert to JSON format
                    job["apply_link"],
                    job["source"],
                    posted_date.isoformat(),
                    scraped_date.isoformat(),
                    job["salary_text"],
                    job["job_type"],
                    1  # is_active = True
                ))
                added_count += 1
                
            except Exception as e:
                logger.error(f"Error adding job {job['title']}: {e}")
                continue
        
        conn.commit()
        
        # Get final count
        cursor.execute("SELECT COUNT(*) FROM jobs")
        final_count = cursor.fetchone()[0]
        
        conn.close()
        
        logger.info(f"✅ Successfully added {added_count} quality jobs!")
        logger.info(f"Total jobs in database: {final_count}")
        
    except Exception as e:
        logger.error(f"❌ Error adding quality jobs: {e}")

if __name__ == "__main__":
    add_quality_jobs()
