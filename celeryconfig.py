from config import settings

broker_url = f"amqp://{settings.rmq_user}:{settings.rmq_password}@{settings.rmq_server}:{settings.rmq_port}/{settings.rmq_vhost}"  # noqa
result_backend = (
    f"redis://:{settings.redis_password}@{settings.redis_server}:{settings.redis_port}"
)
broker_transport_options = {"queue_order_strategy": "priority"}
broker_connection_max_retries = 5
