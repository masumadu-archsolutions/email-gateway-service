import pytest
from fakeredis import aioredis

from app import create_app


@pytest.fixture
def app():
    app = create_app(rate_limit_backend=aioredis.FakeRedis())
    yield app
