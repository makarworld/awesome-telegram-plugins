# Unlimited Pins — техническая документация

> ID: `misha_unlimited_pins` · v2.0 · исходник: `misha_unlimited_pins.plugin`

Пользовательская документация: [README.md](README.md)

## Метаданные

| Поле | Значение |
|------|----------|
| `__id__` | `misha_unlimited_pins` |
| `__version__` | 2.0 |
| `__author__` | @mihailkotovski & @mishabotov |

## Архитектура

Единственный класс `UnlimitedPins` — подмена лимитов `MessagesController`, персистентное состояние закрепов.

## Хуки

### Method hooks
- `MessagesController.pinDialog`
- `MessagesController.reorderPinnedDialogs`
- `MessagesController.applyAppConfig`
- `MessagesController.onFilterUpdate`
- `MessagesStorage.unpinAllDialogsExceptNew`
- `FilterCreateActivity.saveFilterToServer`

### Protocol hooks
- `TL_updatePinnedDialogs`, `TL_updateDialogPinned`
- `TL_messages_getPinnedDialogs`, `TL_messages_toggleDialogPin`
- `TL_messages_reorderPinnedDialogs`, `TL_help_getAppConfig`

### Другие
- `pre_request_hook` / `post_request_hook` / `on_update_hook`
- `on_app_event` — START/RESUME → reapply limits + restore

## Настройки (ключи)

| Ключ | Default | Описание |
|------|---------|----------|
| `max_value` | 100000 | Новый лимит закрепов |
| `persist_pins` | true | Сохранять в JSON |
| `restore_pins_on_start` | true | Восстановление при старте |
| `restore_on_unload` | true | Вернуть лимиты при выгрузке |
| `block_server_updates` | false | Откатывать серверные pin-updates |

## Подменяемые поля

`LIMIT_FIELDS` — 6 полей в `MessagesController` (включая `maxPinnedDialogsCountDefault`), заменяются на `max_value` (max 2147483647).

## Алгоритм

1. Загрузка: сохранить оригинальные лимиты → подменить → хуки
2. pin/unpin: перехват → JSON (debounce)
3. Server sync: `_merge_saved_pins_into_server_list`
4. Восстановление: до 20 попыток, max 300 pins на папку
5. Выгрузка: state → снять хуки → оригинальные лимиты

## Хранение

| Файл | Путь |
|------|------|
| `unlimited_pins_state.json` | `{plugins_dir}/cache/unlimited_pins_state.json` |
| Схема | `PINS_STATE_VERSION = 3` |

## Константы

```python
DEFAULT_MAX = 100000
MAX_RESTORED_PINS_PER_FOLDER = 300
RESTORE_MAX_ATTEMPTS = 20
```

## Разработка

- Тестировать на нескольких аккаунтах и папках (folders/filters)
- При смене схемы — инкремент `PINS_STATE_VERSION`
- `block_server_updates=True` — агрессивный режим, может ломать синхронизацию
