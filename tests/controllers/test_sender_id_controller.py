import uuid

import pytest
from fastapi_pagination import Page, Params

from app.core.exceptions import AppException
from app.models import SenderIdModel
from tests.base_test_case import BaseTestCase


class TestSmsSenderIdController(BaseTestCase):
    @pytest.mark.controller
    def test_create_sender_id(self, test_app):
        result = self.sender_id_controller.add_sender_id(
            auth_user=self.mock_decode_token(self.sender_id_model.user_id),
            obj_data=self.sender_id_test_data.add_sender_id,
        )
        assert result
        assert isinstance(result, SenderIdModel)

    @pytest.mark.controller
    def test_get_all_sender_id(self, test_app):
        result = self.sender_id_controller.get_all_sender_id(
            page_params=Params(),
            auth_user=self.mock_decode_token(self.sender_id_model.user_id),
            query_params={},
        )
        assert result
        assert isinstance(result, Page)
        assert isinstance(result.items, list)

    @pytest.mark.controller
    def test_delete_sender_id(self, test_app):
        result = self.sender_id_controller.delete_sender_id(
            auth_user=self.mock_decode_token(self.sender_id_model.user_id),
            obj_id=self.sender_id_model.id,
        )
        assert result is None

    @pytest.mark.controller
    def test_delete_sender_id_notfound_exc(self, test_app):
        with pytest.raises(AppException.NotFoundException) as not_found:
            self.sender_id_controller.delete_sender_id(
                auth_user=self.mock_decode_token(str(uuid.uuid4())),
                obj_id=str(uuid.uuid4()),
            )
        assert not_found.value.status_code == 404

    @pytest.mark.controller
    def test_approve_sender_id(self, test_app):
        result = self.sender_id_controller.approve_sender_id(
            auth_user=self.mock_decode_token(self.sender_id_model.user_id),
            obj_id=self.sender_id_model.id,
        )
        assert result
        assert isinstance(result, SenderIdModel)

    @pytest.mark.controller
    def test_approve_sender_id_exc(self, test_app):
        with pytest.raises(AppException.NotFoundException) as not_found:
            self.sender_id_controller.approve_sender_id(
                auth_user=self.mock_decode_token(self.sender_id_model.user_id),
                obj_id=str(uuid.uuid4()),
            )
        assert not_found.value.status_code == 404
