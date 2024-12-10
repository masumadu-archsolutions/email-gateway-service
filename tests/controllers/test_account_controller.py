import uuid

import pytest
from fastapi_pagination import Page, Params

from app.core.exceptions import AppException
from app.models import AccountModel
from tests.base_test_case import BaseTestCase


class TestAccountController(BaseTestCase):
    @pytest.mark.controller
    def test_create_account(self, test_app):
        result = self.account_controller.create_account(
            auth_user=self.mock_decode_token(self.email_model.user_id),
            obj_data=self.account_test_data.new_account,
        )
        assert result
        assert isinstance(result, AccountModel)

    @pytest.mark.controller
    def test_get_all_accounts(self, test_app):
        result = self.account_controller.get_all_accounts(
            auth_user=self.mock_decode_token(self.email_model.user_id),
            query_params={},
            page_params=Params(),
        )
        assert result
        assert isinstance(result, Page)
        assert isinstance(result.items, list)

    @pytest.mark.controller
    def test_get_account(self, test_app):
        result = self.account_controller.get_account(obj_id=self.account_model.id)
        assert result
        assert isinstance(result, AccountModel)

    @pytest.mark.controller
    def test_get_account_notfound_exc(self, test_app):
        with pytest.raises(AppException.NotFoundException) as not_found:
            self.account_controller.get_account(obj_id=str(uuid.uuid4()))
        assert not_found.value.status_code == 404

    @pytest.mark.controller
    def test_update_account(self, test_app):
        result = self.account_controller.update_account(
            obj_data=self.account_test_data.update_account,
        )
        assert result
        assert isinstance(result, AccountModel)

    @pytest.mark.controller
    def test_update_account_notfound_exc(self, test_app):
        with pytest.raises(AppException.NotFoundException) as not_found:
            self.account_controller.update_account(
                obj_data=self.account_test_data.invalid_update,
            )
        assert not_found.value.status_code == 404

    @pytest.mark.controller
    def test_delete_account(self, test_app):
        result = self.account_controller.delete_account(
            auth_user=self.mock_decode_token(self.account_model.user_id),
            obj_id=self.account_model.id,
        )
        assert result is None

    @pytest.mark.controller
    def test_delete_account_notfound_exc(self, test_app):
        with pytest.raises(AppException.NotFoundException) as not_found:
            self.account_controller.delete_account(
                auth_user=self.mock_decode_token(str(uuid.uuid4())),
                obj_id=str(uuid.uuid4()),
            )
        assert not_found.value.status_code == 404
