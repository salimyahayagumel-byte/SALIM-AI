import os
import requests

class AIConfigurationError(Exception):
    pass

class AIProviderError(Exception):
    pass

def generate_reply(message, history=None):
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise AIConfigurationError(
            "Ba a saita GEMINI_API_KEY a Render ba. Je Render → salim-ai-dashboard → Environment, "
            "ƙara GEMINI_API_KEY daga Google AI Studio, sannan ka yi redeploy. Kada ka saka key a GitHub."
        )

    model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip() or "gemini-3.8-flash"
    contents = []
    for item in (history or [])[-12:]:
        role = item.get("role")
        content = item.get("content")
        if role in ("user", "assistant") and isinstance(content, str) and content.strip():
            contents.append({
                "role": "user" if role == "user" else "model",
                "parts": [{"text": content[:4000]}]
            })
    contents.append({"role": "user", "parts": [{"text": message}]})

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    try:
        response = requests.post(
            url,
            headers={"x-goog-api-key": api_key, "Content-Type": "application/json"},
            json={
                "systemInstruction": {
                    "parts": [{
                        "text": (
                            "You are SALIM AI, a helpful and honest assistant. Understand Hausa and English. "
                            "Normally reply in the language the user uses. Give clear, practical answers. "
                            "Never claim you opened or controlled a phone app unless the user actually did so. "
                            "Explain when an action requires Android permissions."
                        )
                    }]
                },
                "contents": contents,
                "generationConfig": {"temperature": 0.7, "maxOutputTokens": 2048}
            },
            timeout=(10, 75)
        )
    except requests.Timeout as exc:
        raise AIProviderError("Gemini ta ɗauki lokaci mai tsawo. Ka sake gwadawa.") from exc
    except requests.RequestException as exc:
        raise AIProviderError("Ba a iya haɗuwa da Gemini yanzu. Duba internet sannan ka sake gwadawa.") from exc

    if response.status_code in (401, 403):
        raise AIProviderError("Gemini API key ba daidai ba ne ko ba shi da izini. Duba GEMINI_API_KEY a Render.")
    if response.status_code == 429:
        raise AIProviderError("An kai iyakar amfani na Gemini ko quota. Ka duba AI Studio usage/limits sannan ka sake gwadawa daga baya.")
    if response.status_code >= 500:
        raise AIProviderError("Sabis ɗin Gemini yana da matsala na ɗan lokaci.")
    if not response.ok:
        try:
            detail = response.json().get("error", {}).get("message", "")
        except ValueError:
            detail = ""
        raise AIProviderError(("Gemini API ta ƙi buƙatar: " + detail[:250]) if detail else f"Gemini API status {response.status_code}.")

    try:
        data = response.json()
        parts = data["candidates"][0]["content"]["parts"]
        answer = "\n".join(p.get("text", "") for p in parts if isinstance(p, dict)).strip()
    except (ValueError, KeyError, IndexError, TypeError) as exc:
        raise AIProviderError("Gemini ba ta dawo da amsa a tsarin da ake tsammani ba.") from exc
    if not answer:
        raise AIProviderError("Gemini ba ta dawo da amsa ba. Ka sake gwadawa.")
    return answer
