# 🛒 Kangel Plugins Manager

> Магазин плагинов для exteraGram: каталог, установка и обновление в один тап.  
> 🏷️ Версия **1.4.3** · @ArThirtyFour, @KangelPlugins

## 📥 Скачать

**[kangel_plugins_manager.plugin](https://cdn.jsdelivr.net/gh/makarworld/awesome-telegram-plugins@main/KangelPluginsManager/kangel_plugins_manager.plugin)** · **[исходник](https://github.com/makarworld/awesome-telegram-plugins/blob/main/KangelPluginsManager/kangel_plugins_manager.plugin)**

Архив релиза: **[v1.4.3](releases/v1.4.3/kangel_plugins_manager_v1.4.3.plugin)**

📲 Скачай файл → открой в exteraGram / AyuGram. Нужен клиент **12.5.1+**.

При установке клиент подтянет PyPI-пакет `kangelpluginsmanager==1.4.3` (основной код библиотеки).

## Что делает

- Каталог плагинов с GitHub
- Установка и обновление `.plugin`
- Поиск `@kpm` прямо в чате
- Наборы плагинов (builds)
- Счётчик плагинов на экране (pill)

## Как пользоваться

1. Открой **Plugin Manager** в боковом меню.
2. Выбери плагин → установи или обнови.
3. В чате набери `@kpm` для поиска.
4. Телеметрию можно отключить в настройках (`telemetry_enabled`).

## ⚠️ Важно

Основная функция — **установка кода из интернета**. Устанавливай только плагины от доверенных авторов.

С v1.4.3 логика вынесена в PyPI-пакет [kangelpluginsmanager](https://pypi.org/project/KangelPluginsManager/) — при аудите смотри и `.plugin`, и библиотеку ([исходники](https://github.com/KangelPlugins/PluginManager)).

🟠 **Высокий риск** (по природе магазина, не баг).

📊 [secure.md](secure.md) — ❔ от Pluggy + **⚠️ Осторожно** с учётом PyPI · архив [v1.4.3](releases/v1.4.3/secure_1.4.3.md) · [v1.3.2](releases/v1.3.2/secure_1.3.2.md)

## Для разработчиков

Техническая документация: **[docs.md](docs.md)**
