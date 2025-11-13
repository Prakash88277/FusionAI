// src/pages/Dashboard.js
import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { FaSearch, FaSync } from "react-icons/fa";
import JobCard from "../components/JobCard";
import { getResumeMatches, getDatabaseStats } from "../services/api";

const Dashboard = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [stats, setStats] = useState(null);

  useEffect(() => {
    loadJobs();
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const response = await getDatabaseStats();
      setStats(response.data);
    } catch (err) {
      console.error("Error loading stats:", err);
    }
  };

  const loadJobs = async () => {
    setLoading(true);
    setError("");

    try {
      // First try to load from localStorage (from recent upload)
      const storedJobs = localStorage.getItem("jobRecommendations");
      const resumeId = localStorage.getItem("resumeId");

      if (storedJobs) {
        const parsedJobs = JSON.parse(storedJobs);
        console.log("Loaded jobs from localStorage:", parsedJobs);
        
        // Format jobs from localStorage
        const formattedJobs = parsedJobs.map((item, index) => ({
          id: item.job?.id || index,
          title: item.job?.title || "Job Title",
          company: item.job?.company || "Company",
          location: item.job?.location || "Location",
          description: item.job?.description || "",
          skills: item.job?.skills || [],
          matchScore: item.match_score || 0,
          matching_skills: item.matching_skills || [],
          missing_skills: item.missing_skills || [],
          apply_link: item.job?.apply_link || "#",
          job_type: item.job?.job_type,
          experience_level: item.job?.experience_level,
          salary_text: item.job?.salary_text,
          posted_date: item.job?.posted_date,
        }));
        
        setJobs(formattedJobs);
        setLoading(false);
        return;
      }

      // If no localStorage data, try to fetch from API using resumeId
      if (resumeId) {
        console.log("Fetching jobs from API for resume:", resumeId);
        const response = await getResumeMatches(resumeId, 50, 30);
        
        if (response.data.job_matches && response.data.job_matches.length > 0) {
          const formattedJobs = response.data.job_matches.map((item, index) => ({
            id: item.job?.id || index,
            title: item.job?.title || "Job Title",
            company: item.job?.company || "Company",
            location: item.job?.location || "Location",
            description: item.job?.description || "",
            skills: item.job?.skills || [],
            matchScore: item.match_score || 0,
            matching_skills: item.matching_skills || [],
            missing_skills: item.missing_skills || [],
            apply_link: item.job?.apply_link || "#",
            job_type: item.job?.job_type,
            experience_level: item.job?.experience_level,
            salary_text: item.job?.salary_text,
            posted_date: item.job?.posted_date,
          }));
          
          setJobs(formattedJobs);
          setLoading(false);
          return;
        }
      }

      // If no data found, show message
      setError("No jobs found. Please upload your resume or trigger job scraping.");
      setLoading(false);

    } catch (err) {
      console.error("Error loading jobs:", err);
      setError("Failed to load jobs. Make sure the backend is running and database has jobs.");
      setLoading(false);
    }
  };

  const filteredJobs = jobs.filter((job) =>
    job.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <motion.div
      className="min-h-screen bg-gradient-to-b from-blue-50 to-white pt-24 px-6"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.6 }}
    >
      {/* Header */}
      <div className="max-w-7xl mx-auto mb-10 text-center">
        <motion.h1
          className="text-4xl font-extrabold gradient-text"
          initial={{ y: -10, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
        >
          Smart Job Dashboard
        </motion.h1>
        <p className="text-gray-600 mt-2">
          Explore AI-matched opportunities based on your uploaded resume
        </p>

        {/* Stats */}
        {stats && (
          <div className="mt-4 flex items-center justify-center gap-4 text-sm flex-wrap">
            <span className="px-4 py-2 bg-blue-100 text-blue-800 rounded-full font-medium">
              📊 {stats.total_jobs} Total Jobs in Database
            </span>
            {stats.active_jobs > 0 && (
              <span className="px-4 py-2 bg-green-100 text-green-800 rounded-full font-medium">
                ✅ {stats.active_jobs} Active Jobs
              </span>
            )}
            {jobs.length > 0 && (
              <span className="px-4 py-2 bg-purple-100 text-purple-800 rounded-full font-medium">
                🎯 {jobs.length} Matches Found
              </span>
            )}
          </div>
        )}

        {/* Error Display */}
        {error && (
          <motion.div
            className="mt-4 max-w-2xl mx-auto bg-yellow-50 border border-yellow-200 rounded-xl p-4"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <p className="text-yellow-800 font-medium">{error}</p>
            <button
              onClick={loadJobs}
              className="mt-2 text-sm text-yellow-600 hover:text-yellow-800 underline font-medium"
            >
              Try Again
            </button>
          </motion.div>
        )}

        {/* Search bar and Refresh */}
        <div className="mt-6 flex justify-center gap-3 items-center">
          <div className="search-bar w-full max-w-lg flex items-center gap-3 px-4 py-3 bg-white shadow-md rounded-xl border border-gray-200 focus-within:ring-2 focus-within:ring-blue-400">
            <FaSearch className="text-gray-400" />
            <input
              type="text"
              placeholder="Search job titles..."
              className="w-full bg-transparent outline-none text-gray-700"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          <button
            onClick={() => { loadJobs(); loadStats(); }}
            className="px-4 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors flex items-center gap-2"
            title="Refresh jobs"
          >
            <FaSync className="text-sm" />
          </button>
        </div>
      </div>

      {/* Job Grid */}
      <div className="max-w-7xl mx-auto grid gap-6 md:grid-cols-2 lg:grid-cols-3 auto-rows-fr">
        {loading
          ? [...Array(6)].map((_, i) => (
              <motion.div
                key={i}
                className="h-48 bg-white rounded-2xl shadow-md skeleton"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: i * 0.1 }}
              ></motion.div>
            ))
          : filteredJobs.map((job, i) => (
              <motion.div
                key={job.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
              >
                <JobCard job={job} />
              </motion.div>
            ))}
      </div>

      {/* No Results */}
      {!loading && filteredJobs.length === 0 && (
        <motion.div
          className="text-center text-gray-500 mt-10"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <p>No matching jobs found 😔</p>
        </motion.div>
      )}
    </motion.div>
  );
};

export default Dashboard;
