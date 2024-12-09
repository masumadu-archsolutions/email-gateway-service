from app.core.repository import SQLBaseRepository
from app.models import BatchModel


class BatchRepository(SQLBaseRepository):
    model = BatchModel
    object_name = "batch"
