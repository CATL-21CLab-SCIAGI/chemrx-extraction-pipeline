# Output schema

The JSON output is organized around a ReactionRecord.

| Block | Purpose |
| --- | --- |
| source_pdf, source_sha256, pages | reproducible source identity |
| molecules[] | complete inventory and role assignments |
| molecules[].structure | SMILES, editable artifacts, candidates, properties |
| reaction_smiles | reviewed reaction string; may remain null |
| reaction_components | parser-friendly reactant/agent/product arrays |
| conditions | raw and normalized experimental conditions |
| workup | ordered operations and input/output streams |
| results | yield, mass, appearance, analytical results |
| evidence | page, crop, excerpt, and hash references |
| review | status, agent provenance, unresolved issues |

Recommended acceptance statuses are draft, source_reviewed,
structure_reviewed, passed, unresolved, and failed.

