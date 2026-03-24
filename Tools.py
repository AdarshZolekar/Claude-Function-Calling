"""
Tool definitions and dispatcher for Claude function calling demo.
Add new tools here — no changes needed in main.py.
"""

import math


# ── Tool schemas (sent to the Claude API) ────────────────────────────────────

TOOLS = [
    {
        "name": "score_checker",
        "description": (
            "Evaluates whether a student passed or failed based on their score. "
            "Returns 'Pass' if score > 0.5, otherwise 'Fail'."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "score": {
                    "type": "number",
                    "description": "Numeric score between 0.0 and 1.0",
                }
            },
            "required": ["score"],
        },
    },
    {
        "name": "calculator",
        "description": (
            "Evaluates a safe mathematical expression and returns the result. "
            "Supports +, -, *, /, **, sqrt, and parentheses."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Math expression to evaluate, e.g. '1337 * 42'",
                }
            },
            "required": ["expression"],
        },
    },
    {
        "name": "get_weather",
        "description": (
            "Returns the current weather for a given city. "
            "In a real application, this would call a weather API."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "Name of the city to get weather for",
                }
            },
            "required": ["city"],
        },
    },
]


# ── Tool implementations ──────────────────────────────────────────────────────

def score_checker(score: float) -> dict:
    """Returns Pass/Fail based on score threshold of 0.5."""
    if not (0.0 <= score <= 1.0):
        return {"error": f"Score {score} is out of valid range (0.0–1.0)."}
    result = "Pass" if score > 0.5 else "Fail"
    return {"score": score, "result": result, "threshold": 0.5}


def calculator(expression: str) -> dict:
    """Safely evaluates a math expression using only allowed operations."""
    allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("_")}
    allowed_names["abs"] = abs

    try:
        result = eval(expression, {"__builtins__": {}}, allowed_names)  # noqa: S307
        return {"expression": expression, "result": result}
    except Exception as exc:
        return {"error": f"Could not evaluate '{expression}': {exc}"}


def get_weather(city: str) -> dict:
    """Mock weather data — replace with a real API call (e.g., OpenWeatherMap)."""
    mock_data = {
        "Mumbai": {"temperature_c": 32, "condition": "Humid and partly cloudy", "humidity_pct": 78},
        "Pune":   {"temperature_c": 28, "condition": "Sunny with light breeze",  "humidity_pct": 55},
        "Delhi":  {"temperature_c": 38, "condition": "Hot and hazy",             "humidity_pct": 40},
    }
    data = mock_data.get(city, {"temperature_c": 25, "condition": "Clear skies", "humidity_pct": 60})
    return {"city": city, **data}


# ── Dispatcher ────────────────────────────────────────────────────────────────

_REGISTRY = {
    "score_checker": score_checker,
    "calculator":    calculator,
    "get_weather":   get_weather,
}


def dispatch_tool(name: str, inputs: dict) -> dict:
    """Routes a tool call by name to its implementation."""
    fn = _REGISTRY.get(name)
    if fn is None:
        return {"error": f"Unknown tool: '{name}'"}
    try:
        return fn(**inputs)
    except TypeError as exc:
        return {"error": f"Bad inputs for '{name}': {exc}"}
