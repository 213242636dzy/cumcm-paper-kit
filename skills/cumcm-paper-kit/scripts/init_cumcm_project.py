#!/usr/bin/env python3
"""Create a non-destructive CUMCM project tree from the bundled assets."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import zipfile
from pathlib import Path


DIRECTORIES = (
    "problem",
    "data/raw",
    "data/processed",
    "src",
    "outputs/tables",
    "outputs/figures",
    "paper",
    "support",
    "ledgers",
    "logs",
    "submission",
)


def copy_if_missing(source: Path, destination: Path, created: list[str]) -> None:
    if destination.exists():
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    created.append(str(destination))


def decode_zip_name(name: str) -> str:
    try:
        return name.encode("cp437").decode("gbk")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return name


def prepare_latex_template(source: Path, destination: Path, created: list[str]) -> None:
    if destination.exists():
        return
    destination.mkdir(parents=True, exist_ok=False)
    root = destination.resolve()
    with zipfile.ZipFile(source) as archive:
        for item in archive.infolist():
            relative = Path(decode_zip_name(item.filename))
            target = (destination / relative).resolve()
            if root not in target.parents and target != root:
                raise ValueError(f"Unsafe ZIP member: {item.filename}")
            if item.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(item) as source_stream, target.open("wb") as target_stream:
                shutil.copyfileobj(source_stream, target_stream)

    main_files = list(destination.rglob("论文.tex"))
    if len(main_files) != 1:
        raise RuntimeError(f"Expected one 论文.tex, found {len(main_files)}")
    main_file = main_files[0]
    text = main_file.read_text(encoding="utf-8")
    old = text
    pattern = re.compile(
        r"\\thispagestyle\{empty\}\s*"
        r"\\input\{0\.摘要\.tex\}\s*"
        r"\\thispagestyle\{empty\}\s*"
        r"\\tableofcontents\s*"
        r"\\thispagestyle\{empty\}\s*"
        r"\\newpage\s*"
        r"\\setcounter\{page\}\{1\}\s*"
        r"\\input\{1\.引言\.tex\}"
    )
    text, count = pattern.subn(
        "\\\\input{0.摘要.tex}\n\n\\\\newpage\n\n\\\\input{1.引言.tex}", text, count=1
    )
    if count != 1:
        raise RuntimeError("Could not remove the template table of contents safely")
    if "\\tableofcontents" in text:
        raise RuntimeError("Prepared template still contains \\tableofcontents")
    if text == old:
        raise RuntimeError("Prepared LaTeX template was not changed")
    main_file.write_text(text, encoding="utf-8")
    created.append(str(destination))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a CUMCM paper project without overwriting existing files."
    )
    parser.add_argument("target", type=Path, help="Project directory to create or extend")
    parser.add_argument(
        "--format",
        choices=("word", "latex", "both"),
        default="word",
        help="Template assets to copy (default: word)",
    )
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    assets = skill_root / "assets"
    target = args.target.expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)

    created: list[str] = []
    for relative in DIRECTORIES:
        directory = target / relative
        if not directory.exists():
            directory.mkdir(parents=True)
            created.append(str(directory))

    for source in sorted((assets / "ledgers").glob("*.csv")):
        copy_if_missing(source, target / "ledgers" / source.name, created)

    if args.format in {"word", "both"}:
        source = assets / "templates" / "CUMCM-2026-论文空白模板.docx"
        if not source.exists():
            raise FileNotFoundError(f"Missing bundled Word template: {source}")
        copy_if_missing(source, target / "paper" / source.name, created)

    if args.format in {"latex", "both"}:
        source = assets / "templates" / "2026latex模板.zip"
        if not source.exists():
            raise FileNotFoundError(f"Missing bundled LaTeX template: {source}")
        copy_if_missing(source, target / "paper" / source.name, created)
        prepare_latex_template(source, target / "paper" / "latex-template", created)

    print(json.dumps({"target": str(target), "created": created}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
