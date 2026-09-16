"""SAGE Adapter Layer for mcp-geo-server.

Acts as the single unified bridge between MCP protocol tool handlers and the
SAGE Audit & Measurement Engine (`sage-audit`).

Responsibilities:
- Invokes SAGE Core (`SageAuditor`) for 3-pillar analysis (SEO, AEO, GEO)
- Normalizes and shapes tool-specific responses for AI agent consumption
- Preserves full SAGE Evidence Taxonomy (E0–E5) and CSP diagnostic metadata
- Handles transport, input validation, and engine errors without fabricated scores

(c) 2026 Taqi Molavi — https://molavi.pro — MIT License
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

try:
    import sage_audit
    from sage_audit import SageAuditor, SageConfig
    from sage_audit._version import __version__ as SAGE_VERSION
    SAGE_AVAILABLE = True
except ImportError:  # pragma: no cover
    SAGE_AVAILABLE = False
    SAGE_VERSION = "unknown"
    SageAuditor = None
    SageConfig = None

from mcp_geo_server import __version__ as MCP_SERVER_VERSION

logger = logging.getLogger("mcp_geo_server.adapter")


class SageEngineError(Exception):
    """Raised when SAGE Core engine fails during audit execution."""
    pass


class SageAdapter:
    """Thin adapter invoking SAGE audit engine from MCP tool handlers."""

    def __init__(self, default_backend: str = "auto") -> None:
        if not SAGE_AVAILABLE:
            raise RuntimeError(
                "SAGE engine is unavailable. Install `sage-audit` to run mcp-geo-server."
            )
        self.default_backend = default_backend

    def _get_auditor(self, backend: Optional[str] = None, config: Optional[Any] = None) -> Any:
        cfg = config or SageConfig(embedding_backend=backend or self.default_backend)
        return SageAuditor(config=cfg)

    def _execute_audit(
        self,
        url: Optional[str] = None,
        html_content: Optional[str] = None,
        backend: Optional[str] = None,
        config: Optional[Any] = None,
    ) -> Any:
        """Executes SAGE audit on URL or raw HTML; raises on invalid inputs or engine failure."""
        if not url and not html_content:
            raise ValueError("Either 'url' or 'html_content' must be provided.")

        auditor = self._get_auditor(backend=backend, config=config)
        try:
            if html_content:
                target_url = url or "https://example.local/"
                return auditor.audit_html(html_content, url=target_url)
            else:
                return auditor.audit(str(url))
        except Exception as exc:
            logger.error("SAGE audit failed for url=%s: %s", url, exc, exc_info=True)
            raise SageEngineError(f"SAGE Core execution error: {exc}") from exc

    def audit_full(
        self,
        url: Optional[str] = None,
        html_content: Optional[str] = None,
        backend: Optional[str] = None,
        tool_name: str = "audit_full",
    ) -> Dict[str, Any]:
        """Full 3-pillar audit (SEO + AEO + GEO)."""
        report = self._execute_audit(url=url, html_content=html_content, backend=backend)
        return self._format_response(
            tool=tool_name,
            report=report,
            score=report.overall_score,
            grade=report.grade,
            findings=(
                report.seo.findings + report.aeo.findings + report.geo.findings
            ),
            metrics={
                "seo": report.seo.metrics,
                "aeo": report.aeo.metrics,
                "geo": report.geo.metrics,
            },
            artifacts=report.artifacts,
            metadata={"duration_ms": report.duration_ms, "page": report.page},
        )

    def technical_seo(
        self,
        url: Optional[str] = None,
        html_content: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Pillar 1: Technical SEO analysis."""
        report = self._execute_audit(url=url, html_content=html_content)
        seo = report.seo
        return self._format_response(
            tool="technical_seo",
            report=report,
            score=seo.score,
            grade=seo.grade,
            findings=seo.findings,
            metrics=seo.metrics,
            recommendations=[f.recommendation for f in seo.actionable()],
        )

    def aeo_readiness(
        self,
        url: Optional[str] = None,
        html_content: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Pillar 2: Answer Engine Optimization (AEO) analysis."""
        report = self._execute_audit(url=url, html_content=html_content)
        aeo = report.aeo
        return self._format_response(
            tool="aeo_readiness",
            report=report,
            score=aeo.score,
            grade=aeo.grade,
            findings=aeo.findings,
            metrics=aeo.metrics,
            recommendations=[f.recommendation for f in aeo.actionable()],
        )

    def geo_readiness(
        self,
        url: Optional[str] = None,
        html_content: Optional[str] = None,
        backend: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Pillar 3: Generative Engine Optimization (GEO) & RAG simulation."""
        report = self._execute_audit(url=url, html_content=html_content, backend=backend)
        geo = report.geo
        return self._format_response(
            tool="geo_readiness",
            report=report,
            score=geo.score,
            grade=geo.grade,
            findings=geo.findings,
            metrics=geo.metrics,
            artifacts=geo.artifacts,
            recommendations=[f.recommendation for f in geo.actionable()],
        )

    def entity_analysis(
        self,
        url: Optional[str] = None,
        html_content: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Detailed entity graph, Schema.org completeness, and sameAs authority signals."""
        report = self._execute_audit(url=url, html_content=html_content)
        aeo = report.aeo
        entity_findings = [
            f for f in aeo.findings
            if f.check_id in (
                "aeo.jsonld_presence",
                "aeo.entity_graph",
                "aeo.entity_completeness",
                "aeo.authority_sameas",
                "aeo.entity_linking",
            )
        ]
        return self._format_response(
            tool="entity_analysis",
            report=report,
            score=round(sum(f.score * f.weight for f in entity_findings) / max(sum(f.weight for f in entity_findings), 1.0) * 100.0, 1),
            grade=aeo.grade,
            findings=entity_findings,
            metrics={
                "json_ld_blocks": aeo.metrics.get("json_ld_blocks"),
                "entity_nodes": aeo.metrics.get("entity_nodes"),
                "entity_types": aeo.metrics.get("entity_types"),
            },
        )

    def citation_readiness(
        self,
        url: Optional[str] = None,
        html_content: Optional[str] = None,
        backend: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Citation Survival Proxy (CSP), direct-answer density, and passage chunk geometry."""
        report = self._execute_audit(url=url, html_content=html_content, backend=backend)
        citation_findings = [
            f for f in report.geo.findings
            if f.check_id in ("geo.citation_survival", "geo.retrieval_focus", "geo.retrieval_coverage", "geo.chunk_shape")
        ] + [
            f for f in report.aeo.findings
            if f.check_id == "aeo.direct_answer_density"
        ]
        csp = report.geo.metrics.get("citation_survival_proxy", report.geo.metrics.get("citation_survival_probability"))
        return self._format_response(
            tool="citation_readiness",
            report=report,
            score=csp if csp is not None else 0.0,
            grade=report.geo.grade,
            findings=citation_findings,
            metrics={
                "citation_survival_proxy": csp,
                "csp_details": report.geo.metrics.get("csp_details"),
                "avg_semantic_entropy": report.geo.metrics.get("avg_semantic_entropy"),
                "retrieval_coverage": report.geo.metrics.get("retrieval_coverage"),
                "section_answer_scores": report.aeo.metrics.get("section_answer_scores"),
            },
        )

    def generate_llms_txt(
        self,
        url: Optional[str] = None,
        html_content: Optional[str] = None,
        backend: Optional[str] = None,
    ) -> str:
        """Generates standardized llms.txt manifest via SAGE GEO engine."""
        report = self._execute_audit(url=url, html_content=html_content, backend=backend)
        return report.artifacts.get("llms.txt", "")

    def get_capabilities(self) -> Dict[str, Any]:
        """Discovers active SAGE engine capabilities."""
        return {
            "status": "success",
            "server": "mcp-geo-server",
            "server_version": MCP_SERVER_VERSION,
            "engine": {
                "name": "sage",
                "version": SAGE_VERSION,
                "available": SAGE_AVAILABLE,
                "methodology_version": "2.0.0",
            },
            "capabilities": [
                "audit_full",
                "technical_seo",
                "aeo_readiness",
                "geo_readiness",
                "entity_analysis",
                "citation_readiness",
                "generate_llms_txt",
                "mavi_measurement",
            ],
            "evidence_taxonomy": ["E0", "E1", "E2", "E3", "E4", "E5"],
        }

    def _format_response(
        self,
        tool: str,
        report: Any,
        score: Optional[float] = None,
        grade: Optional[str] = None,
        findings: Optional[List[Any]] = None,
        metrics: Optional[Dict[str, Any]] = None,
        artifacts: Optional[Dict[str, Any]] = None,
        recommendations: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Structures uniform machine-readable JSON output preserving evidence taxonomy."""
        findings_list = []
        if findings:
            for f in findings:
                f_dict = f.model_dump(mode="json") if hasattr(f, "model_dump") else f
                findings_list.append(f_dict)

        recs = recommendations or []
        if not recs and findings:
            recs = [f.recommendation for f in findings if getattr(f, "recommendation", None)]

        res: Dict[str, Any] = {
            "tool": tool,
            "status": "success",
            "engine": {
                "name": "sage",
                "version": SAGE_VERSION,
                "methodology_version": getattr(report, "methodology_version", "2.0.0"),
            },
            "server_version": MCP_SERVER_VERSION,
            "url": getattr(report, "final_url", None) or getattr(report, "url", ""),
            "score": score,
            "grade": grade,
            "findings": findings_list,
            "recommendations": recs,
            "metrics": metrics or {},
        }
        if artifacts:
            res["artifacts"] = artifacts
        if metadata:
            res["metadata"] = metadata
        return res
