# awesome-plugins

Коллекция плагинов для **exteraGram / AyuGram** (Android, Python через Chaquopy).

> Обновлено: 2026-07-21

## О репозитории

Монорепозиторий плагинов. Каждый плагин — отдельная папка с исходником (`.py` или `.plugin`) и `README.md` с детальной документацией.

### Флоу работы

1. Читать **[`README.md`](README.md)** — обзор для пользователей.
2. Читать **`ПапкаПлагина/README.md`** — детали плагина (**обязательно перед правками**).
3. Этот **`docs.md`** — сводная таблица версий и статусов (обновлять при релизах).

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
| [CuteMessages](CuteMessages/README.md) | `cutemessagesenhanced` | 1.7.1 | @mihailkotovski & @mishabotov | Стилизация исходящих сообщений | `cutemessagesenhanced.py` | ✅ |
| [KangelPluginsManager](KangelPluginsManager/README.md) | `kangel_plugins_manager` | 1.3.2 | @ArThirtyFour \| @KangelPlugins | Магазин плагинов | `.plugin` | ✅ |
| [LiveWallpaper](LiveWallpaper/README.md) | `live_wallpaper` | 1.2 | @swagnonher | Живые обои в чатах | `.plugin` | ✅ |
| [UnlimitedPins](UnlimitedPins/README.md) | `misha_unlimited_pins` | 2.0 | @mihailkotovski & @mishabotov | Больше закреплённых чатов | `.plugin` | ✅ |
| [PluginVerifier](PluginVerifier/README.md) | `plugin_verifier` | 2.4.8 | @JasonVurhyz | Верификация и анализ плагинов | `.plugin` | ✅ |
| [ListOfCommands](ListOfCommands/README.md) | `list_of_commands` | 1.0.8 | @bandaliyev | Подсказки dot-команд | `.plugin` | ✅ |
| [TomatoBom](TomatoBom/README.md) | `tomato_bom` | 1.2.8 | Windukk | Кидает помидоры | `.plugin` | ✅ |
| [AIEdit](AIEdit/README.md) | `ai_edit` | 1.0.1 | @abuztrade | AI-редактирование исходящих сообщений | `ai_edit.py` | ✅ |
| [WSBypass](WSBypass/README.md) | `wsbypass` | 3.0.5 | @Th3Nek1t_projects | Обход блокировок Telegram | `.plugin` | ✅ |

## Сводка по типам

### По механизму работы

| Тип | Плагины |
|-----|---------|
| Send message hook | CuteMessages, KangelPluginsManager (`.kpm_send`), ListOfCommands (`.preload`), AIEdit |
| Method / protocol hooks | UnlimitedPins, PluginVerifier, KangelPluginsManager, ListOfCommands, WSBypass |
| Remote code (DEX) | LiveWallpaper |
| UI overlay | TomatoBom |
| Сеть | KangelPluginsManager, LiveWallpaper, PluginVerifier, TomatoBom, AIEdit, WSBypass |
| Локальный прокси / туннель | WSBypass |

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
| WSBypass | 12.5.1 |

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
| WSBypass | низкий–средний | Туннель через KWS-серверы, смена прокси, автообновление с th3web.com |

Подробности — в `README.md` каждого плагина и в `secure.md` (отчёты сгенерированы [Pluggy Bot](https://t.me/pluggy_robot)).

## Структура репозитория

```
awesome-plugins/
  docs.md                          # этот файл — каталог
  .cursor/rules/plugin-workflow.mdc
  CuteMessages/
    cutemessagesenhanced.py
    README.md
    releases/
      v1.7.0/
        cutemessagesenhanced_v1.7.0.plugin
        secure_1.7.0.md
  KangelPluginsManager/
    kangel_plugins_manager.plugin
    README.md
    releases/
      v1.3.2/
        kangel_plugins_manager_v1.3.2.plugin
        secure_1.3.2.md
  LiveWallpaper/
    live_wallpaper.plugin
    README.md
    releases/
      v1.1/
        live_wallpaper_v1.1.plugin
        secure_1.1.md
  UnlimitedPins/
    misha_unlimited_pins.plugin
    README.md
    releases/
      v2.0/
        misha_unlimited_pins_v2.0.plugin
        secure_2.0.md
  PluginVerifier/
    plugin_verifier.plugin
    README.md
    releases/
      v2.4.8/
        plugin_verifier_v2.4.8.plugin
        secure_2.4.8.md
  ListOfCommands/
    list_of_commands.plugin
    README.md
    releases/
      v1.0.8/
        list_of_commands_v1.0.8.plugin
        secure_1.0.8.md
  TomatoBom/
    tomato_bom.plugin
    README.md
    releases/
      v1.2.8/
        tomato_bom_v1.2.8.plugin
        secure_1.2.8.md
  AIEdit/
    ai_edit.py
    README.md
  WSBypass/
    wsbypass.plugin
    README.md
    secure.md
    releases/
      v3.0.5/
        wsbypass_v3.0.5.plugin
        secure_3.0.5.md
```

## Заметки

- **CuteMessages** — единственный плагин с отдельным `.py` исходником; остальные хранятся как `.plugin` (валидный Python).
- У каждого плагина есть `secure.md` в корне папки (актуальная проверка) и `releases/v{version}/` — снимок `{name}_v{version}.plugin` и архивный отчёт `secure_{version}.md`. Отчёты генерируются **[Pluggy Bot](https://t.me/pluggy_robot)** (pluggy_robot.t.me).
- **CuteMessages/README.md** содержит также общую базу знаний по SDK exteraGram (хуки, entities, локализация).
- При извлечении `.plugin` → `.py` для других плагинов — обновить таблицу «Исходник» в этом файле.

## Полезные ссылки

| Ресурс | URL |
|--------|-----|
| SDK docs | https://plugins.exteragram.app/docs |
| Plugin class API | https://plugins.exteragram.app/docs/plugin-class |
| First plugin tutorial | https://plugins.exteragram.app/docs/first-plugin |
| KPM Store | https://github.com/KangelPlugins/Plugins-Store |
