# Output schema

The JSON output is organized around a ReactionRecord.

| Block | Purpose |
| --- | --- |
| source_pdf, source_sha256, pages | reproducible source identity |
| molecules[] | complete inventory and role assignments |
| molecules[].structure | SMILES, derived SMARTS, editable artifacts, candidates, properties |
| molecules[].reported_properties | Astra/reviewer language or figure observations with raw value, normalized value, unit, category, and evidence |
| reaction_smiles, reaction_smarts | reviewed reaction string and derived query pattern; may remain null |
| reaction_components | parser-friendly reactant/agent/product arrays |
| conditions | raw and normalized experimental conditions |
| workup | ordered operations and input/output streams |
| results | yield, mass, appearance, analytical results |
| evidence | page, crop, excerpt, and hash references |
| review | status, agent provenance, unresolved issues |

Recommended acceptance statuses are draft, source_reviewed,
structure_reviewed, passed, unresolved, and failed.

RDKit-derived values belong under molecules[].structure.properties. Literature
and figure observations belong under molecules[].reported_properties. They are
never merged silently: for example, a reported melting-point range remains
raw text plus a separately parsed range, while molecular weight calculated
from SMILES remains a derived RDKit value.

