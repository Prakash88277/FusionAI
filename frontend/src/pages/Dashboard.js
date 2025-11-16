// src/pages/Dashboard.js
import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { FaSearch, FaSync } from "react-icons/fa";
import JobCard from "../components/JobCard";
import { scrapeJobs, searchJobsBySkills, getJobStats } from "../services/zenrowsService";

const Dashboard = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [stats, setStats] = useState(null);

  useEffect(() => {
    loadJobs();
  }, []);

  const loadJobs = async () => {
    setLoading(true);
    setError("");

    try {
      console.log('🚀 Loading live jobs from ZenRows...');
      
      // Check if user has uploaded a resume with skills
      const storedSkills = localStorage.getItem("userSkills");
      let jobs = [];
      
      if (storedSkills) {
        const skills = JSON.parse(storedSkills);
        console.log('👤 User skills found:', skills);
        jobs = await searchJobsBySkills(skills);
      } else {
        console.log('🔍 No user skills found, loading general tech jobs...');
        jobs = await scrapeJobs(['software', 'developer', 'engineer', 'python', 'javascript']);
      }
      
      console.log('✅ Jobs loaded:', jobs.length);
      setJobs(jobs);
      
      // Calculate and set stats
      const jobStats = getJobStats(jobs);
      setStats({
        total_jobs: jobStats.total_jobs,
        active_jobs: jobStats.active_jobs,
        matches_found: jobs.length,
        sources: Object.keys(jobStats.sources).length
      });
      
      setLoading(false);

    } catch (err) {
      console.error("❌ Error loading jobs:", err);
      setError(`Failed to load jobs: ${err.message}`);
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
              📊 {stats.total_jobs} Live Jobs from ZenRows
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
            onClick={loadJobs}
            className="px-4 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors flex items-center gap-2"
            title="Refresh jobs"
            disabled={loading}
          >
            <FaSync className={`text-sm ${loading ? 'animate-spin' : ''}`} />
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
