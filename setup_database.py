import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

print("🔄 Setting up database schema...")

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=os.getenv('PGHOST'),
        user=os.getenv('PGUSER'),
        password=os.getenv('PGPASSWORD'),
        database=os.getenv('PGDATABASE'),
        port=os.getenv('PGPORT'),
        sslmode='require'
    )
    
    cursor = conn.cursor()
    
    # Table 1: Track uploaded datasets
    print("Creating 'datasets' table...")
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS datasets (
        id SERIAL PRIMARY KEY,
        filename VARCHAR(255) NOT NULL,
        file_format VARCHAR(50),
        file_size_mb DECIMAL(10, 2),
        row_count INTEGER,
        column_count INTEGER,
        upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status VARCHAR(50) DEFAULT 'uploaded',
        blob_path VARCHAR(500)
    );
    ''')
    
    # Table 2: Track analysis runs
    print("Creating 'analysis_runs' table...")
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS analysis_runs (
        id SERIAL PRIMARY KEY,
        dataset_id INTEGER REFERENCES datasets(id),
        run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        analysis_type VARCHAR(100),
        insights_generated TEXT,
        recommendations TEXT,
        charts_created INTEGER DEFAULT 0,
        latency_seconds DECIMAL(10, 2),
        cost_usd DECIMAL(10, 4),
        status VARCHAR(50) DEFAULT 'completed'
    );
    ''')
    
    # Table 3: MLflow tracking (Databricks certification alignment)
    print("Creating 'mlflow_runs' table...")
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS mlflow_runs (
        id SERIAL PRIMARY KEY,
        run_id VARCHAR(100) UNIQUE,
        experiment_name VARCHAR(255),
        model_name VARCHAR(255),
        temperature DECIMAL(3, 2),
        max_tokens INTEGER,
        prompt_version VARCHAR(50),
        evaluation_score DECIMAL(5, 2),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ''')
    
    # Table 4: Data governance (Unity Catalog principles)
    print("Creating 'data_governance' table...")
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS data_governance (
        id SERIAL PRIMARY KEY,
        dataset_id INTEGER REFERENCES datasets(id),
        owner VARCHAR(100),
        sensitivity_level VARCHAR(50),
        last_accessed TIMESTAMP,
        access_count INTEGER DEFAULT 0,
        tags TEXT[]
    );
    ''')
    
    # Commit changes
    conn.commit()
    print("\n✅ Database schema created successfully!")
    
    # Verify tables
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name
    """)
    
    tables = cursor.fetchall()
    print("\n📊 Tables in database:")
    for table in tables:
        print(f"  ✓ {table[0]}")
    
    # Close connection
    cursor.close()
    conn.close()
    
    print("\n🎉 Day 1 Database Setup Complete!")
    
except Exception as e:
    print(f"❌ Setup failed: {e}")
