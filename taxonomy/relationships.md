# Relationship Type Definitions

## Version 0.2.0

This document defines all valid relationship types for the pipeline. Each relationship is a directed triple: **Subject → Predicate → Object**, with typed attributes.

The relationship extraction agent (Agent 5) uses this document to validate that extracted relationships conform to the allowed subject/object types and that all required attributes are present.

---

## Conventions

- **Subject/Object constraints**: The allowed entity types for each end of the relationship. These are intentionally broad to accommodate the variety of statements found in real-world documents. The pipeline should capture the data point as stated in the source, even if the subject/object type is uncommon for that relationship.
- **Primary participants**: Marked with **(primary)** — these are the most common subject/object types for this relationship. Other listed types are valid but less frequent.
- **Required attributes**: Must be present for the relationship to be valid. If not extractable, the field is set to `null` and the relationship is flagged as incomplete.
- **Optional attributes**: Enriching information that may or may not be available in the source.
- **Temporal scope**: Most relationships are temporally scoped (they describe a situation at a specific point in time). The `year` or `time_period` attribute captures this.

---

## 1. PRODUCES

An entity produces a mineral, material, or product.

Captures any statement about production output — from mine production by a country, to refined output by a company, to component production by a factory.

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

| Attribute | Type | Required | Controlled vocabulary | Notes |
|---|---|---|---|---|
| volume | numeric | No | — | Production quantity |
| unit | string | Yes (if volume present) | See [units_and_metrics.md](units_and_metrics.md) | e.g., `tonnes`, `kt`, `Mt`, `GWh` |
| metric | string | Yes (if volume present) | See mineral forms in [hierarchy.md](minerals/hierarchy.md) | e.g., `lithium_content`, `lithium_carbonate_equivalent`, `contained_metal` |
| year | integer | Yes | — | Reporting year |
| capacity_type | string | No | `actual`, `nameplate`, `planned`, `under_construction`, `effective`, `suspended` | Distinguishes actual output from capacity |
| supply_chain_stage | string | No | See [controlled_vocabularies.md](controlled_vocabularies.md) | e.g., `mining_extraction`, `refining_smelting` — critical for disambiguating what "production" means |
| rank | integer | No | — | e.g., 1 = world's largest producer |
| share_percent | numeric | No | — | Share of global/regional production |
| share_scope | string | No | — | What the share is relative to (e.g., "global", "regional", "domestic") |
| qualifier | string | No | `estimated`, `withheld`, `revised`, `preliminary`, `forecast` | Data quality qualifier |

---

## 2. CONSUMES

An entity consumes, uses, or creates demand for a mineral, material, or product.

Captures demand-side data, which is distinct from production. Many documents report consumption alongside production.

| Field | Specification |
|---|---|
| Subject types | `country` **(primary)**, `organisation` **(primary)**, `facility`, `region` |
| Object types | `mineral` **(primary)**, `product` |
| Direction | Subject consumes Object |

**Example statements this should capture:**
- "China consumed 75% of global cobalt supply" → CONSUMES(CHN, cobalt)
- "CATL's lithium consumption exceeded 100kt LCE" → CONSUMES(CATL, lithium)
- "The EU battery sector consumed 35kt of nickel sulphate" → CONSUMES(eu_27, nickel)
- "Global EV battery demand reached 750 GWh" → CONSUMES(global, battery_cell)

| Attribute | Type | Required | Controlled vocabulary | Notes |
|---|---|---|---|---|
| volume | numeric | No | — | Consumption quantity |
| unit | string | Yes (if volume present) | See units | |
| metric | string | Yes (if volume present) | See mineral forms | |
| year | integer | Yes | — | |
| share_percent | numeric | No | — | Share of global/regional consumption |
| share_scope | string | No | — | e.g., "global", "domestic" |
| end_use | string | No | — | What the mineral is consumed for (e.g., "batteries", "stainless steel", "magnets") |
| supply_chain_stage | string | No | See controlled vocabularies | At what stage the consumption occurs |
| qualifier | string | No | `estimated`, `forecast`, `preliminary` | |

---

## 3. RESERVES

An entity holds mineral reserves or resources.

| Field | Specification |
|---|---|
| Subject types | `country` **(primary)**, `organisation`, `facility` |
| Object types | `mineral` |
| Direction | Subject has reserves/resources of Object |

**Example statements this should capture:**
- "Australia has lithium reserves of 6.2 Mt" → RESERVES(AUS, lithium)
- "Pilbara Minerals reported ore reserves of 214 Mt at 1.2% Li2O" → RESERVES(Pilbara Minerals, lithium)
- "The Greenbushes mine has proved reserves of 150 Mt" → RESERVES(Greenbushes, lithium)

| Attribute | Type | Required | Controlled vocabulary | Notes |
|---|---|---|---|---|
| volume | numeric | Yes | — | Reserve/resource quantity |
| unit | string | Yes | See units | |
| metric | string | No | See mineral forms | Reporting basis (e.g., `contained_metal`, `ore`, `spodumene_concentrate`) |
| reserve_classification | string | No | `measured`, `indicated`, `inferred`, `proved`, `probable`, `measured_and_indicated`, `unspecified` | JORC/NI 43-101/CRIRSCO classification |
| resource_or_reserve | string | No | `resource`, `reserve` | Distinguishes mineral resources from ore reserves |
| ore_grade | numeric | No | — | e.g., 1.2 (for 1.2% Li2O) |
| ore_grade_unit | string | No | — | e.g., "% Li2O", "% Ni", "g/t" |
| year | integer | Yes | — | As-of year for the estimate |
| reporting_standard | string | No | `jorc`, `ni_43_101`, `samrec`, `crirsco`, `sec_s_k`, `unspecified` | Which reporting code was used |
| qualifier | string | No | `estimated`, `revised` | |

---

## 4. IMPORTS

An entity imports a commodity from another entity.

| Field | Specification |
|---|---|
| Subject types | `country` **(primary)**, `organisation`, `region` |
| Object types | `country` **(primary)**, `organisation`, `region` |
| Direction | Subject imports from Object |

**Example statements this should capture:**
- "Japan imported 15,000 tonnes of cobalt from the DRC" → IMPORTS(JPN, COD)
- "The EU imported 98% of its rare earths from China" → IMPORTS(eu_27, CHN)
- "Tesla sourced lithium hydroxide from Ganfeng" → IMPORTS(Tesla, Ganfeng) (or use SUPPLIES)

| Attribute | Type | Required | Controlled vocabulary | Notes |
|---|---|---|---|---|
| commodity | string | Yes | Mineral canonical names | What is being imported |
| form | string | No | See mineral forms | e.g., `lithium_carbonate`, `copper_concentrate` |
| volume | numeric | No | — | |
| unit | string | Yes (if volume present) | See units | |
| value | numeric | No | — | Trade value |
| currency | string | Yes (if value present) | ISO 4217 | |
| year | integer | Yes | — | |
| share_percent | numeric | No | — | Share of importer's total imports of this commodity |
| share_scope | string | No | — | e.g., "total imports", "imports from this source" |

---

## 5. EXPORTS

An entity exports a commodity to another entity.

| Field | Specification |
|---|---|
| Subject types | `country` **(primary)**, `organisation`, `region` |
| Object types | `country` **(primary)**, `organisation`, `region` |
| Direction | Subject exports to Object |

**Example statements this should capture:**
- "Chile exported 180,000 tonnes of lithium carbonate" → EXPORTS(CHL, ...)
- "Indonesia's nickel ore export ban took effect in 2020" → could be EXPORTS or REGULATES depending on framing
- "Glencore shipped 27kt of cobalt to customers in Asia" → EXPORTS(Glencore, asia_pacific)

| Attribute | Type | Required | Controlled vocabulary | Notes |
|---|---|---|---|---|
| commodity | string | Yes | Mineral canonical names | |
| form | string | No | See mineral forms | |
| volume | numeric | No | — | |
| unit | string | Yes (if volume present) | See units | |
| value | numeric | No | — | |
| currency | string | Yes (if value present) | ISO 4217 | |
| year | integer | Yes | — | |
| share_percent | numeric | No | — | Share of exporter's total exports of this commodity |
| share_scope | string | No | — | |

---

## 6. SUPPLIES / TRADES

A general supply or trade relationship between any two entities. Use this when the relationship is about commercial supply and doesn't fit neatly into IMPORTS/EXPORTS (which are country-level trade flow concepts).

| Field | Specification |
|---|---|
| Subject types | `organisation` **(primary)**, `country`, `facility`, `region` |
| Object types | `organisation` **(primary)**, `country`, `facility`, `region` |
| Direction | Subject supplies/trades to Object |

**Example statements this should capture:**
- "Ganfeng supplies lithium hydroxide to Tesla" → SUPPLIES(Ganfeng, Tesla)
- "SQM signed a long-term offtake with LG Energy Solution" → SUPPLIES(SQM, LG Energy Solution)
- "The Greenbushes mine ships spodumene to Chinese converters" → SUPPLIES(Greenbushes, CHN)

| Attribute | Type | Required | Controlled vocabulary | Notes |
|---|---|---|---|---|
| commodity | string | Yes | Mineral canonical names or product canonical names | |
| form | string | No | See mineral forms | |
| volume | numeric | No | — | |
| unit | string | Yes (if volume present) | See units | |
| value | numeric | No | — | |
| currency | string | Yes (if value present) | ISO 4217 | |
| time_period | string | No | — | e.g., "2023", "Q3 2023", "2020-2023" |
| contract_type | string | No | `spot`, `long_term`, `offtake`, `tolling`, `joint_venture`, `swap` | |
| contract_duration | string | No | — | e.g., "5 years", "2024-2029" |

---

## 7. OPERATES

An entity operates a facility or project.

| Field | Specification |
|---|---|
| Subject types | `organisation` **(primary)**, `country` |
| Object types | `facility` **(primary)** |
| Direction | Subject operates Object |

**Example statements this should capture:**
- "Albemarle operates the Kemerton lithium hydroxide plant" → OPERATES(Albemarle, Kemerton)
- "Indian Rare Earths Limited, a government company, operates the OSCOM plant in Odisha" → OPERATES(IREL, OSCOM)
- "The Indian government operates monazite processing facilities through IREL" → OPERATES(IND, ...) — though typically the government-owned company is the operator

| Attribute | Type | Required | Controlled vocabulary | Notes |
|---|---|---|---|---|
| ownership_percent | numeric | No | — | 0-100 |
| role | string | No | `operator`, `joint_venture_partner`, `minority_stakeholder`, `managing_partner`, `non_operating_partner` | |
| start_date | string | No | — | ISO 8601 date or year |
| end_date | string | No | — | If the operation has ended |
| status | string | No | `active`, `under_construction`, `suspended`, `decommissioned`, `planned` | Current operating status |

---

## 8. LOCATED_IN

An entity is located in a country or region.

| Field | Specification |
|---|---|
| Subject types | `facility` **(primary)**, `organisation` |
| Object types | `country` **(primary)**, `region` |
| Direction | Subject is located in Object |

**Example statements this should capture:**
- "The Greenbushes mine is in Western Australia" → LOCATED_IN(Greenbushes, AUS)
- "BHP is headquartered in Melbourne, Australia" → LOCATED_IN(BHP, AUS)
- "Pensana's Saltend refinery is in the Humber region, UK" → LOCATED_IN(Saltend, GBR)

| Attribute | Type | Required | Controlled vocabulary | Notes |
|---|---|---|---|---|
| sub_national_region | string | No | — | Province, state, or district (free text) |
| location_type | string | No | `headquarters`, `registered_office`, `operational_site`, `project_site` | Clarifies what kind of location this is, especially for organisations |
| coordinates | object | No | — | `{lat, lon}` if available |

---

## 9. OWNS / HAS_STAKE_IN

An entity owns or holds a stake in another entity.

| Field | Specification |
|---|---|
| Subject types | `organisation` **(primary)**, `country` |
| Object types | `organisation` **(primary)**, `facility` |
| Direction | Subject owns/holds stake in Object |

**Example statements this should capture:**
- "Tianqi Lithium owns 26% of Greenbushes" → OWNS(Tianqi, Greenbushes)
- "The DRC government holds a 20% stake in Tenke Fungurume" → OWNS(COD, Tenke Fungurume)
- "Vedanta Resources controls Hindustan Zinc through a 64.9% stake" → OWNS(Vedanta, Hindustan Zinc)
- "Tata Steel acquired Corus Group in 2007" → OWNS(Tata Steel, Corus)

| Attribute | Type | Required | Controlled vocabulary | Notes |
|---|---|---|---|---|
| ownership_percent | numeric | No | — | 0-100; `null` if "owns" but percentage not stated |
| acquisition_date | string | No | — | ISO 8601 date or year |
| transaction_value | numeric | No | — | |
| currency | string | No | ISO 4217 | |
| stake_type | string | No | `majority`, `minority`, `joint_venture`, `wholly_owned`, `strategic`, `controlling` | |
| status | string | No | `current`, `divested`, `pending_approval` | |

---

## 10. SUBSIDIARY_OF

An organisation is a subsidiary or division of a parent organisation. Captures corporate hierarchy.

| Field | Specification |
|---|---|
| Subject types | `organisation` |
| Object types | `organisation` |
| Direction | Subject is a subsidiary of Object |

**Example statements this should capture:**
- "Hindustan Zinc is a subsidiary of Vedanta Resources" → SUBSIDIARY_OF(Hindustan Zinc, Vedanta)
- "IREL is a government enterprise under the Department of Atomic Energy" → SUBSIDIARY_OF(IREL, Dept of Atomic Energy India)
- "LG Energy Solution was spun off from LG Chem" → SUBSIDIARY_OF(LG Energy Solution, LG Chem) + additional context

| Attribute | Type | Required | Controlled vocabulary | Notes |
|---|---|---|---|---|
| parent_ownership_percent | numeric | No | — | Parent's stake in subsidiary |
| relationship_type | string | No | `wholly_owned_subsidiary`, `majority_owned_subsidiary`, `division`, `joint_venture_entity`, `associated_company`, `state_owned_enterprise` | |
| since | string | No | — | When the relationship started |

---

## 11. PARTNERS_WITH

Two entities have a partnership, joint venture, or strategic alliance. Bidirectional.

| Field | Specification |
|---|---|
| Subject types | `organisation` **(primary)**, `country` |
| Object types | `organisation` **(primary)**, `country` |
| Direction | Bidirectional (Subject and Object are partners) |

**Example statements this should capture:**
- "Shenghe Resources and MP Materials have a strategic partnership" → PARTNERS_WITH(Shenghe, MP Materials)
- "India and Australia signed a critical minerals partnership agreement" → PARTNERS_WITH(IND, AUS)
- "KABIL entered a joint venture with an Argentine lithium company" → PARTNERS_WITH(KABIL, ...)

| Attribute | Type | Required | Controlled vocabulary | Notes |
|---|---|---|---|---|
| partnership_type | string | No | `joint_venture`, `strategic_alliance`, `offtake_agreement`, `technology_licence`, `bilateral_agreement`, `mou` | |
| commodity | string | No | Mineral canonical names | What the partnership concerns |
| start_date | string | No | — | |
| end_date | string | No | — | |
| scope | string | No | — | Free text describing what the partnership covers |

---

## 12. REGULATES / RESTRICTS

An entity (policy, country, or institution) regulates, restricts, or incentivises an activity, commodity, or entity.

| Field | Specification |
|---|---|
| Subject types | `policy` **(primary)**, `country` **(primary)**, `organisation` |
| Object types | `mineral` **(primary)**, `country`, `organisation`, `technology`, `product`, `facility` |
| Direction | Subject regulates/restricts Object |

**Example statements this should capture:**
- "The EU Critical Raw Materials Act sets recycling targets for battery materials" → REGULATES(EU CRM Act, lithium)
- "China restricted rare earth exports in 2010" → REGULATES(CHN, rare_earth_elements)
- "Indonesia banned nickel ore exports" → REGULATES(IDN, nickel)
- "India designated lithium as a critical mineral in 2023" → REGULATES(IND, lithium)
- "The US Inflation Reduction Act provides subsidies for domestic battery production" → REGULATES(US IRA, battery_cell)

| Attribute | Type | Required | Controlled vocabulary | Notes |
|---|---|---|---|---|
| regulation_type | string | No | `export_control`, `export_ban`, `import_tariff`, `import_quota`, `environmental_standard`, `strategic_reserve`, `licensing_requirement`, `sanctions`, `subsidy`, `tax_incentive`, `domestic_processing_requirement`, `critical_mineral_designation`, `resource_nationalism` | |
| effective_date | string | No | — | ISO 8601 |
| expiry_date | string | No | — | If time-limited |
| scope | string | No | — | Free text describing what aspect is regulated |
| jurisdiction | string | No | ISO alpha-3 | Country that enacted the regulation |
| impact_description | string | No | — | Free text summary of the regulation's impact |

---

## 13. PROCESSES_AT_STAGE

An entity processes a mineral at a specific supply chain stage. Captures the what-happens-where of the value chain.

| Field | Specification |
|---|---|
| Subject types | `facility` **(primary)**, `organisation` **(primary)**, `country` |
| Object types | `mineral` **(primary)**, `product` |
| Direction | Subject processes Object |

**Example statements this should capture:**
- "The Kwinana plant converts spodumene to lithium hydroxide" → PROCESSES_AT_STAGE(Kwinana, lithium)
- "Ganfeng Lithium refines lithium carbonate and hydroxide" → PROCESSES_AT_STAGE(Ganfeng, lithium)
- "China refines over 60% of global cobalt" → PROCESSES_AT_STAGE(CHN, cobalt)
- "BTR produces anode material from natural and synthetic graphite" → PROCESSES_AT_STAGE(BTR, graphite)

| Attribute | Type | Required | Controlled vocabulary | Notes |
|---|---|---|---|---|
| supply_chain_stage | string | Yes | See [controlled_vocabularies.md](controlled_vocabularies.md) | |
| input_form | string | No | See mineral forms | What form enters the process |
| output_form | string | No | See mineral forms | What form leaves the process |
| capacity | numeric | No | — | Processing capacity |
| capacity_unit | string | No | See units | |
| capacity_type | string | No | `actual`, `nameplate`, `planned`, `under_construction` | |
| share_percent | numeric | No | — | e.g., "processes 60% of global cobalt" |
| share_scope | string | No | — | e.g., "global", "regional" |
| year | integer | No | — | |

---

## 14. USES_TECHNOLOGY

An entity uses a specific technology or process.

| Field | Specification |
|---|---|
| Subject types | `facility` **(primary)**, `organisation`, `country` |
| Object types | `technology` |
| Direction | Subject uses Object |

**Example statements this should capture:**
- "The Kwinana plant uses the Siemens process" → USES_TECHNOLOGY(Kwinana, siemens_process)
- "GCL Technology pioneered FBR granular polysilicon" → USES_TECHNOLOGY(GCL, fbr_process)
- "Indonesian HPAL plants use high-pressure acid leaching" → USES_TECHNOLOGY(IDN, hpal)

| Attribute | Type | Required | Controlled vocabulary | Notes |
|---|---|---|---|---|
| application | string | No | — | What the technology is applied to (e.g., "lithium extraction", "cobalt recovery") |
| status | string | No | `commercial`, `pilot`, `demonstration`, `research`, `planned` | Technology readiness |
| year | integer | No | — | When adoption started or was reported |
| scale | string | No | — | e.g., "10,000 tpa", "commercial scale" |

---

## 15. INVESTS_IN

An entity invests in another entity, project, or technology.

| Field | Specification |
|---|---|
| Subject types | `organisation` **(primary)**, `country` **(primary)**, `facility` |
| Object types | `facility` **(primary)**, `organisation` **(primary)**, `technology`, `mineral` |
| Direction | Subject invests in Object |

**Example statements this should capture:**
- "Tesla invested $3.6B in a Nevada lithium refinery" → INVESTS_IN(Tesla, Nevada refinery)
- "India allocated $1.8B for critical mineral exploration" → INVESTS_IN(IND, lithium) or INVESTS_IN(IND, exploration)
- "The UK government funded Pensana's Saltend REE refinery" → INVESTS_IN(GBR, Saltend)
- "KABIL signed agreements for lithium and cobalt assets overseas" → INVESTS_IN(KABIL, lithium)

| Attribute | Type | Required | Controlled vocabulary | Notes |
|---|---|---|---|---|
| investment_amount | numeric | No | — | |
| currency | string | Yes (if amount present) | ISO 4217 | |
| year | integer | No | — | |
| investment_type | string | No | `equity`, `debt`, `grant`, `offtake_prepayment`, `government_subsidy`, `exploration_spend`, `capex`, `r_and_d` | |
| project_name | string | No | — | |
| investment_stage | string | No | `exploration`, `feasibility`, `construction`, `expansion`, `acquisition` | |

---

## 16. DEPENDS_ON

An entity depends on a mineral, product, technology, or another entity. Captures dependency and criticality relationships.

| Field | Specification |
|---|---|
| Subject types | `product` **(primary)**, `technology` **(primary)**, `country`, `organisation`, `facility` |
| Object types | `mineral` **(primary)**, `product`, `technology`, `country`, `organisation` |
| Direction | Subject depends on Object |

**Example statements this should capture:**
- "NMC811 cathodes require 80% nickel content" → DEPENDS_ON(nmc_cathode, nickel)
- "Japan depends on imports for 100% of its cobalt" → DEPENDS_ON(JPN, cobalt)
- "The Kwinana plant depends on spodumene from Greenbushes" → DEPENDS_ON(Kwinana, Greenbushes)
- "CdTe solar PV depends on tellurium, which is a copper refining byproduct" → DEPENDS_ON(cdte_solar_module, tellurium)
- "DLE technology depends on sorbent availability" → DEPENDS_ON(dle, ...)
- "India's battery ambitions depend on securing overseas lithium" → DEPENDS_ON(IND, lithium)

| Attribute | Type | Required | Controlled vocabulary | Notes |
|---|---|---|---|---|
| quantity_per_unit | numeric | No | — | e.g., kg of lithium per kWh battery capacity |
| unit | string | No | — | Unit for quantity_per_unit |
| product_unit | string | No | — | What "per unit" means (per vehicle, per kWh, per module) |
| substitutability | string | No | `none`, `limited`, `moderate`, `high` | How easily the dependency can be substituted |
| import_dependency_percent | numeric | No | — | For country-level import dependency |
| criticality | string | No | `low`, `medium`, `high`, `critical` | How critical the dependency is |
| year | integer | No | — | |

---

## 17. PRICES

Temporal price data for a mineral or product.

| Field | Specification |
|---|---|
| Subject types | `mineral` **(primary)**, `product` |
| Object types | (none — this is a unary temporal attribute) |
| Direction | N/A |

**Example statements this should capture:**
- "Lithium carbonate spot price reached $78,000/t in November 2022" → PRICES(lithium)
- "Battery cell prices averaged $139/kWh in 2023" → PRICES(battery_cell)
- "Tellurium prices rose to $100/kg" → PRICES(tellurium)

| Attribute | Type | Required | Controlled vocabulary | Notes |
|---|---|---|---|---|
| price | numeric | Yes | — | |
| currency | string | Yes | ISO 4217 | |
| per_unit | string | Yes | See units | e.g., `USD/tonne`, `USD/kg`, `USD/lb`, `USD/kWh` |
| form | string | No | See mineral forms | Which form is priced (e.g., `lithium_carbonate`, `nickel_sulphate`) |
| price_type | string | No | `spot`, `contract`, `average_annual`, `average_quarterly`, `average_monthly`, `futures`, `assessed`, `indicative` | |
| date | string | Yes | — | ISO 8601 date, month (YYYY-MM), or year (YYYY) |
| exchange | string | No | `LME`, `CME`, `SGX`, `SHFE`, `DCE` | If exchange-traded |
| source_assessment | string | No | — | e.g., "Fastmarkets MB", "Benchmark Mineral Intelligence", "Asian Metal" |
| price_trend | string | No | `rising`, `falling`, `stable`, `volatile` | Qualitative trend if stated |

---

## 18. MEMBER_OF

A mineral species belongs to a mineral group. Structural relationship (no temporal attributes).

| Field | Specification |
|---|---|
| Subject types | `mineral` (species level) |
| Object types | `mineral` (group level) |
| Direction | Subject is a member of Object |

| Attribute | Type | Required | Controlled vocabulary | Notes |
|---|---|---|---|---|
| sub_group | string | No | `lree`, `hree` (for REEs) | Optional sub-classification |

---

## 19. EMPLOYS

An entity employs workers.

| Field | Specification |
|---|---|
| Subject types | `organisation` **(primary)**, `facility`, `country` |
| Object types | (none — unary attribute) |
| Direction | N/A |

**Example statements this should capture:**
- "Glencore employs 135,000 people globally" → EMPLOYS(Glencore)
- "The Greenbushes mine employs 1,500 workers" → EMPLOYS(Greenbushes)
- "The Indian mining sector employs over 500,000 people" → EMPLOYS(IND)

| Attribute | Type | Required | Controlled vocabulary | Notes |
|---|---|---|---|---|
| headcount | integer | Yes | — | |
| year | integer | Yes | — | |
| employment_type | string | No | `direct`, `contractor`, `total`, `full_time`, `part_time` | |
| skill_category | string | No | — | Free text |
| sector | string | No | — | For country-level employment, which sector |

---

## 20. EMITS

Environmental impact data for an entity.

| Field | Specification |
|---|---|
| Subject types | `facility` **(primary)**, `organisation` **(primary)**, `technology`, `country` |
| Object types | (none — unary attribute) |
| Direction | N/A |

**Example statements this should capture:**
- "The Kalgoorlie smelter emits 2.4 tCO2 per tonne of nickel" → EMITS(Kalgoorlie)
- "Glencore's total Scope 1+2 emissions were 23 MtCO2e" → EMITS(Glencore)
- "HPAL processing uses 35 m3 of water per tonne of nickel" → EMITS(hpal)
- "China's copper smelting sector emits 3.5 tCO2 per tonne" → EMITS(CHN)

| Attribute | Type | Required | Controlled vocabulary | Notes |
|---|---|---|---|---|
| emission_type | string | Yes | `co2`, `co2e`, `water_usage`, `water_consumption`, `energy_consumption`, `electricity_consumption`, `waste_generated`, `tailings`, `acid_mine_drainage`, `particulates`, `sox`, `nox` | |
| value | numeric | Yes | — | |
| unit | string | Yes | — | e.g., `tCO2/t_product`, `m3/t`, `kWh/t`, `MtCO2e` (absolute) |
| intensity_or_absolute | string | No | `intensity`, `absolute` | Whether the value is per-unit (intensity) or total (absolute) |
| intensity_basis | string | No | — | If intensity: what "per unit" refers to (e.g., "per tonne of copper cathode") |
| year | integer | No | — | |
| scope | string | No | `scope_1`, `scope_2`, `scope_3`, `scope_1_2`, `scope_1_2_3`, `total` | GHG protocol scopes |
| mineral_context | string | No | Mineral canonical names | Which mineral's production this emission relates to |

---

## 21. CONTRADICTS

Links two records that contain conflicting information. Created by the confidence/validation agent (Agent 7). System relationship.

| Field | Specification |
|---|---|
| Subject types | Any record |
| Object types | Any record |
| Direction | Bidirectional (both records are "in conflict") |

| Attribute | Type | Required | Controlled vocabulary | Notes |
|---|---|---|---|---|
| conflict_type | string | Yes | `value_mismatch`, `unit_mismatch`, `temporal_mismatch`, `scope_mismatch`, `attribution_mismatch`, `form_mismatch` | |
| value_a | string | No | — | The conflicting value from record A |
| value_b | string | No | — | The conflicting value from record B |
| resolution_status | string | Yes | `unresolved`, `resolved_a_preferred`, `resolved_b_preferred`, `resolved_both_valid`, `resolved_different_scope` | |
| resolution_notes | string | No | — | Human or agent explanation |

---

## 22. EXTRACTED_FROM (Provenance)

Links any extracted data node back to its source entity and document. System relationship created by the pipeline, not extracted from documents.

| Field | Specification |
|---|---|
| Subject types | Any extracted node (relationship, tag, data point) |
| Object types | `document`, `entity`, `chunk` |
| Direction | Subject was extracted from Object |

| Attribute | Type | Required | Controlled vocabulary | Notes |
|---|---|---|---|---|
| document_id | string | Yes | — | |
| entity_id | string | No | — | |
| chunk_id | string | No | — | |
| page | integer | No | — | |
| extraction_type | string | Yes | `direct`, `inferred` | |
| extraction_method | string | No | See [controlled_vocabularies.md](controlled_vocabularies.md) | |

---

## Relationship extraction guidance

### Direct vs inferred relationships

- **Direct**: The relationship and its key attributes are explicitly stated in the source text. Example: "Australia produced 86,000 tonnes of lithium in 2023" → PRODUCES(AUS, lithium, volume=86000, unit=tonnes, year=2023, extraction_type=direct).
- **Inferred**: The relationship or a specific attribute is derived from context, calculation, or implication. Example: "Australia remained the world's leading lithium producer" → PRODUCES(AUS, lithium, rank=1, extraction_type=inferred). The rank is inferred from "leading."

### Multi-relationship extraction from tables

A single table row often generates multiple relationships. Example: a row in a "World Production" table with columns [Country, 2022 Production, 2023 Production, Reserves] generates:
- PRODUCES(country, mineral, volume=X, year=2022)
- PRODUCES(country, mineral, volume=Y, year=2023)
- RESERVES(country, mineral, volume=Z)

### Multi-relationship extraction from a single sentence

A single sentence may yield multiple relationships. Example: "Albemarle, the world's largest lithium producer, operates the Kemerton hydroxide plant in Western Australia" yields:
- PRODUCES(Albemarle, lithium, rank=1) — inferred from "world's largest"
- OPERATES(Albemarle, Kemerton)
- LOCATED_IN(Kemerton, AUS, sub_national_region="Western Australia")
- PROCESSES_AT_STAGE(Kemerton, lithium, stage=refining_smelting, output_form=lithium_hydroxide)

### Choosing between overlapping relationship types

Some statements could fit multiple relationship types. Guidelines:
- **Country-level trade data** (e.g., customs statistics) → use IMPORTS/EXPORTS.
- **Company-to-company commercial relationships** → use SUPPLIES/TRADES.
- **"X produces Y"** where X is a country, company, or facility → use PRODUCES.
- **"X consumes/uses/demands Y"** → use CONSUMES.
- **"X processes Y into Z"** → use PROCESSES_AT_STAGE (captures the transformation).
- **Ownership vs operation**: "X owns Y" → OWNS. "X operates Y" → OPERATES. Many facilities have both — extract both relationships.
- When genuinely ambiguous, extract the most specific applicable type and note the ambiguity.

### Handling ambiguous scope

When the scope of a relationship is ambiguous (e.g., "China dominates rare earth production" — does this mean mining, refining, or both?), extract what is stated and use the `supply_chain_stage` attribute or a qualifier to capture the ambiguity. Do not invent specificity that isn't in the source.

### Handling aggregate vs specific entities

Documents often make statements at different levels of specificity:
- "China produces 60% of graphite" → PRODUCES(CHN, graphite) — country level
- "BTR is the largest anode material producer" → PRODUCES(BTR, graphite_anode) — company + product level

Both are valid. Do not force aggregation or disaggregation. Extract at the level stated in the source. The graph database handles multi-level querying through entity linkages (LOCATED_IN, SUBSIDIARY_OF, MEMBER_OF).
