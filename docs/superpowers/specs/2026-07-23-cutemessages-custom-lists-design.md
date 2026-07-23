# CuteMessages — editable decoration lists (v1.8.0 draft)

## Goal

Allow users to view/add/remove/reset decoration pools used by classic cute transforms: emojis, kaomoji, sparkles, uwu suffixes, theme emojis, text borders, period/question replacements, extended exclamations, cute actions (ru/en).

## Decisions

1. UI: hybrid list editor (tap to remove + add field + reset to defaults)
2. Empty custom list = that effect adds nothing (no silent fallback to defaults)
3. Missing/invalid setting = built-in defaults
4. Presets: optional via `include_custom_lists_export` (like chat lists)
5. No release packaging; iterate on root `.plugin` only

## Storage

JSON string settings. Defaults stay as in-code lists on `PicMePlugin`.

| Key | Shape |
|-----|--------|
| `custom_emojis` | `string[]` |
| `custom_kaomojis` | `string[]` |
| `custom_sparkles` | `string[]` |
| `custom_uwu_suffixes` | `string[]` |
| `custom_theme_pastel_emojis` | `string[]` |
| `custom_theme_magical_emojis` | `string[]` |
| `custom_theme_nature_emojis` | `string[]` |
| `custom_text_borders` | `[left, right][]` |
| `custom_period_replacements` | `string[]` |
| `custom_question_replacements` | `string[]` |
| `custom_exclamations` | `string[]` |
| `custom_cute_actions_ru` | `string[]` |
| `custom_cute_actions_en` | `string[]` |
| `include_custom_lists_export` | bool |

Draft input key: `custom_list_draft` (cleared after successful add).

## UI

Styles hub → «Custom lists» hub → per-group editors (themes and cute actions nested).

Editor: Header, Input draft, Add action, items (tap remove), empty hint, Reset (red).

Borders add format: `left|right`.

## Runtime

All transform paths read via helpers (`_get_string_list` / `_get_border_list` / theme overlay). Never mutate default lists in place.

## Out of scope

Theme words/prefix/suffix editing, premium custom-emoji packs, release folder / Pluggy.
