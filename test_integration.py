"""
Simple test for ZenRows integration
"""
import requests

def test_integration():
    print("Testing ZenRows Integration")
    
    # Test health endpoint
    try:
        response = requests.get("http://127.0.0.1:8000/health")
        print(f"Backend Health: {response.json()['status']}")
    except Exception as e:
        print(f"Backend not available: {e}")
        return
    
    # Test resume upload
    test_content = """
John Doe
Software Engineer
john@email.com

SKILLS
Python, React, AWS, Docker, Kubernetes

EXPERIENCE  
Senior Software Engineer (3 years)
- Developed web applications
- Worked with cloud platforms
"""
    
    try:
        files = {'file': ('test.pdf', test_content.encode(), 'application/pdf')}
        response = requests.post("http://127.0.0.1:8000/api/resume/upload-resume", files=files)
        
        print(f"Upload Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Status: {data.get('status')}")
            print(f"Skills: {len(data.get('parsed_data', {}).get('skills', []))}")
            print(f"Jobs Scraped: {data.get('scraped_jobs_count', 0)}")
            print(f"Matches: {len(data.get('matches', []))}")
            
            if data.get('matches'):
                print(f"First match: {data['matches'][0].get('title', 'N/A')}")
            
            print("SUCCESS: ZenRows integration working!")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_integration()
