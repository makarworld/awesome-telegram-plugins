# awesome-plugins

Коллекция плагинов для **exteraGram / AyuGram** (Android, Python через Chaquopy).

> Обновлено: 2026-07-20

## О репозитории

Монорепозиторий плагинов. Каждый плагин — отдельная папка с исходником (`.py` или `.plugin`) и `docs.md` с детальной документацией.

### Флоу работы

1. Читать **этот файл** — обзор всех плагинов.
2. Читать **`ПапкаПлагина/docs.md`** — детали конкретного плагина.
3. После изменений обновлять оба уровня документации.

Правило для агента: `.cursor/rules/plugin-workflow.mdc`

## Окружение

| | |
|---|---|
| Клиент | exteraGram / AyuGram (Android) |
| SDK | https://plugins.exteragram.app/docs |
| Python | Chaquopy (Python ↔ Java interop) |
| IDE | `pip install exteragram-utils` (автодополнение; pyright-ошибки импортов — норма) |
| Исходник | `*.py` в папке плагина |
| Артефакт | `*.plugin` — результат сборки |

### Сборка и деплой

Локальный артефакт (копия `.py` → `.plugin` в папке плагина):

```bat
tools\build_plugin.bat CuteMessages
:: → CuteMessages\cutemessagesenhanced.plugin
```

Деплой на устройство — вручную через клиент или (если есть) `python tools/deploy.py`.

## Каталог плагинов

| Папка | ID | Версия | Автор | Назначение | Исходник | docs |
|-------|----|--------|-------|------------|----------|------|
| [CuteMessages](CuteMessages/docs.md) | `cutemessagesenhanced` | 1.7.4 | @mihailkotovski & @mishabotov | Стилизация исходящих сообщений | `cutemessagesenhanced.py` | ✅ |
| [KangelPluginsManager](KangelPluginsManager/docs.md) | `kangel_plugins_manager` | 1.3.2 | @ArThirtyFour \| @KangelPlugins | Магазин плагинов | `.plugin` | ✅ |
| [LiveWallpaper](LiveWallpaper/docs.md) | `live_wallpaper` | 1.1 | @swagnonher | Живые обои в чатах | `.plugin` | ✅ |
| [UnlimitedPins](UnlimitedPins/docs.md) | `misha_unlimited_pins` | 2.0 | @mihailkotovski & @mishabotov | Больше закреплённых чатов | `.plugin` | ✅ |
| [PluginVerifier](PluginVerifier/docs.md) | `plugin_verifier` | 2.4.8 | @JasonVurhyz | Верификация и анализ плагинов | `.plugin` | ✅ |
| [ListOfCommands](ListOfCommands/docs.md) | `list_of_commands` | 1.0.8 | @bandaliyev | Подсказки dot-команд | `.plugin` | ✅ |
| [TomatoBom](TomatoBom/docs.md) | `tomato_bom` | 1.2.8 | Windukk | Кидает помидоры | `.plugin` | ✅ |
| [AIEdit](AIEdit/docs.md) | `ai_edit` | 1.0.1 | @abuztrade | AI-редактирование исходящих сообщений | `ai_edit.py` | ✅ |

## Сводка по типам

### По механизму работы

| Тип | Плагины |
|-----|---------|
| Send message hook | CuteMessages, KangelPluginsManager (`.kpm_send`), ListOfCommands (`.preload`), AIEdit |
| Method / protocol hooks | UnlimitedPins, PluginVerifier, KangelPluginsManager, ListOfCommands |
| Remote code (DEX) | LiveWallpaper |
| UI overlay | TomatoBom |
| Сеть | KangelPluginsManager, LiveWallpaper, PluginVerifier, TomatoBom, AIEdit |

### Минимальные версии клиента

| Плагин | `__min_version__` |
|--------|-------------------|
| CuteMessages | 11.9.0 |
| KangelPluginsManager | 12.1.1 |
| LiveWallpaper | 11.12.0 |
| ListOfCommands | 11.12.0 |
| UnlimitedPins | — |
| PluginVerifier | — |
| TomatoBom | — |
| AIEdit | 12.8.0 |

## Безопасность (кратко)

| Плагин | Риск | Причина |
|--------|------|---------|
| CuteMessages | низкий | Только модификация исходящих сообщений |
| KangelPluginsManager | **высокий** | Устанавливает плагины из интернета + телеметрия |
| LiveWallpaper | **критический** | Загружает и исполняет remote DEX |
| UnlimitedPins | низкий | Локальная манипуляция лимитов |
| PluginVerifier | **критический** | Полезен, но содержит скрытый anti-tamper в себе |
| ListOfCommands | низкий | Только парсинг файлов плагинов |
| TomatoBom | низкий–средний | Overlay + загрузка ассетов с gitflic |
| AIEdit | низкий–средний | Вызов официального AI API Telegram; текст уходит на сервер Cocoon |

Подробности — в `docs.md` каждого плагина и в `secure.md` (отчёты сгенерированы [Pluggy Bot](https://t.me/pluggy_robot)).

## Структура репозитория

```
awesome-plugins/
  docs.md                          # этот файл — каталог
  .cursor/rules/plugin-workflow.mdc
  CuteMessages/
    cutemessagesenhanced.py
    docs.md
    releases/
      v1.7.0/
        cutemessagesenhanced_v1.7.0.plugin
        secure_1.7.0.md
  KangelPluginsManager/
    kangel_plugins_manager.plugin
    docs.md
    releases/
      v1.3.2/
        kangel_plugins_manager_v1.3.2.plugin
        secure_1.3.2.md
  LiveWallpaper/
    live_wallpaper.plugin
    docs.md
    releases/
      v1.1/
        live_wallpaper_v1.1.plugin
        secure_1.1.md
  UnlimitedPins/
    misha_unlimited_pins.plugin
    docs.md
    releases/
      v2.0/
        misha_unlimited_pins_v2.0.plugin
        secure_2.0.md
  PluginVerifier/
    plugin_verifier.plugin
    docs.md
    releases/
      v2.4.8/
        plugin_verifier_v2.4.8.plugin
        secure_2.4.8.md
  ListOfCommands/
    list_of_commands.plugin
    docs.md
    releases/
      v1.0.8/
        list_of_commands_v1.0.8.plugin
        secure_1.0.8.md
  TomatoBom/
    tomato_bom.plugin
    docs.md
    releases/
      v1.2.8/
        tomato_bom_v1.2.8.plugin
        secure_1.2.8.md
  AIEdit/
    ai_edit.py
    docs.md
```

## Заметки

- **CuteMessages** — единственный плагин с отдельным `.py` исходником; остальные хранятся как `.plugin` (валидный Python).
- У каждого плагина есть `secure.md` в корне папки (актуальная проверка) и `releases/v{version}/` — снимок `{name}_v{version}.plugin` и архивный отчёт `secure_{version}.md`. Отчёты генерируются **[Pluggy Bot](https://t.me/pluggy_robot)** (pluggy_robot.t.me).
- **CuteMessages/docs.md** содержит также общую базу знаний по SDK exteraGram (хуки, entities, локализация).
- При извлечении `.plugin` → `.py` для других плагинов — обновить таблицу «Исходник» в этом файле.

## Полезные ссылки

| Ресурс | URL |
|--------|-----|
| SDK docs | https://plugins.exteragram.app/docs |
| Plugin class API | https://plugins.exteragram.app/docs/plugin-class |
| First plugin tutorial | https://plugins.exteragram.app/docs/first-plugin |
| KPM Store | https://github.com/KangelPlugins/Plugins-Store |
