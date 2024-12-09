import os

import fakeredis
import pytest
from fastapi.testclient import TestClient

from app import constants
from app.controllers.v1 import (
    MessageTypeController,
    SenderIdController,
    SmsBatchController,
    SmsController,
)
from app.core.database import Base, engine, get_db_session
from app.models import (
    MessageTypeModel,
    RecipientModel,
    SenderIdModel,
    SmsBatchModel,
    SmsModel,
)
from app.repositories import (
    MessageTypeRepository,
    RecipientRepository,
    SenderIdRepository,
    SmsBatchRepository,
    SmsRepository,
)
from tests.data import MessageTypeTestData, SenderIdTestData, SmsTestData
from tests.utils import MockSideEffects


@pytest.mark.usefixtures("app")
class BaseTestCase(MockSideEffects):
    @pytest.fixture
    def test_app(self, app, mocker):
        app_env = os.getenv("APP_ENV")
        assert app_env == constants.TESTING_ENVIRONMENT, "set APP_ENV=testing"
        self.access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"  # noqa: E501
        self.refresh_token = self.access_token
        self.headers = {"Authorization": f"Bearer {self.access_token}"}
        Base.metadata.drop_all(bind=engine)
        test_client = TestClient(app)
        self.setup_test_data()
        self.setup_patches(mocker)
        self.instantiate_classes(redis_instance=self.redis)
        yield test_client
        Base.metadata.drop_all(bind=engine)

    def setup_test_data(self):
        Base.metadata.create_all(bind=engine)
        self.sms_test_data = SmsTestData()
        self.sms_model = SmsModel(**self.sms_test_data.existing_sms)
        self.commit_data_model(self.sms_model)
        self.sms_batch_model = SmsBatchModel(**self.sms_test_data.existing_sms_task)
        self.commit_data_model(self.sms_batch_model)
        self.sms_recipient_model = RecipientModel(
            **self.sms_test_data.existing_sms_recipient
        )
        self.commit_data_model(self.sms_recipient_model)
        self.message_type_test_data = MessageTypeTestData()
        self.message_type_model = MessageTypeModel(
            **self.message_type_test_data.existing_type
        )
        self.commit_data_model(self.message_type_model)
        self.sender_id_test_data = SenderIdTestData()
        self.sender_id_model = SenderIdModel(
            **self.sender_id_test_data.existing_sender_id
        )
        self.commit_data_model(self.sender_id_model)

    def commit_data_model(self, model):
        with get_db_session() as db_session:
            db_session.add(model)
            db_session.commit()
            db_session.refresh(model)

    def instantiate_classes(self, redis_instance):
        self.sms_repository = SmsRepository()
        self.sms_batch_repository = SmsBatchRepository()
        self.recipient_repository = RecipientRepository()
        self.message_type_repository = MessageTypeRepository()
        self.sender_id_repository = SenderIdRepository()
        self.message_type_controller = MessageTypeController(
            message_type_repository=self.message_type_repository,
            redis_service=redis_instance,
        )
        self.sender_id_controller = SenderIdController(
            sender_id_repository=self.sender_id_repository, redis_service=redis_instance
        )
        self.sms_batch_controller = SmsBatchController(
            sms_repository=self.sms_repository,
            sms_batch_repository=self.sms_batch_repository,
        )
        self.sms_controller = SmsController(
            sms_repository=self.sms_repository,
            sms_batch_repository=self.sms_batch_repository,
            recipient_repository=self.recipient_repository,
            sender_id_repository=self.sender_id_repository,
            message_type_repository=self.message_type_repository,
            sms_batch_controller=self.sms_batch_controller,
            redis_service=redis_instance,
        )

    def setup_patches(self, mocker, **kwargs):
        self.redis = mocker.patch(
            "app.services.redis_service.redis_conn",
            fakeredis.FakeStrictRedis(decode_responses=True),
        )
        self.jwt_decode = mocker.patch(
            "quantum_notify_auth.util.jwt.decode",
            return_value=self.mock_decode_token(str(self.sms_model.user_id)),
        )
        mocker.patch("app.core.log.MailHandler.send_mail")
        mocker.patch("app.controllers.v1.sms_controller.publish_to_kafka")
        mocker.patch("app.controllers.v1.sms_batch_controller.publish_to_kafka")
