import psycopg2
import os
import glob
import subprocess
import yaml

# Load config.yaml

config_path = os.path.join(os.environ["HOME"], "calorimeter/config.yaml")
with open(config_path, "r") as f:
    config = yaml.safe_load(f)

if "password" in config["db"]:
    DB_PASSWORD = config["db"]
    if not DB_PASSWORD:
        print("Database password in config is empty! Aborting")
        exit(1)
else:
    print("Database password not found in config.yaml!")
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    if not DB_PASSWORD:
        print("Database password env var empty! Aborting")
        exit(1)

DB_CONFIG = {
    "host": config["db"]["host"],
    "port": config["db"].get("port", 5432),
    "dbname": config["db"]["name"],
    "user": config["db"]["user"],
    "password": DB_PASSWORD,
}

BACKUP_FILE = config["backup"]["file"]

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
    cursor.execute("SELECT filename FROM migrations;")
    applied_migrations = {row[0] for row in cursor.fetchall()}

    # Find all SQL migration files in order
    migration_files = sorted(glob.glob("*.sql"))

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
            cursor.execute("INSERT INTO migrations (filename) VALUES (%s);", (filename,))
            cursor.execute("COMMIT;")  # Commit if successful
            conn.commit()
            print(f"{filename} applied successfully.")
        except Exception as e:
            cursor.execute("ROLLBACK;")  # Undo changes on error
            print(f"Error applying {filename}: {e}")
            print("Migration process aborted.")
            break

    cursor.close()
    conn.close()
    print("All migrations applied successfully!")

if __name__ == "__main__":
    create_backup()  # Backup first
    run_migrations()  # Apply migrations
