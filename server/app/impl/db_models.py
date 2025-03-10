import datetime
from typing import Optional

from pydantic import BaseModel, UUID4

class User(BaseModel):
    id: int
    telegram_id: int
    name: Optional[str]
    surname: Optional[str]

class Item:
    item_id: UUID4
    item_name: Optional[str]
    place_id: Optional[UUID4]
    calories: float
    proteins: Optional[float]
    fats: Optional[float]
    carbs: Optional[float]

class Record(BaseModel):
    uuid: UUID4
    user_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    item_uuid: UUID4

class Place(BaseModel):
    place_id: UUID4
    place_name: Optional[str]