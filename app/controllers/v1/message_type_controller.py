from datetime import datetime

from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate

from app.repositories import MessageTypeRepository
from app.services import RedisService


class MessageTypeController:
    def __init__(
        self, message_type_repository: MessageTypeRepository, redis_service: RedisService
    ):
        self.message_type_repository = message_type_repository
        self.redis_service = redis_service

    def add_message_type(self, auth_user: dict, obj_data: dict):
        user_id = auth_user.get("id")
        return self.message_type_repository.create(
            obj_in={
                "user_id": user_id,
                "type": obj_data.get("type"),
                "priority": obj_data.get("priority"),
                "description": obj_data.get("description"),
                "created_by": user_id,
                "updated_by": user_id,
            }
        )

    def get_all_message_type(
        self, auth_user: dict, page_params: Params, query_params: dict
    ) -> paginate:
        return self.message_type_repository.advance_query(
            keyword=query_params.get("keyword"),
            sort_param={
                "order": query_params.get("sort_order"),
                "column": query_params.get("sort_by"),
            },
            paginate_data=True,
            page_params=page_params,
        )

    def delete_message_type(self, auth_user: dict, obj_id: str) -> None:
        self.message_type_repository.update_by_id(
            obj_id=obj_id,
            obj_in={
                "is_active": False,
                "is_deleted": True,
                "deleted_by": auth_user.get("id"),
                "deleted_at": datetime.utcnow(),
            },
        )
        return None

    def activate_message_type(self, auth_user: dict, obj_id: str) -> None:
        message_type = self.message_type_repository.update_by_id(
            obj_id=obj_id,
            obj_in={
                "is_active": True,
                "is_deleted": False,
                "updated_by": auth_user.get("id"),
            },
        )
        return message_type

    def verify_message_type(self, message_type: str) -> None:
        return self.message_type_repository.find(filter_param={"type": message_type})
