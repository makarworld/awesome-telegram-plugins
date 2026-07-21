# 🛡️ WS-Bypass (`wsbypass`)

> 🔓 Обход блокировок Telegram через локальный SOCKS-прокси и WebSocket-туннель к KWS-провайдерам.  
> 📦 Исходник: только `wsbypass.plugin` · 🏷️ Версия: **3.0.5** · 📅 Обновлено: 2026-07-21

## 📋 Метаданные

| Поле | Значение |
|------|----------|
| `__id__` | `wsbypass` |
| `__name__` | WS-Bypass |
| `__version__` | 3.0.5 |
| `__author__` | @Th3Nek1t_projects |
| `__description__` | Обход блокировок Telegram |
| `__icon__` | ResistanceDog/24 |
| `__app_version__` | >=12.5.1 |
| `__sdk_version__` | >=1.4.0 |

## ⬇️ Скачать

[⬇ Скачать wsbypass.plugin](https://cdn.jsdelivr.net/gh/makarworld/awesome-telegram-plugins@main/WSBypass/wsbypass.plugin) · [👀 Код](https://github.com/makarworld/awesome-telegram-plugins/blob/main/WSBypass/wsbypass.plugin)

📲 **Установка:** скачай файл → открой в exteraGram / AyuGram (или импортируй через менеджер плагинов).

## 📁 Файлы в папке

```
WSBypass/
  wsbypass.plugin
  README.md
  secure.md
  releases/
    v3.0.5/
      wsbypass_v3.0.5.plugin
      secure_3.0.5.md
```

## 🎯 Назначение

Плагин поднимает локальный SOCKS-прокси на `127.0.0.1` 🏠, проксирует трафик Telegram через WebSocket-мост 🌉 к внешним KWS-серверам и автоматически включает этот прокси в настройках клиента ⚙️. Предназначен для работы Telegram при блокировках (в т.ч. в РФ 🇷🇺).

## 🏗️ Архитектура

| Компонент | Роль |
|-----------|------|
| `TgWsProxyPlugin` | 🎛️ Главный плагин: настройки, автозапуск, обновления |
| `TgWsCore` | 🔌 Локальный SOCKS-сервер, маршрутизация, пул WS-соединений |
| `_TgWsRawWebSocket` / `_TgWsWsPool` | 🔄 WebSocket-клиент и пул прогретых соединений |
| `_kws_*` | 🔑 Регистрация на KWS API, poll/credential, проверка подписки на канал |

## 🌍 Провайдеры

| Режим | API | Релеи | Примечание |
|-------|-----|-------|------------|
| `auto` | авто-выбор | — | ✅ рекомендуется |
| `nimarko` | `calls.nimarko.org` | `r1.nimarko.org` | ⚡ быстрый |
| `th3` | `kws.th3web.com` | `ws.th3web.com` | 🐢 медленный, trickle без подписки |

📢 Для **полной скорости** на провайдере Th3Nekit нужна подписка на канал `@th3nek1t_projects`. Без неё — режим «тонкого канала» 🐌 (достаточно, чтобы открыть Telegram и подписаться).

## 🪝 Хуки

| Хук | Описание |
|-----|----------|
| `ProxyListActivity$TextDetailProxyCell.setProxy` | 🏷️ Подпись локального прокси «Обход блокировок» |
| `ConnectionsManager.onProxyError` | ⚠️ Обработка ошибок прокси |
| `on_app_event` (START/RESUME) | 🔁 Перезапуск туннеля при возврате в приложение |

## ⚙️ Настройки

| Ключ | Описание |
|------|----------|
| `tgws_enabled` | 🟢 Включить туннель |
| `tgws_provider_mode` | 🌐 `auto` / `nimarko` / `th3` |
| `tgws_update_autocheck` | 🔄 Автопроверка обновлений раз в час |
| `advanced_enabled` | 🧰 Расширенные настройки (порт/хост SOCKS) |
| `local_socks_host` | 🏠 Хост локального прокси (по умолчанию `127.0.0.1`) |
| `local_socks_port` | 🔢 Порт локального прокси (по умолчанию `1443`) |
| `route_pref` | 🗺️ Сохранённое предпочтение маршрута (JSON) |
| `kws_ever_authed` / `kws_grace_until` | ⏳ Grace-период после успешной авторизации |
| `kws_cred_{provider}` | 💾 Кэш credential по провайдеру |

📍 Пункты меню в чате 💬 и боковом drawer ведут в настройки плагина.

## 🆙 Обновления

- 📄 Манифест: `https://th3web.com/wsbypass/version.json`
- 🔒 Доверенный хост загрузки: `th3web.com`
- ✅ Проверки: HTTPS, SHA256, Ed25519-подпись, сравнение версии в payload

## 🌐 Сеть

| Назначение | URL |
|------------|-----|
| KWS Nimarko | `https://calls.nimarko.org/api/v1/kws/*` |
| KWS Th3Nekit | `https://kws.th3web.com/api/v1/kws/*` |
| Обновления | `https://th3web.com/wsbypass/version.json` |
| WebSocket Origin | `https://web.telegram.org` |

## 🔐 Безопасность

**Уровень: 🟡 низкий–средний** — туннелирование через сторонние KWS-серверы и смена прокси; автообновление с `th3web.com` (SHA256 + Ed25519).

📊 Отчёт: [secure.md](secure.md) — ❔ Низкий риск · 📦 архив: [v3.0.5](releases/v3.0.5/secure_3.0.5.md)

## 📜 История

| Версия | Примечание |
|--------|------------|
| 3.0.5 | 🎉 Добавлен в репозиторий awesome-plugins |
