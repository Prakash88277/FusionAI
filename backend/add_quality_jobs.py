"""
Add high-quality jobs with real apply links to the database
"""
import sqlite3
import uuid
from datetime import datetime, timedelta
import random
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_quality_jobs():
    """Add realistic jobs with proper apply links"""
    
    quality_jobs = [
        {
            "title": "Senior Software Engineer, Mobile (Android), Platforms and Devices",
            "company": "Google",
            "location": "Bengaluru, Karnataka, India",
            "description": "Lead the development of next-generation features for Android platforms, focusing on performance optimization and system integration across Google’s device ecosystem.",
            "skills": ["Python", "Java", "JavaScript", "Software Engineering", "Problem Solving"],
            "apply_link": "https://www.google.com/about/careers/applications/jobs/results/104992311871447750-senior-software-engineer-mobile-android-platforms-and-devices",
            "salary_text": "₹35-50 LPA",
            "source": "google",
            "job_type": "full_time",
            "experience_level": "senior"
        },
        {
            "title": "Software Engineer III, Machine Learning, Geo",
            "company": "Google",
            "location": "Bengaluru, Karnataka, India",
            "description": "Develop and deploy scalable machine learning models for geographical and mapping products. Requires expertise in geospatial data processing and large-scale model deployment.",
            "skills": ["Python", "Java", "JavaScript", "Software Engineering", "Problem Solving"],
            "apply_link": "https://www.google.com/about/careers/applications/jobs/results/100373991520117446-software-engineer-iii-machine-learning-geo",
            "salary_text": "₹25-40 LPA",
            "source": "google",
            "job_type": "full_time",
            "experience_level": "senior"
        },
        {
            "title": "Staff Software Engineer, AI/ML, Platform and Applications",
            "company": "Google",
            "location": "Bengaluru, Karnataka, India",
            "description": "Provide technical direction and leadership for complex AI/ML systems used across multiple Google products. Influence long-term engineering roadmaps and mentor junior staff.",
            "skills": ["Python", "Java", "JavaScript", "Software Engineering", "Problem Solving"],
            "apply_link": "https://www.google.com/about/careers/applications/jobs/results/83264446654227142-staff-software-engineer-aiml-platform-and-applications",
            "salary_text": "₹55-80 LPA",
            "source": "google",
            "job_type": "full_time",
            "experience_level": "advanced"
        },
        {
            "title": "Software Engineer II, Google Ads",
            "company": "Google",
            "location": "Hyderabad, Telangana, India",
            "description": "Contribute to the core functionality and scaling of the Google Ads platform, developing high-throughput, low-latency services using modern backend technologies.",
            "skills": ["Python", "Java", "JavaScript", "Software Engineering", "Problem Solving"],
            "apply_link": "https://www.google.com/about/careers/applications/jobs/results/98368083952837318-software-engineer-ii-google-ads",
            "salary_text": "₹15-22 LPA",
            "source": "google",
            "job_type": "full_time",
            "experience_level": "mid"
        },
        {
            "title": "Technical Program Manager, University Graduate 2026",
            "company": "Google",
            "location": "Bengaluru, Karnataka, India",
            "description": "Manage cross-functional technical projects and timelines for engineering teams. Requires strong collaboration and foundational knowledge of technical concepts and processes.",
            "skills": ["Python", "Java", "JavaScript", "Software Engineering", "Problem Solving"],
            "apply_link": "https://www.google.com/about/careers/applications/jobs/results/127715274437599942-technical-program-manager-university-graduate-2026",
            "salary_text": "₹10-15 LPA",
            "source": "google",
            "job_type": "full_time",
            "experience_level": "early"
        },
        {
            "title": "Senior Embedded Software Engineer, Silicon Security",
            "company": "Google",
            "location": "Bengaluru, Karnataka, India",
            "description": "Focus on developing and securing embedded software for custom silicon architectures within Google's hardware division, ensuring integrity and performance.",
            "skills": ["Python", "Java", "JavaScript", "Software Engineering", "Problem Solving"],
            "apply_link": "https://www.google.com/about/careers/applications/jobs/results/82584148933255878-senior-embedded-software-engineer-silicon-security",
            "salary_text": "₹30-45 LPA",
            "source": "google",
            "job_type": "full_time",
            "experience_level": "senior"
        },
        {
            "title": "Software Development Engineer II, Amazon Now",
            "company": "Amazon",
            "location": "Bengaluru, Karnataka, India",
            "description": "Contribute to the development of the Amazon Now (Quick Commerce) platform, focusing on scalable microservices, delivery logistics, and high-availability backend systems.",
            "skills": ["Python", "Java", "JavaScript", "Software Engineering", "Problem Solving"],
            "apply_link": "https://amazon.jobs/en-gb/jobs/3077898/software-development-engineer-ii-amazon",
            "salary_text": "₹20-35 LPA",
            "source": "amazon",
            "job_type": "full_time",
            "experience_level": "mid"
        },
        {
            "title": "Software Development Manager, Quick Commerce",
            "company": "Amazon",
            "location": "Bengaluru, Karnataka, India",
            "description": "Lead and mentor a team of SDEs building a brand-new initiative in the fast-growing world of Quick Commerce. Own outcomes and deliver robust, scalable technology solutions.",
            "skills": ["Python", "Java", "JavaScript", "Software Engineering", "Problem Solving"],
            "apply_link": "https://amazon.jobs/en-gb/jobs/3127166/software-development-manager",
            "salary_text": "₹45-70 LPA",
            "source": "amazon",
            "job_type": "full_time",
            "experience_level": "advanced"
        },
        {
            "title": "Senior Software Development Engineer, Annapurna Labs, Elastic Collectives",
            "company": "Amazon",
            "location": "Hyderabad, Telangana, India",
            "description": "Work on optimizing Amazon's global transportation and logistics software, focusing on improving efficiency using data algorithms and performance engineering.",
            "skills": ["Python", "Java", "JavaScript", "Software Engineering", "Problem Solving"],
            "apply_link": "https://amazon.jobs/en-gb/jobs/3127189/senior-software-development-engineer-annapurna-labs-elastic-collectives",
            "salary_text": "₹12-18 LPA",
            "source": "amazon",
            "job_type": "full_time",
            "experience_level": "early"
        },
        {
            "title": "Controls Design Engineer, Data Center Engineering , Data Center Engineering",
            "company": "Amazon",
            "location": "Chennai, Tamil Nadu, India",
            "description": "Design and build high-performance data pipelines and ETL processes to support large-scale retail analytics and reporting systems. Ensure data quality and governance.",
            "skills": ["Python", "Java", "JavaScript", "Software Engineering", "Problem Solving"],
            "apply_link": "https://amazon.jobs/en-gb/jobs/3022851/controls-design-engineer-data-center-engineering-data-center-engineering",
            "salary_text": "₹22-38 LPA",
            "source": "amazon",
            "job_type": "full_time",
            "experience_level": "senior"
        },
        {
            "title": "Automation Engineer, RME",
            "company": "Amazon",
            "location": "Bengaluru, Karnataka, India",
            "description": "Apply machine learning techniques to solve complex business problems within Amazon's services division. Requires expertise in statistical modeling and production deployment.",
            "skills": ["Python", "Java", "JavaScript", "Software Engineering", "Problem Solving"],
            "apply_link": "https://amazon.jobs/en-gb/jobs/3022835/automation-engineer-rme",
            "salary_text": "₹35-55 LPA",
            "source": "amazon",
            "job_type": "full_time",
            "experience_level": "senior"
        },
        {
            "title": "Software Engineer, Product (Technical Leadership)",
            "company": "Meta",
            "location": "Bengaluru, Karnataka, India",
            "description": "Drive technical strategy and system architecture for a large-scale consumer product. Requires excellent programming design, system architecture, and product leadership.",
            "skills": ["Python", "Java", "JavaScript", "Software Engineering", "Problem Solving"],
            "apply_link": "https://www.metacareers.com/jobs/1892835578110898",
            "salary_text": "₹40-65 LPA",
            "source": "meta",
            "job_type": "full_time",
            "experience_level": "advanced"
        },
        {
            "title": "Partner Engineer, Manager (Generative AI)",
            "company": "Meta",
            "location": "Mumbai, Maharashtra, India",
            "description": "Lead a team of engineers focusing on integrating Meta's Generative AI models and large language models (LLMs) with enterprise partner solutions and cloud platforms.",
            "skills": ["Python", "Java", "JavaScript", "Software Engineering", "Problem Solving"],
            "apply_link": "https://www.metacareers.com/jobs/2032865240807295",
            "salary_text": "₹45-75 LPA",
            "source": "meta",
            "job_type": "full_time",
            "experience_level": "advanced"
        },
        {
            "title": "Partner Engineer, Generative AI",
            "company": "Meta",
            "location": "Mumbai, Maharashtra, India",
            "description": "Work hands-on with enterprise partners to implement and optimize Meta's Deep Learning and LLM solutions. Focus on PyTorch and Kubernetes for deployment.",
            "skills": ["Python", "Java", "JavaScript", "Software Engineering", "Problem Solving"],
            "apply_link": "https://www.metacareers.com/jobs/25141192702199005",
            "salary_text": "₹30-50 LPA",
            "source": "meta",
            "job_type": "full_time",
            "experience_level": "senior"
        },
        {
            "title": "Research Scientist, Machine Learning (PhD)",
            "company": "Meta",
            "location": "Bengaluru, Karnataka, India",
            "description": "Conduct cutting-edge research in machine learning and related fields, focusing on innovation and publishing high-impact technical papers. Requires a PhD background.",
            "skills": ["Python", "Java", "JavaScript", "Software Engineering", "Problem Solving"],
            "apply_link": "https://www.metacareers.com/jobs/1835678850417840",
            "salary_text": "₹60-90 LPA",
            "source": "meta",
            "job_type": "full_time",
            "experience_level": "advanced"
        },
        {
            "title": "Software Engineer, Infrastructure (Core Services)",
            "company": "Microsoft",
            "location": "Hyderabad, Telangana, India",
            "description": "Build and maintain the core infrastructure services supporting Azure and related cloud products. Focus on scalability, reliability, and security of foundational components.",
            "skills": ["Python", "Java", "JavaScript", "Software Engineering", "Problem Solving"],
            "apply_link": "https://careers.microsoft.com/v2/global/en/locations/india.html",
            "salary_text": "₹28-42 LPA",
            "source": "microsoft",
            "job_type": "full_time",
            "experience_level": "senior"
        },
        {
            "title": "Senior Data Scientist, Cloud Security",
            "company": "Microsoft",
            "location": "Noida, Uttar Pradesh, India",
            "description": "Apply statistical modeling and machine learning to detect and mitigate threats within Microsoft's cloud security landscape. Requires large-scale data processing skills.",
            "skills": ["Python", "Java", "JavaScript", "Software Engineering", "Problem Solving"],
            "apply_link": "https://careers.microsoft.com/v2/global/en/locations/noida.html",
            "salary_text": "₹35-55 LPA",
            "source": "microsoft",
            "job_type": "full_time",
            "experience_level": "senior"
        },
        {
            "title": "Software Engineer, Backend (Core Payments)",
            "company": "PhonePe",
            "location": "Bengaluru, Karnataka, India",
            "description": "Develop and maintain high-throughput, fault-tolerant backend services for PhonePe's core payments platform. Focus on robustness and transactional integrity.",
            "skills": ["Python", "Java", "JavaScript", "Software Engineering", "Problem Solving"],
            "apply_link": "https://job-boards.greenhouse.io/phonepe/jobs/6076913003",
            "salary_text": "₹18-30 LPA",
            "source": "phonepe",
            "job_type": "full_time",
            "experience_level": "mid"
        },
        {
            "title": "Engineering Manager, Backend (Fraud & Risk)",
            "company": "PhonePe",
            "location": "Pune, Maharashtra, India",
            "description": "Lead an engineering team dedicated to building real-time fraud detection and risk mitigation systems. Requires strong technical leadership and domain expertise in risk systems.",
            "skills": ["Python", "Java", "JavaScript", "Software Engineering", "Problem Solving"],
            "apply_link": "https://job-boards.greenhouse.io/phonepe/jobs/7517285003",
            "salary_text": "₹35-55 LPA",
            "source": "phonepe",
            "job_type": "full_time",
            "experience_level": "senior"
        },
        {
            "title": "Software Architect, Core Engineering",
            "company": "PhonePe",
            "location": "Bengaluru, Karnataka, India",
            "description": "Define the long-term technical vision and architecture for PhonePe's large-scale engineering systems, ensuring optimal performance and design flexibility.",
            "skills": ["Python", "Java", "JavaScript", "Software Engineering", "Problem Solving"],
            "apply_link": "https://job-boards.greenhouse.io/phonepe/jobs/6598552003",
            "salary_text": "₹45-70 LPA",
            "source": "phonepe",
            "job_type": "full_time",
            "experience_level": "advanced"
        },
        {
            "title": "Principal Software Engineer - Python Technologies",
            "company": "Rapid7",
            "location": "Pune, Maharashtra, India",
            "description": "Drive technical initiatives and architect large components using Python for cybersecurity and vulnerability management products. Requires 10+ years of technical ownership.",
            "skills": ["Python", "Java", "JavaScript", "Software Engineering", "Problem Solving"],
            "apply_link": "https://www.hirist.tech/j/rapid7-principal-software-engineer-python-technologies-1547450?ref=sp&jobPos=1",
            "salary_text": "₹40-65 LPA",
            "source": "hirist",
            "job_type": "full_time",
            "experience_level": "advanced"
        },
        {
            "title": "Senior Java Developer - Spring/Hibernate",
            "company": "Synechron",
            "location": "Hyderabad, Telangana, India",
            "description": "Develop and maintain robust enterprise applications using core Java, Spring, and Hibernate frameworks. Focus on banking and financial services domain solutions.",
            "skills": ["Python", "Java", "JavaScript", "Software Engineering", "Problem Solving"],
            "apply_link": "https://www.hirist.tech/j/senior-java-developer-spring-hibernate-1572719?ref=sp&jobPos=1",
            "salary_text": "₹18-28 LPA",
            "source": "hirist",
            "job_type": "full_time",
            "experience_level": "mid"
        },
        {
            "title": "Product Manager - Strategy & Roadmap",
            "company": "Siemens",
            "location": "Bangalore, Karnataka, India",
            "description": "Define the strategic roadmap and requirements for industrial IoT and digital transformation products. Requires a blend of technical understanding and market analysis.",
            "skills": ["Python", "Java", "JavaScript", "Software Engineering", "Problem Solving"],
            "apply_link": "https://www.hirist.tech/j/product-manager-roadmap-and-strategy-1573920?ref=sp_br_prm&jobPos=1",
            "salary_text": "₹25-35 LPA",
            "source": "hirist",
            "job_type": "full_time",
            "experience_level": "senior"
        },
        {
            "title": "DevOps Engineer II",
            "company": "HackerRank",
            "location": "Bangalore, Karnataka, India",
            "description": "Maintain and scale the production environment using automated CI/CD pipelines, focusing on maximizing uptime and optimizing cloud infrastructure costs.",
            "skills": ["Python", "Java", "JavaScript", "Software Engineering", "Problem Solving"],
            "apply_link": "https://job-boards.greenhouse.io/hackerrank/jobs/7325481?gh_jid=7325481",
            "salary_text": "₹15-25 LPA",
            "source": "hackerrank",
            "job_type": "full_time",
            "experience_level": "mid"
        },
        {
            "title": "Senior Frontend Engineer, Core Platform",
            "company": "HackerRank",
            "location": "Bangalore, Karnataka, India",
            "description": "Lead the development of highly interactive and performant user interfaces for the core platform. Requires strong expertise in modern JavaScript frameworks and design principles.",
            "skills": ["Python", "Java", "JavaScript", "Software Engineering", "Problem Solving"],
            "apply_link": "https://job-boards.greenhouse.io/hackerrank/jobs/7100792?gh_jid=7100792",
            "salary_text": "₹28-40 LPA",
            "source": "hackerrank",
            "job_type": "full_time",
            "experience_level": "senior"
        },
        {
            "title": "AWS Cloud Architect",
            "company": "Virtusa",
            "location": "Chennai, Tamil Nadu, India",
            "description": "Design and govern complex, secure cloud environments on AWS for enterprise clients. Focus on large-scale migration and modernization projects.",
            "skills": ["Python", "Java", "JavaScript", "Software Engineering", "Problem Solving"],
            "apply_link": "https://www.virtusa.com/careers/us/new-york/aws/aws-cloud-engineer-kubernetes-eks-specialist/creq232973",
            "salary_text": "₹30-50 LPA",
            "source": "virtusa",
            "job_type": "full_time",
            "experience_level": "advanced"
        },
        {
            "title": "Cloud Platform Architect",
            "company": "Virtusa",
            "location": "Hyderabad, Telangana, India",
            "description": "Define strategy for cloud platform adoption, including migration, modernization, and incorporating AI/GenAI services into client architecture.",
            "skills": ["Python", "Java", "JavaScript", "Software Engineering", "Problem Solving"],
            "apply_link": "https://www.virtusa.com/careers/in/hyderabad/aws/cloud-platform-architect/creq234998",
            "salary_text": "₹40-60 LPA",
            "source": "virtusa",
            "job_type": "full_time",
            "experience_level": "advanced"
        },
        {
            "title": "Python Developer",
            "company": "Hashedin by Deloitte",
            "location": "Bangalore, Kolkata, Pune",
            "description": "HashedIn, a company founded in the year 2010 is a services company focused on building SaaS products and design-led product engineering. Leveraging its SaaS development expertise, HashedIn has been transforming enterprises using its cutting technology by bringing in Multi-tenancy, cloudification, next-gen UI/UX, and modularity.",
            "skills": ["Python", "JavaScript", "Software Engineering", "Problem Solving"],
            "apply_link": "https://www.instahyre.com/job-393500-python-developer-at-hashedin-by-deloitte-bangalore-kolkata-pune/",
            "salary_text": "₹25-38 LPA",
            "source": "instahyre",
            "job_type": "full_time",
            "experience_level": "senior"
        },
        {
            "title": "Java Developer",
            "company": "Cloudesign",
            "location": "Mumbai, India",
            "description": "Cloudesign Technology Solutions is a digital transformation IT consulting and services company, that enables digital transformation for enterprises and technology providers by delivering seamless customer experiences, business efficiency, and actionable insights. We are doing the same thing as any big IT company does but doing it a lot better with innovation in technology, processes, and delivery; thus making it affordable.",
            "skills": ["Python", "Java", "JavaScript", "Software Engineering", "Problem Solving"],
            "apply_link": "https://www.instahyre.com/job-397011-java-developer-at-cloudesign-mumbai/",
            "salary_text": "₹35-50 LPA",
            "source": "instahyre",
            "job_type": "full_time",
            "experience_level": "senior"
        }
    ]
    
    try:
        conn = sqlite3.connect('jobs.db')
        cursor = conn.cursor()
        
        # Get current job count
        cursor.execute("SELECT COUNT(*) FROM jobs")
        initial_count = cursor.fetchone()[0]
        logger.info(f"Current jobs in database: {initial_count}")
        
        added_count = 0
        for job in quality_jobs:
            try:
                # Create job entry
                job_id = str(uuid.uuid4())
                posted_date = datetime.now() - timedelta(days=random.randint(1, 30))
                scraped_date = datetime.now()
                
                cursor.execute("""
                    INSERT INTO jobs (
                        job_id, title, company, location, description, skills,
                        apply_link, source, posted_date, scraped_at, salary_text,
                        job_type, is_active
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    job_id,
                    job["title"],
                    job["company"],
                    job["location"],
                    job["description"],
                    '["' + '", "'.join(job["skills"]) + '"]',  # Convert to JSON format
                    job["apply_link"],
                    job["source"],
                    posted_date.isoformat(),
                    scraped_date.isoformat(),
                    job["salary_text"],
                    job["job_type"],
                    1  # is_active = True
                ))
                added_count += 1
                
            except Exception as e:
                logger.error(f"Error adding job {job['title']}: {e}")
                continue
        
        conn.commit()
        
        # Get final count
        cursor.execute("SELECT COUNT(*) FROM jobs")
        final_count = cursor.fetchone()[0]
        
        conn.close()
        
        logger.info(f"✅ Successfully added {added_count} quality jobs!")
        logger.info(f"Total jobs in database: {final_count}")
        
    except Exception as e:
        logger.error(f"❌ Error adding quality jobs: {e}")

if __name__ == "__main__":
    add_quality_jobs()
