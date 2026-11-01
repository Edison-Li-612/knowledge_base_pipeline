# Relationship Type Definitions

## Version 0.3.1

This document defines all valid **domain** relationship types for the pipeline. Each relationship is a directed triple: **Subject → Predicate → Object**, with typed attributes and mandatory scope dimensions.

Layer 2 (Bounded Interpretation Services, relationship extraction) uses this document to validate that extracted relationships conform to the allowed subject/object types and that all requirement classes are respected.

System relationships used internally by the pipeline (CONTRADICTS, EXTRACTED_FROM, SUPERSEDES) are defined separately in `pipeline_schemas/system_relationships.md`.

---

## Conventions

### Subject/object constraints

The allowed entity types for each end of the relationship. These are intentionally broad to accommodate the variety of statements found in real-world documents. The pipeline should capture the data point as stated in the source, even if the subject/object type is uncommon for that relationship.

Types marked with **(primary)** are the most common for this relationship. Other listed types are valid but less frequent.

### Entity types

`country` | `region` | `organisation` | `facility` | `project` | `mineral` | `product` | `technology` | `policy`

Note: `project` is a new entity type in v0.3.1. It represents a named undertaking that is not yet an operational facility (e.g., "the Kwinana lithium hydroxide project", "India's critical mineral exploration programme"). Projects may graduate to `facility` when operational. Both may coexist in the graph.

### Attribute requirement classes

Attribute requirement is purpose-dependent. This ontology distinguishes between fields required to instantiate a relationship, fields required for specific analytical uses, and fields required for gold-tier admissibility. Missing analytical or gold-tier fields do not invalidate a silver relationship if the structural minimum is satisfied.

| Requirement class | Code | Meaning |
|---|---|---|
| Structural required | `S` | Minimum needed for this relationship to exist at all in silver. Without this, the triple is not instantiated. |
| Analytical required | `A` | Needed for the relationship to support intended downstream analyses (time-series, cross-country comparison, supply chain mapping). Missing = silver record flagged as analytically incomplete. |
| Gold required | `G` | Needed for gold-tier admissibility for this relationship class. All S and A fields must also be met. |
| Conditional required | `C` | Required only if another field is present or a specific subtype applies. The condition is stated in the Notes column. |

A silver relationship needs all `S` fields. An analytically useful silver relationship also needs `A` fields. A gold-eligible relationship needs `S` + `A` + `G` fields plus all scope dimensions complete.

### Relationship families

Relationships are classified into four families. The family affects which requirement fields apply and how contradictions are handled.

| Family | Description | Examples |
|---|---|---|
| Structural | Describes the static structure of the supply chain: who is where, who owns what, what belongs to what. Often atemporal or slowly changing. | LOCATED_IN, SUBSIDIARY_OF, MEMBER_OF, OPERATES, OWNS |
| Transactional | Describes flows of materials, money, or trade between entities. Temporally scoped. | IMPORTS, EXPORTS, SUPPLIES, HAS_SUPPLY_AGREEMENT, INVESTS_IN |
| Capability/Dependency | Describes what an entity can do, what it needs, or what technology it uses. May or may not be temporally scoped. | PRODUCES, CONSUMES, PROCESSES_AT_STAGE, HAS_CAPACITY, USES_TECHNOLOGY, DEPENDS_ON, RESERVES |
| Measurement | Unary records that attach a measured value to an entity. Always temporally scoped. No object entity. | PRICES, EMPLOYS, EMITS |

---

## Scope dimensions (mandatory on every relationship)

Every extracted relationship carries a scope block in addition to its domain-specific attributes. Scope dimensions are used for contradiction detection, gold-tier admissibility, and query-time truth ranking. Two records with different scope dimensions are **not** contradictory; they are measuring different things.

| Scope dimension | Applicability | Description | Example values |
|---|---|---|---|
| `material_form` | Quantitative rels only | What form the quantity is measured in | `contained_metal`, `spodumene_concentrate`, `lithium_carbonate_equivalent`, `rare_earth_oxide`, `ore` |
| `metric_basis` | Quantitative rels only | What the number represents | `production_volume`, `refining_output`, `export_volume`, `capacity_nameplate`, `capacity_actual`, `reserves`, `consumption` |
| `geographic_scope` | All | What geography the data covers | `country_level`, `facility_level`, `regional`, `global` |
| `temporal_scope` | All (may be `atemporal` for structural) | What time period the data covers | `calendar_year_2023`, `fiscal_year_2023`, `Q1_2024`, `monthly_jan_2024`, `cumulative`, `atemporal`, `as_of_date` |
| `reporting_basis` | Where known | How the reporter defines the metric | `company_estimate`, `national_statistics`, `survey_based`, `satellite_derived` |
| `data_source_basis` | All | Primary vs secondary reporting | `primary_source`, `secondary_compilation`, `third_party_estimate` |

For structural relationships (LOCATED_IN, SUBSIDIARY_OF, MEMBER_OF), `material_form` and `metric_basis` are not applicable and should be omitted. `temporal_scope` may be `atemporal` or `as_of_date`.

---

---

## 1. PRODUCES

**Family:** Capability/Dependency

An entity produces a mineral, material, or product. Captures statements about actual production output only. For capacity claims, use HAS_CAPACITY instead.

| Field | Specification |
|---|---|
| Subject types | `country` **(primary)**, `organisation` **(primary)**, `facility`, `region` |
| Object types | `mineral` **(primary)**, `product` |
| Direction | Subject produces Object |

**Example statements this should capture:**
- "Australia produced 86,000 tonnes of lithium in 2023" → PRODUCES(AUS, lithium)
- "Albemarle's lithium production reached 200kt LCE" → PRODUCES(Albemarle, lithium)
- "The Greenbushes mine produced 1.4Mt of spodumene concentrate" → PRODUCES(Greenbushes, lithium)
- "CATL produced 321 GWh of battery cells" → PRODUCES(CATL, battery_cell)
- "Sub-Saharan Africa accounts for 70% of cobalt mine output" → PRODUCES(sub_saharan_africa, cobalt)
- "Australia is the world's largest lithium producer" → PRODUCES(AUS, lithium) with rank=1, no volume

**What this does NOT capture:**
- "The plant has 50kt nameplate capacity" → use HAS_CAPACITY
- "The facility is planned to produce 25kt/year" → use HAS_CAPACITY with capacity_type=planned

| Attribute | Req | Type | Controlled vocabulary | Notes |
|---|---|---|---|---|
| volume | — | numeric | — | Production quantity. Not S-required: structural relationships like "X is a producer of Y" are valid without volume. |
| unit | C | string | See units_and_metrics.md | Required if volume is present |
| metric | C | string | See mineral forms in hierarchy.md | Required if volume is present. e.g., `lithium_content`, `lithium_carbonate_equivalent`, `contained_metal` |
| time_period | A | string | — | Year, quarter, or date range. e.g., "2023", "Q1 2024", "2020-2023". Gold-required for quantitative claims. |
| supply_chain_stage | A | string | See controlled_vocabularies.md | e.g., `mining_extraction`, `refining_smelting`. Critical for disambiguating what "production" means. |
| rank | — | integer | — | e.g., 1 = world's largest producer |
| share_percent | — | numeric | — | Share of global/regional production |
| share_scope | C | string | — | Required if share_percent present. e.g., "global", "regional", "domestic" |
| qualifier | — | string | `estimated`, `withheld`, `revised`, `preliminary`, `forecast` | Data quality qualifier |

**Structural minimum (S):** subject + predicate + object
**Analytical minimum (S+A):** plus at least one production signal (volume, share_percent, or rank), plus time_period, plus supply_chain_stage
**Gold minimum (S+A+G):** plus all scope dimensions populated, plus metric and material_form if quantitative, plus no blocking ambiguities

---

## 2. HAS_CAPACITY

**Family:** Capability/Dependency

*New in v0.3.1.* An entity has a production, processing, or throughput capacity. Separated from PRODUCES to distinguish actual output from capability claims.

| Field | Specification |
|---|---|
| Subject types | `facility` **(primary)**, `organisation`, `country`, `project` |
| Object types | `mineral` **(primary)**, `product` |
| Direction | Subject has capacity for Object |

**Example statements this should capture:**
- "The Kwinana plant has 50kt/year lithium hydroxide capacity" → HAS_CAPACITY(Kwinana, lithium)
- "Pilbara Minerals is expanding Pilgangoora to 1Mtpa spodumene" → HAS_CAPACITY(Pilgangoora, lithium) with capacity_type=planned
- "The proposed Saltend facility will have 12,500 tpa REE separation capacity" → HAS_CAPACITY(Saltend, rare_earth_elements)
- "China has 80% of global lithium refining capacity" → HAS_CAPACITY(CHN, lithium) with share_percent=80

| Attribute | Req | Type | Controlled vocabulary | Notes |
|---|---|---|---|---|
| capacity | S | numeric | — | Capacity quantity |
| unit | S | string | See units | |
| metric | C | string | See mineral forms | Required if mineral is the object |
| capacity_type | A | string | `nameplate`, `effective`, `planned`, `under_construction`, `approved`, `suspended`, `decommissioned` | |
| supply_chain_stage | A | string | See controlled_vocabularies.md | What stage this capacity is for |
| time_period | A | string | — | When this capacity applies or is expected |
| share_percent | — | numeric | — | Share of global/regional capacity |
| share_scope | C | string | — | Required if share_percent present |
| expected_commissioning | — | string | — | For planned/under_construction. ISO 8601 date or year |
| qualifier | — | string | `estimated`, `revised`, `preliminary` | |

**Structural minimum (S):** subject + predicate + object + capacity + unit
**Analytical minimum (S+A):** plus capacity_type + supply_chain_stage + time_period
**Gold minimum (S+A+G):** plus all scope dimensions, plus metric if quantitative

---

## 3. CONSUMES

**Family:** Capability/Dependency

An entity consumes, uses, or creates demand for a mineral, material, or product. Captures actual observed consumption only. For demand forecasts, use qualifier=`forecast` to distinguish.

| Field | Specification |
|---|---|
| Subject types | `country` **(primary)**, `organisation` **(primary)**, `facility`, `region` |
| Object types | `mineral` **(primary)**, `product` |
| Direction | Subject consumes Object |

**Example statements this should capture:**
- "China consumed 75% of global cobalt supply" → CONSUMES(CHN, cobalt)
- "CATL's lithium consumption exceeded 100kt LCE" → CONSUMES(CATL, lithium)
- "Global EV battery demand reached 750 GWh" → CONSUMES(global, battery_cell) with qualifier=forecast if projected

| Attribute | Req | Type | Controlled vocabulary | Notes |
|---|---|---|---|---|
| volume | — | numeric | — | Consumption quantity |
| unit | C | string | See units | Required if volume present |
| metric | C | string | See mineral forms | Required if volume present |
| time_period | A | string | — | |
| share_percent | — | numeric | — | Share of global/regional consumption |
| share_scope | C | string | — | Required if share_percent present |
| end_use | — | string | — | e.g., "batteries", "stainless steel", "magnets" |
| supply_chain_stage | — | string | See controlled vocabularies | At what stage the consumption occurs |
| qualifier | — | string | `estimated`, `forecast`, `preliminary`, `actual` | Distinguishes observed consumption from demand projections |

**Structural minimum (S):** subject + predicate + object
**Analytical minimum (S+A):** plus at least one of volume or share_percent, plus time_period
**Gold minimum (S+A+G):** plus scope dimensions, plus qualifier distinguishing actual from forecast

---

## 4. RESERVES

**Family:** Capability/Dependency

An entity holds mineral reserves or resources.

| Field | Specification |
|---|---|
| Subject types | `country` **(primary)**, `organisation`, `facility` |
| Object types | `mineral` |
| Direction | Subject has reserves/resources of Object |

**Example statements this should capture:**
- "Australia has lithium reserves of 6.2 Mt" → RESERVES(AUS, lithium)
- "Pilbara Minerals reported ore reserves of 214 Mt at 1.2% Li2O" → RESERVES(Pilbara Minerals, lithium)

| Attribute | Req | Type | Controlled vocabulary | Notes |
|---|---|---|---|---|
| volume | S | numeric | — | Reserve/resource quantity |
| unit | S | string | See units | |
| metric | A | string | See mineral forms | Reporting basis (e.g., `contained_metal`, `ore`, `spodumene_concentrate`) |
| resource_or_reserve | A | string | `resource`, `reserve` | Distinguishes mineral resources from ore reserves. Analytically critical for comparability. |
| reserve_classification | — | string | `measured`, `indicated`, `inferred`, `proved`, `probable`, `measured_and_indicated`, `unspecified` | |
| reporting_standard | G | string | `jorc`, `ni_43_101`, `samrec`, `crirsco`, `sec_s_k`, `unspecified` | Gold-required unless source only gives high-level national figure |
| ore_grade | — | numeric | — | e.g., 1.2 |
| ore_grade_unit | C | string | — | Required if ore_grade present. e.g., "% Li2O", "% Ni", "g/t" |
| time_period | A | string | — | As-of year for the estimate |
| qualifier | — | string | `estimated`, `revised` | |

**Structural minimum (S):** subject + object + volume + unit
**Analytical minimum (S+A):** plus resource_or_reserve + metric + time_period
**Gold minimum (S+A+G):** plus reporting_standard (or explicit acknowledgement of national-level figure), plus scope dimensions

---

## 5. IMPORTS

**Family:** Transactional

A country or region imports a commodity from another country or region. Use for country-level trade statistics. For company-level supply, use SUPPLIES or HAS_SUPPLY_AGREEMENT.

| Field | Specification |
|---|---|
| Subject types | `country` **(primary)**, `region` |
| Object types | `country` **(primary)**, `region` |
| Direction | Subject imports from Object |

| Attribute | Req | Type | Controlled vocabulary | Notes |
|---|---|---|---|---|
| commodity | S | string | Mineral/product canonical names | What is being imported |
| form | — | string | See mineral forms | e.g., `lithium_carbonate`, `copper_concentrate` |
| volume | — | numeric | — | |
| unit | C | string | See units | Required if volume present |
| value | — | numeric | — | Trade value |
| currency | C | string | ISO 4217 | Required if value present |
| time_period | A | string | — | Year, quarter, or date range. Harmonised with EXPORTS and SUPPLIES. |
| share_percent | — | numeric | — | Share of importer's total imports of this commodity |
| share_scope | C | string | — | Required if share_percent present |

**Structural minimum (S):** subject + object + commodity
**Analytical minimum (S+A):** plus time_period, plus at least one of volume, value, or share_percent
**Gold minimum (S+A+G):** plus scope dimensions (especially material_form and temporal_scope)

---

## 6. EXPORTS

**Family:** Transactional

A country or region exports a commodity to another entity.

| Field | Specification |
|---|---|
| Subject types | `country` **(primary)**, `region` |
| Object types | `country` **(primary)**, `region` |
| Direction | Subject exports to Object |

| Attribute | Req | Type | Controlled vocabulary | Notes |
|---|---|---|---|---|
| commodity | S | string | Mineral/product canonical names | |
| form | — | string | See mineral forms | |
| volume | — | numeric | — | |
| unit | C | string | See units | Required if volume present |
| value | — | numeric | — | |
| currency | C | string | ISO 4217 | Required if value present |
| time_period | A | string | — | Harmonised: year, quarter, or date range |
| share_percent | — | numeric | — | |
| share_scope | C | string | — | Required if share_percent present |

**Structural minimum (S):** subject + object + commodity
**Analytical minimum (S+A):** plus time_period, plus at least one of volume, value, or share_percent
**Gold minimum (S+A+G):** plus scope dimensions

---

## 7. SUPPLIES

**Family:** Transactional

An entity supplies a commodity to another entity. Captures realised or asserted supply flows between companies, facilities, or from facilities to countries. For contractual agreements without confirmed flow, use HAS_SUPPLY_AGREEMENT.

| Field | Specification |
|---|---|
| Subject types | `organisation` **(primary)**, `facility`, `country` |
| Object types | `organisation` **(primary)**, `facility`, `country`, `region` |
| Direction | Subject supplies to Object |

**Example statements this should capture:**
- "Ganfeng supplied 20kt lithium hydroxide to Tesla in 2024" → SUPPLIES(Ganfeng, Tesla)
- "The Greenbushes mine ships spodumene to Chinese converters" → SUPPLIES(Greenbushes, CHN)

**What this does NOT capture:**
- "SQM signed a long-term offtake with LG Energy Solution" → use HAS_SUPPLY_AGREEMENT

| Attribute | Req | Type | Controlled vocabulary | Notes |
|---|---|---|---|---|
| commodity | S | string | Mineral/product canonical names | |
| form | — | string | See mineral forms | |
| volume | — | numeric | — | |
| unit | C | string | See units | Required if volume present |
| value | — | numeric | — | |
| currency | C | string | ISO 4217 | Required if value present |
| time_period | A | string | — | Year, quarter, or date range |

**Structural minimum (S):** subject + object + commodity
**Analytical minimum (S+A):** plus time_period
**Gold minimum (S+A+G):** plus scope dimensions, plus at least one of volume or value

---

## 8. HAS_SUPPLY_AGREEMENT

**Family:** Transactional

*New in v0.3.1.* Two entities have a contractual supply relationship (offtake, tolling, long-term contract). Separated from SUPPLIES because contractual relationships and realised flows are fundamentally different analytical objects.

| Field | Specification |
|---|---|
| Subject types | `organisation` **(primary)**, `country` |
| Object types | `organisation` **(primary)**, `country` |
| Direction | Subject has supply agreement with Object (supplier → buyer) |

**Example statements this should capture:**
- "SQM signed a long-term offtake with LG Energy Solution" → HAS_SUPPLY_AGREEMENT(SQM, LG Energy Solution)
- "Ganfeng entered a 5-year lithium hydroxide supply deal with BMW" → HAS_SUPPLY_AGREEMENT(Ganfeng, BMW)
- "Pilbara Minerals has an offtake with POSCO for spodumene concentrate" → HAS_SUPPLY_AGREEMENT(Pilbara Minerals, POSCO)

| Attribute | Req | Type | Controlled vocabulary | Notes |
|---|---|---|---|---|
| commodity | S | string | Mineral/product canonical names | |
| form | — | string | See mineral forms | |
| agreement_type | A | string | `offtake`, `long_term_contract`, `tolling`, `swap`, `spot_agreement`, `joint_venture_supply`, `government_to_government` | |
| contracted_volume | — | numeric | — | Annual or total contracted volume |
| unit | C | string | See units | Required if contracted_volume present |
| contract_duration | — | string | — | e.g., "5 years", "2024-2029" |
| start_date | — | string | — | ISO 8601 |
| end_date | — | string | — | ISO 8601 |
| value | — | numeric | — | Contract value if disclosed |
| currency | C | string | ISO 4217 | Required if value present |
| status | — | string | `active`, `signed`, `announced`, `expired`, `terminated`, `under_negotiation` | |

**Structural minimum (S):** subject + object + commodity
**Analytical minimum (S+A):** plus agreement_type
**Gold minimum (S+A+G):** plus scope dimensions, plus at least one of contracted_volume, contract_duration, or start_date

---

## 9. OPERATES

**Family:** Structural

An entity operates a facility or project.

| Field | Specification |
|---|---|
| Subject types | `organisation` **(primary)**, `country` |
| Object types | `facility` **(primary)**, `project` |
| Direction | Subject operates Object |

| Attribute | Req | Type | Controlled vocabulary | Notes |
|---|---|---|---|---|
| ownership_percent | — | numeric | — | 0-100 |
| role | — | string | `operator`, `joint_venture_partner`, `minority_stakeholder`, `managing_partner`, `non_operating_partner` | |
| start_date | — | string | — | ISO 8601 |
| end_date | — | string | — | If the operation has ended |
| status | — | string | `active`, `under_construction`, `suspended`, `decommissioned`, `planned`, `care_and_maintenance` | |

**Structural minimum (S):** subject + object
**Analytical minimum (S+A):** no additional fields required (structural relationship)
**Gold minimum (S+A+G):** plus status if known, plus scope dimensions (geographic_scope, temporal_scope, data_source_basis)

---

## 10. LOCATED_IN

**Family:** Structural

An entity is located in a country or region.

| Field | Specification |
|---|---|
| Subject types | `facility` **(primary)**, `project`, `organisation` |
| Object types | `country` **(primary)**, `region` |
| Direction | Subject is located in Object |

| Attribute | Req | Type | Controlled vocabulary | Notes |
|---|---|---|---|---|
| sub_national_region | — | string | — | Province, state, or district |
| location_type | — | string | `headquarters`, `registered_office`, `operational_site`, `project_site` | Clarifies what kind of location, especially for organisations |
| coordinates | — | object | — | `{lat, lon}` if available |

**Structural minimum (S):** subject + object
**Gold minimum (S+A+G):** plus scope dimensions (geographic_scope=facility_level or country_level, temporal_scope, data_source_basis)

---

## 11. OWNS / HAS_STAKE_IN

**Family:** Structural

An entity owns or holds an economic stake in another entity. Use for ownership percentages, acquisitions, and economic control. For formal corporate hierarchy (parent-subsidiary), use SUBSIDIARY_OF.

**Disambiguation rule:**
- Use OWNS when the statement is about economic stake, control, or transaction value.
- Use SUBSIDIARY_OF when the statement is about formal corporate hierarchy.
- Extract both if both are stated or strongly implied.

| Field | Specification |
|---|---|
| Subject types | `organisation` **(primary)**, `country` |
| Object types | `organisation` **(primary)**, `facility`, `project` |
| Direction | Subject owns/holds stake in Object |

| Attribute | Req | Type | Controlled vocabulary | Notes |
|---|---|---|---|---|
| ownership_percent | — | numeric | — | 0-100; null if "owns" but percentage not stated |
| acquisition_date | — | string | — | ISO 8601 |
| transaction_value | — | numeric | — | |
| currency | C | string | ISO 4217 | Required if transaction_value present |
| stake_type | — | string | `majority`, `minority`, `joint_venture`, `wholly_owned`, `strategic`, `controlling` | |
| status | — | string | `current`, `divested`, `pending_approval`, `announced` | |

**Structural minimum (S):** subject + object
**Analytical minimum (S+A):** no additional fields beyond structural (the ownership fact itself is the value)
**Gold minimum (S+A+G):** plus ownership_percent if stated, plus scope dimensions

---

## 12. SUBSIDIARY_OF

**Family:** Structural

An organisation is a subsidiary or division of a parent organisation. Captures formal corporate hierarchy only.

| Field | Specification |
|---|---|
| Subject types | `organisation` |
| Object types | `organisation` |
| Direction | Subject is a subsidiary of Object |

| Attribute | Req | Type | Controlled vocabulary | Notes |
|---|---|---|---|---|
| relationship_type | — | string | `subsidiary`, `division`, `joint_venture_entity`, `spin_off`, `government_enterprise` | |
| since | — | string | — | When the relationship started |

**Structural minimum (S):** subject + object
**Gold minimum (S+A+G):** plus scope dimensions

---

## 13. PARTNERS_WITH

**Family:** Structural

Two entities have a partnership, joint venture, or strategic alliance. Bidirectional.

| Field | Specification |
|---|---|
| Subject types | `organisation` **(primary)**, `country` |
| Object types | `organisation` **(primary)**, `country` |
| Direction | Bidirectional |

| Attribute | Req | Type | Controlled vocabulary | Notes |
|---|---|---|---|---|
| partnership_type | A | string | `joint_venture`, `strategic_alliance`, `technology_licence`, `bilateral_agreement`, `mou`, `research_collaboration` | Analytically required. Without this, the relationship is too vague for most analyses. |
| commodity | — | string | Mineral canonical names | What the partnership concerns |
| start_date | — | string | — | |
| end_date | — | string | — | |
| scope | — | string | — | Free text describing what the partnership covers |

**Note:** Offtake agreements are no longer captured here. Use HAS_SUPPLY_AGREEMENT instead.

**Structural minimum (S):** subject + object
**Analytical minimum (S+A):** plus partnership_type
**Gold minimum (S+A+G):** plus scope dimensions, plus commodity if applicable

---

## 14. REGULATES / RESTRICTS

**Family:** Transactional (event-like)

An entity (policy, country, or institution) regulates, restricts, or incentivises an activity, commodity, or entity.

| Field | Specification |
|---|---|
| Subject types | `policy` **(primary)**, `country` **(primary)**, `organisation` |
| Object types | `mineral` **(primary)**, `country`, `organisation`, `technology`, `product`, `facility` |
| Direction | Subject regulates/restricts Object |

| Attribute | Req | Type | Controlled vocabulary | Notes |
|---|---|---|---|---|
| regulation_type | A | string | `export_control`, `export_ban`, `import_tariff`, `import_quota`, `environmental_standard`, `strategic_reserve`, `licensing_requirement`, `sanctions`, `subsidy`, `tax_incentive`, `domestic_processing_requirement`, `critical_mineral_designation`, `resource_nationalism` | Analytically required. Without this, the system cannot distinguish restrictive from supportive policy. |
| effective_date | — | string | — | ISO 8601 |
| expiry_date | — | string | — | If time-limited |
| scope_description | — | string | — | Free text describing what aspect is regulated |
| jurisdiction | — | string | ISO alpha-3 | Country that enacted the regulation |
| impact_description | — | string | — | Free text summary of the regulation's impact |
| target_activity | — | string | See supply chain stages | If the regulation targets a specific supply chain activity |

**Structural minimum (S):** subject + object
**Analytical minimum (S+A):** plus regulation_type
**Gold minimum (S+A+G):** plus effective_date or time_period, plus scope dimensions

---

## 15. PROCESSES_AT_STAGE

**Family:** Capability/Dependency

An entity processes a mineral at a specific supply chain stage. Captures the what-happens-where of the value chain. For quantitative processing capacity or throughput, use HAS_CAPACITY.

| Field | Specification |
|---|---|
| Subject types | `facility` **(primary)**, `organisation` **(primary)**, `country` |
| Object types | `mineral` **(primary)**, `product` |
| Direction | Subject processes Object |

**Example statements this should capture:**
- "The Kwinana plant converts spodumene to lithium hydroxide" → PROCESSES_AT_STAGE(Kwinana, lithium)
- "China refines over 60% of global cobalt" → PROCESSES_AT_STAGE(CHN, cobalt) with share_percent=60

**What this does NOT capture:**
- "The plant has 50kt refining capacity" → use HAS_CAPACITY

| Attribute | Req | Type | Controlled vocabulary | Notes |
|---|---|---|---|---|
| supply_chain_stage | S | string | See controlled_vocabularies.md | The stage at which processing occurs. Structurally required because without it, PROCESSES_AT_STAGE has no meaning beyond PRODUCES. |
| input_form | — | string | See mineral forms | What form enters the process |
| output_form | — | string | See mineral forms | What form leaves the process |
| share_percent | — | numeric | — | e.g., "refines 60% of global cobalt" |
| share_scope | C | string | — | Required if share_percent present |
| time_period | — | string | — | |

**Structural minimum (S):** subject + object + supply_chain_stage
**Analytical minimum (S+A):** plus at least one of input_form or output_form
**Gold minimum (S+A+G):** plus scope dimensions

---

## 16. USES_TECHNOLOGY

**Family:** Capability/Dependency

An entity uses a specific technology or process.

| Field | Specification |
|---|---|
| Subject types | `facility` **(primary)**, `organisation`, `country` |
| Object types | `technology` |
| Direction | Subject uses Object |

| Attribute | Req | Type | Controlled vocabulary | Notes |
|---|---|---|---|---|
| application | — | string | — | What the technology is applied to (e.g., "lithium extraction", "cobalt recovery") |
| process_stage | — | string | See supply chain stages | Which supply chain stage this technology is used at |
| mineral_context | — | string | Mineral canonical names | Which mineral this technology application relates to |
| status | — | string | `commercial`, `pilot`, `demonstration`, `research`, `planned` | Technology readiness |
| time_period | — | string | — | |
| scale | — | string | — | e.g., "10,000 tpa", "commercial scale" |

**Structural minimum (S):** subject + object
**Analytical minimum (S+A):** no additional (the technology-use link itself is the value)
**Gold minimum (S+A+G):** plus scope dimensions

---

## 17. INVESTS_IN

**Family:** Transactional

An entity invests in another entity, project, or technology.

| Field | Specification |
|---|---|
| Subject types | `organisation` **(primary)**, `country` **(primary)** |
| Object types | `facility` **(primary)**, `project` **(primary)**, `organisation`, `technology` |
| Direction | Subject invests in Object |

**Note:** `mineral` is no longer a valid object type. Statements like "India allocated $1.8B for lithium exploration" should be encoded as INVESTS_IN(IND, [project]) where the project captures the exploration programme, or as INVESTS_IN(IND, lithium_exploration) with a project entity. This avoids the semantic confusion of "investing in a mineral."

| Attribute | Req | Type | Controlled vocabulary | Notes |
|---|---|---|---|---|
| investment_amount | — | numeric | — | |
| currency | C | string | ISO 4217 | Required if amount present |
| time_period | — | string | — | |
| investment_type | — | string | `equity`, `debt`, `grant`, `offtake_prepayment`, `government_subsidy`, `exploration_spend`, `capex`, `r_and_d` | |
| project_name | — | string | — | |
| investment_stage | — | string | `exploration`, `feasibility`, `construction`, `expansion`, `acquisition` | |

**Structural minimum (S):** subject + object
**Analytical minimum (S+A):** plus at least one of investment_amount or investment_type
**Gold minimum (S+A+G):** plus scope dimensions, plus time_period

---

## 18. DEPENDS_ON

**Family:** Capability/Dependency

An entity depends on a mineral, product, technology, or another entity.

| Field | Specification |
|---|---|
| Subject types | `product` **(primary)**, `technology` **(primary)**, `country`, `organisation`, `facility` |
| Object types | `mineral` **(primary)**, `product`, `technology`, `country`, `organisation` |
| Direction | Subject depends on Object |

| Attribute | Req | Type | Controlled vocabulary | Notes |
|---|---|---|---|---|
| dependency_type | A | string | `material_input`, `import_reliance`, `technology_input`, `supplier_dependency`, `strategic_dependency`, `process_byproduct` | Analytically required. Without this, the predicate is too broad for useful analysis. |
| quantity_per_unit | — | numeric | — | e.g., kg of lithium per kWh |
| unit | C | string | — | Required if quantity_per_unit present |
| product_unit | C | string | — | Required if quantity_per_unit present. What "per unit" means (per vehicle, per kWh, per module) |
| import_dependency_percent | — | numeric | — | For country-level import dependency |
| substitutability | — | string | `none`, `limited`, `moderate`, `high` | |
| criticality | — | string | `low`, `medium`, `high`, `critical` | |
| time_period | — | string | — | |

**Structural minimum (S):** subject + object
**Analytical minimum (S+A):** plus dependency_type
**Gold minimum (S+A+G):** plus scope dimensions, plus at least one quantitative attribute (quantity_per_unit or import_dependency_percent) if applicable

---

## 19. PRICES

**Family:** Measurement (unary)

Temporal price data for a mineral or product.

| Field | Specification |
|---|---|
| Subject types | `mineral` **(primary)**, `product` |
| Object types | (none, unary) |
| Direction | N/A |

| Attribute | Req | Type | Controlled vocabulary | Notes |
|---|---|---|---|---|
| price | S | numeric | — | |
| currency | S | string | ISO 4217 | e.g., `USD`, `EUR`, `CNY` |
| unit_basis | S | string | See units | What the price is per. e.g., `tonne`, `kg`, `lb`, `kWh`. Separated from currency to avoid redundancy. |
| form | A | string | See mineral forms | Which form is priced (e.g., `lithium_carbonate`, `nickel_sulphate`). Analytically required because prices are not comparable across forms. |
| price_type | — | string | `spot`, `contract`, `average_annual`, `average_quarterly`, `average_monthly`, `futures`, `assessed`, `indicative` | |
| date | S | string | — | ISO 8601 date, month (YYYY-MM), or year (YYYY) |
| exchange | — | string | `LME`, `CME`, `SGX`, `SHFE`, `DCE` | If exchange-traded |
| source_assessment | — | string | — | e.g., "Fastmarkets MB", "Benchmark Mineral Intelligence" |
| price_trend | — | string | `rising`, `falling`, `stable`, `volatile` | Qualitative trend if stated |

**Structural minimum (S):** subject + price + currency + unit_basis + date
**Analytical minimum (S+A):** plus form
**Gold minimum (S+A+G):** plus scope dimensions

---

## 20. MEMBER_OF

**Family:** Structural (atemporal)

A mineral species belongs to a mineral group.

| Field | Specification |
|---|---|
| Subject types | `mineral` (species level) |
| Object types | `mineral` (group level) |
| Direction | Subject is a member of Object |

| Attribute | Req | Type | Controlled vocabulary | Notes |
|---|---|---|---|---|
| sub_group | — | string | `lree`, `hree` (for REEs) | Optional sub-classification |

**Structural minimum (S):** subject + object
**This relationship is atemporal.** Scope dimensions: geographic_scope=N/A, temporal_scope=atemporal, material_form=N/A, metric_basis=N/A.

---

## 21. EMPLOYS

**Family:** Measurement (unary)

Employment data for an entity.

| Field | Specification |
|---|---|
| Subject types | `organisation` **(primary)**, `facility`, `country` |
| Object types | (none, unary) |
| Direction | N/A |

| Attribute | Req | Type | Controlled vocabulary | Notes |
|---|---|---|---|---|
| headcount | S | integer | — | |
| time_period | A | string | — | Year or as-of date. Using time_period instead of year to accommodate "as of Q2 2024" or "current headcount" statements. |
| employment_type | — | string | `direct`, `contractor`, `total`, `full_time`, `part_time` | |
| skill_category | — | string | — | Free text |
| sector | — | string | — | For country-level employment, which sector |

**Structural minimum (S):** subject + headcount
**Analytical minimum (S+A):** plus time_period
**Gold minimum (S+A+G):** plus scope dimensions

---

## 22. EMITS

**Family:** Measurement (unary)

Environmental impact data for an entity.

| Field | Specification |
|---|---|
| Subject types | `facility` **(primary)**, `organisation` **(primary)**, `technology`, `country` |
| Object types | (none, unary) |
| Direction | N/A |

| Attribute | Req | Type | Controlled vocabulary | Notes |
|---|---|---|---|---|
| emission_type | S | string | `co2`, `co2e`, `water_usage`, `water_consumption`, `energy_consumption`, `electricity_consumption`, `waste_generated`, `tailings`, `acid_mine_drainage`, `particulates`, `sox`, `nox` | |
| value | S | numeric | — | |
| unit | S | string | — | e.g., `tCO2/t_product`, `m3/t`, `kWh/t`, `MtCO2e` |
| intensity_or_absolute | A | string | `intensity`, `absolute` | Analytically required. Total emissions and per-unit intensity are fundamentally different metrics and must not be conflated. |
| intensity_basis | G | string | — | Gold-required when intensity_or_absolute=intensity. What "per unit" refers to (e.g., "per tonne of copper cathode", "per kWh"). |
| time_period | A | string | — | |
| ghg_scope | — | string | `scope_1`, `scope_2`, `scope_3`, `scope_1_2`, `scope_1_2_3`, `total` | GHG protocol scopes |
| mineral_context | — | string | Mineral canonical names | Which mineral's production this emission relates to |

**Structural minimum (S):** subject + emission_type + value + unit
**Analytical minimum (S+A):** plus intensity_or_absolute + time_period
**Gold minimum (S+A+G):** plus intensity_basis (if intensity), plus scope dimensions

---

## Relationship extraction guidance

### Direct vs inferred relationships

- **Direct**: The relationship and its key attributes are explicitly stated in the source text. Example: "Australia produced 86,000 tonnes of lithium in 2023" → PRODUCES(AUS, lithium, volume=86000, unit=tonnes, time_period="2023", extraction_type=direct).
- **Inferred**: The relationship or a specific attribute is derived from context, calculation, or implication. Example: "Australia remained the world's leading lithium producer" → PRODUCES(AUS, lithium, rank=1, extraction_type=inferred).

### Multi-relationship extraction from tables

A single table row often generates multiple relationships. Example: a row in a "World Production" table with columns [Country, 2022 Production, 2023 Production, Reserves] generates:
- PRODUCES(country, mineral, volume=X, time_period="2022")
- PRODUCES(country, mineral, volume=Y, time_period="2023")
- RESERVES(country, mineral, volume=Z)

### Multi-relationship extraction from a single sentence

A single sentence may yield multiple relationships. Example: "Albemarle, the world's largest lithium producer, operates the Kemerton hydroxide plant in Western Australia" yields:
- PRODUCES(Albemarle, lithium, rank=1)
- OPERATES(Albemarle, Kemerton)
- LOCATED_IN(Kemerton, AUS, sub_national_region="Western Australia")
- PROCESSES_AT_STAGE(Kemerton, lithium, stage=refining_smelting, output_form=lithium_hydroxide)

### Choosing between overlapping relationship types

| Statement pattern | Relationship type |
|---|---|
| Country-level trade data (customs statistics) | IMPORTS / EXPORTS |
| Company-to-company commercial flow (realised) | SUPPLIES |
| Contractual or announced supply agreement | HAS_SUPPLY_AGREEMENT |
| "X produces Y" (actual output) | PRODUCES |
| "X has capacity of Y" (capability claim) | HAS_CAPACITY |
| "X consumes/uses/demands Y" | CONSUMES |
| "X processes Y into Z" | PROCESSES_AT_STAGE |
| "X owns Y" (economic stake) | OWNS |
| "X operates Y" (operational control) | OPERATES |
| "X is a subsidiary of Y" (corporate hierarchy) | SUBSIDIARY_OF |
| When genuinely ambiguous | Extract the most specific applicable type and note the ambiguity |

### Handling ambiguous scope

When the scope of a relationship is ambiguous (e.g., "China dominates rare earth production" without specifying mining vs refining), extract what is stated and use the `supply_chain_stage` attribute to capture the ambiguity. Do not invent specificity that is not in the source. If the stage cannot be determined, leave it null and the record will have incomplete scope dimensions, which affects its analytical and gold eligibility but does not prevent silver storage.

### Handling aggregate vs specific entities

Documents often make statements at different levels of specificity:
- "China produces 60% of graphite" → PRODUCES(CHN, graphite) at country level
- "BTR is the largest anode material producer" → PRODUCES(BTR, graphite_anode) at company + product level

Both are valid. Do not force aggregation or disaggregation. Extract at the level stated in the source. The graph database handles multi-level querying through entity linkages (LOCATED_IN, SUBSIDIARY_OF, MEMBER_OF).

### Requirement class in extraction prompts

When the relationship extraction LLM encounters a statement that yields a relationship with only structural-minimum fields populated, it should still extract it. The extraction prompt must not discard relationships just because analytical or gold fields are missing. Silver storage is explicitly designed for structurally valid but analytically incomplete records. The tier system handles the rest.