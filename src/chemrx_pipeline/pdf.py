"""PDF ingestion with an optional PyMuPDF backend."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .io import sha256_file


class PdfBackendUnavailable(RuntimeError):
    """Raised when PDF features are requested without PyMuPDF."""


def _fitz():
    try:
        import fitz  # type: ignore
    except ImportError as exc:
        raise PdfBackendUnavailable(
            "Install the PDF extra with pip install -e .[pdf]."
        ) from exc
    return fitz


def inspect_pdf(path: str | Path) -> dict[str, Any]:
    fitz = _fitz()
    pdf = Path(path)
    with fitz.open(pdf) as document:
        pages = []
        for index, page in enumerate(document, start=1):
            pages.append(
                {
                    "page": index,
                    "text_chars": len(page.get_text()),
                    "has_images": bool(page.get_images(full=True)),
                }
            )
        return {
            "path": str(pdf),
            "sha256": sha256_file(pdf),
            "page_count": len(document),
            "pages": pages,
        }


def render_pages(
    path: str | Path,
    output_dir: str | Path,
    pages: list[int] | None = None,
    dpi: int = 150,
) -> list[str]:
    fitz = _fitz()
    pdf = Path(path)
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    scale = dpi / 72
    matrix = fitz.Matrix(scale, scale)
    rendered: list[str] = []
    with fitz.open(pdf) as document:
        selected = pages or list(range(1, len(document) + 1))
        for page_number in selected:
            if page_number < 1 or page_number > len(document):
                raise ValueError(f"Page {page_number} is outside 1..{len(document)}")
            output = destination / f"page-{page_number:04d}.png"
            document[page_number - 1].get_pixmap(matrix=matrix, alpha=False).save(output)
            rendered.append(str(output))
    return rendered


def extract_text(path: str | Path, output_dir: str | Path) -> list[str]:
    fitz = _fitz()
    pdf = Path(path)
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    outputs: list[str] = []
    with fitz.open(pdf) as document:
        for page_number, page in enumerate(document, start=1):
            output = destination / f"page-{page_number:04d}.txt"
            output.write_text(page.get_text(), encoding="utf-8")
            outputs.append(str(output))
    return outputs

