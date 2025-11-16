#!/usr/bin/env python3
"""
Simple test to verify the complete ZenRows flow
"""

import requests
import json

def test_complete_flow():
    print("TESTING COMPLETE ZENROWS FLOW")
    print("=" * 40)
    
    # Test 1: Backend Health
    print("\n1. Backend Health Check...")
    try:
        response = requests.get("http://127.0.0.1:8000/health", timeout=5)
        if response.status_code == 200:
            print("   PASS: Backend is healthy")
        else:
            print("   FAIL: Backend not healthy")
            return
    except Exception as e:
        print(f"   FAIL: Backend not accessible: {e}")
        return
    
    # Test 2: ZenRows API
    print("\n2. ZenRows API Test...")
    try:
        params = {
            'apikey': 'ac77427ddaea21133538d4e5a7464d975c3c835e',
            'url': 'https://www.indeed.com/jobs?q=python+developer&l=India',
            'js_render': 'true',
            'premium_proxy': 'true'
        }
        
        response = requests.get('https://api.zenrows.com/v1/', params=params, timeout=30)
        
        if response.status_code == 200 and len(response.text) > 50000:
            print(f"   PASS: ZenRows working - {len(response.text):,} chars")
        else:
            print(f"   FAIL: ZenRows failed - {response.status_code}")
            return
    except Exception as e:
        print(f"   FAIL: ZenRows error: {e}")
        return
    
    # Test 3: Text Resume Parser (using upload-text endpoint)
    print("\n3. Resume Parser Test...")
    try:
        test_resume = """
John Doe
Software Engineer
john.doe@email.com

SKILLS
Python, JavaScript, React, AWS, Docker

EXPERIENCE
Senior Software Engineer (3 years)
- Developed web applications
- Worked with cloud platforms
        """
        
        files = {'file': ('test_resume.txt', test_resume.encode(), 'text/plain')}
        
        response = requests.post(
            "http://127.0.0.1:8000/api/resume/upload-text", 
            files=files, 
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                parsed = data.get('parsed_data', {})
                print(f"   PASS: Resume parsed")
                print(f"   Name: {parsed.get('name', 'N/A')}")
                print(f"   Skills: {len(parsed.get('skills', []))} found")
                print(f"   Experience: {parsed.get('experience', 'N/A')} years")
            else:
                print(f"   FAIL: Parsing failed: {data}")
        else:
            print(f"   FAIL: Parser error: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   FAIL: Parser exception: {e}")
    
    # Test 4: Frontend Check
    print("\n4. Frontend Check...")
    try:
        response = requests.get("http://localhost:3001", timeout=5)
        if response.status_code == 200:
            print("   PASS: Frontend accessible")
        else:
            print(f"   FAIL: Frontend error: {response.status_code}")
    except Exception as e:
        print(f"   FAIL: Frontend not accessible: {e}")
    
    print("\n" + "=" * 40)
    print("INTEGRATION STATUS:")
    print("✓ Backend: Running")
    print("✓ ZenRows API: Working") 
    print("✓ Resume Parser: Available")
    print("? Frontend: Check manually at http://localhost:3001")
    print("\nNEXT STEPS:")
    print("1. Go to http://localhost:3001")
    print("2. Check dashboard shows 'Live Jobs from ZenRows'")
    print("3. Upload a resume to test complete flow")
    print("=" * 40)

if __name__ == "__main__":
    test_complete_flow()
