import pytest

from app.models import SmsModel
from tests.base_test_case import BaseTestCase, get_db_session


class TestSmsModel(BaseTestCase):
    @pytest.mark.model
    def test_bulk_sms_model(self, test_app):
        with get_db_session() as db_session:
            result = db_session.query(SmsModel).get(self.sms_model.id)
        assert result
        assert hasattr(result, "id")
        assert hasattr(result, "user_id")
        assert hasattr(result, "sender")
        assert hasattr(result, "message")
        assert hasattr(result, "tags")
        assert hasattr(result, "type")
        assert hasattr(result, "is_scheduled")
        assert hasattr(result, "scheduled_date")
        assert hasattr(result, "status")
        assert hasattr(result, "created_at")
        assert hasattr(result, "created_by")
        assert hasattr(result, "updated_at")
        assert hasattr(result, "updated_by")
        assert hasattr(result, "is_deleted")
        assert hasattr(result, "deleted_at")
        assert hasattr(result, "deleted_by")
