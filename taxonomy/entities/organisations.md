# Organisation Alias Table

## Version 0.1.0

This table maps organisation name variations to canonical names. When the pipeline encounters any alias, it resolves to the canonical name for consistent storage and graph linking.

**Database mirror:** This table is mirrored in PostgreSQL (`organisation_aliases`).

**Evolution:** When the taxonomy tagging agent encounters an organisation name not in this table, it proposes a new entry through the taxonomy evolution mechanism.

---

## Conventions

- **Canonical name**: The most widely recognised formal name of the organisation.
- **Aliases**: All known variations including abbreviations, stock tickers, former names, and subsidiary names commonly encountered in supply chain documents.
- **Sector**: Primary supply chain sector(s) for this organisation. Uses controlled vocabulary from [controlled_vocabularies.md](../controlled_vocabularies.md).
- **HQ country**: ISO 3166-1 alpha-3 code for headquarters country.
- **Key minerals**: Primary minerals this organisation is associated with.

---

## Diversified miners [extensible]

| Canonical name | Aliases | HQ | Key minerals | Notes |
|---|---|---|---|---|
| BHP Group | BHP, BHP Billiton, BHP Group Limited, BHP Group Ltd | AUS | copper, nickel, manganese | Dual-listed ASX/LSE |
| Rio Tinto | Rio Tinto Group, Rio Tinto plc, Rio Tinto Limited, RIO | GBR/AUS | copper, lithium, rare_earth_elements | Dual-listed LSE/ASX; developing Rincon lithium (Argentina) and Jadar (Serbia) |
| Glencore | Glencore plc, Glencore International, GLEN | CHE | cobalt, copper, nickel | LSE-listed; largest cobalt producer globally via DRC operations |
| Anglo American | Anglo American plc, AAL | GBR | copper, manganese, nickel | LSE-listed; spun off De Beers and SA coal/platinum |
| Vale S.A. | Vale, CVRD, Companhia Vale do Rio Doce | BRA | nickel, copper, cobalt | Major nickel producer (Canada, Indonesia, New Caledonia) |
| South32 | South32 Limited, S32 | AUS | manganese, silicon | Demerged from BHP (2015); South Africa and Australia manganese |
| Vedanta Resources | Vedanta, Vedanta Limited, Sterlite Industries, Hindustan Zinc, VEDL | IND | copper, silicon, rare_earth_elements | Indian conglomerate; London-listed parent (Vedanta Resources Ltd) |
| Tata Steel | Tata Steel Limited, Tata Steel BSL, Tata Steel Europe, Corus | IND | manganese, silicon | India/UK operations; former Corus Group |

---

## Lithium producers [extensible]

| Canonical name | Aliases | HQ | Key minerals | Notes |
|---|---|---|---|---|
| Albemarle Corporation | Albemarle, ALB | USA | lithium | Largest lithium producer (brine: Chile, Atacama; hard-rock: Australia, Greenbushes JV) |
| Sociedad Quimica y Minera | SQM, Sociedad Quimica y Minera de Chile, SQM S.A. | CHL | lithium | Chilean brine operations (Atacama); also iodine, potassium |
| Ganfeng Lithium | Ganfeng, Jiangxi Ganfeng Lithium, Ganfeng Lithium Group, 002460.SZ | CHN | lithium | Vertically integrated; mines + hydroxide/carbonate refining |
| Tianqi Lithium | Tianqi, Chengdu Tianqi, Tianqi Lithium Corporation, 002466.SZ | CHN | lithium | Major stake in Greenbushes (Australia); Kwinana hydroxide plant |
| Pilbara Minerals | Pilbara, PLS, Pilbara Minerals Limited | AUS | lithium | Pilgangoora mine (spodumene); Australia's largest independent lithium miner |
| Mineral Resources | MinRes, Mineral Resources Limited, MIN | AUS | lithium | Mt Marion, Wodgina mines; also mining services |
| Arcadium Lithium | Arcadium, Allkem, Livent, Orocobre, Galaxy Resources | USA/AUS | lithium | Formed from Allkem + Livent merger (2024); multiple former names |
| Sigma Lithium | Sigma, Sigma Lithium Corporation, SGML | BRA | lithium | Grota do Cirilo mine (Brazil); spodumene |
| Cornish Lithium | Cornish Lithium Limited, Cornish Lithium Ltd | GBR | lithium | UK-based exploration; geothermal brine extraction (Cornwall) |
| British Lithium | British Lithium Limited | GBR | lithium | UK-based; hard-rock lithium extraction (Cornwall) |
| Manikaran Power | Manikaran Power Limited | IND | lithium | Indian lithium exploration/processing interests |

---

## Cobalt producers and processors [extensible]

| Canonical name | Aliases | HQ | Key minerals | Notes |
|---|---|---|---|---|
| CMOC Group | CMOC, China Molybdenum, China Moly, CMOC Group Limited, 603993.SS | CHN | cobalt, copper | Tenke Fungurume (DRC) and Kisanfu (DRC) |
| Eurasian Resources Group | ERG, ENRC, Eurasian Natural Resources Corporation | LUX | cobalt, copper, manganese | Private; DRC cobalt through Boss Mining and Metalkol |
| Umicore | Umicore S.A., Umicore N.V. | BEL | cobalt, indium, rare_earth_elements | Refiner and recycler; battery materials |
| Chemaf | Chemicals of Africa, Chemaf S.A.R.L. | COD | cobalt, copper | DRC-based producer |
| Gecamines | La Generale des Carrieres et des Mines, Gecamines S.A. | COD | cobalt, copper | DRC state mining company; JV partner in most DRC operations |

---

## Nickel producers [extensible]

| Canonical name | Aliases | HQ | Key minerals | Notes |
|---|---|---|---|---|
| Norilsk Nickel | Nornickel, MMC Norilsk Nickel, GMKN | RUS | nickel, copper, cobalt | World's largest refined nickel producer; also palladium |
| PT Vale Indonesia | PT Vale, PT International Nickel Indonesia, INCO, PTVI | IDN | nickel | Sorowako laterite operation |
| Nickel Industries | Nickel Industries Limited, NIC | AUS | nickel | Indonesian RKEF operations; listed ASX |
| Sumitomo Metal Mining | SMM, Sumitomo Metal Mining Co. Ltd | JPN | nickel, cobalt, copper | Coral Bay and Taganito (Philippines) HPAL |
| Harita Nickel | PT Harita Nickel, Harita Group | IDN | nickel | Indonesian HPAL; growing MHP producer |
| Hindustan Copper | Hindustan Copper Limited, HCL | IND | copper, nickel | Indian public sector; Khetri, Malanjkhand mines |

---

## Graphite producers [extensible]

| Canonical name | Aliases | HQ | Key minerals | Notes |
|---|---|---|---|---|
| Syrah Resources | Syrah, Syrah Resources Limited, SYR | AUS | graphite | Balama mine (Mozambique); Vidalia active anode material (USA) |
| Tirupati Graphite | Tirupati, Tirupati Graphite plc, TGR | IND/GBR | graphite | India-based; AIM-listed (London); Vatomina (Madagascar) |
| Epsilon Carbon | Epsilon Carbon Private Limited, Epsilon | IND | graphite | Indian synthetic and natural graphite |
| Northern Graphite | Northern Graphite Corporation, NGC | CAN | graphite | Lac des Iles (Canada) |
| BTR New Material | BTR, BTR New Material Group, 835185 | CHN | graphite | World's largest anode material producer |
| Shanshan Technology | Shanshan, Ningbo Shanshan | CHN | graphite | Major anode material producer |

---

## Silicon / polysilicon producers [extensible]

| Canonical name | Aliases | HQ | Key minerals | Notes |
|---|---|---|---|---|
| GCL Technology | GCL-Poly, GCL Technology Holdings, GCL-Poly Energy Holdings, 3800.HK | CHN | silicon | Major polysilicon and FBR granular silicon |
| Tongwei | Tongwei Co. Ltd, Tongwei Solar, 600438.SS | CHN | silicon | Vertically integrated polysilicon + solar cell |
| Daqo New Energy | Daqo, DQ, Daqo New Energy Corp. | CHN | silicon | High-purity polysilicon (Xinjiang) |
| Wacker Chemie | Wacker, Wacker Chemie AG, WCH | DEU | silicon | Polysilicon (Burghausen, Germany; Charleston, USA); also silicones |
| Elkem | Elkem ASA, ELK | NOR | silicon | Metallurgical-grade silicon and ferrosilicon |
| LONGi Green Energy | LONGi, Xi'an LONGi, LONGi Silicon Materials, 601012.SS | CHN | silicon | World's largest monocrystalline wafer and module producer |
| REC Silicon | REC, REC Silicon ASA | NOR | silicon | Moses Lake (USA) FBR polysilicon |
| Ferroglobe | Ferroglobe PLC, Globe Specialty Metals, FerroAtlantica | GBR/USA | silicon | Silicon metal and ferrosilicon; LSE-listed |

---

## Tellurium / indium producers [extensible]

| Canonical name | Aliases | HQ | Key minerals | Notes |
|---|---|---|---|---|
| First Solar | First Solar Inc., FSLR | USA | tellurium | Largest CdTe thin-film PV manufacturer; largest industrial Te consumer |
| 5N Plus | 5N Plus Inc., VNP | CAN | tellurium, indium | Specialty semiconductor and Te/In refiner |
| Korea Zinc | Korea Zinc Co. Ltd, 010130.KS | KOR | indium, tellurium | Major zinc smelter; byproduct In and Te |
| Nyrstar | Nyrstar NV | BEL | indium | Zinc smelting; In recovery |
| Hindustan Zinc | Hindustan Zinc Limited, HZL | IND | indium | Subsidiary of Vedanta; Rajasthan zinc-lead operations; byproduct indium |

---

## Rare earth element producers [extensible]

| Canonical name | Aliases | HQ | Key minerals | Notes |
|---|---|---|---|---|
| China Northern Rare Earth | Northern Rare Earth, Baotou Steel Rare Earth, Inner Mongolia Baotou Steel Rare Earth Hi-Tech, 600111.SS | CHN | rare_earth_elements | World's largest REE producer (Bayan Obo) |
| China Southern Rare Earth | Southern Rare Earth, China Southern Rare Earth Group | CHN | rare_earth_elements | Heavy REE; ionic clay deposits (Jiangxi, Guangdong) |
| Shenghe Resources | Shenghe, Shenghe Resources Holding | CHN | rare_earth_elements | REE trading and processing; strategic partner of MP Materials |
| Lynas Rare Earths | Lynas, Lynas Corporation, Lynas Rare Earths Ltd, LYC | AUS | rare_earth_elements | Mt Weld mine (Australia); LAMP processing (Malaysia); Kalgoorlie cracking/leaching |
| MP Materials | MP Materials Corp., MP, Mountain Pass | USA | rare_earth_elements | Mountain Pass mine (USA); Stage II separation under construction |
| Iluka Resources | Iluka, Iluka Resources Limited, ILU | AUS | rare_earth_elements | Eneabba refinery (Australia); mineral sands |
| Indian Rare Earths | Indian Rare Earths Limited, IREL | IND | rare_earth_elements | Indian government-owned; beach sand mineral processing (Kerala, Odisha, Tamil Nadu) |
| Pensana | Pensana plc, Pensana Rare Earths, PRE | GBR | rare_earth_elements | AIM-listed; Saltend refinery (Humber, UK); Longonjo mine (Angola) |
| Energy Fuels | Energy Fuels Inc., UUUU, EFR | USA | rare_earth_elements | White Mesa mill; REE from monazite processing |

---

## Battery and cathode material producers [extensible]

| Canonical name | Aliases | HQ | Key minerals | Notes |
|---|---|---|---|---|
| CATL | Contemporary Amperex Technology, Contemporary Amperex Technology Co. Limited, 300750.SZ | CHN | lithium, cobalt, nickel, manganese, graphite | World's largest battery manufacturer |
| BYD | BYD Company, Build Your Dreams, BYD Co. Ltd, 002594.SZ | CHN | lithium, manganese | LFP battery manufacturer; vertically integrated EV |
| LG Energy Solution | LGES, LG Chem Energy Solution, LG ES, 373220.KS | KOR | lithium, cobalt, nickel | Major NMC battery manufacturer |
| Samsung SDI | Samsung SDI Co. Ltd, 006400.KS | KOR | lithium, cobalt, nickel | NMC and NCA battery manufacturer |
| Panasonic Energy | Panasonic, Panasonic Energy Co. Ltd | JPN | lithium, cobalt, nickel | Tesla's original battery partner; NCA cells |
| BASF Toda | BASF Toda America, BASF Battery Materials, BASF | DEU | cobalt, nickel, manganese | Cathode active material (CAM) producer |
| Sumitomo Mining (battery materials) | Sumitomo Metal Mining battery division | JPN | nickel, cobalt | NCA cathode precursor |
| Johnson Matthey | Johnson Matthey plc, JMAT | GBR | cobalt, nickel, rare_earth_elements | UK-based; battery materials (exited 2024), PGM catalysts, recycling |
| Tata Chemicals | Tata Chemicals Limited, TCL | IND | lithium | Exploring lithium refining in India/UK (British Lithium partnership) |

---

## Indian sector (additional) [extensible]

| Canonical name | Aliases | HQ | Key minerals | Notes |
|---|---|---|---|---|
| NMDC | NMDC Limited, National Mineral Development Corporation | IND | manganese | Indian public sector miner |
| MOIL | MOIL Limited, Manganese Ore India Limited | IND | manganese | India's largest manganese ore producer |
| NALCO | National Aluminium Company, NALCO Limited | IND | silicon | Aluminium smelter; captive silicon/ferrosilicon potential |
| Khanij Bidesh India | KABIL, Khanij Bidesh India Limited | IND | lithium, cobalt | Indian government JV for overseas critical mineral acquisition |
| Adani Enterprises | Adani, Adani Enterprises Limited, Adani Green | IND | copper, silicon | Mundra copper refinery; polysilicon ambitions |

---

## UK sector (additional) [extensible]

| Canonical name | Aliases | HQ | Key minerals | Notes |
|---|---|---|---|---|
| Cornish Metals | Cornish Metals Inc., CUSN | GBR | copper, indium | South Crofty tin/copper project (Cornwall); listed TSX |
| Mkango Resources | Mkango, Mkango Resources Ltd, MKA | GBR | rare_earth_elements | AIM-listed; Songwe Hill (Malawi) |
| Bushveld Minerals | Bushveld, Bushveld Minerals Limited, BMN | GBR | manganese | AIM-listed; vanadium and manganese (South Africa) |
| Horizonte Minerals | Horizonte, Horizonte Minerals plc, HZM | GBR | nickel | AIM-listed; Araguaia nickel (Brazil) |
| Critical Minerals Association | CMA, Critical Minerals Association UK | GBR | N/A | Industry body, not a producer — but name may appear in policy documents |

---

## Government and institutional bodies [extensible]

These are not producers but frequently appear as document sources or policy actors.

| Canonical name | Aliases | HQ | Role |
|---|---|---|---|
| U.S. Geological Survey | USGS, United States Geological Survey | USA | Primary source for global mineral production/reserves data |
| International Energy Agency | IEA | FRA | Energy transition mineral demand projections |
| British Geological Survey | BGS, British Geological Survey | GBR | UK mineral statistics and criticality assessments |
| Geological Survey of India | GSI | IND | Indian mineral surveys and resource estimation |
| Indian Bureau of Mines | IBM, Indian Bureau of Mines | IND | Indian mineral production statistics and regulation |
| European Commission | EC, EU Commission | BEL | EU Critical Raw Materials Act; policy and regulation |
| World Bank | World Bank Group, IBRD | USA | Development finance for mining; climate minerals reports |
| Benchmark Mineral Intelligence | Benchmark, Benchmark Minerals, BMI | GBR | Market data and price assessments (lithium, cobalt, nickel, graphite, REE) |
| Fastmarkets | Fastmarkets, Metal Bulletin, Industrial Minerals, Fastmarkets MB | GBR | Price reporting agency (PRA) for battery materials and minor metals |
| Shanghai Metals Market | SMM, Shanghai Metals Market | CHN | Chinese metal price data and production statistics |
| Asian Metal | Asian Metal Inc. | CHN | Minor metals market data |
| S&P Global Market Intelligence | S&P Global, SNL Metals & Mining, S&P Global Commodity Insights | USA | Mining industry data, reserves databases |
| Ministry of Mines (India) | MoM India, Ministry of Mines, Government of India | IND | Indian mining policy and production data |
| Department for Business and Trade (UK) | DBT, DBIT, Department for Business, Innovation and Trade | GBR | UK critical minerals strategy |
| NITI Aayog | NITI Aayog, National Institution for Transforming India | IND | Indian policy think tank; critical minerals strategy |
