"""Optional external adapters with explicit failure states."""

from __future__ import annotations

import base64
import os
from pathlib import Path
from typing import Any


class AdapterUnavailable(RuntimeError):
    """Raised when an optional adapter is not installed/configured."""


def decimer_from_image(image: str | Path, endpoint: str | None = None) -> dict[str, Any]:
    """Call DECIMER OCSR for one image when explicitly enabled."""
    try:
        import requests  # type: ignore
    except ImportError as exc:
        raise AdapterUnavailable("Install the OCR extra.") from exc
    url = endpoint or os.environ.get(
        "CHEMRX_DECIMER_ENDPOINT",
        "https://api.naturalproducts.net/latest/ocsr/process-upload",
    )
    payload = {
        "file": (
            Path(image).name,
            base64.b64encode(Path(image).read_bytes()).decode("ascii"),
        ),
        "confirm_upload": "true",
    }
    response = requests.post(url, files=payload, timeout=120)
    response.raise_for_status()
    return {"status": "completed", "endpoint": url, "response": response.json()}


def parse_reaction_with_cdxml_toolkit(cdxml: str | Path) -> dict[str, Any]:
    """Parse a CDXML reaction through cdxml-toolkit when installed."""
    try:
        from cdxml_toolkit import parse_reaction  # type: ignore
    except ImportError as exc:
        raise AdapterUnavailable(
            "Install the CDXML extra with pip install -e .[cdxml]."
        ) from exc
    parsed = parse_reaction(str(cdxml))
    return {"status": "completed", "parser": "cdxml-toolkit", "reaction": parsed}


def native_chemdraw_status() -> dict[str, Any]:
    """Report capability; actual native save/rendering is run-specific."""
    try:
        import win32com.client  # type: ignore  # noqa: F401
    except ImportError:
        return {"available": False, "reason": "pywin32_not_installed"}
    return {
        "available": True,
        "reason": "pywin32_imported",
        "note": "ChemDraw executable/license and actual native save must be tested per run.",
    }

