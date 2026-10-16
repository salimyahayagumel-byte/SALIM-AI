import os, requests
class AIConfigurationError(Exception): pass
class AIProviderError(Exception): pass
def generate_reply(message,history=None):
    key=os.getenv("OPENAI_API_KEY","").strip()
    if not key: raise AIConfigurationError("Ba a saita OPENAI_API_KEY a Render ba. Je Environment, ƙara key ɗinka, sannan ka yi redeploy. Kada ka saka key a GitHub.")
    messages=[{"role":"system","content":"You are SALIM AI, a helpful, honest assistant. Understand Hausa and English, and normally reply in the language the user uses. Give clear, practical answers. Never claim to control phone apps unless the user actually opened them."}]
    for x in (history or [])[-12:]:
        if x.get("role") in ("user","assistant") and isinstance(x.get("content"),str) and x["content"].strip(): messages.append({"role":x["role"],"content":x["content"][:4000]})
    messages.append({"role":"user","content":message})
    try:
        r=requests.post("https://api.openai.com/v1/chat/completions",headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"},json={"model":os.getenv("OPENAI_MODEL","gpt-4o-mini"),"messages":messages,"temperature":0.7},timeout=(10,75))
    except requests.Timeout as e: raise AIProviderError("AI ta ɗauki lokaci mai tsawo. Ka sake gwadawa.") from e
    except requests.RequestException as e: raise AIProviderError("Ba a iya haɗuwa da AI yanzu. Duba internet.") from e
    if r.status_code in (401,403): raise AIProviderError("API key ba daidai ba ne ko ba shi da izini. Duba OPENAI_API_KEY.")
    if r.status_code==429: raise AIProviderError("An kai iyakar amfani ko babu credit. Duba billing/usage na API account.")
    if r.status_code>=500: raise AIProviderError("Sabis ɗin AI yana da matsala na ɗan lokaci.")
    if not r.ok:
        try: detail=r.json().get("error",{}).get("message","")
        except ValueError: detail=""
        raise AIProviderError(("AI API ta ƙi buƙatar: "+detail[:200]) if detail else f"AI API status {r.status_code}.")
    try: answer=r.json()["choices"][0]["message"]["content"].strip()
    except (ValueError,KeyError,IndexError,TypeError) as e: raise AIProviderError("Amsar AI ba ta zo yadda ake tsammani ba.") from e
    if not answer: raise AIProviderError("AI ba ta dawo da amsa ba.")
    return answer
