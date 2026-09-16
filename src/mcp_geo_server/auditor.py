"""GEO Audit & MAVI Measurement Integration Layer.

Deprecated internal scoring methods are forwarded directly to SAGE Core via
`SageAdapter`. No duplicate independent scoring engine is maintained.

(c) 2026 Taqi Molavi — https://molavi.pro — MIT License
"""

from __future__ import annotations

import logging
import warnings
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from mcp_geo_server.adapter import SageAdapter

logger = logging.getLogger("mcp_geo_server.auditor")


class GEOAuditor:
    """Compatibility facade forwarding audit requests directly to SAGE Core."""

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

        # Return structured view conforming to legacy keys but powered by SAGE
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

    @staticmethod
    def measure_mavi(
        html_content: Optional[str] = None,
        url: Optional[str] = None,
        target_brand: Optional[str] = None,
        experiment_data: Optional[Dict[str, Any]] = None,
        custom_weights: Optional[Dict[str, float]] = None,
        manual_layers: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        """Calculates Molavi AI Visibility Index (MAVI) v1 fusing SAGE L1-L4 + GEO-Scope L5 measurements."""
        weights = {
            "L1": 0.15,
            "L2": 0.20,
            "L3": 0.20,
            "L4": 0.20,
            "L5": 0.25,
        }
        if custom_weights:
            weights.update(custom_weights)

        timestamp_utc = datetime.now(timezone.utc).isoformat()
        layers: Dict[str, Any] = {}

        if manual_layers:
            measurement_mode = "manual_override"
            for lid in ["L1", "L2", "L3", "L4", "L5"]:
                val = manual_layers.get(lid)
                layers[lid] = {
                    "layer_id": lid,
                    "score": round(float(val), 1) if val is not None else None,
                    "weight": weights.get(lid, 0.2),
                    "status": "manual_override" if val is not None else "not_measured",
                    "provenance": {
                        "source": "manual",
                        "metric_version": "1.0.0",
                        "timestamp_utc": timestamp_utc,
                        "evidence_count": 1 if val is not None else 0,
                    },
                }
        else:
            measurement_mode = "measured"
            if html_content or url:
                adapter = SageAdapter()
                # Use SAGE Core for L1-L4
                seo_res = adapter.technical_seo(url=url, html_content=html_content)
                aeo_res = adapter.aeo_readiness(url=url, html_content=html_content)
                geo_res = adapter.geo_readiness(url=url, html_content=html_content)

                # L1 Technical Accessibility (SAGE Technical SEO Pillar)
                layers["L1"] = {
                    "layer_id": "L1",
                    "layer_name": "Technical Accessibility",
                    "score": round(seo_res.get("score", 0.0), 1),
                    "weight": weights["L1"],
                    "status": "measured",
                    "provenance": {
                        "source": "sage",
                        "engine_version": seo_res.get("engine", {}).get("version"),
                        "timestamp_utc": timestamp_utc,
                        "evidence_count": len(seo_res.get("findings", [])),
                    },
                }

                # L2 Semantic Extractability (SAGE AEO Direct Answer Density & Sections)
                layers["L2"] = {
                    "layer_id": "L2",
                    "layer_name": "Semantic Extractability",
                    "score": round(aeo_res.get("score", 0.0), 1),
                    "weight": weights["L2"],
                    "status": "measured",
                    "provenance": {
                        "source": "sage",
                        "engine_version": aeo_res.get("engine", {}).get("version"),
                        "timestamp_utc": timestamp_utc,
                        "evidence_count": len(aeo_res.get("findings", [])),
                    },
                }

                # L3 Entity Clarity (SAGE AEO Entity Graph & sameAs Authority)
                entity_res = adapter.entity_analysis(url=url, html_content=html_content)
                layers["L3"] = {
                    "layer_id": "L3",
                    "layer_name": "Entity Clarity",
                    "score": round(entity_res.get("score", 0.0), 1),
                    "weight": weights["L3"],
                    "status": "measured",
                    "provenance": {
                        "source": "sage",
                        "engine_version": entity_res.get("engine", {}).get("version"),
                        "timestamp_utc": timestamp_utc,
                        "evidence_count": len(entity_res.get("findings", [])),
                    },
                }

                # L4 Citation Readiness (SAGE GEO Citation Survival Proxy / RAG Simulation)
                csp_val = geo_res.get("metrics", {}).get("citation_survival_proxy")
                l4_score = float(csp_val) if csp_val is not None else float(geo_res.get("score", 0.0))
                layers["L4"] = {
                    "layer_id": "L4",
                    "layer_name": "Citation Readiness",
                    "score": round(l4_score, 1),
                    "weight": weights["L4"],
                    "status": "measured",
                    "provenance": {
                        "source": "sage",
                        "engine_version": geo_res.get("engine", {}).get("version"),
                        "timestamp_utc": timestamp_utc,
                        "evidence_count": len(geo_res.get("findings", [])),
                    },
                }
            else:
                for lid in ["L1", "L2", "L3", "L4"]:
                    layers[lid] = {
                        "layer_id": lid,
                        "score": None,
                        "weight": weights[lid],
                        "status": "not_measured",
                        "provenance": {"source": "sage", "metric_version": "1.0.0", "timestamp_utc": timestamp_utc, "evidence_count": 0},
                    }

            # L5 Observed AI Visibility (GEO-Scope observations)
            if experiment_data and experiment_data.get("summary", {}).get("successful_executions", 0) > 0:
                summary = experiment_data["summary"]
                sov = summary.get("overall_sov", 0.0) or 0.0
                top1 = summary.get("overall_top1_rate", 0.0) or 0.0
                l5_score = round((sov * 0.60) + (top1 * 0.40), 1)
                layers["L5"] = {
                    "layer_id": "L5",
                    "layer_name": "Observed AI Visibility",
                    "score": l5_score,
                    "weight": weights["L5"],
                    "status": "measured",
                    "provenance": {
                        "source": "geo-scope",
                        "metric_version": "1.0.0",
                        "timestamp_utc": timestamp_utc,
                        "evidence_count": summary.get("successful_executions", 0),
                        "experiment_id": experiment_data.get("experiment_id"),
                    },
                }
            else:
                layers["L5"] = {
                    "layer_id": "L5",
                    "layer_name": "Observed AI Visibility",
                    "score": None,
                    "weight": weights["L5"],
                    "status": "not_measured",
                    "provenance": {"source": "geo-scope", "metric_version": "1.0.0", "timestamp_utc": timestamp_utc, "evidence_count": 0},
                }

        active = [l for l in layers.values() if l["score"] is not None]
        active_count = len(active)
        active_weight_sum = sum(l["weight"] for l in active)

        if active_count > 0 and active_weight_sum > 0:
            raw_score = sum(l["score"] * l["weight"] for l in active)
            mavi_score = round(raw_score / active_weight_sum, 1)
            grade = "A+" if mavi_score >= 85 else "A" if mavi_score >= 70 else "B" if mavi_score >= 50 else "C"
            norm_basis = f"Normalized across {active_count}/5 measured layers; active weight sum = {active_weight_sum:.2f}"
        else:
            mavi_score = None
            grade = "N/A"
            norm_basis = "No layers measured"

        confidence_level = "High" if active_count == 5 else ("Medium" if active_count >= 3 else "Low")

        return {
            "mavi_score": mavi_score,
            "max_score": 100.0,
            "grade": grade,
            "measured_layers_count": active_count,
            "total_layers_count": 5,
            "measurement_mode": measurement_mode if active_count == 5 else "partial_measured",
            "normalization_basis": norm_basis,
            "confidence": {"confidence_level": confidence_level, "confidence_score": round(active_count / 5.0, 2)},
            "layers": layers,
        }

    @staticmethod
    def calculate_mavi(l1: float, l2: float, l3: float, l4: float, l5: float) -> Dict[str, Any]:
        """Legacy helper for manual layer inputs (marked as manual_override)."""
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
