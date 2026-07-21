# Kangel Plugins Manager — техническая документация

> ID: `kangel_plugins_manager` · v1.4.3 · исходник: `kangel_plugins_manager.plugin`

Пользовательская документация: [README.md](README.md)

## Метаданные

| Поле | Значение |
|------|----------|
| `__id__` | `kangel_plugins_manager` |
| `__version__` | 1.4.3 |
| `__author__` | @ArThirtyFour \| @KangelPlugins |
| `__min_version__` | 12.5.1 |
| `__requirements__` | `kangelpluginsmanager==1.4.3` |

## Архитектура (v1.4.3+)

С v1.4.3 плагин — **тонкая обёртка** (~25 строк логики). Вся реализация вынесена в PyPI-пакет.

```
kangel_plugins_manager.plugin          PyPI: kangelpluginsmanager
┌─────────────────────────┐            ┌────────────────────────────────┐
│ class KPM(              │  import    │ KangelPluginsManagerPlugin     │
│   _KPMImpl, BasePlugin) │ ─────────► │ plugin.py (~300 KB)            │
│ pass                    │            │ methods.py, sbroka.py          │
└─────────────────────────┘            │ assests/locale.json, bages.json│
                                       └────────────────────────────────┘
```

| Компонент | Роль |
|-----------|------|
| `KPM` (`.plugin`) | Точка входа exteraGram: метаданные + наследование `BasePlugin` |
| `KangelPluginsManagerPlugin` (PyPI) | Вся логика магазина, UI, хуки, mkStats |
| `methods.py` | Вспомогательные method hooks |
| `sbroka.py` | Утилиты (поиск, индексация) |
| `assests/locale.json` | Локализация ru/en |
| `assests/bages.json` | Бейджи плагинов |

Исходники библиотеки: [github.com/KangelPlugins/PluginManager](https://github.com/KangelPlugins/PluginManager)

## PyPI-пакет `kangelpluginsmanager`

| Поле | Значение |
|------|----------|
| PyPI | [pypi.org/project/KangelPluginsManager](https://pypi.org/project/KangelPluginsManager/) |
| Пин в плагине | `==1.4.3` |
| Актуальная на PyPI | 1.4.3.4 (2026-07-20) |
| Зависимости | `requests>=2.31.0` |
| Python | `>=3.9` |
| Лицензия | MIT |
| Автор | ArThirtyFour |

При анализе безопасности **обязательно** смотреть не только `.plugin`, но и wheel `kangelpluginsmanager` — там весь исполняемый код.

Установка пакета клиентом: через `__requirements__` при загрузке плагина (exteraGram pip).

## Хуки

Логика в `kangelpluginsmanager.plugin.KangelPluginsManagerPlugin` (ранее монолит в `.plugin` до v1.3.2).

### Жизненный цикл
- `on_plugin_load`: mkStats, send hook, deeplink, drawer, install UI, PillStack, inline search
- `on_plugin_unload`: остановка mkStats

### Сообщения
- `on_send_message_hook`: `.kpm_send local|...` / `remote|...`

### Method hooks
- `InstallPluginBottomSheet`, `PluginCell.set`
- `MentionsAdapter.searchForContextBot` / `searchUsernameOrHashtag` — `@kpm`
- `PluginSettingsActivity.fillItems`, PillStack

## Настройки

| Ключ | Default | Описание |
|------|---------|----------|
| `auto_update_on_start` | false | Обновить каталог при старте |
| `auto_update_installed` | false | Обновить установленные |
| `show_drawer_menu` | true | Пункт в drawer |
| `show_plugin_bubbles` | true | Пузырьки на ячейках |
| `telemetry_enabled` | true | mkStats |
| `enforce_version_requirements` | true | Блок `__min_version__` |
| `inline_search_trigger` | `kpm` | Триггер inline |
| `pill_enabled` | true | Pill-виджет |

Скрытые: `mkstats_device_id`, `plugins_sort_mode`, `plugins_status_filter`.

## UI

| Элемент | Описание |
|---------|----------|
| DRAWER_MENU | «Plugin Manager» |
| PillStack | ID `34012501`, счётчик плагинов |
| Deeplinks | `tg://kpm_install?plugin=...`, `tg://kpm_list` |
| Inline | `@kpm` → fake bot results |

## Внешние зависимости

| URL / пакет | Назначение |
|-------------|------------|
| PyPI `kangelpluginsmanager` | Основная логика плагина |
| `raw.githubusercontent.com/KangelPlugins/Plugins-Store/.../store.json` | Каталог |
| `api.github.com/repos/KangelPlugins/Plugins-Store/commits/main` | Версия каталога |
| `mkstats.mk69.su/api` | Телеметрия |

## Алгоритмы

1. Каталог: `store.json` → `.kpm_cache.json` → сравнение версий
2. Установка: download `.plugin` → `__min_version__` → SDK install
3. Inline: подмена `foundContextBot` → `.kpm_send`
4. mkStats: SHA256 fingerprint, PoW, ping/event
5. Поиск: trigram index

## Хранение

| Файл | Содержимое |
|------|------------|
| `{PLUGINS_DIR}/.kpm_cache.json` | Кэш каталога |
| Plugin settings | Все ключи |

## Релизы

| Версия | Файл | Особенности |
|--------|------|-------------|
| 1.4.3 | [releases/v1.4.3/](releases/v1.4.3/) | Обёртка + PyPI `kangelpluginsmanager==1.4.3`, min 12.5.1 |
| 1.3.2 | [releases/v1.3.2/](releases/v1.3.2/) | Монолитный `.plugin` (~5757 строк), min 12.1.1 |

## Разработка

- В репозитории только `.plugin` (валидный Python)
- Локально опционально `.py` → `build_plugin.bat`
- Логика — в [PluginManager](https://github.com/KangelPlugins/PluginManager), публикация на PyPI
- PoW защищает mkStats API, не каталог
