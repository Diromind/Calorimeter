import os
import uuid
from server.app.handles.models import StoreRequest, StoreResponse

from calorimeter.server.app.impl.store import get_user_id

from calorimeter.server.utils.psql_executor import execute_sql_async


async def store_handle(body: StoreRequest) -> StoreResponse:
    """
    Implementation for the /store endpoint.
    Expects a StoreRequest (an object with an 'items' key containing an array of records).
    For each record, generates a new UUID and executes an upsert using the SQL script.
    """
    user_id = get_user_id(body)

    uuids = []

    for item in body.items:
        record_uuid = str(uuid.uuid4())
        uuids.append(record_uuid)
        params = (
            record_uuid,
            body.user_id,
            item.value,
            item.description if item.description is not None else None,
        )
        await execute_sql_async(upsert_sql, params)

    return StoreResponse(uuids=uuids)
