class MockResponse:
    def __init__(self, status_code=200, json=None, text="", content=b""):
        self.status_code = status_code
        self._json = json
        self._text = text
        self._content = content

    def json(self):
        return self._json

    @property
    def text(self):
        return self._text

    @property
    def content(self):
        return self._content


class MockSideEffects:
    # noinspection PyMethodMayBeStatic
    def mock_decode_token(self, id: str):
        return {"id": id, "preferred_username": id}

    def user_service_find_user(self, *args, **kwargs):
        return MockResponse(
            status_code=200,
            json={
                "id": kwargs.get("user_id"),
                "email": "user@example.com",
                "phone": "string",
                "avatar": "string",
                "auth_provider_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "is_email_verified": True,
                "is_phone_verified": True,
                "api_key_enabled": True,
                "last_active": "2023-08-31T12:14:37.325Z",
                "type": kwargs.get("type") or "business",
                "comment": {},
                "status": "inactive",
                "created_at": "2023-08-31T12:14:37.325Z",
                "updated_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "updated_at": "2023-08-31T12:14:37.325Z",
                "is_deleted": True,
                "deleted_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "deleted_at": "2023-08-31T12:14:37.325Z",
                "profile": {"trade_name": "newgas"},
                "role": {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "name": kwargs.get("role"),
                    "description": "string",
                    "created_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "created_at": "2023-08-31T12:14:37.325Z",
                    "updated_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "updated_at": "2023-08-31T12:14:37.325Z",
                    "is_deleted": True,
                    "deleted_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "deleted_at": "2023-08-31T12:14:37.325Z",
                },
            },
        )
