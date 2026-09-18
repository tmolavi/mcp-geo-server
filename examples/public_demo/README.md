# MCP GEO Server Public Demo

`[STANDALONE_DEMO_FIXTURE]` — **Model Context Protocol (MCP) Tool Invocations**

This demo shows how AI agents (Claude Code, Antigravity, Cursor) interact with the MCP GEO Server using standard JSON-RPC 2.0 tool calls.

---

## Files

| File | Description |
|------|-------------|
| `mcp_request_example.json` | Sample JSON-RPC request for `audit_full` tool |
| `mcp_response_example.json` | Standard MCP tool response payload |
| `run_demo.py` | Executable script simulating client tool call execution |

---

## 🚀 How to Run (Under 10 Seconds)

```bash
python examples/public_demo/run_demo.py
```

### Expected Output
```text
======================================================================
MCP GEO Server: AI Agent Protocol Demonstration
======================================================================
• Protocol            : Model Context Protocol (MCP) JSON-RPC 2.0
• Invocated Tool      : audit_full
• Target URL Argument : https://web24.ir
• Execution Mode      : standalone_demo_fixture (offline)
----------------------------------------------------------------------
✓ MCP Capabilities: technical_seo, entity_aeo, generative_geo

[Agent Protocol Interaction]
Agent >> tools/call -> audit_full(url='https://web24.ir')
Server << JSON-RPC Result: Composite Score = 85.0/100
----------------------------------------------------------------------
✓ MCP tool execution verified locally.
======================================================================
```
