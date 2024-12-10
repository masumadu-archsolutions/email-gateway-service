import uuid

import pytest
from fastapi_pagination import Page, Params

from app.core.exceptions import AppException
from app.models import EmailModel
from tests.base_test_case import BaseTestCase


class TestEmailController(BaseTestCase):
    @pytest.mark.controller
    def test_send_email(self, test_app):
        result = self.email_controller.send_email(
            auth_user=self.user_service_find_user(
                user_id=str(self.email_model.user_id)
            ).json(),
            obj_data=self.email_test_data.send_email(
                type_=self.message_type_model.type,
                sender=self.account_model.mail_address,
            ),
        )
        assert result
        assert isinstance(result, dict)

    @pytest.mark.controller
    def test_get_all_email(self, test_app):
        result = self.email_controller.get_all_email(
            auth_user=self.mock_decode_token(self.email_model.user_id),
            page_params=Params(),
            query_params={},
        )

        assert result
        assert isinstance(result, Page)
        assert isinstance(result.items, list)

    @pytest.mark.controller
    def test_get_email(self, test_app):
        result = self.email_controller.get_email(obj_id=self.email_model.id)
        assert result
        assert isinstance(result, EmailModel)

    @pytest.mark.controller
    def test_get_email_notfound_exc(self, test_app):
        with pytest.raises(AppException.NotFoundException) as not_found:
            self.email_controller.get_email(obj_id=str(uuid.uuid4()))
        assert not_found.value.status_code == 404

    @pytest.mark.controller
    def test_get_email_bach(self, test_app):
        result = self.email_controller.get_email_batches(
            email_id=self.email_model.id, page_params=Params()
        )
        assert result
        assert isinstance(result, Page)
        assert isinstance(result.items, list)

    @pytest.mark.controller
    def test_get_email_recipients(self, test_app):
        result = self.email_controller.get_email_recipients(
            email_id=self.email_model.id, page_params=Params()
        )
        assert result
        assert isinstance(result, Page)
        assert isinstance(result.items, list)

    @pytest.mark.controller
    def test_get_recipient_message(self, test_app):
        result = self.email_controller.get_recipient_messages(
            mail_address=self.email_recipient_model.mail_address, page_params=Params()
        )
        assert result
        assert isinstance(result, Page)
        assert isinstance(result.items, list)
