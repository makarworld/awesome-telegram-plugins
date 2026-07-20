# awesome-plugins

Подборка плагинов для **exteraGram / AyuGram** — кастомного Android-клиента Telegram с движком плагинов на Python.

Здесь собраны утилиты, развлечения и инструменты: от милых сообщений и помидорного обстрела до магазина плагинов и аудита безопасности. Каждый плагин — отдельная папка с `.plugin`-файлом, подробным `docs.md` и (где есть) отчётом `secure.md`.

| Плагин | Версия | Зачем ставить | Риск |
|--------|--------|---------------|------|
| [CuteMessages](#cutemessages) | 1.7.7 | Милые исходящие сообщения, undo | 🟢 |
| [Tomato bom](#tomato-bom) | 1.2.8 | Кидать помидоры по UI | 🟡 |
| [LiveWallpaper](#livewallpaper) | 1.1 | Видео-обои в чатах | 🔴 |
| [Unlimited Pins](#unlimited-pins) | 2.0 | Без лимита закрепов | 🟢 |
| [List of Commands](#list-of-commands) | 1.0.8 | Подсказки dot-команд | 🟢 |
| [Kangel Plugins Manager](#kangel-plugins-manager) | 1.3.2 | Магазин плагинов | 🟠 |
| [Plugin Verifier](#plugin-verifier) | 2.4.8 | Проверка плагинов на вирусы | 🔴* |

---

## Плагины

### CuteMessages

**ID:** `cutemessagesenhanced` · **v1.7.7** · @mihailkotovski, @mishabotov  
**Документация:** [CuteMessages/docs.md](CuteMessages/docs.md)

Превращает исходящие сообщения в «милые»: UwU, рамки, эмодзи, растягивание гласных, каомодзи. Можно ограничить чаты whitelist/blacklist, откатить последние 5 сообщений через контекстное меню. Команды `.cute` / `.picme` — быстрый toggle. Локализация ru/en.

Работает через перехват исходящих сообщений до отправки; форматирование (bold, code и т.д.) сохраняется за счёт пересчёта entities.

**Безопасность: 🟢 низкий риск** — только локальная обработка текста, сеть не используется (кроме ссылки доната в настройках).  
Отчёт: [releases/v1.6.1/secure_1.6.1.md](CuteMessages/releases/v1.6.1/secure_1.6.1.md) — ✅ Безопасно.

> Единственный плагин в репозитории с открытым `.py`-исходником — `cutemessagesenhanced.py`. Остальные дорабатывались и документировались здесь же.


---


### Kangel Plugins Manager

**ID:** `kangel_plugins_manager` · **v1.3.2** · @ArThirtyFour, @KangelPlugins  
**Документация:** [KangelPluginsManager/docs.md](KangelPluginsManager/docs.md)

Полноценный магазин плагинов для exteraGram: каталог с GitHub, установка и обновление одним тапом, inline-поиск `@kpm` прямо в чате, pill-виджет со счётчиком, наборы плагинов (builds), deeplink `tg://kpm_install`. Телеметрия mkStats (отключается в настройках).

По сути — App Store внутри Telegram-клиента.

**Безопасность: 🟠 высокий** — основная функция = установка произвольного кода из интернета. PoW защищает API статистики, не каталог.  
Отчёт: [KangelPluginsManager/secure.md](KangelPluginsManager/secure.md) — ⚠️ Осторожно.

---

### Tomato bom

**ID:** `tomato_bom` · **v1.2.8** · Windukk  
**Документация:** [TomatoBom/docs.md](TomatoBom/docs.md)

Чистое развлечение. Включаешь из меню чата или бокового меню — поверх всего UI появляется слой, куда можно кидать помидоры. Тап — один помидор, удержание — пулемёт. Звук splat, GIF-анимация. Выход — двойной тап.

Настраиваются размер помидора, громкость и скорость автострельбы.

**Безопасность: 🟡 низкий–средний** — overlay перехватывает touch; GIF/MP3 качаются с gitflic.ru без checksum. Исполняемого кода нет.

---

### LiveWallpaper

**ID:** `live_wallpaper` · **v1.1** · @swagnonher  
**Документация:** [LiveWallpaper/docs.md](LiveWallpaper/docs.md)

Живые видео-обои вместо скучного фона чата. Python-часть только загружает нативный модуль с сервера — вся магия внутри DEX. При первом запуске — bottom sheet с прогрессом загрузки.

**Безопасность: 🔴 критический** — remote DEX без подписи и хеша. Любая подмена файла на CDN = произвольный код на устройстве.  
Отчёт: [LiveWallpaper/secure.md](LiveWallpaper/secure.md) — 📛 Высокий риск.

Ставить только если полностью доверяете автору и хостингу.

---

### Unlimited Pins

**ID:** `misha_unlimited_pins` · **v2.0** · @mihailkotovski, @mishabotov  
**Документация:** [UnlimitedPins/docs.md](UnlimitedPins/docs.md)

Снимает лимит закреплённых чатов (до 100 000) и помнит состояние между перезапусками. Перехватывает pin/unpin на уровне `MessagesController` и протокола Telegram, сохраняет в локальный JSON. Кнопка «вернуть закрепы» — принудительное восстановление.

**Безопасность: 🟢 низкий** — только локальная манипуляция лимитов, сеть не трогает. Сервер Telegram может откатывать «лишние» закрепы — это ожидаемо.

---

### List of Commands

**ID:** `list_of_commands` · **v1.0.8** · @bandaliyev  
**Документация:** [ListOfCommands/docs.md](ListOfCommands/docs.md)

Набираешь `.` в чате — видишь все dot-команды установленных плагинов с описаниями. Можно отключать ненужные подсказки и добавлять свои. `.preload` — пересобрать кэш после установки нового плагина.

Сканирует папку плагинов regex-парсингом, без выполнения кода.

**Безопасность: 🟢 низкий** — читает только файлы в папке плагинов, сеть не используется.  
Отчёт: [ListOfCommands/secure.md](ListOfCommands/secure.md) — ✅ Безопасно.

---

### Plugin Verifier

**ID:** `plugin_verifier` · **v2.4.8** · @JasonVurhyz  
**Документация:** [PluginVerifier/docs.md](PluginVerifier/docs.md)

«Антивирус» для плагинов. Сверяет SHA256 с whitelist, ищет модификации через MinHash, анализирует `.plugin`/`.dex`/`.so`/`.db`, предупреждает при установке непроверенного, маркирует scammer-аккаунты. В списке плагинов — ✅ или 🔴. Именно он генерирует отчёты `secure.md` в этом репозитории.

**Безопасность: 🔴 парадокс** — полезен для аудита, но сам содержит скрытый anti-tamper (steganography в «ColorOS fix») и тянет blacklist с Supabase. Модифицировать осторожно.

\* *Критический не значит «вредоносный» — скрытые механизмы защиты и широкие привилегии анализа.*

---

## Безопасность — кратко

| Плагин | Уровень | Отчёт |
|--------|---------|-------|
| CuteMessages | 🟢 | [secure_1.6.1.md](CuteMessages/releases/v1.6.1/secure_1.6.1.md) |
| ListOfCommands | 🟢 | [secure.md](ListOfCommands/secure.md) |
| Unlimited Pins | 🟢 | — |
| Tomato bom | 🟡 | — |
| Kangel Plugins Manager | 🟠 | [secure.md](KangelPluginsManager/secure.md) |
| LiveWallpaper | 🔴 | [secure.md](LiveWallpaper/secure.md) |
| Plugin Verifier | 🔴* | — |

- **🟢** — локальная логика, без загрузки кода
- **🟡** — сеть для ассетов или overlay
- **🟠** — установка стороннего кода из интернета
- **🔴** — remote code execution или скрытый anti-tamper

---

## О репозитории

Монорепозиторий: исходники, документация, отчёты безопасности и артефакты `.plugin` для всех семи плагинов выше.

- Технический каталог для разработки — [`docs.md`](docs.md)
- Детали каждого плагина — `ПапкаПлагина/docs.md`
- Правило флоу для агента Cursor — [`.cursor/rules/plugin-workflow.mdc`](.cursor/rules/plugin-workflow.mdc)

### Окружение

| | |
|---|---|
| Клиент | exteraGram / AyuGram (Android) |
| SDK | [plugins.exteragram.app/docs](https://plugins.exteragram.app/docs) |
| Python | Chaquopy (Python ↔ Java) |
| IDE | `pip install exteragram-utils` |
| Артефакт | `*.plugin` — файл для установки в клиент |

### Как обновлять плагины

1. Прочитать `docs.md` (корень + папка плагина).
2. Править `.py` или `.plugin`.
3. Обновить документацию на обоих уровнях.
4. Для `.py` — собрать артефакт и проверить синтаксис:

```bat
python -m py_compile CuteMessages\cutemessagesenhanced.py
tools\build_plugin.bat CuteMessages
```

5. Установить `.plugin` на устройство вручную через клиент.

### Инструменты разработки (Cursor)

По прошлым сессиям (июль 2026):

| Инструмент | Зачем |
|------------|-------|
| **Context7** MCP | Документация SDK exteraGram (`/websites/plugins_exteragram_app`) |
| **zread** MCP | Поиск примеров в экосистеме |
| **ponytail** skill | Минимальные правки без оверинжиниринга |
| **create-rule** skill | Правило `plugin-workflow.mdc` |
| **Plugin Verifier** | Генерация `secure.md`, эталон хуков |
| `tools/build_plugin.bat` | `.py` → `.plugin` |
| `exteragram-utils` | Автодополнение в IDE |

### Структура

```
awesome-plugins/
  README.md              # этот файл
  docs.md                # технический каталог
  tools/build_plugin.bat
  CuteMessages/          # .py + .plugin + docs + releases/
  KangelPluginsManager/
  LiveWallpaper/
  UnlimitedPins/
  PluginVerifier/
  ListOfCommands/
  TomatoBom/
```

### Ссылки

| Ресурс | URL |
|--------|-----|
| SDK | https://plugins.exteragram.app/docs |
| Plugin API | https://plugins.exteragram.app/docs/plugin-class |
| KPM Store | https://github.com/KangelPlugins/Plugins-Store |

---

*Обновлено: 2026-07-20*
