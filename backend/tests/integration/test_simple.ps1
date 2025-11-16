# Simple test for ZenRows integration
Write-Host "Testing ZenRows Integration" -ForegroundColor Yellow

# Check backend health
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" -Method Get -TimeoutSec 5
    Write-Host "Backend Status: $($response.status)" -ForegroundColor Green
} catch {
    Write-Host "Backend not running" -ForegroundColor Red
    exit 1
}

# Test resume upload
$testContent = @"
John Doe
Software Engineer  
john@email.com

SKILLS
Python, React, AWS, Docker

EXPERIENCE
3 years as Software Developer
"@

$tempFile = "$env:TEMP\test_resume.pdf"
$testContent | Out-File -FilePath $tempFile -Encoding UTF8

try {
    $boundary = [System.Guid]::NewGuid().ToString()
    $body = @"
--$boundary
Content-Disposition: form-data; name="file"; filename="test.pdf"
Content-Type: application/pdf

$testContent
--$boundary--
"@

    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/resume/upload-resume" -Method Post -Body $body -ContentType "multipart/form-data; boundary=$boundary" -TimeoutSec 30
    
    Write-Host "Upload Status: $($response.status)" -ForegroundColor Green
    Write-Host "Skills Found: $($response.parsed_data.skills.Count)" -ForegroundColor Cyan
    Write-Host "Jobs Scraped: $($response.scraped_jobs_count)" -ForegroundColor Cyan
    Write-Host "Matches: $($response.matches.Count)" -ForegroundColor Cyan
    
    if ($response.matches.Count -gt 0) {
        Write-Host "Sample Match: $($response.matches[0].title)" -ForegroundColor White
    }
    
    Write-Host "SUCCESS: ZenRows integration working!" -ForegroundColor Green
    
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
} finally {
    if (Test-Path $tempFile) { Remove-Item $tempFile -Force }
}

Write-Host "Test completed" -ForegroundColor Yellow
