import sqlite3
import os
import re

def run_business_queries():
    db_path = "data/warehouse/av_diagnostics.db"
    sql_file = "sql/business_queries.sql"
    
    if not os.path.exists(db_path):
        print("Database not found. Please run the pipeline first: python run_pipeline.py")
        return
    
    if not os.path.exists(sql_file):
        print("SQL file not found.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    with open(sql_file, 'r') as f:
        sql_content = f.read()
    
    # Remove comments and split by semicolon
    sql_content = re.sub(r'--.*', '', sql_content)  # Remove -- comments
    queries = [q.strip() for q in sql_content.split(';') if q.strip()]
    
    for i, query in enumerate(queries, 1):
        if query:
            print(f"\n--- Query {i} ---")
            print(query)
            try:
                cursor.execute(query)
                if query.strip().upper().startswith('SELECT'):
                    results = cursor.fetchall()
                    if results:
                        # Print column names
                        column_names = [desc[0] for desc in cursor.description]
                        print(" | ".join(column_names))
                        print("-" * (sum(len(col) for col in column_names) + 3 * (len(column_names) - 1)))
                        for row in results:
                            print(" | ".join(str(cell) for cell in row))
                    else:
                        print("No results.")
                else:
                    print("Query executed (non-SELECT).")
            except Exception as e:
                print(f"Error: {e}")
    
    conn.close()

if __name__ == "__main__":
    run_business_queries()