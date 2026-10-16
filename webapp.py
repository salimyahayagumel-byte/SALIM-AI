import os
from flask import Flask, jsonify, render_template, request
from ai_client import generate_reply, AIConfigurationError, AIProviderError
app = Flask(__name__)
@app.get("/")
def index(): return render_template("index.html")
@app.get("/health")
def health(): return jsonify(service="SALIM AI", status="healthy", version="4.1.0", ai_configured=bool(os.getenv("OPENAI_API_KEY","").strip()))
@app.post("/api/chat")
def chat():
    data=request.get_json(silent=True) or {}
    message=str(data.get("message","")).strip()
    if not message: return jsonify(error="Rubuta tambaya tukuna."),400
    if len(message)>12000: return jsonify(error="Tambayar ta yi tsawo sosai."),413
    history=data.get("history",[])
    if not isinstance(history,list): history=[]
    history=[{"role":x["role"],"content":str(x.get("content",""))[:4000]} for x in history[-12:] if isinstance(x,dict) and x.get("role") in ("user","assistant")]
    try: return jsonify(reply=generate_reply(message,history))
    except AIConfigurationError as e: return jsonify(error=str(e),code="missing_api_key"),503
    except AIProviderError as e: return jsonify(error=str(e),code="ai_provider_error"),502
    except Exception:
        app.logger.exception("Unexpected chat error")
        return jsonify(error="An samu matsala wajen amsa. Ka sake gwadawa."),500
if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.getenv("PORT","10000")))
