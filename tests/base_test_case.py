import os

import fakeredis
import pytest
from fastapi.testclient import TestClient

from app import constants
from app.controllers.v1 import (
    AccountController,
    BatchController,
    EmailController,
    MessageTypeController,
)
from app.core.database import Base, engine, get_db_session
from app.models import (
    AccountModel,
    BatchModel,
    EmailModel,
    MessageTypeModel,
    RecipientModel,
)
from app.repositories import (
    AccountRepository,
    BatchRepository,
    EmailRepository,
    MessageTypeRepository,
    RecipientRepository,
)
from tests.data import AccountTestData, EmailTestData, MessageTypeTestData
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
        self.email_test_data = EmailTestData()
        self.message_type_test_data = MessageTypeTestData()
        self.account_test_data = AccountTestData()
        self.email_model = EmailModel(**self.email_test_data.existing_email)
        self.commit_data_model(self.email_model)
        self.message_type_model = MessageTypeModel(
            **self.message_type_test_data.existing_type
        )
        self.commit_data_model(self.message_type_model)
        self.batch_model = BatchModel(**self.email_test_data.existing_email_batch)
        self.commit_data_model(self.batch_model)
        self.email_recipient_model = RecipientModel(
            **self.email_test_data.existing_email_recipient
        )
        self.commit_data_model(self.email_recipient_model)
        self.account_model = AccountModel(**self.account_test_data.existing_account)
        self.commit_data_model(self.account_model)

    def commit_data_model(self, model):
        with get_db_session() as db_session:
            db_session.add(model)
            db_session.commit()
            db_session.refresh(model)

    def instantiate_classes(self, redis_instance):
        self.message_type_repository = MessageTypeRepository()
        self.message_type_controller = MessageTypeController(
            message_type_repository=self.message_type_repository,
            redis_service=redis_instance,
        )
        self.email_repository = EmailRepository()
        self.batch_repository = BatchRepository()
        self.recipient_repository = RecipientRepository()
        self.account_repository = AccountRepository()
        self.account_controller = AccountController(
            account_repository=self.account_repository
        )
        self.batch_controller = BatchController(
            email_repository=self.email_repository,
            batch_repository=self.batch_repository,
        )
        self.email_controller = EmailController(
            email_repository=self.email_repository,
            batch_repository=self.batch_repository,
            recipient_repository=self.recipient_repository,
            message_type_repository=self.message_type_repository,
            batch_controller=self.batch_controller,
            account_repository=self.account_repository,
            redis_service=redis_instance,
        )

    def setup_patches(self, mocker, **kwargs):
        self.redis = mocker.patch(
            "app.services.redis_service.redis_conn",
            fakeredis.FakeStrictRedis(decode_responses=True),
        )
        self.jwt_decode = mocker.patch(
            "quantum_notify_auth.util.jwt.decode",
            return_value=self.mock_decode_token(str(self.message_type_model.user_id)),
        )
        mocker.patch("app.core.log.MailHandler.send_mail")
        mocker.patch("app.controllers.v1.email_controller.publish_to_kafka")
        mocker.patch("app.controllers.v1.batch_controller.publish_to_kafka")
