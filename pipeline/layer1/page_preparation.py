"""
Layer 1 — Page Preparation

Converts a raw PDF into per-page PNG images and base64 strings.
Purely deterministic: no LLM involvement.

Output layout (under DOCUMENTS_BASE_PATH):
    DOC-xxxx/
        raw/       original PDF (immutable copy)
        pages/     page_001.png, page_002.png, ...
        manifest.json
"""
from __future__ import annotations

import base64
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

import fitz  # PyMuPDF

from pipeline.config import storage
from pipeline.utils.id_generator import generate_document_id


# DPI target: 150 DPI is equivalent to 2× zoom on a 72-dpi PDF coordinate space.
# Sufficient for DeepSeek OCR; higher improves accuracy at the cost of upload size.
_ZOOM = 2.0          # ~144 DPI; increase to 3.0 for sharper images if OCR quality is poor
_COLORSPACE = fitz.csRGB


def prepare_document(pdf_path: str | Path) -> dict:
    """
    Slice a PDF into page images and create the initial document directory.

    Returns the page_preparation_output schema dict (mirrors /schemas/page_preparation_output.schema.json).

    Args:
        pdf_path: Path to the source PDF.

    Returns:
        {
            "document_id": "DOC-2024-00042",
            "source_file": "/path/to/original.pdf",
            "page_count": 12,
            "pages": [
                {
                    "page_number": 1,
                    "image_path": "/documents/DOC-.../pages/page_001.png",
                    "base64": "<base64_string>",
                    "dimensions": {"width": 2480, "height": 3508}
                },
                ...
            ]
        }
    """
    pdf_path = Path(pdf_path).resolve()
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    document_id = generate_document_id()
    doc_dir = storage.document_dir(document_id)
    pages_dir = storage.pages_dir(document_id)
    raw_dir = storage.raw_dir(document_id)

    # Create directory structure
    pages_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)
    storage.entities_dir(document_id).mkdir(parents=True, exist_ok=True)
    storage.chunks_dir(document_id).mkdir(parents=True, exist_ok=True)

    # Copy original PDF to raw store (immutable reference)
    raw_pdf_path = raw_dir / pdf_path.name
    shutil.copy2(pdf_path, raw_pdf_path)

    # Open PDF and render pages
    pdf = fitz.open(str(pdf_path))
    page_count = len(pdf)
    mat = fitz.Matrix(_ZOOM, _ZOOM)

    pages = []
    for page_index in range(page_count):
        page_num = page_index + 1
        page = pdf[page_index]

        # Render to RGB pixmap
        pix = page.get_pixmap(matrix=mat, colorspace=_COLORSPACE, alpha=False)

        # Save PNG
        image_path = pages_dir / f"page_{page_num:03d}.png"
        pix.save(str(image_path))

        # Encode to base64 for LLM consumption
        image_bytes = pix.tobytes("png")
        b64 = base64.b64encode(image_bytes).decode("utf-8")

        pages.append({
            "page_number": page_num,
            "image_path": str(image_path),
            "base64": b64,
            "dimensions": {
                "width": pix.width,
                "height": pix.height,
            },
        })

    pdf.close()

    output = {
        "document_id": document_id,
        "source_file": str(pdf_path),
        "raw_store_path": str(raw_pdf_path),
        "page_count": page_count,
        "pages": pages,
        "prepared_at": datetime.now(timezone.utc).isoformat(),
    }

    # Write manifest stub (will be filled by document intake)
    _write_manifest_stub(doc_dir, document_id, page_count)

    return output


def load_page_images(document_id: str) -> list[dict]:
    """
    Reload page images for an already-prepared document (e.g., on resume).
    Returns the same pages list as prepare_document, but reads from disk.
    Does NOT re-render — assumes pages/page_NNN.png already exist.
    """
    pages_dir = storage.pages_dir(document_id)
    if not pages_dir.exists():
        raise FileNotFoundError(f"Pages directory not found for {document_id}")

    image_files = sorted(pages_dir.glob("page_*.png"))
    pages = []
    for image_path in image_files:
        page_num = int(image_path.stem.split("_")[1])
        image_bytes = image_path.read_bytes()
        b64 = base64.b64encode(image_bytes).decode("utf-8")

        # Get dimensions without re-rendering
        import struct
        # PNG dimensions are at bytes 16-24
        w = struct.unpack(">I", image_bytes[16:20])[0]
        h = struct.unpack(">I", image_bytes[20:24])[0]

        pages.append({
            "page_number": page_num,
            "image_path": str(image_path),
            "base64": b64,
            "dimensions": {"width": w, "height": h},
        })

    return pages


def _write_manifest_stub(doc_dir: Path, document_id: str, page_count: int) -> None:
    manifest_path = doc_dir / "manifest.json"
    manifest = {
        "document_id": document_id,
        "pipeline_version": "0.3.0",
        "status": "prepared",
        "pages": [
            {"page": i + 1, "status": "pending"}
            for i in range(page_count)
        ],
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    manifest_path.write_text(json.dumps(manifest, indent=2))
