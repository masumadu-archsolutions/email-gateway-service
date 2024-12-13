import uuid

import sqlalchemy as sa

from app.constants import MessageTypePriority
from app.core.database import Base

from .base_model import BaseModel


class MessageTypeModel(Base, BaseModel):
    __tablename__ = "email_message_types"
    id = sa.Column(sa.UUID, primary_key=True, default=uuid.uuid4)
    user_id = sa.Column(sa.UUID, nullable=False, index=True)
    type = sa.Column(sa.String, nullable=False, unique=True)
    delivery_mode = sa.Column(sa.String, nullable=False, server_default="direct")
    priority = sa.Column(
        sa.String,
        nullable=False,
        default=MessageTypePriority.high.value,
        server_default=MessageTypePriority.high.value,
    )
    description = sa.Column(sa.String, nullable=True)
    is_active = sa.Column(sa.Boolean, nullable=False, default=False)
