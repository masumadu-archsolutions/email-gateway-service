class SenderIdTestData:
    @property
    def existing_sender_id(self):
        return {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "sender": "0500228274",
            "description": "string",
            "is_active": True,
            "is_pending": True,
            "approved_at": "2023-07-11T09:11:23.805Z",
            "approved_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "created_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "created_at": "2023-07-11T09:11:23.805Z",
            "updated_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "updated_at": "2023-07-11T09:11:23.805Z",
            "is_deleted": True,
            "deleted_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "deleted_at": "2023-07-11T09:11:23.805Z",
        }

    @property
    def add_sender_id(self):
        return {"sender": "0500228375", "description": "string"}
