from chemrx_pipeline.models import MoleculeRecord, ReportedProperty, ReactionRecord


def test_reaction_serializes_stable_shape():
    record = ReactionRecord(record_id="r1", source_pdf="source.pdf", source_sha256="abc")
    record.molecules.append(MoleculeRecord(id="a", name="benzene", role="solvent"))
    record.molecules[0].reported_properties.append(
        ReportedProperty(
            name="appearance",
            value_raw="white solid",
            extraction_agent="gpt-6-astra/low",
            status="source_reviewed",
        )
    )
    payload = record.to_dict()
    assert payload["record_id"] == "r1"
    assert payload["reaction_components"] == {"reactants": [], "agents": [], "products": []}
    assert payload["molecules"][0]["structure"]["recognition_status"] == "unreviewed"
    assert payload["molecules"][0]["reported_properties"][0]["value_raw"] == "white solid"

