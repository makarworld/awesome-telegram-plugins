# CuteMessages — техническая документация

> ID: `cutemessagesenhanced` · v1.8.0 · файл в репозитории: `cutemessagesenhanced.plugin`

Пользовательская документация: [README.md](README.md)

## Метаданные

| Поле | Значение |
|------|----------|
| `__id__` | `cutemessagesenhanced` |
| `__name__` | CuteMessages |
| `__version__` | 1.8.0 |
| `__author__` | @mihailkotovski & @mishabotov & idea - @bleizix (updated by @abuztrade & @AwesomeTelegramPlugins) |
| `__min_version__` | 11.9.0 |
| `__icon__` | ColorfulMessages/28 |

## Архитектура

| Компонент | Роль |
|-----------|------|
| `PicMePlugin` | Главный класс плагина |
| `LocalizationManager` | Локализация ru/en + override из настроек |

**Точка входа:** `on_send_message_hook` — трансформация текста/caption перед отправкой.

## Хуки

| Хук | Описание |
|-----|----------|
| `on_send_message_hook` | Трансформация исходящих сообщений, `effect_id`, premium emoji |
| `post_request_hook` | undo, авто-реакция после отправки |
| `on_update_hook` | `TL_updateNewMessage` — стоп-слово |
| `LaunchActivity.handleIntent` | deeplink импорт пресетов |
| `MESSAGE_CONTEXT_MENU` | «Омилить», «Отменить омиление» |
| `CHAT_ACTION_MENU` | Настройки, whitelist/blacklist, whitelist топиков |
| `DRAWER_MENU` | Настройки |

Приоритет хука: `-100` если `ignore_dot_commands=True` (раньше других плагинов).

## Поток обработки

```
on_send_message_hook
  ├─ .cute / .picme → toggle enabled → CANCEL
  ├─ enabled == False → skip
  ├─ _should_skip_text (emoji-only 1/3, /, .) → skip
  ├─ _should_apply_in_chat(peer, topic_id) → skip
  ├─ transform + premium emoji entities
  ├─ effect_id (auto_effect)
  ├─ queue auto reaction
  └─ HookStrategy.MODIFY
        ↓
post_request_hook
  ├─ _undo_cache[(dialog_id, msg_id)]
  └─ TL_messages_sendReaction (auto_reaction)
```

## Настройки

| Ключ | Описание |
|------|----------|
| `enabled` | Вкл/выкл эффекты |
| `message_language` | 0=авто, 1=ru, 2=en |
| `chat_filter_mode` | 0=все, 1=whitelist, 2=blacklist |
| `chat_whitelist` / `chat_blacklist` | JSON-массив peer ID |
| `topic_whitelist` | JSON `{"dialog_id": [topic_id, ...]}` |
| `stop_word_enabled` / `stop_word` | Стоп-слово входящих |
| `use_premium_emoji` | Custom emoji по `document_id`; на Desktop — unicode-fallback без установленных паков |
| `premium_emoji_frequency` | 10% / 25% / 50% / 75% / 100% — подмена unicode и составные блоки |
| `auto_effect_enabled` / `auto_effect` | Эффект отправки (личка 1-на-1; ID из `messages.availableEffects`) |
| `auto_reaction_enabled` / `auto_reaction_emoji` | Реакция после отправки |
| `include_lists_export` | Включать списки чатов в пресет |
| Эффекты | emoji, lowercase, uwu, stutter, vowel stretch, cute actions, punctuation, soft sign, text borders, themes |
| `custom_emojis` / `custom_kaomojis` / `custom_sparkles` | JSON-массивы строк; пустой = эффект группы выкл; нет ключа = дефолт |
| `custom_uwu_suffixes` / `custom_exclamations` / `custom_period_replacements` / `custom_question_replacements` | то же |
| `custom_theme_{pastel,magical,nature}_emojis` | кастомные эмодзи тем |
| `custom_text_borders` | JSON `[[left, right], ...]`; добавление в UI: `лево|право` |
| `custom_cute_actions_ru` / `custom_cute_actions_en` | списки действий |
| `include_custom_lists_export` | включать `custom_*` в пресет (по умолчанию нет) |

## Пресеты

Экспорт: `export_settings()` → JSON → base64url → `tg://cutemessages_import?data=...`

Импорт: deeplink hook или «Применить из буфера» → `import_settings()`.

Схема: `{"v": 1, "plugin": "cutemessagesenhanced", "settings": {...}}`

## Entities

При изменении длины текста offset/length entities пересчитываются сегментной трансформацией:

1. `_snapshot_entities` → копия в Python-dict
2. `_collect_protected_ranges` — Code/Pre, ссылки, custom emoji, @mention, телефоны + regex
3. Разбить текст по границам entities и protected spans
4. Трансформировать только незащищённые сегменты
5. `_inject_premium_emoji_entities` при включённом premium (`replace`, шанс из `premium_emoji_frequency`)
6. `_inject_theme_premium_blocks` / `_inject_mur_premium_bands` — составные блоки (тот же шанс; природа +15%, мур ×0.85). Сначала крупные (`block_line`, `grid`, 4+ emoji), иначе мелкий декор.
7. Пересчитать `new_offset` / `new_length` (UTF-16)
8. Отправка: `_apply_entities_to_params` → Java ArrayList; cutify/undo: `_build_java_entities_array` → `editMessage`

### CUSTOM_EMOJI

| Ключ | Когда |
|------|--------|
| `replace` | Подмена unicode → `MessageEntityCustomEmoji` |
| `decoration` | Случайный составной блок при любой теме |
| `mur` | Горизонтальная полоса adapemoji при UwU/мур-стиле |
| `nature` | Только `theme_selector=3`; широкие бордюры и сцены |
| `block_line` | Блок на отдельной строке |
| `layout` + `rows` | Сетка 2×2, 3×3 и т.д. |

Каталог подбора: `.tools/emoji-pack-semantic/plugin_premium_picks.json`, semantic — `output/<pack>/agent_catalog.md`.

## Undo и Cutify

Версии undo хранят `text`, `html` и `entities` (Java `MessageEntity` в dict). Редактирование — `SendMessagesHelper.editMessage(..., entities)` с UTF-16 offset/length; HTML — запасной путь.

## Защищённые фрагменты

- `MessageEntityUrl`, `MessageEntityTextUrl`, `MessageEntityCustomEmoji`, `Code`, `Pre`, mentions, phones, emails, bot commands
- URL: `http(s)://`, `ftp://`, `www.`, `t.me/`, `tg://`
- Сообщения из 1 или 3 эмодзи не трансформируются

## Команды

| Команда | Действие |
|---------|----------|
| `.picme` / `.cute` | Toggle enabled (CANCEL) |

## История

| Версия | Примечание |
|--------|------------|
| 1.8.0 | Подстраницы настроек, пресеты, premium emoji, топики, стоп-слово, авто fx/reaction; редактируемые кастомные списки (эмодзи/каомодзи/спарклы/темы/рамки/пунктуация/actions) |
| 1.7.1 | Cutify, стек undo, защита ссылок — [CHANGELOG](releases/v1.7.1/CHANGELOG.md) |
| 1.7.0 | Whitelist/blacklist, undo — [CHANGELOG](releases/v1.7.0/CHANGELOG.md) |

## Файлы

```
CuteMessages/
  cutemessagesenhanced.plugin
  README.md
  docs.md
  releases/v1.7.1/
```
