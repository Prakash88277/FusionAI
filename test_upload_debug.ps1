# Debug the upload endpoint
try {
    Write-Host "Testing Resume Upload Endpoint..." -ForegroundColor Yellow
    
    # Test the upload endpoint with detailed error handling
    $uploadUri = "http://127.0.0.1:8000/api/resume/upload-resume"
    Write-Host "Endpoint: $uploadUri" -ForegroundColor Cyan
    
    # Create test content
    $testContent = @"
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
"@
    
    # Create multipart form data
    $boundary = [System.Guid]::NewGuid().ToString()
    $LF = "`r`n"
    
    $bodyLines = @(
        "--$boundary",
        'Content-Disposition: form-data; name="file"; filename="test_resume.pdf"',
        "Content-Type: application/pdf$LF",
        $testContent,
        "--$boundary--$LF"
    )
    
    $body = $bodyLines -join $LF
    $contentType = "multipart/form-data; boundary=$boundary"
    
    Write-Host "Making request..." -ForegroundColor Cyan
    
    $response = Invoke-RestMethod -Uri $uploadUri -Method Post -Body $body -ContentType $contentType -Verbose
    
    Write-Host "SUCCESS!" -ForegroundColor Green
    Write-Host "Response:" -ForegroundColor White
    $response | ConvertTo-Json -Depth 5
    
} catch {
    Write-Host "ERROR DETAILS:" -ForegroundColor Red
    Write-Host "Exception Type: $($_.Exception.GetType().Name)" -ForegroundColor Red
    Write-Host "Exception Message: $($_.Exception.Message)" -ForegroundColor Red
    
    if ($_.Exception -is [System.Net.WebException]) {
        $webException = $_.Exception
        Write-Host "Web Exception Status: $($webException.Status)" -ForegroundColor Red
        
        if ($webException.Response) {
            $response = $webException.Response
            Write-Host "HTTP Status: $($response.StatusCode)" -ForegroundColor Red
            Write-Host "Status Description: $($response.StatusDescription)" -ForegroundColor Red
            
            try {
                $reader = New-Object System.IO.StreamReader($response.GetResponseStream())
                $errorContent = $reader.ReadToEnd()
                Write-Host "Error Response Body:" -ForegroundColor Red
                Write-Host $errorContent -ForegroundColor Red
            } catch {
                Write-Host "Could not read error response body" -ForegroundColor Red
            }
        }
    }
    
    Write-Host "Full Exception:" -ForegroundColor Red
    Write-Host $_.Exception.ToString() -ForegroundColor Red
}
