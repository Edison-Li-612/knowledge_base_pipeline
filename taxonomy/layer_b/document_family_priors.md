# Document Family Priors

## Version 0.1.0

**Layer:** B (Operational Mapping Registry).

Document families are groups of documents from the same source series. Each family carries structural conventions, reporting basis priors, reliability modifiers, and parsing templates that the Layer 2 interpretation services can reference without additional LLM calls.

Layer 1 (document intake, Section 5.2.2) assigns a `document_family` tag during metadata extraction. Layer 2 services query this registry before invoking the LLM, applying known conventions first (deterministic-first principle).

---

## How to read this file

Each family entry has:
- **`family_id`**: Machine-readable ID (e.g., `FAM-BGS-CR`).
- **Structural conventions**: How this source formats tables, what units it uses, what abbreviations appear.
- **Reporting basis priors**: The default metric basis and mineral form for numeric figures in this source.
- **Reliability modifier**: Adjustment to the base source-type reliability weight (positive or negative, e.g., +0.05).
- **Parsing templates**: Verified column header mappings for commonly occurring table structures.

---

## Government and Geological Survey Series

### BGS Commodity Reviews

```yaml
family_id: FAM-BGS-CR
display_name: BGS Commodity Review
source_type: government_report
base_reliability: 0.95
reliability_modifier: 0.00
publisher: British Geological Survey
examples:
  - "BGS Cobalt Commodity Review (Petavratzi et al., 2019)"
  - "BGS Lithium Commodity Review"
structural_conventions:
  - Tables typically use '000 tonnes or metric tonnes (t) for production figures.
  - Country production tables have columns: Country | Year | Production | Unit
  - Reserve tables follow USGS convention (contained metal basis unless otherwise stated).
  - Figures are usually labelled with source (e.g., "Source: USGS, 2018").
reporting_basis_priors:
  production: contained_metal (default; some tables use LCE for lithium)
  reserves: contained_metal (matches USGS MCS convention)
  temporal: calendar_year
known_abbreviations:
  - "e": estimated
  - "p": preliminary
  - "r": revised
  - "n.a.": not available
```

### USGS Mineral Commodity Summaries (MCS)

```yaml
family_id: FAM-USGS-MCS
display_name: USGS Mineral Commodity Summaries
source_type: government_report
base_reliability: 0.95
reliability_modifier: +0.00
publisher: United States Geological Survey
examples:
  - "Mineral Commodity Summaries 2024"
  - "Mineral Commodity Summaries 2023"
structural_conventions:
  - Annual publication; covers ~90 mineral commodities.
  - Production tables: Country | Mine Production (tonnes, 2022 and 2023) | Reserves
  - Units: metric tonnes unless noted. Lithium reported in tonnes of contained lithium metal (NOT LCE).
  - Reserve figures use "tonnes" for contained metal; often rounded to nearest 1,000 t.
  - Data qualifiers in table footnotes: e=estimated, NA=not available, W=withheld.
  - Figures often preceded by "e" in the table cell (e.g., "86,000 e").
reporting_basis_priors:
  production: contained_metal
  reserves: contained_metal
  temporal: calendar_year
  lithium_specific: contained_lithium_metal (NOT LCE — USGS has used Li content since ~2018)
known_abbreviations:
  - "e": estimated
  - "W": withheld (proprietary)
  - "NA": not available
  - "—": zero or negligible
parsing_templates:
  world_production_table:
    typical_headers: ["Country", "Mine production", "Reserves"]
    year_columns: ["2022", "2023"]  # current and prior year
    unit_row: often a header row or footnote below the main header
```

### USGS Minerals Yearbook (MYB)

```yaml
family_id: FAM-USGS-MYB
display_name: USGS Minerals Yearbook
source_type: government_report
base_reliability: 0.95
reliability_modifier: +0.00
publisher: United States Geological Survey
structural_conventions:
  - More detailed than MCS; covers individual countries and industries.
  - Tables often include mine, smelter, and refinery production separately.
  - Units vary by chapter; always read column headers.
  - Figures in short tons (st) for some historical US data — check carefully.
reporting_basis_priors:
  production: contained_metal (but verify per-chapter)
  temporal: calendar_year
```

### UN Comtrade / ITC Trade Map

```yaml
family_id: FAM-UN-COMTRADE
display_name: UN Comtrade / ITC Trade Map
source_type: trade_statistics
base_reliability: 0.90
reliability_modifier: +0.00
publisher: UN Statistics Division / International Trade Centre
structural_conventions:
  - Trade flows by HS code (Harmonised System).
  - Values in USD (thousands); quantities in kg or tonnes depending on HS code.
  - Reporters are individual countries; data is self-reported, then mirrored.
  - HS codes of relevance: 2602 (manganese ore), 2604 (nickel ore), 2613 (cobalt ore),
    2825 (lithium compounds: 282520 Li2O, 282521 Li2CO3), 2846 (REE compounds).
reporting_basis_priors:
  trade_values: USD_thousands (convert to USD at extraction)
  trade_volumes: kg (convert to tonnes at extraction)
  temporal: calendar_year
known_issues:
  - Mirror data discrepancies are common (exporter and importer report different values).
  - Classification errors: some lithium carbonate (282521) misclassified as other Li compounds.
  - Confidential flows reported as zero — cross-check against BGS/USGS where available.
```

---

## Industry and Market Analysis Series

### Benchmark Mineral Intelligence

```yaml
family_id: FAM-BMI
display_name: Benchmark Mineral Intelligence
source_type: market_report
base_reliability: 0.70
reliability_modifier: +0.00
publisher: Benchmark Mineral Intelligence Ltd
structural_conventions:
  - Battery supply chain specialist; strong on Li, Co, Ni, Mn, graphite.
  - Prices reported in USD/tonne or USD/kg depending on commodity.
  - Lithium prices in USD/tonne LCE (not contained metal).
  - Often includes capacity databases for gigafactories and cathode/anode plants.
reporting_basis_priors:
  lithium_production: lithium_carbonate_equivalent
  prices: USD_per_tonne (LCE for lithium)
```

### Fastmarkets MB (formerly Metal Bulletin)

```yaml
family_id: FAM-FASTMARKETS
display_name: Fastmarkets MB
source_type: market_report
base_reliability: 0.70
reliability_modifier: +0.00
publisher: Fastmarkets Ltd
structural_conventions:
  - Price reporting agency (PRA); prices are assessed/indicative.
  - Cobalt prices quoted in USD/lb and USD/tonne.
  - Lithium prices in USD/tonne CIF China or DDP Europe/US.
reporting_basis_priors:
  cobalt_prices: USD_per_lb and USD_per_tonne (both often quoted)
```

---

## Company Report Series

### BHP Annual Report / Operational Review

```yaml
family_id: FAM-BHP-AR
display_name: BHP Annual Report and Operational Review
source_type: company_annual_report
base_reliability: 0.80
reliability_modifier: +0.00
publisher: BHP Group
structural_conventions:
  - Fiscal year ending 30 June (FY format: "FY2023" = Jul 2022 - Jun 2023).
  - Production volumes in kt (kilotonnes) or Mt (megatonnes).
  - Copper reported in kt contained copper; nickel in kt contained nickel.
  - Potash (Jansen project) in Mt.
reporting_basis_priors:
  production: contained_metal
  temporal: fiscal_year_jun (FY2023 = 2022-07 to 2023-06)
```

### Glencore Annual Report

```yaml
family_id: FAM-GLENCORE-AR
display_name: Glencore Annual Report
source_type: company_annual_report
base_reliability: 0.80
reliability_modifier: +0.00
publisher: Glencore plc
structural_conventions:
  - Calendar year reporting.
  - Production in tonnes (t) or kilotonnes (kt).
  - Cobalt production in tonnes of cobalt metal equivalent.
  - Nickel production often includes both contained Ni and finished products.
reporting_basis_priors:
  production: contained_metal
  temporal: calendar_year
```

---

## Policy Documents

### EU Critical Raw Materials Act (CRMA)

```yaml
family_id: FAM-EU-CRMA
display_name: EU Critical Raw Materials Act
source_type: policy_document
base_reliability: 0.85
reliability_modifier: +0.00
publisher: European Commission
structural_conventions:
  - Uses EU-specific criticality metrics: supply risk, economic importance.
  - Lists of "critical raw materials" and "strategic raw materials" are distinct.
  - Import dependency figures in % (percent of EU consumption from a single country).
  - Production/processing figures often for EU27 aggregate.
reporting_basis_priors:
  geographic_scope: EU27 or EU member state
  import_dependency: percentage_of_total_consumption
```

### India National Critical Minerals Strategy

```yaml
family_id: FAM-INDIA-NCMS
display_name: India National Critical Minerals Strategy
source_type: policy_document
base_reliability: 0.85
reliability_modifier: +0.00
publisher: Government of India, Ministry of Mines
structural_conventions:
  - Follows Indian fiscal year (April-March, e.g., FY2022-23).
  - Production figures from IBM (Indian Bureau of Mines) and GSI.
  - Import values in INR crore or USD million.
  - Reserves from GSI National Mineral Inventory.
reporting_basis_priors:
  temporal: fiscal_year_apr (FY2022-23 = 2022-04 to 2023-03)
  currency_default: INR (convert to USD at extraction, note exchange rate assumption)
```

---

## Adding new families

When Layer 1 encounters a document from an unregistered source family, it should:
1. Assign the generic source type (e.g., `government_report`, `market_report`).
2. Emit a Layer C proposal with the new family's apparent conventions.
3. After enough documents from the same source are processed, Layer 4 (Taxonomy Governance) reviews the proposal and adds a new entry here.
