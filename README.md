# SALIM AI V4.1
Flask + OpenAI API chat, Hausa/English instructions, browser microphone support, and phone app shortcuts.

## Render setup
Open Render → salim-ai-dashboard → Environment. Add `OPENAI_API_KEY` with your own API key, save, and redeploy. Never put the key in GitHub, HTML, JavaScript, or a public chat. Check `/health` for `ai_configured: true`.

Default model is `gpt-4o-mini`; you may change `OPENAI_MODEL` to a model enabled for your API account. API use may incur charges, and account billing/credits must be active.

App links only request Android/browser to open an app; a web page cannot silently control arbitrary apps. Speech recognition depends on browser support and may use internet.
