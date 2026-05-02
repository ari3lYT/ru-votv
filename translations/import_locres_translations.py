#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path

from pylocres.locres import LocresFile


def make_id(namespace: str, key: str, hash_value: int) -> str:
    parts = [p for p in (namespace.strip(), key.strip()) if p]
    base = "/".join(parts) if parts else key.strip() or f"{hash_value:08X}"
    return f"{base}#{hash_value:08X}"


def load_locres(path: Path) -> dict[str, str]:
    loc = LocresFile()
    loc.read(str(path))
    strings: dict[str, str] = {}
    for namespace in loc:
        ns_name = namespace.name or ""
        for entry in namespace:
            strings[make_id(ns_name, entry.key, entry.hash)] = entry.translation or ""
    return strings


def patch_known_typos(text: str) -> str:
    replacements = {
        "сломманого": "сломанного",
        "Сломманого": "Сломанного",
        "сломманный": "сломанный",
        "Сломманный": "Сломанный",
        "радивыш": "радиовыш",
        "Радивыш": "Радиовыш",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def import_translations(csv_path: Path, locres_path: Path, output_path: Path) -> tuple[int, int, int]:
    imported = load_locres(locres_path)
    updated = 0
    missing = 0
    rows: list[dict[str, str]] = []

    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise SystemExit(f"{csv_path}: empty CSV")
        if "id" not in reader.fieldnames or "russian" not in reader.fieldnames:
            raise SystemExit(f"{csv_path}: expected id and russian columns")

        fieldnames = list(reader.fieldnames)
        for row in reader:
            tid = (row.get("id") or "").strip()
            if tid in imported:
                row["russian"] = patch_known_typos(imported[tid])
                updated += 1
            else:
                missing += 1
            rows.append(row)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return len(rows), updated, missing


def main() -> None:
    parser = argparse.ArgumentParser(description="Import Russian translations from a .locres into Game_strings.csv.")
    parser.add_argument("--csv", type=Path, default=Path("translations/Game/Game_strings.csv"))
    parser.add_argument("--locres", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    output_path = args.output or args.csv
    total, updated, missing = import_translations(args.csv, args.locres, output_path)
    print(f"[INFO] rows={total} updated={updated} missing={missing} output={output_path}")


if __name__ == "__main__":
    main()
