"""Tests for GEO Auditor."""
from mcp_geo_server.auditor import GEOAuditor

def test_analyze_html():
    sample_html = """<html><body>
    <h1>Test Page</h1>
    <script type="application/ld+json">{"@type": "Person", "name": "Taqi Molavi"}</script>
    <p>This is a test paragraph designed for testing the RAG chunking readiness in Generative Engine Optimization.</p>
    </body></html>"""
    res = GEOAuditor.analyze_html(sample_html, "https://molavi.pro")
    assert res["l1_infrastructure"]["has_schema_markup"] is True
    assert res["l1_infrastructure"]["schema_count"] == 1

def test_calculate_mavi():
    res = GEOAuditor.calculate_mavi(10, 18, 22, 20, 15)
    assert res["mavi_score"] == 85.0
    assert res["grade"] == "A+"
