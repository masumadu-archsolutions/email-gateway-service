import uuid
from datetime import datetime
from typing import Literal, Union

from fastapi import Query
from pydantic import BaseModel

from app.constants import MessageTypePriority, SortOrderEnum


class MessageTypeSchema(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    type: str
    priority: str
    delivery_mode: str
    description: Union[str, None]
    is_active: bool
    created_at: datetime
    created_by: Union[str, None]
    updated_at: datetime
    updated_by: Union[str, None]
    is_deleted: bool
    deleted_at: Union[datetime, None]
    deleted_by: Union[str, None]

    class Config:
        from_attributes = True


class AddNMessageTypeSchema(BaseModel):
    type: str
    priority: MessageTypePriority
    delivery_mode: Literal["direct", "broadcast"]
    description: str = None

    class Config:
        use_enum_values = True


class QueryMessageTypeSchema(BaseModel):
    keyword: Union[str, None] = Query(None)
    sort_order: Union[SortOrderEnum, None] = Query(SortOrderEnum.desc)
    sort_by: Union[str, None] = Query("created_at")
