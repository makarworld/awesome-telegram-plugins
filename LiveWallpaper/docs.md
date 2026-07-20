# LiveWallpaper (`live_wallpaper`)

> Живые (видео) обои в чатах вместо статичного фона.  
> Исходник: только `live_wallpaper.plugin` · Версия: **1.1** · Обновлено: 2026-07-20

## Метаданные

| Поле | Значение |
|------|----------|
| `__id__` | `live_wallpaper` |
| `__name__` | LiveWallpaper |
| `__version__` | 1.1 |
| `__author__` | @swagnonher |
| `__description__` | Живые обои в чатах, вместо скучных статичных |
| `__icon__` | Animasha26/22 |
| `__min_version__` | 11.12.0 |

## Файлы в папке

```
LiveWallpaper/
  live_wallpaper.plugin
  docs.md
  secure.md
  releases/
    v1.1/
      live_wallpaper_v1.1.plugin
      secure_1.1.md
```

## Назначение

Загружает нативный DEX-модуль с сервера и делегирует ему всю логику обоев. Python-часть — загрузчик, мост и UI установки.

## Архитектура

| Класс | Роль |
|-------|------|
| `LiveWallpaperPlugin` | Главный плагин |
| `WallpaperRunnableBridge` | `Runnable`-мост Python ↔ DEX |
| `WallpaperInstallerSheet` | BottomSheet с прогрессом загрузки |

Нативный класс: `com.swagaplugins.plugin.wallpaper.LiveWallpaper`.

## Хуки

| Хук | Описание |
|-----|----------|
| `on_plugin_load` | Фоновый `_smart_init` — проверка/загрузка DEX, инъекция |
| `on_plugin_unload` | Вызов `LiveWallpaper.unload()` из DEX |

**Нет** message/protocol hooks — вся логика в DEX.

## Настройки

| Ключ | Описание |
|------|----------|
| `dex_signature` | ETag + Content-Length для инвалидации кэша DEX |

`create_settings()` возвращает заглушку `Header("Загрузка нативного UI...")` — реальный UI внутри DEX.

## UI

- **WallpaperInstallerSheet** — BottomSheet: стикер, прогресс, статус «Подключение к серверу...»
- Нельзя закрыть свайпом до завершения загрузки
- Настройки обоев — в нативном модуле

## Внешние зависимости

| Ресурс | URL / путь |
|--------|------------|
| DEX | `https://storage.yandexcloud.net/4plugins/EveryoneAskedForThis/LiveWallpaper.dex` |
| Локальный DEX | `{app}/dex_modules/LiveWallpaper.dex` (chmod 444) |
| DEX opt | `{app}/dex_opt/` |
| Видео | Скачиваются по URL из DEX через `download_video()` |

Библиотеки: `requests`, `DexClassLoader`.

### Мост Python → DEX

`WallpaperRunnableBridge` обрабатывает команды из DEX:
- `log` — логирование
- `download` — фоновая загрузка видео на диск

## Алгоритм `_smart_init`

```
1. HEAD/GET DEX → ETag + Content-Length
2. Сравнить с dex_signature в настройках
3. Если изменился → скачать → сохранить → _inject_dex
4. Если совпадает → _inject_dex из кэша
5. DexClassLoader → LiveWallpaper.init(pyArgs, pyResult)
```

## Безопасность

| Риск | Уровень | Комментарий |
|------|---------|-------------|
| Remote DEX execution | **критический** | Загрузка и исполнение кода без проверки подписи |
| Произвольные URL | высокий | DEX может запросить скачивание любого видео |
| Компрометация bucket | высокий | Yandex Cloud — единая точка доверия |

**Вывод:** плагин доверяет удалённому DEX полностью. Любое изменение на сервере = произвольный код на устройстве.

## Разработка

- Для отладки смотреть логи `[LiveWallpaper]` / `[WallpaperBridge]`.
- Без исходника DEX изменять поведение обоев из Python нельзя.
- При обновлении DEX на сервере меняется `dex_signature` → перезагрузка у пользователей.
