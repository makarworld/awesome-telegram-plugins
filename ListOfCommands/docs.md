# Меню доступных команд (`list_of_commands`)

> Автоподсказки dot-команд всех установленных плагинов при вводе `.` в чате.  
> Исходник: только `list_of_commands.plugin` · Версия: **1.0.8** · Обновлено: 2026-07-20

## Метаданные

| Поле | Значение |
|------|----------|
| `__id__` | `list_of_commands` |
| `__name__` | Меню доступных команд |
| `__version__` | 1.0.8 |
| `__author__` | @bandaliyev |
| `__description__` | Оптимизированное отображение команд |
| `__icon__` | pus_heen/12 |
| `__min_version__` | 11.12.0 |

## Файлы в папке

```
ListOfCommands/
  list_of_commands.plugin
  docs.md
  secure.md
  releases/
    v1.0.8/
      list_of_commands_v1.0.8.plugin
      secure_1.0.8.md
```

## Назначение

Сканирует папку плагинов, находит dot-команды (`.cmd`) в исходниках и показывает их в панели `MentionsAdapter` при вводе `.` в чате. Позволяет включать/отключать подсказки по командам.

## Архитектура

| Класс | Роль |
|-------|------|
| `CommandHelperPlugin` | Главный плагин |
| `CommandSuggestionsHook` | MethodHook на `MentionsAdapter.searchUsernameOrHashtag` |
| `PluginCommandHarvester` | Парсер команд из `.py`/`.plugin` |

## Хуки

| Хук | Описание |
|-----|----------|
| `MentionsAdapter.searchUsernameOrHashtag` (priority 10) | Подмена `searchResultCommands` / `searchResultCommandsHelp` |
| `on_send_message_hook` | `.preload` — сброс и пересборка кэша команд (CANCEL) |

## Настройки

| Ключ | Описание |
|------|----------|
| `cmd_enabled_{cmd}` | Switch для каждой найденной команды (динамически) |
| `custom_commands` | Свои команды: `.cmd:описание,.cmd2:описание` |

UI:
- Header «Активные подсказки»
- Switch per command с subtext «Плагин: {name}»
- Input для custom commands
- Подсказка: «Обновить вручную: `.preload`»

## Алгоритм `PluginCommandHarvester`

```
1. Сканировать папку plugins (*.py, *.plugin)
2. Regex __name__, __id__
3. Regex команд: '".xxx"' → .xxx
4. Кэш по mtime/size файлов + signature enabled plugins
5. Фильтр: только enabled plugins без ошибок
6. Prefix match по вводу пользователя
```

### Regex
- `__name__\s*=\s*['"]([^'"]+)['"]`
- `__id__\s*=\s*['"]([^'"]+)['"]`
- `['"](\.[a-zA-Z0-9_-]+)[\s'"]`

## Кэширование

| Поле | Описание |
|------|----------|
| `_command_cache` | `{ "items": [...] }` |
| `_dir_signature` | mtime/size файлов в папке |
| `_enabled_plugin_ids` | set ID включённых плагинов |
| `_enabled_signature` | сигнатура enabled-состояния |

Сброс: `.preload` или изменение файлов плагинов.

## UI / меню

Нет пунктов меню — работает через автоподсказки в поле ввода чата.

## Внешние зависимости

- Только SDK
- Читает локальную папку plugins (`.py`, `.plugin`)
- Сеть не используется

## Безопасность

| Риск | Уровень | Комментарий |
|------|---------|-------------|
| Чтение всех plugin-файлов | низкий | Только regex-парсинг, без exec |
| Ложные команды | низкий | Может найти строки, похожие на команды |

## Разработка

- Новая команда в плагине → автоматически появится после `.preload` или перезапуска.
- Команды из выключенных/ошибочных плагинов скрываются.
- При добавлении плагина с dot-командами — обновить этот docs и корневой docs.
