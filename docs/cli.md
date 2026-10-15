# CLI reference

## Ingest a PDF

    chemrx ingest paper.pdf --output runs/paper-001 --dpi 150

This writes page text, rendered page images, a run manifest, and an evidence
manifest. It does not invent structures.

## Create a linked draft

    chemrx draft paper.pdf --output runs/paper-001 --record-id rxn-0001

This performs ingestion and writes an empty structure-reviewed record whose
page images and text files are already linked by relative run paths. Fill the
record after the source and structure review stages.

## Recognize one crop

The CLI or Python adapter can be called from a controlled script:

    chemrx recognize runs/paper-001/pages/page-0012.png -o runs/paper-0011/recognition/page-0012.json

    from chemrx_pipeline.adapters import decimer_from_image
    result = decimer_from_image("runs/paper-001/pages/page-0012.png")

Save the returned response next to the crop and record its endpoint and image
hash. Review the candidate against the source before populating smiles. The
adapter does not claim chemical identity and does not silently change endpoint
or model after a failure.

For multiple reviewed crops, use examples/crops-manifest.json:

    chemrx recognize-batch examples/crops-manifest.json -o runs/paper-001/recognition.json

## Assemble reviewed chemistry

Start from examples/record-template.json, fill source evidence, structures,
reaction components, conditions, and results, then run:

    chemrx assemble reviewed-record.json -o outputs/rxn-0001.json
    chemrx validate-record outputs/rxn-0001.json

Assembly calculates properties for populated SMILES and keeps undefined
materials as null. It never replaces raw reported values. Assembly also writes
molecule SMARTS and, when a reviewed reaction SMILES is present, reaction
SMARTS. SMARTS is a derived query pattern and does not replace the reviewed
SMILES or source structure.

