from typing import List, Optional, Union

from pydantic import BaseModel, Field, model_validator

from calorimeter.server.app.impl.db_models import Item

class StoreRequest(BaseModel):
    user_id: Optional[int] = None
    tg_id: Optional[int] = None
    items: List[Union[Item, int]]

    @model_validator(mode="before")
    def validate_user_fields(cls, values):
        if not values.get("user_id") and not values.get("tg_id"):
            raise ValueError("At least one of 'user_id' or 'tg_id' must be provided.")
        return values

    class Config:
        extra = "forbid"  # Prevent unexpected fields


class StoreResponse(BaseModel):
    uuids: Optional[List[str]] = Field(None, description='UUIDs of the saved records')


class RecordsRequest(BaseModel):
    user_id: int = Field(..., description='ID of the user')


class RecordOutput(BaseModel):
    uuid: Optional[str] = Field(None, description='Unique identifier of the record')
    user_id: Optional[int] = Field(
        None, description='ID of the user associated with the record'
    )


class UserUpdateRequest(BaseModel):
    user_id: int = Field(..., description='ID of the user to update')
    surname: Optional[str] = Field(None, description='Optional surname of the user')
    name: Optional[str] = Field(None, description='Optional first name of the user')


class UserInfo(BaseModel):
    user_id: Optional[int] = Field(None, description="User's ID")
    surname: Optional[str] = Field(None, description="User's surname")
    name: Optional[str] = Field(None, description="User's first name")


class UserIdRequest(BaseModel):
    user_id: int = Field(..., description='ID of the user')
