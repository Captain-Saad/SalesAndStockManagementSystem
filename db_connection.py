import pymysql
import logging
from typing import Optional
from config import get_database_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConnection:
    def __init__(self, **kwargs):
        # Get default config and override with any provided kwargs
        config = get_database_config()
        config.update(kwargs)
        
        self.host = config['host']
        self.user = config['user']
        self.password = config['password']
        self.database = config['database']
        self.charset = config['charset']
        self.connect_timeout = config['connect_timeout']
        self.read_timeout = config['read_timeout']
        self.write_timeout = config['write_timeout']
        self.connection = None

    def __enter__(self) -> Optional[pymysql.Connection]:
        """Establish the connection when entering the context"""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset=self.charset,
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True,
                connect_timeout=self.connect_timeout,
                read_timeout=self.read_timeout,
                write_timeout=self.write_timeout
            )
            logger.info("Database connection established successfully")
            return self.connection
        except pymysql.Error as e:
            logger.error(f"Database connection failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during database connection: {e}")
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Properly close the connection when exiting the context"""
        if self.connection:
            try:
                self.connection.close()
                logger.info("Database connection closed successfully")
            except Exception as e:
                logger.error(f"Error closing database connection: {e}")

    def execute_query(self, query: str, params: tuple = None):
        """Execute a query and return results"""
        try:
            with self as conn:
                if conn is None:
                    return None
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    if query.strip().upper().startswith('SELECT'):
                        return cursor.fetchall()
                    else:
                        conn.commit()
                        return cursor.rowcount
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            return None

    @staticmethod
    def test_connection() -> bool:
        """Test database connection without creating a persistent connection"""
        try:
            with DatabaseConnection() as conn:
                if conn is None:
                    return False
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False
