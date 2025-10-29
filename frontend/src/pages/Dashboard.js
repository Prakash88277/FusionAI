// src/pages/Dashboard.js
import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { FaSearch } from "react-icons/fa";
import JobCard from "../components/JobCard";

const Dashboard = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    setLoading(true);
    setTimeout(() => {
      setJobs([
  {
    id: 1,
    title: "Software Engineer",
    company: "Google",
    location: "Bangalore, India",
    matchScore: 92,
    skills: ["Python", "React", "Machine Learning"],
    apply_link:
      "https://www.google.com/about/careers/applications/jobs/results/74939955737961158-software-engineer-iii-google-cloud",
  },
  {
    id: 2,
    title: "Data Analyst",
    company: "Amazon",
    location: "Hyderabad, India",
    matchScore: 88,
    skills: ["SQL", "Excel", "Tableau"],
    apply_link: "https://www.amazon.jobs/en-gb/jobs/3088358/data-analyst-vendor-flex",
  },
  {
    id: 3,
    title: "AI Research Intern",
    company: "Microsoft",
    location: "Noida, India",
    matchScore: 85,
    skills: ["Deep Learning", "TensorFlow", "Python"],
    apply_link: "https://careers.microsoft.com/students/us/en/job/AIResearchIntern",
  },
  {
    id: 4,
    title: "Frontend Developer",
    company: "Meta (Facebook)",
    location: "Remote",
    matchScore: 83,
    skills: ["React", "JavaScript", "HTML", "CSS"],
    apply_link: "https://www.metacareers.com/jobs/frontend-developer",
  },
  {
    id: 5,
    title: "Backend Engineer",
    company: "Netflix",
    location: "Mumbai, India",
    matchScore: 80,
    skills: ["Node.js", "Express", "MongoDB"],
    apply_link: "https://jobs.netflix.com/backend-engineer",
  },
  {
    id: 6,
    title: "Machine Learning Engineer",
    company: "NVIDIA",
    location: "Pune, India",
    matchScore: 90,
    skills: ["Python", "PyTorch", "CUDA"],
    apply_link: "https://nvidia.wd5.myworkdayjobs.com/en-US/MachineLearningEngineer",
  },
  {
    id: 7,
    title: "Data Scientist",
    company: "IBM",
    location: "Bangalore, India",
    matchScore: 86,
    skills: ["Pandas", "NumPy", "Scikit-learn"],
    apply_link: "https://www.ibm.com/careers/data-scientist",
  },
  {
    id: 8,
    title: "Cloud Solutions Architect",
    company: "Google Cloud",
    location: "Hyderabad, India",
    matchScore: 89,
    skills: ["Google Cloud", "Kubernetes", "DevOps"],
    apply_link: "https://cloud.google.com/careers/solutions-architect",
  },
  {
    id: 9,
    title: "Full Stack Developer",
    company: "Adobe",
    location: "Gurgaon, India",
    matchScore: 84,
    skills: ["JavaScript", "React", "Flask", "REST APIs"],
    apply_link: "https://adobe.wd5.myworkdayjobs.com/en-US/fullstack-developer",
  },
  {
    id: 10,
    title: "DevOps Engineer",
    company: "Atlassian",
    location: "Remote",
    matchScore: 87,
    skills: ["AWS", "CI/CD", "Docker", "Kubernetes"],
    apply_link: "https://www.atlassian.com/company/careers/devops-engineer",
  },
]);

      setLoading(false);
    }, 1200);
  }, []);

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

        {/* Search bar */}
        <div className="mt-6 flex justify-center">
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
        </div>
      </div>

      {/* Job Grid */}
      <div className="max-w-7xl mx-auto grid gap-6 md:grid-cols-2 lg:grid-cols-3">
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
