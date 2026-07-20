# Tomato bom (`tomato_bom`)

> Развлекательный плагин: кидает помидоры поверх UI, зажатие = пулемётный обстрел.  
> Исходник: только `tomato_bom.plugin` · Версия: **1.2.8** · Обновлено: 2026-07-20

## Метаданные

| Поле | Значение |
|------|----------|
| `__id__` | `tomato_bom` |
| `__name__` | Tomato bom |
| `__version__` | 1.2.8 |
| `__author__` | Windukk |
| `__description__` | Кидает помидоры. Зажатие = пулеметный обстрел. |
| `__icon__` | не указан |
| `__min_version__` | не указан |

## Скачать

[Скачать tomato_bom.plugin](https://raw.githubusercontent.com/makarworld/awesome-telegram-plugins/refs/heads/main/TomatoBom/tomato_bom.plugin)

Установка: скачай файл → открой в exteraGram / AyuGram (или импортируй через менеджер плагинов).

## Файлы в папке

```
TomatoBom/
  tomato_bom.plugin
  README.md
  releases/
    v1.2.8/
      tomato_bom_v1.2.8.plugin
      secure_1.2.8.md
```

## Назначение

Fullscreen overlay поверх Activity: тап — помидор, удержание — автострельба. Звук «splat» при попадании. Выход — двойной тап.

## Архитектура

| Класс | Роль |
|-------|------|
| `Plugin` | Главный плагин (`BasePlugin`) |
| `FullScreenTouchListener` | `OnTouchListener` для overlay |

## Хуки

| Хук | Описание |
|-----|----------|
| `on_plugin_load` | Menu items + фоновая загрузка ассетов |

**Нет** message/protocol hooks.

## Настройки

| Ключ | Default | Описание |
|------|---------|----------|
| `tomato_size` | 2000 | Размер GIF в px |
| `sound_volume` | 100 | Громкость 0–100% |
| `fire_interval` | 100 | Интервал автострельбы (мс) |

Дополнительно: кнопка «Мой блог» → `ChatActivity` chat_id `1577053969`.

## Меню

| Тип | Пункт | item_id |
|-----|-------|---------|
| `CHAT_ACTION_MENU` | Бросить помидор | `start_tomato_blocker_chat` |
| `DRAWER_MENU` | Включить обстрел | — |
| `PROFILE_ACTION_MENU` | Обстрелять профиль | (если доступен) |

## Алгоритм

```
1. on_plugin_load → download GIF + MP3 в фоне
2. Menu click → создать FrameLayout overlay на Activity
3. FullScreenTouchListener:
   - ACTION_DOWN → spawn_tomato + start auto loop
   - ACTION_MOVE → обновить координаты
   - ACTION_UP → stop auto loop
   - double tap (<0.3s) → close_overlay
4. spawn_tomato:
   - ImageDecoder/BitmapFactory → GIF frame
   - fade-in анимация
   - SoundPool splat (throttle 50ms)
5. auto loop: random offset ±100px, delay = fire_interval
```

## Внешние зависимости

| Ассет | URL |
|-------|-----|
| GIF | `https://gitflic.ru/project/fdijdkjl/kjhkjh/blob/raw?file=ezgif-4d2382b4323e220f.gif&...` |
| MP3 | `https://gitflic.ru/project/fdijdkjl/kjhkjh/blob/raw?file=c5855692202fecf58526e46da71c34d3.mp3&...` |

Кэш: `{temp}/tomato_assets/tomato.gif`, `splat.mp3`.

Библиотеки: `requests`, `SoundPool`, `ImageDecoder`/`BitmapFactory`.

## Хранение данных

- Только temp-кэш ассетов
- Настройки через plugin settings API
- Runtime: `overlay_view`, `sound_pool`, `assets_ready`

## Безопасность

| Риск | Уровень | Комментарий |
|------|---------|-------------|
| Загрузка бинарников с gitflic | средний | Без checksum-верификации |
| Fullscreen overlay | средний | Перехватывает все touch до двойного тапа |
| RCE | низкий | Только GIF/MP3, без исполняемого кода |

## Разработка

- Overlay блокирует UI — всегда нужен явный выход (double tap).
- `assets_ready` — не показывать overlay до загрузки.
- При смене URL ассетов — очистить `{temp}/tomato_assets/`.
