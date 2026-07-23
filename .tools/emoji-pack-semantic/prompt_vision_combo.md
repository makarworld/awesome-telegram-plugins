# Промпт для vision-анализа **составного** emoji-пака

Паки вроде [лесная тропа 2](https://t.me/addemoji/juliet_diary_lesnaya_tropa_2_by_TgEmojiBot): эмодзи **не самодостаточны** — их ставят **вплотную** (слева-направо, иногда сверху-вниз), чтобы собрать цветок, лиану, горшок, крылья, домик и т.д.

Прикрепите **`pack_sheet.png`** и вставьте текст ниже.

Для составных паков (juliet и аналоги) щит собирайте с **`--cols 8`**: одна строка сетки = один горизонтальный ряд в сообщении, соседние ячейки — кандидаты на склейку.

---

Ты видишь сетку custom emoji. У каждой ячейки номер `#001`… и короткий `document_id`.

**Задача:**

1. Для **каждого** номера — что это за **фрагмент** (левая половина цветка, сегмент лианы, блик, горшок…).
2. Для **наборов**, которые собираются вместе, — отдельные записи в `combos`.

Верни **только валидный JSON** (без markdown):

```json
{
  "pack": "SHORT_NAME",
  "pack_type": "composite",
  "items": [
    {
      "index": 12,
      "tags": ["цветок", "розовый", "левая половина", "природа"],
      "description": "Левая половина розового цветка; без #013 картинка неполная.",
      "description_emoji": "🌸🌿💗",
      "mood": "wholesome",
      "use_when": ["декор сообщения", "весеннее настроение"],
      "usage_mode": "combo_required",
      "combo_group": "pink_flower_1",
      "combo_role": "left",
      "connects": ["right"],
      "combo_with": [13]
    }
  ],
  "combos": [
    {
      "id": "clover_full",
      "name": "Четырёхлистный клевер",
      "layout": "grid",
      "rows": [[179, 180], [187, 188]],
      "parts": ["clover_row_top", "clover_row_bottom"],
      "complete": true,
      "glue": "none",
      "render": "rows_join_newline",
      "description": "Клевер 2×2: верх #179+#180, низ #187+#188.",
      "description_emoji": "🍀💚✨",
      "tags": ["клевер", "удача", "2x2"],
      "mood": "happy",
      "use_when": ["талисман", "весна"],
      "do_not_mix_with": ["heart_apple_row"]
    },
    {
      "id": "sparkle_pink_35",
      "layout": "solo",
      "indices": [35],
      "glue": false,
      "max_per_message": 2,
      "do_not_mix_with": ["sparkle_*"],
      "complete": true,
      "render": "single"
    }
  ]
}
```

**layout:** `solo` | `horizontal` | `sandwich` | `grid` | `stack`

| layout | render (по умолчанию) | как вставлять |
|--------|----------------------|---------------|
| solo | single | один id; `glue: false` |
| horizontal | join_no_space | `order` в одну строку без пробелов |
| sandwich | sandwich_text_middle | left + текст + right |
| grid | rows_join_newline | `rows`: каждая строка join, между строками `\n` |
| stack | join_newline | `order` сверху вниз через `\n` |

**Поля combo (v2):**

| Поле | Описание |
|------|----------|
| `complete` | `true` — готовый объект; `false` — только часть (нужен parent) |
| `visual_short` | 3–8 слов для поиска («тёмный мох + фиолетовые бутоны») |
| `width_risk` | `low` / `medium` / `high` — авто по ширине |
| `placement` | `block` для complete |
| `alone_on_line` | complete-блок на своих строках |
| `allows_text_between` | для sandwich — дыра под текст |
| `do_not_insert_text` | для horizontal — без текста между кусками |
| `left_wing` / `right_wing` | для sandwich (авто из order) |
| `rows` | для `grid` — **обязательно** `[[r1c1,r1c2],[r2c1,r2c2]]` |
| `parent` / `parts` | неполные фрагменты |
| `accent_only` | solo-блики, не для коллажа |

**scenes[]** — готовые рецепты из named blocks:

```json
"scenes": [{
  "id": "morning_path",
  "blocks": ["vine_border_top", "bonsai", "thorn_border"],
  "between_blocks": "blank_line",
  "description": "Доброе утро"
}]
```

**hint_emoji** на item — смысловой поиск (не `fallback_unicode` ⭐️).

**by_tag** — индекс тег → список combo.id (composite) или index (single).

**Поля item:**

| Поле | Значение |
|------|----------|
| `usage_mode` | `combo_required` — только в связке; `combo_optional` — можно и одному; `solo` — самостоятельный акцент |
| `combo_group` | id **полной** сборки (`clover_full`), не части |
| `partial_combo` | id неполной части, если есть |
| `combo_role` | `left`, `right`, `r1c1`…`r2c2`, `stack_1`, `left_wing` |
| `connects` | куда стыкуется: `left`, `right`, `top`, `bottom` |
| `combo_with` | индексы соседей в той же сборке |

**Правила:**

1. `description` — русский, 1–2 предложения; для фрагментов укажи, с чем стыкуется.
2. `description_emoji` — только Unicode-эмодзи (3–8).
3. В `combos` — **готовые мотивы** (цветок, лиана, домик, крылья…), не дублируй один мотив дважды.
4. Длинные бордюры (8+ сегментов) — одна combo с `layout: "horizontal"` и `order`.
5. Крылья/рамки — часто **сэндвич**: левое крыло + текст + правое крыло.
7. Большие объекты 2×2 / 2×3 — только `layout: grid` + `rows`, не одна горизонтальная линия.
8. Блики — всегда `solo`, не склеивать в «гирлянду-объект».
9. Fallback Unicode у таких паков часто одинаковый (⭐️) — опирайся на **картинку**.

Сохраните в `output/<pack>/labels_by_index.json`, затем:

```powershell
python generate_juliet_labels.py
python merge_labels.py --pack juliet_diary_lesnaya_tropa_2_by_TgEmojiBot
python validate_map.py --pack juliet_diary_lesnaya_tropa_2_by_TgEmojiBot
```
