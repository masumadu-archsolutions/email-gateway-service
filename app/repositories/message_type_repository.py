from app.core.repository import SQLBaseRepository
from app.models import MessageTypeModel


class MessageTypeRepository(SQLBaseRepository):
    model = MessageTypeModel
    object_name = "message type"
