"""
Simple job matcher using basic keyword matching
"""

import logging
from typing import List, Dict, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from app.models.job import Job, JobMatch
from app.models.resume import ResumeData

logger = logging.getLogger(__name__)

class SimpleJobMatcher:
    """Simple job matcher using TF-IDF and cosine similarity"""
    
    def __init__(self):
        self.logger = logging.getLogger("app.services.simple_job_matcher")
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        self.job_descriptions: List[str] = []
        self.job_ids: List[str] = []
        self.tfidf_matrix = None
    
    def update_job_corpus(self, jobs: List[Job]):
        """Update the TF-IDF corpus with current jobs"""
        self.job_descriptions = []
        self.job_ids = []
        
        for job in jobs:
            # Create job text for matching
            job_text = f"{job.title} {job.description} {' '.join(job.skills)}"
            self.job_descriptions.append(job_text)
            self.job_ids.append(job.id)
        
        if self.job_descriptions:
            try:
                self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.job_descriptions)
                self.logger.info(f"Updated TF-IDF corpus with {len(self.job_descriptions)} jobs")
            except Exception as e:
                self.logger.error(f"Error creating TF-IDF matrix: {e}")
                self.tfidf_matrix = None
        else:
            self.tfidf_matrix = None
            self.logger.warning("No job descriptions available")
    
    def match_jobs_with_resume(self, resume_data: ResumeData, jobs: List[Job], 
                              limit: int = 20, country: Optional[str] = None) -> List[JobMatch]:
        """Match jobs with resume data"""
        self.logger.info(f"Matching jobs for resume: {resume_data.name}")
        
        if not jobs:
            self.logger.warning("No jobs available for matching")
            return []
        
        # Update job corpus
        self.update_job_corpus(jobs)
        
        if self.tfidf_matrix is None:
            self.logger.warning("No jobs available to perform matching")
            return []
        
        # Create resume text for matching
        resume_text = " ".join(resume_data.skills + resume_data.keywords)
        
        if not resume_text.strip():
            self.logger.warning("Resume has no skills or keywords for matching")
            return []
        
        try:
            # Vectorize resume text
            resume_vector = self.tfidf_vectorizer.transform([resume_text])
            
            # Calculate cosine similarity
            similarity_scores = cosine_similarity(resume_vector, self.tfidf_matrix).flatten()
            
            # Create mapping from job_id to Job object
            jobs_map = {job.id: job for job in jobs}
            
            # Combine scores with jobs and filter
            matched_jobs_with_scores = []
            for i, score in enumerate(similarity_scores):
                job_id = self.job_ids[i]
                job = jobs_map.get(job_id)
                
                if job:
                    # Apply country filter if specified
                    if country and job.country and job.country.lower() != country.lower():
                        continue
                    
                    # Calculate skill match percentage
                    resume_skills_set = set(s.lower() for s in resume_data.skills)
                    job_skills_set = set(s.lower() for s in job.skills)
                    
                    matching_skills = list(resume_skills_set.intersection(job_skills_set))
                    missing_skills = list(job_skills_set.difference(resume_skills_set))
                    
                    skill_match_percentage = 0.0
                    if len(resume_skills_set) > 0:
                        skill_match_percentage = (len(matching_skills) / len(resume_skills_set)) * 100
                    
                    # Create job match
                    job_match = JobMatch(
                        job=job,
                        match_score=round(score * 100, 2),  # Convert to 0-100 scale
                        matching_skills=matching_skills,
                        missing_skills=missing_skills,
                        skill_match_percentage=round(skill_match_percentage, 2),
                        experience_match=True,  # Simplified for now
                        location_match=not country or job.country.lower() == country.lower(),
                        salary_match=True  # Simplified for now
                    )
                    
                    matched_jobs_with_scores.append(job_match)
            
            # Sort by match score
            matched_jobs_with_scores.sort(key=lambda x: x.match_score, reverse=True)
            
            # Return top matches
            result = matched_jobs_with_scores[:limit]
            self.logger.info(f"Found {len(result)} matched jobs")
            return result
            
        except Exception as e:
            self.logger.error(f"Error in job matching: {e}")
            return []
    
    def get_matching_skills(self, resume_skills: List[str], job_skills: List[str]) -> List[str]:
        """Get matching skills between resume and job"""
        resume_skills_set = set(s.lower() for s in resume_skills)
        job_skills_set = set(s.lower() for s in job_skills)
        return list(resume_skills_set.intersection(job_skills_set))
    
    def get_missing_skills(self, resume_skills: List[str], job_skills: List[str]) -> List[str]:
        """Get skills required by job but missing from resume"""
        resume_skills_set = set(s.lower() for s in resume_skills)
        job_skills_set = set(s.lower() for s in job_skills)
        return list(job_skills_set.difference(resume_skills_set))
    
    def calculate_skill_match_percentage(self, resume_skills: List[str], job_skills: List[str]) -> float:
        """Calculate skill match percentage"""
        resume_skills_set = set(s.lower() for s in resume_skills)
        job_skills_set = set(s.lower() for s in job_skills)
        
        if len(resume_skills_set) == 0:
            return 0.0
        
        matching_skills = resume_skills_set.intersection(job_skills_set)
        return (len(matching_skills) / len(resume_skills_set)) * 100

# Create global instance
simple_job_matcher = SimpleJobMatcher()
