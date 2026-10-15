import pytest

from chemrx_pipeline.properties import calculate_properties, validate_smiles


def test_invalid_smiles_is_reported():
    pytest.importorskip("rdkit")
    assert validate_smiles("not-a-smiles")["valid"] is False


def test_benzene_properties():
    pytest.importorskip("rdkit")
    props = calculate_properties("c1ccccc1")
    assert props.formula == "C6H6"
    assert props.heavy_atom_count == 6
    assert props.formal_charge == 0

