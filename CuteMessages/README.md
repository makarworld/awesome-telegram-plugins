# CuteMessages (`cutemessagesenhanced`)

> Плагин: стилизация исходящих сообщений (cute-эффекты, UwU, рамки, undo).  
> Исходник: `cutemessagesenhanced.py` · Версия: **1.7.0** · Обновлено: 2026-07-20

## Метаданные

| Поле | Значение |
|------|----------|
| `__id__` | `cutemessagesenhanced` |
| `__name__` | CuteMessages |
| `__version__` | 1.7.0 |
| `__author__` | @mihailkotovski & @mishabotov & idea - @bleizix (updated by @abuztrade & @AwesomeTelegramPlugins) |
| `__description__` | Makes your messages extra cute with many adorable styles! |
| `__icon__` | ColorfulMessages/28 |
| `__min_version__` | 11.9.0 |

## Скачать

[Скачать cutemessagesenhanced.plugin](https://raw.githubusercontent.com/makarworld/awesome-telegram-plugins/refs/heads/main/CuteMessages/cutemessagesenhanced.plugin)

Установка: скачай файл → открой в exteraGram / AyuGram (или импортируй через менеджер плагинов).

## Файлы в папке

```
CuteMessages/
  cutemessagesenhanced.py          # исходник (рабочий)
  cutemessagesenhanced copy.plugin # локальная копия артефакта
  README.md                        # этот файл
  releases/
    v1.7.0/
      cutemessagesenhanced_v1.7.0.plugin
      secure_1.7.0.md
      CHANGELOG.md
    v1.6.1/
      cutemessagesenhanced_v1.6.1.plugin
      secure_1.6.1.md
```

## Кратко

- **Класс:** `PicMePlugin` (+ `LocalizationManager` ru/en)
- **Точка входа:** `on_send_message_hook` — трансформация текста/caption перед отправкой
- **Фильтр чатов:** все / whitelist / blacklist
- **Команды:** `.cute`, `.picme` — toggle enabled (CANCEL)
- **Undo:** последние 5 сообщений через `MESSAGE_CONTEXT_MENU` + `post_request_hook`
- **Сеть:** только ссылка доната в настройках, без загрузки кода

---

# База знаний: разработка плагинов exteraGram / AyuGram

> Ниже — общие паттерны SDK и детали реализации CuteMessages.  
> Собрано по итогам доработки `cutemessagesenhanced.py`.

---

## 1. Окружение и проект

### Клиент
- **exteraGram / AyuGram** (Android), минимум **11.9.0** (в README репо указано 12.8.1+)
- Включён движок плагинов + developer mode
- Плагины — **Python** через **Chaquopy** (Python ↔ Java interop)

### Документация SDK
- https://plugins.exteragram.app/docs
- Для IDE: `pip install exteragram-utils` (автодополнение, но импорты всё равно «неразрешённые» в pyright — это нормально, SDK живёт только на устройстве)

### Сборка и деплой
```bash
pip install -r requirements-dev.txt
python tools/build_plugin.py cutemessagesenhanced.py
# → dist/cutemessagesenhanced.plugin
python tools/deploy.py dist/cutemessagesenhanced.plugin
```

---

## 2. Анатомия плагина

### Обязательные метаданные (модульный уровень)
```python
__name__ = "CuteMessages"
__description__ = "..."
__icon__ = "ColorfulMessages/28"   # иконка в списке плагинов
__version__ = "1.7.2"
__id__ = "cutemessagesenhanced"   # уникальный ID
__author__ = "..."
__min_version__ = "11.9.0"        # мин. версия клиента
```

### Базовый класс
```python
from base_plugin import BasePlugin, HookResult, HookStrategy, MenuItemData, MenuItemType

class CuteMessagesPlugin(BasePlugin):
    def on_plugin_load(self): ...
    def on_plugin_unload(self): ...
    def create_settings(self): ...
```

### Жизненный цикл
| Метод | Когда вызывается |
|-------|------------------|
| `on_plugin_load()` | Плагин включён — регистрация хуков, меню |
| `on_plugin_unload()` | Плагин выключен — снятие меню, очистка кешей |
| `create_settings()` | UI настроек в `PluginSettingsActivity` |

---

## 3. Ключевые API SDK

### 3.1 Хук исходящих сообщений — главный инструмент

```python
def on_plugin_load(self):
    ignore_commands = self.get_setting("ignore_dot_commands", True)
    priority = -100 if ignore_commands else 200  # раньше других плагинов, если нужно
    self.add_on_send_message_hook(priority)

def on_send_message_hook(self, account, params) -> HookResult:
    # params.message — текст сообщения
    # params.caption — подпись к медиа
    # params.peer — ID чата (dialog_id / peer)
    # params.entities — форматирование (Java ArrayList)
    return HookResult(strategy=HookStrategy.MODIFY, params=params)
```

**HookStrategy:**
| Стратегия | Поведение |
|-----------|-----------|
| (пустой `HookResult`) | Не трогать сообщение |
| `MODIFY` | Изменить `params`, отправить |
| `MODIFY_FINAL` | Изменить и **не** пропускать через другие хуки |
| `CANCEL` | Отменить отправку (для команд `.cute`, `.picme`) |

**Важно:** всегда проверять наличие текста — медиа-сообщения могут не иметь `params.message`.

### 3.2 Post-request хук — получить msg_id после отправки

```python
def on_plugin_load(self):
    self.add_hook("TL_messages_sendMessage")

def post_request_hook(self, request_name, account, response, error) -> HookResult:
    if error or request_name != "TL_messages_sendMessage":
        return HookResult()
    # Парсим response.updates → TL_updateMessageID / TL_updateNewMessage
    # Получаем msg_id и peer для привязки undo-кеша
```

Используется для **undo**: в `on_send_message_hook` сохраняем оригинал в `_pending_undo[(peer,)]`, в `post_request_hook` переносим в `_undo_cache[(peer, msg_id)]`.

### 3.3 Настройки

```python
from ui.settings import Header, Divider, Switch, Selector, Text

def create_settings(self):
    return [
        Header(text="..."),
        Switch(key="enabled", text="...", default=True, on_change=self._handler),
        Selector(key="chat_filter_mode", items=[...], default=0),
        Text(text="...", subtext="..."),
    ]

# Хранение:
self.get_setting("key", default)
self.set_setting("key", value, reload_settings=True)
# Сложные данные — JSON-строка:
self.set_setting("chat_whitelist", json.dumps([123, 456]))
```

### 3.4 Пункты меню

```python
self.add_menu_item(MenuItemData(
    menu_type=MenuItemType.CHAT_ACTION_MENU,      # ⋯ в чате
    # MenuItemType.DRAWER_MENU                    # боковое меню
    # MenuItemType.MESSAGE_CONTEXT_MENU           # долгий тап на сообщение
    text="...",
    subtext="...",
    icon="menu_premium_effects",  # имя ресурса Telegram
    priority=5,
    on_click=self._handler,
))
```

**Контекст в `on_click`:**
- `CHAT_ACTION_MENU`: `context` — dict с `dialog_id`, `peer` и др.
- `MESSAGE_CONTEXT_MENU`: `context["message"]` — Java-объект `MessageObject`

### 3.5 UI-утилиты

```python
from ui.bulletin import BulletinHelper
BulletinHelper.show_info("Текст уведомления")

from android_utils import run_on_ui_thread, log
run_on_ui_thread(lambda: ...)  # обязательно для UI-операций

from client_utils import get_last_fragment, edit_message, get_messages_controller
get_last_fragment().presentFragment(PluginSettingsActivity(plugin))
edit_message(message, text="...", parse_mode="HTML")
```

### 3.6 Иконки
- Используются **имена ресурсов** Telegram: `"msg_favorite"`, `"msg_block"`, `"menu_premium_effects"`
- Не пути к файлам

---

## 4. Архитектура CuteMessages v1.7.0

### Поток обработки сообщения
```
on_send_message_hook
  ├─ .cute / .picme → toggle enabled → CANCEL
  ├─ enabled == False → skip
  ├─ _should_skip_text (точка, слэш) → skip
  ├─ _should_apply_in_chat(peer) → skip
  ├─ _snapshot_entities → _transform_with_entities → _apply_entities_to_params
  ├─ _pending_undo[(dialog_id,)] = {text, html, ts}  # dialog_id нормализуется через _normalize_dialog_id
  └─ HookStrategy.MODIFY
        ↓
post_request_hook (TL_messages_sendMessage / sendMedia / sendMultiMedia)
  └─ _undo_cache[(dialog_id, msg_id)] = record (лимит 5)
```

### Фильтр чатов
- `chat_filter_mode`: 0=все, 1=whitelist, 2=blacklist
- Отдельные настройки: `chat_whitelist`, `chat_blacklist` (JSON-массив peer ID)
- Управление: `CHAT_ACTION_MENU` → один пункт «добавить/убрать из списка» (текст зависит от режима)
- Список в настройках пересобирается через `reload_settings=True` при **любом** изменении whitelist/blacklist (`_set_chat_list` по умолчанию)
- `params.peer` — ID текущего чата

### Команды
| Команда | Действие |
|---------|----------|
| `.picme` | Toggle enabled |
| `.cute` | Toggle enabled |
| `/start`, `/help` | Пропуск (если `ignore_slash_commands=True`) |
| `.anything` | Пропуск (если `ignore_dot_commands=True`) |

### Undo (откат текста)
1. Перед отправкой: сохранить оригинал + HTML-версию entities
2. После отправки: привязать к `(dialog_id, msg_id)` через `post_request_hook`
3. `MESSAGE_CONTEXT_MENU` → «Cute: вернуть оригинал» → `edit_message` на UI thread
4. Контекст меню — Java `Map`, не Python `dict`: читать через `_ctx_get()`, id сообщения — `_message_id_from_obj()`
5. Поиск записи: `_find_undo_record()` — точный ключ, затем fallback по `msg_id`
6. При ошибке HTML: повтор с `parse_mode="html"`, затем plain text
7. Лимит: **5 последних** сообщений (`_undo_cache_limit = 5`)

### Entities (форматирование)
**Проблема:** при изменении длины текста `offset`/`length` entities «съезжают».

**Решение — сегментная трансформация:**
1. `_snapshot_entities` — копия entities в Python-dict
2. Разбить текст по границам entities на сегменты
3. Трансформировать каждый сегмент отдельно (кроме Code/Pre)
4. Пересчитать `new_offset` / `new_length` для каждой entity
5. `_apply_entities_to_params` — записать обратно в Java ArrayList

**Нормализация имён классов:**
```python
# Java: TL_messageEntityBold → Python: MessageEntityBold
if name.startswith("TL_messageEntity"):
    name = "MessageEntity" + name[len("TL_messageEntity"):]
```

---

## 5. Подходы: что пробовали и чем закончилось

### ✅ Работает хорошо

| Подход | Зачем |
|--------|-------|
| `on_send_message_hook` + `HookStrategy.MODIFY` | Основная логика трансформации |
| `post_request_hook` на `TL_messages_sendMessage` | Получить `msg_id` после отправки |
| `MESSAGE_CONTEXT_MENU` + `edit_message` | Undo без сложных хуков |
| `CHAT_ACTION_MENU` для whitelist/blacklist | Простое UX без настроек |
| JSON в `set_setting` для списков peer | Персистентное хранение |
| `BulletinHelper.show_info` | Обратная связь пользователю |
| `run_on_ui_thread` | Безопасные UI-операции |
| Сегментная трансформация entities | Сохранение форматирования |
| Команды `.cute` / `.picme` с `CANCEL` | Быстрый toggle без UI |
| Debug в тексте ошибки (`[debug: TypeError: ... @ file:line]`) | Отладка на устройстве без logcat |

### ❌ Пробовали — отказались

| Подход | Почему не подошло |
|--------|-------------------|
| **Long-press на кнопку Send** через `MethodHook` на `ChatActivityEnterView` | Сложно, хрупко, не работало стабильно; пользователь попросил убрать |
| **`AlertDialogBuilder` при long-press** | Привязан к хуку выше — удалён вместе |
| **Кнопка «Следующее сообщение — милое»** в `CHAT_ACTION_MENU` | Пользователь не хотел; заменено на whitelist/blacklist |
| **`send_mode` selector** (авто / только по кнопке) | Убран вместе с ручным режимом |
| **Единый `chat_list`** | Заменён на раздельные `chat_whitelist` + `chat_blacklist` |
| **Undo с ключом `(account, dialog_id, msg_id)`** | Несовпадения account → не работало; упрощено до `(peer, msg_id)` |
| **Undo cache limit = 100** | Слишком много памяти; снижено до 5 |

### ⚠️ Подводные камни

| Проблема | Решение |
|----------|---------|
| `TypeError: 'ArrayList$Itr' object is not iterable` | Хелпер `_iter_java()` — `toArray()`, `get(i)`, `hasNext()/next()` |
| Entities съезжают | Сегментная трансформация + пересчёт offset/length |
| `KeyError: new_offset` | Инициализация `rec["new_offset"]` / `rec["new_length"]` + `.get()` с дефолтами |
| Импорты SDK «неразрешённые» в IDE | Нормально — SDK только на устройстве |
| Приоритет хука | `-100` если нужно обработать до других плагинов (dot-команды) |
| `peer` может быть `None` | Fallback `0`, проверки `if peer is None` |

---

## 6. Хелпер `_iter_java` — обязателен для Java-коллекций

```python
def _iter_java(self, obj):
    if obj is None:
        return []
    if isinstance(obj, (list, tuple, set)):
        return list(obj)
    try:
        if hasattr(obj, "toArray"):
            return list(obj.toArray())
    except Exception:
        pass
    try:
        if hasattr(obj, "size") and hasattr(obj, "get"):
            return [obj.get(i) for i in range(int(obj.size()))]
    except Exception:
        pass
    try:
        if hasattr(obj, "hasNext") and hasattr(obj, "next"):
            items = []
            while obj.hasNext():
                items.append(obj.next())
            return items
    except Exception:
        pass
    try:
        return list(obj)
    except Exception:
        return []
```

Использовать для: `params.entities`, `response.updates`, любых Java `ArrayList`.

---

## 7. Локализация

Паттерн в `cutemessagesenhanced.py`:
```python
class LocalizationManager:
  strings = {"ru": {...}, "en": {...}}
  def get_string(self, key): ...
locali = LocalizationManager()
```

Язык: `Locale.getDefault().getLanguage()`, fallback `"en"`.

Все UI-строки — через `locali.get_string("KEY")`, не хардкод.

---

## 8. Обработка ошибок

```python
except Exception:
    exc_type, exc_val, exc_tb = sys.exc_info()
    # Лог в logcat
    log(f"Exception:\n{traceback.format_exc()}")
    # Показать пользователю оригинал + debug-инфо
    debug_suffix = f"\n\n[debug: {exc_type.__name__}: {err_msg} @ {file}:{line}]"
    params.message = f"{error_prefix}\n\n{original_text}{debug_suffix}"
    return HookResult(strategy=HookStrategy.MODIFY_FINAL, params=params)
```

`MODIFY_FINAL` — чтобы другие плагины не сломали сообщение об ошибке.

---

## 9. Текущее состояние v1.7.0 (что есть в файле)

### Настройки
- `enabled`, `show_settings_buttons`
- `chat_filter_mode` + `chat_whitelist` / `chat_blacklist`
- `ignore_slash_commands`, `ignore_dot_commands`
- Все эффекты: emoji, lowercase, uwu, stutter, vowel stretch, cute actions, punctuation, soft sign, text borders, themes

### Меню
| Тип | Пункт |
|-----|-------|
| `DRAWER_MENU` | Настройки CuteMessages (`menu_premium_effects`) |
| `CHAT_ACTION_MENU` | Настройки, добавить/убрать из белого или чёрного списка (один пункт) |
| `MESSAGE_CONTEXT_MENU` | Вернуть оригинал (только свои, последние 5) |

### Что вошло в 1.7.0 (относительно 1.6.1)

Полный список: [releases/v1.7.0/CHANGELOG.md](releases/v1.7.0/CHANGELOG.md).

- Фильтр чатов: whitelist / blacklist, список в настройках, кнопка в меню ⋯
- Undo: «вернуть оригинал» (последние 5 сообщений), сохранение entities
- Команды `.cute` / `.picme`, игнор slash-команд (`/start`, `/help`)
- Иконки: `menu_premium_effects`, `msg_favorite`, `msg_block`
- Синхронизация текста кнопки списка при смене чата и после правок в настройках

### Удалено в 1.7.x
- Long-press хук на Send
- `send_mode`, `send_button_menu`
- Кнопка «Следующее милое»
- Единый `chat_list`
- `_force_next_plain` / `_force_next_cute`

---

## 10. Рекомендации для новых плагинов

1. **Начни с `hello_world`** из SDK docs — минимальный рабочий шаблон
2. **Один хук — одна ответственность** — не смешивай UI-хуки с бизнес-логикой
3. **Не хука Java UI напрямую** (`MethodHook`) — только если нет API в SDK; очень хрупко
4. **Всегда `_iter_java`** для Java-коллекций
5. **Тестируй на устройстве** — IDE не видит SDK, py_compile только синтаксис
6. **Логируй через `log()`** + показывай debug в UI при ошибках
7. **Настройки — простые типы**; списки/сложные структуры — JSON-строки
8. **Меню — `CHAT_ACTION_MENU` / `MESSAGE_CONTEXT_MENU`** вместо кастомных overlay
9. **Приоритет хука** — если конфликтуешь с другими плагинами, экспериментируй с priority
10. **Документация:** https://plugins.exteragram.app/docs + Context7 (`/websites/plugins_exteragram_app`)

---

## 11. Полезные ссылки и файлы

| Ресурс | Путь / URL |
|--------|------------|
| Текущий плагин | `cutemessagesenhanced.py` |
| Оригинал (v1.6.x) | `cutemessagesenhanced_original.plugin` |
| SDK docs | https://plugins.exteragram.app/docs |
| Plugin class API | https://plugins.exteragram.app/docs/plugin-class |
| First plugin tutorial | https://plugins.exteragram.app/docs/first-plugin |
| История чата (transcript) | `agent-transcripts/d07d5d00-4373-4172-a42c-05667e5ab9eb/` |

---

## 12. Промпт для нового чата (копипаст)

```
Контекст: разрабатываю плагин exteraGram/AyuGram на Python (Chaquopy).
Файл: cutemessagesenhanced.py, версия 1.7.0.
База знаний: CuteMessages/README.md

Плагин перехватывает исходящие сообщения через on_send_message_hook,
трансформирует текст (cute-эффекты), сохраняет entities,
фильтрует по whitelist/blacklist чатов, поддерживает undo через
MESSAGE_CONTEXT_MENU + post_request_hook на TL_messages_sendMessage.

Важно:
- Java ArrayList итерировать через _iter_java(), не for...in
- entities пересчитывать при изменении длины текста
- UI через run_on_ui_thread
- Не использовать MethodHook на Java UI без крайней необходимости
```

---

*Сгенерировано по итогам сессии разработки CuteMessages Enhanced.*
