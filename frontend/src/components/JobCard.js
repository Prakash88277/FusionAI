import React, { useState } from 'react';
import { motion } from 'framer-motion';

const JobCard = ({ job, index }) => {
  const [showDescription, setShowDescription] = useState(false);

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
      transition={{ duration: 0.3, delay: index * 0.05 }}
      className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 p-6 border border-gray-100 hover:border-blue-200 transform hover:-translate-y-1 h-full flex flex-col"
    >
      {/* Header */}
      <div className="flex justify-between items-start mb-4">
        <div className="flex-1 pr-4">
          <h3 className="text-lg font-bold text-gray-900 mb-1.5 hover:text-blue-600 transition-colors line-clamp-2">
            {job.title}
          </h3>
          <p className="text-base text-gray-700 font-medium mb-1">{job.company}</p>
          <div className="flex items-center text-sm text-gray-500">
            <svg className="w-3.5 h-3.5 mr-1.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
            </svg>
            <span className="truncate">{job.location}</span>
          </div>
        </div>
        <div className={`px-3 py-1.5 rounded-lg text-xs font-bold shadow-md ${getMatchColor(job.match_score || 0)} flex items-center gap-1 flex-shrink-0`}>
          <svg className="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
          </svg>
          <span>{job.matchScore || job.match_score || 85}%</span>
        </div>
      </div>

      {/* Job Details */}
      <div className="flex-1 mb-4">
        {job.description && (
          <div className="mb-4">
            <p className="text-gray-600 text-sm leading-relaxed line-clamp-3">
              {job.description}
            </p>
          </div>
        )}

        {/* Skills */}
        {job.skills && job.skills.length > 0 && (
          <div className="mb-4">
            <div className="flex flex-wrap gap-1.5">
              {job.skills.slice(0, 5).map((skill, idx) => (
                <span
                  key={idx}
                  className="px-2.5 py-1 bg-blue-50 text-blue-700 text-xs rounded-lg font-medium border border-blue-100"
                >
                  {skill}
                </span>
              ))}
              {job.skills.length > 5 && (
                <span className="px-2.5 py-1 bg-gray-100 text-gray-600 text-xs rounded-lg font-medium">
                  +{job.skills.length - 5}
                </span>
              )}
            </div>
          </div>
        )}
      </div>

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
        <div className="mb-4 pb-4 border-b border-gray-100">
          <p className="text-xs font-semibold text-green-600 mb-2">
            ✓ {job.matching_skills.length} Matching Skills
          </p>
          <div className="flex flex-wrap gap-1.5">
            {job.matching_skills.slice(0, 4).map((skill, idx) => (
              <span
                key={idx}
                className="px-2 py-0.5 bg-green-50 text-green-700 text-xs rounded font-medium"
              >
                {skill}
              </span>
            ))}
            {job.matching_skills.length > 4 && (
              <span className="px-2 py-0.5 bg-green-50 text-green-700 text-xs rounded font-medium">
                +{job.matching_skills.length - 4}
              </span>
            )}
          </div>
        </div>
      )}

      {/* Footer */}
      <div className="flex justify-between items-center pt-4">
        <div className="flex items-center text-xs text-gray-500">
          <svg className="w-3.5 h-3.5 mr-1.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
          </svg>
          <span className="truncate">{job.posted_date ? new Date(job.posted_date).toLocaleDateString() : 'Recently'}</span>
        </div>
        <a
          href={job.apply_link || job.applyLink || job.apply_url || '#'}
          target={job.apply_link || job.applyLink || job.apply_url ? "_blank" : "_self"}
          rel="noopener noreferrer"
          onClick={(e) => {
            const applyLink = job.apply_link || job.applyLink || job.apply_url;
            if (!applyLink || applyLink === '#') {
              e.preventDefault();
              alert('Apply link not available for this job');
            }
          }}
          className="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white px-5 py-2 rounded-lg font-semibold text-sm transition-all duration-200 flex items-center gap-2 shadow-md hover:shadow-lg flex-shrink-0"
        >
          <span>Apply</span>
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
          </svg>
        </a>
      </div>
    </motion.div>
  );
};

export default JobCard;
