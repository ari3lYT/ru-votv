# 🇷🇺 Перевод *Voices of the Void*

> Актуальное состояние репозитория: обновлённый `Game.locres` и патч-паки для ветки `0.9.0` (`Build a09i` / локальная сборка `a09j_0001`).

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
* Перевод генерировался автоматически, без полной ручной корректуры — возможны неточности.
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

Этого достаточно, потому что:

* `translations/build_game_locres.py` собирает `Game.locres` через `pylocres`
* `tools/pack.py` использует уже вложенный в репозиторий `tools/u4pak/u4pak.py`, отдельный упаковщик скачивать не нужно

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

mkdir -p translations/output/Game_ru/Localization/Game/ru
cp translations/output/Game_ru.locres translations/output/Game_ru/Localization/Game/ru/Game.locres

python tools/pack.py \
  translations/output/Game_ru \
  translations/output/ZZ_GameRuPatch_P.pak \
  --mount-point ../../../VotV/Content/
```

На выходе получишь:

* `translations/output/Game_ru.locres`
* `translations/output/ZZ_GameRuPatch_P.pak`

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
   mkdir -p translations/output/Game_ru/Localization/Game/ru
   cp translations/output/Game_ru.locres translations/output/Game_ru/Localization/Game/ru/Game.locres
   python tools/pack.py translations/output/Game_ru translations/output/ZZ_GameRuPatch_P.pak --mount-point ../../../VotV/Content/
   ```
4. Протестируй файл, положив его в `VotV/Content/Paks/`, и присылай Pull Request с обновлённым CSV и `.pak`.

Текущий `translations/Game/Game_strings.csv` уже синхронизирован с актуальным `Game.locres` и содержит `16832` строк.

Аналогично можно обновить `Engine.locres` и собрать `ZZ_EngineRuPatch_P.pak`.
