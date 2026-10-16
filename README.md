# SALIM AI V5.0

Flask AI assistant for browser, Render, and local Termux. Features: Gemini integration with useful errors; recent chat context saved in SQLite; browser speech input/output where supported; task list create/complete/delete; health diagnostics; mobile responsive animated radar HUD.

## Render deployment
1. Push these files to the GitHub repository's main branch.
2. Open the existing `salim-ai-dashboard` service in Render.
3. Set `GEMINI_API_KEY` in Environment to a Google AI Studio key. Set `GEMINI_MODEL` to a model available to your project (default `gemini-2.5-flash`).
4. Deploy latest commit and test `/health`.

SQLite on Render may not persist through restarts/redeploys without a persistent disk; set `SALIM_AI_DB` to a path on that disk for persistent data. This starter has no login/authentication; do not store sensitive data in a publicly exposed instance. Never commit `.env` or API keys. Gemini quotas/limits apply.

## Termux
```bash
pkg update && pkg install python
# Extract ZIP, then cd into SALIM-AI-V5.0-COMPLETE
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env
# Add your actual GEMINI_API_KEY, save, then:
python webapp.py
```
Open `http://127.0.0.1:8080`.

## API endpoints
`GET /health`; `POST /api/chat` JSON `{"message":"Sannu"}`; `GET /api/history`; `DELETE /api/history`; `GET /api/tasks`; `POST /api/tasks` JSON `{"title":"Aiki"}`; `PATCH /api/tasks/<id>` JSON `{"completed":true}`; `DELETE /api/tasks/<id>`.

Voice depends on browser support and microphone permissions. Tasks are a saved list, not scheduled background jobs or push notifications. Phone app links do not allow the browser to control arbitrary apps.
