# from unittest import mock
#
# import pytest
#
# from app.tasks import high_priority_sms
# from tests.base_test_case import BaseTestCase
#
#
# class TestCeleryTask(BaseTestCase):
#     @pytest.mark.tasks
#     def test_sms_task(self, test_app):
#         with mock.patch("app.providers.gateway_sms_eagle.requests.get") as request:
#             request.side_effect = self.sms_eagle
#             task = high_priority_sms.apply(
#                 kwargs=self.sms_test_data.sms_task(
#                     report_id=self.sms_delivery_report_model.id,
#                     user_id=self.sms_model.user_id,
#                 )
#             )
#         assert task
#         assert task.state == "SUCCESS"
#         assert task.get() is None
