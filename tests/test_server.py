import pytest
import fastmcp
from main import app


@pytest.fixture
async def client():
    async with fastmcp.Client(app) as client:
        yield client


@pytest.mark.parametrize("limit", [1, 3, 5])
async def test_get_pulses(client: fastmcp.Client, limit: int):
    result = await client.call_tool("get_pulses", {"limit": limit})
    json_data = result.structured_content

    assert json_data is not None

    assert len(json_data["pulses"]["results"]) == limit


async def test_get_indicator_types(client: fastmcp.Client):
    result = await client.call_tool("get_indicator_types")
    json_data = result.structured_content

    assert json_data is not None

    assert len(json_data["indicator_types"]["detail"]) >= 1


@pytest.mark.parametrize(
    ["query", "expected_id"],
    [("twofortythree", 413902), ("MST478293", 402211), ("cyberhunterautofeed", 182496)],
)
async def test_search_user(client: fastmcp.Client, query: str, expected_id: int):
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
async def test_search_pulses(client: fastmcp.Client, query: str, expected_id: str):
    result = await client.call_tool(
        "search_pulses", {"query": query, "page": 1, "limit": 20})
    
    json_data = result.structured_content

    assert json_data is not None

    assert len(json_data["pulses"]["results"]) >= 1

    pulse_exists = any(pulse["id"] == expected_id for pulse in json_data["pulses"]["results"])

    assert pulse_exists, f"expected to find pulse with ID {expected_id}"

@pytest.mark.parametrize(
    ["username", "expected_id"],
    [("twofortythree", 413902), ("MST478293", 402211), ("cyberhunterautofeed", 182496)],
)
async def test_get_user(client: fastmcp.Client, username: str, expected_id: str):
    result = await client.call_tool(
        "get_user", {"username": username, "detail": False})
    
    json_data = result.structured_content

    assert json_data is not None

    user_is_correct = json_data["pulses"]["user_id"] == expected_id

    assert user_is_correct, f"expected to find user {expected_id} but got user {json_data['pulses']['user_id']}"

@pytest.mark.parametrize(
    ["expected_name", "expected_id"],
    [("PoS Scammers Toolbox", "546ce8eb11d40838dc6e43f1"), ("RAZOR BLADES IN THE CANDY JAR", "546cf5ba11d40839ea8821ca"), ("Operation Double Tap", "546fc7bf11d4083bc021c37f")],
)
async def test_get_pulse(client: fastmcp.Client, expected_name: str, expected_id: str):
    result = await client.call_tool(
        "get_pulse", {"pulse_id": expected_id})
    
    json_data = result.structured_content

    assert json_data is not None

    pulse_exists = json_data["pulses"]["name"].strip() == expected_name.strip()

    assert pulse_exists, f"expected to find specific pulse from OTX with ID {expected_name}. instead found {json_data['pulses']['name']}"

@pytest.mark.parametrize(
    ["expected_name", "expected_id"],
    [("PoS Scammers Toolbox", "546ce8eb11d40838dc6e43f1"), ("RAZOR BLADES IN THE CANDY JAR", "546cf5ba11d40839ea8821ca"), ("Operation Double Tap", "546fc7bf11d4083bc021c37f")],
)
async def test_get_pulse_indicators(client: fastmcp.Client, expected_name: str, expected_id: str):
    result = await client.call_tool(
        "get_pulse_indicators", {"pulse_id": expected_id, "limit": 10})
    
    json_data = result.structured_content

    assert json_data is not None

    assert len(json_data["indicators"]["results"]) >= 1

    # indicator_exists = any(indicator["id"] == expected_name for indicator in json_data["indicators"]["results"])

    # assert indicator_exists, f"expected to find indicators for indicator {expected_id}"


@pytest.mark.parametrize(
    "query",
    ["cjds9)MFJ9jfm2489jfdsajmf89sajdfo", "fka90fm34iamf0fj0934imfdisaojf", "fdasm89fjm389fjmasd0f8,jf0j348mf,d8safi"],
)
async def test_search_user_fail(client: fastmcp.Client, query: str):
    result = await client.call_tool(
        "search_user", {"query": query, "page": 1, "limit": 5}
    )
    json_data = result.structured_content

    assert json_data is not None

    search_user_exists = any(user["name"] == query for user in json_data["search_users"]["results"])

    assert not search_user_exists, f"expected to not find user with name {query}"

@pytest.mark.parametrize(
    "query",
    ["PoS Scammers Toolbox", "RAZOR BLADES IN THE CANDY JAR", "Operation Double Tap"],
)
async def test_search_pulses_fail(client: fastmcp.Client, query: str):
    result = await client.call_tool(
        "search_pulses", {"query": query, "page": 1, "limit": 5})
    
    json_data = result.structured_content

    assert json_data is not None

    pulse_exists = any(pulse["name"].strip() == query for pulse in json_data["pulses"]["results"])

    assert pulse_exists, f"expected to find pulse with ID {query}"

@pytest.mark.parametrize(
    "username",
    ["ddejhgrdiunuirvn", "feijfinvj", "fneionorinr"],
)
async def test_get_user_fail(client: fastmcp.Client, username: str):
    with pytest.raises(fastmcp.exceptions.ToolError, check=lambda e: "404" in str(e)):
        result = await client.call_tool(
            "get_user", {"username": username, "detail": False})
        
        json_data = result.structured_content

        assert json_data is not None

        user_is_correct = json_data["pulses"]["user_id"] == username

        assert user_is_correct, f"expected to find user {username} but got user {json_data['pulses']['user_id']}"

@pytest.mark.parametrize(
    "expected_id",
    ["a"*24, "b"*24, "c"*24],
)
async def test_get_pulse_fail(client: fastmcp.Client, expected_id: str):
    with pytest.raises(fastmcp.exceptions.ToolError, check=lambda e: "404" in str(e)):
        result = await client.call_tool(
        "get_pulse", {"pulse_id": expected_id})
    
        json_data = result.structured_content

        assert json_data is not None

        pulse_exists = json_data["pulses"].get("id") != expected_id

        assert pulse_exists, f"expected not to find specific pulse from OTX with ID {expected_id}. instead found {json_data['pulses']['id']}"

@pytest.mark.parametrize(
    "expected_id",
    ["a"*24, "b"*24, "c"*24],
)
async def test_get_pulse_indicators_fail(client: fastmcp.Client, expected_id: str):
    with pytest.raises(fastmcp.exceptions.ToolError, check=lambda e: "404" in str(e)):
        result = await client.call_tool(
            "get_pulse_indicators", {"pulse_id": expected_id, "limit": 10})
        
        json_data = result.structured_content

        assert json_data is not None

        assert not json_data["indicators"].get("results"), f"expected to find indicators for indicator {expected_id}"

