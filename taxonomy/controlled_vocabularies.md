# Controlled Vocabularies

## Version 0.1.0

This document defines all controlled vocabularies (enumerations) used by the pipeline. When tagging or extracting data, agents must use values from these lists. Unrecognised values trigger the taxonomy evolution mechanism.

---

## 1. Supply chain stages

The end-to-end critical mineral supply chain, from resource to recovery. A mineral or facility is tagged with one or more of these stages.

| Canonical name | Display name | Description | Typical facility types |
|---|---|---|---|
| `exploration` | Exploration | Geological survey, prospecting, resource delineation | Exploration sites, drill sites |
| `mining_extraction` | Mining / Extraction | Physical removal of ore from the ground | Open-pit mines, underground mines, brine ponds, DLE plants |
| `beneficiation_concentration` | Beneficiation / Concentration | Upgrading ore to concentrate; removing gangue | Concentrators, flotation plants, dense media separation |
| `refining_smelting` | Refining / Smelting | Converting concentrate to refined metal or chemical product | Smelters, refineries, SX-EW plants, HPAL plants |
| `precursor_production` | Precursor Production | Manufacturing chemical precursors for end-use applications | pCAM plants (battery precursors), chemical plants |
| `component_manufacturing` | Component Manufacturing | Producing components from refined materials | Cathode plants, anode plants, magnet factories, wafer fabs |
| `product_assembly` | Product Assembly / Integration | Assembling components into final products | Battery cell/pack assembly, EV assembly, electronics assembly |
| `use_deployment` | Use / Deployment | In-service use of the final product | (not a facility type; captures demand-side data) |
| `collection_end_of_life` | Collection / End-of-Life | Collecting used products for recycling or disposal | Collection points, dismantling centres |
| `recycling_recovery` | Recycling / Recovery | Recovering materials from end-of-life products or waste | Recycling plants, hydrometallurgical recovery, pyrometallurgical recovery |
| `trading_logistics` | Trading / Logistics | Physical trading, storage, and transportation of materials | Trading houses, warehouses, ports, LME warehouses |

### Tagging rules for supply chain stages

- A **facility** is tagged with the stage(s) at which it operates. A vertically integrated facility may span multiple stages (e.g., a mine with an on-site concentrator → `mining_extraction` + `beneficiation_concentration`).
- A **data point** (e.g., a production figure) is tagged with the stage it describes. "Mine production" → `mining_extraction`. "Refined output" → `refining_smelting`.
- When the stage is ambiguous (e.g., "production" without further context), use the most specific stage inferable from context. If truly ambiguous, tag as `mining_extraction` for raw mineral data (this is the most common default in industry reports) and flag for review.

---

## 2. Source types

Classification of document sources. Determines the default reliability weight used by the confidence scoring agent (Agent 7).

| Canonical name | Display name | Default reliability weight | Notes |
|---|---|---|---|
| `government_report` | Government Report | 0.95 | USGS MCS, BGS World Mineral Production, GSI bulletins, Ministry of Mines annual reports |
| `academic_paper` | Academic Paper | 0.90 | Peer-reviewed journals, conference proceedings |
| `trade_statistics` | Trade Statistics | 0.90 | UN Comtrade, national customs data, ITC Trade Map |
| `technical_standard` | Technical Standard | 0.85 | JORC, NI 43-101, ISO standards |
| `policy_document` | Policy Document | 0.85 | Legislation, white papers, strategy documents (e.g., EU CRM Act, India Critical Minerals Strategy) |
| `company_annual_report` | Company Annual Report | 0.80 | Annual reports, 10-K filings, ASX announcements |
| `company_technical_report` | Company Technical Report | 0.78 | NI 43-101 technical reports, feasibility studies, scoping studies |
| `industry_analysis` | Industry Analysis | 0.75 | Reports from consultancies, think tanks, industry bodies |
| `market_report` | Market Report | 0.70 | Benchmark Minerals, Fastmarkets, CRU, Roskill/Wood Mackenzie |
| `patent` | Patent | 0.70 | Technology/process patents |
| `conference_presentation` | Conference Presentation | 0.65 | Industry conference slides, investor presentations |
| `news_article` | News Article | 0.55 | Reuters, Bloomberg, Mining.com, trade press |
| `blog_or_commentary` | Blog / Commentary | 0.40 | Opinion pieces, blog posts, social media (included only if cited in a formal document) |

### Source type assignment rules

- The document intake agent (Agent 1) assigns the source type during metadata extraction.
- If a document doesn't fit any category, use `industry_analysis` as the default and flag for review.
- A single document may contain content of varying reliability (e.g., a news article quoting USGS data). The source type applies to the *document*, not the individual data point. Specific data points that cite a more authoritative source can have their confidence adjusted upward by the validation agent.

---

## 3. Capacity types

Distinguishes between different meanings of "capacity" or "production."

| Canonical name | Display name | Description |
|---|---|---|
| `actual` | Actual | Realised production or throughput in a given period |
| `nameplate` | Nameplate | Designed/rated capacity of a facility |
| `effective` | Effective | Realistic operating capacity (accounting for downtime, maintenance) |
| `planned` | Planned | Announced future capacity (approved, funded, or in feasibility) |
| `under_construction` | Under Construction | Facility currently being built |
| `suspended` | Suspended | Capacity that exists but is temporarily offline |
| `decommissioned` | Decommissioned | Capacity that has been permanently closed |

---

## 4. Price types

Distinguishes between different price reporting bases.

| Canonical name | Display name | Description |
|---|---|---|
| `spot` | Spot | Current market price for immediate delivery |
| `contract` | Contract | Negotiated price under a supply agreement |
| `average_annual` | Average (Annual) | Average price over a calendar year |
| `average_quarterly` | Average (Quarterly) | Average price over a calendar quarter |
| `average_monthly` | Average (Monthly) | Average price over a calendar month |
| `futures` | Futures | Price of a futures contract (specify delivery month) |
| `assessed` | Assessed | Price assessed by a price reporting agency (PRA) |
| `indicative` | Indicative | Non-binding price estimate or quotation |

---

## 5. Reserve and resource classifications

Based on CRIRSCO-aligned reporting codes (JORC, NI 43-101, SAMREC, etc.).

| Canonical name | Display name | Confidence level | Notes |
|---|---|---|---|
| `measured` | Measured (Mineral Resource) | Highest | Sufficient drilling/sampling for high confidence in tonnage and grade |
| `indicated` | Indicated (Mineral Resource) | Medium | Reasonable confidence; less drilling than measured |
| `inferred` | Inferred (Mineral Resource) | Lowest (resource) | Low confidence; estimated from limited data |
| `proved` | Proved (Ore Reserve) | Highest (reserve) | Economically mineable portion of measured resource |
| `probable` | Probable (Ore Reserve) | Medium (reserve) | Economically mineable portion of indicated resource |
| `unspecified` | Unspecified | Unknown | Source does not distinguish classification |

### Usage note

"Reserves" and "resources" are distinct concepts. Reserves are the economically extractable subset of resources. Many documents (including USGS MCS) use "reserves" loosely. The pipeline stores whatever term the source uses and tags the classification accordingly. If the source says "reserves" without further qualification, use `unspecified`.

---

## 6. Extraction types

How a data point was obtained from the source document.

| Canonical name | Display name | Description |
|---|---|---|
| `direct` | Direct | The value is explicitly stated in the source text, table, or chart label |
| `inferred` | Inferred | The value is derived, calculated, implied, or interpolated from the source |

---

## 7. Extraction methods (for chart/vision data)

How a numeric value was read from a chart or figure by the vision interpretation agent.

| Canonical name | Display name | Confidence modifier | Description |
|---|---|---|---|
| `direct_label_read` | Direct Label Read | +0.15 | Value explicitly printed on or beside the data point |
| `estimated_from_bar_height` | Estimated from Bar Height | 0.00 (baseline) | Interpolated from bar height against axis scale |
| `estimated_from_line_position` | Estimated from Line Position | 0.00 | Interpolated from line/point position against axis scale |
| `estimated_from_area` | Estimated from Area | -0.10 | Inferred from area proportion (pie charts, treemaps) |
| `estimated_from_annotation` | Estimated from Annotation | +0.10 | Read from a text annotation on the chart |
| `read_from_data_table` | Read from Data Table | +0.15 | Chart accompanied by a data table; value read from table |

---

## 8. Data qualifiers

Qualifiers found in tables and text indicating data reliability or status.

| Canonical name | Display name | Common symbols in source | Description |
|---|---|---|---|
| `estimated` | Estimated | e, est., E, (e), estimated | Value is an estimate, not a confirmed measurement |
| `withheld` | Withheld | W, w, —, --, n.a. (context-dependent) | Value suppressed to protect proprietary data |
| `revised` | Revised | r, R, rev., revised | Value has been revised from a previously published figure |
| `preliminary` | Preliminary | p, P, prelim., preliminary | Value is preliminary and subject to revision |
| `not_available` | Not Available | NA, N/A, n.a., .., ... | Data not available |
| `zero` | Zero or negligible | —, -, 0, nil, neg. | Production is zero or too small to report |
| `included_elsewhere` | Included Elsewhere | XX, incl., included in [country] | Data is included in another country's or category's total |

### Parsing priority

When a table cell contains both a number and a qualifier symbol (e.g., "86,000e"), extract the number (86000) and tag with the qualifier (`estimated`). The qualifier is stored as metadata on the data point, not as a replacement for the value.

---

## 9. Facility types

Classification of physical sites in the supply chain.

| Canonical name | Display name | Typical stages |
|---|---|---|
| `open_pit_mine` | Open-pit Mine | mining_extraction |
| `underground_mine` | Underground Mine | mining_extraction |
| `brine_operation` | Brine Operation | mining_extraction |
| `dle_plant` | Direct Lithium Extraction (DLE) Plant | mining_extraction |
| `concentrator` | Concentrator / Beneficiation Plant | beneficiation_concentration |
| `smelter` | Smelter | refining_smelting |
| `refinery` | Refinery | refining_smelting |
| `hpal_plant` | HPAL Plant | refining_smelting |
| `sx_ew_plant` | SX-EW Plant | refining_smelting |
| `precursor_plant` | Precursor Plant (pCAM/CAM) | precursor_production |
| `cathode_plant` | Cathode Active Material Plant | component_manufacturing |
| `anode_plant` | Anode Material Plant | component_manufacturing |
| `magnet_factory` | Permanent Magnet Factory | component_manufacturing |
| `battery_cell_plant` | Battery Cell Plant (Gigafactory) | component_manufacturing, product_assembly |
| `wafer_fab` | Wafer Fabrication Facility | component_manufacturing |
| `recycling_plant` | Recycling Plant | recycling_recovery |
| `port` | Port / Terminal | trading_logistics |
| `warehouse` | Warehouse / Storage | trading_logistics |

---

## 10. Technology / process types [extensible]

Named technologies and processes encountered in supply chain literature.

| Canonical name | Display name | Stage | Minerals | Notes |
|---|---|---|---|---|
| `brine_evaporation` | Solar Brine Evaporation | mining_extraction | lithium | Traditional brine extraction; 12-18 month cycle |
| `dle` | Direct Lithium Extraction (DLE) | mining_extraction | lithium | Emerging technology; multiple sub-types (adsorption, ion exchange, membrane) |
| `hard_rock_mining` | Hard-rock Mining (open-pit/underground) | mining_extraction | lithium, graphite, REE | Conventional mining |
| `froth_flotation` | Froth Flotation | beneficiation_concentration | copper, nickel, graphite | Gravity/chemical separation |
| `dense_media_separation` | Dense Media Separation (DMS) | beneficiation_concentration | lithium (spodumene) | |
| `hpal` | High-Pressure Acid Leaching (HPAL) | refining_smelting | nickel, cobalt | Laterite processing; produces MHP/MSP |
| `rkef` | Rotary Kiln Electric Furnace (RKEF) | refining_smelting | nickel | Laterite → NPI/ferronickel |
| `sx_ew` | Solvent Extraction - Electrowinning (SX-EW) | refining_smelting | copper | Oxide ore processing |
| `flash_smelting` | Flash Smelting | refining_smelting | copper, nickel | Outokumpu process |
| `siemens_process` | Siemens Process | refining_smelting | silicon | TCS-based polysilicon production |
| `fbr_process` | Fluidised Bed Reactor (FBR) | refining_smelting | silicon | Silane-based granular polysilicon |
| `zone_refining` | Zone Refining | refining_smelting | indium, tellurium | High-purity metal production |
| `solvent_extraction` | Solvent Extraction (SX) | refining_smelting | REE, cobalt | Separation of individual REE or Co from mixed solutions |
| `ion_exchange` | Ion Exchange | refining_smelting | REE | REE separation alternative to SX |
| `electrorefining` | Electrorefining | refining_smelting | copper, cobalt, nickel | Electrolytic purification |
| `coprecipitation` | Co-precipitation | precursor_production | nickel, cobalt, manganese | NMC/NCA precursor production (pCAM) |
| `calcination` | Calcination / Sintering | component_manufacturing | lithium, nickel, cobalt | CAM production from pCAM + lithium source |
| `hydrometallurgical_recycling` | Hydrometallurgical Recycling | recycling_recovery | lithium, cobalt, nickel | Acid leaching of battery black mass |
| `pyrometallurgical_recycling` | Pyrometallurgical Recycling | recycling_recovery | cobalt, nickel, copper | Smelting of end-of-life batteries or e-waste |

---

## 11. Product / component types [extensible]

Manufactured items and intermediates commonly referenced in supply chain documents.

| Canonical name | Display name | Key mineral inputs | Notes |
|---|---|---|---|
| `nmc_cathode` | NMC Cathode (Nickel-Manganese-Cobalt) | nickel, manganese, cobalt, lithium | NMC111, NMC532, NMC622, NMC811 variants |
| `nca_cathode` | NCA Cathode (Nickel-Cobalt-Aluminium) | nickel, cobalt, lithium | Tesla/Panasonic chemistry |
| `lfp_cathode` | LFP Cathode (Lithium Iron Phosphate) | lithium | Cobalt-free; dominant in Chinese EVs |
| `lmfp_cathode` | LMFP Cathode (Lithium Manganese Iron Phosphate) | lithium, manganese | Emerging variant of LFP |
| `lco_cathode` | LCO Cathode (Lithium Cobalt Oxide) | lithium, cobalt | Consumer electronics batteries |
| `graphite_anode` | Graphite Anode | graphite | Natural or synthetic graphite |
| `silicon_anode` | Silicon Anode (Si or SiOx composite) | silicon, graphite | Emerging; higher energy density |
| `battery_cell` | Battery Cell | lithium, cobalt, nickel, manganese, graphite | Cylindrical, pouch, or prismatic |
| `battery_pack` | Battery Pack | (aggregated) | Assembled from cells + BMS |
| `ndfeb_magnet` | NdFeB Permanent Magnet | neodymium, praseodymium, dysprosium, terbium | Sintered or bonded |
| `smco_magnet` | SmCo Permanent Magnet | samarium, cobalt | High-temperature applications |
| `cdte_solar_module` | CdTe Thin-Film Solar Module | tellurium | First Solar primary manufacturer |
| `cigs_solar_module` | CIGS Thin-Film Solar Module | indium | Copper-indium-gallium-selenide |
| `mono_si_solar_cell` | Monocrystalline Silicon Solar Cell | silicon | Dominant PV technology |
| `poly_si_solar_cell` | Polycrystalline Silicon Solar Cell | silicon | Legacy PV technology |
| `ev_motor` | EV Traction Motor | neodymium, dysprosium, copper | Permanent magnet synchronous motor (PMSM) |
| `wind_turbine_generator` | Wind Turbine Generator | neodymium, dysprosium, copper | Direct-drive generators use NdFeB magnets |
| `superalloy` | Superalloy | cobalt, nickel | Aerospace and gas turbine applications |
