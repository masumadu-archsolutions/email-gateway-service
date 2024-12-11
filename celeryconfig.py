from config import settings

broker_url = settings.rmq_uri
result_backend = settings.redis_uri
broker_transport_options = {"queue_order_strategy": "priority"}
broker_connection_max_retries = 5
