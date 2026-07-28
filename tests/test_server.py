"""Tests for the MCP GEO Server."""
import pytest
from mcp_geo_server.server import app

@pytest.mark.asyncio
async def test_list_tools():
    """Verify all tools are registered and returned with correct schemas."""
    tools = await app.list_tools()
    tool_names = [tool.name for tool in tools]
    
    assert "audit_geo_url" in tool_names
    assert "calculate_mavi_score" in tool_names
    assert "generate_llms_txt_template" in tool_names

@pytest.mark.asyncio
async def test_call_audit_geo_url():
    """Test calling the audit_geo_url tool."""
    res = await app.call_tool(
        "audit_geo_url",
        {
            "url": "https://molavi.pro",
            "html_content": "<html><body><h1>Molavi Pyramid</h1><p>This is a paragraph with more than twenty words to satisfy the RAG chunking criteria that the auditor implements.</p></body></html>"
        }
    )
    assert res.is_error is False
    assert len(res.content) == 1
    assert res.content[0].type == "text"
    assert "dom_cleanliness_score" in res.content[0].text

@pytest.mark.asyncio
async def test_call_calculate_mavi_score():
    """Test calling calculate_mavi_score tool."""
    res = await app.call_tool(
        "calculate_mavi_score",
        {
            "l1_infrastructure": 9.0,
            "l2_entity_authority": 18.0,
            "l3_rag_retrieval": 22.0,
            "l4_citation_trust": 20.0,
            "l5_agentic_mindshare": 16.0
        }
    )
    assert res.is_error is False
    assert len(res.content) == 1
    assert res.content[0].type == "text"
    assert "mavi_score" in res.content[0].text

@pytest.mark.asyncio
async def test_call_generate_llms_txt_template():
    """Test calling generate_llms_txt_template tool."""
    res = await app.call_tool(
        "generate_llms_txt_template",
        {
            "domain": "molavi.pro",
            "title": "GEO Framework",
            "description": "GEO Pyramid description"
        }
    )
    assert res.is_error is False
    assert len(res.content) == 1
    assert res.content[0].type == "text"
    assert "GEO Framework" in res.content[0].text
    assert "molavi.pro" in res.content[0].text

@pytest.mark.asyncio
async def test_invalid_tool():
    """Test that calling an invalid tool raises ToolError."""
    from mcp.server.mcpserver.exceptions import ToolError
    with pytest.raises(ToolError):
        await app.call_tool("non_existent", {})
