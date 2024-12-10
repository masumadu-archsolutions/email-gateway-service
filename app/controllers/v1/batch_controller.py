from app.constants import EMAIL_BATCH_SIZE, KAFKA_TOPIC_PREFIX
from app.models import RecipientModel
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
        kafka_topic = f"{obj_data.get('trade_name')}_{KAFKA_TOPIC_PREFIX}_{obj_data.get('type')}_batch".upper()  # noqa
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
            publish_to_kafka(
                kafka_topic,
                {
                    "email_id": obj_data.get("email_id"),
                    "sender": obj_data.get("sender"),
                    "recipients": batch,
                    "message": obj_data.get("message"),
                    "type": obj_data.get("type"),
                    "priority": obj_data.get("priority"),
                    "webhook_url": obj_data.get("webhook_url"),
                    "user_id": user_id,
                    "batch_id": str(result.id),
                    "topic": kafka_topic,
                    "queue": obj_data.get("queue"),
                },
            )
            self.batch_repository.update_by_id(
                obj_id=result.id, obj_in={"status": "successful"}
            )
            self.email_repository.update_by_id(
                obj_id=obj_data.get("email_id"), obj_in={"status": "successful"}
            )
        return None
