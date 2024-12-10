import json

from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate

from app.constants import EMAIL_BATCH_SIZE, EMAIL_REQUEST_SIZE, KAFKA_TOPIC_PREFIX
from app.core.exceptions import AppException, HTTPException
from app.models import EmailModel
from app.producer import publish_to_kafka
from app.repositories import (
    AccountRepository,
    BatchRepository,
    EmailRepository,
    MessageTypeRepository,
    RecipientRepository,
)
from app.schema.v1 import MessageTypeSchema
from app.services import RedisService
from app.utils import load_in_batches, remove_none_fields

from .batch_controller import BatchController


class EmailController:
    def __init__(
        self,
        email_repository: EmailRepository,
        batch_repository: BatchRepository,
        recipient_repository: RecipientRepository,
        message_type_repository: MessageTypeRepository,
        account_repository: AccountRepository,
        batch_controller: BatchController,
        redis_service: RedisService,
    ):
        self.email_repository = email_repository
        self.batch_repository = batch_repository
        self.recipient_repository = recipient_repository
        self.message_type_repository = message_type_repository
        self.account_repository = account_repository
        self.batch_controller = batch_controller
        self.redis_service = redis_service

    def send_email(self, auth_user: dict, obj_data: dict) -> dict:
        user_id = auth_user.get("id")
        account = self.sender_account(user_id, obj_data.get("sender"))
        obj_data["name"] = obj_data.get("name") or account.sender_name
        obj_data["password"] = account.password
        message_type = self.validate_message_type(
            user_id=user_id, msg_type=obj_data.get("type")
        )
        obj_data["priority"] = message_type.get("priority")
        obj_data["trade_name"], obj_data["queue"] = self.message_queue(
            auth_user=auth_user, message_type=obj_data.get("type")
        )
        mail = self.create_email_record(user_id=user_id, obj_data=obj_data)
        if mail.total_recipients > EMAIL_BATCH_SIZE:
            self.create_email_request_task(
                obj_data=obj_data, email=mail, auth_user=auth_user
            )
        else:
            obj_data["email_id"] = str(mail.id)
            obj_data["user_id"] = user_id
            self.batch_controller.create_email_batch(obj_data=obj_data)
        return {"id": mail.id, "is_success": True}

    def sender_account(self, user_id: str, sender: str):
        return self.account_repository.find(
            filter_param={
                "user_id": user_id,
                "mail_address": sender,
                "is_deleted": False,
            }
        )

    def validate_message_type(self, msg_type: str, user_id: str):
        try:
            message_type = self.redis_service.get(
                f"email_{user_id}_{msg_type}"
            ) or self.message_type(msg_type, user_id)
        except HTTPException:
            message_type = self.message_type(msg_type, user_id)
        message_type = json.loads(message_type)
        if not message_type.get("is_active"):
            raise AppException.BadRequestException(
                error_message=f"MessageTypeError({msg_type}) not activated"
            )
        return message_type

    # noinspection PyMethodMayBeStatic
    def message_type(self, msg_type: str, user_id: str):
        message_type = self.message_type_repository.find(
            filter_param={"user_id": user_id, "type": msg_type}
        )
        value = MessageTypeSchema.model_validate(message_type).model_dump_json()
        self.redis_service.set(name=f"email_{user_id}_{msg_type}", value=value)
        return value

    def create_email_record(self, user_id: str, obj_data: dict):
        return self.email_repository.create(
            obj_in={
                "user_id": user_id,
                "sender_address": obj_data.get("sender"),
                "sender_name": obj_data.get("name"),
                "subject": obj_data.get("subject"),
                "type": obj_data.get("type"),
                "tags": obj_data.get("tags"),
                "total_recipients": len(obj_data.get("recipients")),
                "require_callback": bool(obj_data.get("webhook_url")),
                "created_by": user_id,
                "updated_by": user_id,
            }
        )

    def create_email_request_task(
        self, obj_data: dict, email: EmailModel, auth_user: dict
    ):
        recipients = obj_data.get("recipients")
        kafka_topic = f"{obj_data.get('trade_name')}_{KAFKA_TOPIC_PREFIX}_{obj_data.get('type')}_request".upper()  # noqa
        for batch in load_in_batches(data=recipients, size=EMAIL_REQUEST_SIZE):
            publish_to_kafka(
                kafka_topic,
                {
                    "email_id": str(email.id),
                    "sender": email.sender_address,
                    "name": obj_data.get("name"),
                    "recipients": batch,
                    "message": obj_data.get("html_body"),
                    "type": email.type,
                    "priority": obj_data.get("priority"),
                    "webhook_url": obj_data.get("webhook_url"),
                    "user_id": auth_user.get("id"),
                    "topic": kafka_topic,
                    "queue": obj_data.get("queue"),
                },
            )
        self.email_repository.update_by_id(
            obj_id=email.id, obj_in={"status": "successful"}
        )
        return None

    # noinspection PyMethodMayBeStatic
    def message_queue(self, auth_user: dict, message_type: str):
        if auth_user.get("type") == "business":
            trade_name = auth_user.get("profile").get("trade_name")
        else:
            trade_name = auth_user.get("profile").get("trade_name")
        return trade_name, f"{trade_name}_{message_type}".lower()

    def get_all_email(
        self, auth_user: dict, page_params: Params, query_params: dict
    ) -> paginate:
        return self.email_repository.advance_query(
            keyword=query_params.get("keyword"),
            date_filter={
                "date": query_params.get("date"),
                "min_date": query_params.get("min_date"),
                "max_date": query_params.get("max_date"),
                "column": query_params.get("date_column"),
            },
            sort_param={
                "order": query_params.get("sort_order"),
                "column": query_params.get("sort_by"),
            },
            filter_params=remove_none_fields({"user_id": auth_user.get("id")}),
            paginate_data=True,
            page_params=page_params,
        )

    def get_email(self, obj_id: str):
        return self.email_repository.find_by_id(obj_id=obj_id)

    def get_email_batches(self, email_id: str, page_params: Params) -> paginate:
        return self.batch_repository.find_all(
            filter_param={"email_id": email_id},
            paginate_data=True,
            page_params=page_params,
        )

    def get_email_recipients(self, email_id: str, page_params: Params) -> paginate:
        batches = self.batch_repository.find_all(filter_param={"email_id": email_id})
        return self.recipient_repository.advance_query(
            contains={"batch_id": [str(batch.id) for batch in batches]},
            paginate_data=True,
            page_params=page_params,
        )

    def get_recipient_messages(self, mail_address: str, page_params: Params) -> paginate:
        return self.recipient_repository.find_all(
            filter_param={"mail_address": mail_address},
            paginate_data=True,
            page_params=page_params,
        )
