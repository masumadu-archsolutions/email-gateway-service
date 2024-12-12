from app.constants import EMAIL_BATCH_SIZE
from app.core.exceptions import AppException
from app.models import AccountModel, RecipientModel
from app.producer import publish_to_kafka
from app.repositories import BatchRepository, EmailRepository
from app.utils import load_in_batches


class BatchController:
    def __init__(
        self,
        email_repository: EmailRepository,
        batch_repository: BatchRepository,
    ):
        self.email_repository = email_repository
        self.batch_repository = batch_repository

    # noinspection PyMethodMayBeStatic
    def create_email_batch(self, obj_data: dict):
        recipients = obj_data.get("recipients")
        user_id = obj_data.get("user_id")
        for batch in load_in_batches(data=recipients, size=EMAIL_BATCH_SIZE):
            result = self.batch_repository.create(
                obj_in={
                    "email_id": obj_data.get("email_id"),
                    "total_recipients": len(batch),
                    "created_by": user_id,
                    "updated_by": user_id,
                }
            )
            RecipientModel.bulk_insert(
                batch_id=str(result.id),
                recipients=batch,
                user_id=user_id,
            )
            self.publish_to_queue(
                obj_data=obj_data,
                recipients=batch,
                user_id=user_id,
                batch_id=str(result.id),
            )
            self.batch_repository.update_by_id(
                obj_id=result.id, obj_in={"status": "successful"}
            )
            self.email_repository.update_by_id(
                obj_id=obj_data.get("email_id"), obj_in={"status": "successful"}
            )
        return None

    # noinspection PyMethodMayBeStatic
    def publish_to_queue(
        self, obj_data: dict, recipients: list, user_id: str, batch_id: str
    ):
        from app.tasks import publish_to_rabbitmq

        try:
            publish_to_rabbitmq(
                queue=obj_data.get("queue"),
                email_data={
                    "email_id": obj_data.get("email_id"),
                    "sender": obj_data.get("sender"),
                    "name": obj_data.get("name"),
                    "subject": obj_data.get("subject"),
                    "password": obj_data.get("password"),
                    "key": AccountModel.generate_key_from_string(
                        passphrase=obj_data.get("sender")
                    ),
                    "recipients": recipients,
                    "html": obj_data.get("html_body"),
                    "text": obj_data.get("text_body"),
                    "type": obj_data.get("type"),
                    "priority": obj_data.get("priority"),
                    "webhook_url": obj_data.get("webhook_url"),
                    "user_id": user_id,
                    "batch_id": batch_id,
                    "queue": obj_data.get("queue"),
                },
            )
        except AppException.InternalServerException:
            publish_to_kafka(
                topic=obj_data.get("topic"),
                value={
                    "email_id": obj_data.get("email_id"),
                    "sender": obj_data.get("sender"),
                    "name": obj_data.get("name"),
                    "subject": obj_data.get("subject"),
                    "password": obj_data.get("password"),
                    "recipients": recipients,
                    "html": obj_data.get("html_body"),
                    "text": obj_data.get("text_body"),
                    "type": obj_data.get("type"),
                    "priority": obj_data.get("priority"),
                    "webhook_url": obj_data.get("webhook_url"),
                    "user_id": user_id,
                    "topic": obj_data.get("topic"),
                    "queue": obj_data.get("queue"),
                },
            )
        return None
