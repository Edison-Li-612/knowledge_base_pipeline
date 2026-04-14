# Country and Region Reference

## Version 0.1.0

This document lists all countries and regions relevant to critical mineral supply chains. It serves as the canonical reference for country code normalisation.

**Normalisation rule:** When the pipeline encounters a country name (e.g., "Australia", "People's Republic of China", "DRC"), it normalises to the ISO 3166-1 alpha-3 code listed here. The tagging agent uses this table for resolution.

---

## Conventions

- **ISO alpha-3**: Standard three-letter country code (ISO 3166-1).
- **Common aliases**: Name variations frequently encountered in supply chain literature.
- **Relevance**: Why this country appears in the critical minerals context (not exhaustive — just the primary reason for inclusion).

---

## Major producing and consuming countries [extensible]

### Asia-Pacific

| ISO alpha-3 | Country name | Common aliases | Mineral relevance |
|---|---|---|---|
| AUS | Australia | Commonwealth of Australia | Lithium (spodumene), rare_earth_elements, nickel, copper, manganese, graphite |
| CHN | China | People's Republic of China, PRC, Mainland China | Dominant in REE, graphite, silicon, cobalt refining, lithium refining, manganese, indium, tellurium |
| IDN | Indonesia | Republic of Indonesia | Nickel (laterite), cobalt (HPAL byproduct), manganese |
| IND | India | Republic of India, Bharat | Manganese, rare_earth_elements, graphite, copper, silicon; growing strategic mineral policy |
| JPN | Japan | Nippon | Battery manufacturing, cobalt/nickel refining, REE magnet production; no significant mining |
| KOR | South Korea | Republic of Korea, ROK | Battery manufacturing (CATL, LG, Samsung SDI); zinc smelting (indium) |
| PRK | North Korea | DPRK, Democratic People's Republic of Korea | Rare_earth_elements (unverified reserves); limited reliable data |
| MMR | Myanmar | Burma, Republic of the Union of Myanmar | Rare_earth_elements (heavy REE ionic clays, Kachin State); significant but opaque |
| PHL | Philippines | Republic of the Philippines | Nickel (laterite) |
| LKA | Sri Lanka | Ceylon | Graphite (vein/lump) |
| VNM | Vietnam | Socialist Republic of Vietnam | Rare_earth_elements (significant reserves); tungsten |
| MNG | Mongolia | | Copper (Oyu Tolgoi); lithium exploration |
| KAZ | Kazakhstan | Republic of Kazakhstan | Copper, manganese, rare_earth_elements |
| UZB | Uzbekistan | Republic of Uzbekistan | Copper |

### Africa

| ISO alpha-3 | Country name | Common aliases | Mineral relevance |
|---|---|---|---|
| COD | Democratic Republic of the Congo | DRC, DR Congo, Congo-Kinshasa, Zaire (historical) | Cobalt (~70% of global mine production), copper |
| ZAF | South Africa | Republic of South Africa, RSA | Manganese (~30% of global supply), chromium, PGMs |
| MOZ | Mozambique | Republic of Mozambique | Graphite (Balama) |
| MDG | Madagascar | Republic of Madagascar | Graphite, nickel (Ambatovy) |
| ZWE | Zimbabwe | Republic of Zimbabwe | Lithium (Bikita, Arcadia) |
| NAM | Namibia | Republic of Namibia | Lithium, rare_earth_elements |
| TZA | Tanzania | United Republic of Tanzania | Graphite, nickel |
| GAB | Gabon | Gabonese Republic | Manganese (Moanda) |
| GHA | Ghana | Republic of Ghana | Manganese |
| MWI | Malawi | Republic of Malawi | Rare_earth_elements (Songwe Hill) |
| AGO | Angola | Republic of Angola | Rare_earth_elements (Longonjo) |
| MAR | Morocco | Kingdom of Morocco | Cobalt |

### Americas

| ISO alpha-3 | Country name | Common aliases | Mineral relevance |
|---|---|---|---|
| USA | United States | United States of America, US, U.S., America | Lithium (brine, hard-rock), rare_earth_elements (Mountain Pass), copper, silicon |
| CAN | Canada | | Nickel (Sudbury, Voisey's Bay), cobalt, graphite, lithium |
| CHL | Chile | Republic of Chile | Lithium (brine, Atacama), copper |
| ARG | Argentina | Argentine Republic | Lithium (brine, Jujuy, Salta, Catamarca) |
| BRA | Brazil | Federative Republic of Brazil | Lithium (spodumene), nickel, graphite, rare_earth_elements, manganese |
| BOL | Bolivia | Plurinational State of Bolivia | Lithium (Salar de Uyuni; limited production) |
| MEX | Mexico | United Mexican States | Lithium (nationalised); copper; silver |
| PER | Peru | Republic of Peru | Copper, lithium exploration |
| CUB | Cuba | Republic of Cuba | Cobalt, nickel |

### Europe

| ISO alpha-3 | Country name | Common aliases | Mineral relevance |
|---|---|---|---|
| GBR | United Kingdom | UK, Britain, Great Britain, England (informal) | REE processing (Pensana/Saltend), lithium exploration (Cornwall), policy/regulation (CMA) |
| FIN | Finland | Republic of Finland | Cobalt (Terrafame), nickel, lithium |
| DEU | Germany | Federal Republic of Germany, Deutschland | Silicon (Wacker), battery manufacturing, no significant mining |
| NOR | Norway | Kingdom of Norway | Silicon (Elkem), nickel, REE (exploration) |
| SWE | Sweden | Kingdom of Sweden | Rare_earth_elements (LKAB/Kiruna), copper |
| PRT | Portugal | Portuguese Republic | Lithium (spodumene; Savannah Resources) |
| SRB | Serbia | Republic of Serbia | Lithium (Jadar; Rio Tinto project, politically sensitive) |
| FRA | France | French Republic | Nickel (New Caledonia overseas territory) |
| BEL | Belgium | Kingdom of Belgium | Cobalt refining (Umicore), indium |
| ESP | Spain | Kingdom of Spain | Lithium exploration |

### Middle East

| ISO alpha-3 | Country name | Common aliases | Mineral relevance |
|---|---|---|---|
| SAU | Saudi Arabia | Kingdom of Saudi Arabia, KSA | Copper, REE exploration; growing critical minerals strategy |
| ARE | United Arab Emirates | UAE, Emirates | Critical minerals investment; recycling |

### Russia and Central Asia

| ISO alpha-3 | Country name | Common aliases | Mineral relevance |
|---|---|---|---|
| RUS | Russia | Russian Federation | Nickel (Norilsk), cobalt, copper, rare_earth_elements; sanctions affect trade data |

---

## Regions and country groups

For aggregate reporting, the pipeline recognises these region tags. Regions are **not** ISO codes; they use the canonical names below.

| Canonical name | Display name | Member countries (non-exhaustive) | Notes |
|---|---|---|---|
| `eu_27` | European Union (EU-27) | DEU, FRA, ESP, PRT, FIN, SWE, BEL, ... | Post-Brexit membership |
| `asean` | ASEAN | IDN, PHL, VNM, MMR, THA, MYS, SGP, LAO, KHM, BRN | Association of Southeast Asian Nations |
| `lithium_triangle` | Lithium Triangle | ARG, BOL, CHL | South American brine region |
| `sub_saharan_africa` | Sub-Saharan Africa | COD, ZAF, MOZ, MDG, ZWE, TZA, GAB, GHA, ... | Common aggregate in reports |
| `latin_america` | Latin America | CHL, ARG, BRA, BOL, MEX, PER, ... | |
| `asia_pacific` | Asia-Pacific | CHN, AUS, IDN, IND, JPN, KOR, PHL, ... | |
| `north_america` | North America | USA, CAN, MEX | |
| `europe` | Europe | GBR, DEU, FRA, NOR, SWE, FIN, ... | Broader than EU-27 |
| `middle_east_north_africa` | Middle East & North Africa (MENA) | SAU, ARE, MAR, ... | |
| `cis` | Commonwealth of Independent States | RUS, KAZ, UZB, ... | |
| `drc_copperbelt` | DRC Copperbelt | COD (sub-national) | Katanga/Haut-Katanga province; most DRC Co/Cu production |

---

## Country name normalisation rules

1. **Exact match first:** Check the "Country name" column. Case-insensitive.
2. **Alias match second:** Check the "Common aliases" column. Case-insensitive. Strip punctuation.
3. **Partial match with caution:** "Congo" alone is ambiguous (COD vs COG). The pipeline should flag this for human review unless context disambiguates (e.g., "Congo cobalt" → COD with high confidence).
4. **Demonyms:** "Australian" → AUS, "Chinese" → CHN, etc. The tagging agent maintains a demonym-to-ISO mapping internally.
5. **Historical names:** "Zaire" → COD, "Burma" → MMR, "Ceylon" → LKA. These map to current ISO codes.
6. **Sub-national entities:** Province/state names (e.g., "Western Australia", "Katanga", "Xinjiang") are stored as location qualifiers on the relationship, not as separate country tags. The country tag remains the national ISO code.
