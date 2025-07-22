import pytest
from glpi_async.managers.tickets import TicketManager
from datetime import datetime


@pytest.mark.asyncio
async def test_create_ticket(mock_api):
    manager = TicketManager(mock_api)
    response = await manager.create(
        name="Test",
        content="Content",
        category_id=1,
        request_source_id=2,
        time_to_resolve=datetime(2025, 1, 1, 12, 0)
    )
    assert response["name"] == "Test"
    assert response["itilcategories_id"] == 1


@pytest.mark.asyncio
async def test_ticket_payload_iso_format():
    data = TicketManager.build_ticket_payload(
        "Test", "Content", 1, 2, datetime(2025, 1, 1, 13, 45)
    )
    assert data["input"]["time_to_resolve"] == "2025-01-01T13:45"
