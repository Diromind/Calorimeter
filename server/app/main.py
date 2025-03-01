from typing import List

from fastapi import FastAPI

from server.app.impl.models import (
    RecordOutput,
    RecordsRequest,
    StoreRequest,
    StoreResponse,
    UserIdRequest,
    UserInfo,
    UserUpdateRequest,
)

from server.app.impl.bulk_store_records import bulk_store_records

app = FastAPI(
    title='Calorimeter API',
    version='1.0.0',
    description='An API for managing calorimeter records',
)


@app.post('/records', response_model=List[RecordOutput])
async def retrieve_records(body: RecordsRequest) -> List[RecordOutput]:
    """
    Retrieve records for a user
    """
    pass


@app.post('/store', response_model=StoreResponse)
async def bulk_store_records(body: StoreRequest) -> StoreResponse:
    """
    Bulk store records
    """
    return await bulk_store_records(body)


@app.post('/update_user', response_model=UserInfo)
async def update_user(body: UserUpdateRequest) -> UserInfo:
    """
    Update user information
    """
    pass


@app.post('/user_info', response_model=UserInfo)
async def get_user_info(body: UserIdRequest) -> UserInfo:
    """
    Retrieve user information
    """
    pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)