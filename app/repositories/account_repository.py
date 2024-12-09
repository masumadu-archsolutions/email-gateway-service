from app.core.repository import SQLBaseRepository
from app.models import AccountModel


class AccountRepository(SQLBaseRepository):
    model = AccountModel
    object_name = "account"
