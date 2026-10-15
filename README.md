# ChemRx Extraction Pipeline

ChemRx is an evidence-first workflow for extracting chemical structures,
reactions, and molecular properties from chemistry literature PDFs. It is
designed for supporting information and experimental sections where a reaction
figure, a paragraph, a general procedure, and characterization pages must be
reconciled into one auditable record.

The repository contains the reusable pipeline, not the 100-record delivery
archive. The completed CATL structured draft remains a separate evidence-heavy
artifact so this code repository stays cloneable and reviewable.

## What it produces

For each source PDF the pipeline can produce:

- page text and rendered page images with SHA-256 evidence manifests;
- a complete molecule inventory with roles and source amounts;
- reviewed composition SMILES and optional full coordination sidecars;
- derived molecule SMARTS and reaction SMARTS after review;
- reaction-side arrays (reactants, agents, products);
- RDKit molecular properties;
- Astra-extracted natural-language properties with raw wording, parsed values,
  units, evidence pages, and reviewer provenance;
- conditions, results, and ordered workup steps;
- editable MOL/CDXML and native ChemDraw previews when those adapters are available;
- a review report that distinguishes passed, unresolved, and failed checks.

## Quick start

    py -m venv .venv
    . .venv/Scripts/Activate.ps1
    pip install -e ".[all,dev]"
    chemrx draft .\paper-supporting-information.pdf -o .\runs\paper-001 --record-id rxn-0001
    chemrx ingest .\paper-supporting-information.pdf -o .\runs\paper-001
    chemrx validate-smiles "c1ccccc1"
    chemrx properties "c1ccccc1"
    chemrx doctor
    pytest

The ingest command is deterministic for a given PDF, DPI, and PyMuPDF
version. It does not claim that page rendering or text extraction has
identified a structure. Recognition and review are explicit stages. A PDF
alone is enough to start
ingestion, but reliable chemical identity still requires image crops and
reviewed candidates; arbitrary PDF OCR is not chemical ground truth.

## Review-first workflow

1. Ingest the PDF and freeze the source SHA-256.
2. Select pages containing the experimental instance, scheme, general
   procedure, workup, and characterization.
3. Create a worker packet from examples/record-template.json.
4. Generate OCSR candidates only through an explicit adapter and retain the
   response, endpoint, image hash, and candidate list.
5. Review connectivity, charge, isotope, stereochemistry, salt fragments,
   metal coordination, and source identity against the original image.
6. Save editable MOL/CDXML and run parser/native readback checks.
7. Calculate RDKit properties and derive SMARTS only for accepted structures.
8. Write the reaction record and evidence manifest. Package only records that
   have closed source evidence and no unresolved core identity.

The detailed rules are in docs/methodology.md, docs/architecture.md,
docs/worker-prompt.md, docs/astra-property-prompt.md, and
docs/requirements-audit.md.

## Optional integrations

- PyMuPDF: PDF text and page rendering (pdf extra).
- RDKit: parsing, canonicalization, and molecular properties (chemistry extra).
- DECIMER/OCSR: candidate structure recognition (ocr extra plus an explicitly
  configured endpoint).
- cdxml-toolkit: editable CDXML reaction parsing (cdxml extra).
- ChemDraw on Windows: native save and render through a separately configured
  licensed installation. The pipeline reports capability and requires a
  run-specific native acceptance receipt.

No adapter silently changes endpoint, model, or representation after failure.

RDKit properties and literature-reported properties are separate channels.
The latter are stored under molecules[].reported_properties and are extracted
from source text/figures by the configured Astra reviewer. Raw wording and
source evidence remain available for review.

## Scope and limitations

This project extracts and organizes evidence. It does not certify chemical
truth, infer missing experimental values, assign unknown absolute
stereochemistry, or turn a valid SMILES parse into a recognition claim. Full
coordination and charge-balanced composition are separate representations when
the literature supports both. Raw HRMS formulas, anomalous masses, conflicting
solvents, and crystal occupancy are preserved as reported and diagnosed
separately.

## Provenance

The design is based on the CATL 100-record structured literature-draft
workflow. That delivery is referenced only as method and validation
provenance; its PDFs and generated structures are not redistributed here.

