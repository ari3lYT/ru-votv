#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


TEXT_REPLACEMENTS = {
    "Помощь и Инфа": "Справка и советы",
    "утчка": "утка",
    "делаэт": "делает",
    "чо утка делает": "чё утка делает",
    "проваленый": "проваленный",
    "Восстановливает": "Восстанавливает",
    "Неизвестное устройства": "Неизвестное устройство",
    "спектограмму": "спектрограмму",
    "спектограммы": "спектрограммы",
    "ТВ Может": "ТВ может",
    "Кастомный ТВ": "Пользовательский телевизор",
    "Кастомный флаг": "Пользовательский флаг",
    "Кастомный ковёр": "Пользовательский ковёр",
    "из папки Asset.": "из папки Assets.",
    "youtube ссылки": "ссылки YouTube",
    "youtube-ссылки": "ссылки YouTube",
    "звёдном": "звёздном",
    "Требует включенную настройку [Пользовательский контент]": "Требуется включить настройку [Пользовательский контент]!",
    "Требует включённой настройки [Пользовательский контент]!": "Требуется включить настройку [Пользовательский контент]!",
    "Требует включения настройки [Пользовательский контент]!": "Требуется включить настройку [Пользовательский контент]!",
    'Смотрите «Справка и советы» для получения дополнительной информации.': "Подробнее см. в меню «Справка и советы».",
    'Для более подробной информации перейдите в меню "Справка и советы".': "Подробнее см. в меню «Справка и советы».",
    'Для более подробной информации перейдите в меню "Справка и советы"': "Подробнее см. в меню «Справка и советы».",
    "Для более подробной информации перейдите в меню «Справка и советы», расположенное в меню ESC, и найдите": (
        "Подробнее: откройте «Справка и советы» в меню ESC и найдите"
    ),
    "Для более подробной информации перейдите в меню «Справка и советы», расположенное в меню ESC.": (
        "Подробнее см. в меню «Справка и советы» в ESC."
    ),
    "(см. раздел помощи для получения дополнительной информации о телевизоре)": (
        "(подробнее о телевизоре см. в меню «Справка и советы»)"
    ),
    "Действует как открытый контейнер (см. раздел помощи «Открытый контейнер»)": (
        "Работает как открытый контейнер (см. «Открытый контейнер» в меню «Справка и советы»)"
    ),
    'Загляните в "Справка и советы" в меню паузы за советами по игровому процессу, если застряли.': (
        "Загляните в меню «Справка и советы» в паузе, если застряли."
    ),
    "Проверьте «Справка и советы»": "Загляните в «Справка и советы»",
    '"Справка и советы"': "«Справка и советы»",
    "Зажав ALT": "зажав ALT",
    "Зажав ЛКМ": "зажав ЛКМ",
    "Зажмите ПКМ чтобы": "Зажмите ПКМ, чтобы",
    "зажмите ПКМ чтобы": "зажмите ПКМ, чтобы",
    " и Нажмите ЛКМ": " и нажмите ЛКМ",
    " и Нажмите E": " и нажмите E",
    " — Нажмите ЛКМ": " — нажмите ЛКМ",
    " - Нажмите ЛКМ": " - нажмите ЛКМ",
    "Информация о рамке обводящей объект": "Информация об обводящей рамке",
    "могут отобразить их содержание": "могут отображать своё содержимое",
    "нажмите ЛКМ чтобы": "нажмите ЛКМ, чтобы",
    "считыватель клюк-карты": "считыватель ключ-карты",
    "на PIN-код панели": "на кодовой панели",
    "на PIN-код панель": "на кодовую панель",
    '"PIN-код панели"': "«Кодовые панели»",
}

EXACT_RUSSIAN_REPLACEMENTS = {
    "Билд ": "Строительство ",
    "отмена": "Отмена",
    "Стат-ка": "Статистика",
    "Инстр.": "Инструменты",
    "инстр.": "инструменты",
    "Объём": "Громкость",
    "Объём:": "Громкость:",
    "text box": "текстовое поле",
    "pigeon": "голубь",
    "голубь.": "голубь",
    "Теория Гауссова поля?": "Теория поля Гаусса?",
    "Слот диска": "Слот для диска",
    "Неприятная находка, но, она может ничего и не значить.": "Неприятная находка, но, может, это ничего и не значит.",
    "Неприятная находка, но, может это ничего.": "Неприятная находка, но, может, это ничего и не значит.",
    "Достать штучку": "Взять",
    "Разбитый дисплей странного оранжевого Керфура, с кровью на ней. Матрица полностью убита": (
        "Часть странного оранжевого робота Керфура. Сильно повреждена и покрыта брызгами крови"
    ),
    "Активен": "Активно",
    "Спокойный": "Окружение",
    "Сигарета во рту": "Сигарета уже во рту",
    "Обычный коврик, адаптируется к неровностям поверхности. Используйте для размещения ковра": (
        "Обычный ковёр, адаптируется к неровностям поверхности. Используйте для размещения ковра"
    ),
    "Обычный коврик, адаптирующийся к неровностям поверхности. Используйте для размещения ковра": (
        "Обычный ковёр, адаптируется к неровностям поверхности. Используйте для размещения ковра"
    ),
    "Мешок с мусором": "Мешок для мусора",
}

ENGLISH_EXACT_TRANSLATIONS = {
    "Auto": "Авто",
    "Charcoal": "Уголь",
    "Dither": "Дизеринг",
    "Green": "Зелёный",
    "Snap": "Привязка",
    "Temporal AA": "Временное сглаживание",
    "Tier Platinum": "Платиновый уровень",
    "Towers": "Вышки",
    "down": "вниз",
    "drink": "пить",
    "find": "найти",
    "soft": "мягкий",
    "Unknown device": "Неизвестное устройство",
    "pigeon": "голубь",
    "text box": "текстовое поле",
    "Red": "Красный",
    "Wip": "В разработке",
    "Keypads": "Кодовые панели",
}


def normalized(text: str) -> str:
    return " ".join(text.split())


def set_contextual_translation(english: str) -> str | None:
    norm = normalized(english)

    if norm == "2d platformer pc minigame failed test":
        return "Проваленный тест мини-игры: 2D-платформер для ПК"

    if norm == "3d printer test":
        return "тест 3D-принтера"

    if english.startswith("A large 3D printer, can print 3D objects sourced from Assets folder."):
        return (
            "Большой 3D-принтер. Печатает 3D-объекты из папки Assets.\r\n"
            "Максимальный размер объекта: 200x200x300 единиц\r\n"
            "\r\n"
            "Требуется включить настройку «Веселье»"
        )

    if english.startswith("A small desktop 3D printer, can print 3D objects sourced from Assets folder."):
        return (
            "Небольшой настольный 3D-принтер. Печатает 3D-объекты из папки Assets.\r\n"
            "Максимальный размер объекта: 35x45x60 единиц\r\n"
            "\r\n"
            "Требуется включить настройку «Веселье»"
        )

    if english.startswith("A pack of cigarretes, 20 cigs in a pack."):
        return (
            "Пачка сигарет, 20 штук.\r\n"
            "\r\n"
            "Как использовать:\r\n"
            "ПКМ - взять сигарету\r\n"
            "Чтобы зажечь сигарету - держите зажигалку, зажмите ALT и нажмите ПКМ\r\n"
            "Чтобы вынуть сигарету - с пустыми руками зажмите ALT и нажмите R"
        )

    if english.startswith("An empty pack of cigarretes."):
        return (
            "Пустая пачка сигарет.\r\n"
            "\r\n"
            "Как использовать:\r\n"
            "ПКМ - взять сигарету\r\n"
            "Чтобы зажечь сигарету - держите зажигалку, зажмите ALT и нажмите ПКМ\r\n"
            "Чтобы вынуть сигарету - с пустыми руками зажмите ALT и нажмите R"
        )

    if english.startswith("A sign of wealth."):
        return (
            "Признак богатства.\r\n"
            "\r\n"
            "Как использовать:\r\n"
            "ПКМ - взять сигару\r\n"
            "Чтобы зажечь сигару - держите зажигалку, зажмите ALT и нажмите ПКМ\r\n"
            "Чтобы вынуть сигару - с пустыми руками зажмите ALT и нажмите R"
        )

    if english.startswith("A portable metal detector, can be equipped."):
        return (
            "Портативный металлоискатель, можно взять в руки.\r\n"
            "Чтобы использовать: возьмите его, зажмите [Left Alt] (по умолчанию) и смотрите на землю"
        )

    if english == "Adjust the volume by holding E and use the Mouse Wheel to scroll.":
        return "Настройте громкость: зажмите E и прокрутите колёсико мыши."

    if english.startswith("Allows to remotely control the TV"):
        return (
            "Позволяет дистанционно управлять телевизором.\r\n"
            "\r\n"
            "Как пользоваться:\r\n"
            "ЛКМ по телевизору - привязать пульт\r\n"
            "ПКМ - вызвать телевизор"
        )

    if english.startswith("Each individual wheel of the ATV can be removed"):
        return (
            "Каждое колесо квадроцикла можно снять: держите гаечный ключ и зажмите ЛКМ на колесе "
            "(полезно для замены, ремонта или чистки). Чтобы установить колесо, держите его в руке "
            "и нажмите ЛКМ на пустом креплении."
        )

    if english.startswith("TV can play video files from the Asset folder"):
        return (
            "ТВ может воспроизводить видеофайлы из папки Assets. Также можно использовать online.txt "
            "для воспроизведения видео по ссылке (нужна прямая ссылка на видеофайл; ссылки YouTube не работают).\r\n"
            "\r\n"
            "Требуется включить настройку [Пользовательский контент]!\r\n"
            "Подробнее см. в меню «Справка и советы»."
        )

    if english.startswith("Uses images from the Asset folder"):
        return (
            "Использует изображения из папки Assets\r\n"
            "\r\n"
            "Требуется включить настройку [Пользовательский контент]!\r\n"
            "Подробнее см. в меню «Справка и советы»."
        )

    if english.startswith("Requires [Custom Content] setting enabled!"):
        return (
            "Требуется включить настройку [Пользовательский контент]!\r\n"
            "Подробнее см. в меню «Справка и советы»."
        )

    if english.startswith("Use the panel, locate a signal, and triangulate its position"):
        return (
            "Используйте панель, найдите сигнал и триангулируйте его положение. Нужно, чтобы сигнал оказался внутри треугольника, который вы рисуете на звёздной карте.\r\n"
            "Управление:\r\n"
            "WASD - двигать сенсор\r\n"
            "Left Shift - быстрое сканирование.\r\n"
            "Left Alt - переключаться между радарами.\r\n"
            "1,2,3 - навести прицел на соответствующий радар\r\n"
            "Enter - запустить пинг."
        )

    if english.startswith("Hold the keycard in your hand, then press LMB on the keycard slot on the keypad"):
        return "Держите ключ-карту в руке, затем нажмите ЛКМ на считыватель ключ-карты на кодовой панели, чтобы открыть дверь."

    if english.startswith("Keypads are found on most doors at a facility"):
        return (
            "Кодовые панели установлены на большинстве дверей комплекса. Они защищают помещения от "
            "несанкционированного доступа с помощью 4-5-значного цифрового кода."
        )

    if english.startswith("Some doors have keypads which use codes or, in this case, the keycard."):
        return (
            "На некоторых дверях есть кодовые панели; обычно для них нужен код, а в этом случае - ключ-карта.\r\n"
            "Чтобы открыть дверь, когда карта в руке, посмотрите на считыватель ключ-карты и нажмите ЛКМ"
        )

    if english.startswith("To exit the room, clear the way and enter"):
        return "Чтобы выйти из комнаты, расчистите путь и введите «1234» на кодовой панели."

    if english.startswith("While you have a keycard in HOLD, look at the keypad card slot"):
        return (
            "Когда ключ-карта в руке, посмотрите на считыватель ключ-карты на кодовой панели "
            "(щель справа) и нажмите ЛКМ.\r\n"
            "Если карта подходит, индикатор на панели загорится зелёным."
        )

    return ENGLISH_EXACT_TRANSLATIONS.get(english)


def polish(csv_path: Path, output_path: Path) -> tuple[int, Counter[str]]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise SystemExit(f"{csv_path}: empty CSV")
        fieldnames = list(reader.fieldnames)
        rows = list(reader)

    counts: Counter[str] = Counter()
    for row in rows:
        english = row.get("english", "")
        russian = row.get("russian", "")

        contextual = set_contextual_translation(english)
        if contextual is not None and contextual != russian:
            russian = contextual
            counts[f"context:{normalized(english)[:70]}"] += 1

        if russian in EXACT_RUSSIAN_REPLACEMENTS:
            old = russian
            russian = EXACT_RUSSIAN_REPLACEMENTS[old]
            counts[f"exact:{old}"] += 1

        for old, new in TEXT_REPLACEMENTS.items():
            hits = russian.count(old)
            if hits:
                russian = russian.replace(old, new)
                counts[old] += hits

        russian = russian.replace("можно изменить, Зажав F.", "можно изменить, нажав ALT + F.")
        row["russian"] = russian

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return len(rows), counts


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply a stricter context polish pass to Game_strings.csv.")
    parser.add_argument("--csv", type=Path, default=Path("translations/Game/Game_strings.csv"))
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    total, counts = polish(args.csv, args.output or args.csv)
    print(f"[INFO] rows={total}")
    for key, count in counts.most_common():
        print(f"[INFO] {key!r}: {count}")


if __name__ == "__main__":
    main()
