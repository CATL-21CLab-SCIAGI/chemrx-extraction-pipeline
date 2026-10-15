# Astra property-extraction prompt

Use the configured gpt-6-astra/low worker for one current reaction and its
source pages only. Read the whole source page before reading a crop. Extract
natural-language molecular properties for every identified molecule and
product. Do not infer values from a general procedure, neighboring compound,
or a different scale variant.

Return a JSON array. Each item must contain:

    {
      "molecule_id": "product_1",
      "name": "melting_point",
      "value_raw": "mp 192-193 °C",
      "value_normalized": {"min": 192, "max": 193},
      "unit": "°C",
      "category": "physical",
      "extraction_agent": "gpt-6-astra/low",
      "confidence": "high",
      "status": "source_reviewed",
      "evidence": [
        {"page": 24, "image": "evidence/page-0024.png",
         "excerpt": "mp 192-193 °C", "sha256": "current-image-sha256"}
      ],
      "notes": []
    }

Read and preserve, when reported:

- appearance and physical state;
- melting, boiling, decomposition, or crystallization temperatures;
- solubility and crystallization behavior;
- NMR, IR, Raman, UV-vis, EPR and HRMS values;
- optical rotation, ee/er, dr and chiral chromatography;
- crystal formula, space group, cell constants and disorder;
- reported molecular formula, ion assignment, isolated mass and yield when
  they describe the molecule or product.

Keep value_raw verbatim. Put a parsed number or range in
value_normalized. Keep unknown values null. If the source has a conflict,
create separate entries or set status unresolved and explain the conflict in
notes. Do not replace an HRMS formula with an RDKit formula, and do not turn a
calculated property into a reported property.

