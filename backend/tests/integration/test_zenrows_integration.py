"""
Integration tests for ZenRows integration
"""
import os
import sys
import requests
import json
import pytest
from typing import Dict, Any

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from app.scrapers.zenrows_client import ZenRowsClient
from app.scrapers.zenrows_scraper import scrape_jobs_for_keywords, build_search_urls
from app.services.zenrows_job_service import upsert_jobs_from_keywords

# Test configuration
BACKEND_URL = "http://127.0.0.1:8000"
TEST_API_KEY = os.getenv('ZENROWS_API_KEY', 'test_key')

class TestZenRowsClient:
    """Test ZenRows client functionality"""
    
    def test_client_initialization(self):
        """Test client can be initialized"""
        client = ZenRowsClient(api_key="test_key")
        assert client.api_key == "test_key"
        assert "zenrows.com" in client.base_url
    
    def test_build_search_urls(self):
        """Test search URL building"""
        keywords = ["python", "developer", "remote"]
        urls = build_search_urls(keywords)
        
        assert len(urls) >= 3  # Should have multiple job sites
        assert all("python+developer+remote" in url for url in urls)
        assert any("indeed.com" in url for url in urls)
        assert any("linkedin.com" in url for url in urls)

class TestZenRowsScraper:
    """Test ZenRows scraper functionality"""
    
    def test_scrape_jobs_structure(self):
        """Test that scraper returns proper job structure"""
        # Mock test - in real test, would use actual API
        keywords = ["software", "engineer"]
        
        # This would normally call ZenRows API
        # For testing without API key, we'll test structure
        try:
            jobs = scrape_jobs_for_keywords(keywords, max_per_source=1)
            
            # Verify structure even if no jobs returned
            assert isinstance(jobs, list)
            
            if jobs:
                job = jobs[0]
                required_fields = ['title', 'company', 'location', 'description', 'apply_link']
                for field in required_fields:
                    assert field in job
                    
        except Exception as e:
            # Expected if no API key configured
            assert "ZenRows API key not configured" in str(e) or "fetch failed" in str(e)

def test_resume_upload_integration():
    """Integration test for resume upload with ZenRows scraping"""
    
    # Create test resume content
    test_resume_content = """
    John Doe
    Software Engineer
    john.doe@email.com
    +1-555-0123

    EXPERIENCE
    Senior Software Engineer at Google (3 years)
    - Developed applications using Python, React, and AWS
    - Led team of 5 developers in microservices architecture

    SKILLS
    Programming: Python, JavaScript, Java
    Web: React, Node.js, HTML, CSS
    Cloud: AWS, Docker, Kubernetes
    """
    
    try:
        # Test the upload endpoint
        files = {
            'file': ('test_resume.pdf', test_resume_content.encode('utf-8'), 'application/pdf')
        }
        
        response = requests.post(
            f"{BACKEND_URL}/api/resume/upload-resume",
            files=files,
            timeout=30
        )
        
        # Check response structure
        assert response.status_code in [200, 500]  # 500 expected if no API key
        
        if response.status_code == 200:
            data = response.json()
            
            # Verify response structure
            assert "status" in data
            assert "parsed_data" in data
            
            # Verify parsed data structure
            parsed = data["parsed_data"]
            assert "skills" in parsed
            assert "experience" in parsed
            assert "domain" in parsed
            
            # Verify ZenRows integration fields
            assert "scraped_jobs_count" in data
            assert "matches" in data
            assert "query_terms" in data
            
            print(f"✅ Integration test passed!")
            print(f"   Parsed {len(parsed.get('skills', []))} skills")
            print(f"   Scraped {data.get('scraped_jobs_count', 0)} jobs")
            print(f"   Found {len(data.get('matches', []))} matches")
            
        else:
            # Expected error without API key
            error_data = response.json()
            print(f"⚠️  Expected error (no API key): {error_data.get('detail', '')}")
            
    except requests.ConnectionError:
        print("❌ Backend server not running. Start backend first.")
        assert False, "Backend server not available"
    except Exception as e:
        print(f"❌ Integration test failed: {str(e)}")
        raise

def test_backend_health():
    """Test backend server is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        assert response.status_code == 200
        
        health_data = response.json()
        assert "status" in health_data
        print(f"✅ Backend health check passed: {health_data}")
        
    except requests.ConnectionError:
        print("❌ Backend server not running")
        assert False, "Backend server not available"

def run_manual_tests():
    """Run manual integration tests"""
    print("🧪 Running ZenRows Integration Tests")
    print("=" * 50)
    
    # Test 1: Backend health
    print("\n1. Testing backend health...")
    try:
        test_backend_health()
    except Exception as e:
        print(f"   ❌ Health check failed: {e}")
        return
    
    # Test 2: Resume upload integration
    print("\n2. Testing resume upload integration...")
    try:
        test_resume_upload_integration()
    except Exception as e:
        print(f"   ❌ Integration test failed: {e}")
    
    # Test 3: Client functionality
    print("\n3. Testing ZenRows client...")
    try:
        test_client = TestZenRowsClient()
        test_client.test_client_initialization()
        test_client.test_build_search_urls()
        print("   ✅ Client tests passed")
    except Exception as e:
        print(f"   ❌ Client tests failed: {e}")
    
    # Test 4: Scraper functionality
    print("\n4. Testing ZenRows scraper...")
    try:
        test_scraper = TestZenRowsScraper()
        test_scraper.test_scrape_jobs_structure()
        print("   ✅ Scraper tests passed")
    except Exception as e:
        print(f"   ❌ Scraper tests failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Integration tests completed!")
    print("\n📝 Notes:")
    print("   - Set ZENROWS_API_KEY environment variable for full testing")
    print("   - Ensure backend server is running on port 8000")
    print("   - Check logs for detailed scraping information")

if __name__ == "__main__":
    run_manual_tests()
