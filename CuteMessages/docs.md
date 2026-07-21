# CuteMessages — техническая документация

> ID: `cutemessagesenhanced` · v1.7.3 · файл в репозитории: `cutemessagesenhanced.plugin`

Пользовательская документация: [README.md](README.md)

## Метаданные

| Поле | Значение |
|------|----------|
| `__id__` | `cutemessagesenhanced` |
| `__name__` | CuteMessages |
| `__version__` | 1.7.3 |
| `__author__` | @mihailkotovski & @mishabotov & idea - @bleizix (updated by @abuztrade & @AwesomeTelegramPlugins) |
| `__min_version__` | 11.9.0 |
| `__icon__` | ColorfulMessages/28 |

## Архитектура

| Компонент | Роль |
|-----------|------|
| `PicMePlugin` | Главный класс плагина |
| `LocalizationManager` | Локализация ru/en |

**Точка входа:** `on_send_message_hook` — трансформация текста/caption перед отправкой.

## Хуки

| Хук | Описание |
|-----|----------|
| `on_send_message_hook` | Трансформация исходящих сообщений |
| `post_request_hook` | `TL_messages_sendMessage` / sendMedia / sendMultiMedia — привязка undo к msg_id |
| `MESSAGE_CONTEXT_MENU` | «Омилить ✨», «Отменить омиление 😢» |
| `CHAT_ACTION_MENU` | Настройки, whitelist/blacklist |
| `DRAWER_MENU` | Настройки |

Приоритет хука: `-100` если `ignore_dot_commands=True` (раньше других плагинов).

## Поток обработки

```
on_send_message_hook
  ├─ .cute / .picme → toggle enabled → CANCEL
  ├─ enabled == False → skip
  ├─ _should_skip_text → skip
  ├─ _should_apply_in_chat(peer) → skip
  ├─ _snapshot_entities → _transform_with_entities → _apply_entities_to_params
  ├─ _pending_undo[(dialog_id,)] = {versions[], index, ts}
  └─ HookStrategy.MODIFY
        ↓
post_request_hook
  └─ _undo_cache[(dialog_id, msg_id)] = record (лимит 5)
```

## Настройки

| Ключ | Описание |
|------|----------|
| `enabled` | Вкл/выкл эффекты |
| `chat_filter_mode` | 0=все, 1=whitelist, 2=blacklist |
| `chat_whitelist` / `chat_blacklist` | JSON-массив peer ID |
| `ignore_slash_commands` | Пропуск `/start`, `/help` |
| `ignore_dot_commands` | Пропуск `.cmd` |
| `show_settings_buttons` | Кнопки в меню |
| Эффекты | emoji, lowercase, uwu, stutter, vowel stretch, cute actions, punctuation, soft sign, text borders, themes |

## Entities

При изменении длины текста offset/length entities пересчитываются сегментной трансформацией:

1. `_snapshot_entities` → копия в Python-dict
2. `_collect_protected_ranges` — Code/Pre, ссылки, @mention, телефоны + regex для plain-текста
3. Разбить текст по границам entities и protected spans
4. Трансформировать только незащищённые сегменты
5. Пересчитать `new_offset` / `new_length`
6. `_apply_entities_to_params` → Java ArrayList

Нормализация: `TL_messageEntityBold` → `MessageEntityBold`.

## Undo и Cutify

1. Перед отправкой: стек версий `[оригинал, милое, …]` в `_pending_undo`
2. После отправки: `_undo_cache[(dialog_id, msg_id)]`, лимит **4096×4 символов** суммарно по всем версиям всех сообщений
3. Сообщения не режутся — при переполнении удаляется целиком самое старое по времени
4. **Отменить омиление 😢** — шаг назад по стеку; на оригинале цикл **оригинал ↔ первое милое**
5. **Cutify ✨** — новая версия в стек (повторные нажатия накапливают историю)
6. Контекст меню — Java `Map`: `_ctx_get()`, `_message_id_from_obj()`
7. При ошибке HTML: повтор `parse_mode="html"`, затем plain

Структура записи undo:

```python
{
    "versions": [{"text": "...", "html": "..."}, ...],
    "index": 1,  # текущая позиция в стеке
    "ts": float,
}
```

## Защищённые фрагменты

Не трансформируются (entity + regex в plain-тексте):

- `MessageEntityUrl`, `MessageEntityTextUrl`, `MessageEntityMention`, `MessageEntityMentionName`, `MessageEntityPhone`, `MessageEntityEmail`, `MessageEntityBotCommand`, `Code`, `Pre`
- URL: `http(s)://`, `www.`, `t.me/`, `tg://`
- `@username`, `tg://user?id=…`, телефоны `+…`

## Команды

| Команда | Действие |
|---------|----------|
| `.picme` / `.cute` | Toggle enabled (CANCEL) |

## Подводные камни

| Проблема | Решение |
|----------|---------|
| `ArrayList$Itr` not iterable | `_iter_java()` |
| Entities съезжают | Сегментная трансформация |
| `peer` может быть `None` | Fallback `0` |

## Отказавшиеся подходы

- Long-press на Send через `MethodHook` — хрупко, удалено
- `send_mode` selector — удалён
- Undo с ключом `(account, dialog_id, msg_id)` — упрощено до `(peer, msg_id)`

## История

| Версия | Примечание |
|--------|------------|
| 1.7.3 | Лимит кэша по символам (16 КБ), стек версий Cutify/Undo |
| 1.7.2 | Undo-toggle, Cutify, защита ссылок/@/телефонов |
| 1.7.1 | |
| 1.7.0 | Whitelist/blacklist, undo, `.cute`/`.picme` — [CHANGELOG](releases/v1.7.0/CHANGELOG.md) |

## Файлы

```
CuteMessages/
  cutemessagesenhanced.plugin   # код плагина (Python), в репозиторий заливается только .plugin
  README.md
  docs.md
  releases/v1.7.0/
```

Локально для правок можно держать `.py` и собирать через `build_plugin.bat` — в git не коммитится.
