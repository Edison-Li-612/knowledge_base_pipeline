# Mineral and Material Hierarchy

## Version 0.1.0

This document defines the full mineral/material taxonomy. Each entry includes:
- **Canonical name** (used as the tag value in pipeline outputs)
- **Display name** (human-readable)
- **Chemical formula** (where applicable)
- **CAS number** (where applicable, for unambiguous chemical identification)
- **Common forms** reported in supply chain literature (each form is a distinct reporting basis)
- **Group membership** (for species that belong to a group)

---

## Structure

The hierarchy uses two levels:
1. **Group level**: A family of related minerals/materials (e.g., rare_earth_elements, platinum_group_metals). Documents may report aggregate data at this level.
2. **Species level**: An individual mineral or material. Documents may report data at this level.

Both levels are valid tagging targets. When a document reports at the group level, the tag uses the group entity. When it reports at the species level, the tag uses the species entity. Neo4j links species to groups via `MEMBER_OF` relationships.

Some minerals are standalone (not part of a group) but may have sub-types distinguished by origin or processing (e.g., natural graphite vs synthetic graphite). These are modelled as species under a group.

---

## 1. Lithium

| Field | Value |
|---|---|
| Canonical name | `lithium` |
| Display name | Lithium |
| Symbol | Li |
| Atomic number | 3 |
| CAS number | 7439-93-2 |
| Group membership | None (standalone) |
| Primary supply chain role | Battery cathodes, ceramics, glass, lubricants, pharmaceuticals |

### Common reporting forms

| Form canonical name | Display name | Chemical formula | CAS number | Notes |
|---|---|---|---|---|
| `lithium_metal` | Lithium metal | Li | 7439-93-2 | Contained metal basis; the reference basis for conversion |
| `lithium_carbonate` | Lithium carbonate | Li2CO3 | 554-13-2 | Most common trading/pricing form |
| `lithium_hydroxide` | Lithium hydroxide monohydrate | LiOH-H2O | 1310-66-3 | Key cathode precursor (NMC, NCA) |
| `lithium_carbonate_equivalent` | Lithium carbonate equivalent (LCE) | Li2CO3-equivalent | N/A | Reporting convention; numerically equivalent to lithium_carbonate |
| `spodumene_concentrate` | Spodumene concentrate | LiAlSi2O6 (variable grade) | 1302-37-0 | Typically reported at 6% Li2O grade; hard-rock source |
| `lithium_oxide` | Lithium oxide | Li2O | 12057-24-8 | Sometimes used in reporting ore grades |
| `brine` | Lithium brine | N/A | N/A | Raw brine; concentration varies; rarely reported as a production figure |
| `lepidolite` | Lepidolite concentrate | K(Li,Al)3(Si,Al)4O10(F,OH)2 | 1317-64-2 | Minor hard-rock source (China) |
| `petalite` | Petalite concentrate | LiAlSi4O10 | 12031-80-0 | Minor hard-rock source |

---

## 2. Cobalt

| Field | Value |
|---|---|
| Canonical name | `cobalt` |
| Display name | Cobalt |
| Symbol | Co |
| Atomic number | 27 |
| CAS number | 7440-48-4 |
| Group membership | None (standalone) |
| Primary supply chain role | Battery cathodes (NMC, NCA, LCO), superalloys, hard metals, catalysts |

### Common reporting forms

| Form canonical name | Display name | Chemical formula | CAS number | Notes |
|---|---|---|---|---|
| `cobalt_metal` | Cobalt metal | Co | 7440-48-4 | Contained metal basis |
| `cobalt_hydroxide` | Cobalt hydroxide | Co(OH)2 | 21041-93-0 | Common intermediate from DRC |
| `cobalt_sulphate` | Cobalt sulphate | CoSO4-7H2O | 10026-24-1 | Battery-grade precursor |
| `cobalt_oxide` | Cobalt oxide | Co3O4 | 1308-06-1 | Used in LCO cathodes |
| `cobalt_carbonate` | Cobalt carbonate | CoCO3 | 513-79-1 | Intermediate product |
| `cobalt_chloride` | Cobalt chloride | CoCl2 | 7646-79-9 | Chemical applications |
| `cobalt_contained` | Cobalt contained (in ore/concentrate) | Co | N/A | Reporting convention for mine output |

---

## 3. Nickel

| Field | Value |
|---|---|
| Canonical name | `nickel` |
| Display name | Nickel |
| Symbol | Ni |
| Atomic number | 28 |
| CAS number | 7440-02-0 |
| Group membership | None (standalone) |
| Primary supply chain role | Stainless steel, battery cathodes (NMC, NCA), superalloys |

### Common reporting forms

| Form canonical name | Display name | Chemical formula | CAS number | Notes |
|---|---|---|---|---|
| `nickel_metal` | Nickel metal (Class I) | Ni | 7440-02-0 | Refined metal; >=99.8% Ni; LME deliverable |
| `nickel_sulphate` | Nickel sulphate | NiSO4-6H2O | 10101-97-0 | Battery-grade precursor |
| `nickel_pig_iron` | Nickel pig iron (NPI) | Ni (in NPI) | N/A | Low-grade ferronickel (1.5-15% Ni); major Chinese/Indonesian product |
| `ferronickel` | Ferronickel | FeNi | N/A | Typically 20-40% Ni; stainless steel feedstock |
| `nickel_matte` | Nickel matte | Ni3S2 | 12035-72-2 | Intermediate smelter product |
| `mixed_hydroxide_precipitate` | Mixed hydroxide precipitate (MHP) | Ni(OH)2 + Co(OH)2 | N/A | HPAL intermediate; contains both Ni and Co |
| `mixed_sulphide_precipitate` | Mixed sulphide precipitate (MSP) | NiS + CoS | N/A | Alternative HPAL intermediate |
| `nickel_contained` | Nickel contained (in ore) | Ni | N/A | Reporting convention for mine output |
| `laterite_ore` | Laterite ore | N/A | N/A | Raw ore; grade varies (0.8-2.5% Ni) |
| `sulphide_ore` | Sulphide ore | N/A | N/A | Raw ore; typically higher grade than laterite |

---

## 4. Manganese

| Field | Value |
|---|---|
| Canonical name | `manganese` |
| Display name | Manganese |
| Symbol | Mn |
| Atomic number | 25 |
| CAS number | 7439-96-5 |
| Group membership | None (standalone) |
| Primary supply chain role | Steelmaking (>90% of demand), battery cathodes (NMC, LMFP), dry cells |

### Common reporting forms

| Form canonical name | Display name | Chemical formula | CAS number | Notes |
|---|---|---|---|---|
| `manganese_metal` | Manganese metal | Mn | 7439-96-5 | Electrolytic manganese metal (EMM) |
| `manganese_ore` | Manganese ore | MnO2 (variable) | N/A | Raw ore; reported in gross weight or Mn content |
| `manganese_dioxide` | Manganese dioxide | MnO2 | 1313-13-9 | Electrolytic manganese dioxide (EMD); battery-grade |
| `manganese_sulphate` | Manganese sulphate | MnSO4-H2O | 10034-96-5 | Battery-grade precursor (high purity) |
| `ferromanganese` | Ferromanganese | FeMn | N/A | High-carbon (HC) or refined; steelmaking alloy |
| `silicomanganese` | Silicomanganese | SiMn | N/A | Steelmaking alloy |
| `manganese_contained` | Manganese contained | Mn | N/A | Reporting convention for mine output |

---

## 5. Graphite

| Field | Value |
|---|---|
| Canonical name | `graphite` |
| Display name | Graphite |
| Symbol | C |
| Atomic number | 6 |
| CAS number | 7782-42-5 |
| Group membership | Group (has sub-types) |
| Primary supply chain role | Battery anodes, refractories, lubricants, brake linings |

### Sub-types (species)

| Species canonical name | Display name | Group | Notes |
|---|---|---|---|
| `natural_graphite` | Natural graphite | graphite | Mined; includes flake, vein, and amorphous varieties |
| `synthetic_graphite` | Synthetic graphite | graphite | Manufactured from petroleum coke or coal tar pitch |

### Common reporting forms

| Form canonical name | Display name | Applies to | Notes |
|---|---|---|---|
| `graphite_ore` | Graphite ore | natural_graphite | Raw ore; grade varies (2-30% C) |
| `graphite_concentrate` | Graphite concentrate | natural_graphite | Beneficiated; typically 90-97% C |
| `flake_graphite` | Flake graphite | natural_graphite | Specific morphology; key for battery applications |
| `vein_graphite` | Vein (lump) graphite | natural_graphite | High purity; primarily from Sri Lanka |
| `amorphous_graphite` | Amorphous graphite | natural_graphite | Lower grade; industrial uses |
| `spherical_graphite` | Spherical graphite (SPG) | natural_graphite | Processed from flake; direct anode material |
| `synthetic_graphite_product` | Synthetic graphite | synthetic_graphite | Manufactured product; anode-grade |
| `graphite_contained` | Graphite contained | graphite | Carbon content basis |

---

## 6. Silicon

| Field | Value |
|---|---|
| Canonical name | `silicon` |
| Display name | Silicon |
| Symbol | Si |
| Atomic number | 14 |
| CAS number | 7440-21-3 |
| Group membership | None (standalone) |
| Primary supply chain role | Semiconductors, solar PV (polysilicon), aluminium alloys, silicones |

### Common reporting forms

| Form canonical name | Display name | Chemical formula | CAS number | Notes |
|---|---|---|---|---|
| `silicon_metal` | Silicon metal (metallurgical-grade) | Si | 7440-21-3 | MG-Si; >=98.5% Si; feedstock for polysilicon and alloys |
| `ferrosilicon` | Ferrosilicon | FeSi | 8049-17-0 | Steelmaking alloy; typically 65-90% Si |
| `polysilicon` | Polysilicon (solar/semiconductor-grade) | Si | 7440-21-3 | >=99.9999% Si (6N+); solar cells and chips |
| `silica` | Silica (silicon dioxide) | SiO2 | 7631-86-9 | Quartz; raw material for Si production |
| `trichlorosilane` | Trichlorosilane (TCS) | SiHCl3 | 10025-78-2 | Intermediate in Siemens process polysilicon |
| `silane` | Silane (monosilane) | SiH4 | 7803-62-5 | Intermediate in fluidised bed reactor (FBR) polysilicon |
| `silicon_wafer` | Silicon wafer | Si | N/A | Processed product; not typically reported as production volume |

---

## 7. Tellurium

| Field | Value |
|---|---|
| Canonical name | `tellurium` |
| Display name | Tellurium |
| Symbol | Te |
| Atomic number | 52 |
| CAS number | 13494-80-9 |
| Group membership | None (standalone) |
| Primary supply chain role | CdTe thin-film solar PV, thermoelectrics, metallurgy, rubber vulcanisation |

### Common reporting forms

| Form canonical name | Display name | Chemical formula | CAS number | Notes |
|---|---|---|---|---|
| `tellurium_metal` | Tellurium metal | Te | 13494-80-9 | Refined metal; contained basis |
| `tellurium_dioxide` | Tellurium dioxide | TeO2 | 7446-07-3 | Sometimes reported as production form |
| `cadmium_telluride` | Cadmium telluride | CdTe | 1306-25-8 | End-use compound for solar PV |
| `bismuth_telluride` | Bismuth telluride | Bi2Te3 | 1304-82-1 | Thermoelectric applications |
| `copper_anode_slimes` | Copper anode slimes | N/A | N/A | Primary source material (byproduct of copper refining) |

### Supply chain notes

Tellurium is almost exclusively a byproduct of copper refining (recovered from anode slimes during electrolytic copper production). Production volumes are constrained by copper refining capacity, not direct mining. This creates a supply ceiling that is largely independent of tellurium demand.

---

## 8. Indium

| Field | Value |
|---|---|
| Canonical name | `indium` |
| Display name | Indium |
| Symbol | In |
| Atomic number | 49 |
| CAS number | 7440-74-6 |
| Group membership | None (standalone) |
| Primary supply chain role | ITO (displays/touchscreens), CIGS solar PV, solders, semiconductors |

### Common reporting forms

| Form canonical name | Display name | Chemical formula | CAS number | Notes |
|---|---|---|---|---|
| `indium_metal` | Indium metal | In | 7440-74-6 | Refined metal; standard purity >=99.99% (4N) |
| `indium_tin_oxide` | Indium tin oxide (ITO) | In2O3-SnO2 | N/A | Dominant end-use form; transparent conductive coating |
| `indium_hydroxide` | Indium hydroxide | In(OH)3 | 20661-21-6 | Intermediate processing product |
| `crude_indium` | Crude indium | In | N/A | Partially refined; typically >=98% In |
| `indium_contained` | Indium contained (in zinc concentrate) | In | N/A | Reporting convention for mine-stage output |

### Supply chain notes

Indium is primarily a byproduct of zinc smelting (recovered from zinc concentrates and residues). Like tellurium, supply is constrained by the primary metal (zinc) production rate. China dominates both primary production and refining (>50% of global supply). Recycling from ITO sputtering targets is a significant secondary source.

---

## 9. Rare Earth Elements (REE)

| Field | Value |
|---|---|
| Canonical name | `rare_earth_elements` |
| Display name | Rare Earth Elements |
| Abbreviation | REE, RE |
| CAS number | N/A (group) |
| Group membership | Group (17 species) |
| Primary supply chain role | Permanent magnets (Nd, Pr, Dy, Tb), catalysts (La, Ce), phosphors (Eu, Y, Tb), glass polishing (Ce), metallurgy (mischmetal) |

### Common group-level reporting forms

| Form canonical name | Display name | Chemical formula | Notes |
|---|---|---|---|
| `rare_earth_oxide` | Rare earth oxide (REO) | RE2O3 (mixed) | Most common aggregate reporting form; total REO production |
| `rare_earth_carbonate` | Rare earth carbonate | RE2(CO3)3 | Some producers report in this form |
| `mischmetal` | Mischmetal | Mixed RE metals | Unseparated RE alloy |
| `total_rare_earth_contained` | Total rare earth (contained metal) | RE | Contained metal equivalent |

### Species (17 elements)

REEs are divided into **light** (LREE) and **heavy** (HREE) sub-groups. The classification boundary varies by source; this taxonomy follows the most common convention.

#### Light Rare Earth Elements (LREE)

| Canonical name | Display name | Symbol | Atomic number | CAS number | Oxide formula | Key applications |
|---|---|---|---|---|---|---|
| `lanthanum` | Lanthanum | La | 57 | 7439-91-0 | La2O3 | FCC catalysts, optical glass, hydrogen storage alloys |
| `cerium` | Cerium | Ce | 58 | 7440-45-1 | CeO2 | Glass polishing, catalytic converters, fuel cells |
| `praseodymium` | Praseodymium | Pr | 59 | 7440-10-0 | Pr6O11 | NdFeB magnets (as NdPr), ceramics pigments |
| `neodymium` | Neodymium | Nd | 60 | 7440-00-8 | Nd2O3 | NdFeB permanent magnets (dominant demand driver) |
| `promethium` | Promethium | Pm | 61 | 7440-12-2 | Pm2O3 | Radioactive; no commercial supply chain relevance |
| `samarium` | Samarium | Sm | 62 | 7440-19-9 | Sm2O3 | SmCo permanent magnets, nuclear applications |
| `europium` | Europium | Eu | 63 | 7440-53-1 | Eu2O3 | Phosphors (red), anti-counterfeiting |

#### Heavy Rare Earth Elements (HREE)

| Canonical name | Display name | Symbol | Atomic number | CAS number | Oxide formula | Key applications |
|---|---|---|---|---|---|---|
| `gadolinium` | Gadolinium | Gd | 64 | 7440-54-2 | Gd2O3 | MRI contrast agents, nuclear applications |
| `terbium` | Terbium | Tb | 65 | 7440-27-9 | Tb4O7 | NdFeB magnets (grain boundary diffusion), phosphors |
| `dysprosium` | Dysprosium | Dy | 66 | 7440-72-4 | Dy2O3 | NdFeB magnets (high-temperature coercivity) |
| `holmium` | Holmium | Ho | 67 | 7440-60-0 | Ho2O3 | Lasers, nuclear applications |
| `erbium` | Erbium | Er | 68 | 7440-52-0 | Er2O3 | Fibre optic amplifiers, lasers |
| `thulium` | Thulium | Tm | 69 | 7440-30-4 | Tm2O3 | Portable X-ray devices, lasers |
| `ytterbium` | Ytterbium | Yb | 70 | 7440-64-4 | Yb2O3 | Fibre lasers, metallurgy |
| `lutetium` | Lutetium | Lu | 71 | 7439-94-3 | Lu2O3 | PET scan detectors, catalysts |

#### Associated element (conventionally grouped with REE)

| Canonical name | Display name | Symbol | Atomic number | CAS number | Oxide formula | Key applications |
|---|---|---|---|---|---|---|
| `yttrium` | Yttrium | Y | 39 | 7440-65-5 | Y2O3 | Ceramics, phosphors, superconductors, LEDs |

### Magnet-critical subset

For many supply chain analyses, the most strategically important REEs are the "magnet materials." The taxonomy marks these for convenient filtering:

| Element | Role in NdFeB magnets | Criticality |
|---|---|---|
| Neodymium (Nd) | Primary magnetic component | Very high |
| Praseodymium (Pr) | Substitutes for / blends with Nd (NdPr didymium) | Very high |
| Dysprosium (Dy) | Increases high-temperature coercivity | Very high |
| Terbium (Tb) | Alternative to Dy for coercivity (grain boundary diffusion) | High |

---

## 10. Copper

| Field | Value |
|---|---|
| Canonical name | `copper` |
| Display name | Copper |
| Symbol | Cu |
| Atomic number | 29 |
| CAS number | 7440-50-8 |
| Group membership | None (standalone) |
| Primary supply chain role | Electrical wiring, motors, transformers, EV systems, electronics, construction |

### Common reporting forms

| Form canonical name | Display name | Chemical formula | CAS number | Notes |
|---|---|---|---|---|
| `copper_metal` | Refined copper (cathode) | Cu | 7440-50-8 | LME Grade A cathode; >=99.99% Cu |
| `copper_concentrate` | Copper concentrate | CuFeS2 (variable) | N/A | Smelter feedstock; typically 20-30% Cu |
| `copper_blister` | Blister copper | Cu | N/A | Smelter output; ~98-99% Cu; goes to electrolytic refining |
| `copper_anode` | Copper anode | Cu | N/A | Cast from blister; feedstock for electrolytic refining |
| `copper_oxide` | Copper oxide | CuO / Cu2O | 1317-38-0 / 1317-39-1 | Oxide ore; processed via SX-EW |
| `copper_sulphate` | Copper sulphate | CuSO4-5H2O | 7758-99-8 | Agriculture, chemical applications |
| `copper_contained` | Copper contained (in ore/concentrate) | Cu | N/A | Reporting convention for mine output |
| `copper_scrap` | Copper scrap | Cu | N/A | Secondary (recycled) source; significant share of supply |

### Supply chain notes

Copper is included because: (a) it is the highest-volume critical mineral for electrification; (b) tellurium and several other trace minerals are byproducts of copper refining; (c) copper production and trade data frequently co-occurs with other critical minerals in source documents.

---

## Entity type quick reference

For pipeline tagging, the valid top-level mineral entity tags are:

| Tag value | Type | Level |
|---|---|---|
| `lithium` | standalone | - |
| `cobalt` | standalone | - |
| `nickel` | standalone | - |
| `manganese` | standalone | - |
| `graphite` | group | group |
| `natural_graphite` | species | species (under graphite) |
| `synthetic_graphite` | species | species (under graphite) |
| `silicon` | standalone | - |
| `tellurium` | standalone | - |
| `indium` | standalone | - |
| `rare_earth_elements` | group | group |
| `lanthanum` | species | species (under rare_earth_elements) |
| `cerium` | species | species (under rare_earth_elements) |
| `praseodymium` | species | species (under rare_earth_elements) |
| `neodymium` | species | species (under rare_earth_elements) |
| `promethium` | species | species (under rare_earth_elements) |
| `samarium` | species | species (under rare_earth_elements) |
| `europium` | species | species (under rare_earth_elements) |
| `gadolinium` | species | species (under rare_earth_elements) |
| `terbium` | species | species (under rare_earth_elements) |
| `dysprosium` | species | species (under rare_earth_elements) |
| `holmium` | species | species (under rare_earth_elements) |
| `erbium` | species | species (under rare_earth_elements) |
| `thulium` | species | species (under rare_earth_elements) |
| `ytterbium` | species | species (under rare_earth_elements) |
| `lutetium` | species | species (under rare_earth_elements) |
| `yttrium` | species | species (under rare_earth_elements) |
| `copper` | standalone | - |

### Form tagging rule

When tagging an entity, the `form` field captures the specific reporting form. If the form is unspecified or ambiguous in the source text, use `contained_metal` as the default (i.e., assume the figure is in contained metal terms unless there is evidence otherwise). If the form is explicitly stated (e.g., "lithium carbonate equivalent"), use the matching canonical form name.
