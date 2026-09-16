# Molavi AI Visibility Index (MAVI) — Measurement Engine v1.0

The **Molavi AI Visibility Index (MAVI)** is a multi-layer diagnostic and empirical measurement framework for Generative Engine Optimization (GEO).

Rather than relying on manually entered scores or arbitrary heuristics, MAVI v1 operates as an automated, measured index derived from two complementary research engines:
1. **SAGE (Search & AI-Engine Guided Evaluation)**: Deterministic webpage analysis of crawler accessibility, semantic structure, entity graphs, and citation extractability (Layers L1–L4).
2. **GEO-Scope**: Empirical multi-model live benchmark observations across search-grounded and direct-completion AI engines (Layer L5).

---

## 1. Multi-Layer Architecture & Provenance

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                      MAVI Composite Index (0 - 100)                        │
└─────────────────────────────────────┬──────────────────────────────────────┘
                                      │
         ┌────────────────────────────┼───────────────────────────┐
         ▼                            ▼                           ▼
 ┌───────────────┐            ┌───────────────┐           ┌───────────────┐
 │   SAGE (L1)   │            │   SAGE (L2)   │           │   SAGE (L3)   │
 │ Technical     │            │ Semantic      │           │ Entity        │
 │ Accessibility │            │ Extractability│           │ Clarity       │
 └───────────────┘            └───────────────┘           └───────────────┘
         │                            │                           │
         └────────────────────────────┼───────────────────────────┘
                                      │
         ┌────────────────────────────┴───────────────────────────┐
         ▼                                                        ▼
 ┌───────────────┐                                        ┌───────────────┐
 │   SAGE (L4)   │                                        │ GEO-Scope (L5)│
 │ Retrieval &   │                                        │ Observed AI   │
 │ Citation Ready│                                        │ Visibility    │
 └───────────────┘                                        └───────────────┘
```

---

## 2. Layer Definitions & Measurement Methodology

### L1: Technical Accessibility
- **Source Engine**: `SAGE` (Pillar 1: Technical SEO)
- **Methodology Weight**: `15%` ($w_1 = 0.15$)
- **What is Measured**:
  - **HTTP Status**: Returns 100.0 for HTTP 200, 70.0 for redirects, 0.0 for client/server errors.
  - **Meta Robots & Crawler Access**: Detects `noindex`, `none`, and explicit AI crawler blocks (`GPTBot`, `PerplexityBot`, `ClaudeBot`, `Google-Extended`).
  - **Canonical URL Integrity**: Validates presence of self-referential or authoritative canonical tag.
  - **Renderability & Text-to-DOM Density**: Evaluates text token density relative to overall HTML payload (optimal $\ge 8.0\%$).

### L2: Semantic Extractability
- **Source Engine**: `SAGE` (Pillar 2: Entity AEO)
- **Methodology Weight**: `20%` ($w_2 = 0.20$)
- **What is Measured**:
  - **Heading Structure & Hierarchy**: Validates single `<h1>` main heading, hierarchical `<h2>`/`<h3>` sectioning.
  - **RAG Chunk Quality**: Counts self-contained, high-information paragraph units (15–120 words).
  - **BLUF (Bottom Line Up Front) Direct Answers**: Detects clear definitions and assertive summary statements in the opening section.
  - **Semantic Density**: Evaluates lexical diversity and vocabulary uniqueness across content tokens.

### L3: Entity Clarity
- **Source Engine**: `SAGE` (Pillar 2: Entity Graph Analysis)
- **Methodology Weight**: `20%` ($w_3 = 0.20$)
- **What is Measured**:
  - **JSON-LD Schema Markup**: Evaluates presence and diversity of structured schemas (`Organization`, `Product`, `SoftwareApplication`, `Person`, `Article`). Note: Points are not awarded merely because JSON-LD exists.
  - **Entity Disambiguation (`sameAs`)**: Identifies grounding links to authoritative entity graphs (`Wikidata`, `Wikipedia`, `LinkedIn`, `Crunchbase`).
  - **Entity Name Consistency**: Matches target brand across `<title>`, `<h1>`, `<meta name="description">`, and JSON-LD schema names.
  - **Attribution & Publisher Identity**: Verifies explicit organization/author entity models.

### L4: Retrieval / Citation Readiness
- **Source Engine**: `SAGE` (Pillar 3: GEO & RAG Simulation)
- **Methodology Weight**: `20%` ($w_4 = 0.20$)
- **Methodology Status**: `Diagnostic Heuristic Proxy (E4)`
- **What is Measured**:
  - **Citation Survival Proxy (CSP)**: Heuristic scoring of chunk density, lexical distinctiveness, and anchor quality.
  - **Structured Data Tables**: Measures presence of HTML `<table>` and markdown comparison matrices.
  - **Quantitative Statistics & Proof Points**: Counts empirical metrics, percentages, benchmark figures, and currency values.
  - **DOM Container Isolation**: Verifies semantic `<main>` or `<article>` containers isolating primary text from navigation boilerplate.

### L5: Observed AI Visibility
- **Source Engine**: `GEO-Scope LIVE Benchmark Experiments`
- **Methodology Weight**: `25%` ($w_5 = 0.25$)
- **What is Measured**:
  - **Share of Model (SoM)**: Target brand mention rate across evaluated prompts in successful inferences.
  - **Top-1 Recommendation Pick Rate**: Frequency of brand appearing as primary recommendation (#1 position).
  - **Multi-Model Provider Coverage**: Proportion of AI engines citing/recommending the target brand.
  - **Zero Fabrication Policy**: If no live benchmark experiment has been executed, L5 is explicitly returned as `null` with status `not_measured`. No synthetic score is fabricated.

---

## 3. Weighting & Normalization Methodology

### Default Methodology Weights
Weights are versioned and labeled as **methodology defaults** (not claimed as universally fitted constants):

$$\mathcal{W} = \{L_1: 0.15, L_2: 0.20, L_3: 0.20, L_4: 0.20, L_5: 0.25\} \quad \left(\sum w_i = 1.00\right)$$

Custom weights can be configured via API or MCP (`custom_weights`).

### Partial MAVI Scoring
When some layers have not been measured (e.g., L1–L4 measured from HTML without an L5 experiment), MAVI computes a normalized score:

$$\text{MAVI}_{\text{normalized}} = \frac{\sum_{i \in \mathcal{M}} w_i \cdot S_i}{\sum_{i \in \mathcal{M}} w_i}$$

where $\mathcal{M}$ is the subset of active, measured layers. Missing layers are never converted to zero.

---

## 4. Confidence Assessment

Confidence is deterministically evaluated based on observable evidence:
- **High**: All 5 layers measured, with LIVE GEO-Scope observations $\ge 10$ and multi-provider coverage.
- **Medium**: 4 layers measured (e.g., SAGE L1–L4 without L5, or simulation-based synthetic L5).
- **Low**: 2–3 layers measured, or low observation count (< 5).
- **Insufficient**: 0 layers measured.

---

## 5. Live vs. Synthetic L5 Distinction

- `observed_live`: Real API observations from Perplexity, Gemini, OpenAI, Claude.
- `synthetic`: Simulation engine data. Labeled `non_observational` with confidence penalty.
- `insufficient_data`: Zero or insufficient successful observations in experiment.
- `not_measured`: No experiment data provided.
