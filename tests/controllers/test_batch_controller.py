import pytest

from tests.base_test_case import BaseTestCase


class TestSmsTaskController(BaseTestCase):
    @pytest.mark.controller
    def test_create_email_batch(self, test_app):
        result = self.batch_controller.create_email_batch(
            obj_data=self.email_test_data.email_batch,
        )
        assert result is None
