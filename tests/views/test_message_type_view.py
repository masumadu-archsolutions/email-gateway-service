from unittest import mock

import pytest

from app.api.api_v1.endpoints import message_type_base_url
from tests.base_test_case import BaseTestCase


@mock.patch("quantum_notify_auth.inter_service_request.DataRequest.http_request")
class TestMessageTypeView(BaseTestCase):
    @pytest.mark.view
    def test_message_type(self, mock_service_request, test_app):
        with test_app as test_client:
            mock_service_request.return_value = self.user_service_find_user(
                user_id=str(self.message_type_model.user_id)
            )
            response = test_client.post(
                f"{message_type_base_url}",
                headers=self.headers,
                json=self.message_type_test_data.add_type,
            )
        response_data = response.json()
        assert response_data
        assert response.status_code == 201
        assert isinstance(response_data, dict)

    @pytest.mark.view
    def test_get_all_message(self, mock_service_request, test_app):
        with test_app as test_client:
            mock_service_request.return_value = self.user_service_find_user(
                user_id=str(self.message_type_model.user_id)
            )
            response = test_client.get(f"{message_type_base_url}", headers=self.headers)
        response_data = response.json()
        assert response_data
        assert response.status_code == 200
        assert isinstance(response_data, dict)

    @pytest.mark.view
    def test_delete_type(self, mock_service_request, test_app):
        with test_app as test_client:
            mock_service_request.return_value = self.user_service_find_user(
                user_id=str(self.message_type_model.user_id)
            )
            response = test_client.delete(
                f"{message_type_base_url}/{self.message_type_model.id}",
                headers=self.headers,
            )
        assert response.status_code == 204
        assert response.content == b""

    @pytest.mark.view
    def test_activate_type(self, mock_service_request, test_app):
        with test_app as test_client:
            mock_service_request.return_value = self.user_service_find_user(
                user_id=str(self.message_type_model.user_id)
            )
            response = test_client.patch(
                f"{message_type_base_url}/{self.message_type_model.id}/activate",
                headers=self.headers,
            )
        response_data = response.json()
        assert response_data
        assert response.status_code == 200
        assert isinstance(response_data, dict)

    @pytest.mark.view
    def test_verify_type(self, mock_service_request, test_app):
        with test_app as test_client:
            mock_service_request.return_value = self.user_service_find_user(
                user_id=str(self.message_type_model.user_id)
            )
            response = test_client.get(
                f"{message_type_base_url}/{self.message_type_model.type}/verify",  # noqa
                headers=self.headers,
            )
        response_data = response.json()
        assert response_data
        assert response.status_code == 200
        assert isinstance(response_data, dict)
