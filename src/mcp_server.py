"""
src/mcp_server.py

MCP (Model Context Protocol) server for Project NAUR.

Exposes the Project Naur SQLite state to external MCP-compatible agents
(e.g., IBM Bob) over stdio transport. Three tools are registered:

  • read_architecture_thread    — fetch the current discussion thread
  • update_domain_constraint    — write a FE / BE / DS constraint + risk level
  • upsert_project_dictionary   — add or update a term in the shared glossary

Usage:
    python -m src.mcp_server
"""

import asyncio
import json
import logging

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

import src.state_manager as sm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("naur.mcp_server")

app = Server("project-naur-engine")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """Advertise the tools this server exposes to the connected MCP agent."""
    return [
        Tool(
            name="read_architecture_thread",
            description=(
                "Fetches the current cross-functional discussion thread from "
                "the Project Naur ledger. Returns the full chat history as a "
                "JSON-encoded list of {role, content} objects."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="update_domain_constraint",
            description=(
                "Writes or overwrites a technical constraint for a specific "
                "engineering domain (FE, BE, or DS) and records its risk level. "
                "Persists to the shared SQLite state so the UI dashboard reflects "
                "the change immediately."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "domain": {
                        "type": "string",
                        "description": "Engineering domain: 'FE', 'BE', or 'DS'.",
                        "enum": ["FE", "BE", "DS"],
                    },
                    "constraint_text": {
                        "type": "string",
                        "description": (
                            "Human-readable description of the technical constraint, "
                            "e.g. 'Must use React 18 with server-side rendering'."
                        ),
                    },
                    "risk_level": {
                        "type": "string",
                        "description": "Alignment risk: 'HIGH', 'MEDIUM', or 'LOW'.",
                        "enum": ["HIGH", "MEDIUM", "LOW"],
                    },
                },
                "required": ["domain", "constraint_text", "risk_level"],
            },
        ),
        Tool(
            name="upsert_project_dictionary",
            description=(
                "Adds a new term or updates an existing term in the shared "
                "Project Dictionary / ontological glossary. Persists to the "
                "SQLite state so the UI reflects the change immediately."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "term": {
                        "type": "string",
                        "description": "The term or concept to define.",
                    },
                    "definition": {
                        "type": "string",
                        "description": "The agreed-upon definition for that term.",
                    },
                },
                "required": ["term", "definition"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Dispatch an incoming tool call to the appropriate state_manager handler."""
    if name == "read_architecture_thread":
        logger.info("[TOOL CALL] read_architecture_thread")
        history = sm.get_chat_history()
        return [TextContent(type="text", text=json.dumps(history, ensure_ascii=False))]

    elif name == "update_domain_constraint":
        domain: str = arguments.get("domain", "").strip().upper()
        constraint_text: str = arguments.get("constraint_text", "").strip()
        risk_level: str = arguments.get("risk_level", "LOW").strip().upper()

        logger.info(
            "[TOOL CALL] update_domain_constraint | domain=%s risk=%s",
            domain, risk_level,
        )

        success = sm.update_constraint(domain, constraint_text, risk_level)
        if success:
            text = f"Success: Constraint for domain '{domain}' updated with risk level '{risk_level}'."
        else:
            text = f"Failure: Could not update constraint for domain '{domain}'. Check server logs."
        return [TextContent(type="text", text=text)]

    elif name == "upsert_project_dictionary":
        term: str = arguments.get("term", "").strip()
        definition: str = arguments.get("definition", "").strip()

        logger.info("[TOOL CALL] upsert_project_dictionary | term='%s'", term)

        success = sm.upsert_glossary_term(term, definition)
        if success:
            text = f"Success: Term '{term}' upserted into the Project Dictionary."
        else:
            text = f"Failure: Could not upsert term '{term}'. Check server logs."
        return [TextContent(type="text", text=text)]

    else:
        raise ValueError(f"Unknown tool: '{name}'")


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
