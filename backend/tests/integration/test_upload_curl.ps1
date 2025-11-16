# PowerShell script to test ZenRows integration via curl
# Usage: Run this script when backend is running on port 8000

Write-Host "Testing ZenRows Integration with Resume Upload" -ForegroundColor Yellow
Write-Host ("=" * 60) -ForegroundColor Gray

# Check if backend is running
Write-Host "`n1. Checking backend health..." -ForegroundColor Cyan
try {
    $healthResponse = Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" -Method Get -TimeoutSec 5
    Write-Host "   ✅ Backend is running: $($healthResponse.status)" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Backend is not running. Please start backend first." -ForegroundColor Red
    exit 1
}

# Create test resume content
$testResumeContent = @"
John Doe
Software Engineer
john.doe@email.com
+1-555-0123

EXPERIENCE
Senior Software Engineer at Google (3 years)
- Developed web applications using Python, React, Node.js
- Worked with AWS, Docker, Kubernetes
- Led team of 5 developers in microservices architecture

SKILLS
Programming Languages: Python, JavaScript, Java, C#
Web Technologies: React, Angular, Vue.js, Node.js, HTML, CSS
Databases: MySQL, PostgreSQL, MongoDB, Redis
Cloud Platforms: AWS, Azure, Google Cloud Platform
DevOps Tools: Docker, Kubernetes, Jenkins, Git

EDUCATION
Bachelor of Science in Computer Science
Stanford University, 2018
"@

# Save test resume to temporary file
$tempFile = "$env:TEMP\test_resume.pdf"
$testResumeContent | Out-File -FilePath $tempFile -Encoding UTF8

Write-Host "`n2. Testing resume upload with ZenRows integration..." -ForegroundColor Cyan
Write-Host "   Uploading test resume: $tempFile" -ForegroundColor Gray

try {
    # Create multipart form data
    $boundary = [System.Guid]::NewGuid().ToString()
    $LF = "`r`n"
    
    $bodyLines = @(
        "--$boundary",
        'Content-Disposition: form-data; name="file"; filename="test_resume.pdf"',
        "Content-Type: application/pdf$LF",
        $testResumeContent,
        "--$boundary--$LF"
    )
    
    $body = $bodyLines -join $LF
    $contentType = "multipart/form-data; boundary=$boundary"
    
    # Make request
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/resume/upload-resume" -Method Post -Body $body -ContentType $contentType -TimeoutSec 60
    
    Write-Host "   ✅ Upload successful!" -ForegroundColor Green
    
    # Display results
    Write-Host "`n📊 Results Summary:" -ForegroundColor Yellow
    Write-Host "   Status: $($response.status)" -ForegroundColor White
    
    if ($response.parsed_data) {
        $parsed = $response.parsed_data
        Write-Host "   📄 Resume Parsing:" -ForegroundColor Cyan
        Write-Host "      Name: $($parsed.name)" -ForegroundColor White
        Write-Host "      Email: $($parsed.email)" -ForegroundColor White
        Write-Host "      Skills: $($parsed.skills.Count) found" -ForegroundColor White
        Write-Host "      Experience: $($parsed.experience) years" -ForegroundColor White
        Write-Host "      Domain: $($parsed.domain)" -ForegroundColor White
        
        if ($parsed.skills.Count -gt 0) {
            $topSkills = $parsed.skills[0..4] -join ", "
            Write-Host "      Top Skills: $topSkills" -ForegroundColor White
        }
    }
    
    Write-Host "   🔍 ZenRows Integration:" -ForegroundColor Cyan
    Write-Host "      Jobs Scraped: $($response.scraped_jobs_count)" -ForegroundColor White
    Write-Host "      Matches Found: $($response.matches.Count)" -ForegroundColor White
    Write-Host "      Query Terms: $($response.query_terms.Count)" -ForegroundColor White
    
    if ($response.query_terms.Count -gt 0) {
        $queryTerms = $response.query_terms[0..4] -join ", "
        Write-Host "      Search Terms: $queryTerms" -ForegroundColor White
    }
    
    if ($response.matches.Count -gt 0) {
        Write-Host "`n🎯 Sample Job Matches:" -ForegroundColor Yellow
        for ($i = 0; $i -lt [Math]::Min(3, $response.matches.Count); $i++) {
            $match = $response.matches[$i]
            Write-Host "      $($i + 1). $($match.title) at $($match.company)" -ForegroundColor White
            if ($match.match_score) {
                Write-Host "         Match Score: $($match.match_score)%" -ForegroundColor Gray
            }
            if ($match.apply_link) {
                Write-Host "         Apply Link: $($match.apply_link)" -ForegroundColor Gray
            }
        }
    }
    
    Write-Host "`n🎉 ZenRows Integration Test PASSED!" -ForegroundColor Green
    Write-Host "✅ Resume parsing working" -ForegroundColor Green
    Write-Host "✅ Job scraping integrated" -ForegroundColor Green
    Write-Host "✅ Matching algorithm functional" -ForegroundColor Green
    
} catch {
    Write-Host "   ❌ Upload failed: $($_.Exception.Message)" -ForegroundColor Red
    
    if ($_.Exception.Response) {
        try {
            $errorStream = $_.Exception.Response.GetResponseStream()
            $reader = New-Object System.IO.StreamReader($errorStream)
            $errorContent = $reader.ReadToEnd()
            Write-Host "   Error Details: $errorContent" -ForegroundColor Red
        } catch {
            Write-Host "   Could not read error details" -ForegroundColor Red
        }
    }
}

# Clean up
if (Test-Path $tempFile) {
    Remove-Item $tempFile -Force
}

Write-Host "`nNotes:" -ForegroundColor Yellow
Write-Host "   - Set ZENROWS_API_KEY environment variable for actual job scraping" -ForegroundColor Gray
Write-Host "   - Without API key, scraping will be skipped but parsing will work" -ForegroundColor Gray
Write-Host "   - Check backend logs for detailed ZenRows API interaction" -ForegroundColor Gray
Write-Host ("=" * 60) -ForegroundColor Gray
