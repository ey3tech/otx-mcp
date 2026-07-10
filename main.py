from fastmcp import FastMCP
from otx_py import OTXClient
from dotenv import load_dotenv
import os

load_dotenv()

app = FastMCP()
otx = OTXClient(os.environ["OTX_KEY"])


@app.tool(description="Get the latest pulses from OTX")
def pulses() -> dict:
    pulses = otx.pulses(5)
    return {"pulses": pulses}


@app.tool(description="Get a specific pulse from OTX by its ID")
def get_pulse(pulse_id: str) -> dict:
    pulse = otx.pulse_id(pulse_id)
    return {"pulse": pulse}


if __name__ == "__main__":
    app.run(transport="http")
