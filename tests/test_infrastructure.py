"""
Infrastructure connectivity test.
Run this after setting up all services to verify the pipeline can reach them.

Usage:
    python tests/test_infrastructure.py

Each check prints PASS or FAIL with a reason.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

results = []


def check(name: str, fn):
    try:
        fn()
        print(f"  PASS  {name}")
        results.append((name, True, None))
    except Exception as exc:
        print(f"  FAIL  {name}: {exc}")
        results.append((name, False, str(exc)))


# ──────────────────────────────────────────
# 1. Config loads without missing env vars
# ──────────────────────────────────────────
print("\n[1/6] Config")

def _check_config():
    from pipeline.config import clarifai, postgres, neo4j, ollama, chromadb, storage
    assert clarifai.pat, "CLARIFAI_PAT not set"
    assert postgres.password, "POSTGRES_PASSWORD not set"
    assert neo4j.password, "NEO4J_PASSWORD not set"
    storage.documents_base.mkdir(parents=True, exist_ok=True)

check("Config loads from .env", _check_config)


# ──────────────────────────────────────────
# 2. PostgreSQL
# ──────────────────────────────────────────
print("\n[2/6] PostgreSQL")

def _check_postgres_connect():
    import psycopg2
    from pipeline.config import postgres
    conn = psycopg2.connect(postgres.dsn)
    conn.close()

def _check_postgres_schema():
    import psycopg2
    from pipeline.config import postgres
    conn = psycopg2.connect(postgres.dsn)
    cur = conn.cursor()
    cur.execute("""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    tables = {row[0] for row in cur.fetchall()}
    conn.close()
    expected = {
        "documents", "processing_manifests", "production_volumes",
        "trade_flows", "prices", "reserves", "staged_tables",
        "pipeline_logs", "taxonomy_evolution_queue", "conversion_factors",
        "organisation_aliases", "document_sources", "ambiguity_log",
        "contradiction_log", "tier_transitions",
    }
    missing = expected - tables
    if missing:
        raise AssertionError(f"Tables not yet created: {missing}. Run: psql -U postgres -d critical_minerals -f db/postgres_schema.sql")

check("PostgreSQL connection", _check_postgres_connect)
check("PostgreSQL schema tables exist", _check_postgres_schema)


# ──────────────────────────────────────────
# 3. Neo4j
# ──────────────────────────────────────────
print("\n[3/6] Neo4j")

def _check_neo4j_connect():
    from neo4j import GraphDatabase
    from pipeline.config import neo4j
    driver = GraphDatabase.driver(neo4j.uri, auth=(neo4j.user, neo4j.password))
    driver.verify_connectivity()
    driver.close()

def _check_neo4j_seed():
    from neo4j import GraphDatabase
    from pipeline.config import neo4j
    driver = GraphDatabase.driver(neo4j.uri, auth=(neo4j.user, neo4j.password))
    with driver.session() as session:
        result = session.run("MATCH (m:Mineral) RETURN count(m) AS cnt")
        cnt = result.single()["cnt"]
    driver.close()
    if cnt == 0:
        raise AssertionError("No Mineral nodes found. Run neo4j_setup.cypher in Neo4j Browser.")

check("Neo4j connection", _check_neo4j_connect)
check("Neo4j seed data (Mineral nodes)", _check_neo4j_seed)


# ──────────────────────────────────────────
# 4. ChromaDB
# ──────────────────────────────────────────
print("\n[4/6] ChromaDB")

def _check_chromadb():
    from db.chromadb_setup import setup_collections
    collections = setup_collections()
    assert "entities" in collections

check("ChromaDB collection setup", _check_chromadb)


# ──────────────────────────────────────────
# 5. Ollama
# ──────────────────────────────────────────
print("\n[5/6] Ollama")

def _check_ollama_running():
    import urllib.request
    from pipeline.config import ollama
    url = f"{ollama.base_url}/api/tags"
    with urllib.request.urlopen(url, timeout=5) as resp:
        assert resp.status == 200

def _check_ollama_models():
    import json, urllib.request
    from pipeline.config import ollama
    url = f"{ollama.base_url}/api/tags"
    with urllib.request.urlopen(url, timeout=5) as resp:
        data = json.loads(resp.read())
    available = {m["name"] for m in data.get("models", [])}
    for model in [ollama.primary_model, ollama.embedding_model]:
        # Partial match — "qwen3:32b" matches "qwen3:32b-instruct-q4_K_M" etc.
        matched = any(model in a or a.startswith(model.split(":")[0]) for a in available)
        if not matched:
            raise AssertionError(f"Model '{model}' not found in Ollama. Available: {available}")

check("Ollama service running", _check_ollama_running)
check("Ollama required models available", _check_ollama_models)


# ──────────────────────────────────────────
# 6. Clarifai / DeepSeek OCR
# ──────────────────────────────────────────
print("\n[6/6] Clarifai DeepSeek OCR")

def _check_clarifai_auth():
    from openai import OpenAI
    from pipeline.config import clarifai
    # Instantiate OpenAI-compatible client pointing at Clarifai
    client = OpenAI(base_url=clarifai.openai_base_url, api_key=clarifai.pat)
    assert client is not None
    assert clarifai.deepseek_ocr_url.startswith("https://clarifai.com/"), \
        f"Unexpected model URL: {clarifai.deepseek_ocr_url}"

check("Clarifai OpenAI-compatible client instantiates", _check_clarifai_auth)


# ──────────────────────────────────────────
# Summary
# ──────────────────────────────────────────
print()
passed = sum(1 for _, ok, _ in results if ok)
total = len(results)
print(f"Results: {passed}/{total} checks passed")

if passed < total:
    print("\nFailed checks:")
    for name, ok, reason in results:
        if not ok:
            print(f"  - {name}: {reason}")
    sys.exit(1)
else:
    print("All infrastructure checks passed.")
