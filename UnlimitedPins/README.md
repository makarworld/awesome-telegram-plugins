# Unlimited Pins (`misha_unlimited_pins`)

> Снимает лимит на количество закреплённых чатов.  
> Исходник: только `misha_unlimited_pins.plugin` · Версия: **2.0** · Обновлено: 2026-07-20

## Метаданные

| Поле | Значение |
|------|----------|
| `__id__` | `misha_unlimited_pins` |
| `__name__` | Unlimited Pins |
| `__version__` | 2.0 |
| `__author__` | @mihailkotovski & @mishabotov |
| `__description__` | позволяет закреплять больше чатов, чем обычно |
| `__icon__` | EmojiAnimations/12 |
| `__min_version__` | не указан |

## Скачать

[Скачать misha_unlimited_pins.plugin](https://raw.githubusercontent.com/makarworld/awesome-telegram-plugins/refs/heads/main/UnlimitedPins/misha_unlimited_pins.plugin)

Установка: скачай файл → открой в exteraGram / AyuGram (или импортируй через менеджер плагинов).

## Файлы в папке

```
UnlimitedPins/
  misha_unlimited_pins.plugin
  README.md
  releases/
    v2.0/
      misha_unlimited_pins_v2.0.plugin
      secure_2.0.md
```

## Назначение

Подменяет внутренние лимиты `MessagesController` и сохраняет/восстанавливает состояние закрепов при перезапуске, синхронизации с сервером и выгрузке плагина.

## Архитектура

| Класс | Роль |
|-------|------|
| `UnlimitedPins` | Единственный класс плагина |

## Хуки

### Method hooks
- `MessagesController.pinDialog`
- `MessagesController.reorderPinnedDialogs`
- `MessagesController.applyAppConfig`
- `MessagesController.onFilterUpdate`
- `MessagesStorage.unpinAllDialogsExceptNew`
- `FilterCreateActivity.saveFilterToServer`

### Protocol hooks
- `TL_updatePinnedDialogs`
- `TL_updateDialogPinned`
- `TL_messages_getPinnedDialogs`
- `TL_messages_toggleDialogPin`
- `TL_messages_reorderPinnedDialogs`
- `TL_help_getAppConfig`

### Другие
- **`pre_request_hook` / `post_request_hook` / `on_update_hook`** — сохранение и восстановление закрепов
- **`on_app_event`** — `START` / `RESUME` → reapply limits + restore

## Настройки

### UI
| Элемент | Описание |
|---------|----------|
| Кнопка «вернуть закрепы» | Принудительное восстановление из сохранённого состояния |

### Скрытые ключи (в коде, не в UI)
| Ключ | Default | Описание |
|------|---------|----------|
| `max_value` | 100000 | Новый лимит закрепов |
| `persist_pins` | true | Сохранять состояние в JSON |
| `restore_pins_on_start` | true | Восстанавливать при старте |
| `restore_on_unload` | true | Вернуть оригинальные лимиты при выгрузке |
| `block_server_updates` | false | Откатывать серверные pin-updates |

## Подменяемые поля лимитов

`LIMIT_FIELDS` — 6 полей в `MessagesController`:
- `maxPinnedDialogsCountDefault`
- и связанные поля лимитов (см. исходник, строки 29–36)

Все заменяются на `max_value` (max 2147483647).

## Алгоритмы

1. **При загрузке:** сохранить оригинальные лимиты → подменить на `max_value` → зарегистрировать хуки.
2. **При pin/unpin:** перехватить → сохранить состояние в JSON (debounce).
3. **При server sync:** `_merge_saved_pins_into_server_list` — слияние локальных и серверных.
4. **Восстановление:** до 20 попыток (`RESTORE_MAX_ATTEMPTS`), max 300 pins на папку (`MAX_RESTORED_PINS_PER_FOLDER`).
5. **При выгрузке:** сохранить state → снять хуки → вернуть оригинальные лимиты.

## Хранение данных

| Файл | Путь |
|------|------|
| `unlimited_pins_state.json` | `{plugins_dir}/cache/unlimited_pins_state.json` |
| Версия схемы | `PINS_STATE_VERSION = 3` |

Структура: `{ "accounts": {...}, "filters": {...} }`.

Runtime: `_original_limits`, `_restore_attempts`, `_restored_folders`, `_restored_filters`.

## Константы

```python
DEFAULT_MAX = 100000
MAX_INT = 2147483647
MAX_RESTORED_PINS_PER_FOLDER = 300
RESTORE_MAX_ATTEMPTS = 20
PINS_STATE_FILE = "unlimited_pins_state.json"
```

## Безопасность

| Риск | Уровень | Комментарий |
|------|---------|-------------|
| Манипуляция pinned dialogs | низкий | Ожидаемое поведение |
| Конфликт с сервером | средний | Сервер может откатывать лишние закрепы |
| Утечка данных | низкий | Только локальный JSON |

Сеть не используется.

## Разработка

- Тестировать на нескольких аккаунтах и папках (folders/filters).
- При изменении схемы state — инкрементировать `PINS_STATE_VERSION`.
- `block_server_updates=True` — агрессивный режим, может ломать синхронизацию.
