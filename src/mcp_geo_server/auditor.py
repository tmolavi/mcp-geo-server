"""GEO Audit Core Logic."""
import json
import re
from typing import Dict, Any, List
from bs4 import BeautifulSoup


class GEOAuditor:
    """Core auditor for Generative Engine Optimization (GEO) standards."""

    @staticmethod
    def analyze_html(html_content: str, url: str) -> Dict[str, Any]:
        soup = BeautifulSoup(html_content, "html.parser")
        
        # 1. Check JSON-LD Schemas
        json_ld_scripts = soup.find_all("script", type="application/ld+json")
        schemas_found = []
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string if script.string else "{}")
                schemas_found.append(data)
            except Exception:
                pass

        # 2. DOM Cleanliness & Token-to-Information Ratio
        text_content = soup.get_text(separator=" ", strip=True)
        word_count = len(text_content.split())
        html_len = len(html_content)
        dom_cleanliness_score = round(min(10.0, (word_count * 100) / max(html_len, 1)), 2)

        # 3. Check Headings Structure
        headings = [h.text.strip() for h in soup.find_all(re.compile(r"^h[1-6]$"))]
        
        # 4. Evaluate RAG Chunk Readiness
        paragraphs = [p.text.strip() for p in soup.find_all("p") if len(p.text.strip()) > 30]
        self_contained_chunks = sum(1 for p in paragraphs if len(p.split()) >= 20 and len(p.split()) <= 100)

        return {
            "url": url,
            "l1_infrastructure": {
                "dom_cleanliness_score": dom_cleanliness_score,
                "word_count": word_count,
                "has_schema_markup": len(schemas_found) > 0,
                "schema_count": len(schemas_found),
                "schemas": schemas_found
            },
            "l3_rag_readiness": {
                "total_paragraphs": len(paragraphs),
                "self_contained_chunks": self_contained_chunks,
                "headings_count": len(headings),
                "heading_structure_sample": headings[:5]
            }
        }

    @staticmethod
    def calculate_mavi(l1: float, l2: float, l3: float, l4: float, l5: float) -> Dict[str, Any]:
        """Calculates Molavi AI Visibility Index (MAVI)."""
        score = round(l1 + l2 + l3 + l4 + l5, 2)
        grade = "A+" if score >= 85 else "A" if score >= 70 else "B" if score >= 50 else "C"
        return {
            "mavi_score": score,
            "max_score": 100.0,
            "grade": grade,
            "breakdown": {
                "L1_Infrastructure": l1,
                "L2_Entity_Authority": l2,
                "L3_RAG_Retrieval": l3,
                "L4_Citation_Trust": l4,
                "L5_Agentic_Mindshare": l5
            }
        }
