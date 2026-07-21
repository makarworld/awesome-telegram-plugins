Проверенно с помощью Pluggy Bot (pluggy_robot.t.me)

❔ Отчёт • Mistral

✦ Метаданные плагина ✦
┌ Название: Kangel Plugins Manager
├ ID: kangel_plugins_manager
├ Версия: 1.4.3
├ Автор: @ArThirtyFour | @KangelPlugins
├ Описание: Первый магазин плагинов , предлагающий удобное управление плагинами
Требования: exteraGram/Ayugram 12.5.1 и выше

First plugin store with easy plugin management
Requirements:exteraGram/AyuGram 12.5.1 or higher
├ Иконка: Kangelcons_by_fStikBot/5
└ Мин. версия: 12.5.1

📅 Дата проверки: 2026-07-21 02:47

✦ Вердикт: ❔ Недостаточно данных
──────────────
☶ Назначение: Плагин предназначен для управления плагинами через магазин плагинов Kangel.
──────────────
❏ Анализ:
• Вердикт 'unknown' из-за недостатка данных: основная логика плагина находится в внешнем модуле 'kangelpluginsmanager', который не предоставлен для анализа.
• Код плагина минимален и не содержит явных вредоносных действий.
• Основная функциональность реализована в внешнем модуле 'kangelpluginsmanager'.
• Отсутствие видимых сетевых запросов или работы с файлами в предоставленном коде.
• Необходим анализ модуля 'kangelpluginsmanager' для полной оценки безопасности.


🌐 Сетевые обращения (статический анализ)
Найдены упоминания: https=1
URL (пример): https://github.com/KangelPlugins/PluginManager

Найдены домены/IP: 1
- github.com; страна IP: DE (Германия); регистрация: 2007-10-09 (18 лет назад); VT: malicious=0, suspicious=0

---

## Дополнение: анализ PyPI-пакета `kangelpluginsmanager` (ручной обзор)

> Дата дополнения: 2026-07-21 · не Pluggy Bot  
> Источники: [PyPI KangelPluginsManager](https://pypi.org/project/KangelPluginsManager/), [github.com/KangelPlugins/PluginManager](https://github.com/KangelPlugins/PluginManager), сравнение с архивом v1.3.2

### Почему Pluggy дал «недостаточно данных»

`.plugin` v1.4.3 — обёртка из 73 строк. Весь исполняемый код подтягивается через `__requirements__ = "kangelpluginsmanager==1.4.3"`. Статический анализ только `.plugin` не видит сеть, файлы и UI-хуки.

### PyPI-пакет

| Поле | Значение |
|------|----------|
| Имя | `kangelpluginsmanager` (PyPI: KangelPluginsManager) |
| Пин в плагине | `==1.4.3` |
| Актуальная на PyPI | 1.4.3.4 (2026-07-20) |
| Зависимости | `requests>=2.31.0` |
| Лицензия | MIT |
| Автор PyPI | ArThirtyFour |
| Уязвимости (PyPI API) | не зафиксированы |

Структура wheel: `plugin.py` (~300 KB), `methods.py`, `sbroka.py`, `assests/locale.json`, `assests/bages.json`. Исходники открыты в репозитории PluginManager.

### Сопоставление с v1.3.2

Логика v1.4.3 совпадает с монолитным `.plugin` v1.3.2 (код вынесен в библиотеку без смены назначения). Выводы отчёта v1.3.2 (**⚠️ Осторожно**) применимы и к v1.4.3, с добавлением вектора supply chain через PyPI.

### Сеть (из кода библиотеки / v1.3.2)

| Домен | Назначение |
|-------|------------|
| `raw.githubusercontent.com` | Каталог `store.json` |
| `api.github.com` | Проверка версии каталога |
| `mkstats.mk69.su` | Телеметрия mkStats (PoW, хеши устройства/плагина) |
| `github.com`, `t.me` | Ссылки в UI, deeplink'и |

HTTPS, таймауты в `requests`/`urllib`. Телеметрия отключается (`telemetry_enabled`).

### Поведение и риски

- **Установка кода из интернета** — основной риск: скачивание `.plugin` по URL из каталога и установка через SDK клиента.
- **Импорт коллекций** (`.kpm`) — может массово ставить плагины (`import_collection` с `auto_install`).
- **Телеметрия mkStats** — анонимные метрики на сторонний сервер; доверие к оператору `mkstats.mk69.su`.
- **dynamic_proxy** — хуки UI Telegram/exteraGram; не вредоносно само по себе, усложняет аудит.
- **Файлы** — чтение/запись в директории плагинов, кэш `.kpm_cache.json`; `shutil` для операций с файлами плагинов.
- **Clipboard / Intent** — открытие ссылок, deeplink `tg://kpm_install`.

Не обнаружено в коде библиотеки: `exec`, `eval`, `subprocess`, `os.system`, произвольный `__import__`.

### Supply chain (новое в v1.4.3)

- Клиент ставит wheel с PyPI при загрузке плагина — доверие к PyPI-аккаунту ArThirtyFour и целостности пакета.
- Пин `==1.4.3` снижает риск неожиданного обновления; на PyPI уже есть 1.4.3.3/1.4.3.4 — они **не** подтянутся автоматически.
- Для полного аудита: прогнать Pluggy Bot по wheel `kangelpluginsmanager-1.4.3` или по репозиторию PluginManager.

### Итоговая оценка (дополнение)

| Вердикт Pluggy (.plugin) | ❔ Недостаточно данных |
| Вердикт с учётом PyPI | **⚠️ Осторожно** (как v1.3.2 + supply chain PyPI) |

Рекомендация: ставить только из доверенного каталога; отключить телеметрию при необходимости; перед установкой сторонних плагинов из магазина — проверять через Plugin Verifier или ручной аудит.