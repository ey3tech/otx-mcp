from typing import Any
from fastmcp import FastMCP
from otx_py import OTXClient
from dotenv import load_dotenv
import os
from msgspec import json

load_dotenv()

app = FastMCP()
otx = OTXClient(os.environ["OTX_KEY"])


@app.tool(description="Get the latest pulses from OTX")
def pulses() -> dict[str, dict]:
    pulses = otx.pulses(5)
    print(json.decode(json.encode(pulses)))
    return {"pulses": json.decode(json.encode(pulses))}


@app.tool(description="Get a specific pulse from OTX by its ID")
def get_pulse(pulse_id: str) -> dict[str, Any]:
    pulse = otx.pulse_id(pulse_id)
    print(json.decode(json.encode(pulse)))
    return {"pulse": json.decode(json.encode(pulse))}


if __name__ == "__main__":
    app.run(transport="http")
