import axios from 'axios';

// Create an axios instance with base URL
const API_BASE = process.env.REACT_APP_API_BASE || "http://127.0.0.1:8000/api";
const API = axios.create({
  baseURL: API_BASE,
  timeout: 120000, // 120 second timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to include auth token and log requests
API.interceptors.request.use(
  (config) => {
    console.log(`Making request to: ${config.baseURL}${config.url}`);
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    if (user.token) {
      config.headers.Authorization = `Bearer ${user.token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add a response interceptor for better error handling
API.interceptors.response.use(
  (response) => {
    console.log(`Response received from: ${response.config.url}`, response.status);
    return response;
  },
  (error) => {
    console.error('API Error:', error);

    if (error.code === 'ERR_NETWORK' || error.code === 'ECONNREFUSED') {
      error.message = 'Server not reachable. Please start backend before uploading.';
    } else if (error.response) {
      // Server responded with error status
      error.message = error.response.data?.detail || error.response.data?.message || 'Server error occurred';
    } else if (error.request) {
      // Request was made but no response received
      error.message = 'No response from server. Please check if backend is running.';
    }

    return Promise.reject(error);
  }
);

// Resume services
export const uploadResume = (formData) =>
  API.post('/resume/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });

export const uploadResumeAndRecommend = (formData, jobSources = "all", limit = 20) =>
  API.post('/resume/upload-and-recommend', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    params: { job_sources: jobSources, limit }
  });

// New Resume Parser API
export const uploadResumeNew = (formData) =>
  API.post('/resume/upload-resume', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });

// Enhanced V2 API - uses database matching
export const uploadResumeAndMatch = (formData, limit = 50, minMatchScore = 30) =>
  API.post('/v2/resume/upload-and-match', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    params: { limit, min_match_score: minMatchScore }
  });

export const getResumeMatches = (resumeId, limit = 50, minMatchScore = 30) =>
  API.get(`/v2/resume/matches/${resumeId}`, {
    params: { limit, min_match_score: minMatchScore }
  });

export const getDatabaseStats = () => API.get('/v2/resume/stats');

// Scraper control
export const triggerScraping = (keywords, location = "India", limitPerSource = 50) =>
  API.post('/scraper/scrape-now', null, {
    params: { keywords, location, limit_per_source: limitPerSource }
  });

export const getScraperStatus = () => API.get('/scraper/scraper-status');

// Job services
export const searchJobs = ({ keywords, location, company, country, limit = 20 } = {}) =>
  API.get('/jobs/search', {
    params: { keywords, location, company, country, limit }
  });

export const matchJobsWithResume = (resumeId, { country, limit = 20 } = {}) =>
  API.get(`/jobs/match/${resumeId}`, {
    params: { country, limit }
  });

export const getJobById = (jobId) => API.get(`/jobs/${jobId}`);

// Get all jobs with optional filtering
export const getJobs = ({ skills, limit = 100 } = {}) =>
  API.get('/jobs/search', {
    params: { keywords: skills, limit }
  });


// Auth services
export const register = (userData) => API.post('/auth/register', userData);

export const login = (credentials) => API.post('/auth/login', credentials);

export default API;