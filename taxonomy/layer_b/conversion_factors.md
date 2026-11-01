# Conversion Factors

## Version 0.2.0

Production and trade figures for the same mineral are reported in different forms across sources. This document maintains conversion factors between forms, enabling normalisation to a common basis (typically contained metal).

**Layer:** B (Operational Mapping Registry). Changes to this file are machine-maintainable with human-reviewable audit trail.

**Assumption logging:**
- `[assumed]`: Derived from LLM pre-trained knowledge or stoichiometric calculation. Awaiting verification against a published reference. **Assumed factors cannot produce gold-tier derived values** (design document Section 3.5).
- `[verified]`: Confirmed against a named published source.

**Database mirror:** This table is mirrored in PostgreSQL (`conversion_factor_log`). All changes are logged with timestamps, old values, and change reasons.

**Update protocol:** When a factor is updated, all derived values in the database that used the old `factor_id` are flagged for recalculation (targeted re-processing via dependency lineage, not a full pipeline re-run).

**`factor_id` naming convention:** `CF-{mineral_short}-{from_short}-{to_short}` (e.g., `CF-Li-lco3-metal`).

---

## How to read this table

- **`factor_id`**: Machine-readable ID used in dependency lineage blocks (see `pipeline_schemas/system_relationships.md` and design Section 4.4).
- **"From" form**: The form in which the source document reports the figure.
- **"To" form**: The target normalised form (usually contained metal).
- **Factor**: Multiply the reported value by this factor to convert. E.g., 1 tonne Li2CO3 × 0.1880 = 0.188 tonnes Li.
- **Derivation**: How the factor was calculated, for auditability.
- **Version**: Incremented when the factor value changes. Referenced in lineage blocks so re-processing is precise.
- **Last updated**: ISO 8601 date.

---

## Lithium

| factor_id | From form | To form | Factor | Derivation | Source | Confidence | version | last_updated |
|---|---|---|---|---|---|---|---|---|
| `CF-Li-lco3-metal` | lithium_carbonate (Li2CO3) | lithium_metal (Li) | 0.1880 | 2 × 6.941 / 73.89 = 0.1879 | Stoichiometric calculation | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-Li-loh-metal` | lithium_hydroxide (LiOH-H2O) | lithium_metal (Li) | 0.1654 | 6.941 / 41.96 = 0.1654 | Stoichiometric calculation | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-Li-lce-metal` | lithium_carbonate_equivalent (LCE) | lithium_metal (Li) | 0.1880 | LCE is defined as equivalent to Li2CO3 | Convention | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-Li-spod6-metal` | spodumene_concentrate (6% Li2O) | lithium_metal (Li) | 0.0279 | 6% × (2 × 6.941 / 29.88) = 6% × 0.4645 = 0.0279 | Stoichiometric at 6% Li2O grade | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-Li-spod5-metal` | spodumene_concentrate (5% Li2O) | lithium_metal (Li) | 0.0232 | 5% × 0.4645 = 0.0232 | Stoichiometric at 5% Li2O grade | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-Li-li2o-metal` | lithium_oxide (Li2O) | lithium_metal (Li) | 0.4645 | 2 × 6.941 / 29.88 = 0.4645 | Stoichiometric calculation | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-Li-metal-lco3` | lithium_metal (Li) | lithium_carbonate (Li2CO3) | 5.3228 | 73.89 / (2 × 6.941) = 5.3228 | Stoichiometric calculation (inverse) | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-Li-loh-lco3` | lithium_hydroxide (LiOH-H2O) | lithium_carbonate (Li2CO3) | 0.8800 | 0.1654 / 0.1880 × 5.3228 = 0.880 | Derived from Li content ratios | [assumed] | 0.1.0 | 2026-04-15 |

### Lithium grade convention note

Spodumene concentrate grades vary. The two most commonly referenced grades are 6% Li2O (standard "chemical-grade" or "SC6") and 5% Li2O. When a source does not specify the grade, assume 6% Li2O unless context indicates otherwise (e.g., African deposits sometimes report at 5.5% or lower).

---

## Cobalt

| factor_id | From form | To form | Factor | Derivation | Source | Confidence | version | last_updated |
|---|---|---|---|---|---|---|---|---|
| `CF-Co-oh2-metal` | cobalt_hydroxide (Co(OH)2) | cobalt_metal (Co) | 0.6346 | 58.93 / 92.95 = 0.6346 | Stoichiometric calculation | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-Co-so4-metal` | cobalt_sulphate (CoSO4-7H2O) | cobalt_metal (Co) | 0.2097 | 58.93 / 281.10 = 0.2097 | Stoichiometric calculation | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-Co-co3o4-metal` | cobalt_oxide (Co3O4) | cobalt_metal (Co) | 0.7342 | 3 × 58.93 / 240.80 = 0.7342 | Stoichiometric calculation | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-Co-coco3-metal` | cobalt_carbonate (CoCO3) | cobalt_metal (Co) | 0.4955 | 58.93 / 118.94 = 0.4955 | Stoichiometric calculation | [assumed] | 0.1.0 | 2026-04-15 |

### Note on DRC cobalt reporting

The DRC (the world's largest cobalt producer) typically reports mine production in contained cobalt metal, but artisanal and small-scale mining (ASM) output is sometimes reported in cobalt hydroxide. When interpreting DRC production data, verify the reporting basis carefully.

---

## Nickel

| factor_id | From form | To form | Factor | Derivation | Source | Confidence | version | last_updated |
|---|---|---|---|---|---|---|---|---|
| `CF-Ni-niso4-metal` | nickel_sulphate (NiSO4-6H2O) | nickel_metal (Ni) | 0.2231 | 58.69 / 262.85 = 0.2231 | Stoichiometric calculation | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-Ni-feni20-metal` | ferronickel (20% Ni) | nickel_metal (Ni) | 0.20 | By definition (20% Ni content) | Grade-dependent | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-Ni-feni35-metal` | ferronickel (35% Ni) | nickel_metal (Ni) | 0.35 | By definition (35% Ni content) | Grade-dependent | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-Ni-npi10-metal` | nickel_pig_iron (10% Ni) | nickel_metal (Ni) | 0.10 | By definition (10% Ni content) | Grade-dependent | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-Ni-ni3s2-metal` | nickel_matte (Ni3S2) | nickel_metal (Ni) | 0.7350 | 3 × 58.69 / 240.21 = 0.7350 | Stoichiometric (pure Ni3S2) | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-Ni-mhp40-metal` | mixed_hydroxide_precipitate (MHP, ~40% Ni) | nickel_metal (Ni) | 0.40 | Typical commercial grade | Industry convention | [assumed] | 0.1.0 | 2026-04-15 |

### Note on NPI grades

Nickel pig iron grades vary widely (1.5% to 15% Ni). Low-grade NPI (<5% Ni) is common in Chinese production; medium-grade (8-12% Ni) and high-grade (>12% Ni) are produced in Indonesia. When a source reports NPI production in gross weight without specifying Ni content, conversion is not possible — flag for human review.

---

## Manganese

| factor_id | From form | To form | Factor | Derivation | Source | Confidence | version | last_updated |
|---|---|---|---|---|---|---|---|---|
| `CF-Mn-ore48-metal` | manganese_ore (48% Mn) | manganese_metal (Mn) | 0.48 | By definition (48% Mn content) | Grade-dependent; 48% is common reference grade | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-Mn-mno2-metal` | manganese_dioxide (MnO2) | manganese_metal (Mn) | 0.6319 | 54.94 / 86.94 = 0.6319 | Stoichiometric calculation | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-Mn-mnso4-metal` | manganese_sulphate (MnSO4-H2O) | manganese_metal (Mn) | 0.3249 | 54.94 / 169.02 = 0.3249 | Stoichiometric calculation | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-Mn-femn78-metal` | ferromanganese (78% Mn, HC) | manganese_metal (Mn) | 0.78 | By definition (78% Mn content) | Standard HC FeMn grade | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-Mn-simn65-metal` | silicomanganese (65% Mn) | manganese_metal (Mn) | 0.65 | By definition (65% Mn content) | Typical SiMn grade | [assumed] | 0.1.0 | 2026-04-15 |

### Note on manganese ore grading

Manganese ore is reported in gross weight, Mn content, or Mn metal equivalent depending on the source. USGS reports mine production in gross weight of ore; some producers report in contained Mn. The grade assumption (48% Mn) is a common reference but varies by deposit (South African ores are typically 36-48%; Australian ores can be 44-50%; Gabon ores ~50%).

---

## Graphite

| factor_id | From form | To form | Factor | Derivation | Source | Confidence | version | last_updated |
|---|---|---|---|---|---|---|---|---|
| `CF-C-conc94-contained` | graphite_concentrate (94% C) | graphite_contained (C) | 0.94 | By definition (94% C content) | Typical commercial grade | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-C-conc97-contained` | graphite_concentrate (97% C) | graphite_contained (C) | 0.97 | By definition (97% C content) | Battery-grade concentrate | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-C-spg9995-contained` | spherical_graphite (SPG, 99.95% C) | graphite_contained (C) | 0.9995 | By definition | Battery anode-grade | [assumed] | 0.1.0 | 2026-04-15 |

### Note on graphite reporting

Graphite production is almost always reported in tonnes of concentrate or product, not contained carbon. Conversion to "contained graphite" is rarely meaningful because the product *is* the carbon. The conversion factors above are included for completeness, but for most analytical purposes, graphite figures should be used as reported.

---

## Silicon

| factor_id | From form | To form | Factor | Derivation | Source | Confidence | version | last_updated |
|---|---|---|---|---|---|---|---|---|
| `CF-Si-sio2-metal` | silica (SiO2) | silicon_metal (Si) | 0.4674 | 28.09 / 60.08 = 0.4674 | Stoichiometric calculation | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-Si-fesi75-metal` | ferrosilicon (75% Si) | silicon_metal (Si) | 0.75 | By definition (75% Si content) | Common FeSi grade | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-Si-tcs-poly` | trichlorosilane (SiHCl3) | polysilicon (Si) | 0.2076 | 28.09 / 135.45 = 0.2076 | Stoichiometric calculation | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-Si-metal-poly-siemens` | silicon_metal → polysilicon (Siemens) | ~1.2 kg MG-Si per kg polysilicon | Process yield | Industry estimates | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-Si-metal-poly-fbr` | silicon_metal → polysilicon (FBR) | ~1.05 kg MG-Si per kg polysilicon | Process yield | Industry estimates | [assumed] | 0.1.0 | 2026-04-15 |

### Note on silicon/polysilicon reporting

Metallurgical-grade silicon (MG-Si) and polysilicon are different products at different points in the value chain. The conversion from silica (SiO2) to Si is stoichiometric but rarely used because nobody reports quartz mining output as "contained silicon." The `CF-Si-metal-poly-*` factors are process yields (not stoichiometric): typically 1.1-1.3 kg MG-Si per kg polysilicon (Siemens process).

---

## Tellurium

| factor_id | From form | To form | Factor | Derivation | Source | Confidence | version | last_updated |
|---|---|---|---|---|---|---|---|---|
| `CF-Te-teo2-metal` | tellurium_dioxide (TeO2) | tellurium_metal (Te) | 0.7995 | 127.60 / 159.60 = 0.7995 | Stoichiometric calculation | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-Te-cdte-metal` | cadmium_telluride (CdTe) | tellurium_metal (Te) | 0.5316 | 127.60 / 240.01 = 0.5316 | Stoichiometric calculation | [assumed] | 0.1.0 | 2026-04-15 |

### Note on tellurium reporting

Tellurium production figures are almost always reported in refined metal tonnes. The only common conversion needed is CdTe → Te for estimating demand from solar PV manufacturers. First Solar's CdTe usage is sometimes reported in CdTe weight or Te weight — verify the basis.

---

## Indium

| factor_id | From form | To form | Factor | Derivation | Source | Confidence | version | last_updated |
|---|---|---|---|---|---|---|---|---|
| `CF-In-inoh3-metal` | indium_hydroxide (In(OH)3) | indium_metal (In) | 0.6910 | 114.82 / 166.85 = 0.6881 | Stoichiometric calculation | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-In-ito-metal` | indium_tin_oxide (ITO, 90% In2O3 / 10% SnO2) | indium_metal (In) | 0.7117 | 0.90 × (2 × 114.82 / 277.64) = 0.90 × 0.8271 = 0.7444; ~78% In by weight in practice | Industry convention | [assumed] | 0.1.0 | 2026-04-15 |

### Note on indium reporting and ITO recycling

Primary indium production is reported in refined metal tonnes. A significant share of indium supply comes from recycling ITO sputtering targets (recovery rates of spent ITO are high, ~70-90%). Recycled indium should be tracked separately from primary production where the source distinguishes them.

---

## Rare Earth Elements

REE conversion is more complex because documents may report individual oxide weights or total REO.

| factor_id | From form | To form | Factor | Derivation | Source | Confidence | version | last_updated |
|---|---|---|---|---|---|---|---|---|
| `CF-REE-la2o3-metal` | La2O3 | La metal | 0.8527 | 2 × 138.91 / 325.81 = 0.8527 | Stoichiometric | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-REE-ceo2-metal` | CeO2 | Ce metal | 0.8141 | 140.12 / 172.12 = 0.8141 | Stoichiometric | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-REE-pr6o11-metal` | Pr6O11 | Pr metal | 0.8278 | 6 × 140.91 / 1021.44 = 0.8278 | Stoichiometric | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-REE-nd2o3-metal` | Nd2O3 | Nd metal | 0.8574 | 2 × 144.24 / 336.48 = 0.8574 | Stoichiometric | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-REE-sm2o3-metal` | Sm2O3 | Sm metal | 0.8624 | 2 × 150.36 / 348.72 = 0.8624 | Stoichiometric | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-REE-eu2o3-metal` | Eu2O3 | Eu metal | 0.8634 | 2 × 151.96 / 351.93 = 0.8634 | Stoichiometric | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-REE-gd2o3-metal` | Gd2O3 | Gd metal | 0.8676 | 2 × 157.25 / 362.50 = 0.8676 | Stoichiometric | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-REE-tb4o7-metal` | Tb4O7 | Tb metal | 0.8503 | 4 × 158.93 / 747.70 = 0.8503 | Stoichiometric | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-REE-dy2o3-metal` | Dy2O3 | Dy metal | 0.8713 | 2 × 162.50 / 373.00 = 0.8713 | Stoichiometric | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-REE-ho2o3-metal` | Ho2O3 | Ho metal | 0.8731 | 2 × 164.93 / 377.86 = 0.8731 | Stoichiometric | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-REE-er2o3-metal` | Er2O3 | Er metal | 0.8745 | 2 × 167.26 / 382.52 = 0.8745 | Stoichiometric | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-REE-tm2o3-metal` | Tm2O3 | Tm metal | 0.8756 | 2 × 168.93 / 385.87 = 0.8756 | Stoichiometric | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-REE-yb2o3-metal` | Yb2O3 | Yb metal | 0.8782 | 2 × 173.04 / 394.08 = 0.8782 | Stoichiometric | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-REE-lu2o3-metal` | Lu2O3 | Lu metal | 0.8795 | 2 × 174.97 / 397.93 = 0.8795 | Stoichiometric | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-REE-y2o3-metal` | Y2O3 | Y metal | 0.7875 | 2 × 88.91 / 225.81 = 0.7875 | Stoichiometric | [assumed] | 0.1.0 | 2026-04-15 |

### Note on REO aggregate reporting

When a source reports "total REO production" (e.g., "China produced 240,000 t REO in 2023"), converting to contained metal is not straightforward because the REO mix varies by deposit and producer. As a rough approximation, a weighted-average REO-to-metal factor of ~0.85 can be used, but this carries significant uncertainty. When possible, use individual oxide breakdowns for more accurate conversion.

---

## Copper

| factor_id | From form | To form | Factor | Derivation | Source | Confidence | version | last_updated |
|---|---|---|---|---|---|---|---|---|
| `CF-Cu-conc25-metal` | copper_concentrate (25% Cu) | copper_metal (Cu) | 0.25 | By definition (25% Cu content) | Grade-dependent; 25% is typical reference | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-Cu-conc30-metal` | copper_concentrate (30% Cu) | copper_metal (Cu) | 0.30 | By definition (30% Cu content) | Grade-dependent | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-Cu-cuo-metal` | copper_oxide (CuO) | copper_metal (Cu) | 0.7988 | 63.55 / 79.55 = 0.7988 | Stoichiometric calculation | [assumed] | 0.1.0 | 2026-04-15 |
| `CF-Cu-cuso4-metal` | copper_sulphate (CuSO4-5H2O) | copper_metal (Cu) | 0.2545 | 63.55 / 249.69 = 0.2545 | Stoichiometric calculation | [assumed] | 0.1.0 | 2026-04-15 |

### Note on copper reporting

Copper mine production is typically reported in contained metal (Cu content of concentrate), not gross ore weight. Refined copper production is reported in cathode weight. The two figures are not directly comparable — mine production includes copper that is lost in smelting/refining (recovery rates are typically 85-95%).
