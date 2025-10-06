# mcp_server.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, Callable
from datetime import datetime
import operator
import math

app = FastAPI(title="MCP Server with 5 Tools")

# ----------------------------
# Tool Function Definitions
# ----------------------------

def calculator_tool(args: Dict[str, Any]) -> Dict[str, Any]:
    expr = args.get("expression")
    try:
        result = eval(expr, {"__builtins__": None}, {"math": math})
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid expression: {str(e)}")

def get_time_tool(args: Dict[str, Any]) -> Dict[str, Any]:
    return {"time": datetime.utcnow().isoformat() + "Z"}

def echo_tool(args: Dict[str, Any]) -> Dict[str, Any]:
    return {"echo": args.get("message", "")}

def reverse_string_tool(args: Dict[str, Any]) -> Dict[str, Any]:
    input_str = args.get("text", "")
    return {"reversed": input_str[::-1]}

def weather_report_tool(args: Dict[str, Any]) -> Dict[str, Any]:
    city = args.get("city", "Unknown")
    return {"city": city, "weather": "Sunny", "temperature": "25°C"}

# ----------------------------
# Tool Registry
# ----------------------------

tool_registry: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {
    "calculator": calculator_tool,
    "get_time": get_time_tool,
    "echo": echo_tool,
    "reverse_string": reverse_string_tool,
    "weather_report": weather_report_tool
}

# ----------------------------
# MCP Input Model
# ----------------------------

class ToolCall(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]

# ----------------------------
# MCP Endpoint
# ----------------------------

@app.post("/mcp/call")
def call_tool(request: ToolCall):
    tool = tool_registry.get(request.tool_name)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    result = tool(request.arguments)
    return {
        "tool": request.tool_name,
        "result": result
    }
