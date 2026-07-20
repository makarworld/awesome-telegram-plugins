# LiveWallpaper — Changelog 1.1 → 1.2

**Дата релиза:** 2026-07-20  
**Плагин:** `live_wallpaper` (LiveWallpaper)  
**Минимальная версия клиента:** 11.12.0 (без изменений)

---

## Авторы обновления 1.2

Форк и усиление безопасности:

**[@abuztrade](https://t.me/abuztrade)** & **[Awesome Telegram Plugins](https://t.me/AwesomeTelegramPlugins)**

Оригинальный плагин и DEX: @swagnonher.

---

## Кратко

Версия **1.2** — обновление безопасности форка поверх **1.1**. Функциональность живых обоев не менялась (логика в DEX), но Python-загрузчик получил проверку целостности DEX, подписанный manifest и защиту локального кэша. Объём кода вырос примерно с **~298** до **~580** строк.

Вердикт Pluggy Bot: **📛 Высокий риск** (v1.1) → **⚠️ Осторожно** (v1.2).

---

## ✨ Добавлено

### Проверка целостности DEX

- Константа **`APPROVED_DEX_SHA256`** — вшитый доверенный хеш одобренного DEX в `.plugin`.
- Перед установкой DEX сверка **SHA256** скачанного файла с trusted hash.
- Проверка SHA256 **локального кэша при каждом `_inject_dex`** — подмена файла на диске блокируется.
- Настройка **`active_dex_sha256`** — последний доверенный хеш (для offline после обновления через manifest).

### Подписанный manifest (`plugin-integrity.json`)

- Корневой [`plugin-integrity.json`](../../../plugin-integrity.json) с `dex_sha256` для `live_wallpaper`.
- Отдельный файл **`plugin-integrity.json.sig`** — RSA SHA256 подпись manifest.
- Верификация подписи через Java `Signature` + вшитый **`MANIFEST_PUBLIC_KEY_PEM`**.
- Неподписанный manifest **игнорируется** (защита от подмены хеша по сети).
- Источники manifest (порядок):
  1. GitHub raw (`plugin-integrity.json` + `.sig`)
  2. Yandex Object Storage `awesomeplugins/AwesomePlugins/` (fallback)

### Fallback при обновлении DEX на сервере

- Если remote DEX на `4plugins` изменился и хеш не совпал — автоматическая попытка скачать **bundled-копию** с GitHub (`LiveWallpaper/LiveWallpaper.dex`).
- Если и bundled не подходит — отказ с сообщением связаться с **@abuztrade**.
- **Ручная загрузка DEX** из проводника (настройки плагина) с проверкой trusted hash.
- Хук `LaunchActivity.onActivityResult` для file picker (`DEX_PICK_REQUEST`).

### Инфраструктура репозитория

- [`LiveWallpaper/LiveWallpaper.dex`](../../LiveWallpaper.dex) — проверенная копия DEX в репозитории (31 КБ).
- [`keys/manifest_public.pem`](../../../keys/manifest_public.pem) — публичный ключ подписи manifest.
- [`.github/workflows/deploy-plugin-integrity.yml`](../../../.github/workflows/deploy-plugin-integrity.yml) — CI: подпись manifest, деплой json + sig в YC, auto-commit `.sig`.
- Исходник **`live_wallpaper.py`** (сборка в `.plugin` через `build_plugin.bat`).

### Документация

- Подробный **статический анализ DEX** в `README.md` (классы, хуки, сеть, риски).
- [`keys/README.md`](../../../keys/README.md) — настройка `MANIFEST_SIGNING_KEY` в GitHub Secrets.

---

## 🔄 Изменено

- **`_smart_init`**: manifest → trusted hash → download → verify → inject (вместо только ETag/Content-Length).
- **`WallpaperInstallerSheet`**: общий путь `_download_and_verify_dex`, статусы при hash mismatch.
- **`create_settings`**: UI установки DEX при ошибке / ручной загрузке (кнопка «Выбрать LiveWallpaper.dex»).
- Метаданные: автор **`@swagnonher & @AwesomeTelegramPlugins`**.

---

## 🛡️ Безопасность (сравнение с 1.1)

| Аспект | v1.1 | v1.2 |
|--------|------|------|
| Проверка DEX | ETag + Content-Length | SHA256 + подписанный manifest |
| Вшитый хеш | нет | `APPROVED_DEX_SHA256` |
| Подпись manifest | нет | RSA SHA256withRSA |
| Проверка кэша при inject | нет | да |
| Подмена DEX на сервере | произвольный код | отказ / bundled / ручной импорт |
| Pluggy вердикт | 📛 Высокий риск | ⚠️ Осторожно |

Остаётся риском: динамическое исполнение DEX, загрузка видео по URL из DEX, отсутствие SSL pinning.

---

## 📁 Новые / изменённые файлы

```
LiveWallpaper/
  live_wallpaper.plugin      # основной артефакт
  live_wallpaper.py          # исходник для сборки
  LiveWallpaper.dex          # эталонная копия DEX
  README.md                  # модель доверия, анализ DEX
  releases/v1.2/
    live_wallpaper_v1.2.plugin
    secure_1.2.md
    CHANGELOG.md             # этот файл

plugin-integrity.json        # manifest (корень репо)
plugin-integrity.json.sig    # подпись manifest
keys/manifest_public.pem
.github/workflows/deploy-plugin-integrity.yml
```

---

## ⚙️ GitHub Secrets (для maintainers)

| Secret | Назначение |
|--------|------------|
| `MANIFEST_SIGNING_KEY` | Приватный RSA-ключ (PEM) для подписи manifest |
| `YC_ACCESS_KEY_ID` | Статический ключ SA для Yandex Object Storage |
| `YC_SECRET_ACCESS_KEY` | Секрет статического ключа YC |

---

## 🔧 Обновление DEX без нового `.plugin`

1. Проверить новый `LiveWallpaper.dex`, посчитать SHA256.
2. Обновить `dex_sha256` в `plugin-integrity.json`, push в `main`.
3. CI подпишет и задеплоит manifest → плагин v1.2+ подхватит новый хеш.
4. Для смены публичного ключа или bootstrap-хеша — новый релиз `.plugin`.

---

## ⬆️ Миграция с 1.1

- Обновить `.plugin` до v1.2.
- При первом запуске плагин запросит manifest (нужна сеть) или использует вшитый `APPROVED_DEX_SHA256`.
- Если локальный DEX не совпадает с trusted hash — переустановка через installer или ручной импорт `LiveWallpaper.dex` из репозитория.

---

## Ссылки

- [Скачать live_wallpaper.plugin](https://raw.githubusercontent.com/makarworld/awesome-telegram-plugins/refs/heads/main/LiveWallpaper/live_wallpaper.plugin)
- [plugin-integrity.json](https://raw.githubusercontent.com/makarworld/awesome-telegram-plugins/refs/heads/main/plugin-integrity.json)
- [Pluggy Bot](https://t.me/pluggy_robot) — отчёт безопасности
