#!/usr/bin/env python3
"""Run static integrity checks for the course repository."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urldefrag, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".idea", ".ipynb_checkpoints", ".venv-bw", "__pycache__", "tmp"}
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
REQUIRED_FILES = (
    Path("envs/bw_env_osxARM.yaml"),
    Path("envs/bw_env_osx64.yaml"),
    Path("envs/bw_env_win64.yaml"),
    Path("tutorials/DAY 3/assets/d3-03b/prospective_aware_2_country_all_yearly.json.gz"),
)


def iter_repository_files(suffix: str) -> list[Path]:
    matches: list[Path] = []
    for directory, subdirectories, filenames in os.walk(ROOT):
        subdirectories[:] = [name for name in subdirectories if name not in SKIP_DIRS]
        base = Path(directory)
        matches.extend(base / name for name in filenames if Path(name).suffix.lower() == suffix)
    return sorted(matches)


def source_text(source: object) -> str:
    if isinstance(source, str):
        return source
    if isinstance(source, list) and all(isinstance(item, str) for item in source):
        return "".join(source)
    raise TypeError("cell source must be a string or a list of strings")


def local_destination(raw_destination: str) -> str | None:
    destination = raw_destination.strip()
    if destination.startswith("<") and ">" in destination:
        destination = destination[1 : destination.index(">")]
    else:
        destination = destination.split(maxsplit=1)[0]

    destination, _ = urldefrag(destination)
    parsed = urlsplit(destination)
    if (
        not destination
        or destination.startswith("#")
        or destination.startswith("/")
        or parsed.scheme
        or parsed.netloc
    ):
        return None
    return unquote(parsed.path)


def has_exact_case(path: Path) -> bool:
    try:
        relative = path.relative_to(ROOT)
    except ValueError:
        return False

    current = ROOT
    for part in relative.parts:
        if not current.is_dir() or part not in {child.name for child in current.iterdir()}:
            return False
        current /= part
    return current.exists()


def check_links(
    document: str,
    base_directory: Path,
    text: str,
    failures: list[str],
) -> int:
    checked = 0
    for match in LINK_RE.finditer(text):
        destination = local_destination(match.group(1))
        if destination is None:
            continue
        checked += 1
        candidate = Path(os.path.normpath(base_directory / destination))
        if not has_exact_case(candidate):
            failures.append(f"{document}: missing or case-mismatched local link: {destination}")
    return checked


def main() -> int:
    failures: list[str] = []
    link_count = 0

    for relative_path in REQUIRED_FILES:
        if not (ROOT / relative_path).is_file():
            failures.append(f"missing required course file: {relative_path}")

    notebooks = iter_repository_files(".ipynb")
    for path in notebooks:
        relative = path.relative_to(ROOT)
        try:
            notebook = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            failures.append(f"{relative}: invalid notebook JSON: {error}")
            continue

        cells = notebook.get("cells")
        if not isinstance(cells, list):
            failures.append(f"{relative}: notebook has no valid cells list")
            continue

        cell_ids: list[str] = []
        for index, cell in enumerate(cells, start=1):
            cell_id = cell.get("id")
            if not isinstance(cell_id, str) or not cell_id:
                failures.append(f"{relative}: cell {index} has no valid id")
            else:
                cell_ids.append(cell_id)

            try:
                text = source_text(cell.get("source"))
            except TypeError as error:
                failures.append(f"{relative}: cell {index}: {error}")
                continue

            if cell.get("cell_type") == "code":
                if cell.get("execution_count") is not None:
                    failures.append(f"{relative}: cell {index} has a stored execution count")
                if cell.get("outputs") != []:
                    failures.append(f"{relative}: cell {index} has stored output")
            elif cell.get("cell_type") == "markdown":
                link_count += check_links(
                    f"{relative} (cell {index})", path.parent, text, failures
                )

        if len(cell_ids) != len(set(cell_ids)):
            failures.append(f"{relative}: duplicate cell ids")

    markdown_files = iter_repository_files(".md")
    nested_readmes = [
        path.relative_to(ROOT)
        for path in markdown_files
        if path.name.casefold() == "readme.md" and path != ROOT / "README.MD"
    ]
    for path in nested_readmes:
        failures.append(f"nested README is not allowed: {path}")

    for path in markdown_files:
        relative = path.relative_to(ROOT)
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as error:
            failures.append(f"{relative}: could not read Markdown file: {error}")
            continue
        link_count += check_links(str(relative), path.parent, text, failures)

    if failures:
        print("Course-material checks failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(
        f"Checked {len(notebooks)} notebooks, {len(markdown_files)} Markdown files, "
        f"and {link_count} local links; all material checks passed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
