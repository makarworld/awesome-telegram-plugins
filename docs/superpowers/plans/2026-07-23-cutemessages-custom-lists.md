# CuteMessages Custom Lists — Implementation Plan

> **For agentic workers:** Use executing-plans. Checkbox steps for tracking.

**Goal:** Editable decoration lists in CuteMessages settings (draft for 1.8.0, no release).

**Architecture:** JSON settings + shared list editor UI; transforms read via helpers; empty list disables that effect.

**Tech Stack:** exteraGram plugin Python (`ui.settings`), existing chat-list UI pattern.

## Global Constraints

- Edit `CuteMessages/cutemessagesenhanced.plugin` only (+ README/docs.md)
- Do not touch `releases/` or Pluggy
- Empty custom list ≠ fallback to defaults
- Borders add format: `left|right`

---

### Task 1: Helpers + wire transforms

**Files:**
- Modify: `CuteMessages/cutemessagesenhanced.plugin`

- [ ] Add `_CUSTOM_LIST_KEYS`, `_get_string_list`, `_set_string_list`, `_get_border_list`, `_set_border_list`, `_active_*` accessors, theme emoji overlay
- [ ] Guard all `random.choice` on these lists for empty
- [ ] Replace direct `self.emojis` / kaomoji / sparkles / uwu / borders / punctuation / exclamations / cute_actions usages in `apply_cute_transformations` and `_transform_exclamations`

### Task 2: Settings UI + i18n + presets

- [ ] Locale keys ru/en for hub, editors, empty, reset, border hint, preset toggle
- [ ] `_settings_custom_lists_hub`, `_build_string_list_editor`, `_build_border_list_editor`, nested theme/actions pages
- [ ] Link from `_settings_styles_hub`
- [ ] Export strips `custom_*` unless `include_custom_lists_export`

### Task 3: Docs + deliver plugin file

- [ ] Update `CuteMessages/docs.md` and `README.md`
- [ ] Deliver `.plugin` via send_document (no releases/)
