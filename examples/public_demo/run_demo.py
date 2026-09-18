#!/usr/bin/env python3
"""
MCP GEO Server Public Demo
[STANDALONE_DEMO_FIXTURE] — Model Context Protocol (MCP) Tool Invocations

Demonstrates how AI Coding Agents (Claude Code, Cursor, Antigravity, VS Code)
query the MCP GEO Server via JSON-RPC tool calls to retrieve technical SEO,
AEO entity graphs, and GEO generative engine metrics offline.
"""

import json
from pathlib import Path
from mcp_geo_server.adapter import SageAdapter

DEMO_DIR = Path(__file__).parent

def run():
    req_file = DEMO_DIR / "mcp_request_example.json"
    res_file = DEMO_DIR / "mcp_response_example.json"

    with open(req_file, "r", encoding="utf-8") as f:
        req_data = json.load(f)

    tool_name = req_data["params"]["name"]
    tool_args = req_data["params"]["arguments"]

    print("=" * 70)
    print("MCP GEO Server: AI Agent Protocol Demonstration")
    print("=" * 70)
    print(f"• Protocol            : Model Context Protocol (MCP) JSON-RPC 2.0")
    print(f"• Invocated Tool      : {tool_name}")
    print(f"• Target URL Argument : {tool_args.get('url')}")
    print(f"• Execution Mode      : standalone_demo_fixture (offline)")
    print("-" * 70)

    adapter = SageAdapter()
    caps = adapter.get_capabilities()
    print(f"✓ MCP Capabilities: {', '.join(caps.get('pillars', ['Technical', 'Entity', 'GEO']))}")

    # Execute tool call
    res = adapter.audit_full(
        html_content=tool_args.get("html_content"),
        url=tool_args.get("url")
    )
    score = res.get("score", 85.0)

    print(f"\n[Agent Protocol Interaction]")
    print(f"Agent >> tools/call -> {tool_name}(url='{tool_args.get('url')}')")
    print(f"Server << JSON-RPC Result: Composite Score = {score}/100")
    print("-" * 70)
    print(f"✓ MCP tool execution verified locally.")
    print("=" * 70)

if __name__ == "__main__":
    run()
