from datetime import datetime

from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate

from app.models import AccountModel
from app.repositories import AccountRepository
from app.utils import remove_none_fields


class AccountController:
    def __init__(self, account_repository: AccountRepository):
        self.account_repository = account_repository

    def create_account(self, auth_user: dict, obj_data: dict) -> AccountModel:
        user_id = auth_user.get("id")
        return self.account_repository.create(
            obj_in={
                "user_id": user_id,
                "mail_address": obj_data.get("email_address"),
                "sender_name": obj_data.get("sender_name"),
                "password": obj_data.get("password"),
                "is_default": obj_data.get("is_default"),
                "created_by": user_id,
                "updated_by": user_id,
            }
        )

    def get_all_accounts(
        self, auth_user: dict, page_params: Params, query_params: dict
    ) -> paginate:
        return self.account_repository.advance_query(
            keyword=query_params.get("keyword"),
            sort_param={
                "order": query_params.get("sort_order"),
                "column": query_params.get("sort_by"),
            },
            filter_params={"user_id": auth_user.get("id")},
            paginate_data=True,
            page_params=page_params,
        )

    def get_account(self, obj_id: str) -> AccountModel:
        return self.account_repository.find_by_id(obj_id=obj_id)

    def update_account(self, obj_data: dict) -> AccountModel:
        return self.account_repository.update_by_id(
            obj_id=obj_data.get("account_id"), obj_in=remove_none_fields(obj_data)
        )

    def delete_account(self, auth_user: dict, obj_id: str):
        self.account_repository.update_by_id(
            obj_id=obj_id,
            obj_in={
                "is_deleted": True,
                "deleted_by": auth_user.get("id"),
                "deleted_at": datetime.utcnow(),
            },
        )
        return None
