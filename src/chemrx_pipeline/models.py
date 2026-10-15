"""Stable, dependency-light data model for pipeline outputs."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class EvidenceRef:
    page: int
    image: str | None = None
    text: str | None = None
    excerpt: str | None = None
    sha256: str | None = None


@dataclass
class PropertySet:
    formula: str | None = None
    exact_mass: float | None = None
    molecular_weight: float | None = None
    formal_charge: int | None = None
    heavy_atom_count: int | None = None
    h_bond_donors: int | None = None
    h_bond_acceptors: int | None = None
    rotatable_bonds: int | None = None
    tpsa: float | None = None
    logp: float | None = None
    source: str = "not_run"


@dataclass
class StructureArtifact:
    smiles: str | None = None
    molfile: str | None = None
    cdxml: str | None = None
    native_preview: str | None = None
    candidate_smiles: list[str] = field(default_factory=list)
    recognition_status: str = "unreviewed"
    review_notes: list[str] = field(default_factory=list)
    properties: PropertySet = field(default_factory=PropertySet)


@dataclass
class MoleculeRecord:
    id: str
    name: str | None
    role: str
    stage: str | None = None
    current_use: bool | None = None
    reported_amount: dict[str, Any] | None = None
    structure: StructureArtifact = field(default_factory=StructureArtifact)
    evidence: list[EvidenceRef] = field(default_factory=list)
    context: dict[str, Any] = field(default_factory=dict)


@dataclass
class ReactionRecord:
    record_id: str
    source_pdf: str
    source_sha256: str
    title: str | None = None
    doi: str | None = None
    pages: list[int] = field(default_factory=list)
    molecules: list[MoleculeRecord] = field(default_factory=list)
    reaction_smiles: str | None = None
    reaction_components: dict[str, list[str]] = field(
        default_factory=lambda: {"reactants": [], "agents": [], "products": []}
    )
    conditions: dict[str, Any] = field(default_factory=dict)
    workup: list[dict[str, Any]] = field(default_factory=list)
    results: dict[str, Any] = field(default_factory=dict)
    evidence: list[EvidenceRef] = field(default_factory=list)
    review: dict[str, Any] = field(
        default_factory=lambda: {
            "status": "draft",
            "structure_agent": "not_run",
            "source_review": "not_run",
            "issues": [],
        }
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class RunManifest:
    run_id: str
    input_pdf: str
    input_sha256: str
    output_dir: str
    pipeline_version: str
    stages: list[dict[str, Any]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

