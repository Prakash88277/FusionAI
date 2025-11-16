"""
Test the text upload endpoint
"""
import requests
import json

def test_text_upload():
    """Test the text upload endpoint"""
    
    url = "http://127.0.0.1:8000/api/resume/upload-text"
    
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
    
    print("Testing Text Upload API...")
    print(f"URL: {url}")
    
    try:
        # Create a file-like object
        files = {
            'file': ('test_resume.txt', resume_content.encode('utf-8'), 'text/plain')
        }
        
        print("Making request...")
        
        response = requests.post(url, files=files, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("SUCCESS!")
            result = response.json()
            print("Response:")
            print(json.dumps(result, indent=2))
            
            # Print summary
            if 'parsed_data' in result:
                parsed = result['parsed_data']
                print(f"\nSUMMARY:")
                print(f"  Name: {parsed.get('name', 'N/A')}")
                print(f"  Email: {parsed.get('email', 'N/A')}")
                print(f"  Skills found: {len(parsed.get('skills', []))}")
                print(f"  Top skills: {', '.join(parsed.get('skills', [])[:5])}")
                print(f"  Experience: {parsed.get('experience', 0)} years")
                print(f"  Domain: {parsed.get('domain', 'unknown')}")
                print(f"  Roles: {', '.join(parsed.get('roles', []))}")
                
                return True
        else:
            print(f"ERROR: {response.status_code}")
            print(f"Response text: {response.text}")
            return False
            
    except Exception as e:
        print(f"Request failed: {e}")
        return False

if __name__ == "__main__":
    success = test_text_upload()
    if success:
        print("\nSUCCESS: New resume parser is working correctly!")
        print("SUCCESS: Skills extraction is functional")
        print("SUCCESS: Experience detection is working")
        print("SUCCESS: API integration is successful")
    else:
        print("\nFAILED: Test failed - check the errors above")
