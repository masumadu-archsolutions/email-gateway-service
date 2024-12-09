import pytest

from app.models import SmsBatchModel
from tests.base_test_case import BaseTestCase, get_db_session


class TestSmsBatchModel(BaseTestCase):
    @pytest.mark.model
    def test_sms_batch_model(self, test_app):
        with get_db_session() as db_session:
            result = db_session.query(SmsBatchModel).get(self.sms_batch_model.id)
        assert result
        assert hasattr(result, "id")
        assert hasattr(result, "sms_id")
        assert hasattr(result, "total_recipients")
        assert hasattr(result, "status")
        assert hasattr(result, "status")
        assert hasattr(result, "created_at")
        assert hasattr(result, "created_by")
        assert hasattr(result, "updated_at")
        assert hasattr(result, "updated_by")
        assert hasattr(result, "is_deleted")
        assert hasattr(result, "deleted_at")
        assert hasattr(result, "deleted_by")
