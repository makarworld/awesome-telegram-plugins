"""Batch-generate labels_by_index.json + semantic_map.json for emoji packs."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from combo_schema import AGENT_RULES, SPACER_GUIDANCE
from item_builder import build_by_tag, build_items

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output"
PROFILES = ROOT / "pack_profiles"

EMOJI_HINTS: dict[str, tuple[str, list[str], str, str]] = {
    "⭐️": ("Декоративный элемент", ["декор", "звезда"], "✨⭐", "neutral"),
    "❤️": ("Символ любви и нежности", ["любовь", "сердце"], "❤️💕", "love"),
    "💖": ("Розовое сердце", ["любовь", "нежность"], "💖💗", "love"),
    "💕": ("Романтика", ["любовь", "романтика"], "💕❤️", "love"),
    "🌸": ("Цветочный акцент", ["цветы", "весна"], "🌸🌷", "wholesome"),
    "🌺": ("Яркий цветок", ["цветы", "лето"], "🌺🌼", "wholesome"),
    "🍓": ("Клубника", ["ягоды", "сладкое"], "🍓🍒", "playful"),
    "🎀": ("Бант", ["декор", "бант"], "🎀✨", "cute"),
    "✨": ("Блик или искра", ["блик", "декор"], "✨💫", "neutral"),
    "🦋": ("Бабочка", ["природа", "легкость"], "🦋🌿", "wholesome"),
    "🍎": ("Яблоко", ["фрукт", "осень"], "🍎🍂", "wholesome"),
    "🌿": ("Зелень", ["природа", "листья"], "🌿🍃", "wholesome"),
    "🐱": ("Котик", ["животные", "милое"], "🐱😺", "cute"),
    "😺": ("Милый кот", ["животные", "милое"], "😺🐾", "cute"),
    "💋": ("Поцелуй", ["флирт", "губы"], "💋💄", "flirty"),
    "🔥": ("Огонь, хайп", ["энергия", "хайп"], "🔥✨", "bold"),
    "💀": ("Череп, мем", ["мем", "ирония"], "💀😈", "edgy"),
    "😈": ("Дьявол", ["мем", "дерзость"], "😈🔥", "edgy"),
    "🎵": ("Музыка", ["музыка", "ритм"], "🎵🎶", "neutral"),
    "📎": ("Скрепка", ["канцелярия", "скрап"], "📎✂️", "neutral"),
    "✂️": ("Ножницы", ["инструмент", "скрап"], "✂️📎", "neutral"),
    "🦌": ("Олень", ["лес", "животные"], "🦌🌲", "wholesome"),
    "🍂": ("Осенняя листва", ["осень", "листья"], "🍂🍁", "nostalgic"),
    "🌲": ("Ель", ["лес", "зима"], "🌲❄️", "wholesome"),
    "🐦": ("Птица", ["природа", "небо"], "🐦🕊️", "wholesome"),
    "🕊️": ("Голубь", ["мир", "небо"], "🕊️☁️", "peaceful"),
    "☁️": ("Облако", ["небо", "мягкость"], "☁️🌤️", "calm"),
    "🌙": ("Луна", ["ночь", "сон"], "🌙✨", "dreamy"),
    "💤": ("Сон", ["сон", "усталость"], "💤😴", "sleepy"),
    "🍵": ("Чай", ["уют", "чай"], "🍵☕", "cozy"),
    "📖": ("Дневник", ["чтение", "ностальгия"], "📖✍️", "nostalgic"),
    "✍️": ("Письмо", ["текст", "записка"], "✍️📝", "neutral"),
    "🎠": ("Карусель", ["декор", "сказка"], "🎠✨", "whimsical"),
    "🫧": ("Пузыри", ["воздух", "легкость"], "🫧💧", "playful"),
    "💧": ("Капля", ["вода", "дождь"], "💧🌧️", "calm"),
    "🌧️": ("Дождь", ["погода", "грусть"], "🌧️☔", "melancholic"),
    "🍒": ("Вишня", ["ягоды", "лето"], "🍒🍓", "sweet"),
    "🌷": ("Тюльпан", ["цветы", "весна"], "🌷🌸", "wholesome"),
    "🌼": ("Ромашка", ["цветы", "лето"], "🌼🌻", "wholesome"),
    "🌻": ("Подсолнух", ["лето", "солнце"], "🌻☀️", "bright"),
    "☀️": ("Солнце", ["свет", "день"], "☀️🌤️", "bright"),
    "🍑": ("Персик", ["фрукт", "нежность"], "🍑🍒", "sweet"),
    "🫐": ("Черника", ["ягоды", "лес"], "🫐🍇", "wholesome"),
    "🍇": ("Виноград", ["фрукт", "богема"], "🍇🍷", "elegant"),
    "🍷": ("Вино", ["напиток", "вечер"], "🍷🕯️", "elegant"),
    "🕯️": ("Свеча", ["уют", "вечер"], "🕯️✨", "cozy"),
    "🧸": ("Мягкая игрушка", ["уют", "детство"], "🧸💕", "cute"),
    "💌": ("Любовное письмо", ["романтика", "письмо"], "💌❤️", "love"),
    "🎧": ("Наушники", ["музыка", "медиа"], "🎧🎵", "neutral"),
    "▶️": ("Воспроизведение", ["медиа", "плеер"], "▶️⏯️", "neutral"),
    "⏯️": ("Пауза/плей", ["медиа", "плеер"], "⏯️🎧", "neutral"),
    "⏮️": ("Предыдущий трек", ["медиа", "плеер"], "⏮️🎵", "neutral"),
    "⏭️": ("Следующий трек", ["медиа", "плеер"], "⏭️🎵", "neutral"),
    "🔤": ("Буква или текст", ["текст", "алфавит"], "🔤✍️", "neutral"),
    "🅰️": ("Буква A", ["текст", "алфавит"], "🅰️🔤", "neutral"),
    "🅱️": ("Буква B", ["текст", "алфавит"], "🅱️🔤", "neutral"),
    "🆎": ("Буква AB", ["текст", "алфавит"], "🆎🔤", "neutral"),
    "🅾️": ("Буква O", ["текст", "алфавит"], "🅾️🔤", "neutral"),
    "🆑": ("Буква CL", ["текст", "алфавит"], "🆑🔤", "neutral"),
    "🆒": ("Cool-текст", ["текст", "стиль"], "🆒✨", "cool"),
    "🆓": ("Free-текст", ["текст", "свобода"], "🆓🕊️", "free"),
    "ℹ️": ("Инфо-текст", ["текст", "подпись"], "ℹ️📝", "neutral"),
    "🆕": ("New-текст", ["текст", "новое"], "🆕✨", "neutral"),
    "🆙": ("Up-текст", ["текст", "рост"], "🆙⬆️", "neutral"),
    "🆗": ("OK-текст", ["текст", "согласие"], "🆗👌", "neutral"),
    "🆘": ("SOS-текст", ["текст", "срочно"], "🆘‼️", "urgent"),
    "🆚": ("VS-текст", ["текст", "сравнение"], "🆚⚔️", "neutral"),
    "🈁": ("Японский текст", ["текст", "азия"], "🈁✨", "neutral"),
    "🈂️": ("Японский текст", ["текст", "азия"], "🈂️✨", "neutral"),
    "🈷️": ("Месяц-текст", ["текст", "календарь"], "🈷️📅", "neutral"),
    "🈶": ("Есть-текст", ["текст", "азия"], "🈶✨", "neutral"),
    "🈯": ("Палец-текст", ["текст", "азия"], "🈯👆", "neutral"),
    "🉐": ("Выгода-текст", ["текст", "азия"], "🉐💰", "neutral"),
    "🈹": ("Скидка-текст", ["текст", "азия"], "🈹🏷️", "neutral"),
    "🈚": ("Нет-текст", ["текст", "азия"], "🈚🚫", "neutral"),
    "🈲": ("Запрет-текст", ["текст", "азия"], "🈲⛔", "neutral"),
    "🉑": ("Можно-текст", ["текст", "азия"], "🉑✅", "neutral"),
    "🈸": ("Заявка-текст", ["текст", "азия"], "🈸📝", "neutral"),
    "🈴": ("Проход-текст", ["текст", "азия"], "🈴✅", "neutral"),
    "🈳": ("Пусто-текст", ["текст", "азия"], "🈳⬜", "neutral"),
    "㊗️": ("Поздравление", ["текст", "праздник"], "㊗️🎉", "festive"),
    "㊙️": ("Секрет", ["текст", "тайна"], "㊙️🤫", "mysterious"),
    "🈺": ("Открыто", ["текст", "бизнес"], "🈺🏪", "neutral"),
    "🈵": ("Полный", ["текст", "занято"], "🈵📦", "neutral"),
}


def h(
    cid: str,
    order: list[int],
    *,
    name: str = "",
    description: str = "",
    description_emoji: str = "✨",
    tags: list[str] | None = None,
    mood: str = "neutral",
    use_when: list[str] | None = None,
    **extra,
) -> dict:
    return {
        "id": cid,
        "layout": "horizontal",
        "order": order,
        "name": name or cid,
        "description": description or name or cid,
        "description_emoji": description_emoji,
        "tags": tags or ["декор"],
        "mood": mood,
        "use_when": use_when or ["декор сообщения"],
        "render": "inline",
        "complete": True,
        "glue": True,
        "do_not_insert_text": True,
        **extra,
    }


def g(
    cid: str,
    rows: list[list[int]],
    *,
    name: str = "",
    description: str = "",
    description_emoji: str = "✨",
    tags: list[str] | None = None,
    mood: str = "neutral",
    use_when: list[str] | None = None,
    **extra,
) -> dict:
    return {
        "id": cid,
        "layout": "grid",
        "rows": rows,
        "name": name or cid,
        "description": description or name or cid,
        "description_emoji": description_emoji,
        "tags": tags or ["декор"],
        "mood": mood,
        "use_when": use_when or ["декор сообщения"],
        "render": "block",
        "complete": True,
        "glue": True,
        **extra,
    }


def sp(idx: int, *, name: str = "spacer") -> dict:
    return {
        "id": f"spacer_{idx:03d}",
        "layout": "spacer",
        "order": [idx],
        "name": name,
        "description": "Пустой стикер-отступ для выравнивания композиции.",
        "description_emoji": "⬜",
        "tags": ["spacer", "отступ"],
        "mood": "neutral",
        "use_when": ["нужен отступ между крупными блоками"],
        "render": "inline",
        "complete": True,
        "glue": False,
    }


def solo(
    idx: int,
    *,
    cid: str,
    description: str,
    description_emoji: str = "✨",
    tags: list[str] | None = None,
    mood: str = "neutral",
    use_when: list[str] | None = None,
    glue: bool = False,
    do_not_mix_with: list[str] | None = None,
) -> dict:
    d: dict = {
        "id": cid,
        "layout": "solo",
        "order": [idx],
        "name": cid,
        "description": description,
        "description_emoji": description_emoji,
        "tags": tags or ["декор"],
        "mood": mood,
        "use_when": use_when or ["акцент"],
        "render": "inline",
        "complete": True,
        "glue": glue,
    }
    if do_not_mix_with:
        d["do_not_mix_with"] = do_not_mix_with
    return d


def label_from_unicode(emoji: str, theme: str) -> tuple[str, list[str], str, str]:
    if emoji in EMOJI_HINTS:
        desc, tags, de, mood = EMOJI_HINTS[emoji]
        return f"{desc} ({theme})", tags + [theme], de, mood
    return (
        f"Элемент пака «{theme}»",
        ["декор", theme],
        emoji if emoji else "✨",
        "neutral",
    )


def enrich_from_raw(items: list[dict], raw_path: Path, theme: str) -> None:
    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    stickers = raw.get("stickers") or raw.get("result", {}).get("stickers", [])
    by_idx = {s["index"]: s for s in stickers if "index" in s}
    for item in items:
        st = by_idx.get(item["index"])
        if not st:
            continue
        if item.get("usage_mode") not in ("combo_optional", "solo") and item.get("combo_group"):
            continue
        emoji = (st.get("emoji") or "").strip()
        if not emoji or emoji == "⭐️" and item.get("combo_group"):
            continue
        desc, tags, de, mood = label_from_unicode(emoji, theme)
        item["description"] = desc
        item["description_emoji"] = de
        item["hint_emoji"] = de
        item["mood"] = mood
        item["tags"] = list(dict.fromkeys(tags + item.get("tags", [])))


def write_labels(pack: str, data: dict) -> Path:
    out = OUTPUT / pack / "labels_by_index.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def run_merge(pack: str) -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "merge_labels.py"), "--pack", pack],
        cwd=ROOT,
        check=True,
    )


def process_pack(pack: str, profile: dict) -> None:
    raw_path = OUTPUT / pack / "pack_raw.json"
    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    count = len(raw.get("stickers") or raw.get("result", {}).get("stickers", []))
    theme = profile.get("theme", pack)
    pack_type = profile.get("pack_type", "single")
    combos_raw = profile.get("combos", [])
    items, combos = build_items(
        count,
        combos_raw,
        theme=theme,
        pack_type=pack_type,
        fallback_tags=profile.get("fallback_tags"),
    )
    enrich_from_raw(items, raw_path, theme)

    spacer_idxs = [i for c in combos if c.get("layout") == "spacer" for i in c["order"]]
    spacers = []
    stickers = raw.get("stickers") or raw.get("result", {}).get("stickers", [])
    by_idx = {s["index"]: s for s in stickers}
    for si in spacer_idxs:
        st = by_idx.get(si, {})
        spacers.append({"index": si, "document_id": st.get("document_id", "")})

    data = {
        "pack": pack,
        "pack_type": pack_type,
        "theme": theme,
        "count": count,
        "items": items,
        "combos": combos,
        "by_tag": build_by_tag(items, combos, pack_type=pack_type),
    }
    if profile.get("scenes"):
        data["scenes"] = profile["scenes"]
    if pack_type == "composite":
        data["agent_rules"] = AGENT_RULES
        data["spacer_guide"] = SPACER_GUIDANCE
        if spacers:
            data["spacers"] = spacers

    write_labels(pack, data)
    run_merge(pack)
    print(f"OK {pack}: {count} items, {len(combos)} combos")


def main() -> None:
    packs = sys.argv[1:] if len(sys.argv) > 1 else None
    for path in sorted(PROFILES.glob("*.json")):
        if packs and path.stem not in packs:
            continue
        profile = json.loads(path.read_text(encoding="utf-8"))
        process_pack(path.stem, profile)


if __name__ == "__main__":
    main()
