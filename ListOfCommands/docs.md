# List of Commands — техническая документация

> ID: `list_of_commands` · v1.0.8 · исходник: `list_of_commands.plugin`

Пользовательская документация: [README.md](README.md)

## Метаданные

| Поле | Значение |
|------|----------|
| `__id__` | `list_of_commands` |
| `__version__` | 1.0.8 |
| `__author__` | @bandaliyev |
| `__min_version__` | 11.12.0 |

## Архитектура

| Класс | Роль |
|-------|------|
| `CommandHelperPlugin` | Главный плагин |
| `CommandSuggestionsHook` | Hook на `MentionsAdapter.searchUsernameOrHashtag` |
| `PluginCommandHarvester` | Парсер команд |

## Хуки

| Хук | Описание |
|-----|----------|
| `MentionsAdapter.searchUsernameOrHashtag` (priority 10) | Подмена `searchResultCommands` |
| `on_send_message_hook` | `.preload` — сброс кэша (CANCEL) |

## Настройки

| Ключ | Описание |
|------|----------|
| `cmd_enabled_{cmd}` | Switch per command (динамически) |
| `custom_commands` | `.cmd:описание,.cmd2:описание` |

## Алгоритм `PluginCommandHarvester`

```
1. Сканировать plugins (*.py, *.plugin)
2. Regex __name__, __id__
3. Regex команд: '".xxx"' → .xxx
4. Кэш по mtime/size + signature enabled plugins
5. Только enabled без ошибок
6. Prefix match по вводу
```

### Regex
- `__name__\s*=\s*['"]([^'"]+)['"]`
- `__id__\s*=\s*['"]([^'"]+)['"]`
- `['"](\.[a-zA-Z0-9_-]+)[\s'"]`

## Кэширование

| Поле | Описание |
|------|----------|
| `_command_cache` | `{ "items": [...] }` |
| `_dir_signature` | mtime/size файлов |
| `_enabled_plugin_ids` | set ID включённых |

Сброс: `.preload` или изменение файлов.

## Разработка

- Новая команда → `.preload` или перезапуск
- Команды выключенных плагинов скрываются
- Сеть не используется
