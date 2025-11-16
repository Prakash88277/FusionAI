"""
Test the resume upload API endpoint using Python requests
"""
import requests
import json

def test_upload_endpoint():
    """Test the upload endpoint"""
    
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
    
    print("Testing Resume Upload API...")
    print(f"URL: {url}")
    
    try:
        # Create a file-like object
        files = {
            'file': ('test_resume.pdf', resume_content.encode('utf-8'), 'application/pdf')
        }
        
        print("Making request...")
        
        response = requests.post(url, files=files, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("SUCCESS!")
            result = response.json()
            print("Response:")
            print(json.dumps(result, indent=2))
            
            # Print summary
            if 'parsed_data' in result:
                parsed = result['parsed_data']
                print(f"\nSummary:")
                print(f"  Skills found: {len(parsed.get('skills', []))}")
                print(f"  Experience: {parsed.get('experience', 0)} years")
                print(f"  Domain: {parsed.get('domain', 'unknown')}")
                print(f"  Roles: {parsed.get('roles', [])}")
        else:
            print(f"ERROR: {response.status_code}")
            print(f"Response text: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def test_simple_endpoint():
    """Test the simple test endpoint first"""
    url = "http://127.0.0.1:8000/api/resume/test"
    
    try:
        print(f"Testing simple endpoint: {url}")
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Simple endpoint test failed: {e}")
        return False

if __name__ == "__main__":
    print("Resume Parser API Test")
    print("=" * 40)
    
    # First test simple endpoint
    if test_simple_endpoint():
        print("\n" + "=" * 40)
        # Then test upload
        test_upload_endpoint()
    else:
        print("Cannot proceed - simple endpoint test failed")
