// src/pages/ScraperControl.js
import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { triggerScraping, getScraperStatus, getDatabaseStats } from "../services/api";

const ScraperControl = () => {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [status, setStatus] = useState(null);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    loadStatus();
    loadStats();
  }, []);

  const loadStatus = async () => {
    try {
      const response = await getScraperStatus();
      setStatus(response.data);
    } catch (err) {
      console.error("Error loading scraper status:", err);
    }
  };

  const loadStats = async () => {
    try {
      const response = await getDatabaseStats();
      setStats(response.data);
    } catch (err) {
      console.error("Error loading stats:", err);
    }
  };

  const handleScrape = async () => {
    setLoading(true);
    setMessage("");

    try {
      const keywords = ["software", "developer", "engineer", "python", "java", "data"];
      await triggerScraping(keywords, "India", 50);
      
      setMessage("✅ Scraping started! Jobs will be added to database in 30-60 seconds. Check back soon!");
      
      // Refresh stats after a delay
      setTimeout(() => {
        loadStats();
      }, 5000);

    } catch (err) {
      setMessage("❌ Error: " + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white pt-24 px-6">
      <div className="max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-2xl shadow-lg p-8"
        >
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            🔧 Scraper Control Panel
          </h1>
          <p className="text-gray-600 mb-8">
            Manually trigger job scraping to populate the database
          </p>

          {/* Database Stats */}
          {stats && (
            <div className="mb-8 p-6 bg-blue-50 rounded-xl">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">
                📊 Database Statistics
              </h2>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                <div className="bg-white p-4 rounded-lg">
                  <p className="text-sm text-gray-600">Total Jobs</p>
                  <p className="text-2xl font-bold text-blue-600">{stats.total_jobs}</p>
                </div>
                <div className="bg-white p-4 rounded-lg">
                  <p className="text-sm text-gray-600">Active Jobs</p>
                  <p className="text-2xl font-bold text-green-600">{stats.active_jobs}</p>
                </div>
                <div className="bg-white p-4 rounded-lg">
                  <p className="text-sm text-gray-600">Resumes</p>
                  <p className="text-2xl font-bold text-purple-600">{stats.total_resumes}</p>
                </div>
              </div>

              {stats.jobs_by_source && Object.keys(stats.jobs_by_source).length > 0 && (
                <div className="mt-4">
                  <p className="text-sm font-medium text-gray-700 mb-2">Jobs by Source:</p>
                  <div className="flex gap-2 flex-wrap">
                    {Object.entries(stats.jobs_by_source).map(([source, count]) => (
                      <span
                        key={source}
                        className="px-3 py-1 bg-white rounded-full text-sm font-medium text-gray-700"
                      >
                        {source}: {count}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Scraper Status */}
          {status && (
            <div className="mb-8 p-6 bg-green-50 rounded-xl">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">
                🤖 Scraper Status
              </h2>
              <div className="space-y-2">
                <p className="text-gray-700">
                  <span className="font-medium">Available Scrapers:</span>{" "}
                  {status.total_scrapers}
                </p>
                <p className="text-gray-700">
                  <span className="font-medium">Sources:</span>{" "}
                  {status.available_sources.join(", ")}
                </p>
                <p className="text-gray-700">
                  <span className="font-medium">Status:</span>{" "}
                  <span className="text-green-600 font-semibold">{status.status}</span>
                </p>
              </div>
            </div>
          )}

          {/* Scrape Button */}
          <div className="mb-6">
            <button
              onClick={handleScrape}
              disabled={loading}
              className={`w-full py-4 px-6 rounded-xl font-semibold text-white text-lg transition-all ${
                loading
                  ? "bg-gray-400 cursor-not-allowed"
                  : "bg-blue-600 hover:bg-blue-700 hover:shadow-lg"
              }`}
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                      fill="none"
                    />
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    />
                  </svg>
                  Scraping in progress...
                </span>
              ) : (
                "🚀 Start Scraping Jobs Now"
              )}
            </button>
          </div>

          {/* Message */}
          {message && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className={`p-4 rounded-xl ${
                message.includes("✅")
                  ? "bg-green-50 text-green-800 border border-green-200"
                  : "bg-red-50 text-red-800 border border-red-200"
              }`}
            >
              <p className="font-medium">{message}</p>
            </motion.div>
          )}

          {/* Info */}
          <div className="mt-8 p-6 bg-gray-50 rounded-xl">
            <h3 className="font-semibold text-gray-800 mb-3">ℹ️ How it works:</h3>
            <ul className="space-y-2 text-sm text-gray-700">
              <li>• Scrapes jobs from Internshala and Naukri</li>
              <li>• Searches for: software, developer, engineer, python, java, data</li>
              <li>• Fetches up to 50 jobs per source</li>
              <li>• Takes 30-60 seconds to complete</li>
              <li>• Jobs are stored in local SQLite database</li>
              <li>• Automatic scraping runs daily at 2:00 AM</li>
            </ul>
          </div>

          {/* Refresh Button */}
          <div className="mt-6 flex justify-center">
            <button
              onClick={() => { loadStats(); loadStatus(); }}
              className="px-6 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg font-medium transition-colors"
            >
              🔄 Refresh Stats
            </button>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default ScraperControl;
