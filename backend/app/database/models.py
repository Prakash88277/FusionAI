"""
Database models for jobs, resumes, and matches
"""
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.database import Base

class Job(Base):
    """Job postings scraped from various sources"""
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True)  # Unique identifier from source
    title = Column(String, index=True)
    company = Column(String, index=True)
    location = Column(String)
    description = Column(Text)
    requirements = Column(Text)
    
    # Skills and experience
    skills = Column(JSON)  # List of skills
    experience_min = Column(Integer, nullable=True)  # Minimum years
    experience_max = Column(Integer, nullable=True)  # Maximum years
    
    # Job details
    job_type = Column(String)  # full_time, part_time, contract, internship
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    salary_text = Column(String, nullable=True)
    
    # Source information
    source = Column(String, index=True)  # google, meta, internshala, naukri, etc.
    apply_link = Column(String)
    posted_date = Column(DateTime, nullable=True)
    
    # Metadata
    scraped_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    matches = relationship("JobMatch", back_populates="job")
    
    def to_dict(self):
        return {
            "id": self.id,
            "job_id": self.job_id,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "description": self.description,
            "requirements": self.requirements,
            "skills": self.skills or [],
            "experience_min": self.experience_min,
            "experience_max": self.experience_max,
            "job_type": self.job_type,
            "salary_text": self.salary_text,
            "source": self.source,
            "apply_link": self.apply_link,
            "posted_date": self.posted_date.isoformat() if self.posted_date else None,
            "scraped_at": self.scraped_at.isoformat() if self.scraped_at else None,
        }


class Resume(Base):
    """Parsed resume data"""
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(String, unique=True, index=True)
    filename = Column(String)
    
    # Extracted information
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    
    # Skills and experience
    skills = Column(JSON)  # List of extracted skills
    experience_years = Column(Float, nullable=True)
    
    # Education and other details
    education = Column(JSON, nullable=True)
    certifications = Column(JSON, nullable=True)
    raw_text = Column(Text, nullable=True)
    
    # Metadata
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    matches = relationship("JobMatch", back_populates="resume")
    
    def to_dict(self):
        return {
            "id": self.id,
            "resume_id": self.resume_id,
            "filename": self.filename,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "skills": self.skills or [],
            "experience_years": self.experience_years,
            "education": self.education,
            "uploaded_at": self.uploaded_at.isoformat() if self.uploaded_at else None,
        }


class JobMatch(Base):
    """Matching results between resumes and jobs"""
    __tablename__ = "job_matches"
    
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), index=True)
    
    # Match scores
    match_score = Column(Float)  # Overall match percentage (0-100)
    skill_match_score = Column(Float)  # Skills match percentage
    experience_match_score = Column(Float)  # Experience match percentage
    
    # Detailed matching
    matching_skills = Column(JSON)  # Skills that match
    missing_skills = Column(JSON)  # Skills required but not in resume
    
    # Metadata
    matched_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    resume = relationship("Resume", back_populates="matches")
    job = relationship("Job", back_populates="matches")
    
    def to_dict(self):
        return {
            "id": self.id,
            "match_score": self.match_score,
            "skill_match_score": self.skill_match_score,
            "experience_match_score": self.experience_match_score,
            "matching_skills": self.matching_skills or [],
            "missing_skills": self.missing_skills or [],
            "job": self.job.to_dict() if self.job else None,
        }
