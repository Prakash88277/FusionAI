import React from 'react';
import { motion } from 'framer-motion';

const JobCard = ({ job, index }) => {
  const getMatchColor = (score) => {
    if (score >= 80) return 'text-green-600 bg-green-50';
    if (score >= 60) return 'text-blue-600 bg-blue-50';
    if (score >= 40) return 'text-yellow-600 bg-yellow-50';
    return 'text-red-600 bg-red-50';
  };

  const getExperienceColor = (level) => {
    switch (level?.toLowerCase()) {
      case 'entry': return 'bg-blue-100 text-blue-800';
      case 'mid': return 'bg-green-100 text-green-800';
      case 'senior': return 'bg-purple-100 text-purple-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getJobTypeColor = (type) => {
    switch (type?.toLowerCase()) {
      case 'full_time': return 'bg-green-100 text-green-800';
      case 'internship': return 'bg-blue-100 text-blue-800';
      case 'part_time': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: index * 0.1 }}
      className="bg-white rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 p-6 border border-gray-100 hover:border-blue-200"
    >
      {/* Header */}
      <div className="flex justify-between items-start mb-4">
        <div className="flex-1">
          <h3 className="text-xl font-bold text-gray-900 mb-1 hover:text-blue-700 transition-colors">
            {job.title}
          </h3>
          <p className="text-lg text-gray-700 font-medium">{job.company}</p>
          <p className="text-sm text-gray-500 flex items-center mt-1">
            <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
            </svg>
            {job.location}
          </p>
        </div>
        <div className={`px-3 py-1 rounded-full text-sm font-bold ${getMatchColor(job.match_score || 0)}`}>
          {job.match_score || 85}% Match
        </div>
      </div>

      {/* Job Details */}
      <div className="mb-4">
        <p className="text-gray-600 text-sm leading-relaxed line-clamp-3">
          {job.description}
        </p>
      </div>

      {/* Skills */}
      {job.skills && job.skills.length > 0 && (
        <div className="mb-4">
          <h4 className="text-sm font-semibold text-gray-700 mb-2">Required Skills:</h4>
          <div className="flex flex-wrap gap-2">
            {job.skills.slice(0, 6).map((skill, idx) => (
              <span
                key={idx}
                className="px-2 py-1 bg-blue-50 text-blue-700 text-xs rounded-md font-medium"
              >
                {skill}
              </span>
            ))}
            {job.skills.length > 6 && (
              <span className="px-2 py-1 bg-gray-50 text-gray-600 text-xs rounded-md">
                +{job.skills.length - 6} more
              </span>
            )}
          </div>
        </div>
      )}

      {/* Job Info */}
      <div className="flex flex-wrap gap-2 mb-4">
        {job.job_type && (
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getJobTypeColor(job.job_type)}`}>
            {job.job_type.replace('_', ' ')}
          </span>
        )}
        {job.experience_level && (
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getExperienceColor(job.experience_level)}`}>
            {job.experience_level}
          </span>
        )}
        {job.salary_text && (
          <span className="px-2 py-1 bg-green-50 text-green-700 rounded-full text-xs font-medium">
            {job.salary_text}
          </span>
        )}
      </div>

      {/* Matching Skills */}
      {job.matching_skills && job.matching_skills.length > 0 && (
        <div className="mb-4">
          <h4 className="text-sm font-semibold text-green-700 mb-2">
            Matching Skills ({job.matching_skills.length}):
          </h4>
          <div className="flex flex-wrap gap-1">
            {job.matching_skills.map((skill, idx) => (
              <span
                key={idx}
                className="px-2 py-1 bg-green-50 text-green-700 text-xs rounded-md font-medium border border-green-200"
              >
                ✓ {skill}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Footer */}
      <div className="flex justify-between items-center pt-4 border-t border-gray-100">
        <div className="flex items-center text-sm text-gray-500">
          <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
          </svg>
          Posted {job.posted_date ? new Date(job.posted_date).toLocaleDateString() : 'Recently'}
        </div>
        <a
          href={job.apply_link}
          target="_blank"
          rel="noopener noreferrer"
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium transition-colors duration-200 flex items-center"
        >
          Apply Now
          <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
          </svg>
        </a>
      </div>
    </motion.div>
  );
};

export default JobCard;
