# WS-Bypass — техническая документация

> ID: `wsbypass` · v3.1.4 · исходник: `wsbypass.plugin`

Пользовательская документация: [README.md](README.md)

## Метаданные

| Поле | Значение |
|------|----------|
| `__id__` | `wsbypass` |
| `__version__` | 3.1.4 |
| `__author__` | @Th3Nek1t_projects |
| `__app_version__` | >=12.5.1 (основной `wsbypass.plugin`) |
| `__sdk_version__` | >=1.4.0 |

### Сборка для старых клиентов

| Файл | `__app_version__` | Назначение |
|------|-------------------|------------|
| `wsbypass.plugin` | `>=12.5.1` | Основная сборка в корне папки |
| `releases/v3.0.5/wsbypass_old_version_fix.plugin` | `>=11.9.0` | Код v3.0.5, пониженное требование к версии клиента |

Отличие — только метаданные `__app_version__`; для пользователей 11.9.0–12.5.0 ссылка в [README.md](README.md).

## Архитектура

```
Telegram → локальный MTProto-прокси (127.0.0.1) → перешифровка → WebSocket → KWS-релей → DC Telegram
```

| Компонент | Роль |
|-----------|------|
| `TgWsProxyPlugin` | Настройки, автозапуск, обновления |
| `TgWsCore` | Локальный SOCKS, маршрутизация, пул WS |
| `_TgWsRawWebSocket` / `_TgWsWsPool` | WebSocket-клиент и пул |
| `_kws_*` | Регистрация KWS API, poll/credential, LTE access check |

## Провайдеры

| Режим | API | Релеи | Trickle | Примечание |
|-------|-----|-------|---------|------------|
| `auto` | авто | — | — | Рекомендуется |
| `nimarko` | `calls.nimarko.org` | `r1.nimarko.org` | нет | Быстрый |
| `th3` | `kws.th3web.com` | `ws.th3web.com` | да | Резервный; полная скорость — подписка на канал |
| `lte` | `kwszh.th3web.com` | `wszh.th3web.com` | нет | LeanVPN Premium; подписка LTE/Ultimate в @VPN_Lean_bot |

Провайдеры — взаимоисключающие переключатели (`tgws_prov_{mode}`). С v3.1.4 переключатель `lte` виден только после подтверждения доступа (`tgws_lte_entitled`).

## Хуки

| Хук | Описание |
|-----|----------|
| `ProxyListActivity$TextDetailProxyCell.setProxy` | Подпись «Обход блокировок» |
| `ConnectionsManager.onProxyError` | Ошибки прокси |
| `on_app_event` (START/RESUME) | Перезапуск туннеля |

## Настройки (ключи)

| Ключ | Описание |
|------|----------|
| `tgws_enabled` | Включить туннель |
| `tgws_provider_mode` | `auto` / `nimarko` / `th3` / `lte` |
| `tgws_prov_{mode}` | Состояние переключателя провайдера |
| `tgws_lte_entitled` | Подтверждённый доступ к LeanVPN Premium |
| `tgws_lte_account` | Индекс аккаунта с активной подпиской LTE/Ultimate |
| `tgws_update_autocheck` | Автопроверка обновлений |
| `advanced_enabled` | Расширенные (порт/хост SOCKS) |
| `local_socks_host` | По умолчанию `127.0.0.1` |
| `local_socks_port` | По умолчанию `1443` |
| `route_pref` | JSON предпочтений маршрута |
| `kws_ever_authed` / `kws_grace_until` | Grace-период |
| `kws_cred_{provider}` | Кэш credential |

## Криптография

- MTProto handshake: `AES-CTR`, ключи из `secret` (16 байт, локально)
- `_tgws_build_crypto_ctx`: `clt_dec/enc`, `tg_enc/dec` для моста client ↔ relay
- `relay_init` генерируется локально, отправляется на WS-релей

## KWS API

| Endpoint | Назначение |
|----------|------------|
| `/api/v1/kws/register?user_id=` | Регистрация |
| `/api/v1/kws/poll` | Poll кода |
| `/api/v1/kws/credential` | Получение `X-Cred` |
| WebSocket | `GET /apiws?dc=N`, Origin: `https://web.telegram.org` |

Заголовок: `X-Cred: {expiry}:{uid}:{hmac}`.

LTE-проверка (v3.1.4): перебор аккаунтов `0..MAX_ACCOUNT_COUNT-1`, inline verification к `@VPN_Lean_bot`, rate-limit 60 с.

## Обновления

- Манифест: `https://th3web.com/wsbypass/version.json`
- Проверки: HTTPS, SHA256, Ed25519

## Сеть

| URL | Назначение |
|-----|------------|
| `calls.nimarko.org/api/v1/kws/*` | KWS Nimarko |
| `kws.th3web.com/api/v1/kws/*` | KWS Th3Nekit |
| `kwszh.th3web.com/api/v1/kws/*` | KWS LeanVPN Premium (CH) |
| `wszh.th3web.com` | WebSocket-релей LeanVPN |
| `th3web.com/wsbypass/version.json` | Обновления |

## Безопасность (техническая)

KWS видит зашифрованный MTProto-трафик и метаданные (UID, DC, объём, IP). Содержимое чатов — только при компрометации MTProto.

SSL fallback: при ошибке верификации сертификата — `CERT_NONE`.

Вердикт Pluggy v3.1.4: **⚠️ Осторожно** ([secure.md](secure.md)).

## История

| Версия | Примечание |
|--------|------------|
| 3.1.4 | Проверка LTE по всем аккаунтам, UI «Переключение…» — [CHANGELOG](releases/v3.1.4/CHANGELOG.md) |
| 3.1.2 | LeanVPN Premium, переключатели провайдеров — [CHANGELOG](releases/v3.1.2/CHANGELOG.md) |
| 3.0.5 | Публикация в awesome-plugins — [CHANGELOG](releases/v3.0.5/CHANGELOG.md) |
