# awesome-plugins — документация для разработчиков

Коллекция плагинов для **exteraGram / AyuGram** (Android, Python через Chaquopy).

> Обновлено: 2026-07-21

## Разделение документации

| Файл | Аудитория | Содержание |
|------|-----------|------------|
| [`README.md`](README.md) | Пользователи | Обзор, скачивание, краткое описание плагинов |
| **`docs.md` (корень)** | Разработчики | Общий флоу, SDK, сборка, каталог |
| **`ПапкаПлагина/README.md`** | Пользователи | Установка, как пользоваться, риски |
| **`ПапкаПлагина/docs.md`** | Разработчики | Хуки, архитектура, настройки, алгоритмы |

Правило для агента: [`.cursor/rules/plugin-workflow.mdc`](.cursor/rules/plugin-workflow.mdc)

## Флоу работы

1. Прочитать **[`README.md`](README.md)** — обзор для пользователей.
2. Прочитать **`ПапкаПлагина/docs.md`** — технические детали плагина (**обязательно перед правками**).
3. При необходимости — этот **`docs.md`** (SDK, сборка, каталог).
4. После изменений:
   - пользовательские правки → `ПапкаПлагина/README.md`;
   - технические детали → `ПапкаПлагина/docs.md`;
   - версия/статус/каталог → корневой `docs.md` и `README.md`.

## Окружение

| | |
|---|---|
| Клиент | exteraGram / AyuGram (Android) |
| SDK | https://plugins.exteragram.app/docs |
| Python | Chaquopy (Python ↔ Java interop) |
| IDE | `pip install exteragram-utils` (автодополнение; pyright-ошибки импортов — норма) |
| Код в репозитории | `*.plugin` — артефакт для пользователей (валидный Python) |
| Локальная разработка | `__id__.py` на ПК → деплой на устройство как `.py`; перед релизом копия в `.plugin` |

### Разработка и публикация (SDK)

Официальный флоу: [plugins.exteragram.app/docs/setup](https://plugins.exteragram.app/docs/setup)

1. **Исходник** — один файл `<plugin_id>.py` (имя = `__id__` + `.py`).
2. **На устройстве** — тот же файл в `.../files/plugins/<plugin_id>.py`; developer mode + DevServer (`42690`) или ADB.
3. **Итерация** — `catalib watch --deploy` ([catalib workflow](https://raito-kyokai.gitbook.io/catalib/deploi/workflow.md)) или ручной push + reload.
4. **Публикация** — тот же код с расширением `.plugin` (установка из чата / raw-ссылки). Содержимое `.py` и `.plugin` идентично.

В этом репозитории `.py` в git не коммитится (`.gitignore`); в main пушится `.plugin`.

```bat
:: однофайловый плагин — перед коммитом релиза:
copy /Y VersionOverride\version_override.py VersionOverride\version_override.plugin

:: модульные проекты (несколько файлов) — catalib:
catalib build
:: → dist\<id>.py и dist\<id>.plugin (одинаковые)
```

Упрощённый хелпер монорепо (не из SDK): `.tools\build_plugin.bat PluginFolder` — копирует единственный `.py` → `.plugin`.

### Ссылки на артефакты

| Назначение | Шаблон |
|------------|--------|
| **Скачать** | `https://cdn.jsdelivr.net/gh/makarworld/awesome-telegram-plugins@main/{путь}` |
| **Код** | `https://github.com/makarworld/awesome-telegram-plugins/blob/main/{путь}` |
| **Raw** | `https://raw.githubusercontent.com/makarworld/awesome-telegram-plugins/refs/heads/main/{путь}` |

## База знаний: SDK exteraGram

### Анатомия плагина

```python
__name__ = "MyPlugin"
__description__ = "..."
__icon__ = "ColorfulMessages/28"
__version__ = "1.0.0"
__id__ = "my_plugin_id"
__author__ = "..."
__min_version__ = "11.9.0"

from base_plugin import BasePlugin, HookResult, HookStrategy, MenuItemData, MenuItemType

class MyPlugin(BasePlugin):
    def on_plugin_load(self): ...
    def on_plugin_unload(self): ...
    def create_settings(self): ...
```

| Метод | Когда вызывается |
|-------|------------------|
| `on_plugin_load()` | Плагин включён — регистрация хуков, меню |
| `on_plugin_unload()` | Плагин выключен — снятие меню, очистка |
| `create_settings()` | UI настроек в `PluginSettingsActivity` |

### Хук исходящих сообщений

```python
def on_plugin_load(self):
    self.add_on_send_message_hook(priority)

def on_send_message_hook(self, account, params) -> HookResult:
    return HookResult(strategy=HookStrategy.MODIFY, params=params)
```

| `HookStrategy` | Поведение |
|----------------|-----------|
| (пустой) | Не трогать |
| `MODIFY` | Изменить `params` |
| `MODIFY_FINAL` | Изменить и не пропускать другие хуки |
| `CANCEL` | Отменить отправку |

### Post-request хук

```python
def on_plugin_load(self):
    self.add_hook("TL_messages_sendMessage")

def post_request_hook(self, request_name, account, response, error) -> HookResult:
    ...
```

### Настройки

```python
from ui.settings import Header, Switch, Selector, Text

def create_settings(self):
    return [Switch(key="enabled", text="...", default=True)]

self.get_setting("key", default)
self.set_setting("key", value, reload_settings=True)
# списки — JSON-строка
```

### Меню

```python
self.add_menu_item(MenuItemData(
    menu_type=MenuItemType.CHAT_ACTION_MENU,
    text="...", icon="menu_premium_effects", on_click=self._handler,
))
```

Типы: `CHAT_ACTION_MENU`, `DRAWER_MENU`, `MESSAGE_CONTEXT_MENU`.

### UI-утилиты

```python
from ui.bulletin import BulletinHelper
from android_utils import run_on_ui_thread, log
from client_utils import get_last_fragment, edit_message
```

Иконки — **имена ресурсов** Telegram (`"msg_favorite"`), не пути к файлам.

### Итерация Java-коллекций

```python
def _iter_java(obj):
    if obj is None: return []
    if hasattr(obj, "toArray"): return list(obj.toArray())
    if hasattr(obj, "size") and hasattr(obj, "get"):
        return [obj.get(i) for i in range(int(obj.size()))]
    ...
```

Использовать для `params.entities`, `response.updates`, любых Java `ArrayList`.

### Рекомендации

1. Начни с [first plugin tutorial](https://plugins.exteragram.app/docs/first-plugin).
2. Один хук — одна ответственность.
3. Не хука Java UI (`MethodHook`) без крайней необходимости.
4. Тестируй на устройстве — IDE не видит SDK.
5. Сложные настройки — JSON в `set_setting`.
6. Документация SDK: https://plugins.exteragram.app/docs · Context7: `/websites/plugins_exteragram_app`

## Каталог плагинов

| Папка | ID | Версия | Файл | README | docs |
|-------|----|--------|------|--------|------|
| [CuteMessages](CuteMessages/) | `cutemessagesenhanced` | 1.7.1 | `cutemessagesenhanced.plugin` | [README](CuteMessages/README.md) | [docs](CuteMessages/docs.md) |
| [KangelPluginsManager](KangelPluginsManager/) | `kangel_plugins_manager` | 1.4.3 | `kangel_plugins_manager.plugin` | [README](KangelPluginsManager/README.md) | [docs](KangelPluginsManager/docs.md) |
| [LiveWallpaper](LiveWallpaper/) | `live_wallpaper` | 1.2 | `live_wallpaper.plugin` | [README](LiveWallpaper/README.md) | [docs](LiveWallpaper/docs.md) |
| [UnlimitedPins](UnlimitedPins/) | `misha_unlimited_pins` | 2.0 | `misha_unlimited_pins.plugin` | [README](UnlimitedPins/README.md) | [docs](UnlimitedPins/docs.md) |
| [PluginVerifier](PluginVerifier/) | `plugin_verifier` | 2.4.8 | `plugin_verifier.plugin` | [README](PluginVerifier/README.md) | [docs](PluginVerifier/docs.md) |
| [ListOfCommands](ListOfCommands/) | `list_of_commands` | 1.0.8 | `list_of_commands.plugin` | [README](ListOfCommands/README.md) | [docs](ListOfCommands/docs.md) |
| [TomatoBom](TomatoBom/) | `tomato_bom` | 1.2.8 | `tomato_bom.plugin` | [README](TomatoBom/README.md) | [docs](TomatoBom/docs.md) |
| [WSBypass](WSBypass/) | `wsbypass` | 3.0.5 | `wsbypass.plugin` | [README](WSBypass/README.md) | [docs](WSBypass/docs.md) |
| [VersionOverride](VersionOverride/) | `version_override` | 1.0.3 | `version_override.plugin` | [README](VersionOverride/README.md) | [docs](VersionOverride/docs.md) |

## Сводка по типам

| Тип | Плагины |
|-----|---------|
| Send message hook | CuteMessages, KangelPluginsManager, ListOfCommands, AIEdit* |
| Method / protocol hooks | UnlimitedPins, PluginVerifier, KangelPluginsManager, ListOfCommands, WSBypass, VersionOverride |
| Remote code (DEX) | LiveWallpaper |
| UI overlay | TomatoBom |
| Сеть | KangelPluginsManager, LiveWallpaper, PluginVerifier, TomatoBom, WSBypass |
| Локальный прокси / туннель | WSBypass |

\* AIEdit — вне этого репозитория.

### Минимальные версии клиента

| Плагин | `__min_version__` |
|--------|-------------------|
| CuteMessages | 11.9.0 |
| KangelPluginsManager | 12.5.1 |
| LiveWallpaper | 11.12.0 |
| ListOfCommands | 11.12.0 |
| VersionOverride | 11.12.0 |
| WSBypass | 12.5.1 (app) |

## Безопасность (кратко)

| Плагин | Риск | Причина |
|--------|------|---------|
| CuteMessages | низкий | Локальная обработка текста |
| KangelPluginsManager | **высокий** | Установка плагинов из интернета |
| LiveWallpaper | **критический** | Remote DEX |
| UnlimitedPins | низкий | Локальная манипуляция лимитов |
| PluginVerifier | **критический** | Anti-tamper, широкие привилегии |
| ListOfCommands | низкий | Regex-парсинг файлов плагинов |
| TomatoBom | низкий–средний | Overlay + загрузка ассетов |
| WSBypass | низкий–средний | Туннель через KWS-серверы |
| VersionOverride | низкий–средний | Обход проверки версии при установке |

Подробности — `secure.md` в папке плагина. Отчёты: [Pluggy Bot](https://t.me/pluggy_robot).

## Структура репозитория

```
awesome-plugins/
  README.md              # обзор для пользователей
  docs.md                # этот файл — общая документация
  .cursor/rules/
  .tools/build_plugin.bat
  CuteMessages/
    README.md
    docs.md
    cutemessagesenhanced.plugin   # код (Python), в git только .plugin
    releases/vX.Y.Z/
```

## Версии и `releases/`

- **Текущая разработка** — `*.plugin` в корне папки плагина, `__version__` внутри файла.
- **`.py` не публикуется** — локально для правок, при необходимости `build_plugin.bat`.
- **`releases/vX.Y.Z/`** — архив опубликованного релиза, не черновик.
- Пока версия не запушена в `main` — в `releases/` ничего не добавлять.
- При релизе: скопировать `.plugin` + `secure_*.md` → обновить каталог здесь и корневой `README.md`.

## Полезные ссылки

| Ресурс | URL |
|--------|-----|
| SDK docs | https://plugins.exteragram.app/docs |
| Plugin class API | https://plugins.exteragram.app/docs/plugin-class |
| KPM Store | https://github.com/KangelPlugins/Plugins-Store |
| Pluggy Bot | https://t.me/pluggy_robot |
| Manifest signing | [keys/README.md](keys/README.md) |
