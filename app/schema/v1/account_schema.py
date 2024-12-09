import uuid
from datetime import datetime
from typing import Union

from pydantic import BaseModel, EmailStr, Field

from app.constants import SortOrderEnum


class AccountSchema(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    mail_address: EmailStr
    sender_name: str
    is_default: bool
    created_by: uuid.UUID
    created_at: datetime
    updated_by: uuid.UUID
    updated_at: datetime
    is_deleted: bool
    deleted_by: Union[uuid.UUID, None]
    deleted_at: Union[datetime, None]

    class Config:
        from_attributes = True


class CreateAccountSchema(BaseModel):
    email_address: EmailStr
    sender_name: str
    password: str
    is_default: bool = False


class UpdateAccountSchema(BaseModel):
    account_id: uuid.UUID
    sender_name: str = None
    password: str = None
    is_default: bool = None


class AccountQuerySchema(BaseModel):
    keyword: Union[str, None] = Field(None)
    sort_order: SortOrderEnum = Field(SortOrderEnum.desc)
    sort_by: Union[str, None] = Field("created_at")
