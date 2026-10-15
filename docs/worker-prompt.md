# Structure-review worker packet

Use one current reaction only. Read the source pages and the ChemDraw skill
before making structures. Work only inside the assigned worker directory.

Return:

- a source page/crop manifest with SHA-256;
- one entry for every reported molecule, including undefined materials;
- natural-language and figure properties for every molecule when reported:
  appearance, physical state, melting/boiling point, NMR, HRMS, IR, UV,
  optical rotation, crystal data, solubility, and other source observations;
- reviewed composition SMILES and, when supported, a full coordination sidecar;
- MOL, editable CDXML, native preview, and readback reports;
- reaction-side arrays for reactants, agents, and products;
- candidate structures and rejected candidates with reasons;
- unresolved stereo, charge, isotope, coordination, or source conflicts;
- raw property text, parsed value, unit, evidence page/crop, and extraction
  provenance. Use gpt-6-astra/low when configured by the calling workflow;
- a final report that says passed, unresolved, or failed for every check.

Do not silently replace a failed OCR endpoint or model. Do not infer an
absolute configuration from layout coordinates. Do not claim native or
cross-reader success from an unexecuted check.

For each reported property, keep value_raw exactly as read, put any parsed
range or numeric value in value_normalized, and attach the source page/crop.
Do not calculate a missing value and label it as reported. If the figure or
text is ambiguous, set status to unresolved and explain why.

