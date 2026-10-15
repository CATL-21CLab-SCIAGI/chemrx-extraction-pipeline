"""Command-line interface for the reusable pipeline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .adapters import decimer_from_image, native_chemdraw_status
from .io import sha256_file, write_json
from .pipeline import create_draft_record, ingest_pdf
from .properties import calculate_properties, reaction_smiles_to_smarts, validate_smiles
from .recognition import recognize_batch
from .review import assemble_record, validate_record


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="chemrx", description="Evidence-first chemistry PDF extraction"
    )
    sub = parser.add_subparsers(dest="command", required=True)
    ingest = sub.add_parser("ingest", help="render a PDF and write text/evidence manifests")
    ingest.add_argument("pdf", type=Path)
    ingest.add_argument("-o", "--output", type=Path, required=True)
    ingest.add_argument("--dpi", type=int, default=150)
    draft = sub.add_parser("draft", help="ingest a PDF and create an evidence-linked JSON draft")
    draft.add_argument("pdf", type=Path)
    draft.add_argument("-o", "--output", type=Path, required=True)
    draft.add_argument("--record-id", default="rxn-0001")
    draft.add_argument("--dpi", type=int, default=150)
    props = sub.add_parser("properties", help="calculate RDKit properties for one SMILES")
    props.add_argument("smiles")
    validate = sub.add_parser("validate-smiles", help="parse and canonicalize one SMILES")
    validate.add_argument("smiles")
    smarts = sub.add_parser("smarts", help="convert molecular or reaction SMILES to SMARTS")
    smarts.add_argument("smiles", help="SMILES or reaction SMILES")
    recognize = sub.add_parser("recognize", help="run the explicit DECIMER candidate adapter on an image")
    recognize.add_argument("image", type=Path)
    recognize.add_argument("-o", "--output", type=Path, required=True)
    recognize.add_argument("--endpoint")
    batch = sub.add_parser("recognize-batch", help="run DECIMER on an explicit crop manifest")
    batch.add_argument("manifest", type=Path)
    batch.add_argument("-o", "--output", type=Path, required=True)
    batch.add_argument("--endpoint")
    assemble = sub.add_parser(
        "assemble",
        help="calculate properties and write an assembled record from a reviewed JSON draft",
    )
    assemble.add_argument("input", type=Path)
    assemble.add_argument("-o", "--output", type=Path, required=True)
    record = sub.add_parser("validate-record", help="validate one assembled reaction JSON record")
    record.add_argument("record", type=Path)
    sub.add_parser("doctor", help="report optional backend availability")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "ingest":
        print(json.dumps(ingest_pdf(args.pdf, args.output, args.dpi), ensure_ascii=False, indent=2))
    elif args.command == "draft":
        path = create_draft_record(args.pdf, args.output, args.record_id, args.dpi)
        print(json.dumps({"status": "draft_created", "record": str(path)}, ensure_ascii=False))
    elif args.command == "properties":
        print(json.dumps(calculate_properties(args.smiles).__dict__, ensure_ascii=False, indent=2))
    elif args.command == "validate-smiles":
        print(json.dumps(validate_smiles(args.smiles), ensure_ascii=False, indent=2))
    elif args.command == "smarts":
        if args.smiles.count(">") == 2:
            value = reaction_smiles_to_smarts(args.smiles)
        else:
            from .properties import smiles_to_smarts

            value = smiles_to_smarts(args.smiles)
        print(json.dumps({"input": args.smiles, "smarts": value}, ensure_ascii=False, indent=2))
    elif args.command == "recognize":
        result = decimer_from_image(args.image, endpoint=args.endpoint)
        result["image"] = str(args.image)
        result["image_sha256"] = sha256_file(args.image)
        write_json(args.output, result)
        print(json.dumps({"status": result["status"], "output": str(args.output)}, ensure_ascii=False))
    elif args.command == "recognize-batch":
        result = recognize_batch(args.manifest, args.output, endpoint=args.endpoint)
        print(json.dumps({"status": result["status"], "items": len(result["items"]), "output": str(args.output)}, ensure_ascii=False))
    elif args.command == "assemble":
        print(json.dumps(assemble_record(args.input, args.output), ensure_ascii=False, indent=2))
    elif args.command == "validate-record":
        print(json.dumps(validate_record(args.record), ensure_ascii=False, indent=2))
    elif args.command == "doctor":
        print(json.dumps({"chemdraw": native_chemdraw_status()}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

