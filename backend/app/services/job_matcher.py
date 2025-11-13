"""
Intelligent job matching service
"""
import logging
from typing import List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.database.models import Job, Resume, JobMatch

logger = logging.getLogger(__name__)


class JobMatcher:
    """Matches resumes with jobs based on skills and experience"""
    
    def __init__(self):
        pass
    
    def match_resume_with_jobs(
        self,
        resume_data: Dict,
        db: Session,
        limit: int = 50,
        min_match_score: float = 30.0
    ) -> List[Dict]:
        """
        Match a resume with jobs from database
        
        Args:
            resume_data: Parsed resume data
            db: Database session
            limit: Maximum number of matches to return
            min_match_score: Minimum match score (0-100)
            
        Returns:
            List of matched jobs with scores
        """
        try:
            resume_skills = [s.lower() for s in resume_data.get('skills', [])]
            resume_experience = resume_data.get('experience_years', 0) or 0
            
            logger.info(f"Matching resume with {len(resume_skills)} skills and {resume_experience} years experience")
            
            # Get all active jobs
            jobs = db.query(Job).filter(Job.is_active == True).all()
            
            logger.info(f"Found {len(jobs)} active jobs in database")
            
            # Calculate match scores for each job
            job_matches = []
            
            for job in jobs:
                match_result = self._calculate_match_score(
                    resume_skills=resume_skills,
                    resume_experience=resume_experience,
                    job=job
                )
                
                if match_result['match_score'] >= min_match_score:
                    job_matches.append({
                        'job': job.to_dict(),
                        'match_score': match_result['match_score'],
                        'skill_match_score': match_result['skill_match_score'],
                        'experience_match_score': match_result['experience_match_score'],
                        'matching_skills': match_result['matching_skills'],
                        'missing_skills': match_result['missing_skills'],
                    })
            
            # Sort by match score (descending)
            job_matches.sort(key=lambda x: x['match_score'], reverse=True)
            
            # Limit results
            job_matches = job_matches[:limit]
            
            logger.info(f"✅ Found {len(job_matches)} matching jobs")
            
            return job_matches
            
        except Exception as e:
            logger.error(f"Error matching jobs: {str(e)}")
            return []
    
    def _calculate_match_score(
        self,
        resume_skills: List[str],
        resume_experience: float,
        job: Job
    ) -> Dict:
        """
        Calculate match score between resume and job
        
        Returns:
            Dictionary with match scores and details
        """
        # Get job skills
        job_skills = [s.lower() for s in (job.skills or [])]
        
        # Calculate skill match
        if not job_skills:
            skill_match_score = 50.0  # Neutral score if no skills specified
            matching_skills = []
            missing_skills = []
        else:
            matching_skills = [s for s in resume_skills if s in job_skills]
            missing_skills = [s for s in job_skills if s not in resume_skills]
            
            skill_match_score = (len(matching_skills) / len(job_skills)) * 100 if job_skills else 0
        
        # Calculate experience match
        job_exp_min = job.experience_min or 0
        job_exp_max = job.experience_max or 100
        
        if job_exp_min == 0 and job_exp_max == 100:
            # No experience requirement
            experience_match_score = 100.0
        elif resume_experience >= job_exp_min and resume_experience <= job_exp_max:
            # Perfect match
            experience_match_score = 100.0
        elif resume_experience < job_exp_min:
            # Under-qualified
            diff = job_exp_min - resume_experience
            experience_match_score = max(0, 100 - (diff * 20))  # Penalize 20% per year
        else:
            # Over-qualified
            diff = resume_experience - job_exp_max
            experience_match_score = max(70, 100 - (diff * 5))  # Smaller penalty for over-qualification
        
        # Calculate overall match score (weighted average)
        # Skills: 70%, Experience: 30%
        overall_match_score = (skill_match_score * 0.7) + (experience_match_score * 0.3)
        
        return {
            'match_score': round(overall_match_score, 2),
            'skill_match_score': round(skill_match_score, 2),
            'experience_match_score': round(experience_match_score, 2),
            'matching_skills': [s.title() for s in matching_skills],
            'missing_skills': [s.title() for s in missing_skills],
        }
    
    def save_matches_to_db(
        self,
        resume_id: int,
        job_matches: List[Dict],
        db: Session
    ) -> int:
        """
        Save job matches to database
        
        Args:
            resume_id: Resume database ID
            job_matches: List of job match dictionaries
            db: Database session
            
        Returns:
            Number of matches saved
        """
        saved_count = 0
        
        try:
            for match in job_matches:
                job_id = match['job']['id']
                
                # Check if match already exists
                existing_match = db.query(JobMatch).filter(
                    and_(
                        JobMatch.resume_id == resume_id,
                        JobMatch.job_id == job_id
                    )
                ).first()
                
                if existing_match:
                    # Update existing match
                    existing_match.match_score = match['match_score']
                    existing_match.skill_match_score = match['skill_match_score']
                    existing_match.experience_match_score = match['experience_match_score']
                    existing_match.matching_skills = match['matching_skills']
                    existing_match.missing_skills = match['missing_skills']
                else:
                    # Create new match
                    new_match = JobMatch(
                        resume_id=resume_id,
                        job_id=job_id,
                        match_score=match['match_score'],
                        skill_match_score=match['skill_match_score'],
                        experience_match_score=match['experience_match_score'],
                        matching_skills=match['matching_skills'],
                        missing_skills=match['missing_skills']
                    )
                    db.add(new_match)
                    saved_count += 1
                
                db.commit()
            
            logger.info(f"💾 Saved {saved_count} job matches to database")
            return saved_count
            
        except Exception as e:
            logger.error(f"Error saving matches: {str(e)}")
            db.rollback()
            return 0


# Global matcher instance
job_matcher = JobMatcher()
