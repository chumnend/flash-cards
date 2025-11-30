import os

from dotenv import load_dotenv
from psycopg2 import connect

load_dotenv()

def drop_all_tables():
    """Drop all tables in the database"""
    try:
        with connect(
            f"dbname={os.getenv('DB_NAME')} "
            f"user={os.getenv('DB_USER')} "
            f"password={os.getenv('DB_PASSWORD')} "
            f"host={os.getenv('DB_HOST')}"
        ) as conn:
            cur = conn.cursor()
            
            # Get all table names
            cur.execute("""
                SELECT tablename FROM pg_tables 
                WHERE schemaname = 'public'
            """)
            tables = cur.fetchall()
            
            if not tables:
                print("No tables found to drop")
                return
            
            # Drop all tables with CASCADE to handle foreign keys
            table_names = [table[0] for table in tables]
            for table_name in table_names:
                cur.execute(f'DROP TABLE IF EXISTS "{table_name}" CASCADE')
                print(f"Dropped table: {table_name}")
            
            conn.commit()
            print(f"Successfully dropped {len(table_names)} table(s)")
            
    except Exception as e:
        print(f"Error dropping tables: {e}")

if __name__ == "__main__":
    drop_all_tables()
