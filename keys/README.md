# 🔑 Ключи подписи manifest

🔐 Публичный ключ для проверки `plugin-integrity.json` в плагине LiveWallpaper.

| Файл | В репозитории | Назначение |
|------|---------------|------------|
| `manifest_public.pem` | ✅ да | 🔓 Верификация в `.plugin` (`MANIFEST_PUBLIC_KEY_PEM`) |
| `manifest_private.pem` | ❌ **нет** (`.gitignore`) | 🔒 Подпись в CI |

## ⚙️ GitHub Secret

**Settings → Secrets and variables → Actions → `MANIFEST_SIGNING_KEY`**

Полное содержимое `manifest_private.pem` (включая `-----BEGIN/END-----`).

При первой настройке сгенерируй пару:

```bash
openssl genrsa -out keys/manifest_private.pem 2048
openssl rsa -in keys/manifest_private.pem -pubout -out keys/manifest_public.pem
```

📋 Скопируй private в Secret, обнови public в репозитории и в `live_wallpaper.plugin`.
