import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
import pymysql

# Load environment variables
load_dotenv()

def test_mysql_connection():
    try:
        # Get database credentials
        db_user = os.getenv("MYSQL_USER")
        db_password = os.getenv("MYSQL_PASSWORD")
        db_host = os.getenv("MYSQL_HOST", "127.0.0.1")
        db_port = os.getenv("MYSQL_PORT", "3306")
        
        print(f"Testing connection to MySQL at {db_host}:{db_port}")
        print(f"User: {db_user}")
        print(f"Password: {'*' * len(db_password) if db_password else 'None'}")
        
        # Create connection URL safely (handles special characters in password)
        url_object = URL.create(
            "mysql+pymysql",
            username=db_user,
            password=db_password,
            host=db_host,
            port=int(db_port) if str(db_port).isdigit() else None,
        )
        print("Connection URL built safely via SQLAlchemy URL object.")
        
        # Test connection
        engine = create_engine(url_object, pool_pre_ping=True)
        
        with engine.connect() as conn:
            # Test basic connection
            result = conn.execute(text("SELECT VERSION()"))
            version = result.scalar_one()
            print(f"✅ MySQL connection successful! Version: {version}")
            
            # Test if we can create database
            db_name = os.getenv("MYSQL_DB", "crypto")
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{db_name}`"))
            print(f"✅ Database '{db_name}' created/verified successfully!")
            
            return True
            
    except Exception as e:
        print(f"❌ MySQL connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing MySQL Connection...")
    success = test_mysql_connection()
    if success:
        print("\n🎉 MySQL setup is working correctly!")
    else:
        print("\n💥 Please check your MySQL configuration and try again.")
