"""
Mock job service to provide sample jobs for testing
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
import uuid
from app.models.job import Job, JobType, ExperienceLevel

logger = logging.getLogger(__name__)

class MockJobService:
    """Mock job service that provides sample jobs for testing"""
    
    def __init__(self):
        self.jobs = self._create_mock_jobs()
    
    def _create_mock_jobs(self) -> List[Job]:
        """Create mock jobs for testing"""
        jobs = [
            Job(
                id=str(uuid.uuid4()),
                title="Senior Python Developer",
                company="TechCorp Solutions",
                location="Bangalore, India",
                description="We are looking for a Senior Python Developer with 5+ years of experience. You will work on our cloud-based platform using Django, Flask, and modern Python frameworks.",
                skills=["python", "django", "flask", "postgresql", "aws", "docker", "kubernetes"],
                skills_required=["python", "django", "flask", "postgresql", "aws", "docker"],
                apply_link="https://techcorp.com/careers/python-developer",
                source="LinkedIn",
                posted_date=datetime.now() - timedelta(days=1),
                scraped_date=datetime.now(),
                job_type=JobType.FULL_TIME,
                experience_level=ExperienceLevel.SENIOR,
                salary_min=1200000,
                salary_max=1800000,
                salary_currency="INR",
                salary_text="₹12-18 LPA"
            ),
            Job(
                id=str(uuid.uuid4()),
                title="Full Stack Developer",
                company="StartupXYZ",
                location="Mumbai, India",
                description="Join our fast-growing startup as a Full Stack Developer. Work with React, Node.js, MongoDB, and modern web technologies.",
                skills=["javascript", "react", "node.js", "mongodb", "express", "html", "css"],
                skills_required=["javascript", "react", "node.js", "mongodb", "express"],
                apply_link="https://startupxyz.com/jobs/fullstack",
                source="Google Careers",
                posted_date=datetime.now() - timedelta(days=2),
                scraped_date=datetime.now(),
                job_type=JobType.FULL_TIME,
                experience_level=ExperienceLevel.MID,
                salary_min=800000,
                salary_max=1200000,
                salary_currency="INR",
                salary_text="₹8-12 LPA"
            ),
            Job(
                id=str(uuid.uuid4()),
                title="Software Engineer",
                company="Microsoft",
                location="Hyderabad, India",
                description="Work on cutting-edge technology at Microsoft. Experience with C#, .NET, Azure, and cloud development preferred.",
                skills=["c#", "dotnet", "azure", "sql", "cloud", "microservices"],
                skills_required=["c#", "dotnet", "azure", "sql", "cloud"],
                apply_link="https://careers.microsoft.com/software-engineer",
                source="Microsoft Careers",
                posted_date=datetime.now() - timedelta(days=3),
                scraped_date=datetime.now(),
                job_type=JobType.FULL_TIME,
                experience_level=ExperienceLevel.MID,
                salary_min=1000000,
                salary_max=1500000,
                salary_currency="INR",
                salary_text="₹10-15 LPA"
            ),
            Job(
                id=str(uuid.uuid4()),
                title="Python Intern",
                company="DataTech Solutions",
                location="Delhi, India",
                description="Internship opportunity for Python developers. Work on data analysis and machine learning projects using pandas, numpy, and scikit-learn.",
                skills=["python", "pandas", "numpy", "machine learning", "data analysis"],
                skills_required=["python", "pandas", "numpy", "machine learning"],
                apply_link="https://datatech.com/internships/python",
                source="Internshala",
                posted_date=datetime.now() - timedelta(days=4),
                scraped_date=datetime.now(),
                job_type=JobType.INTERNSHIP,
                experience_level=ExperienceLevel.ENTRY,
                salary_min=10000,
                salary_max=25000,
                salary_currency="INR",
                salary_text="₹10-25k/month"
            ),
            Job(
                id=str(uuid.uuid4()),
                title="React Developer",
                company="WebStudio",
                location="Chennai, India",
                description="We need a skilled React developer to join our team. Experience with Redux, TypeScript, and modern React patterns required.",
                skills=["react", "redux", "typescript", "javascript", "html", "css"],
                skills_required=["react", "redux", "typescript", "javascript"],
                apply_link="https://webstudio.com/jobs/react-developer",
                source="LinkedIn",
                posted_date=datetime.now() - timedelta(days=5),
                scraped_date=datetime.now(),
                job_type=JobType.FULL_TIME,
                experience_level=ExperienceLevel.MID,
                salary_min=600000,
                salary_max=1000000,
                salary_currency="INR",
                salary_text="₹6-10 LPA"
            ),
            Job(
                id=str(uuid.uuid4()),
                title="DevOps Engineer",
                company="CloudTech",
                location="Pune, India",
                description="Looking for a DevOps engineer with experience in AWS, Docker, Kubernetes, and CI/CD pipelines.",
                skills=["aws", "docker", "kubernetes", "jenkins", "terraform", "python"],
                skills_required=["aws", "docker", "kubernetes", "jenkins", "terraform"],
                apply_link="https://cloudtech.com/careers/devops",
                source="Google Careers",
                posted_date=datetime.now() - timedelta(days=6),
                scraped_date=datetime.now(),
                job_type=JobType.FULL_TIME,
                experience_level=ExperienceLevel.SENIOR,
                salary_min=1400000,
                salary_max=2000000,
                salary_currency="INR",
                salary_text="₹14-20 LPA"
            )
        ]
        return jobs
    
    def get_jobs(self, search_params: Dict[str, Any] = None) -> List[Job]:
        """Get mock jobs with optional filtering"""
        jobs = self.jobs.copy()
        
        if search_params:
            keywords = search_params.get('keywords', '').lower()
            if keywords:
                filtered_jobs = []
                for job in jobs:
                    job_text = f"{job.title} {job.description} {' '.join(job.skills)}".lower()
                    if any(keyword in job_text for keyword in keywords.split()):
                        filtered_jobs.append(job)
                jobs = filtered_jobs
        
        return jobs

# Global mock job service instance
mock_job_service = MockJobService()
