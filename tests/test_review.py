import json

from chemrx_pipeline.review import assemble_record, validate_record


def test_assemble_adds_properties_without_touching_source_amount(tmp_path):
    source = tmp_path / "draft.json"
    output = tmp_path / "assembled.json"
    source.write_text(
        json.dumps(
            {
                "record_id": "r1",
                "source_pdf": "paper.pdf",
                "source_sha256": "abc",
                "molecules": [
                    {
                        "id": "benzene",
                        "role": "reactant",
                        "reported_amount": {"mass_mg": 1},
                        "structure": {"smiles": "c1ccccc1"},
                        "evidence": [{"page": 1}],
                    }
                ],
                "reaction_components": {"reactants": ["c1ccccc1"], "agents": [], "products": []},
                "reaction_smiles": "c1ccccc1>>c1ccccc1",
            }
        ),
        encoding="utf-8",
    )
    assemble_record(source, output)
    result = json.loads(output.read_text(encoding="utf-8"))
    assert result["molecules"][0]["reported_amount"]["mass_mg"] == 1
    assert result["molecules"][0]["structure"]["properties"]["formula"] == "C6H6"
    assert result["molecules"][0]["structure"]["smarts"]
    assert ">>" in result["reaction_smarts"]
    assert validate_record(output)["valid"] is True

