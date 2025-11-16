"""
Test with a simple text file but .docx extension to see if docx parsing works
"""
import requests
import json

def test_with_docx():
    """Test with .docx extension"""
    
    url = "http://127.0.0.1:8000/api/resume/upload-resume"
    
    # Create test resume content
    resume_content = """
John Doe
Software Engineer
john.doe@email.com
+1-234-567-8900

EXPERIENCE
Software Engineer at Google (3 years)
- Developed web applications using React, Node.js, and Python
- Worked with AWS, Docker, and Kubernetes

SKILLS
Programming Languages: Python, JavaScript, Java
Web Technologies: React, Angular, HTML, CSS
Databases: MySQL, MongoDB
Cloud: AWS, Docker
"""
    
    print("Testing with .docx extension...")
    
    try:
        # Create a file-like object with .docx extension
        files = {
            'file': ('test_resume.docx', resume_content.encode('utf-8'), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        }
        
        response = requests.post(url, files=files, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("SUCCESS!")
            result = response.json()
            print(json.dumps(result, indent=2))
        else:
            print(f"ERROR: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_with_docx()
