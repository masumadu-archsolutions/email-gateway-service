import uuid

import pinject
from fastapi import APIRouter, Depends, Request
from fastapi_pagination import Page, Params
from quantum_notify_auth import AuthorizeRequest

from app.controllers.v1 import BatchController, EmailController
from app.repositories import (
    AccountRepository,
    BatchRepository,
    EmailRepository,
    MessageTypeRepository,
    RecipientRepository,
)
from app.schema.v1 import (
    EmailBatchSchema,
    EmailQuerySchema,
    EmailResponseSchema,
    EmailSchema,
    RecipientEmailSchema,
    RecipientSchema,
    SendEmailSchema,
)
from app.services import RedisService

email_router = APIRouter()
email_base_url = "/email/api/v1/gateway"

obj_graph = pinject.new_object_graph(
    modules=None,
    classes=[
        EmailController,
        BatchController,
        EmailRepository,
        RecipientRepository,
        BatchRepository,
        MessageTypeRepository,
        AccountRepository,
        RedisService,
    ],
)
sms_controller: EmailController = obj_graph.provide(EmailController)


@email_router.post(
    "/send",
    response_model=EmailResponseSchema,
    dependencies=[Depends(AuthorizeRequest())],
)
def send_email(payload: SendEmailSchema, request: Request):
    return sms_controller.send_email(
        auth_user=request.state.auth_user, obj_data=payload.model_dump()
    )


@email_router.get(
    "/messages",
    response_model=Page[EmailSchema],
    dependencies=[Depends(AuthorizeRequest())],
)
def get_all_email(
    request: Request,
    query_params: EmailQuerySchema = Depends(),  # noqa
    pagination: Params = Depends(),  # noqa
):
    return sms_controller.get_all_email(
        auth_user=request.state.auth_user,
        page_params=pagination,
        query_params=query_params.model_dump(),
    )


@email_router.get(
    "/{mail_id}/message",
    response_model=EmailSchema,
    dependencies=[Depends(AuthorizeRequest())],
)
def get_email(mail_id: uuid.UUID):
    return sms_controller.get_email(obj_id=str(mail_id))


@email_router.get(
    "/{mail_id}/batches",
    response_model=Page[EmailBatchSchema],
    dependencies=[Depends(AuthorizeRequest())],
)
def get_email_batches(mail_id: uuid.UUID, pagination: Params = Depends()):  # noqa
    return sms_controller.get_email_batches(
        email_id=str(mail_id), page_params=pagination
    )


@email_router.get(
    "/{mail_id}/recipients",
    response_model=Page[RecipientSchema],
    dependencies=[Depends(AuthorizeRequest())],
)
def get_email_recipients(mail_id: uuid.UUID, pagination: Params = Depends()):  # noqa
    return sms_controller.get_email_recipients(
        email_id=str(mail_id), page_params=pagination
    )


@email_router.get(
    "/recipient/{mail_address}/messages",
    response_model=Page[RecipientEmailSchema],
    dependencies=[Depends(AuthorizeRequest())],
)
def get_recipient_messages(mail_address: str, pagination: Params = Depends()):  # noqa
    return sms_controller.get_recipient_messages(
        mail_address=mail_address, page_params=pagination
    )
