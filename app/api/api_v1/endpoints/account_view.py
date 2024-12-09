import uuid

import pinject
from fastapi import APIRouter, Depends, Request, status
from fastapi_pagination import Page, Params
from quantum_notify_auth import AuthorizeRequest

from app.controllers.v1 import AccountController
from app.repositories import AccountRepository
from app.schema.v1 import (
    AccountQuerySchema,
    AccountSchema,
    CreateAccountSchema,
    UpdateAccountSchema,
)

account_router = APIRouter()
account_base_url = "/email/api/v1/gateway/account"

obj_graph = pinject.new_object_graph(
    modules=None,
    classes=[AccountController, AccountRepository],
)
account_controller: AccountController = obj_graph.provide(AccountController)


@account_router.post(
    "",
    response_model=AccountSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(AuthorizeRequest())],
)
def add_account(payload: CreateAccountSchema, request: Request) -> AccountSchema:
    return account_controller.create_account(
        auth_user=request.state.auth_user, obj_data=payload.model_dump()
    )


@account_router.get(
    "", response_model=Page[AccountSchema], dependencies=[Depends(AuthorizeRequest())]
)
def get_all_accounts(
    request: Request,
    query_params: AccountQuerySchema = Depends(),  # noqa
    pagination: Params = Depends(),  # noqa
) -> Page[AccountSchema]:  # noqa
    return account_controller.get_all_accounts(
        auth_user=request.state.auth_user,
        query_params=query_params.model_dump(),
        page_params=pagination,
    )


@account_router.get(
    "/{account_id}",
    response_model=AccountSchema,
    dependencies=[Depends(AuthorizeRequest())],
)
def get_account(account_id: uuid.UUID, request: Request) -> AccountSchema:
    return account_controller.get_account(obj_id=str(account_id))


@account_router.patch(
    "",
    response_model=AccountSchema,
    dependencies=[Depends(AuthorizeRequest())],
)
def update_account(payload: UpdateAccountSchema, request: Request) -> AccountSchema:
    return account_controller.update_account(obj_data=payload.model_dump())


@account_router.delete(
    "/{account_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(AuthorizeRequest())],
)
def delete_account(account_id: uuid.UUID, request: Request) -> None:
    return account_controller.delete_account(
        auth_user=request.state.auth_user, obj_id=str(account_id)
    )
