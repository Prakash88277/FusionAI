// Mock job service that generates relevant jobs based on extracted keywords
import { getJobStats } from './zenrowsService';

// Mock job templates organized by skill categories
const JOB_TEMPLATES = {
  // Programming Languages
  python: [
    {
      title: "Python Developer",
      company: "TechCorp Solutions",
      location: "Bangalore, India",
      description: "We are looking for a skilled Python developer to join our backend team. Work with Django, Flask, and modern Python frameworks.",
      salary_text: "₹6-12 LPA",
      job_type: "Full-time",
      experience_required: "2-4 years"
    },
    {
      title: "Senior Python Engineer",
      company: "DataFlow Technologies",
      location: "Mumbai, India", 
      description: "Lead Python development for data processing pipelines. Experience with pandas, numpy, and machine learning libraries required.",
      salary_text: "₹10-18 LPA",
      job_type: "Full-time",
      experience_required: "4-6 years"
    }
  ],
  
  javascript: [
    {
      title: "JavaScript Developer",
      company: "WebTech Innovations",
      location: "Hyderabad, India",
      description: "Frontend and backend JavaScript development using Node.js, React, and modern ES6+ features.",
      salary_text: "₹5-10 LPA", 
      job_type: "Full-time",
      experience_required: "2-3 years"
    },
    {
      title: "Full Stack JavaScript Engineer",
      company: "Digital Solutions Inc",
      location: "Pune, India",
      description: "Build end-to-end applications using JavaScript, Node.js, React, and MongoDB. Remote-friendly position.",
      salary_text: "₹8-15 LPA",
      job_type: "Full-time",
      experience_required: "3-5 years"
    }
  ],

  react: [
    {
      title: "React Developer",
      company: "Frontend Masters",
      location: "Delhi, India",
      description: "Create responsive web applications using React, Redux, and modern frontend tools. Join our innovative team.",
      salary_text: "₹6-11 LPA",
      job_type: "Full-time", 
      experience_required: "2-4 years"
    },
    {
      title: "Senior React Engineer",
      company: "UI/UX Solutions",
      location: "Chennai, India",
      description: "Lead React development projects, mentor junior developers, and architect scalable frontend solutions.",
      salary_text: "₹12-20 LPA",
      job_type: "Full-time",
      experience_required: "5+ years"
    }
  ],

  nodejs: [
    {
      title: "Node.js Backend Developer", 
      company: "ServerSide Technologies",
      location: "Bangalore, India",
      description: "Build scalable backend APIs using Node.js, Express, and MongoDB. Experience with microservices preferred.",
      salary_text: "₹7-13 LPA",
      job_type: "Full-time",
      experience_required: "2-4 years"
    }
  ],

  // Cloud Platforms
  aws: [
    {
      title: "AWS Cloud Engineer",
      company: "CloudFirst Solutions",
      location: "Mumbai, India", 
      description: "Design and implement AWS cloud infrastructure. EC2, S3, Lambda, and DevOps experience required.",
      salary_text: "₹8-16 LPA",
      job_type: "Full-time",
      experience_required: "3-5 years"
    },
    {
      title: "AWS Solutions Architect",
      company: "Enterprise Cloud Services",
      location: "Bangalore, India",
      description: "Architect cloud solutions for enterprise clients. AWS certification and migration experience preferred.",
      salary_text: "₹15-25 LPA", 
      job_type: "Full-time",
      experience_required: "5+ years"
    }
  ],

  azure: [
    {
      title: "Azure DevOps Engineer",
      company: "Microsoft Partner Solutions",
      location: "Hyderabad, India",
      description: "Implement CI/CD pipelines using Azure DevOps. Experience with Azure services and containerization.",
      salary_text: "₹9-17 LPA",
      job_type: "Full-time", 
      experience_required: "3-5 years"
    }
  ],

  // Databases
  mongodb: [
    {
      title: "MongoDB Database Developer",
      company: "NoSQL Experts",
      location: "Pune, India",
      description: "Design and optimize MongoDB databases. Experience with aggregation pipelines and performance tuning.",
      salary_text: "₹6-12 LPA",
      job_type: "Full-time",
      experience_required: "2-4 years"
    }
  ],

  mysql: [
    {
      title: "Database Administrator",
      company: "DataSafe Solutions", 
      location: "Chennai, India",
      description: "Manage MySQL databases, optimize queries, and ensure data security. Backup and recovery experience required.",
      salary_text: "₹5-10 LPA",
      job_type: "Full-time",
      experience_required: "2-5 years"
    }
  ],

  // DevOps Tools
  docker: [
    {
      title: "DevOps Engineer - Containerization",
      company: "ContainerTech Solutions",
      location: "Bangalore, India",
      description: "Implement Docker containerization and Kubernetes orchestration. CI/CD pipeline experience preferred.",
      salary_text: "₹8-15 LPA",
      job_type: "Full-time",
      experience_required: "3-5 years"
    }
  ],

  kubernetes: [
    {
      title: "Kubernetes Platform Engineer", 
      company: "CloudNative Systems",
      location: "Mumbai, India",
      description: "Manage Kubernetes clusters and container orchestration. Experience with Helm charts and monitoring tools.",
      salary_text: "₹10-18 LPA",
      job_type: "Full-time",
      experience_required: "4-6 years"
    }
  ],

  // Data Science & ML
  "machine learning": [
    {
      title: "Machine Learning Engineer",
      company: "AI Innovations Lab",
      location: "Bangalore, India",
      description: "Develop ML models using Python, TensorFlow, and scikit-learn. Experience with data preprocessing and model deployment.",
      salary_text: "₹10-20 LPA",
      job_type: "Full-time",
      experience_required: "3-5 years"
    }
  ],

  "data science": [
    {
      title: "Data Scientist",
      company: "Analytics Pro",
      location: "Delhi, India", 
      description: "Analyze large datasets and build predictive models. Strong statistics background and Python/R experience required.",
      salary_text: "₹8-16 LPA",
      job_type: "Full-time",
      experience_required: "2-4 years"
    }
  ],

  // Generic fallback jobs
  "software": [
    {
      title: "Software Developer",
      company: "Tech Solutions Ltd",
      location: "Bangalore, India",
      description: "Join our development team to build innovative software solutions. Multiple technology stacks available.",
      salary_text: "₹5-12 LPA",
      job_type: "Full-time",
      experience_required: "1-3 years"
    }
  ],

  "engineer": [
    {
      title: "Software Engineer",
      company: "Engineering Excellence",
      location: "Hyderabad, India", 
      description: "Work on challenging engineering problems with modern technologies. Great learning and growth opportunities.",
      salary_text: "₹6-14 LPA",
      job_type: "Full-time",
      experience_required: "2-4 years"
    }
  ]
};

// Company names for variety
const COMPANIES = [
  "TechCorp Solutions", "InnovateTech", "Digital Dynamics", "CodeCraft Systems",
  "NextGen Technologies", "SmartSoft Solutions", "DataFlow Inc", "CloudFirst",
  "WebTech Innovations", "AI Pioneers", "DevOps Masters", "FullStack Pro",
  "Enterprise Solutions", "Startup Hub", "Tech Unicorn", "Innovation Labs"
];

// Indian cities for job locations
const LOCATIONS = [
  "Bangalore, India", "Mumbai, India", "Delhi, India", "Hyderabad, India",
  "Pune, India", "Chennai, India", "Kolkata, India", "Ahmedabad, India",
  "Gurgaon, India", "Noida, India"
];

// Generate mock jobs based on user skills/keywords
export const generateMockJobs = (keywords = []) => {
  console.log('🎯 Generating mock jobs for keywords:', keywords);
  
  if (!keywords || keywords.length === 0) {
    // Return general tech jobs if no keywords
    keywords = ['software', 'developer', 'engineer'];
  }
  
  const mockJobs = [];
  let jobId = 1;
  
  // Generate jobs for each keyword
  keywords.slice(0, 8).forEach(keyword => {
    const normalizedKeyword = keyword.toLowerCase().trim();
    
    // Find matching job templates
    const templates = JOB_TEMPLATES[normalizedKeyword] || [];
    
    if (templates.length > 0) {
      // Use existing templates for this keyword
      templates.forEach(template => {
        mockJobs.push({
          id: `mock_${jobId++}`,
          title: template.title,
          company: template.company,
          location: template.location,
          description: template.description,
          apply_link: `https://careers.example.com/jobs/${jobId}`,
          source: 'Mock Data',
          posted_date: new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000).toISOString(),
          job_type: template.job_type,
          salary_text: template.salary_text,
          experience_required: template.experience_required,
          skills: [keyword],
          match_score: Math.floor(Math.random() * 30) + 70 // 70-100% match
        });
      });
    } else {
      // Generate dynamic job for this keyword
      const randomCompany = COMPANIES[Math.floor(Math.random() * COMPANIES.length)];
      const randomLocation = LOCATIONS[Math.floor(Math.random() * LOCATIONS.length)];
      
      mockJobs.push({
        id: `mock_${jobId++}`,
        title: `${keyword.charAt(0).toUpperCase() + keyword.slice(1)} Developer`,
        company: randomCompany,
        location: randomLocation,
        description: `We are seeking a skilled ${keyword} professional to join our dynamic team. Work with cutting-edge technologies and contribute to innovative projects.`,
        apply_link: `https://careers.example.com/jobs/${jobId}`,
        source: 'Mock Data',
        posted_date: new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000).toISOString(),
        job_type: 'Full-time',
        salary_text: `₹${Math.floor(Math.random() * 10) + 5}-${Math.floor(Math.random() * 10) + 12} LPA`,
        experience_required: `${Math.floor(Math.random() * 3) + 1}-${Math.floor(Math.random() * 3) + 4} years`,
        skills: [keyword],
        match_score: Math.floor(Math.random() * 25) + 75 // 75-100% match
      });
    }
  });
  
  // Add some general jobs if we don't have enough
  while (mockJobs.length < 6) {
    const generalTemplates = [...JOB_TEMPLATES.software, ...JOB_TEMPLATES.engineer];
    const template = generalTemplates[Math.floor(Math.random() * generalTemplates.length)];
    
    mockJobs.push({
      id: `mock_${jobId++}`,
      ...template,
      apply_link: `https://careers.example.com/jobs/${jobId}`,
      source: 'Mock Data',
      posted_date: new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000).toISOString(),
      skills: keywords.slice(0, 3),
      match_score: Math.floor(Math.random() * 20) + 60 // 60-80% match
    });
  }
  
  // Sort by match score (highest first)
  mockJobs.sort((a, b) => b.match_score - a.match_score);
  
  console.log(`✅ Generated ${mockJobs.length} mock jobs`);
  return mockJobs.slice(0, 12); // Return top 12 jobs
};

// Search jobs by skills (main function used by Dashboard)
export const searchJobsBySkillsMock = async (skills) => {
  console.log('🔍 Mock job search for skills:', skills);
  
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  return generateMockJobs(skills);
};

// Get job statistics for mock data
export const getJobStatsMock = (jobs) => {
  const stats = {
    total_jobs: jobs.length,
    active_jobs: jobs.length,
    sources: { 'Mock Data': jobs.length },
    locations: {},
    companies: {},
    match_scores: {
      high: jobs.filter(j => j.match_score >= 80).length,
      medium: jobs.filter(j => j.match_score >= 60 && j.match_score < 80).length,
      low: jobs.filter(j => j.match_score < 60).length
    }
  };
  
  jobs.forEach(job => {
    // Location stats
    const location = job.location || 'Unknown';
    stats.locations[location] = (stats.locations[location] || 0) + 1;
    
    // Company stats  
    const company = job.company || 'Unknown';
    stats.companies[company] = (stats.companies[company] || 0) + 1;
  });
  
  return stats;
};

export default {
  generateMockJobs,
  searchJobsBySkillsMock,
  getJobStatsMock
};
