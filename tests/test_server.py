"""Integration tests for the MCP GEO Server tool handlers."""
import json
import pytest
from unittest.mock import patch
from mcp_geo_server.server import app

SAMPLE_HTML = """<!DOCTYPE html>
<html>
<head>
<title>MCP GEO Server Test</title>
<meta name="description" content="Testing MCP GEO server tool invocation through SAGE Core adapter.">
<script type="application/ld+json">{"@context": "https://schema.org", "@type": "Product", "name": "Antigravity Agent"}</script>
</head>
<body>
<h1>MCP GEO Server Integration</h1>
<p>Generative Engine Optimization structures content for automated RAG ingestion pipelines and modern AI answer discovery systems.</p>
<h2>What is MAVI?</h2>
<p>MAVI is the Molavi AI Visibility Index measuring multi-layer optimization across technical, semantic, entity, citation, and agentic signals.</p>
</body>
</html>
"""


@pytest.mark.asyncio
async def test_list_all_tools():
    """Verify all new and backward-compatible tools are registered."""
    tools = await app.list_tools()
    tool_names = [tool.name for tool in tools]

    expected = [
        "audit_url",
        "audit_html",
        "technical_seo",
        "aeo_readiness",
        "geo_readiness",
        "entity_analysis",
        "citation_readiness",
        "generate_llms_txt",
        "get_capabilities",
        # Backward compatibility
        "audit_geo_url",
        "measure_mavi",
        "calculate_mavi_score",
        "generate_llms_txt_template",
    ]
    for name in expected:
        assert name in tool_names, f"Tool {name} not found in registered MCP tools"


@pytest.mark.asyncio
async def test_call_audit_html():
    """Test calling the primary audit_html tool."""
    res = await app.call_tool(
        "audit_html",
        {
            "html_content": SAMPLE_HTML,
            "url": "https://example.com/test",
            "embedding_backend": "hashing",
        }
    )
    assert res.is_error is False
    data = json.loads(res.content[0].text)
    assert data["status"] == "success"
    assert data["tool"] == "audit_html"
    assert data["engine"]["name"] == "sage"
    assert "score" in data
    assert len(data["findings"]) >= 20


@pytest.mark.asyncio
async def test_call_geo_readiness():
    """Test calling the geo_readiness tool."""
    res = await app.call_tool(
        "geo_readiness",
        {
            "html_content": SAMPLE_HTML,
            "embedding_backend": "hashing",
        }
    )
    assert res.is_error is False
    data = json.loads(res.content[0].text)
    assert data["status"] == "success"
    assert data["tool"] == "geo_readiness"
    assert "citation_survival_proxy" in data["metrics"]


@pytest.mark.asyncio
async def test_call_entity_analysis():
    """Test calling the entity_analysis tool."""
    res = await app.call_tool(
        "entity_analysis",
        {
            "html_content": SAMPLE_HTML,
        }
    )
    assert res.is_error is False
    data = json.loads(res.content[0].text)
    assert data["status"] == "success"
    assert "Product" in data["metrics"]["entity_types"]


@pytest.mark.asyncio
async def test_call_citation_readiness():
    """Test calling the citation_readiness tool."""
    res = await app.call_tool(
        "citation_readiness",
        {
            "html_content": SAMPLE_HTML,
            "embedding_backend": "hashing",
        }
    )
    assert res.is_error is False
    data = json.loads(res.content[0].text)
    assert data["status"] == "success"
    assert data["metrics"]["csp_details"]["metric_type"] == "heuristic_proxy"


@pytest.mark.asyncio
async def test_call_get_capabilities():
    """Test calling the get_capabilities tool."""
    res = await app.call_tool("get_capabilities", {})
    assert res.is_error is False
    data = json.loads(res.content[0].text)
    assert data["status"] == "success"
    assert data["engine"]["name"] == "sage"
    assert "E5" in data["evidence_taxonomy"]


@pytest.mark.asyncio
async def test_error_handling_invalid_input():
    """Test structured error response on missing input."""
    res = await app.call_tool("technical_seo", {})
    assert res.is_error is False  # Structured MCP error payload returned
    data = json.loads(res.content[0].text)
    assert data["status"] == "failed"
    assert data["error"]["type"] == "invalid_input"
    assert "score" not in data  # No fabricated score!


@pytest.mark.asyncio
async def test_error_handling_sage_engine_failure():
    """Test structured error response when SAGE engine fails."""
    with patch("sage_audit.SageAuditor.audit_html", side_effect=RuntimeError("SAGE internal failure")):
        res = await app.call_tool("geo_readiness", {"html_content": "<p>test</p>"})
        data = json.loads(res.content[0].text)
        assert data["status"] == "failed"
        assert data["error"]["type"] == "sage_engine_error"
        assert "score" not in data  # No fabricated score!


@pytest.mark.asyncio
async def test_backward_compatible_measure_mavi():
    """Test calling measure_mavi tool."""
    res = await app.call_tool(
        "measure_mavi",
        {
            "html_content": SAMPLE_HTML,
            "brand": "Antigravity",
        }
    )
    assert res.is_error is False
    data = json.loads(res.content[0].text)
    assert data["mavi_score"] is not None
    assert data["layers"]["L1"]["provenance"]["source"] == "sage"
    assert data["layers"]["L4"]["provenance"]["source"] == "sage"
