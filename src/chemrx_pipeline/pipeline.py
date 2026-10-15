"""Evidence-first pipeline orchestration."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .io import sha256_file, write_json
from .models import EvidenceRef, ReactionRecord, RunManifest
from .pdf import extract_text, inspect_pdf, render_pages

PIPELINE_VERSION = "0.1.0"


def create_run(pdf: str | Path, output: str | Path) -> RunManifest:
    source = Path(pdf).resolve()
    destination = Path(output).resolve()
    destination.mkdir(parents=True, exist_ok=True)
    manifest = RunManifest(
        run_id=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        input_pdf=str(source),
        input_sha256=sha256_file(source),
        output_dir=str(destination),
        pipeline_version=PIPELINE_VERSION,
    )
    write_json(destination / "run-manifest.json", manifest.to_dict())
    return manifest


def ingest_pdf(pdf: str | Path, output: str | Path, dpi: int = 150) -> dict[str, Any]:
    """Write page text, page images, and a reproducible evidence manifest."""
    destination = Path(output)
    manifest = create_run(pdf, destination)
    inspection = inspect_pdf(pdf)
    text_files = extract_text(pdf, destination / "text")
    image_files = render_pages(pdf, destination / "pages", dpi=dpi)
    evidence = {
        "input": inspection,
        "text_files": text_files,
        "image_files": image_files,
        "sha256": {
            "text": {str(p): sha256_file(p) for p in text_files},
            "images": {str(p): sha256_file(p) for p in image_files},
        },
    }
    manifest.stages.append(
        {"name": "ingest", "status": "completed", "page_count": inspection["page_count"]}
    )
    write_json(destination / "run-manifest.json", manifest.to_dict())
    write_json(destination / "evidence-manifest.json", evidence)
    return evidence


def write_reaction(record: ReactionRecord, output: str | Path) -> Path:
    destination = Path(output)
    destination.mkdir(parents=True, exist_ok=True)
    path = destination / f"{record.record_id}.json"
    write_json(path, record.to_dict())
    return path


def create_draft_record(
    pdf: str | Path,
    output: str | Path,
    record_id: str = "rxn-0001",
    dpi: int = 150,
) -> Path:
    """Ingest a PDF and create an evidence-linked, structure-empty draft."""
    destination = Path(output)
    evidence = ingest_pdf(pdf, destination, dpi=dpi)
    pages = list(range(1, int(evidence["input"]["page_count"]) + 1))
    record = ReactionRecord(
        record_id=record_id,
        source_pdf=str(Path(pdf).resolve()),
        source_sha256=evidence["input"]["sha256"],
        pages=pages,
        evidence=[
            EvidenceRef(
                page=page,
                image=str(destination / "pages" / f"page-{page:04d}.png"),
                text=str(destination / "text" / f"page-{page:04d}.txt"),
            )
            for page in pages
        ],
    )
    return write_reaction(record, destination / "draft")

