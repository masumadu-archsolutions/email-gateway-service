import uuid

import sqlalchemy as sa

from app.core.database import Base

from .base_model import BaseModel


class BatchModel(Base, BaseModel):
    __tablename__ = "email_message_batches"
    id = sa.Column(sa.UUID, primary_key=True, default=uuid.uuid4)
    email_id = sa.Column(
        sa.UUID, sa.ForeignKey("email_messages.id"), nullable=False, index=True
    )
    total_recipients = sa.Column(sa.Integer, nullable=False)
    status = sa.Column(sa.String, nullable=True)
