import base64
import uuid

import sqlalchemy as sa
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from app.core.database import Base

from .base_model import BaseModel


class AccountModel(Base, BaseModel):
    __tablename__ = "email_accounts"
    id = sa.Column(sa.UUID, primary_key=True, default=uuid.uuid4)
    user_id = sa.Column(sa.UUID, nullable=False, index=True)
    mail_address = sa.Column(sa.String, unique=True, nullable=False, index=True)
    sender_name = sa.Column(sa.String, nullable=False)
    _password = sa.Column("password", sa.String, nullable=False)
    is_default = sa.Column(sa.Boolean, nullable=False, default=False)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        # reminder: generate a key for encrypting password
        key = AccountModel.generate_key_from_string(
            salt=self.mail_address, passphrase=self.mail_address
        )
        # reminder: encrypt password
        self._password = AccountModel.encrypt_text(key=key, text=value)

    # noinspection PyMethodMayBeStatic
    @staticmethod
    def generate_key_from_string(salt, passphrase):
        # reminder: generate a passphrase and salt for encryption key
        passphrase = passphrase.encode("utf-8").lower()
        salt = salt.encode("utf-8").upper()
        # reminder: derive the key using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend(),
        )
        key = kdf.derive(passphrase)
        # reminder: return a url-safe base64-encoded key as a string
        return base64.urlsafe_b64encode(key).decode("utf-8")

    # noinspection PyMethodMayBeStatic
    @staticmethod
    def encrypt_text(key: str, text: str):
        cipher_suite = Fernet(key)
        raw_encryption = cipher_suite.encrypt(text.encode("utf-8"))
        return base64.urlsafe_b64encode(raw_encryption).decode("utf-8")

    @staticmethod
    def decrypt_text(passphrase: str, encrypted_text: str):
        # reminder: generate key for decrypting text
        key = AccountModel.generate_key_from_string(
            salt=passphrase, passphrase=passphrase
        )
        cipher_suite = Fernet(key)
        convert_to_byte = base64.urlsafe_b64decode(encrypted_text.encode("utf-8"))
        return cipher_suite.decrypt(convert_to_byte).decode("utf-8")
