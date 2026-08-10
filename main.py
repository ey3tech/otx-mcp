from turtle import pu
from typing import Any
from fastmcp import FastMCP
from otx_py import OTXClient
from dotenv import load_dotenv
import os
from msgspec import json
from msgspec import to_builtins

load_dotenv()

app = FastMCP()
otx = OTXClient(os.environ["OTX_KEY"])


@app.tool(description="Get the latest pulses from OTX")
def get_pulses() -> dict[str, dict]:
    pulses = otx.get_pulses(5)
    return {"pulses": to_builtins(pulses)}

@app.tool(description="Get different indicator types")
def get_indicator_types() -> dict[str, dict]:
    types = otx.get_indicator_types()
    return {"indicator_types": to_builtins(types)}

@app.tool(description="Search for users")
def search_user(query: str) -> dict[str, dict]:
    users = otx.search_users(query, 1, 20)
    return {"search_users": to_builtins(users)}

@app.tool(description="Search for pulses")
def search_pulses(query: str) -> dict[str, dict]:
    pulses = otx.search_pulses(query, 1, 20)
    return {"pulses": to_builtins(pulses)}

@app.tool(description="Get user's username and detail")
def get_user(username: str, detail: bool) -> dict[str, dict]:
    user = otx.get_user(username, detail)
    return {"pulses": to_builtins(user)}

@app.tool(description="Get a specific pulse from OTX by its ID")
def get_pulse(pulse_id: str) -> dict[str, dict]:
    pulse = otx.get_pulse_by_id(pulse_id)
    return {"pulses": to_builtins(pulse)}

@app.tool(description="Get indicators")
def get_pulse_indicators(pulse_id: str, limit: int=25) -> dict[str, dict]:
    pulse_indicator = otx.get_pulse_indicators(pulse_id, limit)
    return {"indicators": to_builtins(pulse_indicator)}

if __name__ == "__main__":
    app.run(transport="http")
