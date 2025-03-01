import os
import uuid
from server.app.impl.models import StoreRequest, StoreResponse
from server.utils.psql_executor import execute_sql_async

async def bulk_store_records(body: StoreRequest) -> StoreResponse:
    """
    Implementation for the /store endpoint.
    Expects a StoreRequest (an object with an 'items' key containing an array of records).
    For each record, generates a new UUID and executes an upsert using the SQL script.
    """
    uuids = []
    script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'psql', 'scripts', 'upsert_calories.sql')
    with open(script_path, 'r') as f:
        upsert_sql = f.read().strip()

    for item in body.items:
        record_uuid = str(uuid.uuid4())
        uuids.append(record_uuid)
        params = (
            record_uuid,
            item.user_id,
            item.value,
            item.description if item.description is not None else None,
        )
        await execute_sql_async(upsert_sql, params)

    return StoreResponse(uuids=uuids)
