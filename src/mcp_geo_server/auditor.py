"""GEO Audit & MAVI Measurement Integration Layer.

Implements MAVI (Molavi AI Visibility Index) Measurement Engine v1:
- L1 Technical Accessibility (SAGE Technical SEO)
- L2 Semantic Extractability (SAGE AEO Structure)
- L3 Entity Clarity (SAGE Entity Graph)
- L4 Retrieval / Citation Readiness (SAGE GEO / CSP Diagnostic)
- L5 Observed AI Visibility (GEO-Scope Empirical Observations)

(c) 2026 Taqi Molavi — https://molavi.pro — MIT License
"""

from __future__ import annotations

import logging
import warnings
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from mcp_geo_server import __version__ as MCP_SERVER_VERSION
from mcp_geo_server.adapter import SageAdapter

logger = logging.getLogger("mcp_geo_server.auditor")

MAVI_METHODOLOGY_VERSION = "MAVI v1.0"

DEFAULT_WEIGHTS: Dict[str, float] = {
    "L1": 0.15,
    "L2": 0.20,
    "L3": 0.20,
    "L4": 0.20,
    "L5": 0.25,
}


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
        """Calculates Molavi AI Visibility Index (MAVI) v1 fusing SAGE L1-L4 + GEO-Scope L5 measurements.

        Features:
        - Strict 5-layer measurement hierarchy (L1-L5)
        - Partial scoring support without fabricating missing data as zero
        - Live vs. Synthetic L5 distinction with quality guard
        - Layer-level provenance and explainability contributors
        - Deterministic confidence assessment and freshness tracking
        """
        # 1. Weights Configuration
        weights = dict(DEFAULT_WEIGHTS)
        weights_provenance = "methodology_defaults_v1"
        if custom_weights:
            # Validate custom weights
            for k, v in custom_weights.items():
                if v < 0:
                    raise ValueError(f"Weight for {k} cannot be negative: {v}")
            weights.update(custom_weights)
            weights_provenance = "custom_configured"

        total_weight_sum = sum(weights.values())
        if total_weight_sum <= 0:
            raise ValueError("Sum of layer weights must be greater than zero.")

        timestamp_utc = measured_at or datetime.now(timezone.utc).isoformat()
        layers: Dict[str, Any] = {}

        # 2. Manual Override Path (isolated and labeled)
        if manual_layers is not None:
            measurement_mode = "manual_override"
            name_map = {
                "L1": "Technical Accessibility",
                "L2": "Semantic Extractability",
                "L3": "Entity Clarity",
                "L4": "Retrieval / Citation Readiness",
                "L5": "Observed AI Visibility",
            }
            for lid in ["L1", "L2", "L3", "L4", "L5"]:
                val = manual_layers.get(lid)
                score = round(float(val), 1) if val is not None else None
                status = "manual_override" if val is not None else "not_measured"
                layers[lid] = {
                    "layer_id": lid,
                    "layer_name": name_map[lid],
                    "weight": weights.get(lid, 0.2),
                    "score": score,
                    "status": status,
                    "provenance": {
                        "source": "manual",
                        "source_engine": "manual",
                        "source_version": "1.0.0",
                        "methodology_version": MAVI_METHODOLOGY_VERSION,
                        "timestamp_utc": timestamp_utc,
                        "evidence_count": 1 if val is not None else 0,
                    },
                    "contributors": [
                        {
                            "signal": "manual_override",
                            "impact": score or 0.0,
                            "description": "Score supplied via manual override mode (non-observational).",
                        }
                    ] if score is not None else [],
                    "findings": ["Manual override input."],
                }
        else:
            measurement_mode = "measured"
            # 3. Automated SAGE Auditing for L1-L4
            if html_content or url:
                adapter = SageAdapter()
                seo_res = adapter.technical_seo(url=url, html_content=html_content)
                aeo_res = adapter.aeo_readiness(url=url, html_content=html_content)
                entity_res = adapter.entity_analysis(url=url, html_content=html_content)
                geo_res = adapter.geo_readiness(url=url, html_content=html_content)

                layers["L1"] = cls._build_l1_layer(seo_res, weights["L1"], timestamp_utc)
                layers["L2"] = cls._build_l2_layer(aeo_res, weights["L2"], timestamp_utc)
                layers["L3"] = cls._build_l3_layer(entity_res, target_brand, weights["L3"], timestamp_utc)
                layers["L4"] = cls._build_l4_layer(geo_res, weights["L4"], timestamp_utc)
            else:
                for lid, lname in [
                    ("L1", "Technical Accessibility"),
                    ("L2", "Semantic Extractability"),
                    ("L3", "Entity Clarity"),
                    ("L4", "Retrieval / Citation Readiness"),
                ]:
                    layers[lid] = {
                        "layer_id": lid,
                        "layer_name": lname,
                        "weight": weights[lid],
                        "score": None,
                        "status": "not_measured",
                        "provenance": {
                            "source": "sage",
                            "source_engine": "sage-audit",
                            "source_version": "unknown",
                            "methodology_version": MAVI_METHODOLOGY_VERSION,
                            "timestamp_utc": timestamp_utc,
                            "evidence_count": 0,
                        },
                        "contributors": [],
                        "findings": [f"{lid} {lname} not measured (provide HTML or URL to measure)."],
                    }

            # 4. Automated GEO-Scope Evaluation for L5
            layers["L5"] = cls._build_l5_layer(experiment_data, target_brand, weights["L5"], timestamp_utc)

        # 5. Compute Partial Scoring and Normalization
        active_layers = [
            l for l in layers.values()
            if l.get("score") is not None and l.get("status") in ("measured", "measured_synthetic", "manual_override")
        ]
        active_count = len(active_layers)
        total_layers = 5

        if active_count == 0:
            mavi_score = None
            grade = "N/A"
            final_mode = "not_measured"
            norm_basis = "No layers were measured; MAVI score undefined."
        else:
            raw_measured = sum(l["score"] * l["weight"] for l in active_layers)
            active_weights_sum = sum(l["weight"] for l in active_layers)
            mavi_score = round(raw_measured / active_weights_sum, 1) if active_weights_sum > 0 else 0.0

            grade = "A+" if mavi_score >= 85 else "A" if mavi_score >= 70 else "B" if mavi_score >= 50 else "C"

            if measurement_mode == "manual_override":
                final_mode = "manual_override"
                norm_basis = f"Manual override score across {active_count}/5 layers"
            elif layers.get("L5", {}).get("status") == "measured_synthetic":
                final_mode = "measured_synthetic"
                norm_basis = f"Normalized across {active_count}/5 layers (includes synthetic L5)"
            elif active_count < total_layers:
                final_mode = "partial_measured"
                active_ids = [l["layer_id"] for l in active_layers]
                norm_basis = f"Normalized across {active_count}/{total_layers} measured layers ({', '.join(active_ids)}); active weight sum = {active_weights_sum:.2f}"
            else:
                final_mode = "measured"
                norm_basis = "Complete 5-layer measured index (100% layer coverage)"

        # 6. Confidence Assessment
        confidence = cls._assess_confidence(layers, active_count, timestamp_utc)

        return {
            "mavi_methodology_version": MAVI_METHODOLOGY_VERSION,
            "mavi_score": mavi_score,
            "max_score": 100.0,
            "grade": grade,
            "measurement_mode": final_mode,
            "measured_layers_count": active_count,
            "total_layers_count": total_layers,
            "normalization_basis": norm_basis,
            "weights": weights,
            "weights_provenance": weights_provenance,
            "confidence": confidence,
            "target_entity": target_brand or "Target Entity",
            "url": url,
            "timestamp_utc": timestamp_utc,
            "layers": layers,
            "limitations": [
                "L1-L4 represent deterministic page-level AI extractability and diagnostic proxies from SAGE.",
                "L4 Citation Survival Proxy (CSP) is a heuristic proxy (E4), not a calibrated empirical probability.",
                "L5 reflects observational visibility only when executed in LIVE mode with sufficient observations.",
                "Synthetic L5 results are simulation-based and non-observational.",
            ],
        }

    @classmethod
    def _build_l1_layer(cls, seo_res: Dict[str, Any], weight: float, timestamp_utc: str) -> Dict[str, Any]:
        """Builds L1 Technical Accessibility layer from SAGE Technical SEO."""
        score = round(float(seo_res.get("score", 0.0)), 1)
        engine_ver = seo_res.get("engine", {}).get("version", "2.0.0")
        findings = seo_res.get("findings", [])
        metrics = seo_res.get("metrics", {})

        contributors = [
            {
                "signal": "technical_seo_baseline",
                "impact": round(score * 0.40, 1),
                "description": f"SAGE Technical SEO audit baseline score: {score}/100",
            },
            {
                "signal": "dom_cleanliness",
                "impact": round(min(30.0, metrics.get("text_to_code_ratio", 0.0) * 300.0), 1),
                "description": f"Text to HTML ratio: {metrics.get('text_to_code_ratio', 0.0):.2%}",
            },
            {
                "signal": "word_count_substance",
                "impact": round(min(30.0, (metrics.get("word_count", 0) / 500.0) * 30.0), 1),
                "description": f"Content word count: {metrics.get('word_count', 0)} words",
            },
        ]

        return {
            "layer_id": "L1",
            "layer_name": "Technical Accessibility",
            "weight": weight,
            "score": score,
            "status": "measured",
            "provenance": {
                "source": "sage",
                "source_engine": "sage-audit",
                "source_version": engine_ver,
                "methodology_version": MAVI_METHODOLOGY_VERSION,
                "timestamp_utc": timestamp_utc,
                "evidence_count": len(findings),
            },
            "contributors": contributors,
            "findings": [f.get("message", "") for f in findings[:5]] if findings else ["Technical SEO verified."],
        }

    @classmethod
    def _build_l2_layer(cls, aeo_res: Dict[str, Any], weight: float, timestamp_utc: str) -> Dict[str, Any]:
        """Builds L2 Semantic Extractability layer from SAGE AEO."""
        score = round(float(aeo_res.get("score", 0.0)), 1)
        engine_ver = aeo_res.get("engine", {}).get("version", "2.0.0")
        findings = aeo_res.get("findings", [])
        metrics = aeo_res.get("metrics", {})

        contributors = [
            {
                "signal": "aeo_structure_baseline",
                "impact": round(score * 0.50, 1),
                "description": f"SAGE AEO structure and extractability score: {score}/100",
            },
            {
                "signal": "schema_entity_depth",
                "impact": round(min(25.0, metrics.get("json_ld_blocks", 0) * 12.5), 1),
                "description": f"JSON-LD structured blocks: {metrics.get('json_ld_blocks', 0)}",
            },
            {
                "signal": "entity_types_coverage",
                "impact": round(min(25.0, len(metrics.get("entity_types", [])) * 10.0), 1),
                "description": f"Identified schema entities: {', '.join(metrics.get('entity_types', [])) or 'None'}",
            },
        ]

        return {
            "layer_id": "L2",
            "layer_name": "Semantic Extractability",
            "weight": weight,
            "score": score,
            "status": "measured",
            "provenance": {
                "source": "sage",
                "source_engine": "sage-audit",
                "source_version": engine_ver,
                "methodology_version": MAVI_METHODOLOGY_VERSION,
                "timestamp_utc": timestamp_utc,
                "evidence_count": len(findings),
            },
            "contributors": contributors,
            "findings": [f.get("message", "") for f in findings[:5]] if findings else ["Semantic extractability verified."],
        }

    @classmethod
    def _build_l3_layer(cls, entity_res: Dict[str, Any], target_brand: Optional[str], weight: float, timestamp_utc: str) -> Dict[str, Any]:
        """Builds L3 Entity Clarity layer from SAGE Entity Analysis."""
        score = round(float(entity_res.get("score", 0.0)), 1)
        engine_ver = entity_res.get("engine", {}).get("version", "2.0.0")
        findings = entity_res.get("findings", [])
        metrics = entity_res.get("metrics", {})
        entity_types = metrics.get("entity_types", [])

        contributors = [
            {
                "signal": "entity_graph_completeness",
                "impact": round(score * 0.40, 1),
                "description": f"Entity graph score: {score}/100",
            },
            {
                "signal": "core_entity_presence",
                "impact": 30.0 if any(t in ("Organization", "Person", "Product", "SoftwareApplication") for t in entity_types) else 10.0,
                "description": f"Core entity types: {', '.join(entity_types) or 'None'}",
            },
            {
                "signal": "brand_disambiguation",
                "impact": 30.0 if target_brand else 15.0,
                "description": f"Target entity disambiguation: {target_brand or 'Generic'}",
            },
        ]

        return {
            "layer_id": "L3",
            "layer_name": "Entity Clarity",
            "weight": weight,
            "score": score,
            "status": "measured",
            "provenance": {
                "source": "sage",
                "source_engine": "sage-audit",
                "source_version": engine_ver,
                "methodology_version": MAVI_METHODOLOGY_VERSION,
                "timestamp_utc": timestamp_utc,
                "evidence_count": len(findings),
            },
            "contributors": contributors,
            "findings": [f.get("message", "") for f in findings[:5]] if findings else ["Entity clarity verified."],
        }

    @classmethod
    def _build_l4_layer(cls, geo_res: Dict[str, Any], weight: float, timestamp_utc: str) -> Dict[str, Any]:
        """Builds L4 Retrieval / Citation Readiness layer from SAGE GEO & CSP diagnostics."""
        metrics = geo_res.get("metrics", {})
        csp_val = metrics.get("citation_survival_proxy")
        score = round(float(csp_val) if csp_val is not None else float(geo_res.get("score", 0.0)), 1)
        engine_ver = geo_res.get("engine", {}).get("version", "2.0.0")
        findings = geo_res.get("findings", [])

        contributors = [
            {
                "signal": "citation_survival_proxy",
                "impact": round(score * 0.60, 1),
                "description": f"SAGE Citation Survival Proxy (CSP): {score}/100 (E4 Heuristic Proxy)",
            },
            {
                "signal": "rag_chunk_count",
                "impact": round(min(20.0, metrics.get("chunk_count", 0) * 4.0), 1),
                "description": f"Extracted semantic chunks: {metrics.get('chunk_count', 0)}",
            },
            {
                "signal": "query_coverage",
                "impact": round(min(20.0, len(metrics.get("queries", [])) * 5.0), 1),
                "description": f"Generated synthetic queries: {len(metrics.get('queries', []))}",
            },
        ]

        return {
            "layer_id": "L4",
            "layer_name": "Retrieval / Citation Readiness",
            "weight": weight,
            "score": score,
            "status": "measured",
            "methodology_status": "diagnostic_heuristic_proxy",
            "provenance": {
                "source": "sage",
                "source_engine": "sage-audit",
                "source_version": engine_ver,
                "methodology_version": MAVI_METHODOLOGY_VERSION,
                "timestamp_utc": timestamp_utc,
                "evidence_count": len(findings),
            },
            "contributors": contributors,
            "findings": [f.get("message", "") for f in findings[:5]] if findings else ["Citation readiness diagnostic verified."],
        }

    @classmethod
    def _build_l5_layer(
        cls,
        experiment_data: Optional[Dict[str, Any]],
        target_brand: Optional[str],
        weight: float,
        timestamp_utc: str,
    ) -> Dict[str, Any]:
        """Builds L5 Observed AI Visibility layer from GEO-Scope experiment observations with quality guard."""
        if not experiment_data:
            return {
                "layer_id": "L5",
                "layer_name": "Observed AI Visibility",
                "weight": weight,
                "score": None,
                "status": "not_measured",
                "source_type": "not_measured",
                "provenance": {
                    "source": "geo-scope",
                    "source_engine": "geo-scope",
                    "source_version": "1.0.0",
                    "methodology_version": MAVI_METHODOLOGY_VERSION,
                    "timestamp_utc": timestamp_utc,
                    "evidence_count": 0,
                },
                "contributors": [],
                "findings": ["L5 Observed AI Visibility not measured (run a GEO-Scope benchmark experiment)."],
            }

        summary = experiment_data.get("summary", {})
        successful_obs = summary.get("successful_executions", 0) or summary.get("successful_observations", 0)
        total_obs = summary.get("total_executions", 0) or summary.get("total_prompts", 0)
        execution_mode = experiment_data.get("execution_mode") or summary.get("execution_mode", "simulate")
        experiment_id = experiment_data.get("experiment_id", "unknown_exp")
        providers = experiment_data.get("providers") or summary.get("providers", [])

        # Quality Guard
        if successful_obs == 0:
            return {
                "layer_id": "L5",
                "layer_name": "Observed AI Visibility",
                "weight": weight,
                "score": None,
                "status": "insufficient_data",
                "source_type": "insufficient_data",
                "provenance": {
                    "source": "geo-scope",
                    "source_engine": "geo-scope",
                    "source_version": "1.0.0",
                    "methodology_version": MAVI_METHODOLOGY_VERSION,
                    "timestamp_utc": timestamp_utc,
                    "evidence_count": 0,
                    "experiment_id": experiment_id,
                },
                "contributors": [],
                "findings": ["Zero successful observations recorded in GEO-Scope experiment (insufficient data)."],
            }

        # Calculate L5 score
        sov = float(summary.get("overall_sov", 0.0) or summary.get("target_brand_mention_rate", 0.0) or 0.0)
        top1 = float(summary.get("overall_top1_rate", 0.0) or summary.get("target_brand_top1_rate", 0.0) or 0.0)
        citation_rate = float(summary.get("overall_citation_rate", 0.0) or 0.0)

        l5_score = round((sov * 0.50) + (top1 * 0.30) + (citation_rate * 0.20), 1)

        is_live = str(execution_mode).lower() in ("live", "observed_live")
        source_type = "observed_live" if is_live else "synthetic"
        status = "measured" if is_live else "measured_synthetic"
        methodology_status = "observational_benchmark" if is_live else "non_observational"

        contributors = [
            {
                "signal": "share_of_model_mentions",
                "impact": round(sov * 0.50, 1),
                "description": f"Brand mention rate across model responses: {sov:.1f}%",
            },
            {
                "signal": "top1_recommendation_rate",
                "impact": round(top1 * 0.30, 1),
                "description": f"Top-1 primary recommendation frequency: {top1:.1f}%",
            },
            {
                "signal": "citation_absorption_rate",
                "impact": round(citation_rate * 0.20, 1),
                "description": f"Domain citation inclusion rate: {citation_rate:.1f}%",
            },
        ]

        return {
            "layer_id": "L5",
            "layer_name": "Observed AI Visibility",
            "weight": weight,
            "score": l5_score,
            "status": status,
            "source_type": source_type,
            "methodology_status": methodology_status,
            "provenance": {
                "source": "geo-scope",
                "source_engine": "geo-scope",
                "source_version": "1.0.0",
                "methodology_version": MAVI_METHODOLOGY_VERSION,
                "timestamp_utc": timestamp_utc,
                "evidence_count": successful_obs,
                "experiment_id": experiment_id,
                "execution_mode": execution_mode,
                "successful_observations": successful_obs,
                "total_observations": total_obs,
                "providers": providers,
            },
            "contributors": contributors,
            "findings": [
                f"Observed visibility: {sov:.1f}% mention rate across {successful_obs} observations ({source_type}).",
                f"Top-1 recommendation rate: {top1:.1f}%.",
            ],
        }

    @classmethod
    def _assess_confidence(
        cls,
        layers: Dict[str, Any],
        active_count: int,
        timestamp_utc: str,
    ) -> Dict[str, Any]:
        """Calculates deterministic confidence assessment based on observable evidence."""
        l5 = layers.get("L5", {})
        l5_source_type = l5.get("source_type", "not_measured")
        l5_obs = l5.get("provenance", {}).get("successful_observations", 0)

        factors = {
            "measured_layers_count": active_count,
            "total_layers": 5,
            "l5_source_type": l5_source_type,
            "l5_successful_observations": l5_obs,
            "freshness_days": 0,
        }

        if active_count == 5 and l5_source_type == "observed_live" and l5_obs >= 10:
            level = "High"
            score = 0.95
        elif active_count >= 4 and l5_source_type in ("observed_live", "not_measured"):
            level = "Medium"
            score = 0.75 if l5_source_type == "observed_live" else 0.65
        elif active_count >= 4 and l5_source_type == "synthetic":
            level = "Medium"
            score = 0.60
            factors["synthetic_l5_penalty"] = "Confidence reduced due to simulation-based L5."
        elif active_count >= 2:
            level = "Low"
            score = 0.40
        else:
            level = "Insufficient"
            score = 0.0

        return {
            "confidence_level": level,
            "confidence_score": score,
            "factors": factors,
        }

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

