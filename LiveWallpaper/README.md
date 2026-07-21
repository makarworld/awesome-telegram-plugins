# 🎬 LiveWallpaper (`live_wallpaper`)

> 🖼️ Живые (видео) обои в чатах вместо статичного фона.  
> 📦 Исходник: только `live_wallpaper.plugin` · 🏷️ Версия: **1.2** (в разработке) · 📅 Обновлено: 2026-07-20

## 📋 Метаданные

| Поле | Значение |
|------|----------|
| `__id__` | `live_wallpaper` |
| `__name__` | LiveWallpaper |
| `__version__` | 1.2 |
| `__author__` | @swagnonher |
| `__description__` | Живые обои в чатах, вместо скучных статичных |
| `__icon__` | Animasha26/22 |
| `__min_version__` | 11.12.0 |

## 📥 Скачать

**[Скачать live_wallpaper.plugin](https://cdn.jsdelivr.net/gh/makarworld/awesome-telegram-plugins@main/LiveWallpaper/live_wallpaper.plugin)** · **[Исходник на GitHub](https://github.com/makarworld/awesome-telegram-plugins/blob/main/LiveWallpaper/live_wallpaper.plugin)**

📲 **Установка:** скачай файл → открой в exteraGram / AyuGram (или импортируй через менеджер плагинов).

## 📁 Файлы в папке

```
LiveWallpaper/
  live_wallpaper.plugin
  LiveWallpaper.dex          # проверенная копия DEX (sha256 в plugin-integrity.json)
  README.md
  secure.md
  releases/
    v1.1/
      live_wallpaper_v1.1.plugin
      secure_1.1.md
    v1.2/
      live_wallpaper_v1.2.plugin   # архив — обновлять только при релизе (push)
      secure_1.2.md
      CHANGELOG.md
```

## 🎯 Назначение

Загружает нативный DEX-модуль с сервера и делегирует ему всю логику обоев. Python-часть — загрузчик, мост и UI установки.

## 🏗️ Архитектура

| Класс | Роль |
|-------|------|
| `LiveWallpaperPlugin` | 🎛️ Главный плагин |
| `WallpaperRunnableBridge` | 🌉 `Runnable`-мост Python ↔ DEX |
| `WallpaperInstallerSheet` | 📥 BottomSheet с прогрессом загрузки |

Нативный класс: `com.swagaplugins.plugin.wallpaper.LiveWallpaper`.

## 🔗 Хуки

| Хук | Описание |
|-----|----------|
| `on_plugin_load` | 🔄 Фоновый `_smart_init` — проверка/загрузка DEX, инъекция |
| `on_plugin_unload` | 🛑 Вызов `LiveWallpaper.unload()` из DEX |

**Нет** message/protocol hooks — вся логика в DEX.

## ⚙️ Настройки

| Ключ | Описание |
|------|----------|
| `dex_signature` | ETag + Content-Length для инвалидации кэша DEX |
| `active_dex_sha256` | Последний доверенный SHA256 DEX (после установки / подписанного manifest) |

`create_settings()` возвращает заглушку `Header("Загрузка нативного UI...")` — реальный UI внутри DEX.

## 🖥️ UI

- **WallpaperInstallerSheet** — BottomSheet: стикер, прогресс, статус «Подключение к серверу...»
- Нельзя закрыть свайпом до завершения загрузки
- Настройки обоев — в нативном модуле

## 🌐 Внешние зависимости

| Ресурс | URL / путь |
|--------|------------|
| DEX (remote) | `https://storage.yandexcloud.net/4plugins/EveryoneAskedForThis/LiveWallpaper.dex` |
| DEX (bundled) | `https://raw.githubusercontent.com/makarworld/awesome-telegram-plugins/refs/heads/main/LiveWallpaper/LiveWallpaper.dex` |
| Manifest + подпись (primary) | `plugin-integrity.json` + `.sig` на GitHub raw |
| Manifest + подпись (fallback) | `plugin-integrity.json` + `.sig` на Yandex `awesomeplugins` |
| Локальный DEX | `{app}/dex_modules/LiveWallpaper.dex` (chmod 444) |
| DEX opt | `{app}/dex_opt/` |
| Видео | Скачиваются по URL из DEX через `download_video()` |

Библиотеки: `requests`, `DexClassLoader`.

### Мост Python → DEX

`WallpaperRunnableBridge` обрабатывает команды из DEX:
- `log` — логирование
- `download` — фоновая загрузка видео на диск

## 🧮 Алгоритм `_smart_init` (v1.2+)

```
1. GET plugin-integrity.json + .sig (GitHub → YC)
2. RSA SHA256 verify подписи → если OK, trusted hash = manifest.dex_sha256
3. Иначе trusted hash = active_dex_sha256 (setting) → иначе APPROVED_DEX_SHA256 (вшит в .plugin)
4. HEAD remote DEX → нужно ли обновление
5. Скачать → sha256 == trusted hash → сохранить → active_dex_sha256
6. При каждом _inject_dex: sha256 локального кэша == trusted hash
7. DexClassLoader → LiveWallpaper.init()
```

### Модель доверия

| Источник хеша | Когда |
|---------------|-------|
| Подписанный manifest | Сеть есть, RSA-подпись валидна — **обновление хеша без нового .plugin** |
| `active_dex_sha256` | Offline после успешной установки |
| `APPROVED_DEX_SHA256` | Константа в `.plugin`, bootstrap при первом запуске |

Неподписанный manifest **игнорируется**.

Вшитый хеш: `167ae2d499f575e156b3aea44956844b332c5e885482e0ff7d707ceee18f8e77`  
Публичный ключ: [`keys/manifest_public.pem`](../keys/manifest_public.pem)

### Обновление DEX в форке

1. Проверить DEX, посчитать sha256
2. Обновить `dex_sha256` в [`plugin-integrity.json`](../plugin-integrity.json), push в `main`
3. CI подписывает (`MANIFEST_SIGNING_KEY`) → заливает json + sig в YC → коммитит `.sig`
4. Плагин v1.2+ подхватывает новый хеш автоматически

См. [`keys/README.md`](../keys/README.md) — настройка `MANIFEST_SIGNING_KEY` в GitHub Secrets.

### Ручная загрузка DEX

Кнопка **«Выбрать LiveWallpaper.dex с устройства»** — хеш сверяется с trusted hash (не с неподписанным manifest).

## 🔬 Анализ DEX-модуля (`LiveWallpaper.dex`)

Статический анализ строк и классов (без декомпиляции исходников). SHA256: `167ae2d4…8f8e77`.

### Классы

| Класс | Назначение |
|-------|------------|
| `LiveWallpaper` | Точка входа: `init()`, `unload()`, установка хуков |
| `LiveWallpaperSettingsFragment` | UI настроек обоев |
| `WallpaperPrefs` | SharedPreferences (`live_wallpaper_prefs`) |
| `WallpaperPlayer` | `MediaPlayer` + `TextureView`, воспроизведение видео |
| `WallpaperBlurController` | Живой блюр фона чата через `BlurredBackgroundSource` |

### Что делает модуль

1. **Хуки Telegram UI** (через `XposedBridge`):
   - `ChatActivity` — `createView`, `onPause`, `onResume`, `onDestroy`, `onActivityResult`
   - `LaunchActivity` — открытие настроек плагина
   - Скрывает стандартный фон чата (`hideStandardBackground`)

2. **Видео-обои в чате:**
   - Пользователь выбирает MP4 из галереи (`ACTION_GET_CONTENT`, `video/*`)
   - Файл копируется во внутреннее хранилище как `local_wallpaper.mp4`
   - `MediaPlayer` воспроизводит видео на `TextureView` в фоне чата
   - Пауза/возобновление при сворачивании чата

3. **Живой блюр:**
   - Подключается к `wallpaperBitmapProvider` / `navbarContentSourceWallpaper`
   - `WallpaperBlurController` обновляет размытие по кадрам видео

4. **Сброс:**
   - Кнопка «Сбросить оформление» — возврат к стандартным анимированным обоям Telegram

5. **Мост с Python:**
   - `download` — запрос загрузки видео по URL (исполняет Python `download_video()`)
   - `log` — логирование в Python

### Сеть и файлы

| Действие | Детали |
|----------|--------|
| Скачивание видео | По URL из DEX через Python-мост (`requests`) |
| Демо-видео по умолчанию | `github.com/sterepandopalcevsto/supreme-octo-palm-tree/.../uOPpbAEGb8mZFYRQ.mp4` |
| Локальные файлы | `local_wallpaper.mp4`, кэш в `getCacheDir()` / `getFilesDir()` |
| Обращения к контактам | Строка `contact_check` — проверка контакта (назначение уточняется без декомпиляции) |

### Настройки внутри DEX

| ID | Описание |
|----|----------|
| `ID_SELECT_WALLPAPER` | Выбрать MP4 из галереи |
| `ID_RESET_WALLPAPER` | Сбросить на стандартные обои |
| `ID_DEBUG_LOGGING` | Отладка плеера |

### Вывод по безопасности DEX

- **Нет** явных URL для отправки данных, токенов, SMS, звонков
- **Есть** method hooks в `ChatActivity` — типично для UI-оверлея, но расширяет поверхность атаки
- **Есть** загрузка произвольных видео по URL через Python-мост
- **Есть** доступ к файловой системе приложения (кэш, prefs)
- Рекомендация автора DEX: вертикальные MP4 без звука для производительности

## 🔐 Безопасность

| Риск | Уровень | Комментарий |
|------|---------|-------------|
| Remote DEX execution | 🔴 **критический** | SHA256 при download + при каждом inject; подписанный manifest |
| Подмена manifest | 🟡 средний | RSA SHA256withRSA; неподписанный manifest игнорируется |
| Произвольные URL | 🟠 высокий | DEX может запросить скачивание любого видео |
| Компрометация bucket | 🟠 высокий | Manifest дублируется на GitHub; доверие через подпись |
| Подмена локального DEX | 🟡 средний | Проверка sha256 перед каждым inject |

**Вывод:** v1.2 — вшитый `APPROVED_DEX_SHA256`, подпись manifest, проверка кэша при inject. Обновление хеша через подписанный `plugin-integrity.json` без релиза `.plugin`.

## 🛠️ Разработка

- Для отладки смотреть логи `[LiveWallpaper]` / `[WallpaperBridge]`.
- Без исходника DEX изменять поведение обоев из Python нельзя.
- При обновлении DEX: правка `plugin-integrity.json` → CI подпись → плагин v1.2+ подхватит хеш.
- Смена публичного ключа или отзыв bootstrap-хеша — новый релиз `.plugin`.
