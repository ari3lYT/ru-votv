#!/usr/bin/env python3
"""Import useful translation edits from a ru-votv fork into the current CSV."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
import re


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FORK_URL = "https://github.com/xXimuS/ru-votv.git"
DEFAULT_FORK_DIR = REPO_ROOT / ".cache" / "ru-votv-forks" / "xXimuS-ru-votv"
DEFAULT_CURRENT_CSV = REPO_ROOT / "translations" / "Game" / "Game_strings.csv"
DEFAULT_REPORT = REPO_ROOT / "translations" / "fork-xximus-translation-diff.csv"
DEFAULT_META = REPO_ROOT / "translations" / "fork-xximus-meta.json"

PLACEHOLDER_RE = re.compile(r"\{[^{}]*\}")
TAG_RE = re.compile(r"</>|<[^>]+>")


def protected_tokens(text: str) -> tuple[list[str], list[str]]:
    return PLACEHOLDER_RE.findall(text), TAG_RE.findall(text)


def tokens_match(source: str, translated: str) -> bool:
    return protected_tokens(source) == protected_tokens(translated)


def ensure_fork(url: str, path: Path) -> None:
    if path.exists():
        try:
            subprocess.run(["git", "-C", str(path), "fetch", "--depth=1", "origin", "main"], check=True, timeout=60)
            subprocess.run(["git", "-C", str(path), "checkout", "-q", "origin/main"], check=True, timeout=60)
            return
        except Exception as exc:  # noqa: BLE001
            print(f"[fork] fetch failed, using local cache: {exc}")
            return
    path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "clone", "--depth=1", url, str(path)], check=True, timeout=120)


def git_rev(path: Path) -> str:
    try:
        return subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True).strip()
    except Exception:  # noqa: BLE001
        return "unknown"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"id", "english", "russian"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise SystemExit(f"{path} missing columns: {', '.join(sorted(missing))}")
        return [
            {
                "id": (row.get("id") or "").strip(),
                "english": row.get("english") or "",
                "russian": row.get("russian") or "",
            }
            for row in reader
        ]


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def is_useful_translation(english: str, russian: str) -> bool:
    value = russian.strip()
    return bool(value) and value != english and tokens_match(english, russian)


def build_fork_indexes(fork_rows: list[dict[str, str]]) -> tuple[dict[str, dict[str, str]], dict[str, str], set[str]]:
    by_id = {row["id"]: row for row in fork_rows if row["id"]}
    variants: defaultdict[str, list[str]] = defaultdict(list)
    for row in fork_rows:
        if is_useful_translation(row["english"], row["russian"]):
            variants[row["english"]].append(row["russian"])

    by_english: dict[str, str] = {}
    conflicts: set[str] = set()
    for english, values in variants.items():
        counts = Counter(values)
        if len(counts) > 1:
            conflicts.add(english)
        by_english[english] = counts.most_common(1)[0][0]
    return by_id, by_english, conflicts


def main() -> None:
    parser = argparse.ArgumentParser(description="Import translations from a ru-votv fork.")
    parser.add_argument("--fork-url", default=DEFAULT_FORK_URL, help="Fork git URL.")
    parser.add_argument("--fork-dir", type=Path, default=DEFAULT_FORK_DIR, help="Local fork cache.")
    parser.add_argument("--fork-csv", type=Path, default=None, help="Fork Game_strings.csv path.")
    parser.add_argument("--csv", type=Path, default=DEFAULT_CURRENT_CSV, help="Current Game_strings.csv.")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT, help="Detailed import report CSV.")
    parser.add_argument("--meta", type=Path, default=DEFAULT_META, help="Metadata JSON path.")
    parser.add_argument("--write", action="store_true", help="Write updated current CSV.")
    args = parser.parse_args()

    if args.fork_csv is None:
        ensure_fork(args.fork_url, args.fork_dir)
        fork_csv = args.fork_dir / "translations" / "Game" / "Game_strings.csv"
    else:
        fork_csv = args.fork_csv

    current_rows = read_csv(args.csv)
    fork_rows = read_csv(fork_csv)
    fork_by_id, fork_by_english, conflicts = build_fork_indexes(fork_rows)

    report_rows: list[dict[str, str]] = []
    stats = {
        "currentRows": len(current_rows),
        "forkRows": len(fork_rows),
        "exactIdApplied": 0,
        "englishApplied": 0,
        "unchanged": 0,
        "skippedTokenMismatch": 0,
        "skippedNoUsefulForkTranslation": 0,
        "forkEnglishConflicts": len(conflicts),
    }

    for row in current_rows:
        source = ""
        fork_ru = ""
        fork_row = fork_by_id.get(row["id"])
        if fork_row and is_useful_translation(row["english"], fork_row["russian"]):
            fork_ru = fork_row["russian"]
            source = "exact-id"
        elif row["english"] in fork_by_english:
            fork_ru = fork_by_english[row["english"]]
            source = "english"

        if not fork_ru:
            stats["skippedNoUsefulForkTranslation"] += 1
            continue
        if not tokens_match(row["english"], fork_ru):
            stats["skippedTokenMismatch"] += 1
            continue
        if row["russian"] == fork_ru:
            stats["unchanged"] += 1
            continue

        old_ru = row["russian"]
        row["russian"] = fork_ru
        if source == "exact-id":
            stats["exactIdApplied"] += 1
        else:
            stats["englishApplied"] += 1
        report_rows.append(
            {
                "source": source,
                "id": row["id"],
                "english": row["english"],
                "old_russian": old_ru,
                "fork_russian": fork_ru,
            }
        )

    write_csv(args.report, ["source", "id", "english", "old_russian", "fork_russian"], report_rows)
    if args.write:
        write_csv(args.csv, ["id", "english", "russian"], current_rows)

    meta = {
        **stats,
        "forkUrl": args.fork_url,
        "forkRevision": git_rev(args.fork_dir) if args.fork_csv is None else "local-file",
        "forkCsv": str(fork_csv),
        "currentCsv": str(args.csv),
        "report": str(args.report),
    }
    args.meta.parent.mkdir(parents=True, exist_ok=True)
    args.meta.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for key, value in meta.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
