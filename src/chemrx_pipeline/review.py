"""Record assembly and validation after source and structure review."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .io import read_json, write_json
from .properties import (
    ChemistryBackendUnavailable,
    calculate_properties,
    reaction_smiles_to_smarts,
    smiles_to_smarts,
    validate_smiles,
)


def assemble_record(input_path: str | Path, output_path: str | Path) -> dict[str, Any]:
    """Attach derived properties without overwriting raw source values."""
    record = read_json(input_path)
    warnings: list[str] = []
    for molecule in record.get("molecules", []):
        structure = molecule.setdefault("structure", {})
        smiles = structure.get("smiles")
        if not smiles:
            structure.setdefault("properties", {"source": "not_run"})
            continue
        try:
            structure["properties"] = calculate_properties(smiles).__dict__
            structure["smarts"] = smiles_to_smarts(smiles)
        except (ChemistryBackendUnavailable, ValueError) as exc:
            structure["properties"] = {"source": "failed", "error": str(exc)}
            warnings.append(f"{molecule.get('id', '<unknown>')}: {exc}")
    record.setdefault("review", {})
    record["review"]["assembly_warnings"] = warnings
    record["review"]["status"] = "structure_reviewed" if not warnings else "unresolved"
    reaction_smiles = record.get("reaction_smiles")
    if reaction_smiles:
        try:
            record["reaction_smarts"] = reaction_smiles_to_smarts(reaction_smiles)
        except (ChemistryBackendUnavailable, ValueError) as exc:
            record["reaction_smarts"] = None
            warnings.append(f"reaction: {exc}")
            record["review"]["status"] = "unresolved"
    write_json(output_path, record)
    return record


def validate_record(path: str | Path) -> dict[str, Any]:
    """Validate record shape and populated SMILES without certifying identity."""
    record = read_json(path)
    errors: list[str] = []
    if not record.get("record_id"):
        errors.append("missing record_id")
    if not record.get("source_pdf"):
        errors.append("missing source_pdf")
    if not record.get("source_sha256"):
        errors.append("missing source_sha256")
    molecules = record.get("molecules")
    if not isinstance(molecules, list) or not molecules:
        errors.append("molecules must be a non-empty list")
        molecules = []
    for index, molecule in enumerate(molecules):
        if not molecule.get("id"):
            errors.append(f"molecules[{index}] missing id")
        structure = molecule.get("structure") or {}
        smiles = structure.get("smiles")
        if smiles:
            try:
                result = validate_smiles(smiles)
            except ChemistryBackendUnavailable as exc:
                errors.append(str(exc))
                continue
            if not result["valid"]:
                errors.append(f"{molecule.get('id')}: invalid SMILES")
        reported = molecule.get("reported_properties", [])
        if not isinstance(reported, list):
            errors.append(f"{molecule.get('id')}: reported_properties must be a list")
        else:
            for prop_index, prop in enumerate(reported):
                if not prop.get("name") or not prop.get("value_raw"):
                    errors.append(
                        f"{molecule.get('id')}: reported_properties[{prop_index}] needs name and value_raw"
                    )
                if prop.get("extraction_agent") in (None, "", "not_run"):
                    errors.append(
                        f"{molecule.get('id')}: reported_properties[{prop_index}] missing Astra/reviewer provenance"
                    )
                for evidence in prop.get("evidence", []):
                    if int(evidence.get("page", 0)) < 1:
                        errors.append(
                            f"{molecule.get('id')}: reported_properties[{prop_index}] invalid evidence page"
                        )
        for evidence in molecule.get("evidence", []):
            if int(evidence.get("page", 0)) < 1:
                errors.append(f"{molecule.get('id')}: invalid evidence page")
    components = record.get("reaction_components", {})
    for key in ("reactants", "agents", "products"):
        if not isinstance(components.get(key, []), list):
            errors.append(f"reaction_components.{key} must be a list")
    return {
        "valid": not errors,
        "errors": errors,
        "record_id": record.get("record_id"),
        "molecule_count": len(molecules),
        "scope": "schema and parser validation; not chemical identity certification",
    }

