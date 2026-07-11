"""
MCP (Model Context Protocol) server for Project NAUR.

Exposes the Project Naur SQLite state to external MCP-compatible agents
(e.g., IBM Bob) over stdio transport. Three tools are registered:

  • read_architecture_thread    — fetch the current discussion thread
  • update_domain_constraint    — write a PROD/FE/BE/DS/UI/GLOBAL constraint + risk level
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
    return [
        Tool(
            name="read_architecture_thread",
            description="Fetches current discussion thread from the ledger.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="update_domain_constraint",
            description="Writes a constraint, its business translation, and risk level.",
            inputSchema={
                "type": "object",
                "properties": {
                    "domain": {"type": "string", "enum": ["PROD", "FE", "BE", "DS", "UI", "GLOBAL"]},
                    "constraint_text": {"type": "string", "description": "Technical engineering constraint."},
                    "business_impact": {"type": "string", "description": "Non-technical translation outlining trade-offs, cost, or legal risk."},
                    "risk_level": {"type": "string", "enum": ["HIGH", "MEDIUM", "LOW"]},
                },
                "required": ["domain", "constraint_text", "business_impact", "risk_level"],
            },
        ),
        Tool(
            name="upsert_project_dictionary",
            description="Adds a term to the glossary.",
            inputSchema={
                "type": "object",
                "properties": {
                    "term": {"type": "string"},
                    "definition": {"type": "string"},
                },
                "required": ["term", "definition"],
            },
        ),
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "read_architecture_thread":
        return [TextContent(type="text", text=json.dumps(sm.get_chat_history(), ensure_ascii=False))]
    elif name == "update_domain_constraint":
        domain = arguments.get("domain", "").strip().upper()
        text = arguments.get("constraint_text", "").strip()
        biz = arguments.get("business_impact", "").strip()
        risk = arguments.get("risk_level", "LOW").strip().upper()
        success = sm.update_constraint(domain, text, biz, risk)
        return [TextContent(type="text", text="Success" if success else "Failure")]
    elif name == "upsert_project_dictionary":
        term = arguments.get("term", "").strip()
        definition = arguments.get("definition", "").strip()
        success = sm.upsert_glossary_term(term, definition)
        return [TextContent(type="text", text="Success" if success else "Failure")]
    else:
        raise ValueError(f"Unknown tool: '{name}'")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())