# 🇷🇺 Перевод *Voices of the Void*

> Актуальное состояние репозитория: обновлённый `Game.locres` и патч-паки для ветки `0.9.0` (проверочная локальная сборка `a09k`).

---

## 📦 Файлы из архива

* **`ZZ_GameRuPatch_P.pak`** — перевод игрового контента (*Game.locres*), обновлённый под текущую `0.9.0` сборку.
* **`ZZ_EngineRuPatch_P.pak`** — перевод интерфейса движка (*Engine.locres*).
  Если перевод меню экрана/движка не нужен, этот файл можно не класть.
* **`ZZ_UISettingsRuPatch_P.pak`** — перевод вшитых текстов меню настроек (`ui_settings.uasset/.uexp`), которые не покрываются обычным `locres`.

---

## 🔧 Установка

1. Открой папку с установленной игрой.
2. Перейди в:

   ```
   WindowsNoEditor/VotV/Content/Paks/
   ```

   Пример пути:
   `C:/Voices Of The Void/a09_0015/WindowsNoEditor/VotV/Content/Paks`
3. Скопируй в эту папку нужные `.pak` файлы **без переименования** — порядок загрузки зависит от имени.
4. Для полной русификации настроек используй вместе `ZZ_GameRuPatch_P.pak` и `ZZ_UISettingsRuPatch_P.pak`.
5. Запускай игру — перевод подключится сам.
6. Чтобы убрать перевод, просто удали эти `.pak`.

---

## 🛠 Как делался перевод

* Исходные тексты извлечены из оригинальных UE4-локализаций (`.locres`).
* Текущий `Game_strings.csv` синхронизирован с актуальным `Game.locres`: `19263` строки.
* Обычные игровые строки переведены; `480` строк оставлены как есть, потому что это технические токены, числа, URL, id, форматы и плейсхолдеры.
* Перевод частично генерировался автоматически, без полной ручной корректуры — возможны неточности.
* Всё собрано обратно в `.locres` и упаковано в `.pak` с корректным mount-point, чтобы перекрывать оригинальные файлы при запуске.
* Часть строк в меню настроек была вшита прямо в `ui_settings`-ассет, поэтому для них собран отдельный UI override-пак.

---

## 🧪 Поддержка и тесты

### Проверено на системах

* Windows 11 Pro 24H2 (OS Build 26100)
* Proton 9.0-4

### Рабочие версии игры

* ✔️ **Alpha 0.9.0 / Build a09i**
* ✔️ **локальная сборка `a09j_0001`** под Proton
* ✔️ **локальная сборка `a09k`** под Proton

Если у тебя другой билд `0.9.0`, ориентируйся не по имени папки, а по факту:
если игра подхватывает `_P.pak` из `VotV/Content/Paks`, этот патч должен монтироваться.

---

## 🤝 Вклад

Хочешь помочь? Делай правки, улучшай текст, открывай форк — вклад приветствуется.

### Что нужно установить для сборки

Минимальный набор для пересборки `Game.locres` и упаковки `.pak` в этом репозитории такой:

1. `Python 3.10+`
2. `pip`
3. пакет `pylocres`

Команда установки:

```bash
python -m pip install pylocres
```

Этого достаточно для сборки `Game_ru.locres`, потому что:

* `translations/build_game_locres.py` собирает `Game.locres` через `pylocres`
* `tools/pack.py` использует уже вложенный в репозиторий `tools/u4pak/u4pak.py`, отдельный упаковщик скачивать не нужно для локальной тестовой упаковки

Релизный `ZZ_GameRuPatch_P.pak` в корне репозитория упакован через `repak` в формате `V11`
с тем же типом индекса, что и основной pak текущей сборки игры. Если хочешь пересобрать именно
релизный `.pak`, установи `repak` отдельно.

Если хочешь ещё и вытаскивать исходные `.locres` из игры сам, а не только пересобирать уже готовый CSV, тогда дополнительно пригодится любой распаковщик `.pak`, например `repak`, `u4pak` или `FModel`. Но для самой сборки перевода из этого репо они не обязательны.

### Быстрый цикл сборки

Если у тебя уже есть этот репозиторий и ты просто хочешь изменить строки и собрать новый патч:

1. Отредактируй `translations/Game/Game_strings.csv`.
2. Положи рядом базовый английский `Game.locres` из игры.
3. Собери новый `locres`.
4. Упакуй его в `.pak`.

Пример команд:

```bash
python translations/build_game_locres.py \
  --strings translations/Game/Game_strings.csv \
  --locres VotV/Content/Localization/Game/en/Game.locres \
  --output translations/output/Game_ru.locres

mkdir -p translations/output/Game_ru_repak/VotV/Content/Localization/Game/ru
cp translations/output/Game_ru.locres translations/output/Game_ru_repak/VotV/Content/Localization/Game/ru/Game.locres

repak pack \
  --version V11 \
  --path-hash-seed 1476701736 \
  --mount-point ../../../ \
  translations/output/Game_ru_repak \
  translations/output/ZZ_GameRuPatch_P.pak
```

На выходе получишь:

* `translations/output/Game_ru.locres`
* `translations/output/ZZ_GameRuPatch_P.pak`

### Хелпер для дублей

В `Game_strings.csv` одинаковый `english` может встречаться много раз с разными `id`. Для этого есть отдельный скрипт:

```bash
python translations/duplicate_helper.py scan --only-conflicts --limit 20
```

Он покажет группы, где один и тот же `english` имеет несколько вариантов `russian`.

Синхронизировать конкретную группу:

```bash
python translations/duplicate_helper.py sync \
  --english "Bone" \
  --strategy translated-most-common \
  --write
```

Что делает стратегия `translated-most-common`:

* если среди дублей уже есть русские варианты, берёт самый частый русский вариант
* если русских вариантов нет, берёт самый частый непустой вариант

Синхронизировать сразу все конфликтующие дубли:

```bash
python translations/duplicate_helper.py sync --all-conflicts --strategy translated-most-common --write
```

### Сравнение с форком xXimuS

Для сравнения переводов из форка можно запустить:

```bash
python translations/import_fork_translations.py
```

Скрипт клонирует/обновляет `xXimuS/ru-votv`, сравнивает переводы сначала по точному `id`,
потом по совпадающему английскому тексту, проверяет сохранность `{...}` и markup-токенов
и пишет подробный отчёт в `translations/fork-xximus-translation-diff.csv`.

Автоматически вливать весь форк в релизный CSV не стоит: там есть и полезные смысловые
исправления, и чисто стилевые правки, и спорные места. Краткий разбор лежит в
`translations/reviews/xximus-fork-review.md`. После ручной проверки можно применить
выбранные строки или запустить скрипт с `--write` на отдельной ветке.

### GUI без повторов

Если не хочешь редактировать CSV руками, есть кроссплатформенный GUI на стандартном `Tkinter`:

```bash
python translations/gui_translator.py
```

Что умеет:

* показывает каждую уникальную строку `english` только один раз
* редактирует один `russian` сразу для всей группы дублей
* ищет по строкам и фильтрует `translated / untranslated / conflict`
* показывает все `id`, которые входят в группу
* показывает переносы строк как `↵`
* сохраняет начальные/конечные пробелы и переносы без `strip`-нормализации
* показывает номера строк в редакторе и номер строки в списке
* корректно заменяет выделение при `Ctrl+V`
* умеет автосохранять CSV
* умеет сохранять CSV
* умеет прямо из окна собрать `Game_ru.locres` и упаковать `ZZ_GameRuPatch_P.pak`

Можно сразу указать свои пути:

```bash
python translations/gui_translator.py \
  --csv translations/Game/Game_strings.csv \
  --locres VotV/Content/Localization/Game/en/Game.locres \
  --output-locres translations/output/Game_ru.locres \
  --output-pak translations/output/ZZ_GameRuPatch_P.pak
```

Если на твоей системе Tk криво рендерит кириллицу или интерфейс слишком мелкий, можно переопределить шрифт и масштаб вручную:

```bash
python translations/gui_translator.py \
  --csv translations/Game/Game_strings.csv \
  --font-family clearlyu \
  --mono-font-family "nimbus mono l" \
  --scale 1.25
```

Если упаковка не срабатывает, сначала проверь:

* что `python` действительно запускает Python 3
* что `pylocres` установлен в тот же интерпретатор
* что структура перед упаковкой именно такая: `Localization/Game/ru/Game.locres`
* что имя итогового файла остаётся с суффиксом `_P.pak`, иначе игра может не перекрыть оригинальные ресурсы

Мини-инструкция для контрибьюторов:
1. Отредактируй `translations/Game/Game_strings.csv` (колонки `id / english / russian`).
2. Собери обновлённый `Game.locres` командой:
   ```bash
   python translations/build_game_locres.py
   ```
   Результат появится в `translations/output/Game_ru.locres`.
3. Подготовь структуру `Localization/Game/ru/Game.locres` и упакуй `.pak`:
   ```bash
   mkdir -p translations/output/Game_ru_repak/VotV/Content/Localization/Game/ru
   cp translations/output/Game_ru.locres translations/output/Game_ru_repak/VotV/Content/Localization/Game/ru/Game.locres
   repak pack --version V11 --path-hash-seed 1476701736 --mount-point ../../../ translations/output/Game_ru_repak translations/output/ZZ_GameRuPatch_P.pak
   ```
4. Протестируй файл, положив его в `VotV/Content/Paks/`, и присылай Pull Request с обновлённым CSV и `.pak`.

Текущий `translations/Game/Game_strings.csv` уже синхронизирован с актуальным `Game.locres` и содержит `19263` строки.

Аналогично можно обновить `Engine.locres` и собрать `ZZ_EngineRuPatch_P.pak`.
