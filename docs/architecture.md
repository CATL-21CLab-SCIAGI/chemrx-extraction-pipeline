# Architecture

Stages: PDF -> page/text ingestion -> evidence manifest -> structure
candidates -> reviewed structures -> reaction assembly -> RDKit properties ->
native save/readback -> JSON/CSV/evidence package.

Optional structure candidates come from DECIMER/OCSR or an editable ChemDraw
source. A worker review packet connects candidates to page crops and hashes.
Reaction output stores both composition SMILES and a full coordination sidecar
when the source supports both.

The pipeline separates five claims:

1. Source evidence: what page, crop, or text supports a value.
2. Recognition: candidate structures produced by OCSR or a human.
3. Chemical identity: reviewed connectivity, charge, isotope, and stereo.
4. Reader consistency: RDKit/CDXML/ChemScript/native round trips.
5. Visual/native acceptance: the saved editable figure opens and renders.

A valid SMILES string only establishes parser validity. It does not establish
that the structure was recognized correctly.

