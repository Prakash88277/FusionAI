import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getJobById } from '../services/api';

const JobDetails = () => {
  const { id } = useParams();
  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchJob = async () => {
      try {
        const { data } = await getJobById(id);
        // Map backend Job to UI shape used here
        const jobFromApi = {
          id: data.id,
          title: data.title,
          company: data.company,
          location: data.location,
          country: data.country,
          salary: data.salary,
          postedDate: data.posted_date,
          skills: data.skills || [],
          matchScore: data.match_score || 0,
          applyLink: data.apply_link,
          description: data.description,
          requirements: (data.description || '').split('. ').slice(0, 5).filter(Boolean),
          responsibilities: (data.description || '').split('. ').slice(0, 5).filter(Boolean),
          matchingSkills: data.matching_skills || [],
          missingSkills: data.missing_skills || [],
        };
        setJob(jobFromApi);
      } catch (err) {
        console.error('Error fetching job details:', err);
        setError('Failed to load job details');
        setJob(null);
      } finally {
        setLoading(false);
      }
    };
    fetchJob();
  }, [id]);

  if (loading) {
    return (
      <div className="container py-4">
        <div className="d-flex justify-content-center align-items-center flex-column" style={{ height: '50vh' }}>
          <div className="spinner-border" role="status"></div>
          <h6 className="mt-2">Loading job details...</h6>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container py-4">
        <div className="alert alert-danger mb-2">
          {error}
        </div>
        <Link to="/dashboard" className="btn btn-primary">
          ← Back to Jobs
        </Link>
      </div>
    );
  }

  if (!job) {
    return (
      <div className="container py-4">
        <div className="alert alert-warning mb-2">
          Job not found
        </div>
        <Link to="/dashboard" className="btn btn-primary">
          ← Back to Jobs
        </Link>
      </div>
    );
  }
  
  return (
    <div className="container py-4">
      <div className="mb-4">
        <Link to="/dashboard" className="btn btn-outline-primary mb-3">
          ← Back to Jobs
        </Link>
        
        <div className="card mb-4">
          <div className="card-body">
            <h2 className="card-title mb-3">{job.title}</h2>
            
            <div className="d-flex flex-wrap mb-3">
              <div className="me-4 mb-2 d-flex align-items-center">
                <span className="me-1">🏢</span>
                <span>{job.company}</span>
              </div>
              
              <div className="me-4 mb-2 d-flex align-items-center">
                <span className="me-1">📍</span>
                <span>{job.location}</span>
              </div>
              
              {job.salary && (
                <div className="me-4 mb-2 d-flex align-items-center">
                  <span className="me-1">💰</span>
                  <span>{job.salary}</span>
                </div>
              )}
              
              {job.postedDate && (
                <div className="me-4 mb-2 d-flex align-items-center">
                  <span className="me-1">📅</span>
                  <span>Posted: {job.postedDate}</span>
                </div>
              )}
            </div>
            
            {job.matchScore !== undefined && (
              <div className="mb-4">
                <h5>Match Score: {Math.round(job.matchScore)}%</h5>
                <div className="progress" style={{height: '10px', borderRadius: '5px'}}>
                  <div 
                    className={`progress-bar ${job.matchScore > 70 ? 'bg-success' : job.matchScore > 40 ? 'bg-warning' : 'bg-danger'}`}
                    role="progressbar" 
                    style={{width: `${job.matchScore}%`}}
                    aria-valuenow={job.matchScore} 
                    aria-valuemin="0" 
                    aria-valuemax="100"
                  ></div>
                </div>
              </div>
            )}
          </div>
        </div>
        
        <div className="row">
          <div className="col-md-8">
            <div className="card mb-4">
              <div className="card-body">
                <h4 className="card-title mb-3">Job Description</h4>
                <p className="card-text" style={{whiteSpace: 'pre-line'}}>{job.description}</p>
              </div>
            </div>
          </div>
          
          <div className="col-md-4">
            {job.matchingSkills && job.matchingSkills.length > 0 && (
              <div className="card mb-4">
                <div className="card-body">
                  <h5 className="card-title mb-3">
                    <span className="text-success">✓</span> Matching Skills
                  </h5>
                  <div>
                    {job.matchingSkills.map((skill, index) => (
                      <span key={index} className="badge bg-success me-2 mb-2">{skill}</span>
                    ))}
                  </div>
                </div>
              </div>
            )}
            
            {job.missingSkills && job.missingSkills.length > 0 && (
              <div className="card mb-4">
                <div className="card-body">
                  <h5 className="card-title mb-3">
                    <span className="text-danger">✗</span> Skills to Develop
                  </h5>
                  <div>
                    {job.missingSkills.map((skill, index) => (
                      <span key={index} className="badge bg-danger me-2 mb-2">{skill}</span>
                    ))}
                  </div>
                </div>
              </div>
            )}
            
            <div className="card">
              <div className="card-body">
                <h5 className="card-title mb-3">Job Details</h5>
                <ul className="list-group list-group-flush">
                  {job.jobType && (
                    <li className="list-group-item d-flex align-items-center">
                      <span className="me-2">⏱️</span>
                      <div>
                        <strong>Job Type</strong>
                        <div>{job.jobType}</div>
                      </div>
                    </li>
                  )}
                  
                  {job.experienceLevel && (
                    <li className="list-group-item d-flex align-items-center">
                      <span className="me-2">📊</span>
                      <div>
                        <strong>Experience</strong>
                        <div>{job.experienceLevel}</div>
                      </div>
                    </li>
                  )}
                  
                  {job.educationLevel && (
                    <li className="list-group-item d-flex align-items-center">
                      <span className="me-2">🎓</span>
                      <div>
                        <strong>Education</strong>
                        <div>{job.educationLevel}</div>
                      </div>
                    </li>
                  )}
                  
                  {job.country && (
                    <li className="list-group-item d-flex align-items-center">
                      <span className="me-2">🌎</span>
                      <div>
                        <strong>Country</strong>
                        <div>{job.country}</div>
                      </div>
                    </li>
                  )}
                  
                  {job.source && (
                    <li className="list-group-item d-flex align-items-center">
                      <span className="me-2">🔍</span>
                      <div>
                        <strong>Source</strong>
                        <div>{job.source}</div>
                      </div>
                    </li>
                  )}
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Helper function to generate mock job details
const generateMockJobDetails = (id) => {
  const companies = ['Google', 'Microsoft', 'Amazon', 'LinkedIn', 'Facebook'];
  const locations = ['Bangalore', 'Hyderabad', 'Mumbai', 'Delhi', 'Remote'];
  const titles = ['Software Engineer', 'Data Scientist', 'Frontend Developer', 'Backend Developer', 'Full Stack Developer'];
  
  const allSkills = [
    'Python', 'Django', 'Flask', 'SQL', 'AWS',
    'JavaScript', 'React', 'Node.js', 'MongoDB', 'Express',
    'Java', 'Spring Boot', 'Hibernate', 'MySQL', 'Docker',
    'C++', 'Data Structures', 'Algorithms', 'System Design',
    'HTML', 'CSS', 'TypeScript', 'Angular', 'Vue.js'
  ];
  
  // Generate a random set of skills for the job
  const shuffled = [...allSkills].sort(() => 0.5 - Math.random());
  const jobSkills = shuffled.slice(0, 8);
  
  // Generate matching and missing skills
  const matchingSkills = jobSkills.slice(0, 5);
  const missingSkills = jobSkills.slice(5);
  
  const matchScore = Math.floor(Math.random() * 41) + 60; // 60-100%
  const minSalary = Math.floor(Math.random() * 10) + 5; // 5-15 LPA
  const maxSalary = minSalary + Math.floor(Math.random() * 10) + 2; // min + (2-12) LPA
  
  const requirements = [
    `${Math.floor(Math.random() * 5) + 1}-${Math.floor(Math.random() * 5) + 5} years of experience in ${jobSkills[0]} and ${jobSkills[1]}`,
    `Strong knowledge of ${jobSkills.slice(0, 3).join(', ')}`,
    `Experience with ${jobSkills.slice(3, 5).join(' and ')}`,
    'Bachelor\'s degree in Computer Science or related field',
    'Excellent problem-solving and communication skills'
  ];
  
  const responsibilities = [
    `Develop and maintain applications using ${jobSkills.slice(0, 3).join(', ')}`,
    `Collaborate with cross-functional teams to define, design, and ship new features`,
    `Optimize application for maximum speed and scalability`,
    `Participate in code reviews and mentor junior developers`,
    `Stay up-to-date with latest industry trends and technologies`
  ];
  
  return {
    id,
    title: titles[id % titles.length],
    company: companies[id % companies.length],
    location: locations[id % locations.length],
    salary: `₹${minSalary} - ${maxSalary} LPA`,
    postedDate: `${Math.floor(Math.random() * 30) + 1} days ago`,
    skills: jobSkills,
    matchScore,
    applyLink: 'https://example.com/apply',
    description: `We are looking for a talented ${titles[id % titles.length]} to join our team. This role requires expertise in ${jobSkills.join(', ')}. You will be working on cutting-edge projects and collaborating with a team of experienced professionals.`,
    requirements,
    responsibilities,
    matchingSkills,
    missingSkills
  };
};

export default JobDetails;