// src/pages/Dashboard.js
import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { FaSearch, FaSync } from "react-icons/fa";
import JobCard from "../components/JobCard";
import { getJobs } from "../services/api";

const Dashboard = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [showingFallback, setShowingFallback] = useState(false);

  useEffect(() => {
    loadJobs();
  }, []);

  const loadJobs = async () => {
    setLoading(true);
    setError("");

    try {
      console.log('🚀 Loading jobs...');

      // Check if we have fresh matches from a recent upload
      const newResumeUploaded = localStorage.getItem("newResumeUploaded");
      const storedMatches = localStorage.getItem("jobMatches");

      if (newResumeUploaded === "true" && storedMatches) {
        console.log('✨ Found fresh matches from recent upload!');
        try {
          const matches = JSON.parse(storedMatches);




          // Transform matches to flat job objects for display
          const formattedJobs = matches.map(match => {
            // Handle both { job: {...} } and direct job object formats
            const jobData = match.job || match;

            return {
              ...jobData,
              // Map _id from n8n to id for React keys
              id: jobData._id || jobData.id,
              // Add match details at top level for the card component
              // Use safe defaults
              match_score: match.match_score || jobData.match_score || 0,
              matching_skills: match.matching_skills || jobData.matching_skills || [],
              missing_skills: match.missing_skills || jobData.missing_skills || [],
              // Ensure apply_link is accessible
              apply_link: jobData.apply_link || jobData.applyLink || jobData.apply_url || '#'
            };
          });

          setJobs(formattedJobs);
          setLoading(false);
          return;

        } catch (e) {
          console.error("Error parsing stored matches:", e);
          // Fall through to other loading methods if parsing fails
        }
      }

      console.log('🔄 No recent upload, fetching available jobs...');

      // If no recent resume upload, fetch latest jobs from DB to show *something* 
      // instead of empty screen, but clearly generic.
      const jobsResponse = await getJobs({ limit: 50 });
      const allJobs = jobsResponse.data || jobsResponse || [];

      console.log(`✅ Loaded ${allJobs.length} jobs from database`);
      setJobs(allJobs);
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

        {/* Fallback Jobs Message */}
        {showingFallback && jobs.length > 0 && (
          <motion.div
            className="mt-4 max-w-2xl mx-auto bg-blue-50 border border-blue-200 rounded-xl p-4"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <p className="text-blue-800 font-medium">
              🎯 No exact skill matches found. Showing {jobs.length} related tech jobs based on your resume keywords.
            </p>
            <p className="text-blue-600 text-sm mt-1">
              Try uploading a different resume or browse all available positions below.
            </p>
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
              key={job.id || i}
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
