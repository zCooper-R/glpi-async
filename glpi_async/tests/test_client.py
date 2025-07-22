import pytest
from glpi_async.client import GLPIClient


@pytest.mark.asyncio
async def test_context_manager(monkeypatch):
    class MockAPI:
        async def init_session(self): self.started = True
        async def kill_session(self): self.killed = True
        async def close(self): self.closed = True

    client = GLPIClient("http://base", "app", "user")
    client.api = MockAPI()

    async with client:
        assert hasattr(client.api, "started")

    assert hasattr(client.api, "killed")
    assert hasattr(client.api, "closed")
