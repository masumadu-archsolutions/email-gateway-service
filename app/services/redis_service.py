import redis
from fastapi.logger import logger
from redis.exceptions import RedisError

from app.core.exceptions import HTTPException, exception_message
from app.core.service_interfaces import CacheServiceInterface
from config import settings

redis_conn = redis.Redis(
    host=settings.redis_server,
    port=settings.redis_port,
    db=0,
    password=f"{settings.redis_password}",
    decode_responses=True,
)


class RedisService(CacheServiceInterface):
    def set(self, name: str, value: str, ex: int = None):
        try:
            redis_conn.set(name=name, value=value, ex=ex)
        except RedisError as exc:
            logger.critical(
                msg=exception_message(
                    error="RedisError", message=str(exc), status_code=500
                )
            )
            raise HTTPException(status_code=500, description=exc)

    def get(self, name: str):
        try:
            data = redis_conn.get(name)
            return data if data else None
        except RedisError as exc:
            logger.critical(
                msg=exception_message(
                    error="RedisError", message=str(exc), status_code=500
                )
            )
            raise HTTPException(status_code=500, description=exc)

    def delete(self, name: str):
        try:
            redis_conn.delete(name)
        except RedisError as exc:
            logger.critical(
                msg=exception_message(
                    error="RedisError", message=str(exc), status_code=500
                )
            )
            raise HTTPException(status_code=500, description=exc)
