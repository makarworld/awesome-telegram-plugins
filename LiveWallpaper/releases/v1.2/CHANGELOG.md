# LiveWallpaper — Changelog 1.1 → 1.2

**Дата релиза:** 2026-07-20  
**Плагин:** `live_wallpaper` (LiveWallpaper)  
**Минимальная версия клиента:** 11.12.0 (без изменений)

---

## Кратко

Версия **1.2** — усиление безопасности загрузки нативного DEX-модуля: проверка SHA256, подписанный manifest, fallback-источники и ручной импорт `.dex`. Вердикт Pluggy: **⚠️ Осторожно** (было **📛 Высокий риск** в 1.1).

---

## ✨ Добавлено

### Цепочка доверия DEX

- **SHA256** при скачивании и перед каждой инъекцией (`_verify_local_dex`, `_download_and_verify_dex`).
- Подписанный manifest [`plugin-integrity.json`](../../../plugin-integrity.json) + `.sig` (RSA + SHA256).
- Bootstrap-хеш `APPROVED_DEX_SHA256` вшит в `.plugin` для первого запуска.
- Настройка `active_dex_sha256` — offline-доверие после успешной установки.

### Источники и fallback

| Приоритет | Источник |
|-----------|----------|
| 1 | `storage.yandexcloud.net` — основной DEX |
| 2 | GitHub raw `LiveWallpaper/LiveWallpaper.dex` — bundled fallback |
| 3 | Ручной импорт через file picker |

Manifest: GitHub → Yandex Cloud (`MANIFEST_URLS`).

### Ручная установка DEX

- Пункт в настройках: «Выбрать LiveWallpaper.dex с устройства».
- `MethodHook` на `LaunchActivity.onActivityResult` (request `42042`).
- Импорт с проверкой SHA256 против доверенного хеша.

### UI установки

- `WallpaperInstallerSheet` — проверка хеша, прогресс, fallback на bundled DEX.
- Сообщения при несовпадении хеша: контакт @abuztrade, инструкция ручной загрузки.

---

## 🔄 Изменено

| Область | Было (1.1) | Стало (1.2) |
|---------|------------|-------------|
| Проверка DEX | Только ETag/Content-Length | SHA256 + RSA manifest |
| Загрузка DEX | Только Yandex Cloud | Yandex → GitHub → ручной импорт |
| Автор | @swagnonher | @swagnonher & @AwesomeTelegramPlugins |
| Вердикт Pluggy | 📛 Высокий риск | ⚠️ Осторожно |

---

## 🔧 Технические детали

### Алгоритм `_smart_init`

```
1. GET plugin-integrity.json + .sig (GitHub → YC)
2. RSA verify → trusted hash = manifest.dex_sha256
3. Иначе: active_dex_sha256 → APPROVED_DEX_SHA256 (вшит)
4. HEAD remote DEX → нужно ли обновление
5. Download → sha256 == trusted → сохранить
6. При inject: sha256 кэша == trusted
7. DexClassLoader → LiveWallpaper.init()
```

### Внешние URL

- DEX: `storage.yandexcloud.net/4plugins/.../LiveWallpaper.dex`
- Bundled: `raw.githubusercontent.com/.../LiveWallpaper/LiveWallpaper.dex`
- Manifest: `plugin-integrity.json` (+ `.sig`)

### Локальные пути

- `{app}/dex_modules/LiveWallpaper.dex` (chmod 444)
- `{app}/dex_opt/` — DexClassLoader

---

## 📦 Файлы релиза

```
LiveWallpaper/releases/v1.2/
  live_wallpaper_v1.2.plugin
  secure_1.2.md
  CHANGELOG.md
```

---

## ✅ Безопасность

По отчёту Pluggy Bot ([secure_1.2.md](./secure_1.2.md)): **⚠️ Осторожно**.

- Remote DEX остаётся — повышенный риск по природе архитектуры.
- Подмена без обхода подписи manifest и SHA256 затруднена.
- MITM возможен из‑за отсутствия SSL pinning.

---

## ⬆️ Миграция с 1.1

- При первом запуске v1.2 может перекачать DEX, если хеш не совпадает с доверенным.
- Если сервер обновился раньше manifest — используйте bundled fallback или ручной импорт.
- Настройки обоев (видео MP4) в DEX — без изменений в Python-части.
