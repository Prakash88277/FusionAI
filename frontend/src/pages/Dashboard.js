import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { searchJobs, matchJobsWithResume } from '../services/api';
import JobCard from '../components/JobCard';

const Dashboard = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [showFilters, setShowFilters] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const [filters, setFilters] = useState({
    location: '',
    company: '',
    salary_min: '',
    salary_max: '',
    experience_level: '',
    job_type: '',
    match_score: 'any'
  });

  const loadMatches = async () => {
    const resumeId = localStorage.getItem('resumeId');
    if (!resumeId) {
      setError('No resume found. Please upload a resume first.');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      console.log('Loading matches for resume ID:', resumeId);
      const response = await matchJobsWithResume(resumeId);
      console.log('Matched Jobs Response:', response.data);
      
      // Handle different response structures
      let jobsData = response.data;
      if (Array.isArray(jobsData)) {
        // Map JobMatch objects to Job objects for display
        const mappedJobs = jobsData.map(jm => ({
          id: jm.job.id,
          title: jm.job.title,
          company: jm.job.company,
          location: jm.job.location,
          description: jm.job.description,
          skills: jm.job.skills || [],
          apply_link: jm.job.apply_link,
          posted_date: jm.job.posted_date,
          match_score: jm.match_score,
          matching_skills: jm.matching_skills || [],
          missing_skills: jm.missing_skills || [],
          skill_match_percentage: jm.skill_match_percentage || 0,
          salary_text: jm.job.salary_text || jm.job.salary || 'Not specified',
          job_type: jm.job.job_type,
          experience_level: jm.job.experience_level,
          source: jm.job.source
        }));
        setJobs(mappedJobs);
      } else if (jobsData.jobs && Array.isArray(jobsData.jobs)) {
        setJobs(jobsData.jobs);
      } else {
        setJobs([]);
      }
      
      if (jobs.length === 0) {
        setError('No jobs found. Try adjusting your filters or upload another resume.');
      }
    } catch (err) {
      console.error('Error loading matches:', err);
      setError('Failed to load job matches');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    setLoading(true);
    setError('');
    
    try {
      const response = await searchJobs({
        keywords: searchTerm,
        ...filters
      });
      
      let jobsData = response.data;
      if (Array.isArray(jobsData)) {
        setJobs(jobsData);
      } else if (jobsData.jobs && Array.isArray(jobsData.jobs)) {
        setJobs(jobsData.jobs);
      } else {
        setJobs([]);
      }
    } catch (err) {
      console.error('Search error:', err);
      setError('Search failed');
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const clearFilters = () => {
    setFilters({
      location: '',
      company: '',
      salary_min: '',
      salary_max: '',
      experience_level: '',
      job_type: '',
      match_score: 'any'
    });
    setSearchTerm('');
  };

  useEffect(() => {
    loadMatches();
    
    // Show success message if coming from upload
    const uploadedResume = localStorage.getItem('resumeUploaded');
    if (uploadedResume) {
      setSuccessMessage('✅ Resume uploaded successfully! Matching jobs are being fetched...');
      localStorage.removeItem('resumeUploaded');
      setTimeout(() => setSuccessMessage(''), 5000);
    }
  }, []);

  // Filter jobs based on current filters
  const filteredJobs = jobs.filter(job => {
    if (filters.match_score !== 'any') {
      const minScore = parseInt(filters.match_score);
      if (job.match_score < minScore) return false;
    }
    
    if (filters.location && !job.location?.toLowerCase().includes(filters.location.toLowerCase())) {
      return false;
    }
    
    if (filters.company && !job.company?.toLowerCase().includes(filters.company.toLowerCase())) {
      return false;
    }
    
    if (filters.experience_level && job.experience_level !== filters.experience_level) {
      return false;
    }
    
    if (filters.job_type && job.job_type !== filters.job_type) {
      return false;
    }
    
    return true;
  });

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="py-6">
            <h1 className="text-3xl font-bold text-gray-900">Job Matching Dashboard</h1>
            <p className="mt-2 text-gray-600">Find your perfect job match based on your resume</p>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Success Message */}
        <AnimatePresence>
          {successMessage && (
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded-lg mb-6"
            >
              {successMessage}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-blue-100">
                <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" dopth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0H8m8 0v2a2 2 0 01-2 2H10a2 2 0 01-2-2V6" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Jobs</p>
                <p className="text-2xl font-bold text-gray-900">{jobs.length}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-green-100">
                <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">High Matches</p>
                <p className="text-2xl font-bold text-gray-900">
                  {jobs.filter(job => job.match_score >= 80).length}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-purple-100">
                <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Avg Match Score</p>
                <p className="text-2xl font-bold text-gray-900">
                  {jobs.length > 0 ? Math.round(jobs.reduce((sum, job) => sum + (job.match_score || 0), 0) / jobs.length) : 0}%
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Search and Filter Section */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 mb-8">
          <div className="p-6">
            <div className="flex flex-col lg:flex-row gap-4 mb-6">
              <div className="flex-1">
                <input
                  type="text"
                  placeholder="Search keywords, title, or skills"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => setShowFilters(!showFilters)}
                  className="px-4 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
                >
                  {showFilters ? 'Hide' : 'Show'} Filters
                </button>
                <button
                  onClick={handleSearch}
                  className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center"
                >
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                  Search
                </button>
                <button
                  onClick={loadMatches}
                  className="px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                >
                  Refresh
                </button>
              </div>
            </div>

            {/* Filters */}
            <AnimatePresence>
              {showFilters && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4"
                >
                  <select
                    value={filters.match_score}
                    onChange={(e) => handleFilterChange('match_score', e.target.value)}
                    className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="any">Any Score</option>
                    <option value="80">80%+ Match</option>
                    <option value="60">60%+ Match</option>
                    <option value="40">40%+ Match</option>
                  </select>

                  <select
                    value={filters.location}
                    onChange={(e) => handleFilterChange('location', e.target.value)}
                    className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">Any Location</option>
                    <option value="Bangalore">Bangalore</option>
                    <option value="Mumbai">Mumbai</option>
                    <option value="Delhi">Delhi</option>
                    <option value="Hyderabad">Hyderabad</option>
                    <option value="Chennai">Chennai</option>
                    <option value="Pune">Pune</option>
                  </select>

                  <select
                    value={filters.experience_level}
                    onChange={(e) => handleFilterChange('experience_level', e.target.value)}
                    className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">Any Experience</option>
                    <option value="entry">Entry Level</option>
                    <option value="mid">Mid Level</option>
                    <option value="senior">Senior Level</option>
                  </select>

                  <select
                    value={filters.job_type}
                    onChange={(e) => handleFilterChange('job_type', e.target.value)}
                    className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">Any Job Type</option>
                    <option value="full_time">Full Time</option>
                    <option value="part_time">Part Time</option>
                    <option value="internship">Internship</option>
                  </select>
                </motion.div>
              )}
            </AnimatePresence>

            {showFilters && (
              <div className="flex justify-end">
                <button
                  onClick={clearFilters}
                  className="text-sm text-gray-500 hover:text-gray-700 underline"
                >
                  Clear all filters
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-blue-600"></div>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        {/* Jobs Grid */}
        {!loading && !error && (
          <div>
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-gray-900">
                {filteredJobs.length > 0 ? `${filteredJobs.length} Jobs Found` : 'No Jobs Found'}
              </h2>
              {filteredJobs.length > 0 && (
                <p className="text-gray-600">
                  Showing {filteredJobs.length} of {jobs.length} jobs
                </p>
              )}
            </div>

            {filteredJobs.length > 0 ? (
              <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
                {filteredJobs.map((job, index) => (
                  <JobCard key={job.id || index} job={job} index={index} />
                ))}
              </div>
            ) : (
              <div className="text-center py-12">
                <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <h3 className="mt-2 text-sm font-medium text-gray-900">No jobs found</h3>
                <p className="mt-1 text-sm text-gray-500">
                  Try adjusting your search criteria or filters to find more jobs.
                </p>
                <div className="mt-6">
                  <button
                    onClick={clearFilters}
                    className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
                  >
                    Clear filters
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;