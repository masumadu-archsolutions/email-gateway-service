import pytest

from app.models import RecipientModel
from tests.base_test_case import BaseTestCase, get_db_session


class TestRecipientModel(BaseTestCase):
    @pytest.mark.model
    def test_recipient_model(self, test_app):
        with get_db_session() as db_session:
            result = db_session.query(RecipientModel).get(self.sms_recipient_model.id)
        assert result
        assert hasattr(result, "id")
        assert hasattr(result, "batch_id")
        assert hasattr(result, "phone")
        assert hasattr(result, "created_at")
        assert hasattr(result, "created_by")
        assert hasattr(result, "updated_at")
        assert hasattr(result, "updated_by")
        assert hasattr(result, "is_deleted")
        assert hasattr(result, "deleted_at")
        assert hasattr(result, "deleted_by")
