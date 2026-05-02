#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


TOKEN_PATTERNS = {
    "brace": re.compile(r"\{[A-Za-z0-9_:.+-]+\}"),
    "angle": re.compile(r"</?[-A-Za-z0-9_:.]+(?:\s+[-A-Za-z0-9_:.]+=(?:\"[^\"]*\"|'[^']*'|[^\s>]+))*\s*/?>"),
    "rich_command": re.compile(
        r"/(?:image|imagesize|align|padding|color|font|scale)\b(?:=(?:[^\s\r\n]+)|\([^)]*\))?",
        re.IGNORECASE,
    ),
    "printf": re.compile(r"%(?:\d+\$)?[-+#0]*(?:\d+|\*)?(?:\.(?:\d+|\*))?[hlL]?[diuoxXfFeEgGcs]"),
}

LATIN_WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9_'-]*")
CYRILLIC_RE = re.compile(r"[А-Яа-яЁё]")
LETTER_RE = re.compile(r"[A-Za-zА-Яа-яЁё]")

LATIN_ALLOWLIST = {
    "AA",
    "API",
    "ASCII",
    "ATV",
    "Bloom",
    "CPU",
    "DLSS",
    "FOV",
    "FPS",
    "GPU",
    "HDR",
    "HTML",
    "HTTP",
    "HTTPS",
    "IP",
    "LMB",
    "MB",
    "MMB",
    "NPC",
    "PC",
    "PNG",
    "RHI",
    "RMB",
    "RTX",
    "SFX",
    "SSGI",
    "SSR",
    "TAA",
    "UI",
    "URL",
    "USB",
    "VSync",
    "WASD",
    "ZIP",
}

KNOWN_SUSPICIOUS = {
    "сломман": "двойная м в слове про поломку",
    "радивыш": "опечатка в радиовышке",
    "Нищюган": "жи/ши, лучше Нищуган",
    "ОтменА": "случайная заглавная буква",
    "баллов": "для награды/points обычно используем очки",
    "Помощь и Инфа": "меню Help & Info переведено разговорно, нужна редакторская проверка",
    "утчка": "мемная строка, проверить по контексту",
    "делаэт": "мемная строка, проверить по контексту",
    "проваленый": "орфографическая ошибка",
    "Восстановливает": "орфографическая ошибка",
    "Неизвестное устройства": "ошибка согласования",
    "ТВ Может": "случайная заглавная буква в середине предложения",
    "Требует включенную настройку": "машинная формулировка",
    "Требуется Веселая настройка": "машинная формулировка",
    "Требуется включенная веселая настройка": "машинная формулировка",
    "Максимальный размер объекта: 200x300 единиц": "потеря средней размерности 3D-принтера",
    "Кастомный": "англицизм в пользовательском контенте",
    "Requires [Custom Content] setting enabled": "английский текст в русском поле",
    "Uses images from the Asset folder": "английский текст в русском поле",
}


@dataclass
class CsvRow:
    line: int
    tid: str
    english: str
    russian: str


def read_rows(path: Path) -> list[CsvRow]:
    rows: list[CsvRow] = []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        required = {"id", "english", "russian"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise SystemExit(f"{path}: missing columns: {', '.join(sorted(missing))}")
        for idx, row in enumerate(reader, start=2):
            rows.append(
                CsvRow(
                    line=idx,
                    tid=row.get("id", ""),
                    english=row.get("english", ""),
                    russian=row.get("russian", ""),
                )
            )
    return rows


def token_counter(text: str) -> Counter[tuple[str, str]]:
    counter: Counter[tuple[str, str]] = Counter()
    for name, pattern in TOKEN_PATTERNS.items():
        for match in pattern.findall(text):
            counter[(name, match)] += 1
    return counter


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def is_probably_untranslated(row: CsvRow) -> bool:
    english = normalize_text(row.english)
    russian = normalize_text(row.russian)
    if not english or english != russian:
        return False
    if not LETTER_RE.search(english):
        return False
    if re.search(r"^(?:https?://|/|[A-Za-z]:\\)", english):
        return False
    if re.fullmatch(r"[A-Z0-9_ .:/\\-]+", english):
        return False
    if len(english) <= 3:
        return False
    return True


def latin_words_requiring_review(text: str) -> list[str]:
    for pattern in TOKEN_PATTERNS.values():
        text = pattern.sub(" ", text)
    words: list[str] = []
    for word in LATIN_WORD_RE.findall(text):
        clean = word.strip("'_-")
        if not clean or clean in LATIN_ALLOWLIST:
            continue
        if clean.upper() in LATIN_ALLOWLIST:
            continue
        if clean.startswith(("http", "www")):
            continue
        if re.fullmatch(r"[A-Z]{2,}[0-9]*", clean):
            continue
        words.append(clean)
    return words


def clip(text: str, limit: int = 150) -> str:
    text = normalize_text(text)
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "..."


def table(rows: list[list[str]]) -> str:
    if not rows:
        return "_Нет._\n"
    out = ["| line | english | russian | note |", "| ---: | --- | --- | --- |"]
    for line, english, russian, note in rows:
        out.append(f"| {line} | {english} | {russian} | {note} |")
    return "\n".join(out) + "\n"


def build_report(rows: list[CsvRow], sample_limit: int) -> str:
    empty_ru = [row for row in rows if not row.russian.strip()]
    placeholder_mismatches: list[list[str]] = []
    untranslated: list[list[str]] = []
    latin_review: list[list[str]] = []
    suspicious_hits: list[list[str]] = []

    suspicious_counts: Counter[str] = Counter()
    latin_counts: Counter[str] = Counter()
    duplicates: defaultdict[str, set[str]] = defaultdict(set)
    duplicate_examples: defaultdict[str, list[CsvRow]] = defaultdict(list)

    for row in rows:
        en_tokens = token_counter(row.english)
        ru_tokens = token_counter(row.russian)
        if en_tokens != ru_tokens and len(placeholder_mismatches) < sample_limit:
            missing = en_tokens - ru_tokens
            extra = ru_tokens - en_tokens
            note_bits = []
            if missing:
                note_bits.append("missing " + ", ".join(f"{token} x{count}" for (_, token), count in missing.items()))
            if extra:
                note_bits.append("extra " + ", ".join(f"{token} x{count}" for (_, token), count in extra.items()))
            placeholder_mismatches.append([str(row.line), clip(row.english), clip(row.russian), "; ".join(note_bits)])

        if is_probably_untranslated(row) and len(untranslated) < sample_limit:
            untranslated.append([str(row.line), clip(row.english), clip(row.russian), "same as English"])

        latin_words = latin_words_requiring_review(row.russian)
        if latin_words:
            latin_counts.update(latin_words)
            if CYRILLIC_RE.search(row.russian) and len(latin_review) < sample_limit:
                latin_review.append([str(row.line), clip(row.english), clip(row.russian), ", ".join(sorted(set(latin_words)))])

        for needle, note in KNOWN_SUSPICIOUS.items():
            if needle in row.russian:
                suspicious_counts[needle] += 1
                if len(suspicious_hits) < sample_limit:
                    suspicious_hits.append([str(row.line), clip(row.english), clip(row.russian), note])

        norm_en = normalize_text(row.english)
        norm_ru = normalize_text(row.russian)
        if norm_en:
            duplicates[norm_en].add(norm_ru)
            if len(duplicate_examples[norm_en]) < 4:
                duplicate_examples[norm_en].append(row)

    duplicate_rows: list[list[str]] = []
    for english, variants in duplicates.items():
        if len(variants) <= 1:
            continue
        examples = duplicate_examples[english]
        rendered = " / ".join(clip(example.russian, 60) for example in examples)
        duplicate_rows.append([str(examples[0].line), clip(english), rendered, f"{len(variants)} variants"])
        if len(duplicate_rows) >= sample_limit:
            break

    lines = [
        "# Translation Audit",
        "",
        f"* CSV rows: {len(rows)}",
        f"* Empty Russian strings: {len(empty_ru)}",
        f"* Format/control token mismatches: {sum(token_counter(row.english) != token_counter(row.russian) for row in rows)}",
        f"* Probably untranslated same-as-English rows: {sum(is_probably_untranslated(row) for row in rows)}",
        f"* Rows with reviewable Latin words in Russian: {sum(bool(latin_words_requiring_review(row.russian)) for row in rows)}",
        f"* English strings with multiple Russian variants: {sum(1 for variants in duplicates.values() if len(variants) > 1)}",
        "",
        "## Suspicious Term Counts",
        "",
    ]

    if suspicious_counts:
        for term, count in suspicious_counts.most_common():
            lines.append(f"* `{term}`: {count}")
    else:
        lines.append("* No configured suspicious terms found.")

    lines.extend(
        [
            "",
            "## Format/Control Token Samples",
            "",
            table(placeholder_mismatches),
            "## Probably Untranslated Samples",
            "",
            table(untranslated),
            "## Latin-In-Russian Samples",
            "",
            table(latin_review),
            "## Suspicious Term Samples",
            "",
            table(suspicious_hits),
            "## Duplicate English With Variant Russian Samples",
            "",
            table(duplicate_rows),
            "## Most Common Reviewable Latin Words",
            "",
        ]
    )

    if latin_counts:
        for word, count in latin_counts.most_common(30):
            lines.append(f"* `{word}`: {count}")
    else:
        lines.append("* None.")

    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit VotV Game_strings.csv for translation review.")
    parser.add_argument("--csv", type=Path, default=Path("translations/Game/Game_strings.csv"))
    parser.add_argument("--output", type=Path, default=Path("translations/reviews/audit-current.md"))
    parser.add_argument("--sample-limit", type=int, default=40)
    args = parser.parse_args()

    rows = read_rows(args.csv)
    report = build_report(rows, args.sample_limit)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print(f"[INFO] audited rows={len(rows)} report={args.output}")


if __name__ == "__main__":
    main()
