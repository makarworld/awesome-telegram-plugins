# 🔍 Plugin Verifier (`plugin_verifier`)

> 🛡️ Локальная верификация и глубокий анализ плагинов, просмотр кода/DB/DEX.  
> 📦 Исходник: только `plugin_verifier.plugin` · 🏷️ Версия: **2.4.8** · 📅 Обновлено: 2026-07-20

## 📋 Метаданные

| Поле | Значение |
|------|----------|
| `__id__` | `plugin_verifier` |
| `__name__` | Plugin Verifier |
| `__version__` | 2.4.8 |
| `__author__` | @JasonVurhyz |
| `__description__` | Интеллектуальная локальная верификация и глубокий анализ плагинов |
| `__icon__` | не указан |
| `__min_version__` | не указан |

## 📥 Скачать

**[Скачать plugin_verifier.plugin](https://cdn.jsdelivr.net/gh/makarworld/awesome-telegram-plugins@main/PluginVerifier/plugin_verifier.plugin)** · **[Исходник на GitHub](https://github.com/makarworld/awesome-telegram-plugins/blob/main/PluginVerifier/plugin_verifier.plugin)**

📲 **Установка:** скачай файл → открой в exteraGram / AyuGram (или импортируй через менеджер плагинов).

## 📁 Файлы в папке

```
PluginVerifier/
  plugin_verifier.plugin
  README.md
  releases/
    v2.4.8/
      plugin_verifier_v2.4.8.plugin
      secure_2.4.8.md
```

## 🎯 Назначение

1. Проверяет плагины по SHA256 whitelist и MinHash similarity.
2. Показывает статус в списке плагинов (✅ / 🔴).
3. Анализирует `.plugin`, `.py`, `.dex`, `.so`, `.db` — эвристики, embedded payloads.
4. Предупреждает при установке непроверенного плагина.
5. Маркирует пользователей из scammer-базы.

## 🏗️ Архитектура

| Класс | Роль |
|-------|------|
| `PluginVerifierPlugin` | 🎛️ Главный плагин |
| `CodeViewerBottomSheet` | 📄 Просмотр исходного кода |
| `DbViewerBottomSheet` | 🗄️ Просмотр SQLite |
| `AnalyzerBottomSheet` | 🔬 Анализ DEX/SO/payloads |
| `_OpenForViewHook` | 🔗 Перехват `AndroidUtilities.openForView` |
| `CodeLoader` | ⏳ Асинхронная загрузка кода |

## 🔗 Хуки

| Хук | Описание |
|-----|----------|
| `InstallPluginBottomSheet` ctor | `async_verify` при установке |
| `PluginCell.set` | Статус в subtitle ячейки |
| `AndroidUtilities.openForView` (все overloads) | Перехват `.dex`, `.so`, `.db`, `.py`, `.plugin` |
| `ChatActivity.onTransitionAnimationEnd` | Диалог «СКАМЕР» при входе в чат |
| `ChatMessageCell.setMessageObject` | Тег scammer на сообщениях |

## ⚙️ Настройки

| Ключ | Описание |
|------|----------|
| `db_pagination_mode` | 0 = append / 1 = replace при просмотре SQLite |

## 🖥️ UI

| Элемент | Описание |
|---------|----------|
| Subtitle в PluginCell | ✅ Проверен / 🔴 Осторожно (клик → оригинал) |
| CodeViewerBottomSheet | Подсветка, прокрутка кода |
| DbViewerBottomSheet | Таблицы SQLite с пагинацией |
| AnalyzerBottomSheet | DEX strings, SO markers, embedded payloads |
| Диалог при установке | Предупреждение о непроверенном плагине |
| Scammer alert | При входе в чат с user_id из blacklist |

## 🌐 Внешние зависимости

| Ресурс | URL |
|--------|-----|
| Supabase API | `https://piehyevxsxgbukhhblwr.supabase.co` |
| Whitelist | `/rest/v1/verified_plugins` — SHA256 + minhash |
| Scammers | `/rest/v1/chat_dumps?select=id` |
| Anon key | Hardcoded в исходнике (`SUPABASE_ANON_KEY`) |

Библиотеки: `requests`, `hashlib`, `ast`, `sqlite3`, `zlib`, `gzip`, `zipfile`.

При анализе — fetch remote `.dex`/`.so` (timeout 5s).

## 🧮 Алгоритмы

### Верификация
1. SHA256 файла vs глобальный whitelist (Supabase).
2. MinHash similarity (порог **0.55**) — обнаружение модификаций проверенного плагина.

### Эвристики (`analyze_heuristics`)
- AST: опасные imports (`socket`, `subprocess`, …)
- `eval`/`exec`, пути `.session`, base64 blobs

### Embedded payloads
- Поиск base64/zlib/gzip/zip внутри `.plugin`

### DEX/SO анализ
- In-memory парсинг строк, классов, suspicious SO markers

### Scammer tagging
- `user.scam = True`, сброс `premium`/`verified`, переименование `first_name`

## 💾 Хранение данных

- `_global_whitelist` — кэш whitelist из Supabase
- `_local_scan_cache` — кэш локальных сканов
- `_scammers_list` — set user_id из DB

## 🔐 Безопасность

### Полезные функции
- Whitelist проверенных плагинов
- Предупреждение при установке
- Анализ embedded payloads

### Критические замечания

**1. Скрытый anti-tamper в `_apply_color_gamut_compat()` (строки 32–83)**

Функция маскируется под «ColorOS fix», но:
- Читает собственный файл плагина
- Извлекает steganographic payload через Unicode-символы (`\u2060`–`\u2063`)
- Сравнивает SHA256 «очищенного» буфера с embedded checksum
- При несовпадении — `raise Exception(decompressed_payload)` из zlib

Это скрытый механизм защиты от модификации файла плагина.

**2. Hardcoded Supabase anon key** — публичный в исходнике.

**3. Remote fetch при анализе** — потенциальный вектор при анализе вредоносных URL.

**4. Scammer DB** — централизованный blacklist без прозрачной модерации.

## 🛠️ Разработка

- `BOILERPLATE_BLACKLIST` — имена, исключаемые из анализа кода.
- Декоратор `@catch` — глотает исключения с логом.
- При работе с плагином учитывать anti-tamper: изменение файла может вызвать crash.
