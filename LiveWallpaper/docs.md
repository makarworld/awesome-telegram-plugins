# LiveWallpaper — техническая документация

> ID: `live_wallpaper` · v1.2 · исходник: `live_wallpaper.plugin`

Пользовательская документация: [README.md](README.md)

## Метаданные

| Поле | Значение |
|------|----------|
| `__id__` | `live_wallpaper` |
| `__version__` | 1.2 |
| `__author__` | @swagnonher |
| `__min_version__` | 11.12.0 |

## Архитектура

| Класс | Роль |
|-------|------|
| `LiveWallpaperPlugin` | Загрузчик, мост, UI установки |
| `WallpaperRunnableBridge` | Runnable Python ↔ DEX |
| `WallpaperInstallerSheet` | BottomSheet с прогрессом |

Нативный класс: `com.swagaplugins.plugin.wallpaper.LiveWallpaper`. Вся логика обоев — в DEX.

## Хуки

| Хук | Описание |
|-----|----------|
| `on_plugin_load` | `_smart_init` — загрузка/инъекция DEX |
| `on_plugin_unload` | `LiveWallpaper.unload()` |

## Настройки

| Ключ | Описание |
|------|----------|
| `dex_signature` | ETag + Content-Length для инвалидации кэша |
| `active_dex_sha256` | Последний доверенный SHA256 |

## Алгоритм `_smart_init` (v1.2+)

```
1. GET plugin-integrity.json + .sig (GitHub → YC)
2. RSA verify → trusted hash = manifest.dex_sha256
3. Иначе: active_dex_sha256 → APPROVED_DEX_SHA256 (вшит)
4. HEAD remote DEX → нужно ли обновление
5. Download → sha256 == trusted → сохранить
6. При inject: sha256 кэша == trusted
7. DexClassLoader → LiveWallpaper.init()
```

### Модель доверия

| Источник | Когда |
|----------|-------|
| Подписанный manifest | RSA валидна — обновление хеша без нового .plugin |
| `active_dex_sha256` | Offline после установки |
| `APPROVED_DEX_SHA256` | Bootstrap при первом запуске |

Вшитый хеш: `167ae2d499f575e156b3aea44956844b332c5e885482e0ff7d707ceee18f8e77`  
Ключ: [`keys/manifest_public.pem`](../keys/manifest_public.pem)

## Внешние зависимости

| Ресурс | URL |
|--------|-----|
| DEX remote | `storage.yandexcloud.net/4plugins/.../LiveWallpaper.dex` |
| DEX bundled | GitHub raw `LiveWallpaper/LiveWallpaper.dex` |
| Manifest | `plugin-integrity.json` + `.sig` |
| Локально | `{app}/dex_modules/LiveWallpaper.dex` (chmod 444) |

## Мост Python → DEX

- `log` — логирование
- `download` — загрузка видео (`download_video()`)

## Анализ DEX (статический)

| Класс | Назначение |
|-------|------------|
| `LiveWallpaper` | init/unload, хуки |
| `WallpaperSettingsFragment` | UI настроек |
| `WallpaperPlayer` | MediaPlayer + TextureView |
| `WallpaperBlurController` | Блюр фона чата |

Хуки: `ChatActivity`, `LaunchActivity`. Локально: `local_wallpaper.mp4`.

## Обновление DEX в форке

1. SHA256 DEX → `plugin-integrity.json`
2. CI подписывает (`MANIFEST_SIGNING_KEY`) → YC + `.sig`
3. Плагин v1.2+ подхватывает автоматически

## Разработка

- Логи: `[LiveWallpaper]`, `[WallpaperBridge]`
- Без исходника DEX — поведение обоев из Python не меняется
- Смена bootstrap-хеша — новый релиз `.plugin`

## Changelog

| Версия | Примечание |
|--------|------------|
| 1.2 | SHA256 DEX, подписанный manifest, fallback, ручной импорт — [CHANGELOG](releases/v1.2/CHANGELOG.md) |
| 1.1 | Первая версия с remote DEX |

## Файлы

```
LiveWallpaper/
  live_wallpaper.plugin
  README.md
  docs.md
  secure.md
  releases/v1.2/
  releases/v1.1/
```
