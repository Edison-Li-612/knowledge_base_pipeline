"""
Layer 1 — Structural Extraction via DeepSeek OCR (Clarifai OpenAI-compatible API)

Two-pass approach per page:

  Pass 1 — Grounding OCR
    Prompt : "<|grounding|>Convert the document to markdown"
    Returns: page content tagged with grounding markers:
               <|ref|>label<|/ref|><|det|>[[x1,y1,x2,y2]]<|/det|>
             Labels include: text, sub_title, table_caption, table,
                             figure_caption, figure, image, etc.
             Tables are returned as inline HTML <table>...</table>.
             Coordinates are 0–999 normalised to image dimensions.

  Pass 2 — Figure parse  (optional, one call per detected chart/figure crop)
    Prompt : "Parse the figure …"
    Returns: extracted data values, axis labels, and title as markdown.
    Tables do NOT need a second OCR pass — their content is already in the
    grounding output as HTML which we parse directly.

Output per page
───────────────
  pages/
    page_NNN_raw_ocr.md          raw grounding response (debugging / reprocessing)
    page_NNN_full.md             clean page markdown; entity positions replaced with
                                 <!-- TABLE:P01-E001 caption="…" --> placeholders
    page_NNN_annotated.jpg       page PNG with coloured bounding boxes:
                                   red = table, blue = chart/figure, green = image

  entities/PNN-ENNN/
    metadata.json                type, caption, bbox (normalised + pixels), page
    crop.jpg                     JPEG crop of the entity from the original page PNG
    table_markdown.md            (table) markdown table parsed from HTML
    table.csv                    (table) CSV derived from table_markdown
    figure_data.md               (chart/figure, only if parse_figures=True)
"""
from __future__ import annotations

import base64
import csv
import io
import json
import re
import time
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

from openai import OpenAI
from PIL import Image, ImageDraw

from pipeline.config import clarifai as clarifai_cfg, storage
from pipeline.utils.id_generator import generate_entity_id


# ============================================================
# Prompts
# ============================================================

_GROUNDING_PROMPT = "<|grounding|>Convert the document to markdown"

# Exact default prompt for figure parsing — DeepSeek OCR handles both charts
# (returns structured data / markdown tables) and photographs (returns a prose
# description).  The output format is the signal we use to distinguish them.
_FIGURE_PARSE_PROMPT = "Parse the figure"


# ============================================================
# Grounding output parsing
# ============================================================
#
# DeepSeek OCR grounding format (actual):
#
#   <|ref|>label<|/ref|><|det|>[[x1,y1,x2,y2]]<|/det|>
#   content …
#
# Each segment is a (label, bbox, content) triple.
# Coordinates are integers in the 0–999 range.
# Tables arrive as HTML: <table><tr><td>…</td></tr></table>

_SEGMENT_RE = re.compile(
    r'<\|ref\|>(?P<label>[^<]*)<\|/ref\|>'
    r'<\|det\|>\[\[(?P<x1>\d+),\s*(?P<y1>\d+),\s*(?P<x2>\d+),\s*(?P<y2>\d+)[^\]]*\]\]<\|/det\|>'
    r'\n?(?P<content>(?:(?!<\|ref\|>)[\s\S])*)',
)

# Labels that indicate table entities from grounding
_TABLE_LABELS   = {'table', '表格', '表'}
# Labels that carry a caption (may appear before OR after their visual entity)
# Any label ending in '_caption' is also treated as a caption.
_CAPTION_LABELS = {'table_caption', 'figure_caption', 'image_caption',
                   'picture_caption', 'chart_caption', 'caption', '标题'}
# Labels that are pure text — include content in page markdown but do not crop
_TEXT_LABELS    = {'text', 'sub_title', 'title', 'paragraph',
                   'heading', 'header', 'footer', 'footnote'}

# Bounding-box annotation colours
# Pass 1 produces only 'table' and 'image'.
# 'chart' is set after Pass 2 figure parse detects structured data output.
_BBOX_COLOURS = {'table': '#FF3333', 'chart': '#3366FF', 'image': '#33BB33'}


def _label_to_type(label: str) -> str | None:
    """
    Map a DeepSeek grounding label to one of two Pass-1 entity types:
      'table'   — table entity; content parsed from inline HTML
      'image'   — any other visual (figure, chart, photo, map, …)
      'caption' — caption label; associated with adjacent visual entity
      None      — text region; included in page markdown but not cropped

    Pass 1 intentionally produces only 'table' and 'image'.
    Chart vs. photograph distinction is deferred to Pass 2 (figure parse).
    """
    low = label.lower().strip()
    if low in _TEXT_LABELS:
        return None
    if low in _CAPTION_LABELS or low.endswith('_caption'):
        return 'caption'
    if low in _TABLE_LABELS:
        return 'table'
    for kw in _TABLE_LABELS:
        if kw in low:
            return 'table'
    # Everything else — figure, chart, graph, image, photo, map, illustration …
    return 'image'


def _detect_figure_type(figure_parse_output: str) -> str:
    """
    Classify a figure entity as 'chart' or 'image' based on the Pass 2
    figure-parse output.

    DeepSeek returns structured / tabular data when the crop is a chart or
    graph, and prose description when it is a photograph or illustration.

    Returns:
      'chart'  — output contains a markdown table or multiple numeric data
                 lines, indicating a data visualisation.
      'image'  — output is prose description; entity needs domain-level
                 analysis by a later agent.
    """
    # Markdown table is the strongest signal
    if re.search(r'^\|.+\|', figure_parse_output, re.MULTILINE):
        return 'chart'
    # Multiple lines carrying numbers (values, percentages, years) → chart
    numeric_lines = [
        ln for ln in figure_parse_output.splitlines()
        if re.search(r'\b\d+(?:[.,]\d+)?\s*(?:%|kt|mt|t\b|kg|usd|\$)?', ln, re.IGNORECASE)
    ]
    if len(numeric_lines) >= 3:
        return 'chart'
    return 'image'


def _parse_grounding(raw: str) -> tuple[str, list[dict]]:
    """
    Parse the grounding OCR output into:
      - clean page markdown  (grounding markers removed; visual entities replaced
                              with <!-- TYPE:idx caption="…" --> placeholders)
      - list of region dicts: {type, caption, bbox_norm, html_content}

    Caption association rules:
      - A caption BEFORE a visual entity → becomes that entity's caption.
      - A caption AFTER  a visual entity → replaces the entity's caption if the
        entity caption was just the bare label (i.e. no proper caption found yet).
    This handles both orderings that DeepSeek produces depending on page layout.
    """
    regions: list[dict] = []
    pending_caption: str | None = None
    markdown_parts: list[str] = []

    # Preamble before the first <|ref|> tag
    first_match = _SEGMENT_RE.search(raw)
    if first_match:
        preamble = raw[:first_match.start()].strip()
        if preamble:
            markdown_parts.append(preamble)

    for match in _SEGMENT_RE.finditer(raw):
        label   = match.group('label').strip()
        x1      = int(match.group('x1'))
        y1      = int(match.group('y1'))
        x2      = int(match.group('x2'))
        y2      = int(match.group('y2'))
        content = match.group('content').strip()

        etype = _label_to_type(label)

        if etype is None:
            # Pure text region — add to page markdown
            if content:
                markdown_parts.append(content)

        elif etype == 'caption':
            if regions and regions[-1]['caption'] == regions[-1].get('_raw_label'):
                # Trailing caption for the most recent visual entity
                regions[-1]['caption'] = content
                # Update the placeholder already written to markdown_parts
                last_visual_idx = len(regions)
                rtype = regions[-1]['type']
                for i in range(len(markdown_parts) - 1, -1, -1):
                    if f':{last_visual_idx} ' in markdown_parts[i]:
                        markdown_parts[i] = (
                            f'<!-- {rtype.upper()}:{last_visual_idx} caption="{content}" -->'
                        )
                        break
            else:
                # Leading caption — buffer for the next visual entity
                pending_caption = content
            if content:
                markdown_parts.append(content)

        else:
            # Visual entity — Pass 1 produces only 'table' or 'image'
            caption = pending_caption or label
            pending_caption = None

            html_content = content if content.strip().startswith('<table') else None

            visual_idx = len(regions) + 1
            regions.append({
                'type':         etype,
                'caption':      caption,
                '_raw_label':   label,       # kept to detect bare-label captions
                'bbox_norm':    (x1, y1, x2, y2),
                'html_content': html_content,
            })

            markdown_parts.append(
                f'<!-- {etype.upper()}:{visual_idx} caption="{caption}" -->'
            )

    page_markdown = '\n\n'.join(p for p in markdown_parts if p)
    return page_markdown, regions


# ============================================================
# HTML table → markdown / CSV
# ============================================================

class _TableHTMLParser(HTMLParser):
    """Minimal HTML table parser: extracts rows as lists of cell strings."""

    def __init__(self) -> None:
        super().__init__()
        self.rows: list[list[str]] = []
        self._current_row: list[str] = []
        self._current_cell: list[str] = []
        self._in_cell = False

    def handle_starttag(self, tag: str, attrs) -> None:  # noqa: ARG002
        if tag == 'tr':
            self._current_row = []
        elif tag in ('td', 'th'):
            self._current_cell = []
            self._in_cell = True

    def handle_endtag(self, tag: str) -> None:
        if tag in ('td', 'th'):
            self._current_row.append(''.join(self._current_cell).strip())
            self._in_cell = False
        elif tag == 'tr' and self._current_row:
            self.rows.append(self._current_row)

    def handle_data(self, data: str) -> None:
        if self._in_cell:
            self._current_cell.append(data)


def _html_table_to_markdown(html: str) -> str:
    """Convert an HTML table to a markdown table string."""
    parser = _TableHTMLParser()
    parser.feed(html)
    rows = parser.rows
    if not rows:
        return ''
    col_count = max(len(r) for r in rows)

    def _pad(row: list[str]) -> list[str]:
        return row + [''] * (col_count - len(row))

    lines = ['| ' + ' | '.join(_pad(rows[0])) + ' |',
             '| ' + ' | '.join(['---'] * col_count) + ' |']
    for row in rows[1:]:
        lines.append('| ' + ' | '.join(_pad(row)) + ' |')
    return '\n'.join(lines)


def _markdown_table_to_csv(table_md: str) -> str:
    """Convert a markdown table string to CSV."""
    rows = []
    for line in table_md.strip().splitlines():
        line = line.strip()
        if re.match(r'^\|[-:\s|]+\|$', line):
            continue  # separator row
        cells = [c.strip() for c in line.strip('|').split('|')]
        rows.append(cells)
    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    return buf.getvalue()


# ============================================================
# Image utilities
# ============================================================

def _norm_to_px(
    bbox: tuple[int, int, int, int],
    img_w: int,
    img_h: int,
) -> tuple[int, int, int, int]:
    """Convert 0–999 normalised bbox to pixel coordinates, clamped to image."""
    x1, y1, x2, y2 = bbox
    return (
        max(0,     int(x1 / 999 * img_w)),
        max(0,     int(y1 / 999 * img_h)),
        min(img_w, int(x2 / 999 * img_w)),
        min(img_h, int(y2 / 999 * img_h)),
    )


def _crop_jpeg(image: Image.Image, bbox_px: tuple[int, int, int, int]) -> bytes:
    """Crop a region from a PIL image and return JPEG bytes."""
    buf = io.BytesIO()
    image.crop(bbox_px).convert('RGB').save(buf, format='JPEG', quality=92)
    return buf.getvalue()


def _annotate_image(image: Image.Image, entities: list[dict]) -> bytes:
    """
    Draw coloured bounding boxes + labels on the page image.
    Red = table, Blue = chart/figure, Green = image.
    Returns JPEG bytes.
    """
    annotated = image.convert('RGB').copy()
    draw = ImageDraw.Draw(annotated)
    for entity in entities:
        bbox = entity.get('bbox_pixels')
        if not bbox:
            continue
        colour = _BBOX_COLOURS.get(entity['type'], '#FFFF00')
        x1, y1, x2, y2 = bbox
        for offset in range(3):
            draw.rectangle(
                [x1 - offset, y1 - offset, x2 + offset, y2 + offset],
                outline=colour,
            )
        short_id = entity['entity_id'].rsplit('-', 2)[-2] + '-' + entity['entity_id'].rsplit('-', 1)[-1]
        draw.text((x1 + 6, y1 + 4), f"{entity['type'].upper()} {short_id}", fill=colour)
    buf = io.BytesIO()
    annotated.save(buf, format='JPEG', quality=90)
    return buf.getvalue()


# ============================================================
# OpenAI client (lazy-initialised, one instance per process)
# ============================================================

_ocr_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _ocr_client
    if _ocr_client is None:
        _ocr_client = OpenAI(
            base_url=clarifai_cfg.openai_base_url,
            api_key=clarifai_cfg.pat,
        )
    return _ocr_client


def _call_ocr(image_bytes: bytes, text_prompt: str, *, mime: str = 'image/png') -> str:
    """Send image + text prompt to DeepSeek OCR; return raw text response."""
    b64 = base64.b64encode(image_bytes).decode('utf-8')
    response = _get_client().chat.completions.create(
        model=clarifai_cfg.deepseek_ocr_url,
        messages=[
            {
                'role': 'user',
                'content': [
                    {'type': 'image_url',
                     'image_url': {'url': f'data:{mime};base64,{b64}'}},
                    {'type': 'text', 'text': text_prompt},
                ],
            }
        ],
        temperature=0.0,
        stream=False,
    )
    raw = response.choices[0].message.content
    if not raw:
        raise ValueError('DeepSeek OCR returned empty content')
    return raw


def _call_with_retry(fn, attempts: int, delay_s: float, *, label: str) -> str:
    last_err = None
    for attempt in range(attempts + 1):
        try:
            return fn()
        except Exception as exc:
            last_err = exc
            if attempt < attempts:
                time.sleep(delay_s)
    raise RuntimeError(
        f"OCR failed after {attempts + 1} attempts ({label}): {last_err}"
    )


# ============================================================
# Public API
# ============================================================

def extract_page(
    document_id: str,
    page_number: int,
    image_path: str | Path,
    *,
    retry_attempts: int = 2,
    retry_delay_s: float = 3.0,
) -> dict:
    """
    Run two-pass extraction on one page image and persist all extracted entities.

    Pass 1 — Grounding OCR
      Produces 'table' and 'image' entities with bounding boxes.
      Table content is parsed directly from the inline HTML in the grounding output.

    Pass 2 — Figure parse  (always runs for every 'image' entity)
      Sends the crop to "Parse the figure".
      Output is analysed by _detect_figure_type():
        'chart' — structured / tabular data returned → data visualisation
        'image' — prose description returned → photograph / illustration,
                  to be handled by a domain-understanding agent in a later layer.

    Args:
        document_id:    e.g. "DOC-2026-00001"
        page_number:    1-based page number
        image_path:     Path to the per-page PNG rendered by page_preparation
        retry_attempts: Retry budget for transient API failures.
        retry_delay_s:  Sleep between retries.

    Returns:
        Dict with entity summaries for this page.
    """
    image_path = Path(image_path)
    image_bytes = image_path.read_bytes()
    pil_image   = Image.open(image_path)
    img_w, img_h = pil_image.size

    # ── Pass 1: grounding OCR ────────────────────────────────────────────────
    raw_grounding = _call_with_retry(
        lambda: _call_ocr(image_bytes, _GROUNDING_PROMPT, mime='image/png'),
        retry_attempts, retry_delay_s,
        label=f"grounding (doc={document_id}, p={page_number})",
    )

    page_markdown, regions = _parse_grounding(raw_grounding)

    # ── Build entity objects ─────────────────────────────────────────────────
    entities: list[dict] = []

    for idx, region in enumerate(regions, start=1):
        entity_id = generate_entity_id(document_id, page_number, idx)
        bbox_px   = _norm_to_px(region['bbox_norm'], img_w, img_h)
        crop_bytes = _crop_jpeg(pil_image, bbox_px)

        entity: dict = {
            'entity_id':       entity_id,
            'type':            region['type'],
            'caption':         region['caption'],
            'bbox_normalized': region['bbox_norm'],
            'bbox_pixels':     list(bbox_px),
            'source':          {'document_id': document_id, 'page': page_number},
            'extraction_tool': 'deepseek-ocr-grounding',
            'crop_bytes':      crop_bytes,
        }

        # ── Table: parse HTML from grounding output directly ─────────────────
        if region['type'] == 'table':
            html = region.get('html_content') or ''
            if html:
                table_md = _html_table_to_markdown(html)
            else:
                # Fallback: table had no inline HTML — run OCR on the crop
                table_md = _call_with_retry(
                    lambda b=crop_bytes: _call_ocr(
                        b,
                        "Convert this table to clean markdown format. "
                        "Reproduce every row and column exactly as shown.",
                        mime='image/jpeg',
                    ),
                    retry_attempts, retry_delay_s,
                    label=f"table OCR fallback (doc={document_id}, p={page_number}, e={idx})",
                )
            entity['table_markdown'] = table_md
            entity['csv_content']    = _markdown_table_to_csv(table_md)

        # ── Pass 2: figure parse for every image entity ──────────────────────
        if region['type'] == 'image':
            figure_data = _call_with_retry(
                lambda b=crop_bytes: _call_ocr(b, _FIGURE_PARSE_PROMPT, mime='image/jpeg'),
                retry_attempts, retry_delay_s,
                label=f"figure parse (doc={document_id}, p={page_number}, e={idx})",
            )
            entity['figure_data'] = figure_data
            # Upgrade type to 'chart' if the parse output contains structured data
            entity['type'] = _detect_figure_type(figure_data)

        entities.append(entity)

    # ── Persist to filesystem ────────────────────────────────────────────────
    _persist_page(document_id, page_number, raw_grounding, page_markdown,
                  entities, pil_image)

    return {
        'document_id': document_id,
        'page':        page_number,
        'entities':    [_summarise(e) for e in entities],
        'extracted_at': datetime.now(timezone.utc).isoformat(),
    }


def extract_document(
    page_preparation_output: dict,
) -> list[dict]:
    """
    Run structural extraction across all pages of a document.

    Args:
        page_preparation_output: Dict returned by page_preparation.prepare_document()
        parse_figures:           Passed through to extract_page.
    """
    document_id = page_preparation_output['document_id']
    results = []
    for page in page_preparation_output['pages']:
        result = extract_page(
            document_id=document_id,
            page_number=page['page_number'],
            image_path=page['image_path'],
        )
        results.append(result)
    return results


# ============================================================
# Filesystem persistence
# ============================================================

def _persist_page(
    document_id: str,
    page_number: int,
    raw_grounding: str,
    page_markdown: str,
    entities: list[dict],
    pil_image: Image.Image,
) -> None:
    """
    Write all page-level and entity-level artefacts to disk.

    Page artefacts  →  pages/
      page_NNN_raw_ocr.md     raw grounding OCR output
      page_NNN_full.md        clean page markdown with entity placeholders
      page_NNN_annotated.jpg  page with coloured bounding boxes drawn

    Entity artefacts  →  entities/PNN-ENNN/
      metadata.json
      crop.jpg
      table_markdown.md + table.csv   (table entities)
      figure_data.md                  (chart/figure with parse_figures=True)
    """
    pages_dir     = storage.pages_dir(document_id)
    entities_base = storage.entities_dir(document_id)
    prefix        = f'page_{page_number:03d}'

    (pages_dir / f'{prefix}_raw_ocr.md').write_text(raw_grounding,  encoding='utf-8')
    (pages_dir / f'{prefix}_full.md').write_text(page_markdown,    encoding='utf-8')
    (pages_dir / f'{prefix}_annotated.jpg').write_bytes(_annotate_image(pil_image, entities))

    for entity in entities:
        entity_id  = entity['entity_id']
        subfolder  = '-'.join(entity_id.split('-')[-2:])   # e.g. P03-E002
        entity_dir = entities_base / subfolder
        entity_dir.mkdir(parents=True, exist_ok=True)

        (entity_dir / 'metadata.json').write_text(
            json.dumps({
                'entity_id':       entity_id,
                'type':            entity['type'],
                'document_id':     document_id,
                'page':            page_number,
                'caption':         entity.get('caption', ''),
                'bbox_normalized': entity.get('bbox_normalized'),
                'bbox_pixels':     entity.get('bbox_pixels'),
                'extraction_tool': entity.get('extraction_tool'),
                'extracted_at':    datetime.now(timezone.utc).isoformat(),
                'source':          entity.get('source'),
            }, indent=2, ensure_ascii=False)
        )

        if entity.get('crop_bytes'):
            (entity_dir / 'crop.jpg').write_bytes(entity['crop_bytes'])

        if entity['type'] == 'table':
            if entity.get('table_markdown'):
                (entity_dir / 'table_markdown.md').write_text(
                    entity['table_markdown'], encoding='utf-8'
                )
            if entity.get('csv_content'):
                (entity_dir / 'table.csv').write_text(
                    entity['csv_content'], encoding='utf-8'
                )

        if entity.get('figure_data'):
            (entity_dir / 'figure_data.md').write_text(
                entity['figure_data'], encoding='utf-8'
            )


def _summarise(entity: dict) -> dict:
    """Lightweight entity summary for the extraction output schema."""
    s = {
        'entity_id':       entity['entity_id'],
        'type':            entity['type'],
        'caption':         entity.get('caption', ''),
        'bbox_normalized': entity.get('bbox_normalized'),
        'source':          entity.get('source'),
    }
    if entity['type'] == 'table':
        tm = entity.get('table_markdown', '')
        s['table_preview'] = tm.splitlines()[0] if tm else ''
    return s

