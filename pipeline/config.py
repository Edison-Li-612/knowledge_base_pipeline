"""
Central configuration loader for the pipeline.
All settings are read from environment variables (loaded from .env by python-dotenv).
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the project root (two levels up from this file)
_PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(_PROJECT_ROOT / ".env")


class ClarifaiConfig:
    pat: str = os.environ["CLARIFAI_PAT"]
    # Full versioned model URL, used as the model parameter in OpenAI-compatible requests
    deepseek_ocr_url: str = os.getenv(
        "CLARIFAI_DEEPSEEK_OCR_URL",
        "https://clarifai.com/deepseek-ai/deepseek-ocr/models/DeepSeek-OCR/versions/c52cf7da9b1c4095b07e2a1ccb842811",
    )
    openai_base_url: str = "https://api.clarifai.com/v2/ext/openai/v1"


class PostgresConfig:
    host: str = os.getenv("POSTGRES_HOST", "localhost")
    port: int = int(os.getenv("POSTGRES_PORT", "5432"))
    db: str = os.getenv("POSTGRES_DB", "critical_minerals")
    user: str = os.getenv("POSTGRES_USER", "postgres")
    password: str = os.environ["POSTGRES_PASSWORD"]

    @property
    def dsn(self) -> str:
        return (
            f"host={self.host} port={self.port} "
            f"dbname={self.db} user={self.user} password={self.password}"
        )


class Neo4jConfig:
    uri: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user: str = os.getenv("NEO4J_USER", "neo4j")
    password: str = os.environ["NEO4J_PASSWORD"]


class OllamaConfig:
    base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    primary_model: str = os.getenv("OLLAMA_PRIMARY_MODEL", "qwen3:32b")
    fallback_model: str = os.getenv("OLLAMA_FALLBACK_MODEL", "qwen3:27b")
    embedding_model: str = os.getenv("OLLAMA_EMBEDDING_MODEL", "qwen3-embedding:8b")


class ChromaDBConfig:
    host: str = os.getenv("CHROMADB_HOST", "localhost")
    port: int = int(os.getenv("CHROMADB_PORT", "8000"))
    collection: str = os.getenv("CHROMADB_COLLECTION", "critical_minerals_entities")


class StorageConfig:
    documents_base: Path = Path(os.getenv("DOCUMENTS_BASE_PATH", str(_PROJECT_ROOT / "documents")))
    schemas: Path = Path(os.getenv("SCHEMAS_PATH", str(_PROJECT_ROOT / "schemas")))
    skills: Path = Path(os.getenv("SKILLS_PATH", str(_PROJECT_ROOT / "skills")))

    def document_dir(self, document_id: str) -> Path:
        return self.documents_base / document_id

    def pages_dir(self, document_id: str) -> Path:
        return self.document_dir(document_id) / "pages"

    def entities_dir(self, document_id: str) -> Path:
        return self.document_dir(document_id) / "entities"

    def raw_dir(self, document_id: str) -> Path:
        return self.document_dir(document_id) / "raw"

    def chunks_dir(self, document_id: str) -> Path:
        return self.document_dir(document_id) / "chunks"


# Singleton instances — import these in other modules
clarifai = ClarifaiConfig()
postgres = PostgresConfig()
neo4j = Neo4jConfig()
ollama = OllamaConfig()
chromadb = ChromaDBConfig()
storage = StorageConfig()
