import uuid


class AccountTestData:
    @property
    def existing_account(self):
        return {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "mail_address": "user@example.com",
            "sender_name": "string",
            "password": "account_password",
            "is_default": True,
            "created_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "created_at": "2023-07-24T09:59:30.337Z",
            "updated_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "updated_at": "2023-07-24T09:59:30.337Z",
            "is_deleted": False,
            "deleted_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "deleted_at": "2023-07-24T09:59:30.337Z",
        }

    @property
    def new_account(self):
        return {
            "email_address": "example@example.com",
            "sender_name": "string",
            "password": "string",
            "is_default": False,
        }

    @property
    def update_account(self):
        return {
            "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "sender_name": "string",
            "password": "1234",
            "is_default": True,
        }

    @property
    def invalid_update(self):
        return {
            "account_id": uuid.uuid4(),
            "sender_name": "wrong_sender",
            "password": "12345",
            "is_default": True,
        }
