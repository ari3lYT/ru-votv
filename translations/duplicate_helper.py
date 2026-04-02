#!/usr/bin/env python3
"""Помощник для работы с дублями в Game_strings.csv.

Сценарии:
* scan: показать группы, где одинаковый english встречается несколько раз
* sync: синхронизировать russian по всем строкам с одинаковым english
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Поиск и синхронизация дублей в Game_strings.csv."
    )
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path("translations/Game/Game_strings.csv"),
        help="Путь до CSV (по умолчанию translations/Game/Game_strings.csv).",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    scan = subparsers.add_parser("scan", help="Показать дубли и конфликтующие переводы.")
    scan.add_argument(
        "--only-conflicts",
        action="store_true",
        help="Показывать только группы, где у одного english несколько разных russian.",
    )
    scan.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Сколько групп вывести.",
    )
    scan.add_argument(
        "--contains",
        default=None,
        help="Фильтр по подстроке в english.",
    )

    sync = subparsers.add_parser("sync", help="Синхронизировать переводы дублей.")
    sync.add_argument(
        "--english",
        default=None,
        help="Точный english-текст, который нужно синхронизировать.",
    )
    sync.add_argument(
        "--id",
        default=None,
        help="ID строки. english будет взят по этой строке.",
    )
    sync.add_argument(
        "--russian",
        default=None,
        help="Явный перевод, который нужно записать во все совпадающие строки.",
    )
    sync.add_argument(
        "--strategy",
        choices=["translated-most-common", "translated-first", "most-common", "first"],
        default="translated-most-common",
        help="Как выбрать перевод, если --russian не передан.",
    )
    sync.add_argument(
        "--all-conflicts",
        action="store_true",
        help="Обработать все конфликтующие группы, а не одну конкретную.",
    )
    sync.add_argument(
        "--write",
        action="store_true",
        help="Записать изменения в CSV. Без этого работает dry-run.",
    )

    return parser.parse_args()


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        required = {"id", "english", "russian"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise SystemExit(f"{path} пропущены колонки: {', '.join(sorted(missing))}")
        return list(reader)


def save_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "english", "russian"])
        writer.writeheader()
        writer.writerows(rows)


def build_groups(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[row["english"]].append(row)
    return groups


def normalized_variants(rows: Iterable[dict[str, str]]) -> list[str]:
    return sorted({(row["russian"] or "").strip() for row in rows if (row["russian"] or "").strip()})


def choose_translation(rows: list[dict[str, str]], strategy: str) -> str | None:
    english = rows[0]["english"]
    russian_values = [(row["russian"] or "").strip() for row in rows if (row["russian"] or "").strip()]
    if not russian_values:
        return None

    translated_values = [value for value in russian_values if value != english]

    if strategy == "translated-most-common":
        source = translated_values or russian_values
        return Counter(source).most_common(1)[0][0]
    if strategy == "translated-first":
        source = translated_values or russian_values
        return source[0]
    if strategy == "most-common":
        return Counter(russian_values).most_common(1)[0][0]
    if strategy == "first":
        return russian_values[0]

    raise AssertionError(f"unknown strategy: {strategy}")


def print_scan(groups: dict[str, list[dict[str, str]]], args: argparse.Namespace) -> None:
    printed = 0
    for english, rows in sorted(groups.items(), key=lambda item: len(item[1]), reverse=True):
        if len(rows) < 2:
            continue
        if args.contains and args.contains not in english:
            continue

        variants = normalized_variants(rows)
        if args.only_conflicts and len(variants) < 2:
            continue

        print(f"COUNT {len(rows)} | DISTINCT_RU {len(variants)}")
        print(f"EN {english!r}")
        counter = Counter((row['russian'] or '').strip() for row in rows if (row['russian'] or '').strip())
        for value, count in counter.most_common(5):
            print(f"  {count:>4} {value!r}")
        print()
        printed += 1
        if printed >= args.limit:
            break

    if printed == 0:
        print("Ничего не найдено.")


def resolve_target_english(
    rows: list[dict[str, str]],
    target_english: str | None,
    target_id: str | None,
) -> str | None:
    if target_english:
        return target_english
    if target_id:
        for row in rows:
            if row["id"] == target_id:
                return row["english"]
        raise SystemExit(f"ID не найден: {target_id}")
    return None


def sync_group(
    rows: list[dict[str, str]],
    english: str,
    explicit_russian: str | None,
    strategy: str,
) -> tuple[int, str] | None:
    group = [row for row in rows if row["english"] == english]
    if not group:
        return None

    replacement = explicit_russian.strip() if explicit_russian else choose_translation(group, strategy)
    if not replacement:
        return None

    changed = 0
    for row in group:
        if row["russian"] != replacement:
            row["russian"] = replacement
            changed += 1
    return changed, replacement


def sync_all_conflicts(rows: list[dict[str, str]], strategy: str) -> list[tuple[str, int, str]]:
    groups = build_groups(rows)
    changes: list[tuple[str, int, str]] = []
    for english, group in groups.items():
        variants = normalized_variants(group)
        if len(group) < 2 or len(variants) < 2:
            continue
        result = sync_group(rows, english, None, strategy)
        if result is None:
            continue
        changed, replacement = result
        if changed:
            changes.append((english, changed, replacement))
    return changes


def main() -> None:
    args = parse_args()
    rows = load_rows(args.csv)
    groups = build_groups(rows)

    if args.command == "scan":
        print_scan(groups, args)
        return

    target_english = resolve_target_english(rows, args.english, args.id)

    if args.all_conflicts:
        changes = sync_all_conflicts(rows, args.strategy)
        print(f"Групп обновлено: {len(changes)}")
        for english, changed, replacement in changes[:20]:
            print(f"{changed:>4} | {english!r} -> {replacement!r}")
        if len(changes) > 20:
            print(f"... и ещё {len(changes) - 20} групп")
        if args.write and changes:
            save_rows(args.csv, rows)
            print(f"Записано: {args.csv}")
        elif not args.write:
            print("Dry-run: CSV не изменён. Добавь --write для записи.")
        return

    if not target_english:
        raise SystemExit("Нужно указать --english, --id или --all-conflicts")

    result = sync_group(rows, target_english, args.russian, args.strategy)
    if result is None:
        raise SystemExit("Не удалось выбрать перевод для синхронизации")

    changed, replacement = result
    total = len(groups.get(target_english, []))
    print(f"EN: {target_english!r}")
    print(f"RU: {replacement!r}")
    print(f"Изменено строк: {changed} из {total}")

    if args.write:
        save_rows(args.csv, rows)
        print(f"Записано: {args.csv}")
    else:
        print("Dry-run: CSV не изменён. Добавь --write для записи.")


if __name__ == "__main__":
    main()
