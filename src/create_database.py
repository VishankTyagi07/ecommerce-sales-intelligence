"""
Create Database and Tables
Executes schema.sql to create database structure

Author: Vishank
Created: 9 December 2025
"""

import sqlite3
import os

def create_database():
    """
    Create SQLite database and execute schema
    """
    print("DATABASE CREATION")
    
    # Ensure database directory exists
    os.makedirs('database', exist_ok=True)
    
    db_path = 'database/ecommerce.db'
    schema_path = 'database/schema.sql'
    
    # Check if schema file exists
    if not os.path.exists(schema_path):
        print(f" ERROR: {schema_path} not found!")
        print("   Please create the schema.sql file first.")
        return False
    
    try:
        # Connect to database (creates file if doesn't exist)
        print(f"\n Connecting to database: {db_path}")
        conn = sqlite3.connect(db_path)
        print("    Connected successfully")
        
        # Read schema file
        print(f"\nReading schema from: {schema_path}")
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        print("   Schema file read successfully")
        
        # Execute schema (create tables)
        print(f"\n Creating tables...")
        conn.executescript(schema_sql)
        print("   ✅ Tables created successfully")
        
        # Verify tables exist
        print(f"\n Verifying tables...")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables = cursor.fetchall()
        
        if tables:
            print(f"   ✅ Found {len(tables)} tables:")
            for table in tables:
                print(f"      - {table[0]}")
        else:
            print("   No tables found!")
        
        # Close connection
        conn.close()
        print("\n✅ Database setup complete!")
        print(f"\n📁 Database created at: {db_path}")

        
        return True
        
    except sqlite3.Error as e:
        print(f"\n Database Error: {e}")
        return False
    except Exception as e:
        print(f"\n Unexpected Error: {e}")
        return False

if __name__ == "__main__":
    create_database()