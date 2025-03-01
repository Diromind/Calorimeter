from typing import List, Optional

from pydantic import BaseModel, Field


class RecordInput(BaseModel):
    user_id: int = Field(..., description='ID of the user creating the record')
    values: List[float] = Field(
        ..., description='Array of numeric values associated with the record'
    )
    description: Optional[str] = Field(
        None, description='Optional description for the record'
    )


class StoreResponse(BaseModel):
    uuids: Optional[List[str]] = Field(None, description='UUIDs of the saved records')


class RecordOutput(BaseModel):
    uuid: Optional[str] = Field(None, description='Unique identifier of the record')
    user_id: Optional[int] = Field(
        None, description='ID of the user associated with the record'
    )


class UserUpdate(BaseModel):
    user_id: int = Field(..., description='ID of the user to update')
    surname: Optional[str] = Field(None, description='Optional surname of the user')
    name: Optional[str] = Field(None, description='Optional first name of the user')


class UserInfo(BaseModel):
    user_id: Optional[int] = Field(None, description="User's ID")
    surname: Optional[str] = Field(None, description="User's surname")
    name: Optional[str] = Field(None, description="User's first name")


class StorePostRequest(BaseModel):
    __root__: List[RecordInput]
