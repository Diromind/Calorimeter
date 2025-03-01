import asyncio
import asyncpg
import psycopg2
import yaml

from utils import fetch_lockbox_secret as utils
from utils import get_config

config = get_config.get_config_value("db")

DB_CONFIG = {
    "host": config["host"],
    "port": config.get("port", 5432),
    "dbname": config["name"],
    "user": config["user"],
}

if "pswd_secret_id" in config:
    DB_CONFIG["password"] = utils.fetch_secret(config["pswd_secret_id"])
else:
    print("No lockbox id for DB password! Aborting")
    exit(1)

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
        await conn.execute(script, params)
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
