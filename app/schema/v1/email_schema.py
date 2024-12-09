import uuid
from datetime import date as ddate
from datetime import datetime
from typing import List, Union

from fastapi import Query
from pydantic import BaseModel, EmailStr

from app.constants import SortOrderEnum


class EmailQuerySchema(BaseModel):
    keyword: Union[str, None] = Query(None)
    date: Union[ddate, None] = Query(None)
    min_date: Union[ddate, None] = Query(None)
    max_date: Union[ddate, None] = Query(None)
    date_column: Union[str, None] = Query(None)
    sort_order: Union[SortOrderEnum, None] = Query(SortOrderEnum.desc)
    sort_by: Union[str, None] = Query("created_at")


class EmailSchema(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    sender_address: str
    sender_name: Union[str, None]
    type: str
    tags: Union[List[str], None]
    is_scheduled: bool
    scheduled_date: Union[datetime, None]
    total_recipients: int
    status: Union[str, None]

    class Config:
        orm_mode = True


class SendEmailSchema(BaseModel):
    sender: EmailStr
    name: str = None
    recipients: List[EmailStr]
    subject: str
    html_body: str
    text_body: str = None
    type: str
    tags: List[str] = None
    webhook_url: str = None


class EmailResponseSchema(BaseModel):
    id: uuid.UUID
    is_success: bool


class EmailBatchSchema(BaseModel):
    id: uuid.UUID
    email_id: uuid.UUID
    total_recipients: int
    status: Union[str, None]

    class Config:
        orm_mode = True


class RecipientSchema(BaseModel):
    id: uuid.UUID
    batch_id: uuid.UUID
    mail_address: EmailStr

    class Config:
        orm_mode = True


class RecipientEmailSchema(BaseModel):
    id: uuid.UUID
    mail_address: EmailStr
    message: Union[EmailSchema, None]

    class Config:
        orm_mode = True
