# Structure-review worker packet

Use one current reaction only. Read the source pages and the ChemDraw skill
before making structures. Work only inside the assigned worker directory.

Return:

- a source page/crop manifest with SHA-256;
- one entry for every reported molecule, including undefined materials;
- reviewed composition SMILES and, when supported, a full coordination sidecar;
- MOL, editable CDXML, native preview, and readback reports;
- reaction-side arrays for reactants, agents, and products;
- candidate structures and rejected candidates with reasons;
- unresolved stereo, charge, isotope, coordination, or source conflicts;
- a final report that says passed, unresolved, or failed for every check.

Do not silently replace a failed OCR endpoint or model. Do not infer an
absolute configuration from layout coordinates. Do not claim native or
cross-reader success from an unexecuted check.

