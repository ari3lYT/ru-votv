# Русский перевод Voices of the Void

Перевод для `Voices of the Void 0.9.0k`.

## Что скачивать

Для полной русификации нужны три файла из корня репозитория:

- `ZZ_GameRuPatch_P.pak` - основной перевод игры.
- `ZZ_EngineRuPatch_P.pak` - перевод интерфейса движка.
- `ZZ_UISettingsRuPatch_P.pak` - перевод меню настроек.

## Установка

1. Открой папку игры.
2. Перейди в:

   ```text
   WindowsNoEditor/VotV/Content/Paks/
   ```

3. Скопируй туда `.pak` файлы без переименования.
4. Запусти игру.

Чтобы удалить перевод, убери эти `.pak` файлы из папки `Paks`.

Если после обновления игры сломалось только меню настроек, сначала удали
`ZZ_UISettingsRuPatch_P.pak`. Основной перевод `Game/Engine` обычно не зависит
от бинарных UI-ассетов.

## Совместимость

Поддерживается:

- Voices of the Void `0.9.0k`
- Windows
- Linux через Proton 9.0

Другие версии игры этим релизом не заявлены.

## Сборка

Для пересборки основного перевода нужен Python 3 и `pylocres`:

```bash
python -m pip install pylocres
python translations/build_game_locres.py \
  --strings translations/Game/Game_strings.csv \
  --locres VotV/Content/Localization/Game/en/Game.locres \
  --output translations/output/Game_ru.locres
```

Для пересборки `ZZ_UISettingsRuPatch_P.pak` нужен `repak` и Rust/Cargo:

```bash
python3 translations/build_ui_settings_pak.py \
  --game-pak /path/to/WindowsNoEditor/VotV/Content/Paks/VotV-WindowsNoEditor.pak \
  --output ZZ_UISettingsRuPatch_P.pak
```

## Вклад

Правки перевода принимаются через Pull Request. Основной файл строк:

```text
translations/Game/Game_strings.csv
```
