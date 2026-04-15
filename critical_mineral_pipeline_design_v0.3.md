# Critical Mineral Supply Chain Knowledge Pipeline

## Design Document v0.3

**Project context:** This pipeline is being developed as part of Eddie's doctoral research at the Institute for Manufacturing (IfM), University of Cambridge, within the Industrial Resilience Research Group and the Global Supply Chain Observatory (GSCO) project. The research sits at the intersection of knowledge management, R&D management, and LLMs, with a focus on how LLMs can elicit, structure, and govern tacit/implicit domain knowledge.

**Last updated:** 2026-04-14

**Changelog from v0.2:**
- Reorganised from numbered agents into six functional layers with clearer separation of deterministic, interpretive, governance, and persistence concerns.
- Introduced bronze/silver/gold epistemic tiering as a system-wide contract, not just a storage pattern.
- Added explicit scope dimensions to every extracted fact and relationship.
- Added machine-actionable dependency lineage to every downstream record.
- Introduced evidence packets as a standard output from every processing step.
- Added ambiguity resolution service with typed ambiguity handling (blocking vs non-blocking).
- Added taxonomy governance service as an offline triage and review function.
- Redesigned taxonomy tagging as LLM-native with constrained semantic execution framework.
- Introduced adjudication layer separating confidence evidence from tier promotion.
- Replaced single confidence score with evidence completeness model.
- Introduced record admissibility policy.
- Added semantic supersession and invalidation mechanics.
- Added document family priors as a first-class concept.
- Split taxonomy into three explicit sub-layers: canonical ontology, operational mapping registry, candidate extensions.
- Introduced "deterministic first, LLM second" as a system-wide design principle, applied per-task rather than per-agent.

---

## 1. System overview

### 1.1 Purpose

An end-to-end, LLM-native pipeline that processes unstructured PDF documents related to critical mineral supply chains, extracts and interprets all entities (text, tables, charts, images), tags them against a pre-defined domain taxonomy, extracts relationships, and writes structured knowledge into a graph database, relational database, and vector store. The system maintains full provenance, dependency lineage, and epistemic tiering from every extracted fact back to its source.

### 1.2 Application domain

The end-to-end critical mineral supply chain, covering the full lifecycle from geological exploration through mining, refining, processing, component manufacturing, product assembly, use, and recycling/recovery.

### 1.3 Core design principles

1. **Deterministic where possible, model where necessary, governed where consequential.** This is the single most important design principle. Every processing task is decomposed into sub-problems. Sub-problems that involve lookup, parsing, validation, or constraint satisfaction are handled deterministically. Sub-problems that involve genuine semantic judgement use LLMs with constrained prompts and bounded outputs. Sub-problems whose outputs have consequential downstream effects (tier promotion, contradiction resolution, taxonomy changes) are governed by explicit policies and audit trails.

2. **LLM-native where semantic understanding matters.** The pipeline's research contribution is demonstrating that LLMs can structure unstructured domain knowledge. The LLM is not bolted onto a conventional ETL pipeline; it is the interpretive core. But "LLM-native" does not mean "LLM-unconstrained." Every LLM call operates within a constrained semantic execution framework: structured prompts, ontology slices (not full taxonomy), bounded output schemas, and explicit uncertainty handling.

3. **Epistemic tiering (bronze/silver/gold).** Knowledge in the system exists at three trust levels. This is not a storage pattern; it is an epistemic contract that governs what the system is willing to assert. Bronze is "what the document seemed to say." Silver is "what the system thinks it means." Gold is "what the system is willing to expose as decision-grade." Tier assignment is a governance act, not merely a confidence threshold.

4. **Full provenance and dependency lineage.** Every downstream record carries machine-actionable lineage: which upstream entities, which taxonomy version, which conversion factors, which skill versions, and which model versions produced it. This enables precise invalidation and targeted re-processing.

5. **Living taxonomy with layered governance.** The domain taxonomy is split into three layers with distinct governance: canonical ontology (stable, versioned, human-approved), operational mapping registry (aliases, unit tables, source conventions), and candidate extensions (proposed by agents, queued for review).

6. **Fault tolerance and resumability.** Processing is page-level modular. Failure on any page does not halt the pipeline. All progress is checkpointed. Processing can be paused and resumed.

7. **Centralised schema management.** All inter-layer data formats are defined as formal output schemas in a central registry.

### 1.4 Technology stack

| Component | Technology | Role |
|---|---|---|
| LLM runtime | Ollama (local) | Hosts all generative and vision models |
| Primary LLMs | Qwen 3.5:32b, Qwen 3.5:27b | Semantic interpretation, tagging, relationship extraction, summarisation |
| Vision capability | Qwen 3.5 (multimodal) | Chart/figure interpretation |
| Embedding model | qwen3-embedding:8b | Vector embeddings |
| OCR/extraction | DeepSeek OCR (existing pipeline) | PDF page slicing and entity extraction |
| Graph database | Neo4j (local) | Entities, relationships, structural knowledge |
| Relational database | PostgreSQL (local) | Analytical projections, staging tables, logs, manifests, governance tables |
| Vector store | ChromaDB | Content and summary embeddings for semantic retrieval |
| Raw document store | Local filesystem (structured) | Original PDF files |

---

## 2. Architecture: six functional layers

### 2.1 Overview

The pipeline is organised into six functional layers rather than a flat list of numbered agents. Each layer has a distinct responsibility and a distinct relationship to determinism, model usage, and governance.

```
Layer 1: Deterministic Extraction and Normalisation
  ↓ produces bronze artefacts
Layer 2: Bounded Interpretation Services
  ↓ produces silver candidates
Layer 3: Ambiguity Resolution Service
  ↔ invoked by Layer 2 (blocking or non-blocking)
Layer 4: Taxonomy Governance Service
  ↔ offline, between processing runs
Layer 5: Adjudication and Trust Management
  ↓ promotes silver → gold or demotes gold → silver
Layer 6: Persistence and Retrieval
  ↓ writes to Neo4j, PostgreSQL, ChromaDB
```

### 2.2 What each layer owns

**Layer 1 (Deterministic Extraction and Normalisation):** Owns all work that does not require semantic judgement. PDF slicing, OCR, layout extraction, numeric parsing, dictionary and alias lookup, unit parsing, obvious schema mapping, hard validation, page image preparation, base64 encoding. Output: bronze artefacts (raw extracted entities with structural metadata, no semantic interpretation).

**Layer 2 (Bounded Interpretation Services):** Owns all work that requires semantic understanding. Text interpretation, table semantic mapping, vision interpretation, taxonomy tagging, relationship extraction, summarisation, embedding. Each service operates within a constrained semantic execution framework: structured prompts, ontology slices, bounded outputs, explicit uncertainty. Output: silver candidates (interpreted, tagged, relationship-extracted, but not yet adjudicated).

**Layer 3 (Ambiguity Resolution Service):** Owns the resolution of uncertainties that individual Layer 2 services cannot resolve alone. Receives typed ambiguity packets. Attempts resolution through a disciplined ladder: deterministic checks first, local evidence expansion second, document family priors third, model adjudication fourth. Routes outcomes back to the calling service or escalates to human review. Operates both synchronously (for blocking ambiguities) and asynchronously (for non-blocking ambiguities).

**Layer 4 (Taxonomy Governance Service):** Owns the controlled evolution of the taxonomy. Clusters unknown concepts proposed by Layer 2 services. Scores proposals by frequency and impact. Checks whether proposals are genuinely new or aliases of existing concepts. Produces review packages for human approval. Triggers targeted re-processing after taxonomy changes. Operates offline, between processing runs.

**Layer 5 (Adjudication and Trust Management):** Owns the promotion and demotion of knowledge between tiers. Computes evidence completeness (not just a single confidence score). Classifies contradictions (with scope alignment). Applies admissibility rules to determine whether silver records qualify for gold. Manages the human review queue. Can demote gold records back to silver when new evidence warrants it.

**Layer 6 (Persistence and Retrieval):** Owns all writes to Neo4j, PostgreSQL, and ChromaDB. Manages bronze, silver, and gold stores. Handles merge-vs-append logic. Maintains dependency lineage. Processes invalidation and re-build requests. Stages raw extracted tables.

---

## 3. Taxonomy and ontology (the "Library")

### 3.1 Three-layer taxonomy architecture

The taxonomy is split into three layers with distinct governance, versioning, and access patterns.

#### Layer A: Canonical ontology (stable, versioned, human-approved)

This layer contains the settled, structural definitions of the domain. Changes are infrequent and require explicit human approval.

Contents:
- Entity type definitions (Mineral/Material, Country/Region, Organisation, Facility/Site, Product/Component, Policy/Regulation, Technology/Process)
- Relationship type definitions (PRODUCES, SUPPLIES, IMPORTS, etc.) with their attribute schemas
- Supply chain stage vocabulary (Exploration through Recycling/Recovery)
- Mineral hierarchy (groups and species, with MEMBER_OF links)
- Quantitative attribute type definitions (Volume, Value, Capacity, Price, Percentage, Temporal)
- Source type enumeration with default reliability weights
- Scope dimension definitions (see Section 4.3)

Version control: Semantic versioning (major.minor.patch). Major versions indicate breaking changes to entity or relationship type definitions. Minor versions indicate new additions. Patch versions indicate corrections.

#### Layer B: Operational mapping registry (dynamic, machine-maintained, human-reviewable)

This layer contains the practical mappings that connect raw document content to canonical ontology concepts. It changes frequently as new documents are processed.

Contents:
- Organisation alias table (BHP → BHP Group, BHP Billiton → BHP Group, etc.)
- Unit and form conversion factors with source and verification status
- Country name variants and ISO code mappings
- Mineral name variants and abbreviation mappings (LCE → lithium_carbonate_equivalent, REO → rare_earth_oxide)
- Source family conventions (e.g., "USGS MCS reports lithium in tonnes of contained lithium metal")
- Common table qualifier symbols (e, W, NA, -, etc.) with standardised meanings

Governance: Machine-maintained with human-reviewable audit trail. New entries can be added automatically when confidence is high (exact alias match), or queued for review when confidence is lower (fuzzy match, novel abbreviation).

#### Layer C: Candidate extensions (proposed, queued, not yet canonical)

This layer holds concepts, relationships, or mappings that agents have proposed but that have not yet been reviewed and accepted.

Contents:
- Proposed new entity types or subtypes
- Proposed new relationship types
- Proposed new controlled vocabulary entries
- Proposed new conversion factors from LLM pre-trained knowledge (marked as "assumed")
- Proposed new aliases or abbreviation mappings

Governance: All entries are proposals. They cannot influence gold-tier records until promoted to Layer A or Layer B. They can influence silver-tier records if the processing pipeline explicitly allows candidate-tier mappings for interpretation (with a flag marking the dependency).

### 3.2 Taxonomy evolution lifecycle

```
Agent encounters unknown concept
  → Emits structured proposal to Layer C (candidate queue)
  → Taxonomy Governance Service (Layer 4) clusters proposals
  → Human reviewer receives review package
  → Approved → promoted to Layer A (if structural) or Layer B (if operational)
  → Rejected → marked as noise, retained for audit
  → Merged → mapped to existing concept, alias added to Layer B
  → After promotion: targeted re-processing of affected silver/gold records
```

### 3.3 Entity types (from canonical ontology, Layer A)

| Entity type | Description | Hierarchy |
|---|---|---|
| Mineral/Material | A mineral commodity or processed material | Two-level: group (e.g., rare earth elements) and species (e.g., neodymium). MEMBER_OF relationships link species to groups. |
| Country/Region | A geographic entity | ISO 3166-1 alpha-3 codes |
| Organisation | Any supply chain participant | Canonical names with alias table in Layer B |
| Facility/Site | Physical supply chain location | Subtypes: mine, refinery, processing_plant, smelter, recycling_facility, port |
| Product/Component | Manufactured items or intermediates | Battery cells, cathodes, anodes, precursors, concentrates, refined chemicals |
| Policy/Regulation | Rules, laws, agreements | Export controls, trade agreements, environmental standards |
| Technology/Process | Methods and technologies | Extraction methods (DLE, brine evaporation, hard-rock mining), refining, recycling |

### 3.4 Relationship types (from canonical ontology, Layer A)

| Relationship | Subject → Object | Key attributes |
|---|---|---|
| PRODUCES | Country/Facility → Mineral | volume, unit, metric, year, capacity_type |
| SUPPLIES / TRADES | Entity → Entity | commodity, volume, value, currency, time_period |
| OPERATES | Organisation → Facility | ownership_percent, start_date |
| LOCATED_IN | Facility → Country/Region | |
| OWNS / HAS_STAKE_IN | Organisation → Organisation/Facility | ownership_percent, acquisition_date |
| IMPORTS / EXPORTS | Country → Country | commodity, volume, value, currency, year, share_percent |
| REGULATES / RESTRICTS | Policy → Commodity/Activity/Country | effective_date, scope |
| PROCESSES_AT_STAGE | Facility → Mineral | supply_chain_stage |
| INVESTS_IN | Organisation → Facility/Project | investment_amount, currency, year |
| DEPENDS_ON | Product/Component → Mineral | quantity_per_unit, unit |
| RESERVES | Country → Mineral | volume, unit, reserve_classification |
| PRICES | Mineral → (temporal) | price, currency, unit, price_type, date |
| MEMBER_OF | Mineral (species) → Mineral (group) | structural |
| EMPLOYS | Organisation/Facility → (workforce) | headcount, year, skill_category |
| EMITS | Facility/Process → (environmental) | co2_per_tonne, water_usage, year |

### 3.5 Conversion factor management

Conversion factors live in Layer B (operational mapping registry). Each factor carries:

| Field | Description |
|---|---|
| mineral | The mineral this factor applies to |
| form_from | Source form (e.g., spodumene_concentrate_6pct) |
| form_to | Target form (e.g., contained_lithium_metal) |
| factor_value | The multiplication factor |
| source | Where this factor came from (llm_pretrained, usgs_factsheet, academic_paper, etc.) |
| verification_status | assumed, verified, disputed |
| verified_against | Reference document/URL if verified |
| last_updated | Timestamp |

**Epistemic rule:** Conversion factors with `verification_status: assumed` can produce silver-tier derived values but are forbidden from automatic gold promotion. Any analytical view using assumed factors must visibly flag this dependency.

### 3.6 Source type enumeration with reliability weights

| Source type | Default reliability weight |
|---|---|
| government_report | 0.95 |
| academic_paper | 0.90 |
| trade_statistics | 0.90 |
| technical_standard | 0.85 |
| policy_document | 0.85 |
| company_annual_report | 0.80 |
| industry_analysis | 0.75 |
| market_report | 0.70 |
| patent | 0.70 |
| news_article | 0.55 |

### 3.7 Document family priors

The source registry (from v0.2) is elevated to a first-class concept. Document families are groups of documents from the same source series (e.g., all USGS Mineral Commodity Summaries, all company annual reports from BHP). Each family can carry:

- **Structural conventions:** How this source typically formats tables, what units it uses, what abbreviations are standard.
- **Reporting basis priors:** "USGS MCS always reports lithium in tonnes of contained lithium metal." "Company X reports in LCE."
- **Reliability modifiers:** A specific source family may be more or less reliable than its generic source type suggests.
- **Parsing templates:** Source-specific table header mappings that have been verified in prior documents.

Document family priors are stored in Layer B (operational mapping registry) and can be referenced by Layer 2 interpretation services to improve accuracy without additional LLM calls.

---

## 4. Core data structures

### 4.1 Evidence packets

Every processing step in the pipeline outputs an evidence packet alongside its primary output. This is a system-wide standard, not optional.

```json
{
  "step_id": "STEP-00042-P01-TAG-001",
  "agent": "taxonomy_tagging",
  "layer": 2,
  "input_refs": ["DOC-2024-00042-P01-E001-L1-C001"],
  "candidate_interpretations": [
    {
      "interpretation": "production_volume refers to mining stage output",
      "evidence": "text says 'producer' and 'output'",
      "confidence": "high"
    },
    {
      "interpretation": "production_volume refers to refining output",
      "evidence": null,
      "confidence": "low"
    }
  ],
  "chosen_interpretation": "production_volume refers to mining stage output",
  "reason": "Explicit use of 'producer' in mining context; USGS MCS convention",
  "unresolved": [],
  "deterministic_checks_passed": ["country_iso_valid", "mineral_in_taxonomy", "unit_parseable", "temporal_valid"],
  "model_used": "qwen3.5:32b",
  "model_call_count": 1,
  "taxonomy_version": "0.3.0",
  "skill_versions": { "taxonomy_tagging": "0.2.1", "taxonomy_reference": "0.3.0" }
}
```

Evidence packets serve three purposes: auditability (why was this decision made?), re-processing (which versions produced this?), and future model training (labelled decision data for fine-tuning specialist models).

### 4.2 Epistemic tiers

| Tier | Definition | Who assigns | What it means | Can be used for |
|---|---|---|---|---|
| Bronze | Raw extraction output | Layer 1 (automatic) | "What the document seemed to say." Structurally parsed but not semantically interpreted. | Provenance, raw reference, debugging |
| Silver | Interpreted, tagged, relationship-extracted | Layer 2 (automatic), Layer 5 (may revise) | "What the system thinks it means." Semantically processed but not yet adjudicated for decision use. | Research analysis, exploration, hypothesis generation |
| Gold | Adjudicated, admissible | Layer 5 (explicit promotion) | "What the system is willing to expose as decision-grade." Meets admissibility criteria. | Analytical tables, dashboards, downstream systems, publications |

**Promotion criteria (silver → gold):**
- All blocking ambiguities resolved
- No unresolved contradictions with existing gold records
- Evidence completeness above threshold (all required scope dimensions populated)
- No dependency on assumed (unverified) conversion factors
- Source type meets minimum reliability threshold for the record class
- Optionally: human approval for specific record classes

**Demotion triggers (gold → silver):**
- New contradictory evidence from a credible source
- Source retraction or correction
- Conversion factor revision that affects derived values
- Taxonomy change that invalidates the tagging basis
- Human review decision

### 4.3 Scope dimensions

Every extracted fact and relationship carries explicit scope descriptors. These are checked before contradiction detection and are part of the admissibility criteria for gold promotion.

| Scope dimension | Description | Example values |
|---|---|---|
| material_form | What form the quantity is measured in | contained_metal, spodumene_concentrate, LCE, Li2CO3, REO, ore |
| metric_basis | What the number represents | production_volume, refining_output, export_volume, capacity_nameplate, capacity_actual, reserves |
| geographic_scope | What geography the data covers | country_level, facility_level, regional, global |
| temporal_scope | What time period the data covers | calendar_year_2023, fiscal_year_2023, Q1_2024, monthly_jan_2024, cumulative |
| reporting_basis | How the reporter defines the metric | company_estimate, national_statistics, survey_based, satellite_derived |
| data_source_basis | Primary vs secondary reporting | primary_source, secondary_compilation, third_party_estimate |

**These are not just metadata fields.** They are part of the relationship schema and are used in:
- Contradiction detection: Two records with different scope dimensions are not contradictory; they are measuring different things.
- Admissibility: Gold-tier records must have all required scope dimensions populated.
- Query-time truth ranking: When multiple records exist for the same entity, scope dimensions allow users to select the appropriate one.

### 4.4 Dependency lineage

Every silver and gold record carries a lineage block:

```json
{
  "lineage": {
    "source_document_id": "DOC-2024-00042",
    "source_entity_ids": ["DOC-2024-00042-P01-E001"],
    "source_chunk_ids": ["DOC-2024-00042-P01-E001-L1-C001"],
    "taxonomy_version": "0.3.0",
    "conversion_factors_used": [
      { "factor_id": "CF-Li-spod-metal", "version": "0.1.0", "verification_status": "assumed" }
    ],
    "skill_versions": {
      "taxonomy_tagging": "0.2.1",
      "relationship_extraction_text": "0.1.3"
    },
    "model_versions": {
      "tagging_model": "qwen3.5:32b",
      "extraction_model": "qwen3.5:32b"
    },
    "processing_timestamp": "2026-04-14T10:05:00Z",
    "evidence_packet_refs": ["STEP-00042-P01-TAG-001", "STEP-00042-P01-REL-001"]
  }
}
```

This lineage is machine-actionable. When a taxonomy version is incremented, a query can identify all records produced under the old version and flag them for re-processing. When a conversion factor is revised, all records that used that factor can be identified and recalculated.

### 4.5 Semantic supersession

When a silver or gold record is updated (not just appended), the system creates a semantic diff:

```json
{
  "supersession_id": "SUP-00042-001",
  "record_id": "REL-00042-001",
  "previous_version": {
    "volume": 61000,
    "metric": "lithium_content",
    "source": "DOC-2023-00018"
  },
  "new_version": {
    "volume": 86000,
    "metric": "lithium_content",
    "source": "DOC-2024-00042"
  },
  "changed_fields": ["volume"],
  "reason": "Updated figure from newer USGS MCS edition",
  "affected_descendants": ["DERIVED-00042-001", "DERIVED-00042-002"],
  "superseded_at": "2026-04-14T10:10:00Z"
}
```

This is distinct from contradiction logging. Supersession means the old value is replaced by a newer, more authoritative value. Contradiction means two values coexist because the system cannot determine which is correct.

---

## 5. Layer 1: Deterministic extraction and normalisation

### 5.1 Responsibilities

This layer handles all work that does not require semantic judgement. Its output is bronze-tier artefacts: structurally parsed, not semantically interpreted.

### 5.2 Components

#### 5.2.1 Page preparation

Identical to Agent 0 in v0.2. PDF slicing, PNG conversion, base64 encoding. Purely deterministic.

**Skills:** `page_preparation.skill.md`

**Output:** Page images and base64 representations stored under the document directory.

#### 5.2.2 Document intake

Revised from v0.2 Agent 1. The metadata extraction process still uses LLM for reading page content (this is inherently multimodal), but the progressive scanning logic, field classification (compulsory/optional), stopping rules, and page cap are deterministic control logic.

**Skills:** `document_intake.skill.md`, `document_source_registry.skill.md`

**Process:** As defined in v0.2: forward scan with progressive context accumulation, backward scan if compulsory fields missing, three-page overshoot, 8-page cap. Source registry check and document registration.

**Output:** Document registration record, processing manifest, source registry linkage. All bronze tier.

#### 5.2.3 Structural extraction (DeepSeek OCR)

Identical to Agent 2 in v0.2. Runs DeepSeek OCR pipeline on each page. Produces typed entities: text blocks (markdown with layout), tables (image + CSV), charts (image + CSV), standalone images.

**Skills:** `structural_extraction.skill.md`, `cross_page_entity.skill.md`

**Entity storage:** Document-nested (as revised in v0.2).

**Output:** Bronze entities with structural metadata, stored under `/documents/DOC-xxxx/entities/`.

#### 5.2.4 Deterministic normalisation pass

**This is new in v0.3.** After structural extraction, a deterministic pass runs over all extracted entities to perform normalisation tasks that do not require semantic judgement.

**Skills:** `deterministic_normalisation.skill.md`

**What it does:**
- **Country name resolution:** Matches country mentions against a gazetteer and alias table. "Australia" → AUS, "PRC" → CHN, "DRC" → COD. Uses exact and fuzzy matching. Unresolved names are flagged for Layer 2.
- **Mineral name resolution:** Matches mineral mentions against the mineral dictionary. "lithium" → lithium, "Li" → lithium, "REO" → rare_earth_oxide. Unresolved terms flagged.
- **Unit parsing:** Parses unit strings into canonical units. "kt" → kilotonnes (×1000 tonnes), "Mt" → megatonnes (×1000000 tonnes), "t" → tonnes. Uses the unit table from Layer B of the taxonomy.
- **Temporal parsing:** Extracts dates, years, quarters from text. "In 2023" → year: 2023. "Q1 2024" → quarter: Q1, year: 2024. "FY2023" → fiscal_year: 2023 (flagged as fiscal, not calendar).
- **Numeric parsing:** Parses numbers from table cells. Handles thousands separators, ranges, qualifiers (e, W, NA, -, ~).
- **Organisation alias resolution:** Matches organisation names against the alias table in Layer B. "BHP Billiton" → BHP Group. Novel names flagged for Layer 2/Layer 4.
- **Known table qualifier mapping:** "e" → estimated, "W" → withheld, "NA" → not_available, "-" → zero_or_nil, "—" → zero_or_nil.

**Output:** Annotated bronze entities. Each entity now carries a `deterministic_annotations` block listing all successful lookups and all unresolved items that need Layer 2 attention.

```json
{
  "entity_id": "DOC-2024-00042-P01-E001",
  "deterministic_annotations": {
    "resolved": [
      { "mention": "Australia", "type": "country", "value": "AUS", "method": "gazetteer_exact" },
      { "mention": "lithium", "type": "mineral", "value": "lithium", "method": "dictionary_exact" },
      { "mention": "2023", "type": "temporal", "value": { "year": 2023 }, "method": "regex_year" },
      { "mention": "86,000 tonnes", "type": "quantity", "value": 86000, "unit": "tonnes", "method": "numeric_parser" }
    ],
    "unresolved": [
      { "mention": "spodumene concentrate", "type": "mineral_form", "reason": "requires context to confirm form mapping" },
      { "mention": "producer", "type": "supply_chain_stage", "reason": "requires semantic inference" }
    ]
  }
}
```

This pass significantly reduces the work Layer 2 must do. For tables with clean headers and well-known entities, the deterministic pass may resolve 60-75% of tagging work before the LLM is invoked.

#### 5.2.5 Text chunking

Identical to Agent 3a in v0.2. Hierarchical chunking with parent chunks (section-level, up to 2048 tokens) and child chunks (512 tokens with 10-15% overlap). Adjacent chunk linking via previous/next IDs. Deterministic process.

**Skills:** `text_chunking.skill.md`, `adjacent_chunk_chaining.skill.md`

---

## 6. Layer 2: Bounded interpretation services

### 6.1 Design principle: constrained semantic execution

Every Layer 2 service operates within a constrained semantic execution framework. This means:

1. **Ontology slices, not full taxonomy.** Each LLM call receives only the relevant portion of the taxonomy for the entity type being processed. This reduces noise, cost, and the chance of spurious mappings.

2. **Structured prompts with task contracts.** Every prompt specifies what the model must do, what it must not do, which output format is required, what to do when uncertain, and which enum values are allowed.

3. **Explicit uncertainty protocol.** The model is explicitly told it is allowed to say: `unknown`, `ambiguous`, `candidate_a_vs_candidate_b`, `needs_escalation`. Forcing a guess is never preferred over declaring uncertainty.

4. **Bounded outputs.** All outputs conform to a JSON schema. The model is instructed to return only valid schema values where controlled vocabularies exist.

5. **Deterministic pre-annotations as input.** Layer 2 services receive the deterministic annotations from Layer 1 Section 5.2.4. They do not re-derive what has already been resolved. They focus on the unresolved residue and on higher-level semantic tasks (stage inference, relationship extraction, contextual disambiguation).

### 6.2 Table interpretation service

Revised from v0.2 Agent 3b. Now receives deterministic annotations alongside the raw table.

**Skills:** `table_interpretation.skill.md`, `table_structure_handling.skill.md`, `table_numeric_parsing.skill.md`, `taxonomy_reference.skill.md`

**LLM task contract:** Given the table headers, a sample of rows, the caption, document family priors (if available), and the deterministic annotations already applied, the LLM is asked to:
- Interpret each column header: what entity type or attribute it maps to, what unit, what metric.
- Resolve any ambiguities flagged by Layer 1 (e.g., "spodumene concentrate" confirmation, metric disambiguation).
- Map column semantics to taxonomy relationship types.
- Not invent new taxonomy values unless explicitly marking them as candidates.
- Use only allowed enum values from the ontology slice provided.
- Declare uncertainty explicitly when it exists.

**Output:** Interpreted table with column mappings, parsed rows, confidence per column, ambiguities resolved, and ambiguities remaining. All silver tier.

If blocking ambiguities remain (e.g., cannot determine whether the metric is contained metal or ore), the service emits an ambiguity packet to Layer 3.

### 6.3 Vision interpretation service

Revised from v0.2 Agent 3c. Same core logic but now with extraction method vocabulary and cross-reference against DeepSeek OCR CSV.

**Skills:** `vision_interpretation.skill.md`

**Output:** Chart interpretation with per-data-point extraction methods, narrative summary, confidence. Silver tier.

### 6.4 Taxonomy tagging service

This is the most important Layer 2 service. Significantly redesigned in v0.3 based on the consultant dialogue.

**Skills:** `taxonomy_tagging.skill.md`, `taxonomy_reference.skill.md`, `taxonomy_support.skill.md`

**Design: LLM-native with constrained semantic execution framework.**

The tagging service operates as a multi-step process:

**Step 1: Receive entity with deterministic pre-annotations.**
The service receives the entity content, its type, local context, provenance, and the deterministic annotations from Layer 1. Many simple tags (country codes, mineral names, dates, units) are already resolved. The service does not re-derive these; it accepts them as given.

**Step 2: Primary tagging call (LLM).**
The LLM receives:
- The entity content
- The deterministic annotations (as established facts, not as candidates to re-evaluate)
- The relevant ontology slice (entity-type-specific, not the full taxonomy)
- Source family priors (if available for this document source)
- Allowed enum values for each tag type
- The uncertainty protocol (allowed to say unknown/ambiguous)
- Few-shot examples from the skill document showing correct tagging for similar entities

The LLM produces structured candidate tags. Each tag includes:

```json
{
  "type": "metric_type",
  "value": "production_volume",
  "mention": "output of 86,000 tonnes",
  "support_type": "inferred",
  "normalisation_method": "contextual_inference",
  "confidence": "high",
  "reasoning": "Text says 'producer' and 'output' in mining context. USGS MCS convention reports mining-stage production."
}
```

The `support_type` field is critical: `explicit` means the tag is directly stated in the text; `inferred` means the tag requires interpretation. This feeds into admissibility scoring.

**Step 3: Deterministic validation (tools/skills).**
After the LLM call, a battery of deterministic checks runs:
- Pydantic schema validation (structural correctness)
- Enum membership checks (are all tag values in the controlled vocabulary?)
- Cross-field constraint checks (e.g., if type is "mineral" and form is specified, is that form valid for that mineral?)
- Unit legality checks (is the unit valid for the metric type?)
- Alias resolution verification (does the normalised value exist in the canonical ontology or operational mapping?)

If validation fails, the output is repaired if possible (e.g., correcting a near-miss enum value) or the tagging call is retried once with the validation error included in the prompt.

**Step 4: Semantic verification (optional second LLM pass).**
For entities where tagging confidence is medium or where inferred tags are present, a verification pass asks:
- Are the proposed tags semantically supported by the provided evidence?
- Which tags are strongly supported vs weakly supported?
- Are there alternative interpretations that should be recorded?

This pass is not run on every entity. It is triggered when the primary tagging call produces any tag with `confidence: medium` or `support_type: inferred` on a consequential tag type (metric, stage, relationship-relevant attributes).

**Step 5: Output decision.**
Based on the validation and verification results:
- Accept as silver (all tags validated, no ambiguities)
- Accept with ambiguity flag (some tags are uncertain, non-blocking)
- Emit ambiguity packet to Layer 3 (blocking ambiguity detected)
- Send to human review queue (validation failed after retry, or very low confidence)

**Taxonomy support mode (invoked by other Layer 2 services):**
As defined in v0.2, the tagging service can be invoked by upstream services (table interpretation, vision interpretation) when they encounter domain terminology they cannot resolve. The invocation conditions remain: the upstream service encounters a term it cannot interpret, that interpretation is required to complete its own task, and local context is insufficient.

**Unrecognised concept handling:**
When the LLM encounters a concept not in the taxonomy, it emits a proposal to the Layer C candidate queue via the taxonomy evolution protocol. The concept is tagged with a provisional value (if the LLM can suggest one) and flagged as `taxonomy_candidate`. Silver records may use candidate tags but they are ineligible for gold promotion until the candidate is either accepted into the canonical ontology or mapped to an existing concept.

### 6.5 Relationship extraction service

Revised from v0.2 Agent 5. Same split by entity type (text, table, chart) with separate skills. Now also receives deterministic annotations and taxonomy tags, reducing redundant inference.

**Skills:** `relationship_extraction_text.skill.md`, `relationship_extraction_table.skill.md`, `relationship_extraction_chart.skill.md`, `taxonomy_reference.skill.md`, `adjacent_chunk_chaining.skill.md`

**Key addition in v0.3:** Every extracted relationship now carries full scope dimensions (Section 4.3) as mandatory fields. The LLM is explicitly prompted to populate material_form, metric_basis, geographic_scope, temporal_scope, reporting_basis, and data_source_basis. If a scope dimension cannot be determined, it is marked as `unspecified` and the relationship is flagged as having incomplete scope (which affects gold admissibility).

**Output schema (revised):**
```json
{
  "relationship_id": "REL-00042-001",
  "subject": { "type": "country", "value": "AUS" },
  "predicate": "PRODUCES",
  "object": { "type": "mineral", "value": "lithium" },
  "attributes": {
    "volume": 86000,
    "unit": "tonnes"
  },
  "scope": {
    "material_form": "lithium_content",
    "metric_basis": "production_volume",
    "geographic_scope": "country_level",
    "temporal_scope": "calendar_year_2023",
    "reporting_basis": "national_statistics",
    "data_source_basis": "primary_source"
  },
  "extraction_type": "direct",
  "provenance": {
    "document_id": "DOC-2024-00042",
    "entity_id": "DOC-2024-00042-P01-E001",
    "chunk_id": "DOC-2024-00042-P01-E001-L1-C001",
    "page": 1,
    "source_text": "Australia remained the world's leading lithium producer, with an estimated output of 86,000 tonnes"
  },
  "tier": "silver",
  "lineage": { ... },
  "evidence_packet_ref": "STEP-00042-P01-REL-001"
}
```

### 6.6 Summarisation and embedding service

Revised from v0.2 Agent 6. No major structural changes. Summaries are explicitly designated as downstream conveniences, not epistemic anchors. They are not used for contradiction detection or admissibility decisions. They exist for retrieval and human consumption.

**Skills:** `summarisation.skill.md`, `embedding.skill.md`

**Output:** Summary text, content and summary vector IDs, ChromaDB metadata with taxonomy tags and scope dimensions.

---

## 7. Layer 3: Ambiguity resolution service

### 7.1 Purpose

A centralised broker for uncertainties that individual Layer 2 services cannot resolve alone. Prevents every service from solving ambiguity in its own bespoke way. Creates a reusable audit trail of uncertainty.

### 7.2 Typed ambiguity handling

Ambiguities are classified by type and severity. Severity determines whether resolution is blocking (the calling service pauses) or non-blocking (the calling service proceeds with a best-effort silver record and the ambiguity service reviews asynchronously).

**Blocking ambiguities (synchronous resolution required):**
- Unit basis ambiguity (cannot determine whether "t" means tonnes or short tons)
- Material form ambiguity (cannot determine whether "production" refers to ore, concentrate, or contained metal)
- Entity identity ambiguity (merge key depends on resolution, e.g., is "Pilbara" the company or the region?)
- Table header semantics (cannot interpret a column without domain knowledge)
- Capacity vs output ambiguity (the value could be either, and the distinction matters)

**Non-blocking ambiguities (asynchronous resolution):**
- Supply chain stage classification (mining vs refining, when unclear but not critical for immediate processing)
- Policy vs market commentary classification
- Soft narrative interpretation (summary wording)
- Organisation alias suggestions (possible match but not certain)
- Temporal scope precision (year known but quarter uncertain)

### 7.3 Resolution ladder

When the ambiguity service receives a packet, it follows a disciplined sequence:

**Step 1: Deterministic resolution.**
Check alias tables, ontology mappings, unit dictionaries, document source family priors, surrounding captions, section headings, and table notes. Many ambiguities that seem semantic can actually be resolved by looking up source conventions.

**Step 2: Local evidence expansion.**
Pull adjacent chunks, neighbouring pages, footnotes, table notes, section introductions, and document metadata. The answer may be in context the calling service did not have.

**Step 3: Document family priors.**
Check whether the same source series or publisher consistently uses the ambiguous term in one way. If USGS MCS always reports lithium in contained metal, and this is a USGS MCS document, that is strong evidence.

**Step 4: Model-based adjudication.**
Only now, if the ambiguity persists, ask the LLM to choose among bounded candidates or explain why uncertainty remains. The LLM receives the ambiguity packet, all evidence gathered in steps 1-3, and the candidate interpretations. It is asked to choose or to confirm that the ambiguity is genuine.

**Step 5: Route outcome.**
- Resolved with high confidence → return resolution to calling service (or update the silver record if asynchronous)
- Resolved with moderate confidence → return resolution with a confidence flag
- Multiple candidates remain → return ranked candidates with probabilities; record remains silver with ambiguity annotation
- Unresolvable → escalate to human review queue

### 7.4 Ambiguity packet format

```json
{
  "ambiguity_id": "AMB-00042-001",
  "requesting_service": "table_interpretation",
  "ambiguity_type": "material_form",
  "severity": "blocking",
  "unresolved_item": "Production (t)",
  "context": {
    "entity_id": "DOC-2024-00042-P01-E002",
    "table_caption": "World Mine Production and Reserves",
    "document_source_family": "USGS Mineral Commodity Summaries",
    "surrounding_text": "estimated output of 86,000 tonnes of lithium content"
  },
  "candidate_interpretations": [
    { "interpretation": "lithium_content (contained metal)", "evidence": "USGS MCS convention", "plausibility": "high" },
    { "interpretation": "spodumene_concentrate", "evidence": "heading mentions 'mine production'", "plausibility": "low" },
    { "interpretation": "lithium_carbonate_equivalent", "evidence": null, "plausibility": "very_low" }
  ],
  "downstream_consequence": "Affects volume normalisation, contradiction detection, and all derived analytical records"
}
```

---

## 8. Layer 4: Taxonomy governance service

### 8.1 Purpose

Manages the controlled evolution of the taxonomy. Operates offline (between processing runs), not as a runtime service.

### 8.2 Responsibilities

1. **Cluster candidate proposals.** Multiple documents may independently surface the same unknown concept. The governance service groups these by semantic similarity and frequency.
2. **Score proposals by impact.** How many existing records would be affected if this concept were added? How frequently has it appeared?
3. **Check for duplicates.** Is the proposed concept actually an alias of an existing concept? Is it a synonym? A sub-type?
4. **Produce review packages.** For each proposal (or cluster of proposals), prepare a human-readable review package: the concept, its proposed mapping, all the contexts in which it appeared, the frequency, the impact, and a recommendation (add, alias, reject).
5. **Apply approved changes.** Merge approved additions into Layer A (canonical ontology) or Layer B (operational mapping). Increment taxonomy version.
6. **Trigger targeted re-processing.** After a taxonomy change, identify all records whose lineage depends on the changed taxonomy version. Flag them for re-processing. The re-processing scope depends on the change type:
   - New entity type or relationship type: no re-processing needed (existing records are unaffected)
   - New controlled vocabulary entry: re-tag entities that contained the previously-unrecognised concept
   - Changed conversion factor: recalculate all derived values that used the old factor
   - Changed alias mapping: re-tag entities that used the old alias

### 8.3 Skills

- `taxonomy_governance.skill.md`: Clustering logic, scoring criteria, duplicate detection, review package format, re-processing trigger rules.

---

## 9. Layer 5: Adjudication and trust management

### 9.1 Purpose

Separates "is this plausible?" from "is this admissible for downstream use?" Plausibility is computed by Layer 2 services. Admissibility is decided by Layer 5 based on governance policies.

### 9.2 Evidence completeness (replacing single confidence score)

In v0.3, the single weighted confidence score is replaced by an evidence completeness model. Instead of computing one number, the adjudication layer checks a set of evidence conditions:

| Condition | Description | Required for gold? |
|---|---|---|
| Source reliability | Source type reliability weight ≥ threshold | Yes |
| Extraction clarity | Extraction type is `direct` or `inferred` with justification | Yes |
| Scope completeness | All six scope dimensions populated (no `unspecified`) | Yes |
| No blocking ambiguities | All blocking ambiguities resolved | Yes |
| No unresolved contradictions | No active CONTRADICTS links with other gold records | Yes |
| No assumed conversions | No dependency on unverified conversion factors | Yes |
| Pydantic valid | Output passes schema validation | Yes |
| Corroboration | Same fact found in at least one other document | No (improves ranking) |
| Human approval | Explicitly reviewed and approved by human | No (required for specific record classes) |

Gold promotion requires all "Yes" conditions to be met. Records that meet most but not all conditions remain silver with a note indicating which conditions are unmet.

This replaces the pseudo-precise 0-1 confidence score with a transparent checklist. Downstream consumers can see exactly why a record is gold or silver, not just a number.

**Confidence bands are retained for ranking within tiers.** Within silver or within gold, a ranking is still useful. But it is computed from the evidence conditions (how many are met, how strongly) rather than from a formula with arbitrary weights.

### 9.3 Contradiction classification

Before classifying two records as contradictory, the adjudication layer performs scope alignment:

1. **Check scope dimensions.** If two records have different material_form, temporal_scope, geographic_scope, or metric_basis, they are not contradictory. They are measuring different things.
2. **Check unit compatibility.** If two records have different units, apply conversion factors (if verified) and recompare.
3. **Check source precedence.** If one record is from a primary source and the other from a secondary compilation, the primary source is preferred (but both are retained).

Only after scope alignment confirms that two records are genuinely about the same thing with the same scope do they enter the contradiction resolution protocol (append-only, CONTRADICTS link, human review flag, as defined in v0.2).

### 9.4 Record admissibility policy

This is the formal policy that governs what enters analytical tables and what is exposed to downstream consumers. Separate from plausibility or confidence.

| Record class | Admissibility rule |
|---|---|
| Production volumes | Gold tier. All scope dimensions required. Government or academic source preferred. |
| Trade flows | Gold tier. At least partial scope. Government or trade statistics source. |
| Prices | Silver acceptable for time-series views. Gold required for reference prices. |
| Reserves | Gold tier. Reserve classification must be specified. |
| Relationships (ownership, operations) | Silver acceptable for graph exploration. Gold required for definitive assertions. |
| Staged raw tables | Bronze. Always admissible as reference. |

---

## 10. Layer 6: Persistence and retrieval

### 10.1 Storage topology

```
/documents/                          # Document-nested storage (bronze + silver artefacts)
  DOC-2024-00042/
    raw/
      usgs_lithium_mcs_2024.pdf
    pages/
      page_001.png
      page_002.png
    entities/
      P01-E001/
        content.md
        metadata.json
        deterministic_annotations.json    # Layer 1 output
        tags.json                         # Layer 2 output
        relationships.json                # Layer 2 output
        evidence_packets/                 # All evidence packets for this entity
          STEP-00042-P01-TAG-001.json
          STEP-00042-P01-REL-001.json
      P01-E002/
        table.png
        table.csv
        metadata.json
        interpretation.json
        deterministic_annotations.json
    chunks/
      P01-E001-L0.json
      P01-E001-L1-C001.json
    manifest.json

/schemas/                            # Centralised output schema registry
/skills/                             # Centralised skill directory
  task/
  reference/
    taxonomy/
      canonical_ontology.md           # Layer A
      operational_mappings.json       # Layer B
      candidate_queue.json            # Layer C
  config/
  evolution/

Neo4j (local)                        # Silver and gold entities + relationships
PostgreSQL (local)                   # Analytical projections, staging, governance, logs
ChromaDB                            # Embeddings for retrieval
```

### 10.2 PostgreSQL schema (revised for v0.3)

**Analytical tables (gold tier by default, silver where policy allows):**
- `production_volumes`: country_code, mineral, year, volume, unit, material_form, metric_basis, geographic_scope, temporal_scope, reporting_basis, data_source_basis, tier, evidence_completeness_json, source_document_id, entity_id, created_at, updated_at
- `trade_flows`: exporter_code, importer_code, commodity, year, volume, value, currency, share_percent, scope dimensions, tier, evidence, source_document_id
- `prices`: mineral, date, price, currency, per_unit, price_type, extraction_method, scope dimensions, tier, source_document_id
- `reserves`: country_code, mineral, volume, unit, reserve_classification, scope dimensions, tier, source_document_id

**Staging tables:**
- `staged_tables`: staged_table_id, document_id, entity_id, page, caption, headers_json, rows_json, footnotes_json, csv_content, interpretation_status, staged_at (always bronze)

**Governance tables:**
- `taxonomy_evolution_queue`: proposal_id, proposed_by_service, concept_mention, context, proposed_mapping_json, frequency_count, impact_score, status (pending/approved/rejected/merged), reviewed_by, reviewed_at
- `conversion_factors`: factor_id, mineral, form_from, form_to, factor_value, source, verification_status (assumed/verified/disputed), verified_against, last_updated
- `conversion_factor_history`: history_id, factor_id, old_value, new_value, reason, changed_at
- `organisation_aliases`: alias_id, canonical_name, alias, source_document_id, confidence, added_at
- `document_sources`: source_id, name, type, publisher, url, publication_frequency, document_count, family_priors_json
- `ambiguity_log`: ambiguity_id, requesting_service, ambiguity_type, severity, resolution_status, resolution_method, resolved_at

**System tables:**
- `documents`: document_id, raw_store_path, title, source_organisation, publication_date, source_type, source_registry_id, page_count, processing_status
- `processing_manifests`: manifest_id, document_id, pipeline_version, status, pages_json, model_versions_json, created_at, updated_at
- `pipeline_logs`: log_id, timestamp, document_id, page, layer, service, action, input_ref, model_used, duration_ms, tokens_json, status, output_summary
- `contradiction_log`: contradiction_id, record_a_id, record_b_id, scope_alignment_result, conflict_type, resolution_status, resolved_by, resolved_at, notes
- `record_history`: history_id, table_name, record_id, field_name, old_value, new_value, change_reason, changed_at, source_document_id
- `supersession_log`: supersession_id, record_id, table_name, previous_version_json, new_version_json, changed_fields, reason, affected_descendants, superseded_at
- `tier_transitions`: transition_id, record_id, from_tier, to_tier, reason, conditions_met_json, conditions_unmet_json, transitioned_at, transitioned_by

### 10.3 Neo4j schema

**Node labels:** Country, Mineral, Organisation, Facility, Product, Policy, Technology, Document, Entity, Chunk

All nodes carry a `tier` property (bronze/silver/gold) and a `lineage` property (JSON string with dependency chain).

**Relationship types:** All from v0.2 plus scope dimension properties on every data-bearing relationship.

### 10.4 Write logic

**Bronze writes:** Automatic, no conditions. Raw extraction results go to filesystem and staged_tables.

**Silver writes:** Automatic after Layer 2 processing. Written to Neo4j and PostgreSQL with tier=silver. ChromaDB vectors upserted.

**Gold writes (promotions):** Only when Layer 5 adjudication confirms all admissibility conditions are met. Updates the tier field on existing silver records. Logs the transition in tier_transitions.

**Gold demotions:** When triggered by contradiction, taxonomy change, or conversion factor revision. Updates tier from gold to silver. Logs the transition. Flags for re-adjudication.

**Merge-vs-append:** As defined in v0.2 but now tier-aware. A new silver record never overwrites an existing gold record. A new gold-eligible record can supersede an existing gold record only if it has equal or better evidence completeness and scope alignment confirms they measure the same thing.

---

## 11. Skills inventory (v0.3)

### Task skills (Layer 1)

| Skill | Purpose |
|---|---|
| `page_preparation.skill.md` | PDF slicing, image conversion, base64 encoding |
| `document_intake.skill.md` | Metadata extraction, progressive scanning, field classification |
| `document_source_registry.skill.md` | Source matching, clustering, family prior management |
| `structural_extraction.skill.md` | DeepSeek OCR configuration, entity type definitions |
| `cross_page_entity.skill.md` | Cross-page entity detection and merging |
| `deterministic_normalisation.skill.md` | Country/mineral/unit/temporal/numeric parsing, alias lookup |
| `text_chunking.skill.md` | Hierarchical chunking, sizing, overlap, boundary rules |
| `adjacent_chunk_chaining.skill.md` | Rules for chaining adjacent chunks for expanded context |

### Task skills (Layer 2)

| Skill | Purpose |
|---|---|
| `table_interpretation.skill.md` | Column mapping, value normalisation, ambiguity handling |
| `table_structure_handling.skill.md` | Merged cells, multi-level headers, footnotes |
| `table_numeric_parsing.skill.md` | Number parsing, qualifiers, locale handling |
| `vision_interpretation.skill.md` | Chart recognition, data extraction, extraction method annotation |
| `taxonomy_tagging.skill.md` | LLM-native tagging with constrained execution framework |
| `taxonomy_support.skill.md` | Inter-service support protocol |
| `relationship_extraction_text.skill.md` | Relationship extraction from narrative text |
| `relationship_extraction_table.skill.md` | Relationship extraction from table rows |
| `relationship_extraction_chart.skill.md` | Relationship extraction from chart data |
| `summarisation.skill.md` | Summary generation rules and quality criteria |
| `embedding.skill.md` | Embedding model config, ChromaDB management |

### Task skills (Layer 3)

| Skill | Purpose |
|---|---|
| `ambiguity_resolution.skill.md` | Typed ambiguity handling, resolution ladder, escalation rules |
| `ambiguity_classification.skill.md` | Blocking vs non-blocking classification criteria |

### Task skills (Layer 4)

| Skill | Purpose |
|---|---|
| `taxonomy_governance.skill.md` | Proposal clustering, scoring, duplicate detection, review packages |
| `reprocessing_triggers.skill.md` | Impact analysis, targeted re-processing scope definitions |

### Task skills (Layer 5)

| Skill | Purpose |
|---|---|
| `evidence_completeness.skill.md` | Evidence condition definitions, gold admissibility checklist |
| `contradiction_classification.skill.md` | Scope alignment logic, contradiction vs scope mismatch |
| `admissibility_policy.skill.md` | Per-record-class admissibility rules |
| `tier_management.skill.md` | Promotion, demotion, supersession rules |

### Task skills (Layer 6)

| Skill | Purpose |
|---|---|
| `database_writing.skill.md` | Cypher/SQL templates, merge keys, tier-aware write logic |
| `table_staging.skill.md` | Raw table staging for PostgreSQL |
| `lineage_management.skill.md` | Dependency tracking, invalidation queries |

### Orchestration skills

| Skill | Purpose |
|---|---|
| `pipeline_orchestration.skill.md` | State machine, page-level flow, pause/resume, retry |
| `logging.skill.md` | Structured log format, evidence packet storage |

### Reference skills

| Skill | Purpose |
|---|---|
| `taxonomy_reference.skill.md` | Access to the three-layer taxonomy |

### Configuration skills

| Skill | Purpose |
|---|---|
| `model_routing.skill.md` | Model selection per task, fallback rules |
| `system_parameters.skill.md` | Chunk sizes, thresholds, DB connections, file paths |

**Total: 32 skill documents** across six layers plus orchestration, reference, and configuration.

---

## 12. Pipeline orchestration (revised for v0.3)

### 12.1 Per-page processing flow

```
For each page in document:

  Layer 1:
    1. Structural extraction (DeepSeek OCR) → bronze entities
    2. Deterministic normalisation pass → annotated bronze entities
    3. Text chunking (if text blocks present) → bronze chunks

  Layer 2 (parallel where possible):
    4a. Table interpretation → silver table interpretations
        → may invoke Layer 3 for blocking ambiguities
        → may invoke taxonomy support mode
    4b. Vision interpretation → silver chart interpretations
        → may invoke Layer 3 for blocking ambiguities
    4c. (Text chunks pass through directly to tagging)

    5. Taxonomy tagging (all entities) → silver tagged entities
        → Step 1: receive deterministic annotations
        → Step 2: LLM primary tagging
        → Step 3: deterministic validation (Pydantic, enums, constraints)
        → Step 4: semantic verification (if needed)
        → Step 5: output decision (accept/flag/escalate)
    
    6. Relationship extraction (all tagged entities) → silver relationships with scope dimensions
    7. Summarisation and embedding → summaries + vectors

  Layer 5:
    8. Evidence completeness assessment
    9. Contradiction detection (with scope alignment)
    10. Tier assignment (silver by default; gold if all conditions met)

  Layer 6:
    11. Write to Neo4j, PostgreSQL, ChromaDB (tier-aware)
    12. Stage raw tables (bronze)
    13. Store evidence packets

  Orchestrator:
    14. Update manifest (page complete/failed/partial)
    15. Log all actions
```

### 12.2 Post-document pass

After all pages complete:
- Cross-page entity merge resolution
- Document-level contradiction check across all extracted relationships
- Document-level evidence completeness review
- Non-blocking ambiguity review (Layer 3 async queue)
- Final manifest update

### 12.3 Pause, resume, and failure handling

As defined in v0.2 but now with lineage-aware checkpointing. The resume checkpoint includes the taxonomy version and all skill/model versions so that version mismatches can be detected.

---

## 13. Confirmed design decisions (v0.3)

1. Architecture uses six functional layers, not flat numbered agents.
2. "Deterministic where possible, LLM where necessary, governed where consequential" is the core design principle.
3. Bronze/silver/gold is an epistemic contract governing the entire system, not just a storage label.
4. Every extracted fact carries six explicit scope dimensions.
5. Every downstream record carries machine-actionable dependency lineage.
6. Every processing step produces an evidence packet.
7. Taxonomy is split into three layers: canonical ontology, operational mapping registry, candidate extensions.
8. Taxonomy tagging is LLM-native with a constrained semantic execution framework (structured prompts, ontology slices, deterministic validation, explicit uncertainty).
9. Taxonomy evolution is governed by an offline governance service, not a runtime agent.
10. Ambiguity resolution is a typed broker service: blocking ambiguities resolved synchronously, non-blocking asynchronously.
11. Contradiction detection uses scope alignment before classification.
12. Gold promotion is a governance act based on evidence completeness, not a confidence threshold.
13. Gold can be demoted back to silver.
14. Conversion factors with assumed verification status are forbidden from gold promotion.
15. Summaries are downstream conveniences, not epistemic anchors.
16. Document family priors are first-class and inform source-specific interpretation conventions.
17. Record admissibility is separated from plausibility.
18. Semantic supersession with diff logging replaces silent overwrites.
19. Entities are stored nested under documents with metadata linking back to source.
20. Tables are staged as-is in PostgreSQL (bronze) before interpretation.

---

## 14. Remaining design work

1. **Detailed taxonomy document:** Draft the full canonical ontology (Layer A) with complete controlled vocabularies, relationship attribute schemas, and scope dimension enums.
2. **Formal output schemas:** JSON Schema or Pydantic models for all inter-layer data formats (15+ schemas).
3. **First skill documents:** Prioritise `taxonomy_reference.skill.md`, `taxonomy_tagging.skill.md`, `deterministic_normalisation.skill.md`, `ambiguity_resolution.skill.md`.
4. **Infrastructure setup:** Neo4j, PostgreSQL (full schema from Section 10.2), ChromaDB, Ollama with Qwen 3.5 models.
5. **Evaluation harness:** 3-5 diverse documents with manual annotations. This is a gating item, not a nice-to-have.
6. **Re-processing logic:** Detailed design for targeted re-processing based on lineage invalidation.
7. **Human review interface:** Queue-based workflow for contradiction resolution, taxonomy proposal review, and ambiguity escalation.
8. **Performance monitoring:** Logging analysis for model call frequency, token usage, and processing time per layer to identify optimisation opportunities.

---

## 15. Next steps (build order)

1. Set up local infrastructure (Neo4j, PostgreSQL, ChromaDB, Ollama).
2. Build Layer 1 components: page preparation, structural extraction (DeepSeek OCR integration), deterministic normalisation pass, text chunking. These have minimal LLM dependency and establish the bronze pipeline.
3. Draft the canonical ontology document and operational mapping tables.
4. Build the taxonomy tagging service (Layer 2) with its constrained execution framework. This is the most critical semantic component.
5. Build the relationship extraction service (Layer 2).
6. Build the ambiguity resolution service (Layer 3).
7. Build the evidence completeness and contradiction detection components (Layer 5).
8. Build the persistence layer (Layer 6) with tier-aware write logic.
9. Integrate and test against manually annotated documents.
10. Build the taxonomy governance service (Layer 4) once enough documents have been processed to generate meaningful candidate proposals.
