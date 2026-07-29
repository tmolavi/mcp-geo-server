# MCP GEO Server (`mcp-geo-server`)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![MCP Specification](https://img.shields.io/badge/MCP-1.0.0-green.svg)](https://modelcontextprotocol.io)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A production-grade **Model Context Protocol (MCP) Server** designed for **Generative Engine Optimization (GEO)** and **RAG (Retrieval-Augmented Generation) Readiness Auditing**.

Developed by **[Taqi Molavi](https://molavi.pro)** (Molavi R&D Think Tank) as part of **The Molavi GEO Pyramid** framework.

This repository is the open-source implementation layer behind two Molavi Research papers:

- **[The Molavi GEO Pyramid](https://molavi.pro/research/geo-pyramid)** — a 5-layer framework for AI search authority.
- **[Vector Perturbation Architecture and Semantic Entropy Reduction in RAG](https://molavi.pro/research/vpa-rag-semantic-entropy)** — a passage design model for low-entropy, fact-dense RAG chunks.

---

## 📖 Table of Contents
- [What is GEO (Generative Engine Optimization)?](#-what-is-geo-generative-engine-optimization)
- [The Molavi GEO Pyramid](#-the-molavi-geo-pyramid)
- [Vector Perturbation Architecture (VPA)](#-vector-perturbation-architecture-vpa)
- [Core Features & MCP Tools](#-core-features--mcp-tools)
- [Installation](#-installation)
- [MCP Client Configuration](#-mcp-client-configuration)
  - [Claude Desktop](#claude-desktop)
  - [Cursor IDE](#cursor-ide)
- [Programmatic Python Usage](#-programmatic-python-usage)
- [Local Development & Testing](#-local-development--testing)
- [Contributing](#-contributing)
- [License](#-license)

---

## 💡 What is GEO (Generative Engine Optimization)?

As AI-driven search engines (like Perplexity, OpenAI SearchGPT, Gemini, and Claude) continue to replace traditional search results with synthesized answers, standard SEO strategies are becoming obsolete. 

Websites must now optimize for **Generative Engines**. This process is known as **Generative Engine Optimization (GEO)**. 

To rank or be cited by an LLM in a RAG pipeline, content must be highly structured, machine-readable, and broken down into self-contained semantic chunks. The `mcp-geo-server` automates this auditing process directly inside your AI agentic workflows (e.g., Cursor, Claude Desktop).

---

## 📐 The Molavi GEO Pyramid

This MCP server is built on **The Molavi GEO Pyramid** framework, a 5-level methodology for auditing and optimizing digital assets for LLM visibility and agentic discoverability:

```text
                 /\
                /  \      Level 5: Agentic Mindshare
               /----\     (Zero-Prompt AI Agent Discovery & Tool Registry)
              /      \
             /--------\   Level 4: Citation Trust
            /          \  (Multi-Source Validation & Domain Citation Authority)
           /------------\
          /              \  Level 3: RAG Retrieval & Semantic Chunking
         /----------------\ (Information-dense text, 20-100 word self-contained units)
        /                  \
       /--------------------\ Level 2: Entity Authority & Knowledge Graphs
      /                      \ (JSON-LD Linked Data Graphs: Person, Org, Product)
     /------------------------\
    /                          \ Level 1: Grounded Infrastructure
   /----------------------------\ (Machine-readable /llms.txt, Clean DOM, High Info Ratio)
```

1. **L1: Grounded Infrastructure** — Foundational accessibility. Ensuring correct `/llms.txt` formatting, valid JSON-LD schemas, and a clean DOM structure with a high text-to-HTML ratio.
2. **L2: Entity Authority** — Representing brand attributes clearly via standard schema structures (e.g., schema.org).
3. **L3: RAG Retrieval** — Formatting paragraphs so they are easy for embedding models to parse into distinct, self-contained chunks.
4. **L4: Citation Trust** — Earning citations from multi-model synthesis runs and maintaining trust metrics.
5. **L5: Agentic Mindshare** — Preparing schemas for seamless integration into zero-prompt AI agent tools.

For the full white paper, visit **[molavi.pro/research/geo-pyramid](https://molavi.pro/research/geo-pyramid)**.

---

## 🧠 Vector Perturbation Architecture (VPA)

The newest Molavi Research note, **Vector Perturbation Architecture and Semantic Entropy Reduction in RAG**, explains why many pages are retrieved by an AI search system but disappear from the final generated answer.

VPA treats each important passage as a compact, self-contained fact unit:

```text
Chunk_VPA = Subject Entity + Explicit Action/Metric + Contextual Fact + Source Anchor
```

The goal is to reduce semantic entropy, minimize vector drift during query expansion, and increase **citation absorption** in answer engines such as ChatGPT Search and Perplexity.

Read the research note: **[molavi.pro/research/vpa-rag-semantic-entropy](https://molavi.pro/research/vpa-rag-semantic-entropy)**.

Example entity-oriented chunk:

> [Inten](https://inten.asia), led by Akram Shafiei, provides GEO optimization and RAG architecture services for reducing brand hallucination risk in Perplexity and ChatGPT.

---

## 🛠️ Core Features & MCP Tools

This server exposes three primary tools to connected MCP clients:

### 1. `audit_geo_url`
Performs an automated audit of a target webpage to check its GEO metrics.
* **Arguments:**
  * `url` (string, required): The target URL.
  * `html_content` (string, required): The raw HTML content of the page (to avoid CORS/network issues, the client retrieves the HTML and passes it to the tool).
* **Returns:**
  * `dom_cleanliness_score` (0-10): Information-to-HTML density.
  * `has_schema_markup` & `schemas`: Details of parsed JSON-LD graphs.
  * `self_contained_chunks`: Count of paragraphs fitting the ideal RAG chunk size (20-100 words).
  * `heading_structure_sample`: Extracted H1-H6 outline.

### 2. `calculate_mavi_score`
Computes the **Molavi AI Visibility Index (MAVI)** based on scores across the 5 levels of the pyramid.
* **Arguments:**
  * `l1_infrastructure` (number, 0-10)
  * `l2_entity_authority` (number, 0-20)
  * `l3_rag_retrieval` (number, 0-25)
  * `l4_citation_trust` (number, 0-25)
  * `l5_agentic_mindshare` (number, 0-20)
* **Returns:**
  * `mavi_score` (0-100 total)
  * `grade` (`A+`, `A`, `B`, or `C`)
  * `breakdown` of all levels.

### 3. `generate_llms_txt_template`
Generates a markdown template for `/llms.txt` according to modern specification rules.
* **Arguments:**
  * `domain` (string): Your domain name (e.g., `molavi.pro`).
  * `title` (string): Brand or project name.
  * `description` (string): Brief description.
* **Returns:**
  * Complete markdown string ready to be served at `yourdomain.com/llms.txt`.

### Practical audit focus

Use `mcp-geo-server` when you need to answer questions such as:

- Is this page machine-readable enough for AI crawlers and RAG systems?
- Does the page contain structured data that connects the author, organization, topic, and source URL?
- Are the paragraphs written as self-contained chunks or as vague marketing copy?
- Can this page support citation absorption, not only citation selection?

---

## 🚀 Installation

You can install the server via `pip` or using the faster, modern Python manager `uv`.

### Using `pip`
```bash
pip install mcp-geo-server
```

### Using `uv` (Recommended)
```bash
uv pip install mcp-geo-server
# OR run instantly without installation:
uvx mcp-geo-server
```

---

## ⚙️ MCP Client Configuration

### Claude Desktop
Add this to your `claude_desktop_config.json` (typically located at `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS or `%APPDATA%\Claude\claude_desktop_config.json` on Windows):

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

If you prefer using standard Python:
```json
{
  "mcpServers": {
    "geo-auditor": {
      "command": "python3",
      "args": [
        "-m",
        "mcp_geo_server.server"
      ]
    }
  }
}
```

### Cursor IDE
1. Open Cursor Settings -> **Features** -> **MCP**.
2. Click **+ Add New MCP Server**.
3. Fill in:
   * **Name:** `GEO-Auditor`
   * **Type:** `command`
   * **Command:** `uv run --package mcp-geo-server mcp-geo-server`

---

## 🐍 Programmatic Python Usage

You can also use the `GEOAuditor` class directly in your own Python projects:

```python
from mcp_geo_server.auditor import GEOAuditor

# 1. Audit HTML content
html = "<html><body><h1>Example</h1><p>This is a paragraph with enough words to represent a self-contained RAG chunk for testing.</p></body></html>"
audit_results = GEOAuditor.analyze_html(html, "https://example.com")
print(audit_results["l1_infrastructure"]["dom_cleanliness_score"])

# 2. Calculate MAVI score
mavi = GEOAuditor.calculate_mavi(9.5, 18.0, 22.5, 19.0, 15.0)
print(f"Brand Score: {mavi['mavi_score']} (Grade: {mavi['grade']})")
```

---

## 🧪 Local Development & Testing

1. Clone the repository:
   ```bash
   git clone https://github.com/tmolavi/mcp-geo-server.git
   cd mcp-geo-server
   ```
2. Create environment & install dependencies using `uv`:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -e ".[dev]"
   ```
3. Run tests:
   ```bash
   uv run pytest
   ```

---

## 🤝 Contributing

Contributions are welcome! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md) guidelines. All contributions are credited under the **Taghi Molavi Antigravity Ecosystem**.

---

## 📄 License

This repository is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Developed with ❤️ by **Taqi Molavi** — [molavi.pro](https://molavi.pro)
