# 🛡️ WS-Bypass

> Помогает открыть Telegram при блокировках через локальный прокси и WebSocket-туннель.  
> 🏷️ Версия **3.0.5** · @Th3Nek1t_projects

## 📥 Скачать

### Обычная версия (exteraGram / AyuGram **12.5.1+**)

**[wsbypass.plugin](https://cdn.jsdelivr.net/gh/makarworld/awesome-telegram-plugins@main/WSBypass/wsbypass.plugin)** · **[код на GitHub](https://github.com/makarworld/awesome-telegram-plugins/blob/main/WSBypass/wsbypass.plugin)**

### Для старых версий клиента (**11.9.0 – 12.5.0**)

Если основной файл не ставится или плагин не запускается — используй сборку с пониженным `__app_version__` (та же логика, проверено на старых клиентах):

**[wsbypass_old_version_fix.plugin](https://cdn.jsdelivr.net/gh/makarworld/awesome-telegram-plugins@main/WSBypass/releases/v3.0.5/wsbypass_old_version_fix.plugin)** · **[код на GitHub](https://github.com/makarworld/awesome-telegram-plugins/blob/main/WSBypass/releases/v3.0.5/wsbypass_old_version_fix.plugin)**

📲 Скачай нужный файл → открой в exteraGram / AyuGram.

## Что делает

Поднимает локальный прокси на телефоне и направляет трафик Telegram через внешние серверы обхода. Прокси в клиенте включается автоматически.

## Как пользоваться

1. Включи плагин и туннель в его настройках.
2. Режим провайдера: **auto** (рекомендуется) или выбери вручную.
3. Для полной скорости на провайдере Th3Nekit подпишись на [@th3nek1t_projects](https://t.me/th3nek1t_projects). Без подписки — медленный режим (хватит, чтобы зайти и подписаться).

## Настройки

- Вкл/выкл туннель
- Провайдер: auto / Nimarko / Th3Nekit
- Автопроверка обновлений
- Расширенные: порт и хост локального прокси (по умолчанию `127.0.0.1:1443`)

## ⚠️ Важно о приватности

Трафик идёт через **сторонние серверы** (`r1.nimarko.org`, `ws.th3web.com`). Это не VPN.

| | |
|--|--|
| **Переписку читать не должны** | Трафик Telegram зашифрован MTProto |
| **Метаданные видят** | Ваш Telegram ID, объём трафика, когда онлайн, IP |
| **Подходит** | Если нужен обход блокировок и вы доверяете оператору KWS |
| **Не подходит** | Если важна анонимность |

🟡 **Низкий–средний риск** · [secure.md](secure.md)

## Для разработчиков

Техническая документация: **[docs.md](docs.md)**
