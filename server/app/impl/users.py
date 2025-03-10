from calorimeter.server.utils.psql_executor import execute_sql_async

async def select_user_by_tg_id(telegram_id: int):
    return await execute_sql_async('select_user_by_tg_id', (telegram_id, ))

async def select_user_by_id(user_id: int):
    return await execute_sql_async('select_user_by_id', (user_id, ))

