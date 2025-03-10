import os

import asyncpg
import psycopg2

from calorimeter.utils import fetch_lockbox_secret as utils
from calorimeter.utils import get_config

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


def get_sql_script(name: str) -> str:
    script_path = os.path.join(os.path.dirname(__file__), '..', 'psql', 'scripts', f'{name}.sql')
    with open(script_path, 'r') as f:
        script = f.read().strip()
    return script

async def execute_sql_async(script: str, params: tuple):
    """Execute SQL script asynchronously using asyncpg."""
    conn = await asyncpg.connect(
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["dbname"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"]
    )
    try:
        await conn.execute(script, *params)
    finally:
        await conn.close()

def execute_sql_sync(script: str, params: tuple):
    """Execute SQL script synchronously using psycopg2."""
    conn = psycopg2.connect(
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["dbname"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"]
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute(script, *params)
        conn.commit()
    finally:
        conn.close()
