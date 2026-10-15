"""Molecular property calculation using optional RDKit."""

from __future__ import annotations

from .models import PropertySet


class ChemistryBackendUnavailable(RuntimeError):
    """Raised when RDKit-backed features are requested without RDKit."""


def _rdkit():
    try:
        from rdkit import Chem  # type: ignore
        from rdkit.Chem import Crippen, Descriptors, Lipinski, rdMolDescriptors  # type: ignore
    except ImportError as exc:
        raise ChemistryBackendUnavailable(
            "Install the chemistry extra with pip install -e .[chemistry]."
        ) from exc
    return Chem, Crippen, Descriptors, Lipinski, rdMolDescriptors


def calculate_properties(smiles: str) -> PropertySet:
    Chem, Crippen, Descriptors, Lipinski, rdMolDescriptors = _rdkit()
    molecule = Chem.MolFromSmiles(smiles)
    if molecule is None:
        raise ValueError(f"RDKit cannot parse SMILES: {smiles}")
    return PropertySet(
        formula=rdMolDescriptors.CalcMolFormula(molecule),
        exact_mass=float(Descriptors.ExactMolWt(molecule)),
        molecular_weight=float(Descriptors.MolWt(molecule)),
        formal_charge=int(Chem.GetFormalCharge(molecule)),
        heavy_atom_count=int(molecule.GetNumHeavyAtoms()),
        h_bond_donors=int(Lipinski.NumHDonors(molecule)),
        h_bond_acceptors=int(Lipinski.NumHAcceptors(molecule)),
        rotatable_bonds=int(Lipinski.NumRotatableBonds(molecule)),
        tpsa=float(rdMolDescriptors.CalcTPSA(molecule)),
        logp=float(Crippen.MolLogP(molecule)),
        source="rdkit",
    )


def validate_smiles(smiles: str) -> dict[str, object]:
    Chem, *_ = _rdkit()
    molecule = Chem.MolFromSmiles(smiles)
    if molecule is None:
        return {"valid": False, "smiles": smiles, "error": "parse_failed"}
    return {
        "valid": True,
        "smiles": smiles,
        "canonical_smiles": Chem.MolToSmiles(molecule, canonical=True),
    }

