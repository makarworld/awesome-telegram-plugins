# 🔍 Plugin Verifier

> Проверяет плагины на подозрительный код и показывает статус в списке.  
> 🏷️ Версия **2.4.8** · @JasonVurhyz

## 📥 Скачать

**[plugin_verifier.plugin](https://cdn.jsdelivr.net/gh/makarworld/awesome-telegram-plugins@main/PluginVerifier/plugin_verifier.plugin)** · **[исходник](https://github.com/makarworld/awesome-telegram-plugins/blob/main/PluginVerifier/plugin_verifier.plugin)**

📲 Скачай файл → открой в exteraGram / AyuGram.

## Что делает

- Сверяет плагины с whitelist по SHA256
- Предупреждает при установке непроверенного
- В списке плагинов — ✅ или 🔴
- Можно просмотреть код, SQLite и анализ DEX
- Помечает аккаунты из базы скамеров

## Как пользоваться

1. Включи плагин — статусы появятся в списке плагинов.
2. При установке нового плагина — читай предупреждение.
3. Тап по статусу — подробности.

## ⚠️ Парадокс

Плагин полезен для аудита, но сам содержит скрытый anti-tamper и тянет blacklist с Supabase. **Не модифицируй файл**, если не понимаешь последствий.

🔴 **Высокий риск** (скрытые механизмы + широкие привилегии), не «вредоносный» в обычном смысле.

📊 [secure.md](secure.md) · архив [v2.4.8](releases/v2.4.8/secure_2.4.8.md)

## Для разработчиков

Техническая документация: **[docs.md](docs.md)**
