# WS-Bypass — Changelog v3.0.5

**Дата релиза:** 2026-07-21  
**Плагин:** `wsbypass` (WS-Bypass)  
**Автор:** [@Th3Nek1t_projects](https://t.me/th3nek1t_projects)  
**Канал автора:** [@th3nek1t_projects](https://t.me/th3nek1t_projects)  
**Минимальная версия клиента:** 12.5.1 (основная сборка) · 11.9.0+ (`wsbypass_old_version_fix.plugin`)

---

## Кратко

**WS-Bypass v3.0.5** — плагин обхода блокировок Telegram через локальный MTProto-прокси и WebSocket-туннель к KWS-серверам. Публикация в каталоге awesome-plugins.

---

## ✨ Возможности

### Туннель и прокси

- Локальный SOCKS/MTProto-прокси на `127.0.0.1:1443` (настраивается).
- Автоматическое включение прокси в клиенте Telegram.
- WebSocket-мост: `Telegram → локальный прокси → KWS-релей → DC Telegram`.
- Origin WebSocket: `https://web.telegram.org`.

### Провайдеры KWS

| Режим | API | Релеи |
|-------|-----|-------|
| `auto` | автовыбор | — |
| `nimarko` | `calls.nimarko.org` | `r1.nimarko.org` |
| `th3` | `kws.th3web.com` | `ws.th3web.com` |

### Канал автора и скорость

- Для **полной скорости** на провайдере Th3Nekit нужна подписка на канал **[@th3nek1t_projects](https://t.me/th3nek1t_projects)**.
- Без подписки — медленный (trickle) режим: хватает, чтобы зайти в Telegram и подписаться.
- Кнопка «Подписаться на канал» и «Канал автора» в настройках плагина.

### Обновления

- Манифест: `https://th3web.com/wsbypass/version.json`.
- Проверка: HTTPS, SHA256, подпись **Ed25519**.
- Автопроверка и ручная установка из настроек.

### Сборки

| Файл | `__app_version__` |
|------|-------------------|
| `wsbypass.plugin` | `>=12.5.1` |
| `wsbypass_old_version_fix.plugin` | `>=11.9.0` |

Одинаковая логика, различается только требование к версии клиента.

---

## 🔧 Технические детали

- Класс: `TgWsProxyPlugin` + `TgWsCore`.
- KWS API: register, poll, credential (`X-Cred` HMAC).
- Криптография: AES-CTR, Ed25519 для обновлений.
- Хуки: `ProxyListActivity.setProxy`, `ConnectionsManager.onProxyError`, `on_app_event`.

---

## ⚠️ Приватность

| Видно оператору KWS | Не видно (при штатном MTProto) |
|---------------------|--------------------------------|
| Telegram ID, IP, объём, время онлайн | Содержимое переписки |

Трафик идёт через сторонние серверы — **не VPN**.

---

## 📦 Файлы релиза

```
WSBypass/releases/v3.0.5/
  wsbypass_v3.0.5.plugin
  wsbypass_old_version_fix.plugin
  secure_3.0.5.md
  CHANGELOG.md
```

---

## ✅ Безопасность

По отчёту Pluggy Bot ([secure_3.0.5.md](./secure_3.0.5.md)): **❔ Низкий риск**.

- Нет вредоносного кода по статическому анализу.
- Риски: туннель через KWS, метаданные, SSL fallback `CERT_NONE`, DNS-кэш.

---

## 🔗 Ссылки

- **Канал автора:** https://t.me/th3nek1t_projects
- **Скачать:** [wsbypass.plugin](https://cdn.jsdelivr.net/gh/makarworld/awesome-telegram-plugins@main/WSBypass/wsbypass.plugin)
