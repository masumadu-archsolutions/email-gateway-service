from app.constants import MessageTypePriority


class MessageTypeTestData:
    @property
    def existing_type(self):
        return {
            "id": "e1185a35-b1b2-4f42-8a4c-5876d3965e88",
            "type": "otp",
            "priority": MessageTypePriority.high.value,
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "is_active": True,
            "description": "a sample message type",
            "created_by": "e1185a35-b1b2-4f42-8a4c-5876d3965e88",
            "updated_by": "e1185a35-b1b2-4f42-8a4c-5876d3965e88",
        }

    @property
    def add_type(self):
        return {"type": "test", "priority": MessageTypePriority.low.value}
