"""
NEW RESUME PARSER - Hybrid approach with improved accuracy
"""
import json
import re
import io
import os
from typing import Dict, List, Any
from sklearn.feature_extraction.text import TfidfVectorizer
import logging

# Try to import pdfminer, fallback to PyPDF2 if not available
try:
    from pdfminer.high_level import extract_text as pdf_extract
    PDFMINER_AVAILABLE = True
except ImportError:
    import PyPDF2
    PDFMINER_AVAILABLE = False

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

logger = logging.getLogger(__name__)

class ResumeParser:
    def __init__(self):
        # Load skills from JSON file
        skills_path = os.path.join(os.path.dirname(__file__), "..", "..", "skills.json")
        try:
            with open(skills_path, "r", encoding="utf-8") as f:
                self.skill_data = json.load(f)
            self.flat_skill_list = [s.lower() for group in self.skill_data.values() for s in group]
            logger.info(f"Loaded {len(self.flat_skill_list)} skills from skills.json")
        except FileNotFoundError:
            logger.warning("skills.json not found, using default skills")
            self.skill_data = {
                "programming": ["python", "javascript", "java", "react", "node.js", "sql"],
                "tools": ["git", "docker", "aws", "linux"]
            }
            self.flat_skill_list = [s.lower() for group in self.skill_data.values() for s in group]

    def extract_text(self, file_bytes, filename):
        """Extract text from PDF or DOCX files"""
        try:
            if filename.lower().endswith(".pdf"):
                return self._extract_pdf_text(file_bytes)
            elif filename.lower().endswith(".docx"):
                return self._extract_docx_text(file_bytes)
            else:
                raise ValueError(f"Unsupported file format: {filename}")
        except Exception as e:
            logger.error(f"Error extracting text from {filename}: {str(e)}")
            raise ValueError(f"Failed to extract text from {filename}: {str(e)}")

    def _extract_pdf_text(self, file_bytes):
        """Extract text from PDF using available libraries"""
        if PDFMINER_AVAILABLE:
            try:
                # Use pdfminer if available
                if isinstance(file_bytes, bytes):
                    file_obj = io.BytesIO(file_bytes)
                else:
                    file_obj = file_bytes
                return pdf_extract(file_obj)
            except Exception as e:
                logger.warning(f"pdfminer failed: {e}, falling back to PyPDF2")
        
        # Fallback to PyPDF2
        try:
            if isinstance(file_bytes, bytes):
                file_obj = io.BytesIO(file_bytes)
            else:
                file_obj = file_bytes
            
            pdf_reader = PyPDF2.PdfReader(file_obj)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text
        except Exception as e:
            logger.error(f"PyPDF2 failed: {e}")
            raise ValueError("Failed to extract text from PDF")

    def _extract_docx_text(self, file_bytes):
        """Extract text from DOCX files"""
        if not DOCX_AVAILABLE:
            raise ValueError("python-docx not available for DOCX processing")
        
        try:
            if isinstance(file_bytes, bytes):
                file_obj = io.BytesIO(file_bytes)
            else:
                file_obj = file_bytes
            
            doc = Document(file_obj)
            return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        except Exception as e:
            logger.error(f"DOCX extraction failed: {e}")
            raise ValueError("Failed to extract text from DOCX")

    def extract_skills(self, text):
        """Extract skills from text using the skills database"""
        text_lower = text.lower()
        found_skills = []
        
        # Look for exact skill matches
        for skill in self.flat_skill_list:
            if skill in text_lower:
                # Avoid partial matches by checking word boundaries for multi-word skills
                if len(skill.split()) > 1:
                    # Multi-word skill - check for exact phrase
                    if skill in text_lower:
                        found_skills.append(skill)
                else:
                    # Single word - check word boundaries
                    pattern = r'\b' + re.escape(skill) + r'\b'
                    if re.search(pattern, text_lower):
                        found_skills.append(skill)
        
        # Remove duplicates and return
        return list(set(found_skills))

    def extract_roles(self, text):
        """Extract job roles/titles from text"""
        roles = [
            "software engineer", "data analyst", "machine learning engineer",
            "frontend developer", "backend developer", "full stack developer",
            "devops engineer", "data scientist", "android developer", "ios developer",
            "web developer", "mobile developer", "qa engineer", "test engineer",
            "product manager", "project manager", "business analyst", "system administrator",
            "network engineer", "security engineer", "cloud engineer", "ai engineer"
        ]
        
        text_lower = text.lower()
        found_roles = []
        
        for role in roles:
            if role in text_lower:
                found_roles.append(role)
        
        return list(set(found_roles))

    def extract_experience(self, text):
        """Extract years of experience from text"""
        text_lower = text.lower()
        
        # Pattern for "X years" or "X+ years"
        patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'(?:experience|exp).*?(\d+)\+?\s*(?:years?|yrs?)',
            r'(\d+)\+?\s*(?:years?|yrs?)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                try:
                    return max([int(match) for match in matches])
                except ValueError:
                    continue
        
        return 0

    def detect_domain(self, skills):
        """Detect the primary domain based on skills"""
        domain_map = {
            "data_science": ["machine learning", "deep learning", "pandas", "tensorflow", "pytorch", "data analysis", "statistics", "python", "r", "jupyter"],
            "web_development": ["react", "angular", "vue", "node.js", "html", "css", "javascript", "typescript", "express", "django", "flask"],
            "cloud_devops": ["docker", "kubernetes", "aws", "azure", "gcp", "jenkins", "ci/cd", "terraform", "ansible"],
            "mobile_development": ["flutter", "react native", "android", "ios", "swift", "kotlin", "xamarin"],
            "backend_development": ["java", "python", "c#", "spring", "asp.net", "sql", "postgresql", "mongodb"],
            "frontend_development": ["react", "angular", "vue", "javascript", "typescript", "css", "html", "sass"],
            "qa_testing": ["selenium", "cypress", "jest", "pytest", "automation testing", "unit testing"]
        }

        domain_scores = {}
        skills_lower = [skill.lower() for skill in skills]
        
        for domain, domain_skills in domain_map.items():
            score = len([s for s in skills_lower if s in [ds.lower() for ds in domain_skills]])
            if score > 0:
                domain_scores[domain] = score

        if not domain_scores:
            return "general"

        # Return domain with highest score
        return max(domain_scores.items(), key=lambda x: x[1])[0]

    def extract_keywords(self, text):
        """Extract important keywords using TF-IDF"""
        try:
            # Clean text
            text = re.sub(r'[^\w\s]', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()
            
            if len(text) < 50:  # Too short for meaningful TF-IDF
                return []
            
            vectorizer = TfidfVectorizer(
                max_features=20, 
                stop_words="english",
                ngram_range=(1, 2),  # Include bigrams
                min_df=1,
                max_df=0.8
            )
            
            try:
                vectorizer.fit_transform([text])
                return list(vectorizer.get_feature_names_out())
            except ValueError:
                # Fallback to simple word extraction
                words = text.lower().split()
                # Filter out common words and return most frequent
                common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an'}
                filtered_words = [w for w in words if w not in common_words and len(w) > 2]
                return list(set(filtered_words))[:20]
                
        except Exception as e:
            logger.warning(f"TF-IDF extraction failed: {e}")
            return []

    def parse(self, file_bytes, filename):
        """Main parsing function - returns structured resume data"""
        try:
            # Extract text
            text = self.extract_text(file_bytes, filename)
            
            if not text or len(text.strip()) < 10:
                raise ValueError("No meaningful text extracted from file")
            
            # Extract all components
            skills = self.extract_skills(text)
            roles = self.extract_roles(text)
            experience = self.extract_experience(text)
            domain = self.detect_domain(skills)
            keywords = self.extract_keywords(text)
            
            # Extract basic info
            name = self._extract_name(text)
            email = self._extract_email(text)
            phone = self._extract_phone(text)
            
            result = {
                "name": name,
                "email": email,
                "phone": phone,
                "skills": skills,
                "roles": roles,
                "experience": experience,
                "domain": domain,
                "keywords": keywords,
                "text_length": len(text),
                "skills_count": len(skills)
            }
            
            logger.info(f"Successfully parsed resume: {len(skills)} skills, {experience} years exp, domain: {domain}")
            return result
            
        except Exception as e:
            logger.error(f"Resume parsing failed: {str(e)}")
            raise ValueError(f"Resume parsing failed: {str(e)}")

    def _extract_name(self, text):
        """Extract name from resume text"""
        lines = text.split('\n')
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if line and len(line.split()) <= 4 and len(line) > 3:
                # Simple heuristic: if it's a short line with 1-4 words, likely a name
                if not re.search(r'[@\d]', line):  # No email or numbers
                    return line.title()
        return "Candidate"

    def _extract_email(self, text):
        """Extract email from resume text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(email_pattern, text)
        return matches[0] if matches else "candidate@example.com"

    def _extract_phone(self, text):
        """Extract phone number from resume text"""
        phone_patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\+?\d{10,15}',
            r'\(\d{3}\)\s*\d{3}[-.\s]?\d{4}'
        ]
        
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0]
        return ""


# Global parser instance
resume_parser = ResumeParser()
