import sqlite3

def explore_sqlite_db(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Fetch all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("Tables in the database:")
    for table_name in tables:
        table_name = table_name[0]
        print(f"- {table_name}")
        
        # Fetch column information for each table
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        print(f"  Columns in {table_name}:")
        for column in columns:
            print(f"    - {column[1]} (Type: {column[2]})")
        
        # Example: Query first few rows of data from the table
        print("  Sample data from this table:")
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
        sample_data = cursor.fetchall()
        for row in sample_data:
            print(f"    {row}")
    
    # Close the connection
    conn.close()

# Use the function
explore_sqlite_db('db.sqlite3')