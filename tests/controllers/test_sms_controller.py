import uuid

import pytest
from fastapi_pagination import Page, Params

from app.core.exceptions import AppException
from app.models import SmsModel
from tests.base_test_case import BaseTestCase


class TestSmsController(BaseTestCase):
    @pytest.mark.controller
    def test_send_sms(self, test_app):
        result = self.sms_controller.send_sms(
            auth_user=self.mock_decode_token(self.sms_model.user_id),
            obj_data=self.sms_test_data.send_sms(
                type_=self.message_type_model.type, sender=self.sender_id_model.sender
            ),
        )
        assert result
        assert isinstance(result, dict)

    @pytest.mark.controller
    def test_send_odoo_sms(self, test_app):
        result = self.sms_controller.send_odoo_sms(
            auth_user=self.mock_decode_token(self.sms_model.user_id),
            obj_data=self.sms_test_data.send_sms_odoo(
                type_=self.message_type_model.type, sender=self.sender_id_model.sender
            ),
        )
        assert result
        assert isinstance(result, dict)

    @pytest.mark.controller
    def test_get_all_sms(self, test_app):
        result = self.sms_controller.get_all_sms(
            auth_user=self.mock_decode_token(self.sms_model.user_id),
            page_params=Params(),
            query_params={},
        )

        assert result
        assert isinstance(result, Page)
        assert isinstance(result.items, list)

    @pytest.mark.controller
    def test_get_sms(self, test_app):
        result = self.sms_controller.get_sms(obj_id=self.sms_model.id)
        assert result
        assert isinstance(result, SmsModel)

    @pytest.mark.controller
    def test_get_sms_notfound_exc(self, test_app):
        with pytest.raises(AppException.NotFoundException) as not_found:
            self.sms_controller.get_sms(obj_id=str(uuid.uuid4()))
        assert not_found.value.status_code == 404

    @pytest.mark.controller
    def test_get_sms_task(self, test_app):
        result = self.sms_controller.get_sms_batches(
            sms_id=self.sms_model.id, page_params=Params()
        )
        assert result
        assert isinstance(result, Page)
        assert isinstance(result.items, list)

    @pytest.mark.controller
    def test_get_sms_recipients(self, test_app):
        result = self.sms_controller.get_sms_recipients(
            sms_id=self.sms_model.id, page_params=Params()
        )
        assert result
        assert isinstance(result, Page)
        assert isinstance(result.items, list)

    @pytest.mark.controller
    def test_get_recipient_message(self, test_app):
        result = self.sms_controller.get_recipient_messages(
            phone=self.sms_recipient_model.phone, page_params=Params()
        )
        assert result
        assert isinstance(result, Page)
        assert isinstance(result.items, list)
