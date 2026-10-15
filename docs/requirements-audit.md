# Requirements audit

This audit describes what the repository can guarantee after installation.

| Requirement | Status | Evidence |
| --- | --- | --- |
| Read a literature PDF | Pass | PyMuPDF ingestion, page text, page images, source SHA-256 |
| Preserve source evidence | Pass | run and evidence manifests with page-level hashes |
| Extract OCSR candidates | Pass with explicit crops | DECIMER adapter and batch recognition manifest |
| Review structures against images | Workflow pass | worker packet, source/recognition/identity/readback statuses |
| Export molecular SMILES | Pass after review | record structure.smiles and RDKit validation |
| Export molecular SMARTS | Pass after review | record structure.smarts and smarts CLI |
| Export reaction SMILES | Pass after review | reaction_smiles and reaction_components |
| Export reaction SMARTS | Pass after review | reaction_smarts derived by RDKit |
| Calculate molecular properties | Pass after review | formula, exact mass, MW, charge, HBD/HBA, rotatable bonds, TPSA, logP |
| Keep solvents, gases, apparatus, mixtures | Pass | complete molecules inventory and nullable structures |
| Handle coordination and salts | Workflow pass | composition and optional full coordination sidecars |
| Native ChemDraw save/readback | Optional host stage | capability probe plus run-specific receipt |
| One-command, ground-truth extraction from any PDF | Not claimed | arbitrary PDF figures need explicit crops and chemical review |

The last row is deliberate. OCSR can propose a valid SMILES that is the wrong
isomer, charge state, bond order, or coordination complex. The pipeline
automates ingestion, candidate generation, parsing, properties, SMARTS, and
packaging; it does not silently certify a structure that has not been checked
against the source image. A CATL Astra/ChemDraw worker can fill the review
packet and then the same assembly and validation commands produce the final
structured record.

