import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ResumeUpload from '../components/ResumeUpload';

const Home = () => {
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const navigate = useNavigate();

  const handleUploadSuccess = () => {
    setUploadSuccess(true);
    // Set flag for dashboard to show success message
    localStorage.setItem('resumeUploaded', 'true');
    // Navigate to dashboard after successful upload
    setTimeout(() => {
      navigate('/dashboard');
    }, 1000);
  };

  return (
    <div>
      <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <h1>AI-Powered Resume-Based Job Search</h1>
        <p>Upload your resume and let AI find the perfect job matches for you</p>
      </div>
      
      <div style={{ maxWidth: '600px', margin: '0 auto' }}>
        {uploadSuccess ? (
          <div className="alert alert-success text-center">
            <h4>✅ Resume Uploaded Successfully!</h4>
            <p>Processing your resume and finding matching jobs...</p>
            <div className="spinner-border" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
          </div>
        ) : (
          <ResumeUpload 
            useCompleteWorkflow={true} 
            onUploadSuccess={handleUploadSuccess}
          />
        )}
      </div>
      
      <div style={{ marginTop: '3rem' }}>
        <h2>How It Works</h2>
        <div style={{ display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem', marginTop: '1rem' }}>
          <div className="card" style={{ flex: '1 1 300px' }}>
            <h3>1. Upload Your Resume</h3>
            <p>Upload your resume in PDF or DOCX format</p>
          </div>
          <div className="card" style={{ flex: '1 1 300px' }}>
            <h3>2. AI Analysis</h3>
            <p>Our AI extracts your skills, experience, and education</p>
          </div>
          <div className="card" style={{ flex: '1 1 300px' }}>
            <h3>3. Job Matching</h3>
            <p>We match your profile with jobs from multiple platforms</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;