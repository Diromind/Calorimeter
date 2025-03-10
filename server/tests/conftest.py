import pytest
import asyncpg

from utils import get_config
from utils import fetch_lockbox_secret

@pytest.fixture(name="service_db", scope="session")
async def _service_db(postgresql_proc):
    dsn = postgresql_proc.dsn()
    pool = await asyncpg.create_pool(dsn)
    yield pool
    await pool.close()


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
        "id1": "test_secret_value_1",
        "id2": "test_secret_value_2",
    }
    # Replace fetch_secret with a lambda that returns a value from our dict.
    monkeypatch.setattr(fetch_lockbox_secret, "fetch_secret", lambda secret_id: test_secrets.get(secret_id))
