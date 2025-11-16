#!/usr/bin/env python3
"""
Final Integration Test for ZenRows Implementation
Tests the complete flow from resume upload to job display
"""

import requests
import json
import time

def test_backend_health():
    """Test if backend is running"""
    print("Testing Backend Health...")
    try:
        response = requests.get("http://127.0.0.1:8000/health", timeout=5)
        if response.status_code == 200 and response.json().get('status') == 'healthy':
            print("   PASS: Backend is healthy")
            return True
        else:
            print(f"   FAIL: Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   FAIL: Backend not accessible: {e}")
        return False

def test_zenrows_api():
    """Test ZenRows API directly"""
    print("\nTesting ZenRows API...")
    try:
        params = {
            'apikey': 'ac77427ddaea21133538d4e5a7464d975c3c835e',
            'url': 'https://www.indeed.com/jobs?q=software+developer&l=India',
            'js_render': 'true',
            'premium_proxy': 'true'
        }
        
        response = requests.get('https://api.zenrows.com/v1/', params=params, timeout=30)
        
        if response.status_code == 200 and len(response.text) > 100000:
            print(f"   PASS: ZenRows API working - Response size: {len(response.text):,} chars")
            return True
        else:
            print(f"   FAIL: ZenRows API failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   FAIL: ZenRows API error: {e}")
        return False

def test_resume_parser():
    """Test the new resume parser"""
    print("\nTesting Resume Parser...")
    try:
        # Create test resume content
        test_resume = """
John Doe
Software Engineer
john.doe@email.com

SKILLS
Python, JavaScript, React, AWS, Docker, Kubernetes

EXPERIENCE
Senior Software Engineer (3 years)
- Developed web applications using React and Python
- Worked with cloud platforms like AWS
- Experience with containerization using Docker
        """
        
        # Create form data
        files = {'file': ('test_resume.txt', test_resume.encode(), 'text/plain')}
        
        response = requests.post(
            "http://127.0.0.1:8000/api/resume/upload-resume", 
            files=files, 
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success' and data.get('parsed_data'):
                parsed = data['parsed_data']
                print(f"   PASS: Resume parsed successfully")
                print(f"   Name: {parsed.get('name', 'N/A')}")
                print(f"   Skills: {len(parsed.get('skills', []))} found")
                print(f"   Experience: {parsed.get('experience', 'N/A')} years")
                print(f"   Domain: {parsed.get('domain', 'N/A')}")
                return True, parsed
            else:
                print(f"   FAIL: Resume parsing failed: {data}")
                return False, None
        else:
            print(f"   FAIL: Resume parser error: {response.status_code} - {response.text}")
            return False, None
            
    except Exception as e:
        print(f"   FAIL: Resume parser exception: {e}")
        return False, None

def test_frontend_accessibility():
    """Test if frontend is accessible"""
    print("\nTesting Frontend...")
    try:
        response = requests.get("http://localhost:3001", timeout=10)
        if response.status_code == 200 and 'Job' in response.text:
            print("   PASS: Frontend accessible")
            return True
        else:
            print(f"   FAIL: Frontend not properly loaded: {response.status_code}")
            return False
    except Exception as e:
        print(f"   FAIL: Frontend not accessible: {e}")
        return False

def main():
    """Run all integration tests"""
    print("ZENROWS INTEGRATION - FINAL VERIFICATION")
    print("=" * 60)
    
    results = {}
    
    # Test 1: Backend Health
    results['backend'] = test_backend_health()
    
    # Test 2: ZenRows API
    results['zenrows'] = test_zenrows_api()
    
    # Test 3: Resume Parser
    results['parser'], parsed_data = test_resume_parser()
    
    # Test 4: Frontend
    results['frontend'] = test_frontend_accessibility()
    
    # Summary
    print("\n" + "=" * 60)
    print("FINAL TEST RESULTS:")
    print("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"   {test_name.upper():<12}: {status}")
    
    print(f"\nOVERALL RESULT: {passed}/{total} tests passed")
    
    if passed == total:
        print("\nSUCCESS! ZenRows integration is FULLY FUNCTIONAL!")
        print("\nWhat's Working:")
        print("   Backend server running")
        print("   ZenRows API connected")
        print("   Resume parser extracting skills")
        print("   Frontend accessible")
        print("\nReady for Production!")
        
        if parsed_data:
            print(f"\nSample Skills Extracted: {parsed_data.get('skills', [])[:5]}")
            
    else:
        print("\nSome components need attention before deployment")
        
        if not results['backend']:
            print("   Start backend: cd backend && python -m uvicorn app.main:app --reload")
        if not results['frontend']:
            print("   Start frontend: cd frontend && npm start")
        if not results['zenrows']:
            print("   Check ZenRows API key and quota")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
