import os
import glob

from dotenv import load_dotenv
from psycopg2 import connect

load_dotenv()


def execute_sql_file(filepath, conn):
    with open(filepath, 'r') as file:
        sql_content = file.read()

    cur = conn.cursor()
    cur.execute(sql_content)
    conn.commit()
    print(f"Executed: {filepath}")


def execute_all_migrations():
    # Get all SQL files in the migrations folder
    sql_files = glob.glob('./migrations/*.sql')
    sql_files.sort()  # Execute files in alphabetical order

    if not sql_files:
        print("No SQL files found in migrations folder")
        return

    try:
        with connect(
            f"dbname={os.getenv('DB_NAME')} "
            f"user={os.getenv('DB_USER')} "
            f"password={os.getenv('DB_PASSWORD')} "
            f"host={os.getenv('DB_HOST')}"
        ) as conn:
            for sql_file in sql_files:
                execute_sql_file(sql_file, conn)
        print(f"Successfully executed {len(sql_files)} migration(s)")
    except Exception as e:
        print(f"Error executing migrations: {e}")


if __name__ == "__main__":
    execute_all_migrations()
