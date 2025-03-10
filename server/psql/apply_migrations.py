import psycopg2
import os
import glob
import subprocess

from utils import fetch_lockbox_secret as utils
from utils import get_config

def make_db_config():
    config = get_config.get_config_value("db")

    db_config = {
        "host": config["host"],
        "port": config.get("port", 5432),
        "dbname": config["name"],
        "user": config["user"],
    }

    if "pswd_secret_id" in config:
        db_config["password"] = utils.fetch_secret(config["pswd_secret_id"])
    else:
        print("No lockbox id for DB password! Aborting")
        exit(1)

    return db_config


DB_CONFIG = make_db_config()

BACKUP_FILE = get_config.get_config_value("backup")["file"]

def create_backup():
    print("Creating database backup...")

    try:
        print("pg_dump", "-U", DB_CONFIG["user"], "-d", DB_CONFIG["dbname"], "-F", "c", "-f", BACKUP_FILE)
        subprocess.run(
            ["pg_dump", "-h", DB_CONFIG["host"],
                        "-U", DB_CONFIG["user"],
                        "-d", DB_CONFIG["dbname"],
                        "-F", "c",
                        "-f", BACKUP_FILE],
            check=True,
            env={**os.environ, "PGPASSWORD": DB_CONFIG["password"]}
        )
        print(f"Backup saved to {BACKUP_FILE}")
    except subprocess.CalledProcessError:
        print("Backup failed! Aborting migrations.")
        exit(1)

def run_migrations():
    """Runs all pending migrations."""
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Ensure the migrations table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calorimeter.migrations (
            id SERIAL PRIMARY KEY,
            filename TEXT UNIQUE NOT NULL,
            applied_at TIMESTAMPTZ DEFAULT now()
        );
    """)
    conn.commit()

    # Get already applied migrations
    cursor.execute("SELECT filename FROM calorimeter.migrations;")
    applied_migrations = {row[0] for row in cursor.fetchall()}

    # Find all SQL migration files in order
    migr_path = os.path.join(os.environ["HOME"], "calorimeter/server/psql/migrations/*.sql")
    migration_files = sorted(glob.glob(migr_path))

    for filepath in migration_files:
        filename = os.path.basename(filepath)

        if filename in applied_migrations:
            print(f"Skipping {filename}, already applied.")
            continue

        print(f"Applying {filename}...")

        with open(filepath, "r", encoding="utf-8") as f:
            sql = f.read()

        try:
            cursor.execute("BEGIN;")  # Start a transaction
            cursor.execute(sql)  # Run SQL migration
            cursor.execute("INSERT INTO calorimeter.migrations (filename) VALUES (%s);", (filename,))
            cursor.execute("COMMIT;")  # Commit if successful
            conn.commit()
            print(f"{filename} applied successfully.")
        except Exception as e:
            cursor.execute("ROLLBACK;")  # Undo changes on error
            print(f"Error applying {filename}: {e}")
            print("Migration process aborted.")
            exit(1)

    cursor.close()
    conn.close()
    print("All migrations applied successfully!")

if __name__ == "__main__":
    create_backup()  # Backup first
    run_migrations()  # Apply migrations
