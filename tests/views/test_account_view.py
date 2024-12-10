from unittest import mock

import pytest
from quantum_notify_auth.util import AccountRoleEnum

from app.api.api_v1.endpoints import account_base_url
from tests.base_test_case import BaseTestCase


@mock.patch("quantum_notify_auth.inter_service_request.DataRequest.http_request")
class TestAccountView(BaseTestCase):
    @pytest.mark.view
    def test_create_account(self, mock_service_request, test_app):
        with test_app as test_client:
            mock_service_request.return_value = self.user_service_find_user(
                user_id=str(self.account_model.user_id),
                role=AccountRoleEnum.user.value,
            )
            response = test_client.post(
                f"{account_base_url}",
                headers=self.headers,
                json=self.account_test_data.new_account,
            )
        response_data = response.json()
        assert response_data
        assert response.status_code == 201
        assert isinstance(response_data, dict)

    @pytest.mark.view
    def test_get_all_accounts(self, mock_service_request, test_app):
        with test_app as test_client:
            mock_service_request.return_value = self.user_service_find_user(
                user_id=str(self.account_model.user_id),
                role=AccountRoleEnum.user.value,
            )
            response = test_client.get(account_base_url, headers=self.headers)
        response_data = response.json()
        assert response_data
        assert response.status_code == 200
        assert isinstance(response_data, dict)

    @pytest.mark.view
    def test_get_account(self, mock_service_request, test_app):
        with test_app as test_client:
            mock_service_request.return_value = self.user_service_find_user(
                user_id=str(self.account_model.user_id),
                role=AccountRoleEnum.user.value,
            )
            response = test_client.get(
                f"{account_base_url}/{self.account_model.id}",
                headers=self.headers,
            )
        response_data = response.json()
        assert response_data
        assert response.status_code == 200
        assert isinstance(response_data, dict)

    @pytest.mark.view
    def test_update_account(self, mock_service_request, test_app):
        with test_app as test_client:
            mock_service_request.return_value = self.user_service_find_user(
                user_id=str(self.account_model.user_id),
                role=AccountRoleEnum.user.value,
            )
            response = test_client.patch(
                f"{account_base_url}",
                headers=self.headers,
                json=self.account_test_data.update_account,
            )
        response_data = response.json()
        assert response_data
        assert response.status_code == 200
        assert isinstance(response_data, dict)

    @pytest.mark.view
    def test_delete_account(self, mock_service_request, test_app):
        with test_app as test_client:
            mock_service_request.return_value = self.user_service_find_user(
                user_id=str(self.account_model.user_id),
                role=AccountRoleEnum.user.value,
            )
            response = test_client.delete(
                f"{account_base_url}/{self.account_model.id}",
                headers=self.headers,
            )
        assert response.status_code == 204
        assert response.content == b""
