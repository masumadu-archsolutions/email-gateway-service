from amqp import exceptions as amqp_exc
from kombu import Exchange, Queue
from kombu import exceptions as kombu_exc

from app.celery_app import celery
from app.core.exceptions import AppException


def publish_to_rabbitmq(
    email_data: dict,
    queue: str,
    queue_type: str = "direct",
    task_name: str = "send_email_task",
):
    try:
        celery.send_task(
            task_name,
            kwargs=email_data,
            queue=Queue(
                name=queue,
                exchange=Exchange(queue, type=queue_type),
                routing_key=queue,
            ).name,
        )
    except (kombu_exc.KombuError, amqp_exc.AMQPError) as exc:
        raise AppException.InternalServerException(
            error_message=f"CeleryBrokerError({exc})",
            context=f"CeleryBrokerError({exc})",
        )
