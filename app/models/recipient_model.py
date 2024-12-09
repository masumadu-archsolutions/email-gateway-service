import uuid

import sqlalchemy as sa

from app.core.database import Base, get_db_session

from .base_model import BaseModel
from .batch_model import BatchModel
from .email_model import EmailModel


class RecipientModel(Base, BaseModel):
    __tablename__ = "email_message_recipients"
    id = sa.Column(sa.UUID, primary_key=True, default=uuid.uuid4)
    batch_id = sa.Column(sa.UUID, sa.ForeignKey("email_message_batches.id"), index=True)
    mail_address = sa.Column(sa.String, nullable=False)

    @classmethod
    def bulk_insert(cls, batch_id: str, recipients: list, user_id: str):
        with get_db_session() as db_session:
            db_session.bulk_insert_mappings(
                RecipientModel,
                [
                    dict(
                        mail_address=recipient,
                        batch_id=batch_id,
                        created_by=user_id,
                        updated_by=user_id,
                    )
                    for recipient in recipients
                ],
            )
            db_session.commit()

    @property
    def message(self):
        with get_db_session() as db_session:
            result = (
                db_session.query(EmailModel)
                .join(BatchModel, BatchModel.email_id == EmailModel.id)
                .filter(BatchModel.id == self.batch_id)
                .first()
            )
            return result
