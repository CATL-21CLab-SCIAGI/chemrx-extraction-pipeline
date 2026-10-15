import pytest

from chemrx_pipeline.pdf import inspect_pdf


def test_pdf_backend_error_is_actionable(tmp_path):
    pytest.importorskip("fitz")
    with pytest.raises(Exception):
        inspect_pdf(tmp_path / "missing.pdf")

