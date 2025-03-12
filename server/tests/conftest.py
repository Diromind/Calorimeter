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
    # Parse the DSN from postgresql_proc
    dsn = postgresql_proc.dsn()
    parsed = urlparse(dsn)

    def fake_psycopg2_connect(**kwargs):
        # Ignore any passed kwargs and connect using our test DSN.
        # Note: We use a hard-coded password ("test_password")
        # which should match what your fetch_secret monkeypatch returns.
        return psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port,
            dbname=parsed.path.lstrip("/"),
            user=parsed.username,
            password="test_password"
        )

    # Patch psycopg2.connect so that any call in run_migrations() uses our fake connector.
    monkeypatch.setattr(apply_migrations, "connect", fake_psycopg2_connect)
    # Optionally, if you have a wrapper function for psycopg2 connections,
    # patch it as well. For example, if psql_executor exposes psycopg2_connection():
    monkeypatch.setattr(apply_migrations, "psycopg2_connection", fake_psycopg2_connect)