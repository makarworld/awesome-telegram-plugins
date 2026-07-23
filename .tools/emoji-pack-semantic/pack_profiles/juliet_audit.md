# Vision-аудит: juliet_diary_lesnaya_tropa_2_by_TgEmojiBot

Сетка **8×25** (`pack_sheet.png` с `--cols 8`), `#001`–`#200`. Строка на щите = горизонтальный ряд в чате — видно, что с чем склеено. Эталон для semantic_map v2.

## Ключевые зоны

| id / индексы | Тип | rows / order | complete | sandwich | visual_short |
|---|---|---|---|---|---|
| vine_border_top | horizontal | 1–8 | true | — | зелёная лиана с белыми цветами |
| fairy_flying | solo | 9 | true | — | летящая фея |
| mushroom_house | solo | 10 | true | — | грибной домик |
| pink_flower_1 | horizontal | 12–13 | true | do_not_insert_text | розовый цветок две половинки |
| moth_wings | sandwich | 49, 50 | true | allows_text_between | белые крылья мотылька |
| butterfly_wings_1 | horizontal | 55–56 | true | do_not_insert_text | крылья бабочки (стык, не рамка) |
| butterfly_wings_2 | horizontal | 73–74 | true | do_not_insert_text | крылья бабочки 2 |
| butterfly_wings_3 | horizontal | 189–190 | true | do_not_insert_text | крылья бабочки 3 |
| forest_table_scene | grid | [[105,106],[107,108],[109,110]] | true | — | письма, чашка, фея на олене |
| bonsai | grid | [[157,158],[165]] | true | — | бонсай: крона + горшок |
| deep_forest_panorama | grid | [[166,167,168,169,170,171,172,173,174],[175,176,177,178]] | true | — | тёмный мох + фиолетовые бутоны |
| clover_full | grid | [[179,180],[187,188]] | true | — | четырёхлистный клевер 2×2 |
| sparkle_* | solo | 35,47,75,96,112,132,186,199 | accent_only | — | блик-акцент, не объект |
| spacer_191/192 | spacer | 191, 192 | true | — | пустой отступ |

## Блики (не complete для коллажа)

`#047`, `#075`, `#112`, `#186`, `#199` (+ остальные sparkle_*) — solo-акценты, `max_per_message` 1–2, не склеивать в сцену.

## Исправления относительно v1

1. **flowers_165_178** → удалить; `#165` в **bonsai**, остальное → **deep_forest_panorama** (grid 2 ряда).
2. **bonsai** — `stack` → `grid` `[[157,158],[165]]`.
3. **Бабочки** `#55–56`, `#73–74`, `#189–190` — `horizontal` + `do_not_insert_text: true` (нет дыры под текст).
4. **Мотылёк** `#49–50` — оставить `sandwich` (широкие крылья, дыра под текст).
5. **vine_border_top** — `width_risk: high`, `alone_on_line: true`.
6. **forest_table_scene** — новая grid-сцена для `#105–110` (письма, чашка, фея+олень).
7. Мелкие solo в зоне `#83–95` — части поляны, `complete: false` где нужен parent.

## scenes[]

| id | blocks | описание |
|---|---|---|
| morning_path | vine_border_top, bonsai, thorn_border | Доброе утро: шапка-лиана, бонсай, нижний бордюр |
| forest_tea | vine_border_top, forest_table_scene, thorn_border | Чаепитие в лесу |
| text_frame | moth_wings, spacer_191 | Рамка с текстом между крыльями |

## Подбор для CuteMessages (`plugin_premium_picks.json`)

| Режим | Juliet combos | Почему |
|---|---|---|
| **replace** (все темы) | sparkle #035, fairy #009, daisy #016, mushroom #010 | Компактные solo, есть unicode-fallback |
| **decoration** (все темы) | pink_flower, бабочки #055–056/#073–074/#189–190, цветы, грибы, bonsai, clover, heart_apple, fairy_hat, child_in_flowers | complete, width_risk low, ≤2–4 в ряд |
| **nature only** | vine_border #001–008, forest_table, deep_forest, thorn_border | широкие сцены и бордюры |
| **не в плагин** | moth_wings (sandwich), spacer_191/192 | нужен sandwich-layout / техотступ |

Щит **8 колонок** — строка #001–#008 = `vine_border_top` целиком.
