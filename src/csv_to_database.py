"""
CSV to SQL Database Converter
Loads CSV file(s) into SQLite database

Author: Vishank
Created: 10 December 2024
"""

import pandas as pd
import sqlite3
import os
import glob

def csv_to_database(csv_path, table_name=None, db_path='database/ecommerce.db'):
    """
    Loading CSV file into SQLite database
    
    Args:
        csv_path (str): Path to CSV file
        table_name (str): Name for database table (filename)
        db_path (str): Path to database file
    
    Returns:
        bool: True if successful
    """
    
    
    print("CSV TO DATABASE CONVERTER")
    
    
    # Check if CSV exists
    if not os.path.exists(csv_path):
        print(f"❌ ERROR: CSV file not found: {csv_path}")
        return False
    
    try:
        # Determine table name
        if table_name is None:
            # Use filename without extension
            table_name = os.path.splitext(os.path.basename(csv_path))[0]
            table_name = table_name.lower().replace(' ', '_').replace('-', '_')
        
        print(f"\n📂 Reading CSV: {csv_path}")
        
        # Read CSV file
        df = pd.read_csv(csv_path)
        
        print(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns")
        print(f"\nOriginal columns: {', '.join(df.columns)}")
        
        # Clean column names
        df.columns = df.columns.str.strip()  # Remove whitespace
        df.columns = df.columns.str.replace(' ', '_')  # Replace spaces with underscore
        df.columns = df.columns.str.replace('[^a-zA-Z0-9_]', '', regex=True)  # Remove special chars
        df.columns = df.columns.str.lower()  # Lowercase
        
        print(f"Cleaned columns: {', '.join(df.columns)}")
        
        # Show data types
        print(f"\nData types:")
        for col in df.columns:
            dtype = df[col].dtype
            null_count = df[col].isnull().sum()
            print(f"   {col}: {dtype} ({null_count} nulls)")
        
        # Create database directory if needed
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Connect to database
        print(f"\n📊 Creating/connecting to database: {db_path}")
        conn = sqlite3.connect(db_path)
        
        # Load data into database
        print(f"\n📥 Loading data into table: '{table_name}'")
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        
        # Verify
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"✅ Verified: {count:,} rows loaded successfully")
        
        # Show sample data
        print(f"\n📋 Sample data from '{table_name}':")
        sample = pd.read_sql(f"SELECT * FROM {table_name} LIMIT 3", conn)
        print(sample.to_string())
        
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ CONVERSION COMPLETE!")
        print("=" * 60)
        print(f"\n📁 Database: {db_path}")
        print(f"📊 Table: {table_name}")
        print(f"📈 Rows: {count:,}")
        print("\n🚀 Next steps:")
        print("   1. Open database in DB Browser to verify")
        print("   2. Run queries using src/analytics.py")
        print("   3. Start your analysis!")
        print("=" * 60 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def multiple_csvs_to_database(csv_folder, db_path='database/ecommerce.db'):
    """
    Load multiple CSV files from a folder into database
    Each CSV becomes a separate table
    
    Args:
        csv_folder (str): Folder containing CSV files
        db_path (str): Path to database file
    
    Returns:
        bool: True if successful
    """
    
    print("=" * 60)
    print("MULTIPLE CSVs TO DATABASE")
    print("=" * 60)
    
    # Find all CSV files
    csv_files = glob.glob(os.path.join(csv_folder, '*.csv'))
    
    if not csv_files:
        print(f"❌ ERROR: No CSV files found in: {csv_folder}")
        return False
    
    print(f"\n📂 Found {len(csv_files)} CSV file(s):")
    for csv_file in csv_files:
        print(f"   - {os.path.basename(csv_file)}")
    
    # Create database connection
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    
    success_count = 0
    
    for csv_file in csv_files:
        try:
            # Get table name from filename
            table_name = os.path.splitext(os.path.basename(csv_file))[0]
            table_name = table_name.lower().replace(' ', '_').replace('-', '_')
            
            print(f"\n{'='*60}")
            print(f"Processing: {os.path.basename(csv_file)}")
            print('='*60)
            
            # Read CSV
            df = pd.read_csv(csv_file)
            print(f"   Rows: {len(df)}")
            print(f"   Columns: {len(df.columns)}")
            
            # Clean column names
            df.columns = df.columns.str.strip().str.replace(' ', '_').str.lower()
            df.columns = df.columns.str.replace('[^a-zA-Z0-9_]', '', regex=True)
            
            # Load into database
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            print(f"   ✅ Loaded into table: '{table_name}'")
            
            success_count += 1
            
        except Exception as e:
            print(f"   ❌ ERROR loading {csv_file}: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("LOADING SUMMARY")
    print("=" * 60)
    
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = cursor.fetchall()
    
    print(f"\n📊 Tables in database:")
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"   {table_name}: {count:,} rows")
    
    conn.close()
    
    print("\n" + "=" * 60)
    print(f"✅ Loaded {success_count}/{len(csv_files)} files successfully!")
    print("=" * 60)
    print(f"\n📁 Database: {db_path}")
    print("=" * 60 + "\n")
    
    return success_count == len(csv_files)


def inspect_csv(csv_path):
    """
    Inspect CSV file before loading
    Shows structure, data types, sample data
    
    Args:
        csv_path (str): Path to CSV file
    """
    
    print("=" * 60)
    print("CSV FILE INSPECTOR")
    print("=" * 60)
    
    if not os.path.exists(csv_path):
        print(f"❌ ERROR: File not found: {csv_path}")
        return
    
    try:
        print(f"\n📂 File: {csv_path}")
        print(f"📏 Size: {os.path.getsize(csv_path) / 1024:.2f} KB")
        
        # Read CSV
        df = pd.read_csv(csv_path)
        
        print(f"\n📊 STRUCTURE:")
        print(f"   Rows: {len(df):,}")
        print(f"   Columns: {len(df.columns)}")
        
        print(f"\n📋 COLUMNS:")
        for i, col in enumerate(df.columns, 1):
            dtype = df[col].dtype
            null_count = df[col].isnull().sum()
            unique_count = df[col].nunique()
            print(f"   {i:2d}. {col:30s} | Type: {str(dtype):10s} | Nulls: {null_count:5d} | Unique: {unique_count:6d}")
        
        print(f"\n🔍 SAMPLE DATA (First 5 rows):")
        print(df.head().to_string())
        
        print(f"\n📈 STATISTICS:")
        print(df.describe().to_string())
        
        print(f"\n⚠️  DATA QUALITY CHECKS:")
        print(f"   Total missing values: {df.isnull().sum().sum()}")
        print(f"   Duplicate rows: {df.duplicated().sum()}")
        
        # Check for potential date columns
        date_cols = []
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    pd.to_datetime(df[col], errors='raise')
                    date_cols.append(col)
                except:
                    pass
        
        if date_cols:
            print(f"   Potential date columns: {', '.join(date_cols)}")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()


# ==========================================
# MAIN EXECUTION
# ==========================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("=" * 60)
        print("CSV TO DATABASE CONVERTER - USAGE")
        print("=" * 60)
        print("\n📖 OPTION 1: Inspect CSV file")
        print("   python src/csv_to_database.py inspect <csv_file>")
        print("\n   Example:")
        print("   python src/csv_to_database.py inspect data/sales.csv")
        
        print("\n📥 OPTION 2: Convert single CSV to database")
        print("   python src/csv_to_database.py convert <csv_file> [table_name]")
        print("\n   Examples:")
        print("   python src/csv_to_database.py convert data/sales.csv")
        print("   python src/csv_to_database.py convert data/sales.csv orders")
        
        print("\n📦 OPTION 3: Convert multiple CSVs from folder")
        print("   python src/csv_to_database.py convert-folder <folder_path>")
        print("\n   Example:")
        print("   python src/csv_to_database.py convert-folder data/csv_files/")
        
        print("\n" + "=" * 60 + "\n")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "inspect":
        if len(sys.argv) < 3:
            print("❌ ERROR: Please provide CSV file path")
            print("   python src/csv_to_database.py inspect data/sales.csv")
            sys.exit(1)
        
        csv_path = sys.argv[2]
        inspect_csv(csv_path)
    
    elif command == "convert":
        if len(sys.argv) < 3:
            print("❌ ERROR: Please provide CSV file path")
            print("   python src/csv_to_database.py convert data/sales.csv")
            sys.exit(1)
        
        csv_path = sys.argv[2]
        table_name = sys.argv[3] if len(sys.argv) > 3 else None
        csv_to_database(csv_path, table_name)
    
    elif command == "convert-folder":
        if len(sys.argv) < 3:
            print("❌ ERROR: Please provide folder path")
            print("   python src/csv_to_database.py convert-folder data/")
            sys.exit(1)
        
        folder_path = sys.argv[2]
        multiple_csvs_to_database(folder_path)
    
    else:
        print(f"❌ ERROR: Unknown command '{command}'")
        print("   Use: inspect, convert, or convert-folder")
        sys.exit(1)
