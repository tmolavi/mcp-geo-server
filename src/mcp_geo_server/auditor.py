"""GEO Audit & MAVI Measurement Integration Layer.

Thin adapter/orchestrator delegating:
- SAGE Core audits via SageAdapter
- Canonical MAVI calculation via geo_scope.mavi.MAVIEngine

(c) 2026 Taqi Molavi — https://molavi.pro — MIT License
"""

from __future__ import annotations

import logging
import warnings
from typing import Any, Dict, Optional

from mcp_geo_server.adapter import SageAdapter

try:
    from geo_scope.mavi import (
        MAVIEngine,
        MAVIReport,
        LayerWeights,
        MAVI_METHODOLOGY_VERSION,
    )
    GEO_SCOPE_AVAILABLE = True
except ImportError:  # pragma: no cover
    GEO_SCOPE_AVAILABLE = False
    MAVIEngine = None
    MAVIReport = None
    LayerWeights = None
    MAVI_METHODOLOGY_VERSION = "MAVI v1.0"

logger = logging.getLogger("mcp_geo_server.auditor")


class GEOAuditor:
    """Compatibility facade and MAVI Measurement Engine v1 orchestrator."""

    @staticmethod
    def analyze_html(html_content: str, url: str = "https://example.local/") -> Dict[str, Any]:
        """[Deprecated] Forward to SAGE Core via SageAdapter.

        Maintained for backwards compatibility with legacy callers.
        """
        warnings.warn(
            "GEOAuditor.analyze_html is deprecated. Use SageAdapter.geo_readiness or SageAdapter.audit_full.",
            DeprecationWarning,
            stacklevel=2,
        )
        adapter = SageAdapter()
        geo_result = adapter.geo_readiness(url=url, html_content=html_content)
        seo_result = adapter.technical_seo(url=url, html_content=html_content)
        entity_result = adapter.entity_analysis(url=url, html_content=html_content)

        metrics = geo_result.get("metrics", {})
        seo_metrics = seo_result.get("metrics", {})

        return {
            "url": url,
            "engine": geo_result.get("engine"),
            "l1_infrastructure": {
                "dom_cleanliness_score": seo_metrics.get("text_to_code_ratio", 0.0) * 100.0,
                "word_count": seo_metrics.get("word_count", 0),
                "has_schema_markup": entity_result.get("metrics", {}).get("json_ld_blocks", 0) > 0,
                "schema_count": entity_result.get("metrics", {}).get("json_ld_blocks", 0),
                "schemas": entity_result.get("metrics", {}).get("entity_types", []),
            },
            "l3_rag_readiness": {
                "total_paragraphs": metrics.get("chunk_count", 0),
                "self_contained_chunks": metrics.get("chunk_count", 0),
                "headings_count": len(metrics.get("queries", [])),
                "heading_structure_sample": metrics.get("queries", [])[:5],
                "citation_survival_proxy": metrics.get("citation_survival_proxy"),
            },
            "sage_findings": geo_result.get("findings", []),
        }

    @classmethod
    def measure_mavi(
        cls,
        html_content: Optional[str] = None,
        url: Optional[str] = None,
        target_brand: Optional[str] = None,
        experiment_data: Optional[Dict[str, Any]] = None,
        custom_weights: Optional[Dict[str, float]] = None,
        manual_layers: Optional[Dict[str, float]] = None,
        measured_at: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Calculates Molavi AI Visibility Index (MAVI) v1 by delegating to canonical MAVIEngine in geo-scope."""
        if not GEO_SCOPE_AVAILABLE or MAVIEngine is None:
            raise RuntimeError("geo-scope is required for MAVI calculation but not available.")

        engine = MAVIEngine(weights=custom_weights)
        report: MAVIReport = engine.measure(
            html_content=html_content,
            url=url,
            target_brand=target_brand,
            experiment_data=experiment_data,
            manual_layers=manual_layers,
        )
        report_dict = report.to_dict()
        if measured_at:
            report_dict["timestamp_utc"] = measured_at
        return report_dict

    @staticmethod
    def calculate_mavi(l1: float, l2: float, l3: float, l4: float, l5: float) -> Dict[str, Any]:
        """Legacy helper for manual layer inputs (marked as manual_override / legacy_manual)."""
        score = round(l1 + l2 + l3 + l4 + l5, 2)
        grade = "A+" if score >= 85 else "A" if score >= 70 else "B" if score >= 50 else "C"
        return {
            "mavi_score": score,
            "max_score": 100.0,
            "grade": grade,
            "mode": "manual_override",
            "mavi_mode": "legacy_manual",
            "measurement_engine": False,
            "breakdown": {
                "L1_Infrastructure": l1,
                "L2_Entity_Authority": l2,
                "L3_RAG_Retrieval": l3,
                "L4_Citation_Trust": l4,
                "L5_Agentic_Mindshare": l5,
            },
        }

