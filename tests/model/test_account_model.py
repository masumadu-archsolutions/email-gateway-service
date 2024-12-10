import pytest

from app.models import AccountModel
from tests.base_test_case import BaseTestCase, get_db_session


class TestAccountModel(BaseTestCase):
    @pytest.mark.model
    def test_account_model(self, test_app):
        with get_db_session() as db_session:
            result = db_session.query(AccountModel).get(self.account_model.id)
        assert result
        assert hasattr(result, "id")
        assert hasattr(result, "user_id")
        assert hasattr(result, "mail_address")
        assert hasattr(result, "sender_name")
        assert hasattr(result, "_password")
        assert hasattr(result, "is_default")
        assert hasattr(result, "created_at")
        assert hasattr(result, "created_by")
        assert hasattr(result, "updated_by")
        assert hasattr(result, "updated_at")
        assert hasattr(result, "is_deleted")
        assert hasattr(result, "deleted_by")
        assert hasattr(result, "deleted_at")
