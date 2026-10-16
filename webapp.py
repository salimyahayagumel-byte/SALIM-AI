"""SALIM AI TERMINAL — local-response, no AI API key required."""
import os
from flask import Flask, jsonify, render_template, request
from ai_client import local_reply

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/health")
def health():
    return jsonify({"service": "SALIM AI TERMINAL", "status": "healthy", "mode": "local-no-api-key"})

@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    language = str(data.get("language", "ha")).strip().lower()
    if not message:
        return jsonify({"ok": False, "reply": "Ban ji tambayarka ba. Ka sake magana.", "mode": "local"}), 400
    if len(message) > 2000:
        return jsonify({"ok": False, "reply": "Maganarka ta yi tsawo. Ka taƙaita ta, don Allah.", "mode": "local"}), 413
    reply = local_reply(message, language)
    return jsonify({"ok": True, "reply": reply, "mode": "local-no-api-key"})

@app.errorhandler(404)
def not_found(_error):
    return jsonify({"ok": False, "error": "Ba a sami wannan adireshin ba."}), 404

@app.errorhandler(500)
def server_error(_error):
    return jsonify({"ok": False, "error": "An samu matsalar cikin server."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port, debug=False)
