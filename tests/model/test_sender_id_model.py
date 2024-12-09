import pytest

from app.models import SenderIdModel
from tests.base_test_case import BaseTestCase, get_db_session


class TestSmsSenderIdModel(BaseTestCase):
    @pytest.mark.model
    def test_sender_id_model(self, test_app):
        with get_db_session() as db_session:
            result = db_session.query(SenderIdModel).get(self.sender_id_model.id)
        assert result
        assert hasattr(result, "id")
        assert hasattr(result, "user_id")
        assert hasattr(result, "sender")
        assert hasattr(result, "description")
        assert hasattr(result, "is_active")
        assert hasattr(result, "is_pending")
        assert hasattr(result, "approved_at")
        assert hasattr(result, "approved_by")
        assert hasattr(result, "created_by")
        assert hasattr(result, "created_at")
        assert hasattr(result, "updated_by")
        assert hasattr(result, "updated_at")
        assert hasattr(result, "is_deleted")
        assert hasattr(result, "deleted_by")
        assert hasattr(result, "deleted_at")
