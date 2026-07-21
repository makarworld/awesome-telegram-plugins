# Kangel Plugins Manager — техническая документация

> ID: `kangel_plugins_manager` · v1.3.2 · исходник: `kangel_plugins_manager.plugin`

Пользовательская документация: [README.md](README.md)

## Метаданные

| Поле | Значение |
|------|----------|
| `__id__` | `kangel_plugins_manager` |
| `__version__` | 1.3.2 |
| `__author__` | @ArThirtyFour \| @KangelPlugins |
| `__min_version__` | 12.1.1 |

## Архитектура

| Класс | Роль |
|-------|------|
| `KangelPluginsManager` | Главный плагин |
| `MkStatsCoreClient` | Телеметрия mkStats (PoW) |
| `KPMSettingsHeaderHook` | Хук заголовка настроек |

## Хуки

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

| URL | Назначение |
|-----|------------|
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

## Разработка

- В репозитории только `.plugin` (валидный Python)
- Локально опционально `.py` → `build_plugin.bat`
- Локализация: `_tr()` ru/en
- PoW защищает mkStats API, не каталог
