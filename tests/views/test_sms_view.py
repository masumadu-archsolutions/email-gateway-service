from unittest import mock

import pytest

from app.api.api_v1.endpoints.email_view import sms_base_url
from tests.base_test_case import BaseTestCase


@mock.patch("quantum_notify_auth.inter_service_request.DataRequest.http_request")
class TestSmsView(BaseTestCase):
    @pytest.mark.view
    def test_send_sms(self, mock_service_request, test_app):
        with test_app as test_client:
            mock_service_request.return_value = self.user_service_find_user(
                user_id=str(self.sms_model.user_id)
            )
            response = test_client.post(
                f"{sms_base_url}/send",
                headers=self.headers,
                json=self.sms_test_data.send_sms(
                    type_=self.message_type_model.type,
                    sender=self.sender_id_model.sender,
                ),
            )
        response_data = response.json()
        assert response_data
        assert response.status_code == 200
        assert isinstance(response_data, dict)

    @pytest.mark.view
    def test_send_odoo_sms(self, mock_service_request, test_app):
        with test_app as test_client:
            mock_service_request.return_value = self.user_service_find_user(
                user_id=str(self.sms_model.user_id)
            )
            response = test_client.post(
                f"{sms_base_url}/send/odoo",
                headers=self.headers,
                json=self.sms_test_data.send_sms_odoo(
                    type_=self.message_type_model.type,
                    sender=self.sender_id_model.sender,
                ),
            )
        response_data = response.json()
        assert response_data
        assert response.status_code == 200
        assert isinstance(response_data, dict)

    @pytest.mark.view
    def test_get_all_sms(self, mock_service_request, test_app):
        with test_app as test_client:
            mock_service_request.return_value = self.user_service_find_user(
                user_id=str(self.sms_model.user_id)
            )
            response = test_client.get(f"{sms_base_url}/messages", headers=self.headers)
        response_data = response.json()
        assert response_data
        assert response.status_code == 200
        assert isinstance(response_data, dict)

    @pytest.mark.view
    def test_get_sms(self, mock_service_request, test_app):
        with test_app as test_client:
            mock_service_request.return_value = self.user_service_find_user(
                user_id=str(self.sms_model.user_id)
            )
            response = test_client.get(
                f"{sms_base_url}/{self.sms_model.id}/message", headers=self.headers
            )
        response_data = response.json()
        assert response_data
        assert response.status_code == 200
        assert isinstance(response_data, dict)

    @pytest.mark.view
    def test_get_sms_task(self, mock_service_request, test_app):
        with test_app as test_client:
            mock_service_request.return_value = self.user_service_find_user(
                user_id=str(self.sms_model.user_id)
            )
            response = test_client.get(
                f"{sms_base_url}/{self.sms_model.id}/batches",
                headers=self.headers,
            )
        response_data = response.json()
        assert response_data
        assert response.status_code == 200
        assert isinstance(response_data, dict)

    @pytest.mark.view
    def test_get_sms_recipient(self, mock_service_request, test_app):
        with test_app as test_client:
            mock_service_request.return_value = self.user_service_find_user(
                user_id=str(self.sms_model.user_id)
            )
            response = test_client.get(
                f"{sms_base_url}/{self.sms_model.id}/recipients",
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
                user_id=str(self.sms_model.user_id)
            )
            response = test_client.get(
                f"{sms_base_url}/recipient/{self.sms_recipient_model.phone}/messages",
                headers=self.headers,
            )
        response_data = response.json()
        assert response_data
        assert response.status_code == 200
        assert isinstance(response_data, dict)
