# SALIM AI V4.2 — Gemini API

- Gemini API powers the chat; default model is `gemini-3.8-flash`.
- Hausa and English responses.
- Browser microphone and Android/browser app shortcuts.
- Keep `GEMINI_API_KEY` in Render Environment only; never commit it to GitHub.
- Create a key at https://aistudio.google.com/apikey
- In Render → `salim-ai-dashboard` → Environment, add `GEMINI_API_KEY` with your own key, then redeploy.
- Free tier is subject to model availability, rate limits, quota and Google policies. Check AI Studio usage.
- App shortcuts can request app opening but cannot silently control all phone apps.
