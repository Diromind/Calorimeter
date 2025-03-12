import psycopg2
import pytest
import asyncpg

from calorimeter.utils import get_config
from calorimeter.utils import fetch_lockbox_secret
from calorimeter.server.utils import psql_executor
from calorimeter.server.psql import apply_migrations

from urllib.parse import urlparse

@pytest.fixture(name="calorimeter_db", scope="session")
async def _service_db(postgresql_proc):
    dsn = postgresql_proc.dsn()
    pool = await asyncpg.create_pool(dsn)
    yield pool
    await pool.close()

@pytest.fixture(autouse=True)
def patch_asyncpg_connection(monkeypatch, calorimeter_db):
    monkeypatch.setattr(psql_executor, "asyncpg_connection", lambda : calorimeter_db)

@pytest.fixture(autouse=True)
def patch_config(monkeypatch):
    test_config = {
        "db": {
            "name": "calorimeter_db",
            "user": "calorimeter_robot",
            "host": "localhost",
            "port": 5432,
            "pswd_secret_id": "test_secret_id_for_pg_pswd"
        },
        "backup": {
            "file": "test_db_backup.dump"
        },
        "telegram": {
            "token_secret_id": "test_tg_token"
        }
    }
    # Override __read_config__ to always return our test_config.
    monkeypatch.setattr(get_config, "__read_config__", lambda cache={'content': None}: test_config)


@pytest.fixture(autouse=True)
def patch_fetch_secret(monkeypatch):
    # Define a mapping of secret IDs to test secret values.
    test_secrets = {
        "test_secret_id_for_pg_pswd": "password_mock",
        "test_tg_token": "telegram_token_mock",
    }
    # Replace fetch_secret with a lambda that returns a value from our dict.
    monkeypatch.setattr(fetch_lockbox_secret, "fetch_secret", lambda secret_id: test_secrets.get(secret_id))


@pytest.fixture(autouse=True)
def patch_psycopg2_connection(monkeypatch, postgresql_proc):
    # Manually build connection parameters from postgresql_proc's attributes.
    host = getattr(postgresql_proc, "host", "localhost")
    port = getattr(postgresql_proc, "port", 5432)
    dbname = getattr(postgresql_proc, "dbname", "postgres")
    user = getattr(postgresql_proc, "user", "postgres")
    # Set a test password; ensure it matches what your secret patch returns.
    password = "test_password"

    def fake_psycopg2_connect(**kwargs):
        # Ignores kwargs and connects using the temporary DB credentials.
        return psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
        )

    # Patch psycopg2.connect globally as well as any wrapper in your utils.
    monkeypatch.setattr(psycopg2, "connect", fake_psycopg2_connect)
    monkeypatch.setattr(psql_executor, "psycopg2_connection", fake_psycopg2_connect)