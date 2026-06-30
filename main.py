from fastmcp import FastMCP

app = FastMCP()

@app.tool()
def add(x: int, y: int) -> int:
    return x + y

if __name__ == "__main__":
    app.run(transport="http")
