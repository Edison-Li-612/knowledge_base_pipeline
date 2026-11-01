# Pipeline System Relationship Schemas

## Version 0.1.0

This document defines the system-level relationships used internally by the pipeline infrastructure. These are **not domain ontology** — they are not extracted from documents and are not written by Layer 2 services. They are created by the pipeline itself during adjudication and persistence.

These schemas are contracts between layers. Any change here must be coordinated across the Layer 5 and Layer 6 implementations.

---

## CONTRADICTS

Links two silver or gold records that contain conflicting information about the same real-world fact. Created by Layer 5 (Adjudication and Trust Management) during contradiction detection.

### Important distinction

**CONTRADICTS ≠ scope mismatch.** Two records with different scope dimensions (e.g., one is calendar_year production, one is fiscal_year) are not contradictory — they describe different things. Layer 5 must check scope alignment before classifying a pair as CONTRADICTS. Only records with matching scope dimensions on the conflicting field should be linked by CONTRADICTS.

### Schema

| Field | Type | Required | Controlled vocabulary | Notes |
|---|---|---|---|---|
| `record_id_a` | string | Yes | — | ID of the first conflicting record |
| `record_id_b` | string | Yes | — | ID of the second conflicting record |
| `conflict_type` | string | Yes | `value_mismatch`, `unit_mismatch`, `temporal_mismatch`, `scope_mismatch`, `attribution_mismatch`, `form_mismatch` | |
| `conflicting_field` | string | Yes | — | The specific field(s) in conflict (e.g., `volume`, `year`) |
| `value_a` | string | Yes | — | The conflicting value from record A exactly as extracted |
| `value_b` | string | Yes | — | The conflicting value from record B exactly as extracted |
| `scope_checked` | boolean | Yes | — | Whether scope dimensions were verified before flagging as CONTRADICTS; always `true` at write time |
| `resolution_status` | string | Yes | `unresolved`, `resolved_a_preferred`, `resolved_b_preferred`, `resolved_both_valid`, `resolved_different_scope` | Set to `unresolved` at creation; updated by Layer 5 or human review |
| `resolution_notes` | string | Yes | — | Layer 5 explanation or human note; set to `"pending_review"` if unresolved at creation |
| `resolved_by` | string | Yes | `layer5_automatic`, `human_review`, `pending` | Set to `pending` at creation; updated when resolved |
| `resolved_at` | string | Yes | ISO 8601 or `null` | Set to `null` at creation; populated when resolved |
| `created_at` | string | Yes | ISO 8601 | When this contradiction was detected |

### Storage

- **PostgreSQL**: `contradiction_log` table.
- **Neo4j**: CONTRADICTS edge between the two record nodes (for graph traversal queries).

### Lifecycle

1. Layer 5 detects two silver/gold records with overlapping scope and different values.
2. Layer 5 checks scope dimensions — if scopes differ, reclassify as `resolved_different_scope` immediately.
3. If a genuine conflict, write CONTRADICTS record with `resolution_status: unresolved`.
4. Layer 5 attempts automatic resolution (applies source reliability weights, checks for newer/superseding source).
5. If resolved automatically, update `resolution_status` and `resolved_by: layer5_automatic`.
6. If unresolvable, route to human review queue. Human updates `resolution_status` and `resolution_notes`.
7. Neither record is promoted to gold until the contradiction is resolved.

---

## EXTRACTED_FROM

Links any extracted data record (silver or gold) back to its source document entity — the specific page entity from which the data was extracted. Created by Layer 6 (Persistence) at write time. Never extracted from documents.

### Purpose

EXTRACTED_FROM is the primary provenance link. It is the lowest-level lineage record: "this data point came from this specific page entity in this document." It complements the dependency lineage block (which records the *processing* provenance — which taxonomy version, which model, etc.) by recording the *document* provenance.

### Schema

| Field | Type | Required | Notes |
|---|---|---|---|
| `source_record_id` | string | Yes | The extracted data record (relationship, tag, or data point) |
| `document_id` | string | Yes | The document this was extracted from |
| `entity_id` | string | Yes | The specific entity (table, chart, text block) within the page; always known from Layer 1 bronze artefacts |
| `chunk_id` | string | Yes | The text chunk within the entity; set to the entity_id itself for non-text entities (tables, charts) |
| `page_number` | integer | Yes | Page number within the document; always known from bronze artefacts |
| `extraction_type` | string | Yes | `direct` — value explicitly stated in source; `inferred` — derived from context or calculation |
| `extraction_method` | string | Yes | `text_extraction`, `table_extraction`, `chart_extraction`, `image_extraction` — which Layer 2 service extracted this |
| `epistemic_tier_at_extraction` | string | Yes | `bronze` or `silver` — the tier at which the source entity existed when this link was created |
| `created_at` | string | Yes | ISO 8601 timestamp |

### Storage

- **Neo4j**: EXTRACTED_FROM edge between the data record node and the document/entity node.
- **PostgreSQL**: `pipeline_logs` table includes extraction provenance for all writes.

### Relationship to dependency lineage

EXTRACTED_FROM records *document provenance* (where did the raw data come from?). The dependency lineage block on each silver/gold record records *processing provenance* (which taxonomy version, model version, skill version, and conversion factors were used to produce the interpretation?). Both are needed for full auditability.

---

## SUPERSEDES

Created by Layer 6 when a silver or gold record is updated with a newer, more authoritative value. Distinct from CONTRADICTS — supersession implies the old value is replaced; contradiction implies ambiguity about which value is correct.

### Schema

| Field | Type | Required | Notes |
|---|---|---|---|
| `supersession_id` | string | Yes | Unique ID for this supersession event |
| `old_record_id` | string | Yes | The record being replaced |
| `new_record_id` | string | Yes | The record doing the replacing |
| `changed_fields` | array | Yes | Which fields changed (e.g., `["volume", "year"]`) |
| `reason` | string | Yes | Why the old record was superseded (e.g., "Updated figure from newer USGS MCS edition") |
| `affected_descendants` | array | Yes | IDs of derived records that depend on the old value; set to `[]` if none exist |
| `superseded_at` | string | Yes | ISO 8601 timestamp |

### Storage

- **PostgreSQL**: `tier_transitions` table (also used for bronze → silver → gold promotions).
- **Neo4j**: SUPERSEDES edge between old and new record nodes (retained for audit; old node marked `status: superseded`).
