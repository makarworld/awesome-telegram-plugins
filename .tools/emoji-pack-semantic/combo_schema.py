"""Нормализация combo-метаданных для semantic_map v2."""

from __future__ import annotations

from copy import deepcopy

LAYOUTS = frozenset({"solo", "horizontal", "sandwich", "grid", "stack", "spacer"})

MOODS = frozenset({
    "love", "neutral", "happy", "wholesome", "sad", "playful", "cute", "flirty",
    "bold", "edgy", "nostalgic", "peaceful", "calm", "dreamy", "sleepy", "cozy",
    "magical", "wild", "romantic", "melancholic", "bright", "sweet", "elegant",
    "festive", "mysterious", "urgent", "cool", "free", "whimsical",
})

RENDER_BY_LAYOUT = {
    "solo": "single",
    "horizontal": "join_no_space",
    "sandwich": "sandwich_text_middle",
    "grid": "rows_join_newline",
    "stack": "join_newline",
    "spacer": "padding",
}

GLUE_BY_LAYOUT = {
    "solo": False,
    "horizontal": "horizontal",
    "sandwich": False,
    "grid": "none",
    "stack": "vertical",
    "spacer": False,
}

AGENT_RULES = [
    "Одна combo с complete=true = один блок (свои строки); следующая complete — после пустой строки.",
    "Запрещено в одной строке: combo+spacer+combo, solo+solo, коллаж из готовых картинок.",
    "Spacer только между блоками / поля grid — не между чужими complete в ряд.",
    "Несколько complete в одном сообщении — только по scenes[] (готовые рецепты).",
    "Бери только готовые combos[] с complete=true; не собирай сам из соседних index.",
    "layout=solo → один document_id; glue=false; не цепочка.",
    "layout=horizontal → order в одну строку без пробелов; do_not_insert_text=true → без текста между кусками.",
    "layout=sandwich → left_wing + текст + right_wing; только при allows_text_between=true.",
    "layout=grid → rows построчно: в строке join без пробелов, между строками \\n.",
    "layout=stack → order сверху вниз через \\n.",
    "Если complete=false — не используй как готовый объект; нужен parent.",
    "Число emoji == числу id в combo/rows; нет rows — не выдумывай многострочность.",
    "layout=spacer — пустой стикер для отступа; не декор, не в rows combo.",
]

SPACER_GUIDANCE = {
    "description": "Пустые/прозрачные стикеры — только вёрстка, не смысл и не часть рисунка.",
    "usage": [
        "Отступ между двумя complete combo в строке (1–3 spacer).",
        "Поля слева/справа от grid/horizontal, чтобы не прилипало к краям чата.",
        "Зазор между stack-слоем и следующим блоком.",
        "Несколько spacer подряд = шире поле; можно чередовать #191 и #192.",
        "Не включать в rows/order декоративных combo.",
    ],
}

COMBO_EXTRA_KEYS = (
    "visual_short",
    "width_risk",
    "placement",
    "alone_on_line",
    "allow_adjacent_combos",
    "orphan_forbidden",
    "left_wing",
    "right_wing",
    "allows_text_between",
    "do_not_insert_text",
    "gap",
    "accent_only",
)


def _flat_indices(combo: dict) -> list[int]:
    if combo.get("rows"):
        out: list[int] = []
        for row in combo["rows"]:
            out.extend(int(i) for i in row)
        return out
    return [int(i) for i in combo.get("indices") or combo.get("order") or []]


def _width_risk(combo: dict) -> str:
    layout = combo.get("layout", "horizontal")
    if layout == "grid":
        rows = combo.get("rows") or []
        width = max((len(row) for row in rows), default=0)
    else:
        width = len(combo.get("order") or combo.get("indices") or [])
    if width >= 9:
        return "high"
    if width >= 5:
        return "medium"
    return "low"


def _normalize_sandwich(c: dict) -> None:
    order = [int(i) for i in c.get("order") or c.get("indices") or []]
    if len(order) < 2:
        raise ValueError(f"combo {c.get('id')}: sandwich needs 2+ indices")
    if not c.get("allows_text_between"):
        c["layout"] = "horizontal"
        c["do_not_insert_text"] = True
        c.setdefault("render", RENDER_BY_LAYOUT["horizontal"])
        c.setdefault("glue", GLUE_BY_LAYOUT["horizontal"])
        return
    c["left_wing"] = int(c.get("left_wing", order[0]))
    c["right_wing"] = int(c.get("right_wing", order[-1]))
    c["order"] = [c["left_wing"], c["right_wing"]]
    c["indices"] = list(c["order"])
    c.setdefault("gap", "wide")


def _normalize_horizontal(c: dict) -> None:
    if c.get("do_not_insert_text") is None and not c.get("allows_text_between"):
        c["do_not_insert_text"] = True


def _apply_complete_defaults(c: dict) -> None:
    complete = c.get("complete", True)
    if complete:
        c.setdefault("placement", "block")
        c.setdefault("alone_on_line", True)
        c.setdefault("allow_adjacent_combos", False)
    else:
        c.setdefault("orphan_forbidden", True)


def normalize_combo(combo: dict) -> dict:
    c = deepcopy(combo)
    layout = c.get("layout", "horizontal")
    if layout not in LAYOUTS:
        raise ValueError(f"Unknown layout {layout!r} in combo {c.get('id')}")

    if layout == "grid":
        rows = c.get("rows")
        if not rows:
            raise ValueError(f"combo {c.get('id')}: grid requires rows")
        c["rows"] = [[int(i) for i in row] for row in rows]
        c["indices"] = _flat_indices(c)
    else:
        if "indices" not in c and "order" in c:
            c["indices"] = [int(i) for i in c["order"]]
        elif "indices" in c:
            c["indices"] = [int(i) for i in c["indices"]]

    if "order" not in c and layout in ("horizontal", "sandwich", "stack"):
        c["order"] = list(c["indices"])

    if layout == "sandwich":
        _normalize_sandwich(c)
        layout = c["layout"]
    elif layout == "horizontal":
        _normalize_horizontal(c)

    c.setdefault("render", RENDER_BY_LAYOUT[layout])
    c.setdefault("glue", GLUE_BY_LAYOUT[layout])
    c.setdefault("complete", layout == "solo" or c.get("complete", True))

    if layout == "spacer":
        c.setdefault("item_type", "spacer")
        c.setdefault("max_per_message", 8)
        c.setdefault("complete", True)
        c.setdefault("do_not_mix_with", [])
    elif layout == "solo":
        c.setdefault("max_per_message", 1)
        if "do_not_mix_with" not in combo:
            if str(c.get("id", "")).startswith("sparkle_"):
                c["do_not_mix_with"] = ["sparkle_*"]
                c.setdefault("accent_only", True)
                c.setdefault("max_per_message", 2)
            else:
                c["do_not_mix_with"] = []

    _apply_complete_defaults(c)
    c.setdefault("width_risk", _width_risk(c))
    if c.get("complete") and c["width_risk"] == "high":
        c.setdefault("alone_on_line", True)

    mood = c.get("mood")
    if mood and mood not in MOODS:
        c["mood"] = "neutral"

    return c


def normalize_combos(combos: list[dict]) -> list[dict]:
    return [normalize_combo(c) for c in combos]


def index_to_primary_combo(combos: list[dict]) -> dict[int, dict]:
    """Индекс → combo с наивысшим приоритетом (parent grid > part > horizontal)."""
    ranked: list[tuple[int, dict]] = []
    for combo in combos:
        priority = 0
        if combo.get("layout") == "spacer":
            priority = 35
        elif combo.get("layout") == "grid" and combo.get("complete"):
            priority = 30
        elif combo.get("parent"):
            priority = 10
        elif combo.get("complete") is False:
            priority = 5
        elif combo.get("layout") == "solo":
            priority = 20
        else:
            priority = 15
        for idx in _flat_indices(combo):
            ranked.append((priority, combo))
    ranked.sort(key=lambda x: x[0], reverse=True)
    out: dict[int, dict] = {}
    for _, combo in ranked:
        for idx in _flat_indices(combo):
            if idx not in out:
                out[idx] = combo
    return out


def grid_role(idx: int, rows: list[list[int]]) -> str:
    for r, row in enumerate(rows, start=1):
        for c, i in enumerate(row, start=1):
            if int(i) == int(idx):
                return f"r{r}c{c}"
    return "cell"


def connects_for(combo: dict, idx: int) -> list[str]:
    layout = combo["layout"]
    if layout in ("solo", "spacer"):
        return []
    if layout == "grid":
        rows = combo["rows"]
        for r, row in enumerate(rows):
            if idx not in row:
                continue
            c = row.index(idx)
            dirs = []
            if c > 0:
                dirs.append("left")
            if c < len(row) - 1:
                dirs.append("right")
            if r > 0:
                dirs.append("top")
            if r < len(rows) - 1:
                dirs.append("bottom")
            return dirs
        return []
    if layout == "sandwich":
        order = combo["order"]
        pos = order.index(idx)
        return ["right"] if pos == 0 else ["left"]
    if layout == "stack":
        order = combo["order"]
        pos = order.index(idx)
        dirs = []
        if pos > 0:
            dirs.append("top")
        if pos < len(order) - 1:
            dirs.append("bottom")
        return dirs
    order = combo["order"]
    pos = order.index(idx)
    dirs = []
    if pos > 0:
        dirs.append("left")
    if pos < len(order) - 1:
        dirs.append("right")
    return dirs
