from unittest import mock

import pytest

from app.api.api_v1.endpoints import sender_id_base_url
from tests.base_test_case import BaseTestCase


@mock.patch("quantum_notify_auth.inter_service_request.DataRequest.http_request")
class TestSenderIdView(BaseTestCase):
    @pytest.mark.view
    def test_add_sender_id(self, mock_service_request, test_app):
        with test_app as test_client:
            mock_service_request.return_value = self.user_service_find_user(
                user_id=str(self.sender_id_model.user_id)
            )
            response = test_client.post(
                f"{sender_id_base_url}",
                headers=self.headers,
                json=self.sender_id_test_data.add_sender_id,
            )
        response_data = response.json()
        assert response_data
        assert response.status_code == 201
        assert isinstance(response_data, dict)

    @pytest.mark.view
    def test_get_all_sender_id(self, mock_service_request, test_app):
        with test_app as test_client:
            mock_service_request.return_value = self.user_service_find_user(
                user_id=str(self.sender_id_model.user_id)
            )
            response = test_client.get(
                f"{sender_id_base_url}",
                headers=self.headers,
            )
        response_data = response.json()
        assert response_data
        assert response.status_code == 200
        assert isinstance(response_data, dict)

    @pytest.mark.view
    def test_delete_sender_i(self, mock_service_request, test_app):
        with test_app as test_client:
            mock_service_request.return_value = self.user_service_find_user(
                user_id=str(self.sender_id_model.user_id)
            )
            response = test_client.delete(
                f"{sender_id_base_url}/{self.sender_id_model.id}",
                headers=self.headers,
            )
        assert response.status_code == 204
        assert response.content == b""

    @pytest.mark.view
    def test_approve_sender_id(self, mock_service_request, test_app):
        with test_app as test_client:
            mock_service_request.return_value = self.user_service_find_user(
                user_id=str(self.sender_id_model.user_id)
            )
            response = test_client.patch(
                f"{sender_id_base_url}/{self.sender_id_model.id}",
                headers=self.headers,
            )
        response_data = response.json()
        assert response_data
        assert response.status_code == 200
        assert isinstance(response_data, dict)
