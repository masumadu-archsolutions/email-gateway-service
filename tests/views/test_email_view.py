from unittest import mock

import pytest

from app.api.api_v1.endpoints.email_view import email_base_url
from tests.base_test_case import BaseTestCase


@mock.patch("quantum_notify_auth.inter_service_request.DataRequest.http_request")
class TestSmsView(BaseTestCase):
    @pytest.mark.view
    def test_send_email(self, mock_service_request, test_app):
        with test_app as test_client:
            mock_service_request.return_value = self.user_service_find_user(
                user_id=str(self.account_model.user_id)
            )
            response = test_client.post(
                f"{email_base_url}/send",
                headers=self.headers,
                json=self.email_test_data.send_email(
                    type_=self.message_type_model.type,
                    sender=self.account_model.mail_address,
                ),
            )
        response_data = response.json()
        assert response_data
        assert response.status_code == 200
        assert isinstance(response_data, dict)

    @pytest.mark.view
    def test_get_all_email(self, mock_service_request, test_app):
        with test_app as test_client:
            mock_service_request.return_value = self.user_service_find_user(
                user_id=str(self.email_model.user_id)
            )
            response = test_client.get(
                f"{email_base_url}/messages", headers=self.headers
            )
        response_data = response.json()
        assert response_data
        assert response.status_code == 200
        assert isinstance(response_data, dict)

    @pytest.mark.view
    def test_get_email(self, mock_service_request, test_app):
        with test_app as test_client:
            mock_service_request.return_value = self.user_service_find_user(
                user_id=str(self.email_model.user_id)
            )
            response = test_client.get(
                f"{email_base_url}/{self.email_model.id}/message", headers=self.headers
            )
        response_data = response.json()
        assert response_data
        assert response.status_code == 200
        assert isinstance(response_data, dict)

    @pytest.mark.view
    def test_get_email_batch(self, mock_service_request, test_app):
        with test_app as test_client:
            mock_service_request.return_value = self.user_service_find_user(
                user_id=str(self.email_model.user_id)
            )
            response = test_client.get(
                f"{email_base_url}/{self.email_model.id}/batches",
                headers=self.headers,
            )
        response_data = response.json()
        assert response_data
        assert response.status_code == 200
        assert isinstance(response_data, dict)

    @pytest.mark.view
    def test_get_email_recipient(self, mock_service_request, test_app):
        with test_app as test_client:
            mock_service_request.return_value = self.user_service_find_user(
                user_id=str(self.email_model.user_id)
            )
            response = test_client.get(
                f"{email_base_url}/{self.email_model.id}/recipients",
                headers=self.headers,
            )
        response_data = response.json()
        assert response_data
        assert response.status_code == 200
        assert isinstance(response_data, dict)

    @pytest.mark.view
    def test_get_recipient_message(self, mock_service_request, test_app):
        with test_app as test_client:
            mock_service_request.return_value = self.user_service_find_user(
                user_id=str(self.email_model.user_id)
            )
            response = test_client.get(
                f"{email_base_url}/recipient/{self.email_recipient_model.mail_address}/messages",  # noqa
                headers=self.headers,
            )
        response_data = response.json()
        assert response_data
        assert response.status_code == 200
        assert isinstance(response_data, dict)
