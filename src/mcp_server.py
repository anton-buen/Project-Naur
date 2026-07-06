"""
src/mcp_server.py

MCP (Model Context Protocol) server for Project NAUR.

Exposes the CognitiveAlignmentEngine to external MCP-compatible agents
(e.g., IBM Bob) over stdio transport. The server registers a single tool,
`process_architecture_intent`, that accepts a natural-language string,
runs it through the engine's assumption-extraction pipeline, and returns
a human-readable result string.

Usage:
    python -m src.mcp_server
"""

import asyncio
import logging

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from mcp import types

from src.engine import CognitiveAlignmentEngine

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("naur.mcp_server")

# ---------------------------------------------------------------------------
# Server initialisation
# ---------------------------------------------------------------------------

# The server name must match the key used in .bob/mcp.json
app = Server("project-naur-engine")

# ---------------------------------------------------------------------------
# Tool registration
# ---------------------------------------------------------------------------

@app.list_tools()
async def list_tools() -> list[Tool]:
    """Advertise the tools this server exposes to the connected MCP agent."""
    return [
        Tool(
            name="process_architecture_intent",
            description=(
                "Pass a natural-language architecture intent or discussion "
                "thread entry to the Cognitive Alignment Engine. "
                "The engine extracts cross-functional assumptions for the "
                "Frontend, Backend, and Data-Science domains and persists "
                "them to the shared session state. "
                "Returns a success or failure message."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "user_input": {
                        "type": "string",
                        "description": (
                            "The architecture intent or message to process, "
                            "e.g. 'We need real-time updates for the dashboard'."
                        ),
                    }
                },
                "required": ["user_input"],
            },
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Dispatch incoming tool calls to the appropriate handler.

    Currently only `process_architecture_intent` is registered.
    """
    if name != "process_architecture_intent":
        raise ValueError(f"Unknown tool: '{name}'")

    user_input: str = arguments.get("user_input", "").strip()

    if not user_input:
        return [
            TextContent(
                type="text",
                text="Error: 'user_input' must be a non-empty string.",
            )
        ]

    logger.info("[TOOL CALL] process_architecture_intent | input='%s'", user_input)

    try:
        # Instantiate a fresh engine for each call so it always reads the
        # latest persisted state from disk before processing.
        engine = CognitiveAlignmentEngine()
        success: bool = engine.process_intent(user_input)
    except Exception as exc:
        logger.exception("[TOOL ERROR] CognitiveAlignmentEngine raised an exception.")
        return [
            TextContent(
                type="text",
                text=f"Error: The engine encountered an unexpected problem — {exc}",
            )
        ]

    if success:
        message = (
            "Success: The architecture intent was processed and cross-functional "
            "assumptions have been updated in the session state."
        )
        logger.info("[TOOL RESULT] success")
    else:
        message = (
            "Failure: The engine could not extract assumptions from the provided "
            "input. Check the server logs for details."
        )
        logger.warning("[TOOL RESULT] failure")

    return [TextContent(type="text", text=message)]


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

async def main() -> None:
    """Start the MCP server and serve requests over stdio."""
    logger.info("[SERVER] project-naur-engine MCP server starting over stdio…")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
