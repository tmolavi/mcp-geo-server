# MCP GEO Server (`mcp-geo-server`)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![MCP Specification](https://img.shields.io/badge/MCP-1.0.0-green.svg)](https://modelcontextprotocol.io)
[![SAGE Core](https://img.shields.io/badge/Engine-SAGE%20Audit%20v2.0-blueviolet.svg)](https://github.com/tmolavi/sage-audit)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A production-grade **Model Context Protocol (MCP) Server** that exposes the **SAGE (Search & AI-Engine Guided Evaluation)** auditing and measurement engine to AI agents (Claude Desktop, Cursor, Antigravity, custom agents).

Developed by **[Taqi Molavi](https://molavi.pro)** (Molavi R&D Think Tank) as the official tool-exposure and protocol adapter layer for the **SAGE Core** framework.

---

## 🏛️ Architecture: Thin SAGE Adapter

`mcp-geo-server` implements a strict separation of concerns:

```text
AI Agent / Claude Desktop / Cursor / Antigravity
                     │
                     ▼ (MCP JSON-RPC Protocol)
           mcp-geo-server (Protocol & Transport Layer)
                     │
                     ▼ (Python API / SageAdapter)
            SAGE Core (`sage-audit` Engine)
         ┌───────────┼───────────┐
         ▼           ▼           ▼
      Pillar 1    Pillar 2    Pillar 3
    Technical SEO  Entity AEO   GEO & RAG
```

* **`mcp-geo-server`**: Responsible exclusively for MCP protocol negotiation, tool definitions, transport error handling, and standard JSON shaping.
* **`sage-audit`**: The single source of truth for auditing, semantic embedding, RAG simulation, Citation Survival Proxy (CSP), and the SAGE Evidence Taxonomy (E0–E5).

---

## 🛠️ MCP Tools Reference

### Full Audits
* **`audit_url(url, embedding_backend="auto")`**  
  Performs a complete 3-pillar audit (Technical SEO, Entity AEO, GEO Readiness) against a live URL.
* **`audit_html(html_content, url="https://example.local/", embedding_backend="auto")`**  
  Performs a complete 3-pillar audit on raw HTML strings (ideal for local development, CI/CD, or offline snapshots).

### Pillar-Specific Tools
* **`technical_seo(url=None, html_content=None)`**  
  Pillar 1: Audits DOM hygiene, clean heading outlines, canonical tags, AI crawler directives (GPTBot, ClaudeBot, PerplexityBot in robots.txt), and header policies.
* **`aeo_readiness(url=None, html_content=None)`**  
  Pillar 2: Evaluates Answer Engine Optimization including JSON-LD schema depth, sameAs authority graph connections, and direct-answer density.
* **`geo_readiness(url=None, html_content=None, embedding_backend="auto")`**  
  Pillar 3: Generative Engine Optimization with RAG chunking simulation, semantic density, and Citation Survival Proxy (CSP).
* **`entity_analysis(url=None, html_content=None)`**  
  Deep analysis of linked-data schemas (Organization, Person, Product, Article), entity disambiguation, and knowledge graph signals.
* **`citation_readiness(url=None, html_content=None, embedding_backend="auto")`**  
  Evaluates fact density, source attribution, numeric verification anchors, and Citation Survival Proxy diagnostic factors.

### Utilities & Capabilities
* **`generate_llms_txt(domain, title, description, key_sections=None)`**  
  Generates a clean, spec-compliant `/llms.txt` file for generative engines and AI crawlers.
* **`get_capabilities()`**  
  Returns supported pillars, available vector embedding backends, SAGE engine version, and active evidence taxonomy definitions.

### Legacy & Backward Compatibility
* **`audit_geo_url(url, html_content)`** — Forwards to `audit_html` with deprecation notice.
* **`calculate_mavi_score(...)`** — Legacy manual-input MAVI calculator (marked `mode: manual_override`).
* **`measure_mavi(...)`** — 5-layer MAVI measurement engine with SAGE L1–L4 automation.

---

## 📊 Evidence Taxonomy & CSP Diagnostics

Every finding and metric exposed by `mcp-geo-server` carries SAGE Evidence Taxonomy levels to guarantee transparency:

| Level | Classification | Meaning |
|---|---|---|
| **E0** | Fact | Deterministic binary technical verification (HTTP status, canonical match). |
| **E1** | Standard | Backed by open published specifications (Schema.org, robots.txt RFC 9309). |
| **E2** | Documented | Directly verified by official documentation from Google, OpenAI, Anthropic. |
| **E3** | Empirical | Backed by published empirical benchmark findings. |
| **E4** | Heuristic | Industry-standard structural optimization practices. |
| **E5** | Hypothesis | Experimental or uncalibrated exploratory heuristic. |

**Citation Survival Proxy (CSP)** findings are clearly exposed as diagnostic indices and proxy metrics—never misrepresented as uncalibrated citation probabilities.

---

## 🚀 Installation

```bash
# Install with uv (Recommended)
uv pip install mcp-geo-server

# Or with pip
pip install mcp-geo-server
```

---

## ⚙️ MCP Client Configuration

### Claude Desktop
Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "geo-auditor": {
      "command": "uv",
      "args": [
        "run",
        "--package",
        "mcp-geo-server",
        "mcp-geo-server"
      ]
    }
  }
}
```

### Cursor IDE
1. Open Settings -> **Features** -> **MCP**.
2. Click **+ Add New MCP Server**.
3. **Command:** `uv run --package mcp-geo-server mcp-geo-server`

---

## 🐍 Python Usage

```python
from mcp_geo_server.adapter import SageAdapter

adapter = SageAdapter()

# Full audit
result = adapter.audit_full(url="https://example.com")
print(f"Overall Score: {result['score']}/100 ({result['grade']})")

# Pillar 3: GEO & RAG Readiness
geo = adapter.geo_readiness(url="https://example.com")
print(f"CSP Diagnostic: {geo['metrics']['citation_survival_proxy']}")
```

---

## 🧪 Testing

```bash
uv run pytest -v
```

---

## 🏛️ Ecosystem

MCP GEO Server operates as the protocol integration component of the **Molavi AI Visibility Stack**:

- **Discovery**: [AnswerPath GEO](https://github.com/tmolavi/answerpath-geo)
- **Measurement**: [GEO-Scope](https://github.com/tmolavi/geo-scope)
- **Diagnostics**: [SAGE Audit](https://github.com/tmolavi/sage-audit)
- **Action**: [SiteProbe](https://github.com/tmolavi/siteprobe)
- **Protocol**: [MCP GEO Server](https://github.com/tmolavi/mcp-geo-server)

## 📖 Runnable Python Client Example

Run the bundled MCP adapter example script:
```bash
python examples/mcp_client_example.py
```

---

## 📄 License & Author

Developed by **Taghi Molavi** — [molavi.pro](https://molavi.pro)  
MIT License — Copyright (c) 2026 Taghi Molavi

