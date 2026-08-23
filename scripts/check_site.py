#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "examples_manifest.json").read_text(encoding="utf-8"))
CODE_RE = re.compile(
    r"^```\{(webr|r)\}\s*\n(.*?)^```\s*$", flags=re.MULTILINE | re.DOTALL
)


def fail(message: str) -> None:
    raise SystemExit(f"Site check failed: {message}")


def body_without_front_matter(text: str) -> str:
    match = re.match(r"\A---\s*\n.*?\n---\s*\n", text, flags=re.DOTALL)
    if not match:
        fail("a QMD file has no valid YAML front matter")
    return text[match.end() :]


def check_page(entry: dict) -> int:
    path = ROOT / entry["file"]
    if not path.is_file():
        fail(f"missing page {entry['file']}")

    text = path.read_text(encoding="utf-8")
    blocks = CODE_RE.findall(text)
    if len(blocks) != entry["block_count"]:
        fail(
            f"{entry['file']} contains {len(blocks)} code blocks; "
            f"expected {entry['block_count']}"
        )

    expected_engine = "webr" if entry["runtime"] == "webr" else "r"
    if any(engine != expected_engine for engine, _ in blocks):
        fail(f"{entry['file']} uses the wrong R runtime fence")

    hashes = [
        hashlib.sha256(block.rstrip("\n").encode("utf-8")).hexdigest()
        for _, block in blocks
    ]
    if hashes != entry["sha256"]:
        fail(f"{entry['file']} no longer matches the original R examples")

    body = body_without_front_matter(text)
    body_without_code = CODE_RE.sub("", body)
    headings = re.findall(r"^## (.+)$", body_without_code, flags=re.MULTILINE)
    if len(headings) != len(blocks):
        fail(f"{entry['file']} must have one short heading per example")

    prose_only = body_without_code
    prose_only = re.sub(r"^## .+$", "", prose_only, flags=re.MULTILINE)
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", prose_only) if p.strip()]
    if blocks and len(paragraphs) != len(blocks):
        fail(f"{entry['file']} must have one short description per example")
    if any(len(paragraph.split()) > 35 for paragraph in paragraphs):
        fail(f"{entry['file']} contains a description longer than 35 words")

    return len(blocks)


def main() -> None:
    quarto = (ROOT / "_quarto.yml").read_text(encoding="utf-8")
    if "ECON 5280: Applied Econometrics" not in quarto:
        fail("the course title is not Applied Econometrics")
    if "Causal Inference and Machine Learning" in quarto:
        fail("the former course title remains in _quarto.yml")

    forbidden = [
        path.relative_to(ROOT)
        for path in ROOT.rglob("*")
        if path.is_file() and path.suffix.lower() in {".tex", ".pdf"}
    ]
    if forbidden:
        fail(f"LaTeX/PDF files are present: {forbidden}")

    total = sum(check_page(entry) for entry in MANIFEST["pages"])
    if total != 33:
        fail(f"found {total} original R examples; expected 33")

    qmd_pages = {
        str(path.relative_to(ROOT)) for path in (ROOT / "chapters").glob("*.qmd")
    }
    expected_pages = {entry["file"] for entry in MANIFEST["pages"]}
    if qmd_pages != expected_pages:
        fail("the chapter page set differs from the manifest")

    if (ROOT / "chapters/house.csv").read_bytes() != (ROOT / "data/house.csv").read_bytes():
        fail("the Chapter 8 browser copy of house.csv is out of sync")

    print(f"Site check: PASS ({len(expected_pages)} pages, {total} original R examples)")


if __name__ == "__main__":
    main()
