# Plugin Verifier — техническая документация

> ID: `plugin_verifier` · v2.4.8 · исходник: `plugin_verifier.plugin`

Пользовательская документация: [README.md](README.md)

## Метаданные

| Поле | Значение |
|------|----------|
| `__id__` | `plugin_verifier` |
| `__version__` | 2.4.8 |
| `__author__` | @JasonVurhyz |

## Архитектура

| Класс | Роль |
|-------|------|
| `PluginVerifierPlugin` | Главный плагин |
| `CodeViewerBottomSheet` | Просмотр кода |
| `DbViewerBottomSheet` | SQLite viewer |
| `AnalyzerBottomSheet` | DEX/SO/payloads |
| `_OpenForViewHook` | Перехват `openForView` |
| `CodeLoader` | Асинхронная загрузка |

## Хуки

| Хук | Описание |
|-----|----------|
| `InstallPluginBottomSheet` ctor | `async_verify` при установке |
| `PluginCell.set` | ✅/🔴 в subtitle |
| `AndroidUtilities.openForView` | `.dex`, `.so`, `.db`, `.py`, `.plugin` |
| `ChatActivity.onTransitionAnimationEnd` | Диалог «СКАМЕР» |
| `ChatMessageCell.setMessageObject` | Тег scammer |

## Настройки

| Ключ | Описание |
|------|----------|
| `db_pagination_mode` | 0=append / 1=replace в SQLite viewer |

## Алгоритмы

### Верификация
1. SHA256 vs whitelist (Supabase)
2. MinHash similarity (порог **0.55**)

### Эвристики
- AST: опасные imports (`socket`, `subprocess`, …)
- `eval`/`exec`, `.session`, base64 blobs
- Embedded payloads: base64/zlib/gzip/zip

### Scammer tagging
- `user.scam = True`, сброс premium/verified

## Внешние зависимости

| URL | Назначение |
|-----|------------|
| `piehyevxsxgbukhhblwr.supabase.co` | Whitelist + scammers |
| `/rest/v1/verified_plugins` | SHA256 + minhash |
| `/rest/v1/chat_dumps?select=id` | Scammer IDs |

`SUPABASE_ANON_KEY` — hardcoded. При анализе — fetch remote `.dex`/`.so` (timeout 5s).

## Критические замечания

**1. Anti-tamper в `_apply_color_gamut_compat()` (стр. 32–83)**

Маскируется под «ColorOS fix»:
- Читает собственный файл
- Steganography через Unicode `\u2060`–`\u2063`
- SHA256 vs embedded checksum
- При несовпадении — `raise Exception` из zlib

**2.** Hardcoded Supabase key  
**3.** Remote fetch при анализе  
**4.** Централизованный scammer blacklist

## Разработка

- `BOILERPLATE_BLACKLIST` — исключения из анализа
- Декоратор `@catch`
- Изменение файла может вызвать crash anti-tamper
