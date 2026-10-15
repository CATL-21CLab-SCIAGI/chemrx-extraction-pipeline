# Extraction methodology

## 1. Establish the experiment boundary

Read the specific experimental paragraph, applicable general procedure,
reaction scheme, and adjacent pages. Keep scale variants, optimization
entries, crystallizations, analytical samples, and downstream steps distinct.
Do not copy a general procedure into an instance unless the SI explicitly
applies it.

## 2. Build the complete inventory

Record every reported substance with its original name, role, stage, amount,
and evidence page. Keep solvents, standards, gases, workup materials,
apparatus, mixtures, and undefined materials in the inventory. Use null when
a discrete molecular identity is not defined.

## 3. Extract and review structures

Use the whole reaction image and focused crops. Retain OCSR candidates and
source hashes. Correct candidates through an auditable edit step. Preserve
explicit hydrogens, charges, isotopes, stereochemistry, salt fragments,
metal coordination, and source identity. For complexes, store both the
charge-balanced composition and a source-known coordination sidecar when the
source supports it.

## 4. Extract reaction conditions and properties

Capture amounts, equivalents, concentration, addition order, temperature,
time, atmosphere, pressure, light/electrochemical settings, and solvent.
Calculate molecular formula, exact mass, molecular weight, charge, HBD/HBA,
rotatable bonds, TPSA, and logP only after structure review. Store raw
reported values beside derived values.

## 5. Validate before accepting

Validate every structure with a parser, compare saved MOL/CDXML readback,
check native ChemDraw save/render where available, and inspect the actual
pixels for clipping or missing labels. Keep unresolved and failed distinct
from passed. Never force a cross-reader pass by changing stereochemistry or
coordination representation.

