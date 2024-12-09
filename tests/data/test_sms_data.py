import uuid


class SmsTestData:
    @property
    def existing_sms(self):
        return {
            "id": "3fa85f64-5717-4562-b3fc-2c963f600fa6",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "sender": "newgas",
            "message": "string",
            "type": "otp",
            "is_scheduled": True,
            "scheduled_date": "2023-07-10T15:41:23.136Z",
            "total_recipients": 1,
            "status": "successful",
            "created_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "updated_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        }

    def send_sms(self, type_: str, sender: str):
        return {
            "sender": sender,
            "recipients": ["0500228274"],
            "tags": ["order"],
            "type": type_,
            "message": "string",
            "webhook_url": "https://example.com/webhook",
        }

    def send_sms_odoo(self, type_: str, sender: str):
        return {
            "sender": sender,
            "recipients": [{"uuid": str(uuid.uuid4()), "number": "0500228274"}],
            "tags": ["order"],
            "type": type_,
            "message": "string",
            "webhook_url": "https://example.com/webhook",
        }

    @property
    def existing_sms_task(self):
        return {
            "id": "3fa85f64-5717-4562-b3fc-2c963f600fa6",
            "sms_id": self.existing_sms.get("id"),
            "total_recipients": 1,
            "status": "successful",
            "created_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "updated_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        }

    @property
    def existing_sms_recipient(self):
        return {
            "id": "3fa85f64-5717-4562-b3fc-2c963f600fa6",
            "batch_id": self.existing_sms_task.get("id"),
            "phone": "0200000000",
            "created_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "updated_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        }

    @property
    def sms_batch(self):
        return {
            "sms_id": "3fa85f64-5717-4562-b3fc-2c963f600fa6",
            "sender": "newgas",
            "recipients": ["0500228274"],
            "tags": ["order"],
            "type": "otp",
            "message": "string",
            "webhook_url": "https://example.com/webhook",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f600fa6",
        }
