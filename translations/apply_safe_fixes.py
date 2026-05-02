#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


TEXT_REPLACEMENTS = {
    "/размер изображения=": "/imagesize=",
    "/выровнять=": "/align=",
    "/подкладка=": "/padding=",
    "ОтменА": "Отмена",
    "Нищюган": "Нищуган",
    "25 баллов": "25 очков",
    "Работает как Открытый Контейнер (Прочитайте совет о «Открытый Контейнер» в разделе «Помощь и Инфа»)": (
        "Работает как открытый контейнер (см. «Открытый контейнер» в разделе «Помощь и Инфа»)"
    ),
    'Проверьте "Помощь и Инфа" в меню паузы для рекомендации по игровому процессу или если вы запутались.': (
        'Загляните в "Помощь и Инфа" в меню паузы за советами по игровому процессу, если застряли.'
    ),
}

ROW_REPLACEMENTS = {
    "Use - Press E\r\nAction list - Hold E\r\nPickup - Press R\r\nPut in inventory - Hold R": {
        "Использовать - Нажать {E}\r\nСписок действий - Зажать {E}\r\nПодобрать - Нажать R\r\nПоложить в инвентарь - Зажать R": (
            "Использовать - Нажать E\r\nСписок действий - Зажать E\r\nПодобрать - Нажать R\r\nПоложить в инвентарь - Зажать R"
        ),
        "Использовать - Нажать {E}\nСписок действий - Зажать {E}\nПодобрать - Нажать R\nПоложить в инвентарь - Зажать R": (
            "Использовать - Нажать E\nСписок действий - Зажать E\nПодобрать - Нажать R\nПоложить в инвентарь - Зажать R"
        ),
    }
}


def apply_fixes(csv_path: Path, output_path: Path) -> tuple[int, Counter[str]]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise SystemExit(f"{csv_path}: empty CSV")
        required = {"id", "english", "russian"}
        missing = required - set(reader.fieldnames)
        if missing:
            raise SystemExit(f"{csv_path}: missing columns: {', '.join(sorted(missing))}")
        fieldnames = list(reader.fieldnames)
        rows = list(reader)

    counts: Counter[str] = Counter()
    for row in rows:
        text = row.get("russian", "")
        for old, new in ROW_REPLACEMENTS.get(row.get("english", ""), {}).items():
            hit_count = text.count(old)
            if hit_count:
                text = text.replace(old, new)
                counts[f"row:{old}"] += hit_count
        for old, new in TEXT_REPLACEMENTS.items():
            hit_count = text.count(old)
            if hit_count:
                text = text.replace(old, new)
                counts[old] += hit_count
        row["russian"] = text

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return len(rows), counts


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply conservative, context-safe Russian translation fixes.")
    parser.add_argument("--csv", type=Path, default=Path("translations/Game/Game_strings.csv"))
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    output_path = args.output or args.csv
    total, counts = apply_fixes(args.csv, output_path)
    print(f"[INFO] rows={total} output={output_path}")
    if not counts:
        print("[INFO] no replacements applied")
        return
    for old, count in counts.most_common():
        print(f"[INFO] replaced {old!r}: {count}")


if __name__ == "__main__":
    main()
