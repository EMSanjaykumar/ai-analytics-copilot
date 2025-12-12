import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

print("🔄 Testing PostgreSQL connection...")

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=os.getenv('PGHOST'),
        user=os.getenv('PGUSER'),
        password=os.getenv('PGPASSWORD'),
        database=os.getenv('PGDATABASE'),
        port=os.getenv('PGPORT'),
        sslmode='require'  # Azure requires SSL
    )
    
    cursor = conn.cursor()
    
    # Test query
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    
    print("✅ PostgreSQL connection successful!")
    print(f"📊 PostgreSQL version: {version[0][:50]}...")
    
    # Close connection
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Connection failed!")
    print(f"Error: {e}")
    print("\n🔧 Troubleshooting:")
    print("1. Check your .env file has the correct password")
    print("2. Verify PostgreSQL firewall allows your IP")
    print("3. Ensure PostgreSQL server is running in Azure Portal")
