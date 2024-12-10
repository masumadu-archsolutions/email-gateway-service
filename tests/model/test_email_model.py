import pytest

from app.models import EmailModel
from tests.base_test_case import BaseTestCase, get_db_session


class TestEmailModel(BaseTestCase):
    @pytest.mark.model
    def test_email_model(self, test_app):
        with get_db_session() as db_session:
            result = db_session.query(EmailModel).get(self.email_model.id)
        assert result
        assert hasattr(result, "id")
        assert hasattr(result, "user_id")
        assert hasattr(result, "sender_address")
        assert hasattr(result, "sender_name")
        assert hasattr(result, "subject")
        assert hasattr(result, "html_body")
        assert hasattr(result, "text_body")
        assert hasattr(result, "is_scheduled")
        assert hasattr(result, "scheduled_date")
        assert hasattr(result, "type")
        assert hasattr(result, "tags")
        assert hasattr(result, "total_recipients")
        assert hasattr(result, "require_callback")
        assert hasattr(result, "status")
        assert hasattr(result, "created_at")
        assert hasattr(result, "created_at")
        assert hasattr(result, "created_by")
        assert hasattr(result, "updated_at")
        assert hasattr(result, "updated_by")
        assert hasattr(result, "is_deleted")
        assert hasattr(result, "deleted_at")
        assert hasattr(result, "deleted_by")
