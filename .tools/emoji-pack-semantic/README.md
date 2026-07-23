# Emoji Pack Semantic

Локальный инструмент: скачивает custom emoji pack через [Telegram Bot API](https://core.telegram.org/bots/api#getstickerset), собирает **одну PNG-сетку** для одного vision-запроса к ИИ и сливает семантические метки в `semantic_map.json` с `document_id` для плагинов (exteraGram / CuteMessages).

## Безопасность токена

- Токен бота храните **только** в локальном `.env` (см. `.env.example`).
- **Не коммитьте** `.env` и `output/`.
- Если токен попадал в чат — отзовите в [@BotFather](https://t.me/BotFather) → `/revoke` и создайте новый.

## Установка

```powershell
cd .tools/emoji-pack-semantic
pip install -r requirements.txt
copy .env.example .env
# Вставьте TELEGRAM_BOT_TOKEN в .env
```

## Составные паки (combo)

Паки вроде [лесная тропа 2](https://t.me/addemoji/juliet_diary_lesnaya_tropa_2_by_TgEmojiBot): эмодзи **ставят вплотную** и собирают цветы, лианы, крылья, домики. Fallback Unicode часто один (⭐️) — смысл только из картинки.

Используйте **`prompt_vision_combo.md`** вместо `prompt_vision.md`.

Дополнительные поля в `labels_by_index.json`:

| Поле | Назначение |
|------|------------|
| `usage_mode` | `combo_required` / `combo_optional` / `solo` |
| `combo_group` | id сборки |
| `combo_role` | `left`, `right`, `segment_N`, `left_wing`… |
| `connects` | стороны стыковки |
| `combo_with` | индексы соседей |
| `combos[]` | готовые мотивы с `layout`, `rows`, `render`, `complete`, `glue` |

Поля combo: `layout`, `rows`, `render`, `complete`, `glue`, `visual_short`, `width_risk`, `allows_text_between`, `left_wing`/`right_wing`, `scenes[]`, `by_tag`, `hint_emoji`.

Правила для агента: [`agent_rules_composite.md`](agent_rules_composite.md) — копируются в `semantic_map.json` как `agent_rules`.

Валидация: `python validate_map.py --pack <pack>`.

**Для агента** (после merge): `agent_catalog.md` + `agent_index.json` — компактный слой без 200× полного emoji. Схема: `semantic_map.schema.json`.

`semantic_map.json` для таких паков содержит `"pack_type": "composite"` и массив `combos`.

Пример:

```powershell
python fetch_pack.py --url https://t.me/addemoji/juliet_diary_lesnaya_tropa_2_by_TgEmojiBot
python build_sheet.py --pack juliet_diary_lesnaya_tropa_2_by_TgEmojiBot --cell 96 --cols 8
python generate_juliet_labels.py
python merge_labels.py --pack juliet_diary_lesnaya_tropa_2_by_TgEmojiBot
python validate_map.py --pack juliet_diary_lesnaya_tropa_2_by_TgEmojiBot
```

## Полный флоу (одиночные паки)

Пример пака: [t.me/addemoji/epicdepartmenthopeful_by_fStikBot](https://t.me/addemoji/epicdepartmenthopeful_by_fStikBot)

### 1. Скачать пак

```powershell
python fetch_pack.py --name epicdepartmenthopeful_by_fStikBot
# или
python fetch_pack.py --url https://t.me/addemoji/epicdepartmenthopeful_by_fStikBot
```

Результат: `output/<pack>/pack_raw.json`, `output/<pack>/assets/*`.

Для анимированных `.tgs` / видео берётся **thumbnail** из API (статичный кадр).

### 2. Собрать сетку для vision

```powershell
python build_sheet.py --pack epicdepartmenthopeful_by_fStikBot --cell 112 --cols 10
```

Результат:

| Файл | Назначение |
|------|------------|
| `pack_sheet.png` | Одно изображение — отправить в Cursor / ChatGPT / Claude Vision |
| `gallery.html` | Проверка в браузере (zoom, номера, полные id) |
| `sheet_meta.json` | Параметры сборки |

### 3. Vision-запрос к ИИ

1. Откройте `prompt_vision.md`.
2. Прикрепите `output/<pack>/pack_sheet.png`.
3. Вставьте промпт, укажите имя пака в поле `pack`.
4. Сохраните ответ как `output/<pack>/labels_by_index.json`.

### 4. Финальная карта

```powershell
python merge_labels.py --pack epicdepartmenthopeful_by_fStikBot
```

Результат: `output/<pack>/semantic_map.json`:

```json
{
  "pack": "epicdepartmenthopeful_by_fStikBot",
  "title": "...",
  "emojis": [
    {
      "document_id": 5408846744727334338,
      "index": 1,
      "fallback_unicode": "🤡",
      "tags": ["грусть", "мем"],
      "description": "...",
      "description_emoji": "😢💧😞",
      "mood": "sad",
      "use_when": ["..."]
    }
  ]
}
```

## Как использовать semantic_map.json

**Агенту** — не весь `semantic_map.json` (~300 KB), а:

1. `agent_catalog.md` — правила, scenes, combos (Markdown, ~3–15 KB)
2. `agent_index.json` — `by_tag`, `document_ids` по combo, `solo_by_index`
3. `semantic_map.json` — только если нужен один конкретный emoji

Генерация (автоматически после `merge_labels.py`):

```powershell
python export_agent_catalog.py --pack juliet_diary_lesnaya_tropa_2_by_TgEmojiBot
```

**Плагин / код:**

1. Контекст для ИИ: «нужен грустный мем» → поиск по `tags` / `mood` / `by_tag` → `document_id`.
2. В будущем — подстановка в `MessageEntityCustomEmoji` (CuteMessages и др.) вместо жёсткой Unicode-карты.

**Поиск по смыслу (логика, не в v1):**

- Запрос: настроение `sad` + контекст «жалоба».
- Фильтр по `mood`, `tags`, `use_when`.
- Выбор `document_id` для вставки в сообщение.

## Что не входит в v1

- Интеграция в CuteMessages
- Автовызов vision API из скрипта
- Парсинг `t.me/addemoji` без Bot API
- Полный рендер Lottie (`.tgs`)

## Структура

```
.tools/emoji-pack-semantic/
  fetch_pack.py      # getStickerSet + getFile
  build_sheet.py     # pack_sheet.png + gallery.html
  merge_labels.py    # labels + pack_raw → semantic_map.json + agent_*
  export_agent_catalog.py  # agent_catalog.md + agent_index.json
  validate_map.py    # инварианты v2
  semantic_map.schema.json # JSON Schema v2
  item_builder.py    # build_items + by_tag
  combo_schema.py    # нормализация combos
  generate_juliet_labels.py
  batch_analyze.py   # batch по pack_profiles/*.json
  prompt_vision.md
  prompt_vision_combo.md
  common.py
  output/            # gitignored
```
