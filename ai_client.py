"""Google Gemini API client using only Python standard library."""
import json
import os
import urllib.request
import urllib.parse
import urllib.error

API_BASE = "https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent"

def ask_gemini(messages):
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key:
        return "Ba a saita GEMINI_API_KEY ba. Ka saka Gemini API key a cikin .env sannan ka sake kunna SALIM AI."

    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
    system_text = ""
    contents = []
    for item in messages:
        role = item.get("role", "user")
        content = item.get("content", "")
        if role == "system":
            system_text = str(content)
        elif role in ("user", "assistant"):
            contents.append({
                "role": "user" if role == "user" else "model",
                "parts": [{"text": str(content)}]
            })

    payload = {"contents": contents, "generationConfig": {"temperature": 0.4, "maxOutputTokens": 1200}}
    if system_text:
        payload["systemInstruction"] = {"parts": [{"text": system_text}]}
    url = API_BASE.format(model) + "?key=" + urllib.parse.quote(key, safe="")
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            data = json.loads(response.read().decode("utf-8"))
        candidates = data.get("candidates", [])
        if not candidates:
            return "Gemini bai dawo da amsa ba. Ka gwada sake tambaya ko duba iyakar amfani (quota)."
        parts = candidates[0].get("content", {}).get("parts", [])
        answer = "\n".join(part.get("text", "") for part in parts if part.get("text"))
        return answer.strip() or "Gemini bai dawo da rubutacciyar amsa ba."
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        return f"Gemini API ta dawo da kuskure ({exc.code}): {detail}"
    except Exception as exc:
        return f"Ba a iya haɗuwa da Gemini ba: {exc}"
