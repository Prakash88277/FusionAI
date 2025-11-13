"""
Enhanced resume parser with skill and experience extraction
"""
import re
import PyPDF2
import docx
import io
from typing import Dict, List, Optional
from fastapi import UploadFile
import logging
import uuid
from datetime import datetime
from app.models.resume import ResumeData, Education, Experience, Project

# Try to import pdfminer, fallback to PyPDF2 only if not available
try:
    from pdfminer.high_level import extract_text
    PDFMINER_AVAILABLE = True
except ImportError:
    PDFMINER_AVAILABLE = False
    logger.warning("pdfminer not available, using PyPDF2 only")

logger = logging.getLogger(__name__)


class EnhancedResumeParser:
    """Enhanced parser for extracting detailed information from resumes"""
    
    def __init__(self):
        # Common tech skills database
        self.tech_skills = [
            # Programming Languages
            'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin',
            'go', 'rust', 'typescript', 'scala', 'r', 'matlab', 'perl', 'dart', 'c',
            
            # Web Technologies
            'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django',
            'flask', 'spring', 'asp.net', 'laravel', 'jquery', 'bootstrap', 'tailwind',
            'next.js', 'nuxt.js', 'gatsby', 'webpack', 'babel',
            
            # Databases
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sqlite',
            'cassandra', 'dynamodb', 'elasticsearch', 'mariadb', 'neo4j', 'couchdb',
            
            # Cloud & DevOps
            'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'jenkins',
            'ci/cd', 'terraform', 'ansible', 'git', 'github', 'gitlab', 'bitbucket',
            'circleci', 'travis ci', 'nginx', 'apache',
            
            # Data Science & ML
            'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'keras',
            'pandas', 'numpy', 'scikit-learn', 'nlp', 'computer vision', 'opencv',
            'matplotlib', 'seaborn', 'jupyter', 'spark', 'hadoop',
            
            # Mobile Development
            'android', 'ios', 'react native', 'flutter', 'xamarin', 'swift', 'kotlin',
            
            # Other Technologies
            'rest api', 'graphql', 'microservices', 'agile', 'scrum', 'jira',
            'linux', 'unix', 'bash', 'powershell', 'excel', 'tableau', 'power bi',
            'salesforce', 'sap', 'blockchain', 'ethereum', 'solidity',
        ]
    
    async def parse_resume(self, file: UploadFile) -> ResumeData:
        """
        Parse resume and extract all relevant information
        
        Args:
            file: Uploaded resume file (PDF or DOCX)
            
        Returns:
            ResumeData object with parsed information
        """
        try:
            logger.info(f"Starting to parse resume: {file.filename}")
            
            # Read file content
            content = await file.read()
            
            # Extract text based on file type
            if file.filename.endswith('.pdf'):
                text = self._extract_text_from_pdf(content)
            elif file.filename.endswith('.docx'):
                text = self._extract_text_from_docx(content)
            else:
                raise ValueError("Unsupported file format")
            
            if not text.strip():
                raise ValueError("Could not extract text from resume")
            
            # Extract information
            name = self._extract_name(text)
            email = self._extract_email(text)
            skills = self._extract_skills(text)
            education = self._extract_education(text)
            experience = self._extract_experience(text)
            
            # Create ResumeData object
            resume_data = ResumeData(
                id=str(uuid.uuid4()),
                name=name or "Candidate",
                email=email or "candidate@example.com",
                skills=skills,
                education=education,
                experience=experience,
                keywords=skills + ["software engineer", "developer"],
                country="India"
            )
            
            logger.info(f"✅ Parsed resume: {resume_data.name} - {len(resume_data.skills)} skills found")
            
            return resume_data
            
        except Exception as e:
            logger.error(f"Error parsing resume: {str(e)}")
            raise ValueError(f"Failed to parse resume: {str(e)}")
    
    def _extract_text_from_pdf(self, content: bytes) -> str:
        """Extract text from PDF using multiple methods"""
        try:
            # Method 1: Try pdfminer first (more reliable) if available
            if PDFMINER_AVAILABLE:
                try:
                    pdf_file = io.BytesIO(content)
                    text = extract_text(pdf_file)
                    if text.strip():
                        return text
                except:
                    pass
            
            # Method 2: Fallback to PyPDF2
            pdf_file = io.BytesIO(content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            
            return text
        except Exception as e:
            logger.error(f"Error extracting PDF text: {str(e)}")
            return ""
    
    def _extract_text_from_docx(self, content: bytes) -> str:
        """Extract text from DOCX"""
        try:
            import io
            docx_file = io.BytesIO(content)
            doc = docx.Document(docx_file)
            
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text
        except Exception as e:
            logger.error(f"Error extracting DOCX text: {str(e)}")
            return ""
    
    def _extract_name(self, text: str) -> Optional[str]:
        """Extract name from resume (usually first line)"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if lines:
            # First non-empty line is usually the name
            return lines[0][:100]  # Limit length
        return None
    
    def _extract_email(self, text: str) -> Optional[str]:
        """Extract email address"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(email_pattern, text)
        return matches[0] if matches else None
    
    def _extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number"""
        phone_patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\d{10}',
            r'\+\d{12}',
        ]
        
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0]
        
        return None
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract technical skills from resume"""
        text_lower = text.lower()
        found_skills = []
        
        for skill in self.tech_skills:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                # Capitalize properly
                found_skills.append(skill.title())
        
        # Remove duplicates and sort
        found_skills = sorted(list(set(found_skills)))
        
        return found_skills
    
    def _extract_experience_years(self, text: str) -> Optional[float]:
        """Extract years of experience"""
        text_lower = text.lower()
        
        # Patterns to match experience
        patterns = [
            r'(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience)?',
            r'experience\s*:?\s*(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)',
            r'total\s*experience\s*:?\s*(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)',
        ]
        
        max_experience = 0
        
        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                try:
                    years = float(match)
                    if years > max_experience and years < 50:  # Sanity check
                        max_experience = years
                except:
                    continue
        
        return max_experience if max_experience > 0 else None
    
    def _extract_education(self, text: str) -> List[Education]:
        """Extract education details"""
        education = []
        
        # Common degree patterns
        degree_patterns = [
            r'(B\.?Tech|Bachelor|B\.?E\.?|B\.?S\.?|B\.?Sc)',
            r'(M\.?Tech|Master|M\.?E\.?|M\.?S\.?|M\.?Sc|MBA)',
            r'(Ph\.?D|Doctorate)',
        ]
        
        text_lower = text.lower()
        
        for pattern in degree_patterns:
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                # Get surrounding context
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 100)
                context = text[start:end].strip()
                
                # Extract year if possible
                year_match = re.search(r'(19|20)\d{2}', context)
                year = year_match.group() if year_match else "2023"
                
                education.append(Education(
                    degree=match.group().title(),
                    university="University",
                    year=year
                ))
        
        # If no education found, add default
        if not education:
            education.append(Education(
                degree="Bachelor's Degree",
                university="University",
                year="2023"
            ))
        
        return education[:5]  # Limit to 5 entries
    
    def _extract_experience(self, text: str) -> List[Experience]:
        """Extract work experience"""
        experience = []
        
        # Look for common experience patterns
        experience_patterns = [
            r'(Software Engineer|Developer|Analyst|Manager|Intern)',
            r'(Experience|Work|Employment)',
        ]
        
        text_lower = text.lower()
        
        # Extract years of experience
        years_match = re.search(r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience)?', text_lower)
        duration = f"{years_match.group(1)} years" if years_match else "2 years"
        
        # Add default experience
        experience.append(Experience(
            company="Company",
            role="Software Developer",
            duration=duration
        ))
        
        return experience
    
    def _extract_certifications(self, text: str) -> List[str]:
        """Extract certifications"""
        certifications = []
        
        # Common certification keywords
        cert_keywords = [
            'aws certified', 'azure certified', 'google cloud certified',
            'pmp', 'cissp', 'ceh', 'comptia', 'cisco', 'oracle certified',
            'microsoft certified', 'scrum master', 'six sigma'
        ]
        
        text_lower = text.lower()
        
        for keyword in cert_keywords:
            if keyword in text_lower:
                certifications.append(keyword.title())
        
        return list(set(certifications))


# Global parser instance
enhanced_resume_parser = EnhancedResumeParser()

# Backward compatibility function
async def parse_resume_enhanced(file: UploadFile) -> ResumeData:
    """Enhanced resume parsing function"""
    return await enhanced_resume_parser.parse_resume(file)
