import pytest
from glpi_async.api import AsyncGLPIAPI


class MockResponse:
    def __init__(self, json_data=None, status_code=200, text="OK"):
        self._json_data = json_data or {}
        self.status_code = status_code
        self.text = text

    def raise_for_status(self): pass

    def json(self):
        return self._json_data


class MockClient:
    headers = {}

    async def request(self, method, path, **kwargs):
        if method == "GET" and path == "/initSession":
            return MockResponse({"session_token": "test-token"})
        elif method == "POST" and path == "Ticket":
            return MockResponse({"id": 1, **kwargs.get("json", {}).get("input", {})})
        elif method == "GET" and path.startswith("ITILCategory"):
            return MockResponse({"name": "Mock Category"})
        return MockResponse()

    async def aclose(self): pass


@pytest.fixture
def mock_api():
    api = AsyncGLPIAPI("http://test", "app", "user")
    api.client = MockClient()
    return api
