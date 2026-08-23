#!/usr/bin/env python3

from __future__ import annotations

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


def check_page(entry: dict) -> int:
    path = ROOT / entry["file"]
    if not path.is_file():
        fail(f"missing page {entry['file']}")

    text = path.read_text(encoding="utf-8")
    blocks = CODE_RE.findall(text)

    expected_engine = "webr" if entry["runtime"] == "webr" else "r"
    if any(engine != expected_engine for engine, _ in blocks):
        fail(f"{entry['file']} uses the wrong R runtime fence")

    return len(blocks)


def main() -> None:
    devcontainer = json.loads(
        (ROOT / ".devcontainer/devcontainer.json").read_text(encoding="utf-8")
    )
    if devcontainer.get("remoteUser") != "rstudio":
        fail("the Rocker dev container must use its existing rstudio user")

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

    qmd_pages = {
        str(path.relative_to(ROOT)) for path in (ROOT / "chapters").glob("*.qmd")
    }
    expected_pages = {entry["file"] for entry in MANIFEST["pages"]}
    if qmd_pages != expected_pages:
        fail("the chapter page set differs from the manifest")

    if (ROOT / "chapters/house.csv").read_bytes() != (ROOT / "data/house.csv").read_bytes():
        fail("the Chapter 8 browser copy of house.csv is out of sync")

    print(
        f"Site check: PASS ({len(expected_pages)} pages, {total} R examples; "
        "example code and counts are editable)"
    )


if __name__ == "__main__":
    main()
