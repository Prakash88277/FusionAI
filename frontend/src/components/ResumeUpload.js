// src/components/ResumeUpload.js
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { AiOutlineUpload } from "react-icons/ai";
import { uploadResumeAndMatch } from "../services/api";
// Mock service no longer needed - using real API

const ResumeUpload = ({ onUpload }) => {
  const [fileName, setFileName] = useState("");
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setFileName(file.name);
    setError("");
    setUploading(true);

    try {
      // Clear previous data to ensure fresh state
      localStorage.removeItem("jobMatches");
      localStorage.removeItem("newResumeUploaded");

      console.log('📄 Uploading resume to new parser...');
      const formData = new FormData();
      formData.append("file", file);

      // Use enhanced resume matcher API
      const response = await uploadResumeAndMatch(formData);

      console.log('✅ Resume parsed and matched successfully');

      console.log('✅ Resume parsed and matched successfully');
      console.log('🔍 Raw Server Response:', JSON.stringify(response.data, null, 2));

      // Robust extraction of matches from potential structures
      let matches = [];
      const data = response.data;

      if (Array.isArray(data)) {
        matches = data;
      } else if (typeof data === 'object' && data !== null) {
        // Check common wrapper keys
        if (Array.isArray(data.job_matches)) matches = data.job_matches;
        else if (Array.isArray(data.jobs)) matches = data.jobs;
        else if (Array.isArray(data.matches)) matches = data.matches;
        else if (Array.isArray(data.data)) matches = data.data;
        // Check if it's a single job object (has title/company)
        else if (data.title && data.company) {
          console.log('💡 Response appears to be a single job object, wrapping in array');
          matches = [data];
        }
        // Last resort: Check if object values form the list (e.g. {"0": job1, "1": job2} or map)
        else {
          const allValues = Object.values(data);
          // 1. Look for nested array
          const arrayValue = allValues.find(val => Array.isArray(val) && val.length > 0);

          if (arrayValue) {
            console.log('💡 Found an array in response object values, using it');
            matches = arrayValue;
          }
          // 2. Check if the values themselves are the jobs (map structure)
          else if (allValues.length > 0 && allValues.every(val =>
            val && typeof val === 'object' && (val.title || val.company || val.match_score)
          )) {
            console.log('💡 Response appears to be a map of job objects, converting to array');
            matches = allValues;
          }
        }
      }

      if (matches.length === 0) {
        console.warn('⚠️ Could not extract job array from response. Response structure:', data);
      }

      console.log('📦 Storing', matches.length, 'matches');
      localStorage.setItem("jobMatches", JSON.stringify(matches));
      localStorage.setItem("newResumeUploaded", "true");
      localStorage.setItem("resumeUploaded", "true");

      // Mark upload as successful
      if (onUpload) onUpload(file);

      console.log('🔄 Redirecting to dashboard...');
      navigate("/dashboard");

    } catch (err) {
      console.error("Upload error:", err);
      setUploading(false);

      let errorMessage = "Failed to upload resume. ";
      if (err.code === "ERR_NETWORK") {
        errorMessage += "Please make sure the backend server is running.";
      } else if (err.response?.data?.detail) {
        errorMessage += err.response.data.detail;
      } else {
        errorMessage += "Please try again.";
      }
      setError(errorMessage);
    }
  };

  return (
    <motion.div
      className="flex flex-col items-center justify-center py-20 px-4 bg-gradient-to-b from-white via-blue-50 to-blue-100 min-h-[70vh]"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.8 }}
    >
      <motion.div
        whileHover={{ scale: 1.03 }}
        transition={{ type: "spring", stiffness: 200 }}
        className="resume-upload border-2 border-dashed border-blue-400 rounded-2xl p-10 text-center shadow-xl bg-white/70 backdrop-blur-lg max-w-lg w-full"
      >
        <motion.div
          animate={{ y: [0, -8, 0] }}
          transition={{ repeat: Infinity, duration: 2.5 }}
          className="flex flex-col items-center gap-3"
        >
          <AiOutlineUpload className="text-5xl text-blue-600" />
          <h2 className="text-2xl font-semibold text-gray-800">
            Upload Your Resume
          </h2>
          <p className="text-gray-500 text-sm">
            Upload your resume to find AI-matched job recommendations
          </p>
        </motion.div>

        <div className="mt-6">
          <input
            ref={(input) => (window.fileInputRef = input)}
            type="file"
            accept=".pdf,.docx"
            onChange={handleFileChange}
            className="hidden"
            id="resume-file-input"
          />
          <motion.button
            onClick={() => !uploading && document.getElementById('resume-file-input').click()}
            whileHover={!uploading ? { scale: 1.05 } : {}}
            whileTap={!uploading ? { scale: 0.95 } : {}}
            className={`px-8 py-3 rounded-xl font-semibold text-white shadow-lg transition-all duration-300 ${uploading
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 cursor-pointer"
              }`}
            disabled={uploading}
            type="button"
          >
            {uploading ? (
              <div className="flex items-center gap-2">
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                <span>Analyzing Resume & Matching Jobs... (this may take a minute)</span>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <AiOutlineUpload className="text-xl" />
                <span>Choose File</span>
              </div>
            )}
          </motion.button>

          {fileName && !uploading && !error && (
            <motion.p
              className="mt-4 text-sm text-gray-700 font-medium flex items-center justify-center gap-2"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              <svg className="w-4 h-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              {fileName}
            </motion.p>
          )}

          {error && (
            <motion.div
              className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm"
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <div className="flex items-start gap-2">
                <svg className="w-5 h-5 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
                <span>{error}</span>
              </div>
            </motion.div>
          )}
        </div>
      </motion.div>
    </motion.div>
  );
};

export default ResumeUpload;
