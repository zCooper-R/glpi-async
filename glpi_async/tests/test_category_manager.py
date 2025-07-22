import pytest
from glpi_async.managers.categories import CategoryManager


@pytest.mark.asyncio
async def test_list_categories(mock_api):
    async def mock_get(path, **kwargs):
        return {"data": [1, 2, 3]}
    mock_api.get = mock_get

    manager = CategoryManager(mock_api)
    result = await manager.list()
    assert "data" in result
