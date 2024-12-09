import uuid

import pytest
from fastapi_pagination import Page, Params

from app.core.exceptions import AppException
from app.models import MessageTypeModel
from tests.base_test_case import BaseTestCase


class TestMessageTypeController(BaseTestCase):
    @pytest.mark.controller
    def test_add_type(self, test_app):
        result = self.message_type_controller.add_message_type(
            auth_user=self.mock_decode_token(self.message_type_model.user_id),
            obj_data=self.message_type_test_data.add_type,
        )

        assert result
        assert isinstance(result, MessageTypeModel)

    @pytest.mark.controller
    def test_get_all_type(self, test_app):
        result = self.message_type_controller.get_all_message_type(
            auth_user=self.mock_decode_token(self.message_type_model.user_id),
            query_params={},
            page_params=Params(),
        )
        assert result
        assert isinstance(result, Page)
        assert isinstance(result.items, list)

    @pytest.mark.controller
    def test_delete_type(self, test_app):
        result = self.message_type_controller.delete_message_type(
            auth_user=self.mock_decode_token(self.message_type_model.user_id),
            obj_id=self.message_type_model.id,
        )
        assert result is None

    @pytest.mark.controller
    def test_delete_type_notfound_exc(self, test_app):
        with pytest.raises(AppException.NotFoundException) as not_found:
            self.message_type_controller.delete_message_type(
                auth_user=self.mock_decode_token(str(uuid.uuid4())),
                obj_id=str(uuid.uuid4()),
            )
        assert not_found.value.status_code == 404

    @pytest.mark.controller
    def test_activate_type(self, test_app):
        result = self.message_type_controller.activate_message_type(
            auth_user=self.mock_decode_token(self.message_type_model.user_id),
            obj_id=self.message_type_model.id,
        )

        assert result
        assert isinstance(result, MessageTypeModel)

    @pytest.mark.controller
    def test_verify_type(self, test_app):
        result = self.message_type_controller.verify_message_type(
            message_type=self.message_type_model.type,
        )
        assert result
        assert isinstance(result, MessageTypeModel)
