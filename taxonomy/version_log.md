# Taxonomy Version Log

All changes to the taxonomy are recorded here. Each version increment follows semantic versioning:
- **Major** (X.0.0): Breaking structural changes (e.g., entity types renamed, relationship schemas restructured).
- **Minor** (0.X.0): New content added (new minerals, organisations, vocabularies) that is backward-compatible.
- **Patch** (0.0.X): Corrections to existing content (typo fixes, conversion factor updates, alias additions).

Timestamps use ISO 8601 with minute-level precision (UTC).

---

## v0.2.0 — 2026-04-14T10:30Z

**Type:** Minor release (backward-compatible additions and restructuring)

**Changes to `relationships.md`:**
- **Broadened subject/object types across all relationship definitions.** Previously, many relationships were too narrow (e.g., PRODUCES only accepted `country` or `facility` as subjects; now also accepts `organisation` and `region`). This accommodates the full range of statements found in real-world supply chain documents (e.g., "Albemarle produced 200kt LCE").
- **Added 4 new relationship types:**
  - `CONSUMES` — demand-side counterpart to PRODUCES (country/org/facility consumes a mineral or product)
  - `SUBSIDIARY_OF` — corporate hierarchy (org is a subsidiary of org)
  - `PARTNERS_WITH` — partnerships, JVs, strategic alliances, bilateral agreements
  - `USES_TECHNOLOGY` — facility/org/country uses a specific technology or process
- **Added `(primary)` markers** to indicate most common subject/object types while keeping others valid.
- **Added concrete example statements** for every relationship type to guide the extraction agent.
- **Added guidance sections:** "Choosing between overlapping relationship types", "Multi-relationship extraction from a single sentence", "Handling aggregate vs specific entities."
- **Enriched attributes** on several relationships: added `share_scope`, `supply_chain_stage` to PRODUCES; `status` to OPERATES and OWNS; `intensity_or_absolute` to EMITS; `form` to PRICES; `import_dependency_percent` to DEPENDS_ON; expanded controlled vocabulary options throughout.
- Total relationship types: 22 (up from 18).

---

## v0.1.0 — 2026-04-13T16:50Z (Seed)

**Type:** Initial release (seed taxonomy)

**Scope:**
- 10 mineral groups: lithium, cobalt, nickel, manganese, graphite, silicon, tellurium, indium, rare earth elements (17 species), copper
- ~60 organisation alias entries across diversified miners, lithium, cobalt, nickel, graphite, silicon, tellurium/indium, REE, battery materials, and India/UK sectors
- ~50 country entries with ISO alpha-3 codes and common aliases
- 12 region/country group definitions
- 18 relationship type definitions with full attribute schemas
- 11 supply chain stages
- 13 source types with reliability weights
- 7 capacity types, 8 price types, 6 reserve classifications
- Complete unit system with parsing rules
- ~40 conversion factors (stoichiometric and grade-dependent) with assumption logging
- Domain validation ranges for sanity checking
- 18 facility types, 20 technology/process types, 17 product/component types

**Known gaps to address in future versions:**
- Additional minerals: gallium, germanium, tungsten, vanadium, antimony, titanium, tin, zirconium, beryllium, tantalum, niobium, platinum group metals
- Organisation alias table is a starter set; will grow significantly as documents are processed
- Conversion factors marked `[assumed]` need verification against published references (USGS, BGS, academic sources)
- Country list may need expansion for smaller producing nations as they appear in documents
- India- and UK-specific facility data (mines, refineries, processing plants) not yet enumerated
