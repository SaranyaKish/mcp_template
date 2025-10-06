from fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("My MCP Server")

# Tool 1: Greeting
@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"

# Tool 2: Reverse string
@mcp.tool
def reverse(text: str) -> str:
    return text[::-1]

# Tool 3: Convert to uppercase
@mcp.tool
def uppercase(text: str) -> str:
    return text.upper()

# Tool 4: Convert to lowercase
@mcp.tool
def lowercase(text: str) -> str:
    return text.lower()

# Tool 5: Capitalize the first letter
@mcp.tool
def capitalize(text: str) -> str:
    return text.capitalize()

# Run the server
if __name__ == "__main__":
    mcp.run()
