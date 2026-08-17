from otx_py.client import PulsesResponse
from fastmcp import FastMCP
from otx_py import OTXClient
from dotenv import load_dotenv
import os
from msgspec import to_builtins

load_dotenv()

app = FastMCP()
OTX_KEY = os.environ.get("OTX_KEY")
if not OTX_KEY:
    raise ValueError("OTX_KEY isn't found")
otx = OTXClient(OTX_KEY)


@app.tool(description="Get the latest pulses from OTX")
def get_pulses(limit: int = 5) -> dict:
    pulses = otx.get_pulses(limit)
    return to_builtins(pulses)


@app.tool(description="Get different indicator types")
def get_indicator_types() -> dict:
    types = otx.get_indicator_types()
    return to_builtins(types)


@app.tool(description="Search for users")
def search_user(
    query: str,
    page: int = 1,
    limit: int = 20,
) -> dict:
    users = otx.search_users(query, page, limit)
    return to_builtins(users)


@app.tool(description="Search for pulses")
def search_pulses(query: str, page: int = 1, limit: int = 20) -> dict:
    pulses = otx.search_pulses(query, page, limit)
    return to_builtins(pulses)


@app.tool(description="Get user's username and detail")
def get_user(username: str, detail: bool) -> dict:
    user = otx.get_user(username, detail)
    return to_builtins(user)


@app.tool(description="Get a specific pulse from OTX by its ID")
def get_pulse(pulse_id: str) -> dict:
    pulse = otx.get_pulse_by_id(pulse_id)
    return to_builtins(pulse)


@app.tool(description="Get indicators")
def get_pulse_indicators(pulse_id: str, limit: int = 25) -> dict:
    pulse_indicator = otx.get_pulse_indicators(pulse_id, limit)
    return to_builtins(pulse_indicator)


if __name__ == "__main__":
    app.run(transport="http")
