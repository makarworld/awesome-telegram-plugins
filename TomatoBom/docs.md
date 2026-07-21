# Tomato bom — техническая документация

> ID: `tomato_bom` · v1.2.8 · исходник: `tomato_bom.plugin`

Пользовательская документация: [README.md](README.md)

## Метаданные

| Поле | Значение |
|------|----------|
| `__id__` | `tomato_bom` |
| `__version__` | 1.2.8 |
| `__author__` | Windukk |

## Архитектура

| Класс | Роль |
|-------|------|
| `Plugin` | Главный плагин |
| `FullScreenTouchListener` | `OnTouchListener` для overlay |

## Хуки

- `on_plugin_load` — menu items + фоновая загрузка ассетов
- Нет message/protocol hooks

## Настройки

| Ключ | Default | Описание |
|------|---------|----------|
| `tomato_size` | 2000 | Размер GIF (px) |
| `sound_volume` | 100 | Громкость 0–100% |
| `fire_interval` | 100 | Интервал автострельбы (мс) |

## Меню

| Тип | item_id |
|-----|---------|
| `CHAT_ACTION_MENU` | `start_tomato_blocker_chat` |
| `DRAWER_MENU` | Включить обстрел |
| `PROFILE_ACTION_MENU` | Обстрелять профиль |

## Алгоритм

```
on_plugin_load → download GIF + MP3
Menu click → FrameLayout overlay на Activity
FullScreenTouchListener: DOWN=spawn+auto, UP=stop, double tap=close
spawn_tomato: GIF frame + SoundPool splat (throttle 50ms)
```

## Внешние зависимости

| Ассет | URL |
|-------|-----|
| GIF | `gitflic.ru/project/fdijdkjl/kjhkjh/.../ezgif-....gif` |
| MP3 | `gitflic.ru/project/fdijdkjl/kjhkjh/.../c585569....mp3` |

Кэш: `{temp}/tomato_assets/`. Библиотеки: `requests`, `SoundPool`, `ImageDecoder`.

## Разработка

- Overlay блокирует UI — выход только double tap
- Не показывать overlay до `assets_ready`
- При смене URL — очистить `{temp}/tomato_assets/`
