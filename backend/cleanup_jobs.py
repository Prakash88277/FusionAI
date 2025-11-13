"""
Clean up database - remove jobs with N/A titles or descriptions
"""
import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def cleanup_database():
    """Remove jobs with N/A or invalid data"""
    try:
        # Connect to database
        conn = sqlite3.connect('jobs.db')
        cursor = conn.cursor()
        
        # Count current jobs
        cursor.execute("SELECT COUNT(*) FROM jobs")
        total_before = cursor.fetchone()[0]
        logger.info(f"Total jobs before cleanup: {total_before}")
        
        # Delete jobs with N/A or empty titles
        cursor.execute("""
            DELETE FROM jobs 
            WHERE title IS NULL 
            OR title = '' 
            OR title = 'N/A' 
            OR title LIKE '%N/A%'
            OR company IS NULL
            OR company = ''
            OR company = 'N/A'
            OR company LIKE '%N/A%'
        """)
        
        deleted_count = cursor.rowcount
        logger.info(f"Deleted {deleted_count} jobs with N/A or invalid data")
        
        # Count remaining jobs
        cursor.execute("SELECT COUNT(*) FROM jobs")
        total_after = cursor.fetchone()[0]
        logger.info(f"Total jobs after cleanup: {total_after}")
        
        # Commit changes
        conn.commit()
        conn.close()
        
        logger.info("✅ Database cleanup completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Error during cleanup: {e}")

if __name__ == "__main__":
    cleanup_database()
