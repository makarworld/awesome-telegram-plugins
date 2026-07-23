# Правила для агента (composite emoji packs) — v2

Вставьте в system prompt или rule при использовании `semantic_map.json` с `pack_type: composite`.

1. Одна combo с `complete: true` = один блок (свои строки); следующая complete — после пустой строки.
2. Запрещено в одной строке: combo+spacer+combo, solo+solo, коллаж из готовых картинок.
3. Spacer только между блоками / поля grid — не между чужими complete в ряд.
4. Несколько complete в одном сообщении — только по `scenes[]` (готовые рецепты).
5. Бери только готовые `combos[]` с `"complete": true`. Не собирай сам из соседних `index`.
6. `layout=solo` — один `document_id`; `glue=false`; не цепочка.
7. `layout=horizontal` — `order` в одну строку без пробелов; `do_not_insert_text: true` → без текста между кусками.
8. `layout=sandwich` — `left_wing` + текст + `right_wing`; только при `allows_text_between: true`.
9. `layout=grid` — `rows` построчно: в строке join без пробелов, между строками `\n`.
10. `layout=stack` — `order` сверху вниз через `\n`.
11. Если `complete=false` — неполный пазл; используй `parent` combo.
12. Число tg-emoji == числу id в combo/`rows`; нет `rows` — не выдумывай многострочность.
13. **Spacer** (`layout=spacer`, `spacers[]`) — пустые стикеры для отступов. Не декор.
14. Поиск по смыслу: `by_tag` + `hint_emoji` (не `fallback_unicode`).

**Контекст:** `agent_catalog.md` + `agent_index.json`, не весь `semantic_map.json`.
