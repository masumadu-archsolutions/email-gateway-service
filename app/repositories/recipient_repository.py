from app.core.repository import SQLBaseRepository
from app.models import RecipientModel


class RecipientRepository(SQLBaseRepository):
    model = RecipientModel
    object_name = "recipient"
