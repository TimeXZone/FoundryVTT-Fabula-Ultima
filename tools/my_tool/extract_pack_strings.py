import argparse
import json
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from openpyxl import Workbook

TARGET_KEYS = {"name", "description", "content"}
ENTRIES_SHEET = "Entries"
TRANSLATIONS_SHEET = "Translations"


def iter_json_files(base_dir: Path) -> Iterable[Path]:
    for path in base_dir.rglob("*.json"):
        if path.is_file():
            yield path


def collect_strings(node, path: List[str], rel_path: str, entries: List[Tuple[str, str]]):
    if isinstance(node, dict):
        for key, value in node.items():
            next_path = path + [str(key)]
            if key in TARGET_KEYS and isinstance(value, str):
                pointer = "/" + "/".join(next_path)
                identifier = f"{rel_path}::{pointer}"
                entries.append((identifier, value))
            else:
                collect_strings(value, next_path, rel_path, entries)
    elif isinstance(node, list):
        for idx, item in enumerate(node):
            collect_strings(item, path + [str(idx)], rel_path, entries)


def write_workbook(entries: List[Tuple[str, str]], output_path: Path):
    wb = Workbook()
    ws_entries = wb.active
    ws_entries.title = ENTRIES_SHEET
    ws_entries.append(["Identifier", "English Text"])
    for identifier, text in entries:
        ws_entries.append([identifier, text])

    ws_translations = wb.create_sheet(TRANSLATIONS_SHEET)
    ws_translations.append(["English Text", "Chinese Translation"])

    seen: Dict[str, None] = {}
    for _, english in entries:
        if english not in seen:
            ws_translations.append([english, ""])
            seen[english] = None

    wb.save(output_path)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Extract 'name', 'description', and 'content' strings from JSON files "
            "under a directory into an XLSX workbook with entries and translations sheets."
        )
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("src/packs"),
        help="Base directory containing JSON files to extract from (default: src/packs)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("pack_strings.xlsx"),
        help="Output XLSX file path (default: pack_strings.xlsx)",
    )
    args = parser.parse_args()

    base_dir: Path = args.input
    output_path: Path = args.output

    if not base_dir.exists():
        raise SystemExit(f"Input directory does not exist: {base_dir}")

    entries: List[Tuple[str, str]] = []
    for json_file in sorted(iter_json_files(base_dir)):
        rel_path = str(json_file.relative_to(base_dir))
        with json_file.open("r", encoding="utf-8") as f:
            data = json.load(f)
        collect_strings(data, [], rel_path, entries)

    write_workbook(entries, output_path)
    print(f"Extracted {len(entries)} entries to {output_path}")


if __name__ == "__main__":
    main()