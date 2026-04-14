# Units and Metrics Reference

## Version 0.1.0

This document defines the canonical unit system, metric types, and normalisation rules for the pipeline. Agents use this when parsing numeric values, normalising units, and validating extracted data.

---

## 1. Mass units

The pipeline normalises all mass values to **metric tonnes (t)** as the canonical storage unit. Conversion happens at extraction time; both the original value/unit and the normalised value are stored.

| Canonical name | Display name | Symbol(s) in source | Conversion to tonnes | Notes |
|---|---|---|---|---|
| `tonnes` | Metric tonnes | t, mt (lowercase), tonne, tonnes, metric ton, metric tons | 1.0 | **Canonical unit**. Note: "mt" is ambiguous (could mean megatonnes in some contexts). |
| `kilotonnes` | Kilotonnes | kt, Kt, ktonnes, thousand tonnes, '000 tonnes | 1,000 | Common in production reports |
| `megatonnes` | Megatonnes | Mt, MT, Mtonnes, million tonnes | 1,000,000 | Common in reserves reporting |
| `kilograms` | Kilograms | kg, Kg, kilogram, kilograms | 0.001 | Common for minor metals (Te, In) and per-unit intensities |
| `grams` | Grams | g, gram, grams | 0.000001 | Rare; used for precious metals and some REE |
| `pounds` | Pounds | lb, lbs, pound, pounds | 0.000453592 | Common in US copper, cobalt pricing |
| `short_tons` | Short tons (US) | st, short ton, short tons | 0.907185 | US convention; less common in mineral reporting |
| `long_tons` | Long tons (Imperial) | lt, long ton, long tons | 1.01605 | Older UK convention; rare in modern reports |
| `ounces_troy` | Troy ounces | oz, troy oz, t oz | 0.0000311035 | Precious metals and some PGM/REE contexts |

### Mass unit parsing rules

1. **"mt" ambiguity**: Lowercase "mt" could mean "metric tonnes" (1 t) or "megatonnes" (1,000,000 t). Resolve using context:
   - If the number is small (e.g., "240 mt") and the context is global production of a major mineral → likely megatonnes is wrong; probably metric tonnes or a typo. Flag for review.
   - If the number is very large (e.g., "6.2 mt" for reserves) → likely megatonnes.
   - When truly ambiguous, flag for human review.

2. **"kt" context**: "kt" almost always means kilotonnes in mining/mineral contexts. In precious metals, "kt" could mean karat — but this is distinguishable by context.

3. **Thousands separators**: Documents may use commas (61,000) or periods (61.000) as thousands separators depending on locale. The table numeric parsing agent handles this using locale detection heuristics (see Agent 3b skills).

---

## 2. Volume and liquid units

Less common in mineral reporting but used for brine, water usage, and some chemical processes.

| Canonical name | Display name | Symbol(s) | Notes |
|---|---|---|---|
| `litres` | Litres | L, l, litre, liter | |
| `cubic_metres` | Cubic metres | m3, m^3, cubic metre | Water usage, brine volumes |
| `gallons_us` | US gallons | gal, gallon | Rare in mineral contexts |
| `barrels` | Barrels | bbl | Oil contexts; occasionally for brine |

---

## 3. Currency units

For trade values, investment amounts, and pricing.

| Canonical name | ISO 4217 | Symbol(s) | Notes |
|---|---|---|---|
| `usd` | USD | $, US$, USD | Default assumption when "$" appears without qualifier |
| `eur` | EUR | EUR, euro | |
| `gbp` | GBP | GBP, pound sterling | |
| `cny` | CNY | CNY, RMB, yuan, renminbi | Chinese pricing data |
| `inr` | INR | INR, Rs, rupee | Indian data |
| `aud` | AUD | A$, AUD | Australian mining/export data |
| `cad` | CAD | C$, CAD | Canadian mining data |
| `brl` | BRL | R$, BRL | Brazilian data |
| `clp` | CLP | CLP, Chilean peso | Chilean lithium data |
| `jpy` | JPY | JPY, yen | Japanese data |
| `krw` | KRW | KRW, won | South Korean data |
| `zar` | ZAR | ZAR, rand | South African data |

### Currency parsing rules

- When "$" appears without a country qualifier, assume USD unless the document context strongly indicates otherwise (e.g., an Australian company report using "$" likely means AUD — check the document metadata).
- Store all values in the original currency. Do not convert currencies at extraction time. Currency conversion is a downstream analytical operation, not an extraction operation.

---

## 4. Price units (compound)

Prices are reported as currency per mass unit.

| Common format | Canonical representation | Notes |
|---|---|---|
| USD/t, $/t, $/tonne | `{currency: USD, per_unit: tonnes}` | Most common for bulk minerals |
| USD/kg, $/kg | `{currency: USD, per_unit: kilograms}` | Common for minor metals (Te, In, REE) |
| USD/lb, $/lb | `{currency: USD, per_unit: pounds}` | Common for copper, cobalt (US market) |
| CNY/t, RMB/t | `{currency: CNY, per_unit: tonnes}` | Chinese domestic pricing |
| USD/kWh, $/kWh | `{currency: USD, per_unit: kWh}` | Battery cell pricing |

---

## 5. Percentage and share metrics

| Canonical name | Display name | Description |
|---|---|---|
| `market_share` | Market share | Entity's share of total global/regional market |
| `import_share` | Import share | Share of a country's imports from a specific source |
| `export_share` | Export share | Share of a country's exports to a specific destination |
| `ownership_percent` | Ownership percentage | Stake in a company or facility |
| `recovery_rate` | Recovery rate | Percentage of target material recovered in processing |
| `ore_grade` | Ore grade | Concentration of target mineral in ore (%) |
| `capacity_utilisation` | Capacity utilisation | Actual production as % of nameplate capacity |
| `recycling_rate` | Recycling rate | Percentage of end-of-life material that is recycled |
| `growth_rate` | Growth rate | Year-on-year or period-on-period percentage change |

---

## 6. Temporal units and conventions

| Format | Canonical representation | Example |
|---|---|---|
| Calendar year | `YYYY` (integer) | 2023 |
| Year-month | `YYYY-MM` (string) | 2023-06 |
| Full date | `YYYY-MM-DD` (string, ISO 8601) | 2023-06-15 |
| Quarter | `YYYY-QN` (string) | 2023-Q3 |
| Half-year | `YYYY-HN` (string) | 2023-H1 |
| Date range | `YYYY-YYYY` or `YYYY-MM to YYYY-MM` | 2020-2023, 2023-01 to 2023-06 |
| Fiscal year | `FY-YYYY` (string) | FY-2023 (note: fiscal year boundaries vary by company/country) |

### Temporal parsing rules

1. **Year is the minimum temporal resolution.** If a production figure says "2023", store `year: 2023`. If it says "Q3 2023", store `year: 2023, quarter: 3`.
2. **"Last year" / "previous year"**: Resolve relative to the document's publication date (from Agent 1 metadata). If the document is dated 2024, "last year" = 2023.
3. **Fiscal year ambiguity**: Different countries and companies have different fiscal year boundaries (e.g., India: Apr-Mar; Japan: Apr-Mar; Australia: Jul-Jun; US: Oct-Sep for government, Jan-Dec for most companies). When a source says "FY2023" without specifying boundaries, store the fiscal year label and note the ambiguity. Do not assume calendar year alignment.
4. **Forecast vs historical**: If a figure is a forecast (e.g., "projected 2030 production"), tag with `year: 2030` and add a qualifier: `forecast`. Do not mix forecasts with historical data in the same analytical tables without clear labelling.

---

## 7. Metric types (reporting basis)

The "metric" field on a data point specifies what the number represents in terms of the mineral's form. This is distinct from the unit (which is mass or currency).

| Canonical name | Display name | Applies to | Notes |
|---|---|---|---|
| `contained_metal` | Contained metal | All minerals | The mass of the pure element; default if unspecified |
| `lithium_content` | Lithium content | Lithium | Equivalent to contained_metal for Li |
| `lithium_carbonate_equivalent` | Lithium carbonate equivalent (LCE) | Lithium | See conversion factors |
| `lithium_carbonate` | Lithium carbonate | Lithium | Mass of Li2CO3 product |
| `lithium_hydroxide` | Lithium hydroxide | Lithium | Mass of LiOH-H2O product |
| `spodumene_concentrate` | Spodumene concentrate | Lithium | Mass of concentrate product (specify grade) |
| `cobalt_contained` | Cobalt contained | Cobalt | Mass of Co |
| `nickel_contained` | Nickel contained | Nickel | Mass of Ni |
| `nickel_class_i` | Nickel Class I | Nickel | Refined Ni (>=99.8%); LME deliverable |
| `nickel_pig_iron` | NPI gross weight | Nickel | Gross weight of NPI product (requires grade for Ni content) |
| `manganese_ore` | Manganese ore (gross weight) | Manganese | Mass of ore (requires grade for Mn content) |
| `manganese_contained` | Manganese contained | Manganese | Mass of Mn |
| `graphite_concentrate` | Graphite concentrate | Graphite | Mass of concentrate product |
| `rare_earth_oxide` | Rare earth oxide (REO) | REE | Total REO mass (mixed oxides) |
| `individual_reo` | Individual rare earth oxide | REE species | Mass of specific oxide (e.g., Nd2O3) |
| `copper_contained` | Copper contained | Copper | Mass of Cu |
| `copper_cathode` | Refined copper cathode | Copper | Mass of cathode product |
| `tellurium_metal` | Tellurium metal | Tellurium | Mass of Te |
| `indium_metal` | Indium metal | Indium | Mass of In |
| `silicon_metal` | Metallurgical-grade silicon | Silicon | Mass of MG-Si product |
| `polysilicon` | Polysilicon | Silicon | Mass of polysilicon product |

### Metric resolution rules

1. If the source explicitly states the metric (e.g., "86,000 tonnes of lithium content"), use the stated metric directly.
2. If the source uses an abbreviation (e.g., "LCE", "REO"), resolve via the taxonomy and tag accordingly.
3. If the source is ambiguous (e.g., "86,000 tonnes of lithium"), default to `contained_metal` and note the ambiguity. The taxonomy support agent (Agent 4 support mode) can be invoked for disambiguation using document context.
4. If a known source consistently uses a specific metric (e.g., USGS MCS reports lithium in contained Li), this convention can be stored as a source-level default and applied automatically.

---

## 8. Domain validation ranges

Sanity-check ranges for common data points. The validation agent (Agent 7) uses these to flag outliers. Values outside these ranges are not automatically rejected — they are flagged for review.

| Data point | Mineral | Plausible range | Notes |
|---|---|---|---|
| Country annual mine production | Lithium | 0 - 250,000 t Li content | Australia ~86kt (2023), Chile ~44kt |
| Country annual mine production | Cobalt | 0 - 200,000 t Co | DRC ~170kt (2023) |
| Country annual mine production | Nickel | 0 - 2,000,000 t Ni | Indonesia ~1.8Mt (2023, contained) |
| Country annual mine production | Manganese | 0 - 25,000,000 t ore | South Africa ~7Mt ore (2023) |
| Country annual mine production | Graphite | 0 - 1,500,000 t | China ~1.1Mt (2023) |
| Country annual mine production | REE (REO) | 0 - 300,000 t REO | China ~240kt REO (2023) |
| Country annual mine production | Copper | 0 - 10,000,000 t Cu | Chile ~5.3Mt (2023) |
| Global annual production | Tellurium | 0 - 1,000 t | ~500-600t globally (2023) |
| Global annual production | Indium | 0 - 2,000 t | ~900-1000t globally (2023) |
| Lithium price | — | 1,000 - 200,000 USD/t LCE | Range covers historical lows to 2022 peak |
| Cobalt price | — | 10,000 - 100,000 USD/t | |
| Nickel price | — | 5,000 - 60,000 USD/t | LME nickel |
| Copper price | — | 3,000 - 15,000 USD/t | LME copper |
| Country reserves | Lithium | 0 - 25,000,000 t Li | Bolivia ~21Mt (USGS) |
| Country reserves | Cobalt | 0 - 10,000,000 t Co | DRC ~4Mt |
| Country reserves | Nickel | 0 - 50,000,000 t Ni | Indonesia ~21Mt |

**Important**: These ranges are approximate guides as of 2023-2024. They should be updated periodically. Extreme events (e.g., the 2022 lithium price spike) can temporarily push values outside "normal" ranges.
