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
    """Return the list of tools exposed by this MCP server.

    Returns:
        A list of ``Tool`` descriptors for ``read_architecture_thread``,
        ``update_domain_constraint``, and ``upsert_project_dictionary``.
    """
    return [
        Tool(
            name="read_architecture_thread",
            description="Fetches current discussion thread from the ledger.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="update_domain_constraint",
            description="Writes a constraint, its business translation, detailed explanation, and risk level.",
            inputSchema={
                "type": "object",
                "properties": {
                    "domain": {"type": "string", "enum": ["PROD", "FE", "BE", "DS", "UI", "GLOBAL"]},
                    "constraint_text": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Exactly 1-2 bullet points. STRICTLY NO meta-commentary.",
                    },
                    "business_impact": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Exactly 1-2 bullet points in 100% Layman terms. No meta-commentary.",
                    },
                    "deep_dive": {"type": "string", "description": "REQUIRED. Put long-form technical explanations here."},
                    "risk_level": {"type": "string", "enum": ["HIGH", "MEDIUM", "LOW"]},
                },
                "required": ["domain", "constraint_text", "business_impact", "deep_dive", "risk_level"],
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
    """Dispatch an incoming tool call to the appropriate state-manager function.

    Args:
        name: The registered tool name.
        arguments: Key-value payload supplied by the MCP client.

    Returns:
        A single-element list containing a ``TextContent`` with ``"Success"``
        or ``"Failure"`` as the text body.

    Raises:
        ValueError: If *name* does not match any registered tool.
    """
    if name == "read_architecture_thread":
        return [TextContent(type="text", text=json.dumps(sm.get_chat_history(), ensure_ascii=False))]

    elif name == "update_domain_constraint":
        domain = arguments.get("domain", "").strip().upper()

        valid_domains = ["PROD", "FE", "BE", "DS", "UI", "GLOBAL"]
        if domain not in valid_domains:
            return [TextContent(
                type="text",
                text=f"Error: invalid domain {domain!r}. Must be one of {valid_domains}.",
            )]

        t_data = arguments.get("constraint_text", [])
        if isinstance(t_data, list):
            text = "\n".join(t_data).replace("\\n", "\n")
        else:
            return [TextContent(type="text", text="Error: 'constraint_text' must be a JSON array of strings.")]

        b_data = arguments.get("business_impact", [])
        if isinstance(b_data, list):
            biz = "\n".join(b_data).replace("\\n", "\n")
        else:
            return [TextContent(type="text", text="Error: 'business_impact' must be a JSON array of strings.")]

        deep = arguments.get("deep_dive", "").strip().replace("\\n", "\n")
        risk_level = arguments.get("risk_level", "LOW").strip().upper()

        success = sm.update_constraint(domain, text, biz, deep, risk_level)
        return [TextContent(type="text", text="Success" if success else "Failure: database write error.")]

    elif name == "upsert_project_dictionary":
        term = arguments.get("term", "").strip()
        defn = arguments.get("definition", "").strip()
        if not term:
            return [TextContent(type="text", text="Error: 'term' must be a non-empty string.")]
        success = sm.upsert_glossary_term(term, defn)
        return [TextContent(type="text", text="Success" if success else "Failure: database write error.")]

    else:
        raise ValueError(f"Unknown tool: '{name}'")


async def main() -> None:
    """Start the MCP server and run until the stdio streams close."""
    sm.init_db()
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
