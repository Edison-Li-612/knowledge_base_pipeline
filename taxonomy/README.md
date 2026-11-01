# Critical Mineral Supply Chain Taxonomy

## Version 0.2.0

**Purpose:** The central domain taxonomy for the Critical Mineral Supply Chain Knowledge Pipeline. Defines the controlled vocabularies, entity types, relationship types, unit systems, scope dimensions, and reference data that govern how every layer of the pipeline interprets, tags, and structures extracted information.

**Design reference:** `critical_mineral_pipeline_design_v0.3.md`, Sections 3–4.

**Governance:** This taxonomy is a living document organised into three layers with distinct governance, versioning, and access patterns. All changes are version-controlled and logged in [version_log.md](version_log.md).

---

## Three-layer architecture

```
taxonomy/
├── layer_a/          ← Canonical ontology (stable, versioned, human-approved)
├── layer_b/          ← Operational mapping registry (dynamic, human-reviewable)
├── layer_c/          ← Candidate extensions (proposed by pipeline, queued for review)
└── pipeline_schemas/ ← System relationship schemas (CONTRADICTS, EXTRACTED_FROM, evidence packets)
```

### Layer A — Canonical ontology

Contains the settled, structural definitions of the domain. Changes are infrequent and require explicit human approval. All content here is version-controlled with semantic versioning (major.minor.patch).

| File | Description |
|---|---|
| [layer_a/mineral_hierarchy.md](layer_a/mineral_hierarchy.md) | Mineral and material hierarchy: groups, species, forms, chemical formulas, CAS numbers |
| [layer_a/relationships.md](layer_a/relationships.md) | Domain relationship type definitions with subject/object constraints, attribute schemas, and scope dimensions |
| [layer_a/controlled_vocabularies.md](layer_a/controlled_vocabularies.md) | All controlled vocabularies: supply chain stages, source types, capacity types, price types, reserve classifications, etc. |
| [layer_a/units_and_metrics.md](layer_a/units_and_metrics.md) | Canonical units, metric types, normalisation rules, and parsing guidance |

### Layer B — Operational mapping registry

Contains practical mappings from raw document content to canonical ontology concepts. Machine-maintained with human-reviewable audit trail.

| File | Description |
|---|---|
| [layer_b/conversion_factors.md](layer_b/conversion_factors.md) | Form-to-form conversion factors with `factor_id`, version, source, and verification status |
| [layer_b/organisation_aliases.md](layer_b/organisation_aliases.md) | Organisation alias table (canonical name ↔ variants) |
| [layer_b/country_mappings.md](layer_b/country_mappings.md) | Country and region reference with ISO 3166-1 alpha-3 codes and name variants |
| [layer_b/document_family_priors.md](layer_b/document_family_priors.md) | Per-source-family structural conventions, reporting basis priors, and parsing templates |

### Layer C — Candidate extensions

Holds concepts, relationships, or mappings proposed by pipeline services that have not yet been reviewed. See [layer_c/README.md](layer_c/README.md) for governance rules and proposal format.

### Pipeline schemas

System-level relationship schemas used internally by the pipeline. These are **not domain ontology** — they are infrastructure contracts used by Layer 5 (Adjudication) and Layer 6 (Persistence).

| File | Description |
|---|---|
| [pipeline_schemas/system_relationships.md](pipeline_schemas/system_relationships.md) | CONTRADICTS and EXTRACTED_FROM schemas |

---

## Mineral scope (v0.2.0)

This taxonomy covers 10 mineral/material groups selected for relevance to energy transition, defence, and semiconductor supply chains:

1. Lithium
2. Cobalt
3. Nickel
4. Manganese
5. Graphite (natural and synthetic)
6. Silicon (metallurgical-grade and polysilicon)
7. Tellurium
8. Indium
9. Rare Earth Elements (17 species + yttrium)
10. Copper

Additional minerals (gallium, germanium, tungsten, vanadium, antimony, titanium, tin, etc.) are added through the Layer C → Layer A promotion cycle as documents referencing them are processed.

---

## How pipeline layers use this taxonomy

| Layer | Usage |
|---|---|
| **Layer 1** (Deterministic Extraction) | Unit parsing and alias lookup from Layer B (conversion factors, organisation aliases, country mappings). No semantic interpretation. |
| **Layer 2** (Bounded Interpretation) | Full Layer A access for taxonomy tagging, relationship extraction, and table semantic mapping. Receives ontology slices (not the full taxonomy) per LLM call. Emits Layer C proposals for unrecognised concepts. |
| **Layer 3** (Ambiguity Resolution) | Reads Layer A relationship constraints and scope dimension definitions to check whether apparent contradictions are actually scope mismatches. May query Layer B document family priors for source-level disambiguation. |
| **Layer 4** (Taxonomy Governance) | Owns the Layer C queue. Clusters proposals, scores by frequency/impact, produces review packages. Promotes accepted proposals to Layer A or B and triggers targeted re-processing. |
| **Layer 5** (Adjudication) | Uses scope dimensions (Layer A) and conversion factor verification status (Layer B) to evaluate gold promotion criteria. Writes CONTRADICTS records per `pipeline_schemas/system_relationships.md`. |
| **Layer 6** (Persistence) | Uses canonical names (Layer A) as merge keys for deduplication. Writes EXTRACTED_FROM provenance links per `pipeline_schemas/system_relationships.md`. |

---

## Conventions

- **Canonical names** are `lowercase_snake_case` (e.g., `lithium_carbonate`, `mining_extraction`).
- **Display names** are Title Case (e.g., "Lithium Carbonate", "Mining / Extraction").
- **Chemical formulas** use standard notation (e.g., Li2CO3, LiOH-H2O).
- **ISO codes** are used for countries (ISO 3166-1 alpha-3) and currencies (ISO 4217).
- **Confidence values** range from 0.00 to 1.00.
- Tables marked `[extensible]` are expected to grow via the Layer C proposal cycle.
- Entries marked `[assumed]` are derived from LLM pre-trained knowledge and await verification against published references. Assumed conversion factors cannot produce gold-tier derived values.
