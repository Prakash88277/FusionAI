from pydantic import BaseModel
from typing import List, Optional

class Education(BaseModel):
    degree: str
    university: str
    year: Optional[str] = None

class Experience(BaseModel):
    company: str
    role: str
    duration: Optional[str] = None
    description: Optional[str] = None

class Project(BaseModel):
    name: str
    description: Optional[str] = None
    technologies: Optional[List[str]] = None

class ResumeData(BaseModel):
    id: Optional[str] = None
    name: str
    email: str
    phone: Optional[str] = None
    country: Optional[str] = None
    skills: List[str]
    education: List[Education]
    experience: List[Experience]
    projects: Optional[List[Project]] = None
    keywords: List[str]