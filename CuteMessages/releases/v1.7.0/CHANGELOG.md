# CuteMessages — Changelog 1.6.1 → 1.7.0

**Дата релиза:** 2026-07-20  
**Плагин:** `cutemessagesenhanced` (CuteMessages)  
**Минимальная версия клиента:** 11.9.0 (без изменений)

---

## Авторы обновления 1.7.0

Эту ветку **1.7.x** разработал и довел до релиза:

**[@abuztrade](https://t.me/abuztrade)** & **[Awesome Telegram Plugins](https://t.me/AwesomeTelegramPlugins)** ([@AwesomeTelegramPlugins](https://t.me/AwesomeTelegramPlugins))

Оригинальный плагин и идея: @mihailkotovski, @mishabotov, @bleizix.

---

## Кратко

Версия **1.7.0** — крупное обновление поверх стабильной **1.6.1**. Плагин по-прежнему делает исходящие сообщения «милыми», но теперь умеет работать выборочно по чатам, сохранять форматирование Telegram, откатывать последние отправки и не мешать бот-командам.

Объём кода вырос примерно с **~710** до **~2000+** строк.

---

## ✨ Добавлено

### Фильтр чатов (whitelist / blacklist)

- Настройка **«Режим фильтра чатов»**: все чаты / только белый список / все кроме чёрного списка.
- Отдельные списки `chat_whitelist` и `chat_blacklist` (JSON в настройках плагина).
- **Динамический список чатов в настройках** — имена пользователей и групп, кнопка «Убрать» для каждого чата.
- Пункт в меню чата **⋯** с динамическим текстом:
  - «Cute: добавить в белый список» / «удалить из белого списка»
  - «Cute: добавить в чёрный список» / «удалить из чёрного списка»
- Иконки: `msg_favorite` (белый список), `msg_block` (чёрный список).
- Автообновление текста кнопки при смене чата (`ChatActivity.onTransitionAnimationEnd`).
- Мгновенное обновление списка в настройках при добавлении/удалении чата.

### Undo — «вернуть оригинал»

- Пункт **MESSAGE_CONTEXT_MENU** (долгий тап на своё сообщение): «Cute: вернуть оригинал».
- Сохранение оригинального текста и HTML-версии с entities **до** трансформации.
- Привязка к `(dialog_id, msg_id)` через `post_request_hook` после отправки.
- Лимит: **5 последних** изменённых сообщений.
- Восстановление через `edit_message` с поддержкой HTML-форматирования.
- Хуки отправки: `TL_messages_sendMessage`, `TL_messages_sendMedia`, `TL_messages_sendMultiMedia`.

### Сохранение форматирования (entities)

- Сегментная трансформация текста с пересчётом `offset` / `length` entities.
- Поддержка **bold**, *italic*, `code`, ссылок и других типов форматирования Telegram.
- Корректная работа с **подписями к медиа** (`caption` + `captionEntities`).
- Итерация Java `ArrayList` через `_iter_java()` (безопасный обход коллекций Chaquopy).

### Команды и совместимость

- Команда **`.cute`** — toggle включения/выключения (аналог `.picme`).
- Настройка **«Игнорировать команды ботов (/)»** — не трогать `/start`, `/help` и т.п.
- Единая логика пропуска текста: `_should_skip_text()` для dot- и slash-команд.

### UI и локализация

- Двуязычное описание плагина в метаданных (EN + RU).
- Иконка настроек в меню: `menu_premium_effects` (drawer + меню чата ⋯).
- Bulletin-уведомления при добавлении/удалении чата из списка.
- Расширенные строки локализации ru/en для фильтра, списков и undo (~30 новых ключей).

### Надёжность

- Расширенная обработка ошибок: `MODIFY_FINAL` + debug-суффикс с типом исключения и местом в коде.
- Нормализация `dialog_id` через `DialogObject.getPeerDialogId()`.
- Чтение контекста меню из Java `Map` (`_ctx_get()`), не только Python `dict`.
- Обновление UI через `run_on_ui_thread` для меню и bulletin.

---

## 🔄 Изменено

| Область | Было (1.6.1) | Стало (1.7.0) |
|---------|--------------|---------------|
| Трансформация текста | Только plain text, entities терялись | Сегментная обработка с сохранением entities |
| Медиа | Только `params.message` | `message` и `caption` с отдельными entities |
| Команда toggle | Только `.picme` | `.picme` и `.cute` |
| Пропуск команд | Только dot (`.`) | Dot + slash (`/`) |
| Меню чата | Только «Настройки» | Настройки + управление списком чатов |
| Иконка настроек | `msg_settings_14` | `menu_premium_effects` |
| Автор в метаданных | @mihailkotovski & @mishabotov & @bleizix | + `(updated by @AwesomeTelegramPlugins)` |
| `on_plugin_load` | Только send hook | Send hook + protocol hooks + меню undo/списка |
| Хранение списков чатов | — | JSON-массивы peer ID в настройках |

---

## 🔧 Технические детали

### Новые зависимости SDK

```python
from hook_utils import find_class
from client_utils import edit_message
from org.telegram.messenger import DialogObject, UserObject, ChatObject
from base_plugin import AppEvent, MethodHook
```

### Архитектура undo

```
on_send_message_hook
  → сохранить оригинал + HTML в _pending_undo (FIFO-очередь)
  → MODIFY params

post_request_hook (sendMessage / sendMedia / sendMultiMedia)
  → извлечь msg_id из TL_updateMessageID / TL_updateNewMessage
  → _undo_cache[(dialog_id, msg_id)] = record (лимит 5)

MESSAGE_CONTEXT_MENU → «вернуть оригинал»
  → _find_undo_record() → edit_message()
```

### Архитектура фильтра чатов

```
chat_filter_mode: 0 = все | 1 = whitelist | 2 = blacklist
_should_apply_in_chat(peer) → skip/modify в on_send_message_hook
CHAT_ACTION_MENU → _toggle_chat_in_list()
create_settings() → _build_chat_filter_settings() (динамический список)
```

---

## 📦 Файлы релиза

```
CuteMessages/releases/v1.7.0/
  cutemessagesenhanced_v1.7.0.plugin
  secure_1.7.0.md
  CHANGELOG.md          ← этот файл
```

---

## ✅ Безопасность

По отчёту Pluggy Bot ([secure_1.7.0.md](./secure_1.7.0.md)): **безопасно**.

- Локальная обработка текста, без передачи сообщений на сторонние серверы.
- Сеть: только ссылка доната в настройках (`t.me`).
- Undo работает только с собственными последними сообщениями пользователя.

---

## ⬆️ Миграция с 1.6.1

- Настройки эффектов (UwU, рамки, темы и т.д.) **сохраняются** — ключи не менялись.
- Новые настройки по умолчанию:
  - `chat_filter_mode` = 0 (все чаты)
  - `ignore_slash_commands` = true
  - `chat_whitelist` / `chat_blacklist` = `[]`
- После обновления рекомендуется один раз открыть настройки плагина и при необходимости выбрать режим фильтра.

---

## 🙏 Благодарности

- **@mihailkotovski**, **@mishabotov**, **@bleizix** — оригинальный CuteMessages и идея.
- **@abuztrade** & **@AwesomeTelegramPlugins** — разработка и выпуск обновления **1.6.1 → 1.7.0**.
- Сообщество exteraGram / AyuGram за тестирование и обратную связь.
