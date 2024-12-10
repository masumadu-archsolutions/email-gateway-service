class EmailTestData:
    @property
    def existing_email(self):
        return {
            "id": "3fa85f64-5717-4562-b3fc-2c963f600fa6",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "sender_address": "example@example.com",
            "sender_name": "name",
            "subject": "subject",
            "type": "type",
            "tags": ["tags"],
            "total_recipients": 1,
            "require_callback": False,
            "created_by": "3fa85f64-5717-4562-b3fc-2c963f600fa6",
            "updated_by": "3fa85f64-5717-4562-b3fc-2c963f600fa6",
        }

    def send_email(self, type_: str, sender: str):
        return {
            "sender": sender,
            "name": "string",
            "recipients": ["user@example.com"],
            "subject": "string",
            "html_body": "string",
            "text_body": "string",
            "type": type_,
            "tags": ["string"],
            "webhook_url": "string",
        }

    @property
    def existing_email_batch(self):
        return {
            "id": "3fa85f64-5717-4562-b3fc-2c963f600fa6",
            "email_id": self.existing_email.get("id"),
            "total_recipients": 1,
            "status": "successful",
            "created_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "updated_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        }

    @property
    def existing_email_recipient(self):
        return {
            "id": "3fa85f64-5717-4562-b3fc-2c963f600fa6",
            "batch_id": self.existing_email_batch.get("id"),
            "mail_address": "test@example.com",
            "created_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "updated_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        }

    @property
    def email_batch(self):
        return {
            "email_id": self.existing_email.get("id"),
            "sender": "newgas",
            "recipients": ["0500228274"],
            "tags": ["order"],
            "type": "otp",
            "message": "string",
            "webhook_url": "https://example.com/webhook",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f600fa6",
        }
