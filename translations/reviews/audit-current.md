# Translation Audit

* CSV rows: 19263
* Empty Russian strings: 0
* Format/control token mismatches: 0
* Probably untranslated same-as-English rows: 188
* Rows with reviewable Latin words in Russian: 822
* English strings with multiple Russian variants: 51

## Suspicious Term Counts

* `Помощь и Инфа`: 127
* `утчка`: 6
* `делаэт`: 3

## Format/Control Token Samples

_Нет._

## Probably Untranslated Samples

| line | english | russian | note |
| ---: | --- | --- | --- |
| 14 | uuuuuuu uu$$$$$$$$$$$uu uu$$$$$$$$$$$$$$$$$uu u$$$$$$$$$$$$$$$$$$$$$u u$$$$$$$$$$$$$$$$$$$$$$$u u$$$$$$$$$$$$$$$$$$$$$$$$$u u$$$$$$$$$$$$$$$$$$$$$$$$... | uuuuuuu uu$$$$$$$$$$$uu uu$$$$$$$$$$$$$$$$$uu u$$$$$$$$$$$$$$$$$$$$$u u$$$$$$$$$$$$$$$$$$$$$$$u u$$$$$$$$$$$$$$$$$$$$$$$$$u u$$$$$$$$$$$$$$$$$$$$$$$$... | same as English |
| 15 | uuuuuuu uu$$$$$$$$$$$uu uu$$$$$$$$$$$$$$$$$uu u$$$$$$$$$$$$$$$$$$$$$u u$$$$$$$$$$$$$$$$$$$$$$$u u$$$$$$$$$$$$$$$$$$$$$$$$$u u$$$$$$$$$$$$$$$$$$$$$$$$... | uuuuuuu uu$$$$$$$$$$$uu uu$$$$$$$$$$$$$$$$$uu u$$$$$$$$$$$$$$$$$$$$$u u$$$$$$$$$$$$$$$$$$$$$$$u u$$$$$$$$$$$$$$$$$$$$$$$$$u u$$$$$$$$$$$$$$$$$$$$$$$$... | same as English |
| 23 | | {a}/{b} | | {a}/{b} | same as English |
| 440 | "{a}" | "{a}" | same as English |
| 442 | "{a}" - {b} | "{a}" - {b} | same as English |
| 444 | ## #e## #es# uθ##### æ####### #θ#he#œ##a##aœg# ####θ œdsi# go ## ed ##sœ e##i.##o æ# a#####es# | ## #e## #es# uθ##### æ####### #θ#he#œ##a##aœg# ####θ œdsi# go ## ed ##sœ e##i.##o æ# a#####es# | same as English |
| 478 | ************/************/************/**#*********/************/0x6D98C60F67CA49EB3AE6CDB8/*#**********/*********#**/0x64291EEF5F4DECFF700F3E86/****... | ************/************/************/**#*********/************/0x6D98C60F67CA49EB3AE6CDB8/*#**********/*********#**/0x64291EEF5F4DECFF700F3E86/****... | same as English |
| 479 | ************/************/************/**#*********/************/0x6D98C60F67CA49EB3AE6CDB8/*#**********/*********#**/0x64291EEF5F4DECFF700F3E86/****... | ************/************/************/**#*********/************/0x6D98C60F67CA49EB3AE6CDB8/*#**********/*********#**/0x64291EEF5F4DECFF700F3E86/****... | same as English |
| 480 | ************/************/************/**#*********/************/0x6D98C60F67CA49EB3AE6CDB8/*#**********/*********#**/0x64291EEF5F4DECFF700F3E86/****... | ************/************/************/**#*********/************/0x6D98C60F67CA49EB3AE6CDB8/*#**********/*********#**/0x64291EEF5F4DECFF700F3E86/****... | same as English |
| 481 | ************/************/************/**#*********/************/0x6D98C60F67CA49EB3AE6CDB8/*#**********/*********#**/0x64291EEF5F4DECFF700F3E86/****... | ************/************/************/**#*********/************/0x6D98C60F67CA49EB3AE6CDB8/*#**********/*********#**/0x64291EEF5F4DECFF700F3E86/****... | same as English |
| 482 | ********/********/****#***/********#********/********/********/********/********/********/********/********/********/ACX.K<35/A2X.K<97/A8X.K<99/A5X.K... | ********/********/****#***/********#********/********/********/********/********/********/********/********/********/ACX.K<35/A2X.K<97/A8X.K<99/A5X.K... | same as English |
| 483 | ********/********/****#***/********#********/********/********/********/********/********/********/********/********/ACX.K<35/A2X.K<97/A8X.K<99/A5X.K... | ********/********/****#***/********#********/********/********/********/********/********/********/********/********/ACX.K<35/A2X.K<97/A8X.K<99/A5X.K... | same as English |
| 484 | ********/********/****#***/********#********/********/********/********/********/********/********/********/********/ACX.K<35/A2X.K<97/A8X.K<99/A5X.K... | ********/********/****#***/********#********/********/********/********/********/********/********/********/********/ACX.K<35/A2X.K<97/A8X.K<99/A5X.K... | same as English |
| 485 | ********/********/****#***/********#********/********/********/********/********/********/********/********/********/ACX.K<35/A2X.K<97/A8X.K<99/A5X.K... | ********/********/****#***/********#********/********/********/********/********/********/********/********/********/ACX.K<35/A2X.K<97/A8X.K<99/A5X.K... | same as English |
| 504 | +{a}/lvl | +{a}/lvl | same as English |
| 535 | -{a} | -{a} | same as English |
| 700 | 9999.99m | 9999.99m | same as English |
| 701 | 9999.99m | 9999.99m | same as English |
| 702 | 9999.99s | 9999.99s | same as English |
| 721 | <g>{perc}%</> | <g>{perc}%</> | same as English |

## Latin-In-Russian Samples

| line | english | russian | note |
| ---: | --- | --- | --- |
| 21 | - X{amount} |{item}|: for {points} points | - X{amount} |{item}|: за {points} очков | X |
| 26 | "Berd" award plushie | Наградная плюшевая игрушка "Berd" | Berd |
| 38 | "Charborg" award plushie | "Charborg" наградная плюшевая игрушка | Charborg |
| 39 | "Charborg" award plushie(?) | Наградная плюшевая игрушка(?) "Charborg" | Charborg |
| 40 | "Cocktail of Peace and Fire" hot sauce bottle | Бутылка горячего соуса "Cocktail of Peace and Fire" | Cocktail, Fire, Peace, and, of |
| 41 | "Cocktail of Peace and Fire" hot sauce bottle | Бутылка горячего соуса "Cocktail of Peace and Fire" | Cocktail, Fire, Peace, and, of |
| 42 | "Cocktail of Peace and Fire" hot sauce bottle | Бутылка горячего соуса "Cocktail of Peace and Fire" | Cocktail, Fire, Peace, and, of |
| 43 | "Cocktail of Peace and Fire" hot sauce bottle | Бутылка горячего соуса "Cocktail of Peace and Fire" | Cocktail, Fire, Peace, and, of |
| 44 | "Cocktail of Peace and Fire" hot sauce bottle | Бутылка горячего соуса "Cocktail of Peace and Fire" | Cocktail, Fire, Peace, and, of |
| 48 | "Gooseworx" award plushie | Наградная плюшевая игрушка "Gooseworx" | Gooseworx |
| 49 | "Gooseworx" award plushie | Наградная плюшевая игрушка "Gooseworx" | Gooseworx |
| 50 | "Gooseworx" award plushie | Наградная плюшевая игрушка "Gooseworx" | Gooseworx |
| 56 | "Jolly Wangcore" award plushie | Наградная плюшевая игрушка "Jolly Wangcore" | Jolly, Wangcore |
| 57 | "Jolly Wangcore" award plushie | Наградная плюшевая игрушка "Jolly Wangcore" | Jolly, Wangcore |
| 413 | "Minerva" award plushie | Наградная плюшевая игрушка "Minerva" | Minerva |
| 414 | "MonikaCinnyRoll" award plushie | Наградная плюшевая игрушка "MonikaCinnyRoll" | MonikaCinnyRoll |
| 419 | "Sam" award plushie | Наградная плюшевая игрушка "Sam" | Sam |
| 420 | "Spazmatic Banana" award plushie | Наградная плюшевая игрушка "Spazmatic Banana" | Banana, Spazmatic |
| 421 | "Spazmatic Banana" award plushie | Наградная плюшевая игрушка "Spazmatic Banana" | Banana, Spazmatic |
| 422 | "Spazmatic Banana" award plushie | Наградная плюшевая игрушка "Spazmatic Banana" | Banana, Spazmatic |

## Suspicious Term Samples

| line | english | russian | note |
| ---: | --- | --- | --- |
| 2614 | A heavy medium sized TV Requires [Custom Content] setting enabled! See "Hints and Tips" for more information. | Тяжёлый телевизор среднего размера Требует включения настройки [Пользовательский контент]! Смотрите «Помощь и Инфа» для получения дополнительной инфо... | меню Help & Info переведено разговорно, нужна редакторская проверка |
| 2615 | A heavy medium sized TV Requires [Custom Content] setting enabled! See "Hints and Tips" for more information. | Тяжёлый телевизор среднего размера Требует включения настройки [Пользовательский контент]! Смотрите «Помощь и Инфа» для получения дополнительной инфо... | меню Help & Info переведено разговорно, нужна редакторская проверка |
| 2616 | A heavy medium sized TV Requires [Custom Content] setting enabled! See "Hints and Tips" for more information. | Тяжёлый телевизор среднего размера Требует включения настройки [Пользовательский контент]! Смотрите «Помощь и Инфа» для получения дополнительной инфо... | меню Help & Info переведено разговорно, нужна редакторская проверка |
| 2617 | A heavy medium sized TV Requires [Custom Content] setting enabled! See "Hints and Tips" for more information. | Тяжёлый телевизор среднего размера Требует включения настройки [Пользовательский контент]! Смотрите «Помощь и Инфа» для получения дополнительной инфо... | меню Help & Info переведено разговорно, нужна редакторская проверка |
| 2618 | A heavy medium sized TV Requires [Custom Content] setting enabled! See "Hints and Tips" for more information. | Тяжёлый телевизор среднего размера Требует включения настройки [Пользовательский контент]! Смотрите «Помощь и Инфа» для получения дополнительной инфо... | меню Help & Info переведено разговорно, нужна редакторская проверка |
| 2619 | A heavy medium sized TV Requires [Custom Content] setting enabled! See "Hints and Tips" for more information. | Тяжёлый телевизор среднего размера Требует включения настройки [Пользовательский контент]! Смотрите «Помощь и Инфа» для получения дополнительной инфо... | меню Help & Info переведено разговорно, нужна редакторская проверка |
| 2620 | A heavy medium sized TV Requires [Custom Content] setting enabled! See "Hints and Tips" for more information. | Тяжёлый телевизор среднего размера Требует включения настройки [Пользовательский контент]! Смотрите «Помощь и Инфа» для получения дополнительной инфо... | меню Help & Info переведено разговорно, нужна редакторская проверка |
| 2635 | A horizontal picture. Can be hung on a wall. Requires [Custom Content] setting enabled! See "Hints and Tips" for more information. | Горизонтальная картина. Можно повесить на стену. Требует включения настройки [Пользовательский контент]! Смотрите «Помощь и Инфа» для получения допол... | меню Help & Info переведено разговорно, нужна редакторская проверка |
| 2636 | A horizontal picture. Can be hung on a wall. Requires [Custom Content] setting enabled! See "Hints and Tips" for more information. | Горизонтальная картина. Можно повесить на стену. Требует включения настройки [Пользовательский контент]! Смотрите «Помощь и Инфа» для получения допол... | меню Help & Info переведено разговорно, нужна редакторская проверка |
| 2637 | A horizontal picture. Can be hung on a wall. Requires [Custom Content] setting enabled! See "Hints and Tips" for more information. | Горизонтальная картина. Можно повесить на стену. Требует включения настройки [Пользовательский контент]! Смотрите «Помощь и Инфа» для получения допол... | меню Help & Info переведено разговорно, нужна редакторская проверка |
| 2638 | A horizontal picture. Can be hung on a wall. Requires [Custom Content] setting enabled! See "Hints and Tips" for more information. | Горизонтальная картина. Можно повесить на стену. Требует включения настройки [Пользовательский контент]! Смотрите «Помощь и Инфа» для получения допол... | меню Help & Info переведено разговорно, нужна редакторская проверка |
| 2639 | A horizontal picture. Can be hung on a wall. Requires [Custom Content] setting enabled! See "Hints and Tips" for more information. | Горизонтальная картина. Можно повесить на стену. Требует включения настройки [Пользовательский контент]! Смотрите «Помощь и Инфа» для получения допол... | меню Help & Info переведено разговорно, нужна редакторская проверка |
| 2640 | A horizontal picture. Can be hung on a wall. Requires [Custom Content] setting enabled! See "Hints and Tips" for more information. | Горизонтальная картина. Можно повесить на стену. Требует включения настройки [Пользовательский контент]! Смотрите «Помощь и Инфа» для получения допол... | меню Help & Info переведено разговорно, нужна редакторская проверка |
| 2641 | A horizontal picture. Can be hung on a wall. Requires [Custom Content] setting enabled! See "Hints and Tips" for more information. | Горизонтальная картина. Можно повесить на стену. Требует включения настройки [Пользовательский контент]! Смотрите «Помощь и Инфа» для получения допол... | меню Help & Info переведено разговорно, нужна редакторская проверка |
| 2642 | A horizontal picture. Can be hung on a wall. Requires [Custom Content] setting enabled! See "Hints and Tips" for more information. | Горизонтальная картина. Можно повесить на стену. Требует включения настройки [Пользовательский контент]! Смотрите «Помощь и Инфа» для получения допол... | меню Help & Info переведено разговорно, нужна редакторская проверка |
| 2643 | A horizontal picture. Can be hung on a wall. Requires [Custom Content] setting enabled! See "Hints and Tips" for more information. | Горизонтальная картина. Можно повесить на стену. Требует включения настройки [Пользовательский контент]! Смотрите «Помощь и Инфа» для получения допол... | меню Help & Info переведено разговорно, нужна редакторская проверка |
| 2644 | A horizontal picture. Can be hung on a wall. Requires [Custom Content] setting enabled! See "Hints and Tips" for more information. | Горизонтальная картина. Можно повесить на стену. Требует включения настройки [Пользовательский контент]! Смотрите «Помощь и Инфа» для получения допол... | меню Help & Info переведено разговорно, нужна редакторская проверка |
| 2645 | A horizontal picture. Can be hung on a wall. Requires [Custom Content] setting enabled! See "Hints and Tips" for more information. | Горизонтальная картина. Можно повесить на стену. Требует включения настройки [Пользовательский контент]! Смотрите «Помощь и Инфа» для получения допол... | меню Help & Info переведено разговорно, нужна редакторская проверка |
| 2653 | A huge plasma tv, can be attached to the wall. Requires [Custom Content] setting enabled! See "Hints and Tips" for more information. | Огромный плазменный телевизор, можно прикрепить к стене. Требует включения настройки [Пользовательский контент]! Смотрите «Помощь и Инфа» для получен... | меню Help & Info переведено разговорно, нужна редакторская проверка |
| 2654 | A huge plasma tv, can be attached to the wall. Requires [Custom Content] setting enabled! See "Hints and Tips" for more information. | Огромный плазменный телевизор, можно прикрепить к стене. Требует включения настройки [Пользовательский контент]! Смотрите «Помощь и Инфа» для получен... | меню Help & Info переведено разговорно, нужна редакторская проверка |

## Duplicate English With Variant Russian Samples

| line | english | russian | note |
| ---: | --- | --- | --- |
| 4409 | A part of the weird orange Kerfur robot. Heavily damaged and covered with blood splatters | Разбитый дисплей странного оранжевого Керфура, с кровью на ... / Часть странного оранжевого робота Керфура. Сильно поврежден... | 2 variants |
| 5332 | Active | Активно / Активно / Активен / Активно | 2 variants |
| 5430 | Ambience | Окружение / Спокойный | 2 variants |
| 5476 | An empty plastic bottle. | Пустая пластиковая бутылка. Мусор, который можно утилизиров... / Пустая пластиковая бутылка. Мусор, который можно утилизиров... / Пустая пластиковая бутылка. Мусор, который можно утилизиров... / Пустая пластиковая бутылка. Мусор, который можно утилизиров... | 2 variants |
| 6269 | Basic | Базовое / Базовые | 2 variants |
| 6540 | Bone | Кость (череп) / Кость (череп) / Кость (череп) / Кость (череп) | 5 variants |
| 7160 | Build | Строительство / Строительство / Строительство / Строительство | 3 variants |
| 7387 | Calculations | O6PA6OTKA / Обработка | 2 variants |
| 7800 | Cancel | Отмена / Отмена / отмена | 2 variants |
| 8403 | Cig is quipped | Сигарета во рту / Сигарета уже во рту / Сигарета уже во рту | 2 variants |
| 8753 | Coordinates | KOOPDNHATbI / Координаты | 2 variants |
| 9164 | Deer part | Конечность оленя / Конечность оленя / Конечность оленя / Конечность оленя | 3 variants |
| 9224 | Default rug, adapts over the uneven terrain. Use to place the rug | Обычный ковёр, адаптируется к неровностям поверхности. Испо... / Обычный коврик, адаптируется к неровностям поверхности. Исп... / Обычный ковёр, адаптируется к неровностям поверхности. Испо... / Обычный коврик, адаптируется к неровностям поверхности. Исп... | 3 variants |
| 9351 | Disc slot | Слот для диска / Слот диска | 2 variants |
| 9367 | Disturbing find, but maybe it's nothing. | Неприятная находка, но, она может ничего и не значить. / Неприятная находка, но, может это ничего. | 2 variants |
| 9397 | Downloading | Загрузка / 3AI`PY3KA | 2 variants |
| 9992 | Equipment | Надето / Надето / Экипировка | 2 variants |
| 10526 | Garbage bag | Мешок с мусором / Мешок с мусором / Мешок с мусором / Мешок с мусором | 2 variants |
| 10742 | Gaussian field theory? | Теория Гауссова поля? / Теория поля Гаусса? | 2 variants |
| 11619 | Kerfur part | Сломанный дисплей Керфура / Часть корпуса Керфура | 2 variants |

## Most Common Reviewable Latin Words

* `u`: 108
* `E`: 103
* `D`: 100
* `qwe`: 67
* `Assets`: 43
* `K`: 40
* `R`: 36
* `z`: 34
* `A`: 31
* `x1`: 30
* `r`: 28
* `X`: 26
* `Alt`: 25
* `uu`: 24
* `o`: 23
* `txt`: 23
* `g`: 22
* `sv`: 22
* `x2`: 21
* `n`: 19
* `online`: 19
* `Shift`: 17
* `h`: 17
* `k`: 17
* `e`: 16
* `i`: 16
* `C`: 16
* `youtube`: 16
* `x300`: 15
* `a`: 14
