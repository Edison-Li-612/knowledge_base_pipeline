"""
ChromaDB collection setup for the pipeline.

ChromaDB runs as an in-process library (no separate service needed).
Run this once to initialise collections, then import the client in other modules.

Usage:
    python db/chromadb_setup.py
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import chromadb
from chromadb.config import Settings


def get_client() -> chromadb.PersistentClient:
    """Return a persistent ChromaDB client stored under ./chromadb_store/."""
    store_path = Path(__file__).parent.parent / "chromadb_store"
    store_path.mkdir(exist_ok=True)
    return chromadb.PersistentClient(
        path=str(store_path),
        settings=Settings(anonymized_telemetry=False),
    )


def setup_collections() -> dict:
    """Create (or get existing) collections. Safe to run multiple times."""
    client = get_client()

    # Main entity collection: content + summary embeddings for all entity types
    entities = client.get_or_create_collection(
        name="critical_minerals_entities",
        metadata={
            "description": "Content and summary embeddings for all extracted entities",
            "hnsw:space": "cosine",
        },
    )

    print(f"[chromadb] Collection 'critical_minerals_entities': "
          f"{entities.count()} vectors")

    return {"entities": entities}


if __name__ == "__main__":
    print("Setting up ChromaDB collections...")
    collections = setup_collections()
    print("Done.")
