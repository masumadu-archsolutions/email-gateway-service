import json
import os
import sys

import pinject
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from loguru import logger as loguru_logger

# Add "app" root to PYTHONPATH so we can import from app i.e. from app import create_app.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app  # noqa: E402
from app.core.exceptions import AppExceptionCase  # noqa: E402
from config import settings  # noqa: E402

if __name__ == "__main__":
    loguru_logger.info("CONNECTING TO KAFKA SERVER")
    try:
        consumer = KafkaConsumer(
            bootstrap_servers=settings.kafka_bootstrap_servers.split("|"),
            auto_offset_reset="earliest",
            group_id=settings.kafka_consumer_group,
            security_protocol="SASL_PLAINTEXT",
            sasl_mechanism="SCRAM-SHA-256",
            sasl_plain_username=settings.kafka_server_username,
            sasl_plain_password=settings.kafka_server_password,
            enable_auto_commit=False,
        )
    except KafkaError as exc:
        loguru_logger.error(f"KafkaError({exc}) occurred while connecting")
    else:
        subscriptions = settings.kafka_subscriptions.split("|")
        consumer.subscribe(subscriptions)
        loguru_logger.info(f"Topic Subscription List: {subscriptions}")
        loguru_logger.info("AWAITING MESSAGES\n")

        app = create_app()
        # Create Application before importing from app
        from app.controllers.v1 import BatchController
        from app.repositories import BatchRepository, EmailRepository

        for msg in consumer:
            data = json.loads(msg.value)
            email_id = data.get("email_id")
            total = len(data.get("recipients"))
            loguru_logger.info(
                f"EmailRequest[{settings.app_name}({settings.app_env}) | Email{email_id, total} | received]"  # noqa
            )
            obj_graph = pinject.new_object_graph(
                modules=None,
                classes=[
                    BatchController,
                    EmailRepository,
                    BatchRepository,
                ],
            )
            batch_controller: BatchController = obj_graph.provide(BatchController)
            try:
                batch_controller.create_email_batch(obj_data=data)
                loguru_logger.info(
                    f"EmailRequest[{settings.app_name}({settings.app_env}) | Email{email_id, total} | successful]\n"  # noqa
                )
            except AppExceptionCase:
                loguru_logger.info(
                    f"EmailRequest[{settings.app_name}({settings.app_env}) | Email{email_id, total} | failed]"  # noqa
                )
            consumer.commit()
            loguru_logger.info(
                f"EmailRequest[{settings.app_name}({settings.app_env}) | Email{email_id, total} | offset commit successful]"  # noqa
            )
