import pytest
from glpi_async.api import AsyncGLPIAPI


@pytest.mark.asyncio
async def test_init_session():
    from .conftest import MockClient

    api = AsyncGLPIAPI("http://fake", "app-token", "user-token")
    api.client = MockClient()
    await api.init_session()

    assert api.session_token == "test-token"
    assert api.client.headers['Session-Token'] == "test-token"
