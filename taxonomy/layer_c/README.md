# Layer C: Candidate Extensions

## Purpose

Layer C is the proposal queue for the taxonomy. It holds concepts, relationships, and mappings that have been encountered during processing but have not yet been reviewed and accepted into Layer A (canonical ontology) or Layer B (operational mapping registry).

Layer C entries are **proposals only**. They have no authority over gold-tier records. They may influence silver-tier records only when the pipeline is explicitly configured to allow candidate-tier mappings, and any such record is flagged with `candidate_dependency: true`.

---

## Governance rules

1. **Any pipeline service (Layer 2, 3) may emit a proposal.** Proposals are written here as structured YAML or Markdown entries.
2. **Proposals are never edited in place.** They are either promoted, rejected, or merged — never silently updated.
3. **Layer 4 (Taxonomy Governance Service)** owns the review cycle. It clusters proposals by frequency and semantic similarity, scores them by impact, and produces review packages for human approval.
4. **After human approval**, an accepted proposal is:
   - Promoted to `layer_a/` (if it is a structural definition: new entity type, relationship type, or controlled vocabulary entry)
   - Promoted to `layer_b/` (if it is an operational mapping: alias, abbreviation, conversion factor, source convention)
   - Merged (mapped to an existing concept; alias added to `layer_b/`)
   - Rejected (marked as noise, retained here for audit)
5. **After promotion**, Layer 4 triggers targeted re-processing of affected silver/gold records.

---

## Proposal format

Each proposal is a separate YAML file named `proposal_{YYYYMMDD}_{type}_{slug}.yaml`.

```yaml
proposal_id: PROP-2026-00001
type: new_entity_type          # new_entity_type | new_relationship | new_vocab_entry | new_alias | new_conversion_factor
proposed_concept: "battery_recycler"
description: "An organisation whose primary activity is recycling end-of-life batteries"
parent_type: "organisation"    # if a subtype proposal
encountered_in:
  - document_id: DOC-2026-00001
    page: 14
    context: "companies such as Li-Cycle and Redwood Materials, specialist battery recyclers"
frequency: 1
proposed_by: "layer2_taxonomy_tagging"
proposed_at: "2026-04-15T10:22:00Z"
status: pending                # pending | approved | rejected | merged
review_notes: ""
```

---

## Current proposals

*(Empty at initialisation. Populated at runtime.)*
