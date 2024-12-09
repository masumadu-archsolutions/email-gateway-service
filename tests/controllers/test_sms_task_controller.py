import pytest

from tests.base_test_case import BaseTestCase


class TestSmsTaskController(BaseTestCase):
    @pytest.mark.controller
    def test_create_sms_task(self, test_app):
        result = self.sms_batch_controller.create_sms_batch(
            obj_data=self.sms_test_data.sms_batch,
        )
        assert result is None
