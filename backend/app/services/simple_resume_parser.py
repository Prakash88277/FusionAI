"""
Simple resume parser for testing purposes
"""

import io
import re
import logging
import uuid
from datetime import datetime
from typing import List, Dict, Optional
from fastapi import UploadFile
from app.models.resume import ResumeData, Education, Experience, Project

logger = logging.getLogger(__name__)

class SimpleResumeParser:
    """Simple resume parser for testing"""
    
    def __init__(self):
        self.logger = logging.getLogger("app.services.simple_resume_parser")
    
    async def parse_resume(self, file: UploadFile) -> ResumeData:
        """Parse resume file and extract basic information"""
        try:
            self.logger.info(f"Starting to parse resume: {file.filename}")
            
            # Read file content
            content = await file.read()
            
            # For testing, create a simple text representation
            text = content.decode('utf-8', errors='ignore') if isinstance(content, bytes) else str(content)
            
            # Extract basic information using simple patterns
            email = self.extract_email(text)
            skills = self.extract_skills(text)
            
            # Create resume data
            resume_data = ResumeData(
                id=str(uuid.uuid4()),
                name="Candidate",  # Simplified name extraction
                email=email,
                skills=skills,
                education=[Education(degree="Bachelor's Degree", university="University", year="2023")],
                experience=[Experience(company="Company", role="Position", duration="2 years")],
                keywords=skills + ["software engineer", "developer"],
                country="India"
            )
            
            self.logger.info(f"Successfully parsed resume for: {resume_data.name}")
            return resume_data

        except Exception as e:
            self.logger.error(f"Error parsing resume: {str(e)}")
            raise ValueError(f"Failed to parse resume: {str(e)}")
    
    def extract_email(self, text: str) -> str:
        """Extract email from text"""
        try:
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            matches = re.findall(email_pattern, text)
            if matches:
                return matches[0]
            return "candidate@example.com"
        except:
            return "candidate@example.com"
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from text"""
        try:
            # Common technical skills
            common_skills = [
                "python", "javascript", "java", "c++", "react", "node.js", "django", "flask",
                "mongodb", "mysql", "postgresql", "aws", "docker", "kubernetes", "git",
                "html", "css", "sql", "machine learning", "data science", "pandas", "numpy"
            ]
            
            text_lower = text.lower()
            found_skills = []
            
            for skill in common_skills:
                if skill in text_lower:
                    found_skills.append(skill)
            
            # Return at least some default skills if none found
            if not found_skills:
                found_skills = ["python", "javascript", "web development"]
            
            return found_skills
            
        except:
            return ["python", "javascript", "web development"]

# Create global parser instance
simple_resume_parser = SimpleResumeParser()

# Backward compatibility function
async def parse_resume(file: UploadFile) -> ResumeData:
    """Backward compatibility function"""
    return await simple_resume_parser.parse_resume(file)
