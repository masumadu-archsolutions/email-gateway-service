from fastapi import FastAPI

from .endpoints import (
    account_base_url,
    account_router,
    email_base_url,
    email_router,
    message_type_base_url,
    message_type_router,
)


def init_api_v1(app: FastAPI):
    app.include_router(router=email_router, tags=["Email"], prefix=email_base_url)
    app.include_router(router=account_router, tags=["Account"], prefix=account_base_url)
    app.include_router(
        router=message_type_router,
        tags=["Email Message Type"],
        prefix=message_type_base_url,
    )
