# Critical Mineral Supply Chain Knowledge Pipeline

## Design Document v0.2

**Project context:** This pipeline is being developed as part of Eddie's doctoral research at the Institute for Manufacturing (IfM), University of Cambridge, within the Industrial Resilience Research Group and the Global Supply Chain Observatory (GSCO) project.

**Last updated:** 2026-04-13

**Changelog from v0.1:**
- Agent 1: Revised metadata acquisition logic with smart stopping, compulsory/optional field classification, page cap, and progressive context accumulation.
- Agent 2: Reverted to document-nested entity storage (entities are stored under the document directory, with metadata linking back to source).
- Agent 3a: Added hierarchical chunking (parent-child chunk structure) alongside adjacent chunk linking.
- Agent 3b: Added special table handling skills.
- Agent 4: Clarified the taxonomy support invocation conditions and distinguished support mode from normal tagging mode.
- Agent 8: Added staging SQL for raw extracted tables.
- Added Section 3.4: Centralised output schema registry.
- Incorporated answers to all open questions from v0.1.
- Updated taxonomy to include individual REE species with group-level fallback, alias table for organisations, and LLM-sourced conversion factors with assumption logging.

---

## 1. System overview

### 1.1 Purpose

An end-to-end, LLM-native pipeline that processes unstructured PDF documents related to critical mineral supply chains, extracts and interprets all entities (text, tables, charts, images), tags them against a pre-defined domain taxonomy, extracts relationships, and writes structured knowledge into a graph database, relational database, and vector store. The system must maintain full provenance and traceability from every extracted fact back to its source document, page, and entity.

### 1.2 Application domain

The end-to-end critical mineral supply chain, covering the full lifecycle from geological exploration through mining, refining, processing, component manufacturing, product assembly, use, and recycling/recovery. Target minerals include but are not limited to lithium, cobalt, nickel, graphite, rare earth elements (including individual REE species), and manganese.

### 1.3 Core design principles

1. **LLM-native.** The pipeline uses local LLMs through Ollama as the primary intelligence layer. All semantic interpretation, tagging, relationship extraction, summarisation, and validation tasks are performed by LLMs.
2. **Multi-model routing.** Different tasks may use different models from the Qwen 3.5 family (or other families) depending on the complexity, modality, and accuracy requirements. The system supports smooth switching between models.
3. **Modular agent architecture.** The pipeline is composed of distinct agents, each responsible for a well-defined task. Each agent's behaviour is governed by one or more skill documents (skill.md files). New agents and skills can be added as the system evolves.
4. **Full provenance.** Every extracted statement, relationship, or data point traces back to the original chunk, entity, page, and document from which it was derived.
5. **Living taxonomy.** The domain taxonomy/ontology (the "Library") is a standalone, versioned reference document. It evolves in a controlled manner as new concepts, units, and relationships are encountered during document processing.
6. **Fault tolerance.** Processing is page-level modular. Failure on any single page does not halt the pipeline. All progress is checkpointed, and processing can be paused and resumed.
7. **Centralised schema management.** All inter-agent data formats are defined as formal output schemas in a central registry, ensuring consistency across the pipeline.

### 1.4 Technology stack

| Component | Technology | Role |
|---|---|---|
| LLM runtime | Ollama (local) | Hosts all generative and vision models |
| Primary LLMs | Qwen 3.5:32b, Qwen 3.5:27b | Text reasoning, tagging, relationship extraction, summarisation, validation |
| Vision capability | Qwen 3.5 (multimodal) | Chart/figure interpretation (the Qwen 3.5 family supports vision natively) |
| Embedding model | qwen3-embedding:8b | Vector embeddings for text chunks and summaries |
| OCR/extraction | DeepSeek OCR (existing pipeline) | PDF page slicing and entity extraction |
| Graph database | Neo4j (local) | Stores entities, relationships, and structural knowledge |
| Relational database | PostgreSQL (local) | Stores denormalised analytical projections, staging tables for raw extracts, logs, manifests |
| Vector store | ChromaDB | Stores content and summary embeddings for semantic retrieval |
| Raw document store | Local filesystem (structured) | Retains all original PDF files for traceability |

---

## 2. Taxonomy and ontology (the "Library")

### 2.1 Role in the system

The taxonomy is the single most important design artefact. It determines the schema of PostgreSQL tables, the node and edge types in Neo4j, the tag vocabulary used by the taxonomy tagging agent, the output JSON schemas, and the controlled vocabularies for all categorical fields. Almost every agent in the pipeline references it.

The taxonomy is maintained as a standalone, versioned document. A dedicated skill (`taxonomy_reference.skill.md`) allows agents to browse and utilise this document whilst performing tasks.

The taxonomy should be as holistic as possible, addressing most data points associated with the critical mineral supply chain domain. It will grow continuously as new concepts are encountered.

### 2.2 Taxonomy evolution mechanism

The taxonomy is a living document. It will evolve as the pipeline encounters new concepts, units, or relationships that were not anticipated in the initial design. However, evolution must be carefully controlled.

A dedicated skill (`taxonomy_evolution.skill.md`) governs this process:

1. The agent flags the unrecognised concept with a proposed addition (new entity type, new relationship type, new unit, new controlled vocabulary entry).
2. The proposed addition is logged in a taxonomy evolution queue (PostgreSQL table).
3. A human reviewer (or a dedicated review agent with strict validation rules) approves, modifies, or rejects the proposal.
4. Approved additions are merged into the taxonomy document with a version increment.
5. All agents pick up the updated taxonomy on their next invocation.
6. When a taxonomy update affects existing data, a targeted re-processing workflow is triggered (see Section 6.2, point 7).

### 2.3 Proposed taxonomy structure

#### 2.3.1 Entity types

| Entity type | Description | Examples |
|---|---|---|
| Mineral/Material | A mineral commodity or processed material. Supports hierarchical granularity: group level (e.g., rare earth elements) and species level (e.g., neodymium). Documents may report at either level; the taxonomy accommodates both. | Lithium, cobalt, nickel, graphite, rare earth elements, neodymium, dysprosium, praseodymium, manganese |
| Country/Region | A geographic entity (ISO 3166-1 alpha-3 codes) | AUS, CHL, CHN, ARG, COD, USA |
| Organisation | Any entity involved in the supply chain. Organisations have an alias table (see 2.3.8) to handle name variations. | Mining companies, refiners, manufacturers, traders, government bodies, research institutions |
| Facility/Site | A physical location where supply chain activities occur | Mines, refineries, processing plants, smelters, recycling facilities, ports |
| Product/Component | A manufactured item or intermediate product | Battery cells, cathodes, anodes, precursors, concentrates, refined chemicals |
| Policy/Regulation | A rule, law, or agreement that affects the supply chain | Export controls, trade agreements, environmental standards, strategic reserves policy |
| Technology/Process | A method or technology used in supply chain activities | Extraction methods (DLE, brine evaporation, hard-rock mining), refining processes, recycling technologies |

#### 2.3.2 Mineral hierarchy

The mineral taxonomy uses a two-level hierarchy to accommodate varying document granularity:

```
Rare Earth Elements (group)
  ├── Neodymium (Nd)
  ├── Dysprosium (Dy)
  ├── Praseodymium (Pr)
  ├── Terbium (Tb)
  ├── Lanthanum (La)
  ├── Cerium (Ce)
  ├── Samarium (Sm)
  ├── Europium (Eu)
  ├── Gadolinium (Gd)
  ├── Yttrium (Y)
  └── [other REEs]

Lithium (individual mineral)
Cobalt (individual mineral)
Nickel (individual mineral)
Graphite (individual mineral)
  ├── Natural graphite
  └── Synthetic graphite
Manganese (individual mineral)
Copper (individual mineral)
Platinum Group Metals (group)
  ├── Platinum (Pt)
  ├── Palladium (Pd)
  ├── Rhodium (Rh)
  └── [others]
```

When a document reports at the group level (e.g., "total rare earth oxide production"), the tag uses the group entity. When it reports at the species level (e.g., "neodymium oxide production"), the tag uses the species entity. Both are valid. Relationships to a group entity and to its constituent species are linked in Neo4j via MEMBER_OF relationships.

#### 2.3.3 Relationship types

| Relationship | Subject → Object | Key attributes |
|---|---|---|
| PRODUCES | Country/Facility → Mineral | volume, unit, metric, year, capacity_type (nameplate/actual) |
| SUPPLIES / TRADES | Entity → Entity | commodity, volume, value, currency, time_period |
| OPERATES | Organisation → Facility | ownership_percent, start_date |
| LOCATED_IN | Facility → Country/Region | |
| OWNS / HAS_STAKE_IN | Organisation → Organisation/Facility | ownership_percent, acquisition_date |
| IMPORTS / EXPORTS | Country → Country | commodity, volume, value, currency, year, share_percent |
| REGULATES / RESTRICTS | Policy → Commodity/Activity/Country | effective_date, scope |
| PROCESSES_AT_STAGE | Facility → Mineral | supply_chain_stage |
| INVESTS_IN | Organisation → Facility/Project | investment_amount, currency, year |
| DEPENDS_ON | Product/Component → Mineral | quantity_per_unit, unit |
| RESERVES | Country → Mineral | volume, unit, reserve_classification (measured/indicated/inferred) |
| PRICES | Mineral → (temporal attribute) | price, currency, unit, price_type (spot/contract), date |
| MEMBER_OF | Mineral (species) → Mineral (group) | (structural, no temporal attributes) |
| EMPLOYS | Organisation/Facility → (workforce data) | headcount, year, skill_category |
| EMITS | Facility/Process → (environmental data) | co2_per_tonne, water_usage_per_tonne, year |

#### 2.3.4 Supply chain stages (controlled vocabulary)

Exploration → Mining/Extraction → Beneficiation/Concentration → Refining/Smelting → Precursor production → Component manufacturing → Product assembly/integration → Use/Deployment → Collection/End-of-life → Recycling/Recovery

#### 2.3.5 Quantitative attribute types

| Attribute | Sub-fields |
|---|---|
| Volume/Quantity | value, unit (tonnes, kg, kt, Mt, etc.), metric (lithium_content, LCE, spodumene_concentrate, lithium_hydroxide, contained_metal, ore, REO, etc.) |
| Value | value, currency (USD, EUR, CNY, AUD, etc.) |
| Capacity | value, unit, capacity_type (nameplate, actual, planned, under_construction) |
| Price | value, currency, per_unit, price_type (spot, contract, average, futures), date |
| Percentage | value, percentage_of (market_share, ownership, import_share, recovery_rate, grade) |
| Temporal | year, quarter, month, date_range, as_of_date |

#### 2.3.6 Unit and form conversion layer

Production figures for the same mineral are reported in different forms across sources. The taxonomy maintains conversion factors sourced initially from LLM pre-trained knowledge and progressively verified and updated.

| Mineral | Form | Conversion to contained metal | Source | Confidence |
|---|---|---|---|---|
| Lithium | Spodumene concentrate (6% Li2O) | × 0.028 | LLM pre-trained knowledge (initial) | assumed |
| Lithium | Lithium carbonate (Li2CO3) | × 0.188 | LLM pre-trained knowledge (initial) | assumed |
| Lithium | Lithium hydroxide (LiOH·H2O) | × 0.165 | LLM pre-trained knowledge (initial) | assumed |
| Lithium | Lithium carbonate equivalent (LCE) | × 0.188 | LLM pre-trained knowledge (initial) | assumed |
| Cobalt | Cobalt hydroxide | × 0.387 | LLM pre-trained knowledge (initial) | assumed |
| Nickel | Nickel sulphate (NiSO4·6H2O) | × 0.223 | LLM pre-trained knowledge (initial) | assumed |

**Assumption logging:** Every conversion factor carries a `source` field and a `confidence` field. Initial values derived from LLM pre-trained knowledge are marked as `assumed`. When a conversion factor is verified against a published reference (e.g., a USGS fact sheet, an academic source), the source and confidence are updated. All assumption changes are logged in the `conversion_factor_log` table in PostgreSQL, creating a full audit trail of what was assumed, when it was verified, and what the verified value is.

**Update mechanism:** Conversion factors can be updated at any time. When updated, any derived values in the database that used the old factor can be flagged for recalculation. This is a targeted re-processing task, not a full pipeline re-run.

#### 2.3.7 Source type enumeration

| Source type | Default reliability weight |
|---|---|
| `government_report` | 0.95 |
| `academic_paper` | 0.90 |
| `trade_statistics` | 0.90 |
| `technical_standard` | 0.85 |
| `company_annual_report` | 0.80 |
| `industry_analysis` | 0.75 |
| `market_report` | 0.70 |
| `patent` | 0.70 |
| `policy_document` | 0.85 |
| `news_article` | 0.55 |

#### 2.3.8 Organisation alias table

Organisations frequently appear under different names across documents. The taxonomy maintains an alias table that maps variations to a canonical name:

| Canonical name | Aliases |
|---|---|
| BHP Group | BHP, BHP Billiton, BHP Group Limited |
| Albemarle Corporation | Albemarle, ALB |
| Sociedad Química y Minera | SQM, Sociedad Quimica y Minera de Chile |
| Ganfeng Lithium | Ganfeng, Jiangxi Ganfeng Lithium |
| Pilbara Minerals | Pilbara, PLS |
| CATL | Contemporary Amperex Technology, Contemporary Amperex Technology Co. Limited |

This table is extensible. When the taxonomy tagging agent encounters an organisation name that is not in the alias table, it proposes a new entry through the taxonomy evolution mechanism. The alias table is stored in PostgreSQL and also referenced in the taxonomy document.

---

## 3. Agent and skill architecture

### 3.1 Overview

The pipeline comprises ten agents (Agent 0 through Agent 8, plus the Pipeline Orchestrator). Each agent is governed by one or more skill documents that define its behaviour, prompts, input/output schemas, and rules.

### 3.2 Skill management

All skills are stored in a central skill directory. Skills fall into four categories:

1. **Task skills:** Define how a specific agent performs its work (prompts, rules, output formats).
2. **Reference skills:** Provide access to shared knowledge (the taxonomy document, conversion tables, controlled vocabularies).
3. **Configuration skills:** Define system-wide parameters (model routing, chunk sizes, confidence thresholds, database connection details).
4. **Evolution skills:** Govern the controlled growth of the taxonomy and other reference documents.

Skills are versioned. When a skill is updated, the version increment is recorded in the pipeline manifest so that any processing run can be fully reproduced.

### 3.3 Centralised output schema registry

All inter-agent data formats are defined as formal schemas in a central registry. This registry serves as the single source of truth for what each agent produces and what each downstream agent expects to receive.

**Location:** `/schemas/` directory containing JSON Schema or Pydantic model definitions.

**Schema files:**
```
/schemas/
  page_preparation_output.schema.json
  document_intake_output.schema.json
  manifest.schema.json
  structural_extraction_output.schema.json
  text_chunk.schema.json
  table_interpretation_output.schema.json
  chart_interpretation_output.schema.json
  taxonomy_tags.schema.json
  taxonomy_support_request.schema.json
  taxonomy_support_response.schema.json
  relationship.schema.json
  summary_and_embedding.schema.json
  confidence_result.schema.json
  database_write_result.schema.json
  pipeline_log_entry.schema.json
```

**Governance rules:**
1. Any change to a schema requires a version increment and must be backward-compatible where possible.
2. Breaking changes require a migration plan for existing data.
3. Every agent's skill document references the relevant schemas from the registry, ensuring the skill and the schema stay in sync.
4. The orchestrator validates agent outputs against the schema before passing data downstream. Schema validation failures are logged and the entity is flagged.

### 3.4 Agent decomposition

#### Agent 0: Page Preparation Agent

**Purpose:** Converts raw PDF into a form that downstream agents can process. This is the true first stage of the pipeline, executing before any LLM-based analysis.

**Skills required:**
- `page_preparation.skill.md`: PDF slicing rules, output format specifications, image conversion parameters, base64 encoding settings.

**Process:**
1. Receives a raw PDF file path.
2. Slices the PDF into individual pages.
3. Converts each page into a high-resolution image (PNG).
4. Encodes each page image as base64 for multimodal LLM consumption.
5. Stores page images under the document directory.

**Input schema reference:** Raw file path (string).

**Output schema reference:** `page_preparation_output.schema.json`
```json
{
  "source_file": "/incoming/usgs_lithium_mcs_2024.pdf",
  "page_count": 12,
  "pages": [
    {
      "page_number": 1,
      "image_path": "/documents/DOC-2024-00042/pages/page_001.png",
      "base64": "<base64_encoded_string>",
      "dimensions": { "width": 2480, "height": 3508 }
    }
  ]
}
```

**Design note:** This agent is deterministic (no LLM involved). It is a preprocessing utility that ensures all downstream agents receive pages in a consistent, model-readable format.

---

#### Agent 1: Document Intake Agent

**Purpose:** Extracts document-level metadata and creates the processing manifest and document registration record. Also registers the document in the document source store for future clustering and linking.

**Skills required:**
- `document_intake.skill.md`: Metadata extraction prompts, field classification (compulsory/optional), stopping logic, progressive context accumulation rules, page cap.
- `document_source_registry.skill.md`: Rules for checking existing sources, matching/linking new documents to known sources, creating new source entries.

**Metadata field classification:**

| Field | Status | Description |
|---|---|---|
| `title` | Compulsory | Main title of the document |
| `source_organisation` | Compulsory | Publisher or authoring organisation |
| `source_type` | Compulsory | Enum from taxonomy (government_report, academic_paper, etc.) |
| `language` | Compulsory | ISO 639-1 language code |
| `publication_date` | Optional | Date of publication (year at minimum) |
| `authors` | Optional | Individual or institutional authors |
| `doi_or_isbn` | Optional | Digital object identifier or ISBN |
| `edition_or_version` | Optional | For recurring publications (e.g., "2024 edition") |
| `abstract_or_summary` | Optional | If present in the document |

**Process (revised from v0.1):**

The agent scans pages progressively, maintaining a running context of all metadata acquired so far. This prevents the LLM from mistaking section titles for the document title or overwriting earlier correct values with later incorrect ones.

1. **Forward scan:** Read page 1 and extract any available metadata. Store results in a `metadata_draft` object. Send the current `metadata_draft` to the LLM alongside each subsequent page, so the model knows what has already been identified and can distinguish new metadata from section headings or subsidiary titles.
2. **Continue forward:** Read pages 2, 3, ... up to a cap. For each page, the LLM receives the page image AND the current `metadata_draft`. It can add new field values but should not overwrite already-acquired compulsory fields unless it has high confidence the earlier value was incorrect (with an explanation logged).
3. **Backward scan:** If compulsory fields are still missing after the forward scan, read the last page, then second-to-last, etc., up to the cap. Many documents place copyright, publisher, and date information at the end.
4. **Stopping logic:** The agent stops scanning when EITHER:
   - All compulsory fields are filled AND three consecutive pages have yielded no new metadata (the "overshoot" rule), OR
   - The page cap has been reached.
5. **Page cap:** Maximum of 8 pages scanned total (forward + backward combined). Most document metadata is found within the first 3 and last 2 pages. If compulsory fields remain unfilled after the cap, they are marked as `"not_found"` and flagged for human review.

6. **Source registry check:** The agent checks the document source registry to see if this source already exists. If so, links the new document to the existing source entry. If not, creates a new source entry.
7. **Document registration:** Copies the raw PDF to the raw document store, assigns a unique document ID, and creates the processing manifest.

**Input schema reference:** `page_preparation_output.schema.json`

**Output schema reference:** `document_intake_output.schema.json`
```json
{
  "document_id": "DOC-2024-00042",
  "raw_store_path": "/documents/DOC-2024-00042/raw/usgs_lithium_mcs_2024.pdf",
  "metadata": {
    "title": "Mineral Commodity Summaries 2024 - Lithium",
    "source_organisation": "U.S. Geological Survey",
    "publication_date": "2024-01",
    "source_type": "government_report",
    "page_count": 12,
    "language": "en",
    "authors": "not_found",
    "doi_or_isbn": "not_found",
    "edition_or_version": "2024",
    "abstract_or_summary": "not_found",
    "source_registry_id": "SRC-0003",
    "linked_documents": ["DOC-2023-00018", "DOC-2022-00011"],
    "metadata_scan_log": {
      "pages_scanned_forward": [1, 2, 3, 4],
      "pages_scanned_backward": [12, 11],
      "total_pages_scanned": 6,
      "fields_not_found": ["authors", "doi_or_isbn", "abstract_or_summary"],
      "stopping_reason": "all_compulsory_filled_and_overshoot_complete"
    }
  },
  "manifest": {
    "document_id": "DOC-2024-00042",
    "pipeline_version": "0.2.0",
    "status": "in_progress",
    "pages": [
      { "page": 1, "status": "pending" },
      { "page": 2, "status": "pending" }
    ],
    "model_versions": {
      "intake_llm": "qwen3.5:32b",
      "extraction_ocr": "deepseek-ocr",
      "text_llm": "qwen3.5:32b",
      "vision_llm": "qwen3.5:32b",
      "embedding": "qwen3-embedding:8b"
    },
    "created_at": "2026-04-13T10:00:00Z"
  }
}
```

**Document source registry (PostgreSQL table: `document_sources`):**

This tracks known document sources for clustering and linking:

| Field | Type | Description |
|---|---|---|
| source_id | TEXT PK | e.g., SRC-0003 |
| name | TEXT | e.g., "USGS Mineral Commodity Summaries" |
| type | TEXT | Source type enum value |
| publisher | TEXT | e.g., "U.S. Geological Survey" |
| url | TEXT | Optional URL for the publication series |
| publication_frequency | TEXT | annual, quarterly, one-off, irregular |
| document_count | INTEGER | Number of documents processed from this source |

---

#### Agent 2: Structural Extraction Agent

**Purpose:** Decomposes each page into typed entities: text blocks (with layout-aware markdown), tables (as images and CSV), charts/figures (as images and, where possible, CSV), and standalone images.

**Skills required:**
- `structural_extraction.skill.md`: Entity type definitions, DeepSeek OCR configuration, output format rules.
- `cross_page_entity.skill.md`: Rules for detecting entities that span page boundaries, and the process for combining adjacent pages into a single image for joint analysis.

**Process:**
1. Receives page images from Agent 0.
2. Runs the DeepSeek OCR pipeline on each page. This pipeline produces:
   - Markdown text with layout information for text blocks.
   - PNG images of detected tables, plus CSV representations.
   - PNG images of detected charts/figures, plus CSV representations where applicable.
   - Standalone images extracted from the page.
3. Each extracted entity is assigned a unique entity ID and stored under the document directory (nested storage), with metadata fields linking it back to the source document and page.
4. If the LLM (or heuristic rules) detects that an entity may span across a page boundary, the cross-page entity skill is triggered. This skill combines the two page images by stacking them vertically and re-runs extraction on the combined image.

**Entity storage structure (document-nested):**
```
/documents/DOC-2024-00042/
  raw/
    usgs_lithium_mcs_2024.pdf
  pages/
    page_001.png
    page_002.png
  entities/
    P01-E001/
      content.md          # Text block markdown
      metadata.json       # Entity metadata with source links
    P01-E002/
      table.png           # Table image
      table.csv           # Table CSV representation
      metadata.json
    P02-E003/
      chart.png           # Chart image
      chart.csv           # Chart CSV (if extractable)
      metadata.json
    P02-E004/
      image.png           # Standalone image
      metadata.json
```

Each `metadata.json` contains:
```json
{
  "entity_id": "DOC-2024-00042-P01-E002",
  "type": "table",
  "document_id": "DOC-2024-00042",
  "page": 1,
  "caption": "World Mine Production and Reserves",
  "bounding_box": { "x0": 72, "y0": 360, "x1": 540, "y1": 580 },
  "cross_page": false,
  "extraction_tool": "deepseek-ocr",
  "extracted_at": "2026-04-13T10:05:00Z"
}
```

**Input schema reference:** `page_preparation_output.schema.json` (single page)

**Output schema reference:** `structural_extraction_output.schema.json`
```json
{
  "document_id": "DOC-2024-00042",
  "page": 1,
  "entities": [
    {
      "entity_id": "DOC-2024-00042-P01-E001",
      "type": "text_block",
      "content_markdown": "## Domestic Production and Use\n\nIn 2023, Australia remained...",
      "section_heading": "Domestic Production and Use",
      "heading_level": 2,
      "storage_path": "/documents/DOC-2024-00042/entities/P01-E001/",
      "source": { "document_id": "DOC-2024-00042", "page": 1 }
    },
    {
      "entity_id": "DOC-2024-00042-P01-E002",
      "type": "table",
      "image_path": "/documents/DOC-2024-00042/entities/P01-E002/table.png",
      "csv_path": "/documents/DOC-2024-00042/entities/P01-E002/table.csv",
      "csv_content": "Country,2022 Production (t),2023 Production (t),Reserves (t)\nAustralia,61000,86000,6200000\n...",
      "caption": "World Mine Production and Reserves",
      "storage_path": "/documents/DOC-2024-00042/entities/P01-E002/",
      "source": { "document_id": "DOC-2024-00042", "page": 1 }
    }
  ],
  "cross_page_flags": [
    {
      "entity_id": "DOC-2024-00042-P01-E002",
      "flag": "potential_continuation",
      "next_page": 2,
      "reason": "Table appears truncated at bottom of page"
    }
  ]
}
```

---

#### Agent 3a: Text Chunking Agent

**Purpose:** Takes text block entities and applies hierarchical, structure-aware chunking to produce appropriately sized text chunks for downstream processing and embedding.

**Skills required:**
- `text_chunking.skill.md`: Chunk size targets, overlap percentage, paragraph/sentence boundary rules, metadata inheritance rules, hierarchical chunking rules.
- `adjacent_chunk_chaining.skill.md`: Rules for how downstream agents can chain adjacent chunks together when analysis requires broader context. The LLM can follow the chain links and consume additional chunks until it decides it has enough context.

**Hierarchical chunking model:**

The chunking agent produces a two-level hierarchy:

1. **Parent chunks (level 0):** Correspond to natural document sections (a full section under a heading, or a coherent multi-paragraph block). These preserve the full context of the section. Parent chunks may be large (up to 2048 tokens).
2. **Child chunks (level 1):** Subdivisions of parent chunks, targeting 512 tokens with approximately 10-15% overlap, split at paragraph or sentence boundaries. These are the primary units for embedding and retrieval.

Each child chunk carries a reference to its parent chunk, and each parent chunk carries references to all its children. This allows retrieval systems to find a relevant child chunk and then "zoom out" to the parent for full context.

```
Section: "Domestic Production and Use" (parent chunk, 1800 tokens)
  ├── Child chunk 1 (512 tokens): paragraphs 1-3
  ├── Child chunk 2 (480 tokens): paragraphs 3-5 (with overlap)
  └── Child chunk 3 (340 tokens): paragraphs 5-6
```

**Adjacent chunk chaining:**

Child chunks within the same parent are linked via `previous_chunk_id` and `next_chunk_id`. Downstream agents (particularly relationship extraction) can follow these links to consume adjacent chunks when the current chunk does not provide sufficient context for extraction. The chaining skill provides rules for when and how to expand context:

1. The agent reads the current chunk and attempts extraction.
2. If the chunk ends mid-sentence or mid-thought, or if a relationship requires context from a preceding/following statement, the agent follows the chain link.
3. The agent continues chaining until it determines it has sufficient context or reaches the parent chunk boundary.

**Input schema reference:** `structural_extraction_output.schema.json` (text_block entities)

**Output schema reference:** `text_chunk.schema.json`
```json
{
  "parent_chunk": {
    "chunk_id": "DOC-2024-00042-P01-E001-L0",
    "parent_entity_id": "DOC-2024-00042-P01-E001",
    "document_id": "DOC-2024-00042",
    "type": "parent_chunk",
    "level": 0,
    "page": 1,
    "section_heading": "Domestic Production and Use",
    "content": "[full section text]",
    "token_count": 1800,
    "child_chunk_ids": [
      "DOC-2024-00042-P01-E001-L1-C001",
      "DOC-2024-00042-P01-E001-L1-C002",
      "DOC-2024-00042-P01-E001-L1-C003"
    ],
    "provenance": {
      "document_id": "DOC-2024-00042",
      "entity_id": "DOC-2024-00042-P01-E001",
      "page": 1
    }
  },
  "child_chunks": [
    {
      "chunk_id": "DOC-2024-00042-P01-E001-L1-C001",
      "parent_chunk_id": "DOC-2024-00042-P01-E001-L0",
      "parent_entity_id": "DOC-2024-00042-P01-E001",
      "document_id": "DOC-2024-00042",
      "type": "child_chunk",
      "level": 1,
      "page": 1,
      "section_heading": "Domestic Production and Use",
      "content": "In 2023, Australia remained the world's leading lithium producer...",
      "token_count": 512,
      "chunk_index": 1,
      "total_chunks": 3,
      "previous_chunk_id": null,
      "next_chunk_id": "DOC-2024-00042-P01-E001-L1-C002",
      "provenance": {
        "document_id": "DOC-2024-00042",
        "entity_id": "DOC-2024-00042-P01-E001",
        "page": 1
      }
    }
  ]
}
```

**Design note:** Tables, charts, and images are NOT chunked. They are treated as atomic entities. Only text blocks undergo chunking.

---

#### Agent 3b: Table Interpretation Agent

**Purpose:** Interprets the semantic meaning of table columns and values using the taxonomy and LLM domain knowledge. Maps column headers to ontology attributes and normalises values.

**Skills required:**
- `table_interpretation.skill.md`: Column mapping prompts, value normalisation rules, ambiguity handling, acronym resolution.
- `table_structure_handling.skill.md`: Rules for handling complex table structures: merged cells, multi-level headers, footnotes within tables, implicit row groupings, unit annotations in headers vs cells.
- `table_numeric_parsing.skill.md`: Rules for parsing numeric values from tables: handling thousands separators (comma vs period by locale), ranges ("10,000-15,000"), qualitative indicators ("W" for withheld, "—" for zero, "NA"), and rounding indicators ("e" for estimated).
- `taxonomy_reference.skill.md`: The taxonomy document, for mapping columns to known entity types and attributes.

**Process:**
1. Receives table entities from Agent 2 (CSV content plus the table image for visual verification).
2. Sends the table headers, a sample of rows, the table caption, and any surrounding text context to the LLM along with the taxonomy.
3. The LLM interprets each column: what entity type or attribute it maps to, what unit it represents, and whether any acronyms or jargon need resolution.
4. If the LLM cannot resolve a column header or value with confidence, it invokes the taxonomy tagging agent's support mode (see Agent 4).
5. Values are parsed into typed fields (numeric, string, date) and normalised where possible (e.g., country name → ISO code, "W" → withheld, "e" → estimated).
6. The raw table is also staged in PostgreSQL (see Agent 8) as a faithful reproduction of the original table for reference.

**Input schema reference:** `structural_extraction_output.schema.json` (table entities)

**Output schema reference:** `table_interpretation_output.schema.json`
```json
{
  "entity_id": "DOC-2024-00042-P01-E002",
  "interpreted_columns": [
    {
      "column_index": 0,
      "original_header": "Country",
      "mapped_type": "country",
      "normalisation": "name_to_iso3166_alpha3"
    },
    {
      "column_index": 1,
      "original_header": "2022 Production (t)",
      "mapped_type": "production_volume",
      "unit": "tonnes",
      "metric": "lithium_content",
      "metric_source": "taxonomy_support_disambiguation",
      "temporal": "2022"
    },
    {
      "column_index": 3,
      "original_header": "Reserves (t)",
      "mapped_type": "reserves",
      "unit": "tonnes",
      "reserve_classification": "unspecified"
    }
  ],
  "parsed_rows": [
    {
      "row_index": 0,
      "values": {
        "country": { "raw": "Australia", "normalised": "AUS" },
        "production_2022": { "raw": "61,000", "value": 61000, "unit": "tonnes", "qualifier": null },
        "production_2023": { "raw": "86,000", "value": 86000, "unit": "tonnes", "qualifier": "e" },
        "reserves": { "raw": "6,200,000", "value": 6200000, "unit": "tonnes", "qualifier": null }
      }
    }
  ],
  "interpretation_confidence": 0.88,
  "ambiguities_resolved": [
    {
      "issue": "Metric for production columns not specified in header",
      "resolution": "Resolved via taxonomy support: USGS MCS reports lithium in tonnes of lithium content",
      "resolution_source": "taxonomy_support_agent"
    }
  ],
  "table_notes": [
    { "symbol": "e", "meaning": "Estimated" },
    { "symbol": "W", "meaning": "Withheld to avoid disclosing company proprietary data" }
  ],
  "provenance": {
    "document_id": "DOC-2024-00042",
    "entity_id": "DOC-2024-00042-P01-E002",
    "page": 1
  }
}
```

---

#### Agent 3c: Vision Interpretation Agent

**Purpose:** Interprets charts, figures, and standalone images using the Qwen 3.5 vision model.

**Skills required:**
- `vision_interpretation.skill.md`: Chart type recognition prompts, data extraction templates, description format rules, confidence annotation rules, extraction method vocabulary.

**Extraction method vocabulary:**

| Method | Description | Default confidence modifier |
|---|---|---|
| `direct_label_read` | A numeric value is explicitly printed on or beside the data point | +0.15 |
| `estimated_from_bar_height` | Value interpolated from bar height against axis scale | 0.00 (baseline) |
| `estimated_from_line_position` | Value interpolated from line position against axis scale | 0.00 |
| `estimated_from_area` | Value inferred from area proportion (pie charts, treemaps) | -0.10 |
| `estimated_from_annotation` | Value read from a text annotation on the chart | +0.10 |

**Input schema reference:** `structural_extraction_output.schema.json` (chart/figure/image entities)

**Output schema reference:** `chart_interpretation_output.schema.json`
```json
{
  "entity_id": "DOC-2024-00042-P02-E003",
  "type": "chart_interpretation",
  "chart_type": "bar_chart",
  "x_axis": { "label": "Year", "type": "temporal" },
  "y_axis": { "label": "Price", "unit": "USD/tonne" },
  "extracted_data": [
    { "year": 2019, "value": 11000, "extraction_method": "estimated_from_bar_height" },
    { "year": 2020, "value": 8500, "extraction_method": "estimated_from_bar_height" },
    { "year": 2021, "value": 17000, "extraction_method": "estimated_from_bar_height" },
    { "year": 2022, "value": 78000, "extraction_method": "estimated_from_bar_height" },
    { "year": 2023, "value": 22000, "extraction_method": "estimated_from_bar_height" }
  ],
  "narrative_summary": "Lithium carbonate prices spiked dramatically in 2022 to approximately $78,000/tonne before falling back to around $22,000/tonne in 2023.",
  "overall_confidence": 0.72,
  "confidence_notes": "All values are approximate as they are read from bar heights rather than labelled data points.",
  "csv_cross_reference": {
    "csv_available": true,
    "discrepancies": []
  },
  "provenance": {
    "document_id": "DOC-2024-00042",
    "entity_id": "DOC-2024-00042-P02-E003",
    "page": 2
  }
}
```

---

#### Agent 4: Taxonomy Tagging Agent

**Purpose:** Assigns taxonomy tags to all entity types. Also serves as a domain knowledge support service for upstream agents.

**Skills required:**
- `taxonomy_tagging.skill.md`: Tagging rules, multi-label assignment logic, confidence thresholds for tag assignment, normalisation rules, extensive examples of correct and incorrect tagging.
- `taxonomy_reference.skill.md`: The full ontology document.
- `taxonomy_support.skill.md`: Protocol for receiving and responding to support requests from other agents.
- `taxonomy_evolution.skill.md`: Process for proposing taxonomy additions when unrecognised concepts are encountered.

**Two operating modes:**

**Mode 1: Normal tagging (Phase 3 of the pipeline).**
Every entity passes through this mode. The agent reads the entity content, identifies all taxonomy-relevant mentions, and assigns tags from the controlled vocabularies.

**Mode 2: Support invocation (invoked by upstream agents during Phase 2).**
Upstream agents (specifically Agent 3b: Table Interpretation and Agent 3c: Vision Interpretation) can invoke the taxonomy agent when they encounter domain-specific terminology that they cannot resolve on their own.

**When support mode is triggered:** The distinction is critical. Normal tagging happens in Phase 3 and applies tags to already-processed entities. Support invocation happens during Phase 2, when an upstream agent needs domain understanding to complete its own processing task. The specific conditions for triggering support:

1. The upstream agent encounters a term, acronym, unit, or abbreviation that it cannot confidently interpret (e.g., "REO (kt)", "LCE", "DLE", "NPI" in a table header).
2. The interpretation of this term is required for the agent to complete its task (e.g., the table interpretation agent cannot correctly parse column values without knowing what "REO" means and what unit "kt" represents).
3. The upstream agent cannot resolve the ambiguity from the local context alone (the table caption and surrounding text are insufficient).

If the upstream agent can complete its task without domain disambiguation (e.g., a table with clear headers like "Country" and "Production (tonnes)"), it does NOT invoke support mode. Support mode is for genuine ambiguity, not routine processing.

**Support request/response protocol:**

Request:
```json
{
  "requesting_agent": "table_interpretation",
  "request_id": "SUPP-00042-001",
  "query_type": "term_disambiguation",
  "term": "REO (kt)",
  "context": {
    "entity_id": "DOC-2024-00042-P01-E002",
    "table_caption": "World REE Production by Country",
    "surrounding_text": "Global rare earth production increased by 12% in 2023..."
  }
}
```

Response:
```json
{
  "request_id": "SUPP-00042-001",
  "resolution": {
    "term": "REO",
    "full_form": "Rare Earth Oxides",
    "mapped_type": "mineral",
    "mapped_value": "rare_earth_elements",
    "form": "rare_earth_oxide",
    "unit_abbreviation": "kt",
    "unit_full": "kilotonnes",
    "unit_value": "tonnes",
    "unit_multiplier": 1000
  },
  "confidence": 0.95,
  "taxonomy_version": "0.2.0"
}
```

**Normal tagging output schema reference:** `taxonomy_tags.schema.json`
```json
{
  "entity_ref": "DOC-2024-00042-P01-E001-L1-C001",
  "tags": [
    {
      "type": "mineral",
      "value": "lithium",
      "form": "spodumene_concentrate",
      "mention": "lithium content from spodumene concentrate"
    },
    {
      "type": "country",
      "value": "AUS",
      "mention": "Australia"
    },
    {
      "type": "country",
      "value": "CHL",
      "mention": "Chile"
    },
    {
      "type": "supply_chain_stage",
      "value": "mining_extraction",
      "mention": "lithium producer"
    },
    {
      "type": "temporal",
      "value": "2023",
      "mention": "In 2023"
    },
    {
      "type": "metric_type",
      "value": "production_volume",
      "mention": "output of 86,000 tonnes"
    }
  ],
  "unrecognised_concepts": [],
  "tagging_confidence": 0.91
}
```

---

#### Agent 5: Relationship Extraction Agent

**Purpose:** Extracts structured relationships (triples with attributes) from tagged entities.

**Skills required (split by entity type):**
- `relationship_extraction_text.skill.md`: Prompts and rules for extracting relationships from narrative text chunks. Handles implicit relationships ("Australia remained the leading producer" implies PRODUCES with rank=1), conditional statements, and temporal qualifiers.
- `relationship_extraction_table.skill.md`: Prompts and rules for extracting relationships from interpreted table rows. Each row typically maps to one or more relationship instances. Handles multi-column relationships and derived attributes.
- `relationship_extraction_chart.skill.md`: Prompts and rules for extracting relationships from chart data. Temporal series data maps to multiple relationship instances across time periods.
- `taxonomy_reference.skill.md`: Ensures relationship types and attributes conform to the ontology.
- `adjacent_chunk_chaining.skill.md`: Allows the agent to follow chunk chain links when context is insufficient.

**Input schema reference:** Any tagged entity from Agent 4 (text chunks, interpreted tables, chart interpretations).

**Output schema reference:** `relationship.schema.json`
```json
{
  "source_entity_ref": "DOC-2024-00042-P01-E001-L1-C001",
  "relationships": [
    {
      "relationship_id": "REL-00042-001",
      "subject": { "type": "country", "value": "AUS" },
      "predicate": "PRODUCES",
      "object": { "type": "mineral", "value": "lithium", "form": "spodumene_concentrate" },
      "attributes": {
        "volume": 86000,
        "unit": "tonnes",
        "metric": "lithium_content",
        "year": 2023,
        "rank": 1
      },
      "extraction_type": "direct",
      "provenance": {
        "document_id": "DOC-2024-00042",
        "entity_id": "DOC-2024-00042-P01-E001",
        "chunk_id": "DOC-2024-00042-P01-E001-L1-C001",
        "page": 1,
        "source_text": "Australia remained the world's leading lithium producer, with an estimated output of 86,000 tonnes"
      }
    }
  ]
}
```

**Extraction type vocabulary:** `direct` (the relationship and its attributes are explicitly stated), `inferred` (the relationship or a specific attribute is computed, derived, or inferred).

---

#### Agent 6: Summarisation and Embedding Agent

**Purpose:** Generates concise summaries and produces vector embeddings for semantic retrieval.

**Skills required:**
- `summarisation.skill.md`: Summary length targets (1-3 sentences per entity), style rules (concise, factual, tag-enriched), quality criteria (faithful to source, includes key quantitative data, incorporates taxonomy tags), what to include/exclude.
- `embedding.skill.md`: Model configuration for qwen3-embedding:8b, vector dimensions, ChromaDB collection naming, metadata fields.

**Input schema reference:** Entities with tags and relationships from Agents 4 and 5.

**Output schema reference:** `summary_and_embedding.schema.json`
```json
{
  "entity_ref": "DOC-2024-00042-P01-E001-L1-C001",
  "summary": "2023 global lithium production data: Australia led with 86,000t lithium content (spodumene concentrate), Chile 44,000t, China 33,000t. Mining/extraction stage.",
  "embeddings": {
    "content_vector_id": "VEC-00042-P01-E001-L1-C001-content",
    "summary_vector_id": "VEC-00042-P01-E001-L1-C001-summary",
    "vector_dimension": 4096,
    "model": "qwen3-embedding:8b",
    "chromadb_collection": "critical_minerals_entities"
  },
  "chromadb_metadata": {
    "document_id": "DOC-2024-00042",
    "page": 1,
    "entity_type": "text_chunk",
    "chunk_level": 1,
    "minerals": ["lithium"],
    "countries": ["AUS", "CHL", "CHN"],
    "supply_chain_stage": "mining_extraction",
    "year": 2023
  }
}
```

---

#### Agent 7: Confidence Scoring and Validation Agent

**Purpose:** Scores confidence, detects contradictions, flags items for review.

**Skills required:**
- `confidence_scoring.skill.md`: Scoring formula, weight assignments, band thresholds.
- `contradiction_detection.skill.md`: Two-layer matching logic (deterministic then semantic), comparison rules, contradiction classification, resolution protocol.
- `validation_rules.skill.md`: Domain-specific validation rules.

**Confidence scoring formula:**

| Signal | Weight | Description |
|---|---|---|
| Source reliability | 0.30 | Based on source type (see taxonomy 2.3.7) |
| Extraction clarity | 0.30 | Based on extraction_type and extraction_method |
| Internal consistency | 0.20 | Domain validation checks (value in range, unit valid, temporal valid) |
| Corroboration | 0.20 | Same fact found in other processed documents |

Confidence bands: HIGH (> 0.85), MEDIUM (0.50-0.85), LOW (< 0.50, auto-flagged for review).

**Two-layer contradiction detection:**

**Layer 1 (deterministic, runs on every record):** Queries Neo4j and PostgreSQL using taxonomy tags as index-based filters. Compares attribute values. Flags potential contradictions when values differ beyond tolerance thresholds.

**Layer 2 (semantic, runs only on flagged or ambiguous records):** Queries ChromaDB for semantically similar records. Sends matches to the LLM for detailed comparison. The LLM determines whether records are genuinely contradictory, refer to different scopes, or are compatible once unit conversion is applied.

**Contradiction resolution protocol:** Append-only. Both records retained. CONTRADICTS link in Neo4j. Contradiction logged in PostgreSQL. Flagged for human review. Never silently overwrite.

**Input/output schema references:** `relationship.schema.json` (input), `confidence_result.schema.json` (output).

---

#### Agent 8: Database Writer Agent

**Purpose:** Writes validated data to Neo4j, PostgreSQL, and ChromaDB. Also stages raw extracted tables.

**Skills required:**
- `database_writing.skill.md`: Cypher templates, SQL templates, ChromaDB upsert logic, merge key definitions, write ordering, consistency checks.
- `table_staging.skill.md`: Rules for staging raw extracted tables in PostgreSQL as faithful reproductions.

**Write logic principles:**

1. **Neo4j:** MERGE operations keyed on natural identity.
   - Country: merge on `{code}`
   - Mineral: merge on `{name, form}`
   - Organisation: merge on `{canonical_name}` (resolved via alias table)
   - PRODUCES: merge on `{subject, predicate, object, year, metric}`

2. **PostgreSQL analytical tables:** Populated in parallel with Neo4j.
   - MERGE (overwrite): Same merge key exists AND new record has equal/higher confidence AND validation = "approved". Previous values logged in history table.
   - APPEND: Same merge key exists but contradiction detected. Both retained.
   - INSERT: No matching record.

3. **PostgreSQL staging tables for raw tables:**
   - Every table extracted from a document is staged as-is in a `staged_tables` table. This preserves the original table structure (headers, rows, footnotes) exactly as extracted, before any interpretation or normalisation.
   - Schema: `staged_table_id`, `document_id`, `entity_id`, `page`, `caption`, `headers_json`, `rows_json`, `footnotes_json`, `csv_content`, `staged_at`.
   - This serves as a reference layer: analysts can query staged tables directly when they need the raw data before pipeline interpretation.

4. **ChromaDB:** Upsert by vector ID. Metadata refreshed on upsert.

**Input schema reference:** Validated data from Agents 6 and 7.

**Output schema reference:** `database_write_result.schema.json`
```json
{
  "document_id": "DOC-2024-00042",
  "page": 1,
  "write_results": {
    "neo4j": {
      "nodes_created": 4,
      "nodes_merged": 1,
      "relationships_created": 6,
      "relationships_merged": 0
    },
    "postgresql": {
      "analytical_rows_inserted": 6,
      "analytical_rows_updated": 0,
      "staged_tables_inserted": 1
    },
    "chromadb": {
      "vectors_upserted": 8
    }
  },
  "consistency_check": "passed"
}
```

---

#### Pipeline Orchestrator and Logging Service

**Purpose:** Manages end-to-end execution, maintains manifests, handles pause/resume, coordinates retry logic, and provides structured logging.

**Skills required:**
- `pipeline_orchestration.skill.md`: State machine rules, page-level processing flow, agent invocation order, error handling policy, pause/resume protocol.
- `logging.skill.md`: Log format, log levels, structured log fields, log storage.

**Processing model:**

Per page:
1. Agent 2 (structural extraction) → produces entities.
2. Agents 3a/3b/3c (text chunking, table interpretation, vision interpretation) → run in parallel on their respective entity types. Table interpretation and vision interpretation may invoke Agent 4 in support mode during this phase.
3. Agent 4 (taxonomy tagging, normal mode) → tags all processed entities.
4. Agent 5 (relationship extraction) → extracts relationships from tagged entities.
5. Agent 6 (summarisation and embedding) → generates summaries and embeddings.
6. Agent 7 (confidence and validation) → scores and validates relationships.
7. Agent 8 (database writer) → writes to all stores.
8. Manifest updated: page marked complete.

**Post-document pass:** After all pages complete, a document-level validation pass runs for cross-page consistency, entity merge resolution, and cross-entity relationship synthesis.

**Failure handling:**
- Page-level failure: Log failure, mark page as "failed" in manifest, proceed to next page.
- Agent-level failure on a page: Log the specific agent failure, mark the page as "partial_failure" with details of which agent failed, proceed to next page.
- Failed pages can be retried independently.

**Pause and resume:**
1. Pause completes current page processing.
2. Manifest updated with current state.
3. Resume checkpoint written: document_id, last completed page, pipeline version, model versions, pending flags.
4. On resume: read checkpoint, verify version compatibility (log warnings on mismatch), continue from first incomplete page.

**Structured log entry:**
```json
{
  "timestamp": "2026-04-13T10:05:02Z",
  "document_id": "DOC-2024-00042",
  "page": 1,
  "agent": "taxonomy_tagging",
  "mode": "normal",
  "action": "tag_entity",
  "input_ref": "DOC-2024-00042-P01-E001-L1-C001",
  "model_used": "qwen3.5:32b",
  "duration_ms": 2340,
  "tokens_used": { "input": 1200, "output": 380 },
  "status": "success",
  "output_summary": "Assigned 7 tags (2 countries, 1 mineral, 1 stage, 1 temporal, 1 metric, 1 form)"
}
```

---

## 4. Data architecture

### 4.1 Storage topology

```
/documents/                          # Document-nested storage
  DOC-2024-00042/
    raw/
      usgs_lithium_mcs_2024.pdf      # Original PDF (immutable)
    pages/
      page_001.png                   # Page images
      page_002.png
    entities/
      P01-E001/                      # Text block
        content.md
        metadata.json
      P01-E002/                      # Table
        table.png
        table.csv
        metadata.json
      P02-E003/                      # Chart
        chart.png
        chart.csv
        metadata.json
    chunks/
      P01-E001-L0.json              # Parent chunk
      P01-E001-L1-C001.json         # Child chunks
      P01-E001-L1-C002.json
    manifest.json                    # Processing manifest
    intake_log.json                  # Metadata scan log

/schemas/                            # Centralised output schema registry
  page_preparation_output.schema.json
  document_intake_output.schema.json
  ...

/skills/                             # Centralised skill directory
  task/
    page_preparation.skill.md
    document_intake.skill.md
    ...
  reference/
    taxonomy_reference.skill.md
    taxonomy_document.md             # The actual taxonomy
  config/
    model_routing.skill.md
    system_parameters.skill.md
  evolution/
    taxonomy_evolution.skill.md

Neo4j (local)
PostgreSQL (local)
ChromaDB
```

### 4.2 PostgreSQL schema

**Core analytical tables:**
- `production_volumes`: country_code, mineral, year, volume, unit, metric, form, confidence, confidence_band, extraction_type, source_document_id, entity_id, validation_status, created_at, updated_at
- `trade_flows`: exporter_code, importer_code, commodity, year, volume, value, currency, share_percent, confidence, extraction_type, source_document_id, entity_id, validation_status
- `prices`: mineral, date, price, currency, per_unit, price_type, extraction_method, confidence, source_document_id, entity_id, validation_status
- `reserves`: country_code, mineral, volume, unit, reserve_classification, year, confidence, source_document_id, entity_id, validation_status

**Staging tables:**
- `staged_tables`: staged_table_id, document_id, entity_id, page, caption, headers_json, rows_json, footnotes_json, csv_content, interpretation_status, staged_at

**System tables:**
- `documents`: document_id, raw_store_path, title, source_organisation, publication_date, source_type, source_registry_id, page_count, processing_status, created_at, updated_at
- `document_sources`: source_id, name, type, publisher, url, publication_frequency, document_count
- `processing_manifests`: manifest_id, document_id, pipeline_version, status, pages_json, model_versions_json, created_at, updated_at
- `pipeline_logs`: log_id, timestamp, document_id, page, agent, mode, action, input_ref, model_used, duration_ms, tokens_json, status, output_summary
- `contradiction_log`: contradiction_id, record_a_id, record_b_id, conflict_type, resolution_status, resolved_by, resolved_at, notes
- `taxonomy_evolution_queue`: proposal_id, proposed_by_agent, concept_mention, context, proposed_mapping_json, status, reviewed_by, reviewed_at
- `conversion_factor_log`: factor_id, mineral, form_from, form_to, factor_value, source, confidence, previous_value, changed_at, changed_by
- `organisation_aliases`: alias_id, canonical_name, alias, source_document_id, added_at
- `record_history`: history_id, table_name, record_id, field_name, old_value, new_value, change_reason, changed_at, source_document_id

### 4.3 Neo4j schema

**Node labels:** Country, Mineral, Organisation, Facility, Product, Policy, Technology, Document, Entity, Chunk

**Relationship types:** PRODUCES, SUPPLIES, TRADES, OPERATES, LOCATED_IN, OWNS, HAS_STAKE_IN, IMPORTS_FROM, EXPORTS_TO, REGULATES, RESTRICTS, PROCESSES_AT_STAGE, INVESTS_IN, DEPENDS_ON, RESERVES, PRICES, MEMBER_OF, EMPLOYS, EMITS, CONTRADICTS, EXTRACTED_FROM (provenance), PART_OF (hierarchy)

**Cross-document synthesis:** When querying by a shared entity (e.g., all records for Company A), the graph naturally aggregates all relationships involving that entity across all documents. This enables cross-document synthesis without a dedicated synthesis step. For analytical queries requiring a "single truth" selection from multiple records, a query-time resolution can apply confidence-based ranking: the highest-confidence, most-recent record is presented as the default view, with alternatives accessible.

### 4.4 ChromaDB collections

- `critical_minerals_entities`: Content and summary embeddings for all entity types. Metadata fields: document_id, page, entity_type, chunk_level, minerals (list), countries (list), supply_chain_stage, year, confidence_band.

---

## 5. Skills inventory

### 5.1 Task skills (24 total)

| Skill file | Used by | Purpose |
|---|---|---|
| `page_preparation.skill.md` | Agent 0 | PDF slicing, image conversion, base64 encoding |
| `document_intake.skill.md` | Agent 1 | Metadata extraction, field classification, stopping logic, progressive context |
| `document_source_registry.skill.md` | Agent 1 | Source matching, clustering, linking |
| `structural_extraction.skill.md` | Agent 2 | Entity type definitions, DeepSeek OCR configuration |
| `cross_page_entity.skill.md` | Agent 2 | Cross-page entity detection and merging |
| `text_chunking.skill.md` | Agent 3a | Hierarchical chunking, sizing, overlap, boundary rules |
| `adjacent_chunk_chaining.skill.md` | Agent 3a, Agent 5 | Rules for chaining adjacent chunks for expanded context |
| `table_interpretation.skill.md` | Agent 3b | Column mapping, value normalisation, acronym resolution |
| `table_structure_handling.skill.md` | Agent 3b | Merged cells, multi-level headers, footnotes, implicit groupings |
| `table_numeric_parsing.skill.md` | Agent 3b | Number parsing, qualifiers (W, e, NA), locale handling |
| `vision_interpretation.skill.md` | Agent 3c | Chart recognition, data extraction, extraction method annotation |
| `taxonomy_tagging.skill.md` | Agent 4 | Tagging rules, multi-label logic, normalisation, extensive examples |
| `taxonomy_support.skill.md` | Agent 4 | Inter-agent support protocol, request/response format, invocation conditions |
| `relationship_extraction_text.skill.md` | Agent 5 | Relationship extraction from narrative text |
| `relationship_extraction_table.skill.md` | Agent 5 | Relationship extraction from table rows |
| `relationship_extraction_chart.skill.md` | Agent 5 | Relationship extraction from chart data |
| `summarisation.skill.md` | Agent 6 | Summary generation rules and quality criteria |
| `embedding.skill.md` | Agent 6 | Embedding model config, ChromaDB collection management |
| `confidence_scoring.skill.md` | Agent 7 | Scoring formula, weights, band thresholds |
| `contradiction_detection.skill.md` | Agent 7 | Two-layer matching logic, resolution protocol |
| `validation_rules.skill.md` | Agent 7 | Domain-specific validation checks |
| `database_writing.skill.md` | Agent 8 | Cypher/SQL templates, merge keys, consistency rules |
| `table_staging.skill.md` | Agent 8 | Raw table staging rules for PostgreSQL |
| `pipeline_orchestration.skill.md` | Orchestrator | State machine, pause/resume, retry logic |
| `logging.skill.md` | Orchestrator | Log format, structured fields, storage |

### 5.2 Reference skills (1)

| Skill file | Used by | Purpose |
|---|---|---|
| `taxonomy_reference.skill.md` | Agents 3b, 4, 5, 7 | Access to the full taxonomy/ontology document |

### 5.3 Configuration skills (2)

| Skill file | Purpose |
|---|---|
| `model_routing.skill.md` | Which LLM model to use for which task, fallback rules |
| `system_parameters.skill.md` | Chunk sizes, confidence thresholds, DB connections, file paths |

### 5.4 Evolution skills (1)

| Skill file | Used by | Purpose |
|---|---|---|
| `taxonomy_evolution.skill.md` | Agent 4 | Controlled process for proposing and approving taxonomy additions |

---

## 6. Design decisions and resolved questions

### 6.1 Confirmed decisions (updated from v0.1)

1. Entities are stored nested under the document directory, with metadata fields linking back to source document and page.
2. PostgreSQL analytical tables are populated in parallel with Neo4j, not derived from it.
3. Neo4j is the canonical store for relationships. SQL tables are denormalised projections.
4. Tables, charts, and images are not chunked. Only text blocks undergo chunking.
5. Text chunking uses a hierarchical model: parent chunks (section-level, up to 2048 tokens) and child chunks (512 tokens, the primary embedding unit).
6. Cross-page entities are handled by stacking page images and re-processing jointly.
7. Contradictions are handled via append-only storage with CONTRADICTS links and human review flags.
8. The relationship extraction agent uses separate skills per entity type (text, table, chart).
9. All extractions carry `extraction_type` (direct/inferred) and `extraction_method` fields.
10. The taxonomy is a living "Library" with a controlled evolution mechanism.
11. The taxonomy tagging agent operates in two modes: normal tagging (Phase 3) and support invocation (Phase 2, for upstream agent disambiguation).
12. Output schemas are managed in a centralised registry under `/schemas/`.
13. Raw extracted tables are staged in PostgreSQL for reference before interpretation.
14. Document intake uses progressive context accumulation with compulsory/optional field classification, smart stopping, and a page cap of 8.
15. Conversion factors are initially sourced from LLM pre-trained knowledge, marked as "assumed", and logged. They can be updated and verified over time.
16. Organisation name resolution uses an alias table in the taxonomy/PostgreSQL.
17. The mineral hierarchy supports both group level (rare earth elements) and species level (neodymium), with MEMBER_OF relationships linking them.
18. Cross-document synthesis happens naturally through graph queries filtered by shared entities. Single-truth selection uses confidence-based ranking at query time.

### 6.2 Remaining design work

1. **Re-processing logic:** When the taxonomy is updated, a targeted re-processing workflow should identify which existing records are affected and re-run only the relevant pipeline stages on those records. The scope of impact depends on the type of taxonomy change (new entity type = no re-processing needed, changed conversion factor = re-processing of affected derived values, changed controlled vocabulary = re-tagging of affected entities). This logic needs detailed design.
2. **Human review interface:** The system flags items for human review (contradictions, low-confidence extractions, taxonomy evolution proposals). The interface for this can be designed later but should eventually support a queue-based workflow with approval/rejection actions.
3. **Performance optimisation:** As the database grows, monitoring query performance for contradiction detection (Layer 1 and Layer 2) and establishing indexing strategies for Neo4j and PostgreSQL.
4. **Testing and evaluation:** A testing set of 3-5 diverse document types with manually annotated expected outputs should be prepared to validate pipeline accuracy.

---

## 7. Next steps

1. **Draft the full taxonomy document** (`taxonomy_document.md`) with complete controlled vocabularies, conversion factors, and the organisation alias table.
2. **Define formal output schemas** (JSON Schema or Pydantic models) for all 15 inter-agent data formats listed in Section 3.3.
3. **Write the first skill documents**, prioritising: `taxonomy_reference.skill.md`, `taxonomy_tagging.skill.md`, `document_intake.skill.md`, `structural_extraction.skill.md`.
4. **Set up local infrastructure:** Neo4j, PostgreSQL (with schema from Section 4.2), ChromaDB, Ollama with Qwen 3.5 models, qwen3-embedding:8b.
5. **Build and test Agents 0 and 2** first (page preparation and structural extraction via DeepSeek OCR), as these are closest to Eddie's existing pipeline work.
6. **Integrate Agent 1** (document intake) with the source registry.
7. **Build Agent 4** (taxonomy tagging) and the taxonomy reference skill, as this is the most critical semantic component.
8. **Iteratively add remaining agents**, testing each against the manually annotated testing set.
