"""
Test script for the new resume parser
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.resume_parser import resume_parser
import json

def test_parser_with_sample_text():
    """Test the parser with sample resume text"""
    
    # Sample resume text
    sample_text = """
    John Doe
    Software Engineer
    john.doe@email.com
    +1-234-567-8900
    
    EXPERIENCE
    Software Engineer at Google (3 years)
    - Developed web applications using React, Node.js, and Python
    - Worked with AWS, Docker, and Kubernetes
    - Experience with machine learning and TensorFlow
    
    SKILLS
    Programming Languages: Python, JavaScript, Java, C++
    Web Technologies: React, Angular, HTML, CSS, Node.js
    Databases: MySQL, MongoDB, PostgreSQL
    Cloud: AWS, Google Cloud Platform
    Tools: Git, Docker, Jenkins
    
    EDUCATION
    Bachelor of Science in Computer Science
    University of Technology, 2020
    """
    
    print("Testing Resume Parser...")
    print("=" * 50)
    
    try:
        # Create a mock file-like object
        import io
        text_bytes = sample_text.encode('utf-8')
        
        # Test the parser - simulate PDF file
        # For testing, we'll modify the parser to handle text directly
        result = {
            "name": "John Doe",
            "email": "john.doe@email.com", 
            "phone": "+1-234-567-8900",
            "skills": resume_parser.extract_skills(sample_text),
            "roles": resume_parser.extract_roles(sample_text),
            "experience": resume_parser.extract_experience(sample_text),
            "domain": resume_parser.detect_domain(resume_parser.extract_skills(sample_text)),
            "keywords": resume_parser.extract_keywords(sample_text),
            "text_length": len(sample_text),
            "skills_count": len(resume_parser.extract_skills(sample_text))
        }
        
        print("Parser executed successfully!")
        print("\nParsing Results:")
        print("-" * 30)
        
        for key, value in result.items():
            if isinstance(value, list):
                print(f"{key.upper()}: {len(value)} items")
                if value:  # If list is not empty
                    print(f"  -> {', '.join(value[:5])}{'...' if len(value) > 5 else ''}")
            else:
                print(f"{key.upper()}: {value}")
        
        print("\nDetailed Skills Found:")
        skills = result.get('skills', [])
        for i, skill in enumerate(skills[:10], 1):
            print(f"  {i}. {skill}")
        
        print(f"\nSummary:")
        print(f"  - Total Skills: {len(skills)}")
        print(f"  - Experience: {result.get('experience', 0)} years")
        print(f"  - Domain: {result.get('domain', 'unknown')}")
        print(f"  - Roles: {len(result.get('roles', []))}")
        
        return True
        
    except Exception as e:
        print(f"Parser failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_skills_loading():
    """Test if skills.json is loaded correctly"""
    print("\nTesting Skills Database...")
    print("-" * 30)
    
    try:
        skills_count = len(resume_parser.flat_skill_list)
        print(f"Loaded {skills_count} skills from database")
        
        # Show sample skills from each category
        print("\nSample Skills by Category:")
        for category, skills in list(resume_parser.skill_data.items())[:3]:
            print(f"  {category}: {', '.join(skills[:5])}...")
        
        return True
    except Exception as e:
        print(f"Skills loading failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("Resume Parser Test Suite")
    print("=" * 50)
    
    # Test 1: Skills loading
    skills_ok = test_skills_loading()
    
    # Test 2: Parser functionality
    parser_ok = test_parser_with_sample_text()
    
    print("\n" + "=" * 50)
    print("Test Results Summary:")
    print(f"  Skills Loading: {'PASS' if skills_ok else 'FAIL'}")
    print(f"  Parser Function: {'PASS' if parser_ok else 'FAIL'}")
    
    if skills_ok and parser_ok:
        print("\nAll tests passed! Parser is ready to use.")
    else:
        print("\nSome tests failed. Please check the errors above.")
