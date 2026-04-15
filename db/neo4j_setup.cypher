// Critical Mineral Supply Chain Pipeline — Neo4j Setup
// v0.3.0
// Run against your Neo4j instance via Neo4j Browser or cypher-shell:
//   cypher-shell -u neo4j -p <password> -f neo4j_setup.cypher

// ============================================================
// CONSTRAINTS (enforce uniqueness and existence)
// ============================================================

// Country nodes are unique by ISO alpha-3 code
CREATE CONSTRAINT country_code_unique IF NOT EXISTS
FOR (c:Country) REQUIRE c.code IS UNIQUE;

// Mineral nodes are unique by canonical name + form combination
CREATE CONSTRAINT mineral_name_unique IF NOT EXISTS
FOR (m:Mineral) REQUIRE m.canonical_name IS UNIQUE;

// Organisation nodes are unique by canonical name
CREATE CONSTRAINT organisation_name_unique IF NOT EXISTS
FOR (o:Organisation) REQUIRE o.canonical_name IS UNIQUE;

// Facility nodes are unique by facility_id
CREATE CONSTRAINT facility_id_unique IF NOT EXISTS
FOR (f:Facility) REQUIRE f.facility_id IS UNIQUE;

// Product nodes are unique by canonical name
CREATE CONSTRAINT product_name_unique IF NOT EXISTS
FOR (p:Product) REQUIRE p.canonical_name IS UNIQUE;

// Policy nodes are unique by policy_id
CREATE CONSTRAINT policy_id_unique IF NOT EXISTS
FOR (pol:Policy) REQUIRE pol.policy_id IS UNIQUE;

// Technology nodes are unique by canonical name
CREATE CONSTRAINT technology_name_unique IF NOT EXISTS
FOR (t:Technology) REQUIRE t.canonical_name IS UNIQUE;

// Document nodes are unique by document_id
CREATE CONSTRAINT document_id_unique IF NOT EXISTS
FOR (d:Document) REQUIRE d.document_id IS UNIQUE;

// Entity nodes are unique by entity_id
CREATE CONSTRAINT entity_id_unique IF NOT EXISTS
FOR (e:Entity) REQUIRE e.entity_id IS UNIQUE;

// Chunk nodes are unique by chunk_id
CREATE CONSTRAINT chunk_id_unique IF NOT EXISTS
FOR (ch:Chunk) REQUIRE ch.chunk_id IS UNIQUE;

// ============================================================
// INDEXES (query performance)
// ============================================================

// Country lookup by name (for alias resolution)
CREATE INDEX country_name_index IF NOT EXISTS
FOR (c:Country) ON (c.name);

// Mineral lookup by display name and group
CREATE INDEX mineral_display_index IF NOT EXISTS
FOR (m:Mineral) ON (m.display_name);

CREATE INDEX mineral_group_index IF NOT EXISTS
FOR (m:Mineral) ON (m.mineral_group);

// Organisation lookup by alias (before alias resolution)
CREATE INDEX organisation_alias_index IF NOT EXISTS
FOR (o:Organisation) ON (o.canonical_name);

// Facility lookup by name
CREATE INDEX facility_name_index IF NOT EXISTS
FOR (f:Facility) ON (f.name);

// Tier index (for filtering gold/silver/bronze)
CREATE INDEX country_tier_index IF NOT EXISTS
FOR (c:Country) ON (c.tier);

CREATE INDEX mineral_tier_index IF NOT EXISTS
FOR (m:Mineral) ON (m.tier);

// Document source lookup
CREATE INDEX document_source_index IF NOT EXISTS
FOR (d:Document) ON (d.source_organisation);

// ============================================================
// SEED DATA: Country nodes (major producing/consuming countries)
// These are structural nodes — they exist regardless of documents processed.
// ============================================================

MERGE (c:Country {code: 'AUS'}) SET c.name = 'Australia', c.tier = 'gold';
MERGE (c:Country {code: 'CHN'}) SET c.name = 'China', c.tier = 'gold';
MERGE (c:Country {code: 'IDN'}) SET c.name = 'Indonesia', c.tier = 'gold';
MERGE (c:Country {code: 'IND'}) SET c.name = 'India', c.tier = 'gold';
MERGE (c:Country {code: 'GBR'}) SET c.name = 'United Kingdom', c.tier = 'gold';
MERGE (c:Country {code: 'USA'}) SET c.name = 'United States', c.tier = 'gold';
MERGE (c:Country {code: 'CHL'}) SET c.name = 'Chile', c.tier = 'gold';
MERGE (c:Country {code: 'ARG'}) SET c.name = 'Argentina', c.tier = 'gold';
MERGE (c:Country {code: 'BRA'}) SET c.name = 'Brazil', c.tier = 'gold';
MERGE (c:Country {code: 'COD'}) SET c.name = 'Democratic Republic of the Congo', c.tier = 'gold';
MERGE (c:Country {code: 'ZAF'}) SET c.name = 'South Africa', c.tier = 'gold';
MERGE (c:Country {code: 'RUS'}) SET c.name = 'Russia', c.tier = 'gold';
MERGE (c:Country {code: 'CAN'}) SET c.name = 'Canada', c.tier = 'gold';
MERGE (c:Country {code: 'JPN'}) SET c.name = 'Japan', c.tier = 'gold';
MERGE (c:Country {code: 'KOR'}) SET c.name = 'South Korea', c.tier = 'gold';
MERGE (c:Country {code: 'DEU'}) SET c.name = 'Germany', c.tier = 'gold';
MERGE (c:Country {code: 'NOR'}) SET c.name = 'Norway', c.tier = 'gold';
MERGE (c:Country {code: 'MOZ'}) SET c.name = 'Mozambique', c.tier = 'gold';
MERGE (c:Country {code: 'PHL'}) SET c.name = 'Philippines', c.tier = 'gold';
MERGE (c:Country {code: 'ZWE'}) SET c.name = 'Zimbabwe', c.tier = 'gold';

// ============================================================
// SEED DATA: Mineral group nodes
// ============================================================

MERGE (m:Mineral {canonical_name: 'lithium'})
  SET m.display_name = 'Lithium', m.symbol = 'Li',
      m.mineral_group = 'standalone', m.tier = 'gold';

MERGE (m:Mineral {canonical_name: 'cobalt'})
  SET m.display_name = 'Cobalt', m.symbol = 'Co',
      m.mineral_group = 'standalone', m.tier = 'gold';

MERGE (m:Mineral {canonical_name: 'nickel'})
  SET m.display_name = 'Nickel', m.symbol = 'Ni',
      m.mineral_group = 'standalone', m.tier = 'gold';

MERGE (m:Mineral {canonical_name: 'manganese'})
  SET m.display_name = 'Manganese', m.symbol = 'Mn',
      m.mineral_group = 'standalone', m.tier = 'gold';

MERGE (m:Mineral {canonical_name: 'graphite'})
  SET m.display_name = 'Graphite', m.symbol = 'C',
      m.mineral_group = 'group', m.tier = 'gold';

MERGE (m:Mineral {canonical_name: 'natural_graphite'})
  SET m.display_name = 'Natural Graphite',
      m.mineral_group = 'species', m.tier = 'gold';

MERGE (m:Mineral {canonical_name: 'synthetic_graphite'})
  SET m.display_name = 'Synthetic Graphite',
      m.mineral_group = 'species', m.tier = 'gold';

MERGE (m:Mineral {canonical_name: 'silicon'})
  SET m.display_name = 'Silicon', m.symbol = 'Si',
      m.mineral_group = 'standalone', m.tier = 'gold';

MERGE (m:Mineral {canonical_name: 'tellurium'})
  SET m.display_name = 'Tellurium', m.symbol = 'Te',
      m.mineral_group = 'standalone', m.tier = 'gold';

MERGE (m:Mineral {canonical_name: 'indium'})
  SET m.display_name = 'Indium', m.symbol = 'In',
      m.mineral_group = 'standalone', m.tier = 'gold';

MERGE (m:Mineral {canonical_name: 'copper'})
  SET m.display_name = 'Copper', m.symbol = 'Cu',
      m.mineral_group = 'standalone', m.tier = 'gold';

MERGE (m:Mineral {canonical_name: 'rare_earth_elements'})
  SET m.display_name = 'Rare Earth Elements',
      m.abbreviation = 'REE', m.mineral_group = 'group', m.tier = 'gold';

// REE species
MERGE (m:Mineral {canonical_name: 'neodymium'})
  SET m.display_name = 'Neodymium', m.symbol = 'Nd',
      m.mineral_group = 'species', m.sub_group = 'lree', m.tier = 'gold';

MERGE (m:Mineral {canonical_name: 'praseodymium'})
  SET m.display_name = 'Praseodymium', m.symbol = 'Pr',
      m.mineral_group = 'species', m.sub_group = 'lree', m.tier = 'gold';

MERGE (m:Mineral {canonical_name: 'dysprosium'})
  SET m.display_name = 'Dysprosium', m.symbol = 'Dy',
      m.mineral_group = 'species', m.sub_group = 'hree', m.tier = 'gold';

MERGE (m:Mineral {canonical_name: 'terbium'})
  SET m.display_name = 'Terbium', m.symbol = 'Tb',
      m.mineral_group = 'species', m.sub_group = 'hree', m.tier = 'gold';

MERGE (m:Mineral {canonical_name: 'lanthanum'})
  SET m.display_name = 'Lanthanum', m.symbol = 'La',
      m.mineral_group = 'species', m.sub_group = 'lree', m.tier = 'gold';

MERGE (m:Mineral {canonical_name: 'cerium'})
  SET m.display_name = 'Cerium', m.symbol = 'Ce',
      m.mineral_group = 'species', m.sub_group = 'lree', m.tier = 'gold';

MERGE (m:Mineral {canonical_name: 'yttrium'})
  SET m.display_name = 'Yttrium', m.symbol = 'Y',
      m.mineral_group = 'species', m.sub_group = 'hree', m.tier = 'gold';

// MEMBER_OF relationships for graphite species
MATCH (s:Mineral {canonical_name: 'natural_graphite'}),
      (g:Mineral {canonical_name: 'graphite'})
MERGE (s)-[:MEMBER_OF]->(g);

MATCH (s:Mineral {canonical_name: 'synthetic_graphite'}),
      (g:Mineral {canonical_name: 'graphite'})
MERGE (s)-[:MEMBER_OF]->(g);

// MEMBER_OF relationships for REE species
MATCH (s:Mineral {canonical_name: 'neodymium'}),
      (g:Mineral {canonical_name: 'rare_earth_elements'})
MERGE (s)-[:MEMBER_OF {sub_group: 'lree'}]->(g);

MATCH (s:Mineral {canonical_name: 'praseodymium'}),
      (g:Mineral {canonical_name: 'rare_earth_elements'})
MERGE (s)-[:MEMBER_OF {sub_group: 'lree'}]->(g);

MATCH (s:Mineral {canonical_name: 'dysprosium'}),
      (g:Mineral {canonical_name: 'rare_earth_elements'})
MERGE (s)-[:MEMBER_OF {sub_group: 'hree'}]->(g);

MATCH (s:Mineral {canonical_name: 'terbium'}),
      (g:Mineral {canonical_name: 'rare_earth_elements'})
MERGE (s)-[:MEMBER_OF {sub_group: 'hree'}]->(g);

MATCH (s:Mineral {canonical_name: 'lanthanum'}),
      (g:Mineral {canonical_name: 'rare_earth_elements'})
MERGE (s)-[:MEMBER_OF {sub_group: 'lree'}]->(g);

MATCH (s:Mineral {canonical_name: 'cerium'}),
      (g:Mineral {canonical_name: 'rare_earth_elements'})
MERGE (s)-[:MEMBER_OF {sub_group: 'lree'}]->(g);

MATCH (s:Mineral {canonical_name: 'yttrium'}),
      (g:Mineral {canonical_name: 'rare_earth_elements'})
MERGE (s)-[:MEMBER_OF {sub_group: 'hree'}]->(g);
