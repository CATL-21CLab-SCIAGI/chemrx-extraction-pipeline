# Natural-language molecular properties

The pipeline has two property channels:

1. molecules[].structure.properties contains values calculated from a reviewed
   SMILES with RDKit.
2. molecules[].reported_properties contains what the literature says or
   shows, extracted by the Astra image/text reviewer.

The second channel is intentionally open-ended because literature properties
are not limited to molecular descriptors. Typical entries include:

- appearance and physical state: white solid, orange oil, crystals;
- melting or boiling point, decomposition temperature;
- solubility or crystallization behavior;
- NMR, IR, Raman, UV-vis, EPR and HRMS observations;
- optical rotation, ee/er, dr, stereochemical or chiral HPLC results;
- crystal formula, space group, cell constants, occupancy and disorder;
- source-reported molecular formula, ion assignment, yield and analytical
  mass when attached to a molecule.

Each entry must contain:

- name: stable label such as melting_point or nmr_1h;
- value_raw: exact natural-language value from the SI or figure;
- value_normalized: optional parsed number, range, list, or structured object;
- unit: only when the source provides or unambiguously states one;
- category: physical, spectroscopic, mass_spectrometric, crystallographic,
  stereochemical, solubility, or other;
- extraction_agent: for example gpt-6-astra/low;
- confidence and status;
- evidence: page, crop, excerpt, and hash references.

The Astra worker reads the whole source page and the relevant crop, preserves
the raw wording, and then proposes a normalized value. The main reviewer
checks that the number, unit, sample identity, and experimental variant match
the source. A derived RDKit value never overwrites a reported value, and a
reported value never overwrites a derived value.

