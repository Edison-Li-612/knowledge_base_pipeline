"""
Deterministic ID generation for the pipeline.

All IDs are unique, human-readable, and traceable.
"""
from __future__ import annotations

import threading
from datetime import datetime, timezone

_lock = threading.Lock()
_counters: dict[str, int] = {}


def _next(prefix: str) -> str:
    with _lock:
        _counters[prefix] = _counters.get(prefix, 0) + 1
        return f"{prefix}-{datetime.now(timezone.utc).strftime('%Y')}-{_counters[prefix]:05d}"


def generate_document_id() -> str:
    """e.g. DOC-2024-00042"""
    return _next("DOC")


def generate_entity_id(document_id: str, page: int, entity_num: int) -> str:
    """e.g. DOC-2024-00042-P01-E002"""
    return f"{document_id}-P{page:02d}-E{entity_num:03d}"


def generate_chunk_id(entity_id: str, level: int, chunk_index: int | None = None) -> str:
    """
    e.g. DOC-2024-00042-P01-E001-L0      (parent chunk)
         DOC-2024-00042-P01-E001-L1-C002  (child chunk)
    """
    if level == 0:
        return f"{entity_id}-L0"
    return f"{entity_id}-L{level}-C{chunk_index:03d}"


def generate_relationship_id(document_id: str) -> str:
    """e.g. REL-2024-00042"""
    with _lock:
        key = f"REL-{document_id}"
        _counters[key] = _counters.get(key, 0) + 1
        return f"REL-{document_id}-{_counters[key]:03d}"


def generate_ambiguity_id(document_id: str) -> str:
    """e.g. AMB-2024-00042-001"""
    with _lock:
        key = f"AMB-{document_id}"
        _counters[key] = _counters.get(key, 0) + 1
        return f"AMB-{document_id}-{_counters[key]:03d}"


def generate_step_id(document_id: str, page: int, step_type: str) -> str:
    """e.g. STEP-00042-P01-TAG-001"""
    doc_num = document_id.split("-")[-1]
    with _lock:
        key = f"STEP-{document_id}-P{page}-{step_type}"
        _counters[key] = _counters.get(key, 0) + 1
        return f"STEP-{doc_num}-P{page:02d}-{step_type.upper()}-{_counters[key]:03d}"


def generate_source_id() -> str:
    """e.g. SRC-0003"""
    return _next("SRC")
