from typing import List

from pydantic import UUID4

from server.app.impl.db_models import Item
from server.app.handles.models import StoreRequest

from server.app.impl.users import select_user_by_tg_id
from server.app.impl.exceptions import RequestMissingDataException

async def get_user_id(body: StoreRequest) -> UUID4:
    if body.user_id:
        user_id = body.user_id
    elif body.tg_id:
        user_id = await select_user_by_tg_id(body.tg_id)
    else:
        raise RequestMissingDataException("Must provide user_id or tg_id")

    return user_id


async def save_items_to_db(items: List[Item]):
    pass