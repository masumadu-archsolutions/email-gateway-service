import uuid

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

from app.core.database import Base

from .base_model import BaseModel


class EmailModel(Base, BaseModel):
    __tablename__ = "email_messages"
    id = sa.Column(sa.UUID, primary_key=True, default=uuid.uuid4)
    user_id = sa.Column(sa.UUID, nullable=False, index=True)
    sender_address = sa.Column(sa.String, nullable=False, index=True)
    sender_name = sa.Column(sa.String, nullable=True, index=True)
    subject = sa.Column(sa.String, nullable=True)
    html_body = sa.Column(sa.String, nullable=True)
    text_body = sa.Column(sa.String, nullable=True)
    type = sa.Column(sa.String, nullable=False)
    tags = sa.Column(JSONB)
    is_scheduled = sa.Column(sa.Boolean, nullable=False, default=False)
    scheduled_date = sa.Column(sa.DateTime(timezone=True), nullable=True)
    total_recipients = sa.Column(sa.Integer, nullable=False)
    require_callback = sa.Column(
        sa.Boolean, nullable=False, default=False, server_default="False"
    )
    status = sa.Column(sa.String, nullable=True)
