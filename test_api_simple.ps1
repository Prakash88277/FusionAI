# Simple test for the resume parser API
try {
    Write-Host "Testing Resume Parser API..." -ForegroundColor Yellow
    
    # Test with a simple GET request first to check if endpoint exists
    $testUri = "http://127.0.0.1:8000/api/resume/"
    Write-Host "Testing base endpoint: $testUri" -ForegroundColor Cyan
    
    try {
        $response = Invoke-WebRequest -Uri $testUri -Method GET -ErrorAction Stop
        Write-Host "Base endpoint accessible: $($response.StatusCode)" -ForegroundColor Green
    } catch {
        Write-Host "Base endpoint test failed: $($_.Exception.Message)" -ForegroundColor Yellow
    }
    
    # Now test the actual upload endpoint
    $uploadUri = "http://127.0.0.1:8000/api/resume/upload-resume"
    Write-Host "Testing upload endpoint: $uploadUri" -ForegroundColor Cyan
    
    # Create a simple multipart request
    $filePath = "test_resume_sample.pdf"
    $fileContent = Get-Content $filePath -Raw
    
    $boundary = [System.Guid]::NewGuid().ToString()
    $LF = "`r`n"
    
    $bodyLines = @(
        "--$boundary",
        'Content-Disposition: form-data; name="file"; filename="test_resume.pdf"',
        "Content-Type: application/pdf$LF",
        $fileContent,
        "--$boundary--$LF"
    )
    
    $body = $bodyLines -join $LF
    $contentType = "multipart/form-data; boundary=$boundary"
    
    $response = Invoke-RestMethod -Uri $uploadUri -Method Post -Body $body -ContentType $contentType
    
    Write-Host "SUCCESS!" -ForegroundColor Green
    Write-Host "Response:" -ForegroundColor White
    $response | ConvertTo-Json -Depth 5
    
} catch {
    Write-Host "ERROR:" -ForegroundColor Red
    Write-Host "Exception: $($_.Exception.Message)" -ForegroundColor Red
    
    if ($_.Exception.Response) {
        Write-Host "Status Code: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
        try {
            $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
            $errorContent = $reader.ReadToEnd()
            Write-Host "Error Content: $errorContent" -ForegroundColor Red
        } catch {
            Write-Host "Could not read error response" -ForegroundColor Red
        }
    }
}
