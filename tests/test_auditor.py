"""Tests for GEO Auditor & MAVI Measurement."""
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
    assert res["mode"] == "manual_override"

def test_measure_mavi_automated():
    sample_html = """<html><body>
    <h1>Taqi Molavi GEO Framework</h1>
    <script type="application/ld+json">{"@type": "Person", "name": "Taqi Molavi"}</script>
    <p>According to research benchmarks, structured entity models improve AI visibility by 65% across search engines.</p>
    <table><tr><th>Metric</th><th>Score</th></tr><tr><td>MAVI</td><td>85</td></tr></table>
    </body></html>"""
    res = GEOAuditor.measure_mavi(html_content=sample_html, target_brand="Taqi Molavi")
    assert res["mavi_score"] is not None
    assert res["measured_layers_count"] == 4
    assert res["layers"]["L5"]["status"] == "not_measured"
    assert res["layers"]["L1"]["status"] == "measured"
