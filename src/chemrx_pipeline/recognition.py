"""Batch orchestration for explicit structure-recognition crops."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .adapters import decimer_from_image
from .io import read_json, sha256_file, write_json


def recognize_batch(
    manifest_path: str | Path,
    output_path: str | Path,
    endpoint: str | None = None,
) -> dict[str, Any]:
    """Run DECIMER on a user-reviewed crop manifest.

    The manifest is intentionally explicit: automatic page-wide OCSR is not
    treated as reliable structure identity. Each item must name its crop and
    source page so a reviewer can trace the result.
    """
    manifest = read_json(manifest_path)
    if isinstance(manifest, list):
        items = manifest
    else:
        items = manifest.get("images", [])
    results: list[dict[str, Any]] = []
    for item in items:
        image = Path(item["image"])
        result = decimer_from_image(image, endpoint=endpoint)
        results.append(
            {
                "id": item.get("id"),
                "role": item.get("role"),
                "page": item.get("page"),
                "image": str(image),
                "image_sha256": sha256_file(image),
                "recognition": result,
            }
        )
    payload = {
        "status": "completed",
        "manifest": str(manifest_path),
        "endpoint": endpoint,
        "items": results,
        "review_required": True,
    }
    write_json(output_path, payload)
    return payload

