"""Tests for GEO Auditor & MAVI Measurement Engine v1."""
import pytest
from mcp_geo_server.auditor import GEOAuditor, MAVI_METHODOLOGY_VERSION

SAMPLE_HTML = """<html><body>
<h1>Taqi Molavi GEO Framework</h1>
<script type="application/ld+json">{"@context": "https://schema.org", "@type": "Person", "name": "Taqi Molavi"}</script>
<p>According to research benchmarks, structured entity models improve AI visibility by 65% across search engines.</p>
<table><tr><th>Metric</th><th>Score</th></tr><tr><td>MAVI</td><td>85</td></tr></table>
</body></html>"""


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
    assert res["mavi_mode"] == "legacy_manual"


def test_measure_mavi_automated_sage_only():
    """Acceptance Scenario B: SAGE Only measurements (L1-L4 measured, L5 not measured)."""
    res = GEOAuditor.measure_mavi(html_content=SAMPLE_HTML, target_brand="Taqi Molavi")
    assert res["mavi_methodology_version"] == MAVI_METHODOLOGY_VERSION
    assert res["mavi_score"] is not None
    assert res["measured_layers_count"] == 4
    assert res["total_layers_count"] == 5
    assert res["measurement_mode"] == "partial_measured"
    assert res["layers"]["L1"]["status"] == "measured"
    assert res["layers"]["L2"]["status"] == "measured"
    assert res["layers"]["L3"]["status"] == "measured"
    assert res["layers"]["L4"]["status"] == "measured"
    assert res["layers"]["L5"]["status"] == "not_measured"
    assert res["layers"]["L5"]["score"] is None
    assert res["confidence"]["confidence_level"] == "Medium"


def test_measure_mavi_full_live_experiment():
    """Acceptance Scenario A: Full 5-layer MAVI with live GEO-Scope experiment."""
    exp_data = {
        "experiment_id": "exp_live_2026",
        "execution_mode": "live",
        "providers": ["perplexity", "gemini", "openai"],
        "summary": {
            "successful_executions": 120,
            "total_executions": 120,
            "overall_sov": 75.0,
            "overall_top1_rate": 60.0,
            "overall_citation_rate": 80.0,
        },
    }
    res = GEOAuditor.measure_mavi(
        html_content=SAMPLE_HTML,
        target_brand="Taqi Molavi",
        experiment_data=exp_data,
    )
    assert res["mavi_score"] is not None
    assert res["measured_layers_count"] == 5
    assert res["measurement_mode"] == "measured"
    assert res["confidence"]["confidence_level"] == "High"
    assert res["layers"]["L5"]["status"] == "measured"
    assert res["layers"]["L5"]["source_type"] == "observed_live"
    assert res["layers"]["L5"]["methodology_status"] == "observational_benchmark"
    assert res["layers"]["L5"]["score"] == 71.5  # (75*0.5 + 60*0.3 + 80*0.2)


def test_measure_mavi_synthetic_experiment():
    """Acceptance Scenario C: Synthetic GEO-Scope simulation data."""
    exp_data = {
        "experiment_id": "exp_sim_2026",
        "execution_mode": "simulate",
        "providers": ["chatgpt_search"],
        "summary": {
            "successful_executions": 50,
            "total_executions": 50,
            "overall_sov": 65.0,
            "overall_top1_rate": 40.0,
            "overall_citation_rate": 50.0,
        },
    }
    res = GEOAuditor.measure_mavi(
        html_content=SAMPLE_HTML,
        target_brand="Taqi Molavi",
        experiment_data=exp_data,
    )
    assert res["measurement_mode"] == "measured_synthetic"
    assert res["layers"]["L5"]["status"] == "measured_synthetic"
    assert res["layers"]["L5"]["source_type"] == "synthetic"
    assert res["layers"]["L5"]["methodology_status"] == "non_observational"
    assert "synthetic_l5_penalty" in res["confidence"]["factors"]


def test_measure_mavi_insufficient_data_experiment():
    """Acceptance Scenario D: Poor experiment quality (0 observations)."""
    exp_data = {
        "experiment_id": "exp_failed",
        "execution_mode": "live",
        "summary": {
            "successful_executions": 0,
            "total_executions": 50,
        },
    }
    res = GEOAuditor.measure_mavi(
        html_content=SAMPLE_HTML,
        target_brand="Taqi Molavi",
        experiment_data=exp_data,
    )
    assert res["layers"]["L5"]["status"] == "insufficient_data"
    assert res["layers"]["L5"]["score"] is None
    assert res["measured_layers_count"] == 4  # Does not count insufficient L5 as 0


def test_measure_mavi_custom_weights_and_validation():
    """Acceptance Scenario E: Custom configurable weights."""
    custom = {"L1": 0.10, "L2": 0.20, "L3": 0.20, "L4": 0.20, "L5": 0.30}
    res = GEOAuditor.measure_mavi(html_content=SAMPLE_HTML, custom_weights=custom)
    assert res["weights_provenance"] == "custom_configured"
    assert res["weights"]["L1"] == 0.10
    assert res["weights"]["L5"] == 0.30

    with pytest.raises(ValueError, match="cannot be negative"):
        GEOAuditor.measure_mavi(html_content=SAMPLE_HTML, custom_weights={"L1": -0.1})


def test_measure_mavi_explainability_contributors():
    """Acceptance Scenario F: Explainability contributors in every layer."""
    res = GEOAuditor.measure_mavi(html_content=SAMPLE_HTML, target_brand="Taqi Molavi")
    for lid in ["L1", "L2", "L3", "L4"]:
        layer = res["layers"][lid]
        assert len(layer["contributors"]) >= 2
        for c in layer["contributors"]:
            assert "signal" in c
            assert "impact" in c
            assert "description" in c


def test_measure_mavi_manual_override_mode():
    """Acceptance Scenario G: Manual layer override."""
    manual = {"L1": 80.0, "L2": 70.0, "L3": 90.0, "L4": 65.0, "L5": 85.0}
    res = GEOAuditor.measure_mavi(manual_layers=manual)
    assert res["measurement_mode"] == "manual_override"
    assert res["layers"]["L1"]["status"] == "manual_override"
    assert res["layers"]["L1"]["score"] == 80.0
    assert res["mavi_score"] is not None


def test_measure_mavi_strict_delegation_deduplication(monkeypatch):
    """Verify that GEOAuditor.measure_mavi strictly delegates to canonical geo_scope.mavi.MAVIEngine."""
    import mcp_geo_server.auditor as auditor_module
    from geo_scope.mavi.engine import MAVIEngine
    from geo_scope.mavi.models import MAVIReport

    # Verify MCP auditor module does NOT define duplicate internal calculation helpers
    assert not hasattr(auditor_module, "DEFAULT_WEIGHTS")
    assert not hasattr(auditor_module.GEOAuditor, "_build_l1_layer")
    assert not hasattr(auditor_module.GEOAuditor, "_build_l5_layer")
    assert not hasattr(auditor_module.GEOAuditor, "_assess_confidence")

    # Verify delegation call flow
    called = False
    original_measure = MAVIEngine.measure

    def spy_measure(self, *args, **kwargs):
        nonlocal called
        called = True
        return original_measure(self, *args, **kwargs)

    monkeypatch.setattr(MAVIEngine, "measure", spy_measure)

    res = GEOAuditor.measure_mavi(html_content=SAMPLE_HTML, target_brand="Taqi Molavi")
    assert called is True
    assert isinstance(res, dict)
    assert "mavi_score" in res
    assert res["measured_layers_count"] == 4


