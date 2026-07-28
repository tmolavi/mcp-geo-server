"""MCP GEO Server Main Entry Point."""
from mcp.server import MCPServer
from mcp_geo_server.auditor import GEOAuditor
import json

app = MCPServer("mcp-geo-server")

@app.tool()
def audit_geo_url(url: str, html_content: str) -> str:
    """Audits a webpage for Generative Engine Optimization (GEO) standards and RAG readiness based on The Molavi GEO Pyramid.

    Args:
        url: The target URL to audit.
        html_content: Raw HTML content of the webpage to analyze.
    """
    result = GEOAuditor.analyze_html(html_content, url)
    return json.dumps(result, indent=2, ensure_ascii=False)

@app.tool()
def calculate_mavi_score(
    l1_infrastructure: float,
    l2_entity_authority: float,
    l3_rag_retrieval: float,
    l4_citation_trust: float,
    l5_agentic_mindshare: float
) -> str:
    """Calculates the Molavi AI Visibility Index (MAVI) score for an entity or brand.

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
        l5_agentic_mindshare
    )
    return json.dumps(result, indent=2, ensure_ascii=False)

@app.tool()
def generate_llms_txt_template(domain: str, title: str, description: str) -> str:
    """Generates a standardized /llms.txt file content for a domain.

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

if __name__ == "__main__":
    app.run("stdio")
