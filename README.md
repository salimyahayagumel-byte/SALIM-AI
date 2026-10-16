# SALIM AI TERMINAL V4.0 — No AI API Key

This version uses browser speech recognition and speech synthesis with a local, rule-based response engine. It does not call Gemini, OpenAI, or any AI API.

## Features
- Microphone-first interface; no text input or Send button.
- Browser speech recognition (if supported by the browser).
- Browser text-to-speech for spoken replies (if supported).
- Built-in Hausa and English responses.
- Flask `/api/chat` local endpoint and `/health` health check.
- No AI API key environment variable required.

## Important limitations
This is not a full general-purpose AI model. It responds to a limited set of built-in patterns and returns an honest fallback for unknown questions. Browser speech recognition support and language quality vary. Some browsers use an internet-based speech recognition service even though this application itself does not use an AI API key. Speech synthesis may use installed device voices.

## Deploy to Render
1. Push this project to the `main` branch of your GitHub repository.
2. In Render, confirm the service is connected to branch `main` and automatic deploys are enabled.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn --workers 1 --threads 4 --timeout 120 webapp:app`
5. Health check path: `/health`
6. No AI API key is needed. Do not add Gemini/OpenAI keys for this version.

If an existing Render service is marked Blueprint managed, check the `render.yaml` configuration and sync/apply the Blueprint changes as appropriate.

## Run locally in Termux
```bash
pkg update
pkg install python
cd SALIM-AI-TERMINAL-V4.0-NO-API-KEY
python -m pip install -r requirements.txt
python webapp.py
```
Open `http://127.0.0.1:8080` in your browser. Browser microphone features generally require HTTPS or localhost.

## API test
```bash
curl http://127.0.0.1:8080/health
curl -X POST http://127.0.0.1:8080/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"Sannu SALIM AI","language":"ha"}'
```
