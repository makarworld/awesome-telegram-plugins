# Kangel Plugins Manager (`kangel_plugins_manager`)

> Магазин и менеджер плагинов для exteraGram / AyuGram.  
> Исходник: только `kangel_plugins_manager.plugin` · Версия: **1.3.2** · Обновлено: 2026-07-20

## Метаданные

| Поле | Значение |
|------|----------|
| `__id__` | `kangel_plugins_manager` |
| `__name__` | Kangel Plugins Manager |
| `__version__` | 1.3.2 |
| `__author__` | @ArThirtyFour \| @KangelPlugins |
| `__description__` | Первый магазин плагинов с удобным управлением. Требует exteraGram/AyuGram 12.1.1+ |
| `__icon__` | Kangelcons_by_fStikBot/5 |
| `__min_version__` | 12.1.1 |

## Скачать

[Скачать kangel_plugins_manager.plugin](https://raw.githubusercontent.com/makarworld/awesome-telegram-plugins/refs/heads/main/KangelPluginsManager/kangel_plugins_manager.plugin)

Установка: скачай файл → открой в exteraGram / AyuGram (или импортируй через менеджер плагинов).

## Файлы в папке

```
KangelPluginsManager/
  kangel_plugins_manager.plugin   # рабочая копия (~5757 строк)
  README.md
  secure.md
  releases/
    v1.3.2/
      kangel_plugins_manager_v1.3.2.plugin
      secure_1.3.2.md
```

> Исходника `.py` нет — только `.plugin` (валидный Python).

## Назначение

Полноценный магазин плагинов: каталог из GitHub, установка/обновление `.plugin`, inline-поиск в чате, pill-виджет со счётчиком, builds (наборы плагинов), deeplink-установка, телеметрия mkStats.

## Архитектура

| Класс | Роль |
|-------|------|
| `KangelPluginsManager` | Главный плагин (`BasePlugin`) |
| `MkStatsCoreClient` | Клиент телеметрии mkStats (PoW handshake) |
| `KPMSettingsHeaderHook` | Хук заголовка `PluginSettingsActivity` |

## Хуки

### Жизненный цикл
- **`on_plugin_load`**: mkStats, send hook, deeplink (`LaunchActivity.handleIntent`), drawer menu, install/update UI, `PluginsActivity`, settings header, PillStack, inline search.
- **`on_plugin_unload`**: остановка mkStats, снятие хуков.

### Сообщения
- **`on_send_message_hook`**: команды `.kpm_send local|...` / `remote|...` — установка или отправка плагина через чат.

### Method hooks (основные)
- `InstallPluginBottomSheet` — диалог установки, guard версий
- `PluginCell.set` — bubbles, сортировка, фильтры статуса
- `MentionsAdapter.searchForContextBot` / `searchUsernameOrHashtag` — inline-поиск `@kpm`
- `PluginSettingsActivity.fillItems` — кастомный header
- PillStack interactions

## Настройки

Главное меню разбито на подразделы:

### Управление плагинами
- Обновить список, установить, обновить установленные, очистить кэш

### Автообновления
| Ключ | По умолчанию | Описание |
|------|--------------|----------|
| `auto_update_on_start` | false | Обновлять каталог при старте |
| `auto_update_installed` | false | Обновлять установленные плагины |

### UI
| Ключ | По умолчанию | Описание |
|------|--------------|----------|
| `show_drawer_menu` | true | Пункт в боковом меню |
| `show_plugin_bubbles` | true | Пузырьки на ячейках плагинов |
| `show_add_button` | true | Кнопка «Добавить» в PluginsActivity |
| `show_update_button` | true | Кнопка «Обновить» |
| `inline_search_enabled` | — | Inline-поиск в чате |
| `inline_search_trigger` | `kpm` | Триггер `@kpm` |
| `pill_enabled` | true | Pill-виджет со счётчиком |
| `pill_click_action` | 0 | Действие по клику на pill |

### Прочее
| Ключ | По умолчанию | Описание |
|------|--------------|----------|
| `telemetry_enabled` | true | Телеметрия mkStats |
| `logs_enabled` | true | Подробные логи |
| `enforce_version_requirements` | true | Блокировать плагины ниже `__min_version__` |

### Скрытые (runtime)
- `mkstats_device_id`, `mkstats_install_token`
- `plugins_sort_mode`, `plugins_status_filter`

## UI / меню

| Элемент | Описание |
|---------|----------|
| **DRAWER_MENU** | «Plugin Manager» |
| **PillStack** | ID `34012501`, тег `kpm_pill` — счётчик плагинов |
| Bottom sheets | Установка, обновление, поиск, builds, about |
| Inline search | `@kpm` / `@trigger` → fake bot results |
| Deeplinks | `tg://kpm_install?plugin=...`, `tg://kpm_list` |

## Внешние зависимости

| Тип | URL / ресурс |
|-----|--------------|
| Каталог | `https://raw.githubusercontent.com/KangelPlugins/Plugins-Store/.../store.json` |
| GitHub API | `https://api.github.com/repos/KangelPlugins/Plugins-Store/commits/main` |
| Телеметрия | `https://mkstats.mk69.su/api` (override: `MKSTATS_API_URL`) |
| Telegram | @KangelPlugins, @KangelPluginsManager, @KPMAppealBot |
| GitHub | https://github.com/KangelPlugins/Plugins-Store |

Библиотеки: `requests`, `urllib.request`.

## Алгоритмы

1. **Каталог:** загрузка `store.json` → кэш `.kpm_cache.json` → сравнение версий с локальными.
2. **Установка:** скачивание `.plugin` → проверка `__min_version__` → установка через SDK.
3. **Inline search:** локальные + remote плагины → подмена `foundContextBot` → `.kpm_send`.
4. **mkStats:** SHA256 device fingerprint, PoW challenge, ping/event.
5. **Поиск:** trigram index по каталогу.
6. **Builds:** сохранение/загрузка наборов плагинов.

## Хранение данных

| Файл / ключ | Содержимое |
|-------------|------------|
| `{PLUGINS_DIR}/.kpm_cache.json` | Кэш каталога |
| Plugin settings | Все ключи настроек |
| `_sticker_cache` | Runtime-кэш стикеров |

Константы: `KPM_PILL_ID = 34012501`, `PLUGINS_DIR = get_plugins_dir()`.

## Безопасность

| Риск | Уровень | Комментарий |
|------|---------|-------------|
| Установка плагинов из интернета | **высокий** | Основная функция магазина |
| Телеметрия mkStats | средний | Отключается `telemetry_enabled` |
| Inline fake bot | средний | Подмена результатов поиска |
| Version guard | снижает риск | `enforce_version_requirements` |

PoW защищает API mkStats, но **не** защищает от вредоносных плагинов в каталоге.

## Разработка

- Для правок нужно извлечь `.plugin` → `.py` или работать напрямую с `.plugin` (это валидный Python).
- Локализация: `_tr()` — ru/en строки в начале файла.
- При добавлении фич обновлять этот `README.md` и корневой `docs.md`.
