# tests/test_store_async.py
import pytest

@pytest.mark.asyncio
async def test_async_query(service_db):
    print("enter", flush=True)
    async with service_db.acquire() as conn:
        print(1, flush=True)
        result = await conn.fetchval("SELECT 1")
        assert result == 1
