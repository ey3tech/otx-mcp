from mcp.types import TextContent
import pytest
from fastmcp import Client
from main import app
from msgspec import json


@pytest.fixture
async def client():
    async with Client(app) as client:
        yield client


@pytest.mark.parametrize("limit", [1, 3, 5])
async def test_get_pulses(client: Client, limit: int):
    result = await client.call_tool("get_pulses", {"limit": limit})
    json_data = result.structured_content

    assert json_data is not None

    assert len(json_data["pulses"]["results"]) == limit


async def test_get_indicator_types(client: Client):
    result = await client.call_tool("get_indicator_types")
    json_data = result.structured_content

    assert json_data is not None

    assert len(json_data["indicator_types"]["detail"]) >= 1


@pytest.mark.parametrize(
    ["query", "expected_id"],
    [("twofortythree", 413902), ("MST478293", 402211), ("cyberhunterautofeed", 182496)],
)
async def test_search_user(client: Client, query: str, expected_id: int):
    result = await client.call_tool(
        "search_user", {"query": query, "page": 1, "limit": 20}
    )
    json_data = result.structured_content

    assert json_data is not None

    assert len(json_data["search_users"]["results"]) >= 1

    search_user_exists = any(user["user_id"] == expected_id for user in json_data["search_users"]["results"])

    assert search_user_exists, f"expected to find user with ID {expected_id}"

@pytest.mark.parametrize(
    ["query", "expected_id"],
    [("PoS Scammers Toolbox", "546ce8eb11d40838dc6e43f1"), ("RAZOR BLADES IN THE CANDY JAR", "546cf5ba11d40839ea8821ca"), ("Operation Double Tap", "546fc7bf11d4083bc021c37f")],
)
async def test_search_pulses(client: Client, query: str, expected_id: str):
    result = await client.call_tool(
        "search_pulses", {"query": query, "page": 1, "limit": 1})
    
    json_data = result.structured_content

    assert json_data is not None

    assert len(json_data["pulses"]["results"]) >= 1

    pulse_exists = any(pulse["id"] == expected_id for pulse in json_data["pulses"]["results"])

    assert pulse_exists, f"expected to find pulse with ID {expected_id}"


