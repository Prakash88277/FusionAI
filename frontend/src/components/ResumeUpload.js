import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { uploadResume, uploadResumeAndRecommend } from '../services/api';

const ResumeUpload = ({ onUploadSuccess, useCompleteWorkflow = false }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (selectedFile.type === 'application/pdf' || 
          selectedFile.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
        setFile(selectedFile);
        setError('');
      } else {
        setFile(null);
        setError('Please upload a PDF or DOCX file');
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file to upload');
      return;
    }

    setUploading(true);
    setError('');
    
    try {
      console.log('Starting upload process...');
      console.log('File selected:', file.name, 'Size:', file.size);
      
      const formData = new FormData();
      formData.append('file', file);
      
      let response;
      if (useCompleteWorkflow) {
        console.log('Using complete workflow...');
        // Use complete workflow: parse resume + scrape jobs + match
        response = await uploadResumeAndRecommend(formData, "all", 20);
        
        // Store resume data
        if (response.data.resume_data) {
          localStorage.setItem('resumeId', response.data.resume_data.id || '');
          if (response.data.resume_data.country) {
            localStorage.setItem('resumeCountry', response.data.resume_data.country);
          }
        }
        
        // Store job recommendations
        if (response.data.job_recommendations) {
          localStorage.setItem('jobRecommendations', JSON.stringify(response.data.job_recommendations));
        }
      } else {
        console.log('Using simple upload...');
        // Use simple upload
        response = await uploadResume(formData);
        localStorage.setItem('resumeId', response.data.id || '');
        if (response.data.country) {
          localStorage.setItem('resumeCountry', response.data.country);
        }
      }
      
      console.log('Upload successful!', response.data);
      setUploading(false);
      
      // Call success callback if provided
      if (onUploadSuccess) {
        onUploadSuccess();
      } else {
        navigate('/dashboard');
      }
      
    } catch (err) {
      setUploading(false);
      console.error('Upload error:', err);
      
      // Better error handling
      let errorMessage = 'Failed to upload and parse resume';
      
      if (err.code === 'ERR_NETWORK' || err.code === 'ECONNREFUSED') {
        errorMessage = 'Server not reachable. Please start backend before uploading.';
      } else if (err.message && err.message.includes('Server not reachable')) {
        errorMessage = err.message;
      } else if (err.response?.data?.detail) {
        errorMessage = err.response.data.detail;
      } else if (err.message) {
        errorMessage = err.message;
      }
      
      setError(errorMessage);
    }
  };

  return (
    <div className="card">
      <h2>Upload Your Resume</h2>
      <p>Upload your resume to find matching jobs</p>
      
      <form onSubmit={handleSubmit}>
        <div className="resume-upload" onClick={() => document.getElementById('resume-file').click()}>
          <input
            type="file"
            id="resume-file"
            accept=".pdf,.docx"
            onChange={handleFileChange}
            style={{ display: 'none' }}
          />
          {file ? (
            <div>
              <p>Selected file: {file.name}</p>
              <p>Size: {(file.size / 1024 / 1024).toFixed(2)} MB</p>
            </div>
          ) : (
            <div>
              <p>Drag and drop your resume here or click to browse</p>
              <p>Supported formats: PDF, DOCX</p>
            </div>
          )}
        </div>
        
        {error && <p style={{ color: 'red' }}>{error}</p>}
        
        <button 
          type="submit" 
          className="btn btn-primary" 
          style={{ marginTop: '1rem', width: '100%' }}
          disabled={!file || uploading}
        >
          {uploading ? 'Uploading...' : 'Find Matching Jobs'}
        </button>
      </form>
    </div>
  );
};

export default ResumeUpload;