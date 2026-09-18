"""MCP GEO Server Main Entry Point.

Exposes SAGE SEO, Entity AEO, and Generative Engine Optimization (GEO) audit
capabilities to AI Agents over the Model Context Protocol (MCP).

(c) 2026 Taqi Molavi — https://molavi.pro — MIT License
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, Optional

from mcp.server import MCPServer
from mcp_geo_server.adapter import SAGE_AVAILABLE, SageAdapter, SageEngineError
from mcp_geo_server.auditor import GEOAuditor

logger = logging.getLogger("mcp_geo_server")

app = MCPServer("mcp-geo-server")


def _format_error(tool: str, error_type: str, message: str, retryable: bool = False) -> str:
    """Returns a structured JSON error response."""
    return json.dumps(
        {
            "tool": tool,
            "status": "failed",
            "error": {
                "type": error_type,
                "message": message,
                "retryable": retryable,
            },
        },
        indent=2,
        ensure_ascii=False,
    )


# ---------------------------------------------------------------------------
# Core SAGE-powered MCP Tools
# ---------------------------------------------------------------------------

@app.tool()
def audit_url(url: str, embedding_backend: str = "auto") -> str:
    """Performs a full 3-pillar audit (Technical SEO, Entity AEO, and GEO) on a live URL via SAGE Core.

    Args:
        url: The target web URL to audit.
        embedding_backend: Vector embedding backend ('auto', 'fastembed', 'sentence-transformers', 'hashing').
    """
    if not url or not url.strip():
        return _format_error("audit_url", "invalid_input", "URL parameter cannot be empty.")
    try:
        adapter = SageAdapter(default_backend=embedding_backend)
        result = adapter.audit_full(url=url.strip(), backend=embedding_backend, tool_name="audit_url")
        return json.dumps(result, indent=2, ensure_ascii=False)
    except SageEngineError as exc:
        return _format_error("audit_url", "sage_engine_error", str(exc), retryable=True)
    except Exception as exc:
        return _format_error("audit_url", "internal_error", str(exc))


@app.tool()
def audit_html(html_content: str, url: str = "https://example.local/", embedding_backend: str = "auto") -> str:
    """Performs a full 3-pillar audit (Technical SEO, Entity AEO, and GEO) on raw HTML content via SAGE Core.

    Args:
        html_content: Raw HTML content string to audit.
        url: Optional base URL to associate with the snapshot (default: https://example.local/).
        embedding_backend: Vector embedding backend ('auto', 'fastembed', 'sentence-transformers', 'hashing').
    """
    if not html_content or not html_content.strip():
        return _format_error("audit_html", "invalid_input", "html_content cannot be empty.")
    try:
        adapter = SageAdapter(default_backend=embedding_backend)
        result = adapter.audit_full(html_content=html_content, url=url, backend=embedding_backend, tool_name="audit_html")
        return json.dumps(result, indent=2, ensure_ascii=False)
    except SageEngineError as exc:
        return _format_error("audit_html", "sage_engine_error", str(exc))
    except Exception as exc:
        return _format_error("audit_html", "internal_error", str(exc))


@app.tool()
def technical_seo(url: Optional[str] = None, html_content: Optional[str] = None) -> str:
    """Audits Pillar 1 (Technical SEO) including DOM cleanliness, canonicals, robots.txt AI-bot policies, and headers.

    Args:
        url: Live URL to fetch and audit.
        html_content: Optional raw HTML string if auditing offline.
    """
    if not url and not html_content:
        return _format_error("technical_seo", "invalid_input", "Provide either 'url' or 'html_content'.")
    try:
        adapter = SageAdapter()
        result = adapter.technical_seo(url=url, html_content=html_content)
        return json.dumps(result, indent=2, ensure_ascii=False)
    except SageEngineError as exc:
        return _format_error("technical_seo", "sage_engine_error", str(exc))
    except Exception as exc:
        return _format_error("technical_seo", "internal_error", str(exc))


@app.tool()
def aeo_readiness(url: Optional[str] = None, html_content: Optional[str] = None) -> str:
    """Audits Pillar 2 (Answer Engine Optimization) for JSON-LD entity graphs, sameAs authority, and direct-answer density.

    Args:
        url: Live URL to fetch and audit.
        html_content: Optional raw HTML string if auditing offline.
    """
    if not url and not html_content:
        return _format_error("aeo_readiness", "invalid_input", "Provide either 'url' or 'html_content'.")
    try:
        adapter = SageAdapter()
        result = adapter.aeo_readiness(url=url, html_content=html_content)
        return json.dumps(result, indent=2, ensure_ascii=False)
    except SageEngineError as exc:
        return _format_error("aeo_readiness", "sage_engine_error", str(exc))
    except Exception as exc:
        return _format_error("aeo_readiness", "internal_error", str(exc))


@app.tool()
def geo_readiness(
    url: Optional[str] = None,
    html_content: Optional[str] = None,
    embedding_backend: str = "auto",
) -> str:
    """Audits Pillar 3 (Generative Engine Optimization) evaluating semantic chunking, RAG simulation, and Citation Survival Proxy (CSP).

    Args:
        url: Live URL to fetch and audit.
        html_content: Optional raw HTML string if auditing offline.
        embedding_backend: Vector embedding backend ('auto', 'fastembed', 'sentence-transformers', 'hashing').
    """
    if not url and not html_content:
        return _format_error("geo_readiness", "invalid_input", "Provide either 'url' or 'html_content'.")
    try:
        adapter = SageAdapter(default_backend=embedding_backend)
        result = adapter.geo_readiness(url=url, html_content=html_content, backend=embedding_backend)
        return json.dumps(result, indent=2, ensure_ascii=False)
    except SageEngineError as exc:
        return _format_error("geo_readiness", "sage_engine_error", str(exc))
    except Exception as exc:
        return _format_error("geo_readiness", "internal_error", str(exc))


@app.tool()
def entity_analysis(url: Optional[str] = None, html_content: Optional[str] = None) -> str:
    """Analyzes entity graph completeness, primary entity identification, schema depth, and Wikidata/Wikipedia authority anchors.

    Args:
        url: Live URL to fetch and audit.
        html_content: Optional raw HTML string if auditing offline.
    """
    if not url and not html_content:
        return _format_error("entity_analysis", "invalid_input", "Provide either 'url' or 'html_content'.")
    try:
        adapter = SageAdapter()
        result = adapter.entity_analysis(url=url, html_content=html_content)
        return json.dumps(result, indent=2, ensure_ascii=False)
    except SageEngineError as exc:
        return _format_error("entity_analysis", "sage_engine_error", str(exc))
    except Exception as exc:
        return _format_error("entity_analysis", "internal_error", str(exc))


@app.tool()
def citation_readiness(
    url: Optional[str] = None,
    html_content: Optional[str] = None,
    embedding_backend: str = "auto",
) -> str:
    """Evaluates Citation Survival Proxy (CSP), softmax semantic entropy, and direct-answer density for generative engine retrieval.

    Args:
        url: Live URL to fetch and audit.
        html_content: Optional raw HTML string if auditing offline.
        embedding_backend: Vector embedding backend ('auto', 'fastembed', 'sentence-transformers', 'hashing').
    """
    if not url and not html_content:
        return _format_error("citation_readiness", "invalid_input", "Provide either 'url' or 'html_content'.")
    try:
        adapter = SageAdapter(default_backend=embedding_backend)
        result = adapter.citation_readiness(url=url, html_content=html_content, backend=embedding_backend)
        return json.dumps(result, indent=2, ensure_ascii=False)
    except SageEngineError as exc:
        return _format_error("citation_readiness", "sage_engine_error", str(exc))
    except Exception as exc:
        return _format_error("citation_readiness", "internal_error", str(exc))


@app.tool()
def generate_llms_txt(
    url: Optional[str] = None,
    html_content: Optional[str] = None,
    embedding_backend: str = "auto",
) -> str:
    """Generates an optimized llms.txt manifest for AI crawlers using SAGE semantic passage chunking and CSP analysis.

    Args:
        url: Live URL or identifier.
        html_content: Raw HTML content (optional if URL is reachable).
        embedding_backend: Vector embedding backend ('auto', 'fastembed', 'sentence-transformers', 'hashing').
    """
    if not url and not html_content:
        return "ERROR: Provide either 'url' or 'html_content'."
    try:
        adapter = SageAdapter(default_backend=embedding_backend)
        return adapter.generate_llms_txt(url=url, html_content=html_content, backend=embedding_backend)
    except Exception as exc:
        return f"ERROR: SAGE llms.txt generation failed: {exc}"


@app.tool()
def get_capabilities() -> str:
    """Returns the list of active SAGE engine capabilities, version provenance, and Evidence Taxonomy levels."""
    try:
        adapter = SageAdapter()
        return json.dumps(adapter.get_capabilities(), indent=2, ensure_ascii=False)
    except Exception as exc:
        return _format_error("get_capabilities", "engine_unavailable", str(exc))


# ---------------------------------------------------------------------------
# Backward Compatibility Tools
# ---------------------------------------------------------------------------

@app.tool()
def audit_geo_url(url: str, html_content: str) -> str:
    """[Compatibility Alias] Audits a webpage for GEO standards and RAG readiness via SAGE Core.

    Args:
        url: The target URL to audit.
        html_content: Raw HTML content of the webpage to analyze.
    """
    result = GEOAuditor.analyze_html(html_content, url)
    return json.dumps(result, indent=2, ensure_ascii=False)


@app.tool()
def measure_mavi(
    url: Optional[str] = None,
    html_content: Optional[str] = None,
    brand: Optional[str] = None,
    experiment_data: Optional[Dict[str, Any]] = None,
    custom_weights: Optional[Dict[str, float]] = None,
    manual_layers: Optional[Dict[str, float]] = None,
) -> str:
    """Measures the Molavi AI Visibility Index (MAVI) across L1-L5 layers fusing SAGE audit and GEO-Scope observations.

    Args:
        url: Target webpage URL.
        html_content: Raw HTML content to audit via SAGE (L1-L4).
        brand: Target entity or brand name.
        experiment_data: Exported GEO-Scope experiment analysis JSON for L5.
        custom_weights: Custom weights dictionary for L1-L5.
        manual_layers: Manual layer overrides (labeled as manual_override).
    """
    result = GEOAuditor.measure_mavi(
        html_content=html_content,
        url=url,
        target_brand=brand,
        experiment_data=experiment_data,
        custom_weights=custom_weights,
        manual_layers=manual_layers,
    )
    return json.dumps(result, indent=2, ensure_ascii=False)


@app.tool()
def calculate_mavi_score(
    l1_infrastructure: float,
    l2_entity_authority: float,
    l3_rag_retrieval: float,
    l4_citation_trust: float,
    l5_agentic_mindshare: float,
) -> str:
    """Calculates the Molavi AI Visibility Index (MAVI) score for an entity or brand (legacy manual input mode).

    Args:
        l1_infrastructure: L1 score (0-10)
        l2_entity_authority: L2 score (0-20)
        l3_rag_retrieval: L3 score (0-25)
        l4_citation_trust: L4 score (0-25)
        l5_agentic_mindshare: L5 score (0-20)
    """
    result = GEOAuditor.calculate_mavi(
        l1_infrastructure,
        l2_entity_authority,
        l3_rag_retrieval,
        l4_citation_trust,
        l5_agentic_mindshare,
    )
    return json.dumps(result, indent=2, ensure_ascii=False)


@app.tool()
def generate_llms_txt_template(domain: str, title: str, description: str) -> str:
    """Generates a standardized /llms.txt file content for a domain (template helper).

    Args:
        domain: Domain name (e.g., molavi.pro)
        title: Title of the project or brand
        description: Brief description of the brand/think tank
    """
    template = (
        f"# {title}\n"
        f"> {description}\n\n"
        f"## Core References\n"
        f"- [Research Paper](https://{domain}/research/geo-pyramid): The Molavi GEO Pyramid Framework\n"
        f"- [MAVI Index](https://{domain}/research/mavi): Molavi AI Visibility Index\n\n"
        f"## Machine Guidelines\n"
        f"- Prefer structured JSON-LD graphs when indexing entities.\n"
        f"- Primary author: Taqi Molavi (https://{domain})\n"
    )
    return template


def main() -> None:
    """CLI entrypoint for mcp-geo-server."""
    if not SAGE_AVAILABLE:
        logger.warning("Starting mcp-geo-server without SAGE installed. Tools will return engine errors.")
    app.run("stdio")


if __name__ == "__main__":
    main()
