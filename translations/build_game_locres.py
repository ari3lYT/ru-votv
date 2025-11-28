#!/usr/bin/env python3
"""Собираем обновлённый Game.locres из Game_strings.csv с помощью pylocres."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from pylocres.locres import LocresFile


def _make_id(namespace: str, key: str, hash_value: int) -> str:
    parts = [p for p in (namespace.strip(), key.strip()) if p]
    base = "/".join(parts) if parts else key.strip() or f"{hash_value:08X}"
    return f"{base}#{hash_value:08X}"


def load_strings(strings_path: Path) -> dict[str, str]:
    mapping: dict[str, str] = {}
    with strings_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        required = {"id", "english", "russian"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise SystemExit(f"{strings_path} пропущены колонки: {', '.join(sorted(missing))}")
        for row in reader:
            tid = (row.get("id") or "").strip()
            ru = (row.get("russian") or "").strip()
            if tid and ru:
                mapping[tid] = ru
    return mapping


def apply(strings: dict[str, str], locres_path: Path, output_path: Path) -> tuple[int, int, int]:
    loc = LocresFile()
    loc.read(str(locres_path))
    total_entries = 0
    updated = 0
    missing = 0

    for namespace in loc:
        ns_name = namespace.name or ""
        for entry in namespace:
            total_entries += 1
            tid = _make_id(ns_name, entry.key, entry.hash)
            if tid in strings:
                entry.translation = strings[tid]
                updated += 1
            else:
                missing += 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    loc.write(str(output_path))
    return total_entries, updated, missing


def main() -> None:
    parser = argparse.ArgumentParser(description="Собрать Game.locres из Game_strings.csv и исходного locres.")
    parser.add_argument(
        "--strings",
        type=Path,
        default=Path("translations/Game/Game_strings.csv"),
        help="CSV с колонками id, english, russian (по умолчанию translations/Game/Game_strings.csv).",
    )
    parser.add_argument(
        "--locres",
        type=Path,
        default=Path("VotV/Content/Localization/Game/en/Game.locres"),
        help="Базовый locres (обычно английский).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("translations/output/Game_ru.locres"),
        help="Куда сохранить собранный locres.",
    )
    args = parser.parse_args()

    strings = load_strings(args.strings)
    total, updated, missing = apply(strings, args.locres, args.output)
    print(
        f"[INFO] Записан {args.output} | всего записей: {total}, обновлено переводов: {updated}, "
        f"пропущено (нет перевода): {missing}"
    )


if __name__ == "__main__":
    main()
