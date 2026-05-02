# Русский перевод Voices of the Void

Перевод для `Voices of the Void 0.9.0k`.

Основной перевод игры (`Game.locres`) основан на ручном переводе
Antoha256M и MrLololoshenka:

- Thunderstore: https://thunderstore.io/c/voices-of-the-void/p/Antoha256M/Manual_Russian_Translation/
- Профиль автора из манифеста: https://discord.com/users/887093938685616138

В этом репозитории поверх этой базы оставлены наши дополнительные патчи:
перевод `Engine.locres`, перевод меню настроек `ui_settings` и локальные
исправления. Подробности по источникам: `translations/SOURCES.md`.

## Что скачивать

Для полной русификации нужны три файла из корня репозитория:

- `ZZ_GameRuPatch_P.pak` - основной перевод игры.
- `ZZ_EngineRuPatch_P.pak` - перевод интерфейса движка.
- `ZZ_UISettingsRuPatch_P.pak` - перевод меню настроек.

Для Thunderstore-релиза эти же файлы собираются в один zip-пакет.

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

Сборка Thunderstore-пакета:

```bash
./tools/package_thunderstore.sh 1.0.0
```

Готовый zip появится в `dist/`.

## Вклад

Правки перевода принимаются через Pull Request. Основной файл строк:

```text
translations/Game/Game_strings.csv
```
