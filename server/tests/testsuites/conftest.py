import pytest
import asyncpg

@pytest.fixture(name="service_db", scope="session")
async def _service_db(postgresql_proc):
    dsn = postgresql_proc.dsn()
    pool = await asyncpg.create_pool(dsn)
    yield pool
    await pool.close()
