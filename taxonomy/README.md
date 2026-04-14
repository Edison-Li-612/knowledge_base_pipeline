# Critical Mineral Supply Chain Taxonomy

## Version 0.1.0 (Seed)

**Purpose:** This is the central domain taxonomy for the Critical Mineral Supply Chain Knowledge Pipeline. It defines the controlled vocabularies, entity types, relationship types, unit systems, and reference data that govern how every agent in the pipeline interprets, tags, and structures extracted information.

**Governance:** This taxonomy is a living document. It evolves through the taxonomy evolution mechanism defined in the pipeline design document (Section 2.2). All changes are version-controlled and logged in [version_log.md](version_log.md).

---

## File index

| File | Description |
|---|---|
| [minerals/hierarchy.md](minerals/hierarchy.md) | Mineral and material hierarchy: groups, species, forms, chemical formulas, CAS numbers |
| [minerals/conversion_factors.md](minerals/conversion_factors.md) | Unit and form conversion factors with source and confidence tracking |
| [entities/organisations.md](entities/organisations.md) | Organisation alias table (~50 seed entries, with India/UK focus) |
| [entities/countries_regions.md](entities/countries_regions.md) | Country and region reference with ISO 3166-1 alpha-3 codes |
| [relationships.md](relationships.md) | Relationship type definitions with subject/object constraints and attribute schemas |
| [controlled_vocabularies.md](controlled_vocabularies.md) | All controlled vocabularies: supply chain stages, source types, capacity types, price types, reserve classifications, extraction types, etc. |
| [units_and_metrics.md](units_and_metrics.md) | Canonical units, metric types, normalisation rules, and parsing guidance |
| [version_log.md](version_log.md) | Taxonomy version history and changelog |

---

## Mineral scope (v0.1.0)

This seed covers 10 mineral/material groups selected for relevance to energy transition, defence, and semiconductor supply chains:

1. Lithium
2. Cobalt
3. Nickel
4. Manganese
5. Graphite (natural and synthetic)
6. Silicon (metallurgical-grade and polysilicon)
7. Tellurium
8. Indium
9. Rare Earth Elements (17 species)
10. Copper

Additional minerals (e.g., gallium, germanium, tungsten, vanadium, antimony, titanium, tin) can be added through the taxonomy evolution mechanism as documents referencing them are processed.

---

## How agents use this taxonomy

| Agent | Usage |
|---|---|
| Agent 3b (Table Interpretation) | Looks up mineral forms, units, and conversion factors to interpret table columns. May invoke Agent 4 support mode for ambiguous terms. |
| Agent 3c (Vision Interpretation) | References mineral names and units when interpreting chart axes and labels. |
| Agent 4 (Taxonomy Tagging) | Tags entities against the full controlled vocabulary. Proposes additions for unrecognised concepts. |
| Agent 5 (Relationship Extraction) | Uses relationship type definitions and attribute schemas to structure extracted triples. |
| Agent 7 (Confidence/Validation) | Uses source type reliability weights, domain validation rules, and unit validity checks. |
| Agent 8 (Database Writer) | Uses merge keys and canonical names from this taxonomy to deduplicate records. |

---

## Conventions used in this taxonomy

- **Canonical names** are lowercase_snake_case (e.g., `lithium_carbonate`, `mining_extraction`).
- **Display names** are title case (e.g., "Lithium Carbonate", "Mining/Extraction").
- **Chemical formulas** use standard notation (e.g., Li2CO3, LiOH-H2O).
- **ISO codes** are used for countries (ISO 3166-1 alpha-3) and languages (ISO 639-1).
- **Confidence values** range from 0.00 to 1.00.
- Tables marked with `[extensible]` are expected to grow via the taxonomy evolution mechanism.
- Entries marked `[assumed]` are derived from LLM pre-trained knowledge and await verification against published references.
