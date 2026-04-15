-- Critical Mineral Supply Chain Pipeline — PostgreSQL Schema
-- v0.3.0
-- Run against database: critical_minerals
-- Usage: psql -U postgres -d critical_minerals -f postgres_schema.sql

-- ============================================================
-- EXTENSIONS
-- ============================================================
CREATE EXTENSION IF NOT EXISTS "pgcrypto";  -- for gen_random_uuid()

-- ============================================================
-- ANALYTICAL TABLES (gold tier by default; silver where policy allows)
-- ============================================================

CREATE TABLE IF NOT EXISTS production_volumes (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    country_code    CHAR(3),                -- ISO 3166-1 alpha-3
    organisation    TEXT,                   -- canonical org name (if reported at org level)
    facility        TEXT,                   -- facility name (if reported at facility level)
    mineral         TEXT NOT NULL,          -- taxonomy canonical name
    year            SMALLINT,
    volume          NUMERIC,
    unit            TEXT,                   -- tonnes, kt, Mt, etc.
    -- Scope dimensions (v0.3)
    material_form       TEXT,               -- contained_metal, LCE, spodumene_concentrate, etc.
    metric_basis        TEXT,               -- production_volume, refining_output, capacity_nameplate, etc.
    geographic_scope    TEXT,               -- country_level, facility_level, regional, global
    temporal_scope      TEXT,               -- calendar_year_2023, Q1_2024, etc.
    reporting_basis     TEXT,               -- company_estimate, national_statistics, etc.
    data_source_basis   TEXT,               -- primary_source, secondary_compilation, etc.
    -- Epistemic
    tier                TEXT NOT NULL DEFAULT 'silver' CHECK (tier IN ('bronze','silver','gold')),
    evidence_completeness_json  JSONB,
    -- Provenance
    source_document_id  TEXT,
    entity_id           TEXT,
    lineage_json        JSONB,
    -- Audit
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS trade_flows (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    exporter_code   CHAR(3),
    importer_code   CHAR(3),
    exporter_org    TEXT,
    importer_org    TEXT,
    commodity       TEXT NOT NULL,
    material_form   TEXT,
    year            SMALLINT,
    volume          NUMERIC,
    unit            TEXT,
    value           NUMERIC,
    currency        CHAR(3),
    share_percent   NUMERIC,
    -- Scope dimensions
    geographic_scope    TEXT,
    temporal_scope      TEXT,
    reporting_basis     TEXT,
    data_source_basis   TEXT,
    -- Epistemic
    tier                TEXT NOT NULL DEFAULT 'silver' CHECK (tier IN ('bronze','silver','gold')),
    evidence_completeness_json  JSONB,
    -- Provenance
    source_document_id  TEXT,
    entity_id           TEXT,
    lineage_json        JSONB,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS prices (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    mineral         TEXT,
    product         TEXT,
    date            DATE,
    year            SMALLINT,
    quarter         SMALLINT,
    price           NUMERIC,
    currency        CHAR(3),
    per_unit        TEXT,
    material_form   TEXT,
    price_type      TEXT,               -- spot, contract, average_annual, assessed, etc.
    exchange        TEXT,               -- LME, CME, SHFE, etc.
    source_assessment TEXT,
    -- Scope dimensions
    temporal_scope      TEXT,
    reporting_basis     TEXT,
    data_source_basis   TEXT,
    -- Epistemic
    tier                TEXT NOT NULL DEFAULT 'silver' CHECK (tier IN ('bronze','silver','gold')),
    evidence_completeness_json  JSONB,
    source_document_id  TEXT,
    entity_id           TEXT,
    lineage_json        JSONB,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS reserves (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    country_code            CHAR(3),
    organisation            TEXT,
    facility                TEXT,
    mineral                 TEXT NOT NULL,
    volume                  NUMERIC,
    unit                    TEXT,
    material_form           TEXT,
    reserve_classification  TEXT,       -- measured, indicated, inferred, proved, probable, unspecified
    resource_or_reserve     TEXT,       -- resource or reserve
    ore_grade               NUMERIC,
    ore_grade_unit          TEXT,
    reporting_standard      TEXT,       -- jorc, ni_43_101, samrec, etc.
    year                    SMALLINT,
    -- Scope dimensions
    geographic_scope        TEXT,
    temporal_scope          TEXT,
    reporting_basis         TEXT,
    data_source_basis       TEXT,
    -- Epistemic
    tier                    TEXT NOT NULL DEFAULT 'silver' CHECK (tier IN ('bronze','silver','gold')),
    evidence_completeness_json  JSONB,
    source_document_id      TEXT,
    entity_id               TEXT,
    lineage_json            JSONB,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================
-- STAGING TABLE (always bronze — faithful raw reproduction)
-- ============================================================

CREATE TABLE IF NOT EXISTS staged_tables (
    staged_table_id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id             TEXT NOT NULL,
    entity_id               TEXT NOT NULL,
    page                    SMALLINT,
    caption                 TEXT,
    headers_json            JSONB,
    rows_json               JSONB,
    footnotes_json          JSONB,
    csv_content             TEXT,
    interpretation_status   TEXT NOT NULL DEFAULT 'pending'
                                CHECK (interpretation_status IN ('pending','interpreted','failed')),
    staged_at               TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================
-- GOVERNANCE TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS taxonomy_evolution_queue (
    proposal_id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    proposed_by_service TEXT NOT NULL,
    concept_mention     TEXT NOT NULL,
    context_json        JSONB,
    proposed_mapping_json JSONB,
    frequency_count     INTEGER NOT NULL DEFAULT 1,
    impact_score        NUMERIC,
    status              TEXT NOT NULL DEFAULT 'pending'
                            CHECK (status IN ('pending','approved','rejected','merged')),
    reviewed_by         TEXT,
    reviewed_at         TIMESTAMPTZ,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS conversion_factors (
    factor_id           TEXT PRIMARY KEY,   -- e.g. CF-Li-spod6-metal
    mineral             TEXT NOT NULL,
    form_from           TEXT NOT NULL,
    form_to             TEXT NOT NULL,
    factor_value        NUMERIC NOT NULL,
    derivation          TEXT,
    source              TEXT,
    verification_status TEXT NOT NULL DEFAULT 'assumed'
                            CHECK (verification_status IN ('assumed','verified','disputed')),
    verified_against    TEXT,
    last_updated        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS conversion_factor_history (
    history_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    factor_id       TEXT NOT NULL REFERENCES conversion_factors(factor_id),
    old_value       NUMERIC,
    new_value       NUMERIC,
    reason          TEXT,
    changed_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS organisation_aliases (
    alias_id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    canonical_name      TEXT NOT NULL,
    alias               TEXT NOT NULL,
    source_document_id  TEXT,
    confidence          NUMERIC,
    added_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (canonical_name, alias)
);

CREATE TABLE IF NOT EXISTS document_sources (
    source_id               TEXT PRIMARY KEY,   -- e.g. SRC-0001
    name                    TEXT NOT NULL,
    type                    TEXT,               -- government_report, academic_paper, etc.
    publisher               TEXT,
    url                     TEXT,
    publication_frequency   TEXT,               -- annual, quarterly, one-off, irregular
    document_count          INTEGER NOT NULL DEFAULT 0,
    family_priors_json      JSONB,              -- reporting conventions for this source family
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ambiguity_log (
    ambiguity_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    requesting_service  TEXT NOT NULL,
    ambiguity_type      TEXT NOT NULL,
    severity            TEXT NOT NULL CHECK (severity IN ('blocking','non_blocking')),
    unresolved_item     TEXT,
    context_json        JSONB,
    candidate_interpretations_json JSONB,
    resolution_status   TEXT NOT NULL DEFAULT 'unresolved'
                            CHECK (resolution_status IN ('unresolved','resolved','escalated')),
    resolution_method   TEXT,
    resolution_json     JSONB,
    resolved_at         TIMESTAMPTZ,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================
-- SYSTEM TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS documents (
    document_id             TEXT PRIMARY KEY,
    raw_store_path          TEXT,
    title                   TEXT,
    source_organisation     TEXT,
    publication_date        DATE,
    publication_year        SMALLINT,
    source_type             TEXT,
    source_registry_id      TEXT REFERENCES document_sources(source_id),
    page_count              SMALLINT,
    language                CHAR(2),
    authors                 TEXT,
    doi_or_isbn             TEXT,
    edition_or_version      TEXT,
    abstract_or_summary     TEXT,
    processing_status       TEXT NOT NULL DEFAULT 'pending'
                                CHECK (processing_status IN
                                    ('pending','in_progress','completed','failed','partial')),
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS processing_manifests (
    manifest_id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id         TEXT NOT NULL REFERENCES documents(document_id),
    pipeline_version    TEXT NOT NULL,
    taxonomy_version    TEXT,
    status              TEXT NOT NULL DEFAULT 'pending'
                            CHECK (status IN ('pending','in_progress','completed','failed','paused')),
    pages_json          JSONB,          -- per-page status tracking
    model_versions_json JSONB,
    resume_checkpoint   JSONB,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS pipeline_logs (
    log_id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    document_id     TEXT,
    page            SMALLINT,
    layer           SMALLINT,
    service         TEXT,
    action          TEXT,
    input_ref       TEXT,
    model_used      TEXT,
    duration_ms     INTEGER,
    tokens_json     JSONB,              -- {input: N, output: N}
    status          TEXT NOT NULL CHECK (status IN ('success','failure','warning')),
    output_summary  TEXT,
    error_detail    TEXT
);

CREATE TABLE IF NOT EXISTS contradiction_log (
    contradiction_id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    record_a_id                 TEXT NOT NULL,
    record_a_table              TEXT NOT NULL,
    record_b_id                 TEXT NOT NULL,
    record_b_table              TEXT NOT NULL,
    scope_alignment_result      TEXT,   -- aligned or scope_mismatch_on_[dimension]
    conflict_type               TEXT,
    resolution_status           TEXT NOT NULL DEFAULT 'unresolved'
                                    CHECK (resolution_status IN
                                        ('unresolved','resolved_a_preferred','resolved_b_preferred',
                                         'resolved_both_valid','resolved_different_scope')),
    resolved_by                 TEXT,
    resolved_at                 TIMESTAMPTZ,
    notes                       TEXT,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS record_history (
    history_id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    table_name          TEXT NOT NULL,
    record_id           TEXT NOT NULL,
    field_name          TEXT NOT NULL,
    old_value           TEXT,
    new_value           TEXT,
    change_reason       TEXT,
    changed_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source_document_id  TEXT
);

CREATE TABLE IF NOT EXISTS supersession_log (
    supersession_id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    record_id               TEXT NOT NULL,
    table_name              TEXT NOT NULL,
    previous_version_json   JSONB,
    new_version_json        JSONB,
    changed_fields          TEXT[],
    reason                  TEXT,
    affected_descendants    TEXT[],
    superseded_at           TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tier_transitions (
    transition_id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    record_id               TEXT NOT NULL,
    table_name              TEXT NOT NULL,
    from_tier               TEXT NOT NULL CHECK (from_tier IN ('bronze','silver','gold')),
    to_tier                 TEXT NOT NULL CHECK (to_tier IN ('bronze','silver','gold')),
    reason                  TEXT,
    conditions_met_json     JSONB,
    conditions_unmet_json   JSONB,
    transitioned_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    transitioned_by         TEXT        -- 'system' or human reviewer name
);

-- ============================================================
-- INDEXES (performance)
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_production_volumes_mineral_year
    ON production_volumes (mineral, year);
CREATE INDEX IF NOT EXISTS idx_production_volumes_country
    ON production_volumes (country_code);
CREATE INDEX IF NOT EXISTS idx_production_volumes_tier
    ON production_volumes (tier);
CREATE INDEX IF NOT EXISTS idx_production_volumes_doc
    ON production_volumes (source_document_id);

CREATE INDEX IF NOT EXISTS idx_trade_flows_commodity_year
    ON trade_flows (commodity, year);
CREATE INDEX IF NOT EXISTS idx_trade_flows_exporter
    ON trade_flows (exporter_code);
CREATE INDEX IF NOT EXISTS idx_trade_flows_importer
    ON trade_flows (importer_code);

CREATE INDEX IF NOT EXISTS idx_prices_mineral_date
    ON prices (mineral, date);

CREATE INDEX IF NOT EXISTS idx_reserves_mineral
    ON reserves (mineral, country_code);

CREATE INDEX IF NOT EXISTS idx_staged_tables_doc
    ON staged_tables (document_id);

CREATE INDEX IF NOT EXISTS idx_pipeline_logs_doc_page
    ON pipeline_logs (document_id, page);
CREATE INDEX IF NOT EXISTS idx_pipeline_logs_timestamp
    ON pipeline_logs (timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_org_aliases_canonical
    ON organisation_aliases (canonical_name);
CREATE INDEX IF NOT EXISTS idx_org_aliases_alias
    ON organisation_aliases (alias);

CREATE INDEX IF NOT EXISTS idx_taxonomy_queue_status
    ON taxonomy_evolution_queue (status);
