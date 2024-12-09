import uuid

import pinject
from fastapi import APIRouter, Depends, Request, status
from fastapi_pagination import Page, Params
from quantum_notify_auth import AuthorizeRequest

from app.controllers.v1 import MessageTypeController
from app.repositories import MessageTypeRepository
from app.schema.v1 import (
    AddNMessageTypeSchema,
    MessageTypeSchema,
    QueryMessageTypeSchema,
)
from app.services import RedisService

message_type_router = APIRouter()
message_type_base_url = "/email/api/v1/gateway/message-type"

obj_graph = pinject.new_object_graph(
    modules=None,
    classes=[MessageTypeController, MessageTypeRepository, RedisService],
)
message_type_controller: MessageTypeController = obj_graph.provide(MessageTypeController)


@message_type_router.post(
    "",
    response_model=MessageTypeSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(AuthorizeRequest())],
)
def add_message_type(payload: AddNMessageTypeSchema, request: Request):
    return message_type_controller.add_message_type(
        auth_user=request.state.auth_user, obj_data=payload.model_dump()
    )


@message_type_router.get(
    "",
    response_model=Page[MessageTypeSchema],
    dependencies=[Depends(AuthorizeRequest())],
)
def get_all_message_type(
    request: Request,
    query_params: QueryMessageTypeSchema = Depends(),  # noqa
    pagination: Params = Depends(),  # noqa
):
    return message_type_controller.get_all_message_type(
        auth_user=request.state.auth_user,
        query_params=query_params.model_dump(),
        page_params=pagination,
    )


@message_type_router.delete(
    "/{message_type_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(AuthorizeRequest())],
)
def delete_message_type(message_type_id: uuid.UUID, request: Request):
    return message_type_controller.delete_message_type(  # noqa
        auth_user=request.state.auth_user, obj_id=str(message_type_id)
    )


@message_type_router.patch(
    "/{message_type_id}/activate",
    response_model=MessageTypeSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AuthorizeRequest())],
)
def activate_message_type(message_type_id: uuid.UUID, request: Request):
    return message_type_controller.activate_message_type(  # noqa
        auth_user=request.state.auth_user, obj_id=str(message_type_id)
    )


@message_type_router.get(
    "/{message_type}/verify",
    response_model=MessageTypeSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AuthorizeRequest())],
)
def verify_message_type(message_type: str):
    return message_type_controller.verify_message_type(message_type=message_type)
